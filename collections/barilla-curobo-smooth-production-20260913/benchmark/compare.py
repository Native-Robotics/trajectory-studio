"""Verify same-source A/B evidence and compare compute, resources and motion."""
import json,hashlib,statistics,sys
from pathlib import Path
ROOT=Path('/home/luke/.codex/worktrees/tp-curobo-core');sys.path.insert(0,str(ROOT))
from snippets.benchmark_metrics import trajectory_metrics
BASE=Path('/home/luke/.codex/visualizations/2026/09/12/01a0969d-cc8b-77e1-8566-8b3bd1679634')
OUT=BASE/'curobo-continuous-production-benchmark-summary-20260913'
IDS=[3,4,21,54,59,69,95,118,119,133]

def read(p):return json.loads(p.read_text())
def summary(values):
    known=[v for v in values if v is not None]
    return statistics.median(known) if len(known)==len(values) else None

def main():
    OUT.mkdir(exist_ok=False);all_summaries=[]
    full=read(BASE/'curobo-continuous-production-full-20260913/manifest.json')
    for kind in ('fresh','warm'):
        dirs=[BASE/f'curobo-continuous-production-{mode}-{kind}10-20260913' for mode in ('control','enabled')]
        manifests=[read(p/'manifest.json') for p in dirs]
        expected=IDS if kind=='fresh' else [tid for tid in IDS for _ in range(2)]
        for enabled,(m,p) in enumerate(zip(manifests,dirs)):
            assert m['run_status']=='complete' and [r['task_id'] for r in m['rows']]==expected
            assert m['source_evidence']==full['source_evidence']
            assert all(hashlib.sha256((ROOT/n).read_bytes()).hexdigest()==h for n,h in m['source_evidence']['sha256_by_path'].items())
            assert m['config']['Planner']['CuRoboPlanner']['continuous_motion'] is bool(enabled)
            pid_sets=[set(r['child_pids']) for r in m['rows']]
            if kind=='warm':
                assert all(v==pid_sets[0] for v in pid_sets)
            else:
                assert all(not a.intersection(b) for i,a in enumerate(pid_sets) for b in pid_sets[i+1:])
            for r in m['rows']:
                assert r['status']=='SOLVED' and r['stats']['qualification']['constraints_valid'] and r['stats']['preacceptance_collision_valid']
                assert r['child_pids']
                assert all(a['capture_history_preserved'] and a['graph_randomness_isolated'] for part in r['stats']['parts'] for a in part['attempts'])
        configs=[json.loads(json.dumps(m['config'])) for m in manifests]
        for c in configs:c['Planner']['CuRoboPlanner'].pop('continuous_motion')
        assert configs[0]==configs[1], 'Unexpected A/B configuration difference'
        rows=[]
        for iteration,(control,enabled) in enumerate(zip(*(m['rows'] for m in manifests))):
            tid=control['task_id'];parts=[read(p/'tasks'/f'{iteration:03}-{tid:03}.result.json')['parts'] for p in dirs]
            measured=kind=='fresh' or iteration%2==1
            continuous=enabled['stats'].get('continuous_motion',{})
            metrics=[trajectory_metrics(v) for v in parts] if measured else None
            rows.append({'iteration':iteration,'task_id':tid,'included_in_summary':measured,'continuous_accepted':continuous.get('accepted',False),'reason':continuous.get('reason'),'exact_output_match':parts[0]==parts[1], 'control_elapsed_s':control['elapsed_s'],'enabled_elapsed_s':enabled['elapsed_s'],'additional_continuous_s':continuous.get('elapsed_s'), 'motion_control_enabled':metrics})
        selected=[m['rows'] if kind=='fresh' else m['rows'][1::2] for m in manifests]
        metrics={k:[summary([r[k] for r in rs]) for rs in selected] for k in ('elapsed_s','sampled_cpu_s','peak_summed_rss_mb','peak_gpu_compute_mb')}
        measured=[r for r in rows if r['included_in_summary']]
        quality={k:[summary([r['motion_control_enabled'][mode][k] for r in measured]) for mode in range(2)] for k in ('duration_s','rms_jerk_rad_s3','normalized_jerk','total_mileage_rad','peak_jerk_rad_s3')}
        item={'kind':kind,'requests_per_mode':len(expected),'measured_per_mode':10,'metrics_control_enabled':metrics,'motion_metrics_control_enabled':quality,'continuous_accepted_measured':sum(r['continuous_accepted'] for r in measured),'rows':rows,'scope':'One sequential same-source A/B trial on the historical fixed ten. Warm summaries use second requests. Resource samples every50ms; medians are observational, not confidence intervals. Motion quality metrics do not replace constraint checks.'}
        (OUT/f'{kind}.json').write_text(json.dumps(item,indent=2));all_summaries.append({k:v for k,v in item.items() if k!='rows'});print(json.dumps(all_summaries[-1],indent=2),flush=True)
    (OUT/'summary.json').write_text(json.dumps(all_summaries,indent=2));(OUT/'compare.py').write_bytes(Path(__file__).read_bytes())
if __name__=='__main__':main()
