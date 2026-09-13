"""Audit saved replay evidence and export fidelity; does not re-run validation."""
import hashlib
import json
import math
import numpy as np
from pathlib import Path

ROOT=Path('/home/luke/.codex/worktrees/tp-curobo-core')
BASE=Path('/home/luke/.codex/visualizations/2026/09/12/01a0969d-cc8b-77e1-8566-8b3bd1679634')
REPLAY=BASE/'curobo-continuous-production-full-20260913'
SOURCE=Path('/home/luke/git/trajectory-studio/collections/barilla-curobo-20260912/tasks')


def read(p):
    return json.loads(p.read_text())


def finite(value):
    if isinstance(value,list):
        return all(finite(v) for v in value)
    if isinstance(value,dict):
        return all(finite(v) for v in value.values())
    return not isinstance(value,(int,float)) or math.isfinite(value)


def main():
    m=read(REPLAY/'manifest.json')
    assert m['run_status']=='complete', 'Replay is not terminal'
    assert m['constraint_version']=='strict-original-v2-recorded-joint-caps'
    assert m['config']['Planner']['CuRoboPlanner']['linear_fast_path'] is True
    rows=m['rows']
    assert len(rows)==135 and {r['task_id'] for r in rows}==set(range(135))
    assert [r['iteration'] for r in rows]==list(range(135))
    hashes=m['source_evidence']['sha256_by_path']
    assert all(hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest for name,digest in hashes.items()), 'Source changed'
    index=read(REPLAY/'trajectories.json')
    assert len(index)==135 and {i['task_id'] for i in index}==set(range(135))
    byid={i['task_id']:i for i in index}
    part_count=0
    joint_cap_ratios=[]
    for r in rows:
        tid=r['task_id']
        assert r['status']=='SOLVED', (tid,r['status'])
        assert r['stats']['qualification']['constraints_valid'] is True, tid
        assert r['stats']['preacceptance_collision_valid'] is True, tid
        assert all(a['graph_randomness_isolated'] is True for part in r['stats']['parts'] for a in part['attempts']), tid
        assert all(a['capture_history_preserved'] is True for part in r['stats']['parts'] for a in part['attempts']), tid
        payload=read(REPLAY/'tasks'/f'{tid:03}.json')
        original=read(SOURCE/f'{tid:03}.json')
        # Joint enum deserialization normalizes spelling in the input mapping.
        original['equipment_model']['dh_parameters']['joint_type']=[name.upper() for name in original['equipment_model']['dh_parameters']['joint_type']]
        assert payload==original, tid
        result=read(REPLAY/'tasks'/f"{r['iteration']:03}-{tid:03}.result.json")
        assert {k:v for k,v in result.items() if k!='parts'}==r, tid
        item=byid[tid]
        prefix=REPLAY/'Trajectories'/'traj'/item['id']
        assert read(prefix.with_suffix('.repr'))==payload, tid
        export=read(prefix.with_suffix('.traj'))
        assert export['parts']==result['parts'] and export['planner_status']=='SOLVED', tid
        assert export['task_id']==tid and export['desired_id']==payload['desired_id'], tid
        assert len(export['parts'])==len(payload['parts'])==item['num_parts'], tid
        assert export['parts'] and finite(export['parts']), tid
        for part in export['parts']:
            coefficients=np.asarray(part['coeffs']); widths=np.diff(part['knots']); ratios={}
            for order,field in enumerate(('max_velocity','max_acceleration','max_jerk'),1):
                bounds=payload['equipment_model'].get(field)
                if bounds is None: continue
                assert len(bounds)==len(coefficients) and all(math.isfinite(b) and b>0 for b in bounds)
                peak=[]
                for joint in coefficients:
                    values=[]
                    for column,width in zip(joint.T,widths):
                        derivative=np.polyder(column,order)
                        roots=np.roots(np.polyder(derivative))
                        times=[0.,width,*[float(r.real) for r in roots if abs(r.imag)<1e-10 and 0<r.real<width]]
                        values.extend(np.abs(np.polyval(derivative,times)))
                    peak.append(max(values))
                ratios[field]=float(np.max(np.array(peak)/bounds))
                assert ratios[field]<=1+1e-6,(tid,field,ratios[field])
            joint_cap_ratios.append({'task_id':tid,'ratios':ratios})
            knots=part['knots']
            assert len(knots)>=2 and all(b>a for a,b in zip(knots,knots[1:])), tid
        part_count+=len(export['parts'])
    (REPLAY/'independent-recorded-joint-cap-audit.json').write_text(json.dumps(joint_cap_ratios,indent=2))
    summary={'tasks':135,'parts':part_count,'matching_source_files':len(hashes),'recorded_constraint_passes':135,'recorded_core_FCL_passes':135,'production_SOLVED':135,'payload_and_export_fidelity':True,'allowed_input_normalization':'DH joint_type enum names uppercased by deserialization; all other fields equal','scope':'Saved-evidence audit, not a new continuous-time or collision proof.'}
    summary['continuous_accepted'] = sum(r['stats'].get('continuous_motion',{}).get('accepted',False) for r in rows)
    summary['continuous_rejected'] = sum(not r['stats'].get('continuous_motion',{}).get('accepted',False) for r in rows)
    assert m['config']['Planner']['CuRoboPlanner']['continuous_motion'] is True
    for r in rows:
        c = r['stats']['continuous_motion']
        if c['accepted']:
            assert c['candidate_duration_s'] < c['baseline_duration_s']
            assert c['qualification']['constraints_valid']
            assert r['stats']['retiming_mode'] == 'continuous conic timing'
    (REPLAY/'evidence-audit.json').write_text(json.dumps(summary,indent=2))
    previous=BASE/'curobo-rnd-numeric-fk-full-20260913'
    motion_rows=[]
    for row in rows:
        name=f"{row['iteration']:03}-{row['task_id']:03}.result.json"
        old=read(previous/'tasks'/name)
        new=read(REPLAY/'tasks'/name)
        motion_rows.append({'task_id':row['task_id'],'parts_exactly_equal':old['parts']==new['parts']})
    (REPLAY/'motion-exact-comparison.json').write_text(json.dumps({'baseline':previous.name,'exact_matches':sum(r['parts_exactly_equal'] for r in motion_rows),'rows':motion_rows},indent=2))
    print(json.dumps(summary,indent=2))
    print('Exact trajectory matches:',sum(r['parts_exactly_equal'] for r in motion_rows))

if __name__=='__main__':
    main()
