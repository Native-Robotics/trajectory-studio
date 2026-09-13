"""Publish a guarded offline R&D comparison, with verified baseline fallback."""
import json
import hashlib
import shutil
import statistics
import html
from pathlib import Path
BASE=Path('/home/luke/.codex/visualizations/2026/09/12/01a0969d-cc8b-77e1-8566-8b3bd1679634')
ROOT=Path('/home/luke/.codex/worktrees/studio-barilla-rebuild')
RUN=BASE/'curobo-continuous-conic-full-20260913'
PAIRS=ROOT/'collections/barilla-curobo-reference-20260913'
OUT=ROOT/'collections/barilla-curobo-continuous-reference-20260913'

def read(path): return json.loads(path.read_text())

def main():
    results=read(RUN/'results.json'); audit=read(RUN/'exact-export-audit.json')
    assert len(results)==135 and audit['complete']
    by_task={r['task_id']:r for r in results}; checked={r['task_id']:r for r in audit['rows']}
    assert set(checked)=={r['task_id'] for r in results if r['valid']}
    for tid,r in checked.items():
        assert r['original_FCL_valid'] and r['qualification_1200hz']['constraints_valid']
        assert hashlib.sha256((RUN/f'{tid:03}.traj').read_bytes()).hexdigest()==r['sha256']
    shutil.copytree(PAIRS,OUT)
    rows=read(OUT/'trajectories.json'); comparison=[]
    for row in rows:
        if row['pair_role']!='curobo': continue
        tid=row['task_id']; trial=by_task[tid]; baseline=row['duration']
        accepted=trial['valid'] and trial['duration_s']<baseline-1e-6
        record={'task_id':tid,'id':row['id'],'baseline_duration_s':baseline,'candidate_duration_s':trial.get('duration_s'), 'candidate_valid':trial['valid'],'selected':'continuous' if accepted else 'baseline','reason':'Passed exact-export audit and shorter travel time' if accepted else trial.get('error','Candidate is not faster')}
        if accepted:
            path=OUT/'Trajectories/traj'/f"{row['id']}.traj"
            shutil.copy2(RUN/f'{tid:03}.traj',path)
            row['duration']=trial['duration_s'];row['planner_status']='QUALIFIED_OFFLINE_PROTOTYPE'
            row['reference_source']='cuRobo native path with offline continuous-motion post-processing'
            row['postprocess_s']=trial['elapsed_s'];row['timing_optimizer_s']=trial['timing']['optimizer_s']
        else:
            row['reference_source']='corrected cuRobo baseline retained: '+record['reason']
        # A mixed offline workflow has no measured end-to-end planning latency.
        row['baseline_compute_s']=row.pop('compute_s',None)
        row.pop('mileage_sum_rad',None)
        row['continuous_motion_selected']=accepted
        record['selected_duration_s']=row['duration']
        record['reduction_pct']=100*(1-row['duration']/baseline)
        comparison.append(record)
    assert len(comparison)==135 and all(r['selected_duration_s']<=r['baseline_duration_s']+1e-6 for r in comparison)
    summary={'tasks':135,'valid_candidates':len(checked),'selected_continuous':sum(r['selected']=='continuous' for r in comparison),'retained_baseline':sum(r['selected']=='baseline' for r in comparison),'median_all_task_reduction_pct':statistics.median(r['reduction_pct'] for r in comparison),'sum_baseline_s':sum(r['baseline_duration_s'] for r in comparison),'sum_selected_s':sum(r['selected_duration_s'] for r in comparison),'rows':comparison,'scope':'Offline R&D selection, not integrated production planning. Reference recordings are unchanged and do not all satisfy recorded TCP limits. No end-to-end compute speedup claim.'}
    (OUT/'comparison.json').write_text(json.dumps(summary,indent=2))
    (OUT/'trajectories.json').write_text(json.dumps(rows,indent=2))
    for name in ('results.json','exact-export-audit.json','provenance.json','continuous_motion_conic.py','conic_speed.py','verify_continuous_corpus.py'):
        shutil.copy2(RUN/name,OUT/name)
    # Keep local report navigation correct for this new, separate collection.
    page=(OUT/'index.html').read_text()
    start=page.index('id="sidebar-left"');pos=page.index('>',start)+1
    page=page[:pos]+'<p style="padding:8px 12px;color:#ffd276;font-size:12px">Offline smooth-motion R&amp;D · <a href="report.html">135-task comparison →</a></p>'+page[pos:]
    page=page.replace('cuRobo + Reference pairs · Trajectory Studio','Continuous cuRobo + reference · R&D')
    page=page.replace('href="corpus.html"','href="../../corpus.html"').replace('href="collections/','href="../')
    (OUT/'index.html').write_text(page)
    table=''.join(f'<tr><td><a href="index.html#{html.escape(r["id"])}">{r["task_id"]} · {r["id"][:8]}</a></td><td>{r["baseline_duration_s"]:.2f}</td><td>{r["selected_duration_s"]:.2f}</td><td>{r["reduction_pct"]:.1f}%</td><td>{html.escape(r["selected"])}</td><td>{html.escape(r["reason"])}</td></tr>' for r in comparison)
    doc=f'''<!doctype html><meta charset="utf-8"><title>Continuous cuRobo: 135-task R&amp;D</title><style>body{{font:17px/1.5 system-ui;max-width:1200px;margin:35px auto;padding:0 24px;background:#111723;color:#e7edf5}}a{{color:#55d4ed}}table{{border-collapse:collapse;width:100%}}td,th{{text-align:left;padding:8px;border-bottom:1px solid #364355}}.notice{{color:#ffd276}}</style><h1>Smoother motion, shorter travel</h1><p class="notice">Offline R&amp;D. Production integration remains in progress.</p><p><b>{summary['selected_continuous']} / 135 tasks use a faster, validated continuous-motion candidate.</b> The other {summary['retained_baseline']} retain the corrected cuRobo baseline. No selected trajectory is slower than that baseline.</p><p>Median travel-time reduction across all 135 tasks: <b>{summary['median_all_task_reduction_pct']:.1f}%</b>. Sum of individual travel times: {summary['sum_baseline_s']:.1f} → {summary['sum_selected_s']:.1f} s; this is not a scheduled production-cycle measurement.</p><p>All {len(checked)} valid candidate exports were reopened and checked: 1200 Hz Cartesian constraints, analytic joint velocity/acceleration/jerk extrema against recorded caps, position/velocity/acceleration continuity at joins, and original FCL collision checks. Cartesian and collision checks are sampled, not continuous-time proofs. Rejected and slower candidates were excluded.</p><p>For screenshot task 2: 7.56 → 6.32 s. Its 2.57 s reference exceeds recorded TCP limits (2 m/s, 1 m/s²): measured peaks are about 2.74 m/s and 9.62 m/s². Matching that reference time would not be a comparison under equal constraints.</p><p>Timing uses a conic speed-profile solve. These are CPU post-processing results from native cuRobo paths, not new integrated GPU runs. Compute fields are omitted because end-to-end planning latency for this combined workflow has not been measured.</p><p><a href="index.html#236e7d6c7f2343a27196c7806774659f42f95dbe607e08c39d807c06659060f3-curobo">Open screenshot trajectory with its -ref pair</a> · <a href="../barilla-shape-timing-task002-20260913/report.html">Detailed shape/dynamics charts</a> · <a href="comparison.json">All comparisons</a> · <a href="exact-export-audit.json">Exact-export audit</a></p><table><tr><th>Task</th><th>Baseline s</th><th>Selected s</th><th>Reduction</th><th>Selected</th><th>Reason</th></tr>{table}</table>'''
    (OUT/'report.html').write_text(doc)
    (OUT/'README.md').write_text('# Continuous-motion R&D comparison\n\n'+summary['scope']+'\n\nSee comparison.json, exact-export-audit.json and provenance.json. Each cuRobo entry is a validated faster offline candidate or the unchanged corrected baseline; each -ref is the original recording.\n')
    (OUT/'pairing.json').write_text(json.dumps({'count':135,'curobo_source':'offline continuous candidates with corrected baseline fallback','reference_source':'original recorded Barilla','selection':'exact-export valid and strictly faster only'},indent=2))
    print(json.dumps({k:v for k,v in summary.items() if k!='rows'},indent=2))
if __name__=='__main__': main()
