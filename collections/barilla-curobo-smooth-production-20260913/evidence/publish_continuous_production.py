"""Publish audited production-worker results and same-source benchmark evidence."""
import json,hashlib,shutil,html
from pathlib import Path
BASE=Path('/home/luke/.codex/visualizations/2026/09/12/01a0969d-cc8b-77e1-8566-8b3bd1679634')
ROOT=Path('/home/luke/.codex/worktrees/studio-barilla-rebuild');CORE=Path('/home/luke/.codex/worktrees/tp-curobo-core')
RUN=BASE/'curobo-continuous-production-full-20260913';BENCH=BASE/'curobo-continuous-production-benchmark-summary-20260913'
PAIRS=ROOT/'collections/barilla-curobo-reference-20260913';OUT=ROOT/'collections/barilla-curobo-continuous-production-20260913'
def read(p):return json.loads(p.read_text())
def main():
    manifest=read(RUN/'manifest.json');audit=read(RUN/'evidence-audit.json');exact=read(RUN/'exact-export-audit.json');motion=read(RUN/'motion-comparison.json');bench=read(BENCH/'summary.json')
    assert manifest['run_status']=='complete' and audit['production_SOLVED']==135
    assert exact['complete'] and exact['valid_exports']==135 and motion['complete'] and motion['tasks']==135
    assert len(bench)==2 and all(r['measured_per_mode']==10 for r in bench)
    assert all(hashlib.sha256((CORE/n).read_bytes()).hexdigest()==h for n,h in manifest['source_evidence']['sha256_by_path'].items())
    shutil.copytree(PAIRS,OUT)
    (OUT/"recorded-joint-limits-audit.json").unlink(missing_ok=True)
    rows=read(PAIRS/'trajectories.json');latest={r['task_id']:r for r in read(RUN/'trajectories.json')};run_rows={r['task_id']:r for r in manifest['rows']};checks={r['task_id']:r for r in exact['rows']}
    for i,row in enumerate(rows):
        if row['pair_role']=='ref':continue
        tid=row['task_id'];fresh=latest[tid];c=run_rows[tid]['stats']['continuous_motion']
        assert fresh['id']==row['id'] and fresh['desired_id']==row['pair_id']
        for suffix in ('.traj','.repr'):shutil.copy2(RUN/'Trajectories/traj'/(row['id']+suffix),OUT/'Trajectories/traj'/(row['id']+suffix))
        assert hashlib.sha256((OUT/'Trajectories/traj'/(row['id']+'.traj')).read_bytes()).hexdigest()==checks[tid]['sha256']
        rows[i]={**fresh,'pair_id':row['pair_id'],'pair_role':'curobo','box_number':row.get('box_number'),'place_pallet':row.get('place_pallet'),'continuous_motion_selected':c['accepted'],'continuous_motion_reason':c.get('reason'),'recorded_joint_jerk_valid':True,'reference_source':'production worker, continuous motion enabled; baseline fallback where needed','compute_source':'sequential full135 replay; benchmark comparison is separate'}
    (OUT/'trajectories.json').write_text(json.dumps(rows,indent=2))
    for name in ('manifest.json','evidence-audit.json','exact-export-audit.json','independent-recorded-joint-cap-audit.json','motion-comparison.json'):shutil.copy2(RUN/name,OUT/name)
    shutil.copytree(BENCH,OUT/'benchmark')
    page=(OUT/'index.html').read_text();pos=page.index('>',page.index('id="sidebar-left"'))+1
    page=page[:pos]+'<p style="padding:8px 12px;font-size:12px;color:#ffd276">Production worker replay · <a style="color:#55d4ed" href="report.html">Continuous-motion results →</a></p>'+page[pos:]
    page=page.replace('cuRobo + Reference pairs · Trajectory Studio','Production continuous cuRobo + reference · Studio')
    (OUT/'index.html').write_text(page)
    table=''.join(f'<tr><td><a href="index.html#{html.escape(r["id"])}">{r["task_id"]} · {r["id"][:8]}</a></td><td>{r["old_duration_s"]:.2f}</td><td>{r["new_duration_s"]:.2f}</td><td>{"continuous" if r["continuous_accepted"] else "baseline"}</td><td>{html.escape(r["reason"] or "Qualified faster candidate")}</td></tr>' for r in motion['rows'])
    benchmark_table=''
    for b in bench:
        for key,label in [('elapsed_s','request time (s)'),('sampled_cpu_s','CPU time (s)'),('peak_summed_rss_mb','peak summed RSS (MiB)'),('peak_gpu_compute_mb','GPU compute allocation (MiB)')]:
            a,z=b['metrics_control_enabled'][key];fmt=lambda x:'unavailable' if x is None else f'{x:.3f}'
            benchmark_table+=f'<tr><td>{b["kind"]}</td><td>{label}</td><td>{fmt(a)}</td><td>{fmt(z)}</td></tr>'
    report=f'''<!doctype html><meta charset="utf-8"><title>Production cuRobo continuous motion</title><style>body{{font:17px/1.5 system-ui;max-width:1200px;margin:35px auto;padding:0 24px;background:#111723;color:#e7edf5}}a{{color:#55d4ed}}table{{border-collapse:collapse;width:100%}}td,th{{text-align:left;padding:8px;border-bottom:1px solid #364355}}</style><h1>Continuous motion through the production worker</h1><p><b>135/135 tasks solved.</b> {motion['continuous_accepted']} accepted continuous candidates; {motion['baseline_retained']} retained their validated baseline. The option remains disabled by default. These are actual worker outputs from core 60eb607a, rather than the earlier offline selection.</p><p>All 135 exported splines were reopened: 1200 Hz Cartesian checks, analytic recorded joint caps, C2 joins and original FCL. The worker also performed its normal final validation. Cartesian/dynamic/collision checks are sampled, not continuous-time proofs.</p><p>Compared with the previous corrected replay: median travel-time reduction {motion['median_reduction_pct']:.1f}%; sum of individual durations {motion['sum_old_s']:.1f}→{motion['sum_new_s']:.1f}s. {motion['shorter_than_previous']} shorter and {motion['longer_than_previous']} longer results. The acceptance comparison uses each request's own baseline; the previous replay is reported separately. The sum is not a scheduled cycle-time measurement.</p><p>The original 2.57s screenshot reference exceeds its recorded TCP acceleration limit: about 9.62 m/s² versus 1 m/s². Its timing is not an equal-limit target. Reference recordings remain unchanged.</p><p><a href="index.html#236e7d6c7f2343a27196c7806774659f42f95dbe607e08c39d807c06659060f3-curobo">Open screenshot trajectory and -ref pair</a> · <a href="motion-comparison.json">Per-task motion and jerk metrics</a> · <a href="exact-export-audit.json">Exact-export audit</a></p><p>For the shown trajectory, travel time drops from 7.56 s to 6.32 s (16.4%). Position, velocity and acceleration remain continuous at joins. Peak joint jerk increases from 11.08 to 16.23 rad/s³, within the recorded limits; faster motion does not improve every smoothness metric. Across the 97 faster results, 75 also reduce RMS joint jerk.</p><h2>End-to-end benchmark</h2><p>Same ten tasks as the earlier benchmark, including gains and fallbacks. One sequential same-source A/B trial, 60 requests total. Warm summaries use the second request per task; fresh summaries use a new worker. Medians below include request processing and final validation. Resources are sampled every 50 ms; RSS may double-count shared pages. These are observations, not latency guarantees or confidence intervals.</p><table><tr><th>Mode</th><th>Metric</th><th>Continuous off</th><th>Continuous on</th></tr>{benchmark_table}</table><p><a href="benchmark/summary.json">Summary</a> · <a href="benchmark/warm.json">Warm requests and motion metrics</a> · <a href="benchmark/fresh.json">Fresh requests and motion metrics</a></p><p>The timing optimizer's earlier 39× stage improvement does not imply an end-to-end planner speedup. Continuous motion adds path-polishing and qualification work. Shorter duration also does not guarantee lower RMS jerk; all per-task metrics are retained for inspection.</p><h2>All tasks</h2><table><tr><th>Task</th><th>Previous s</th><th>Current s</th><th>Selected</th><th>Reason</th></tr>{table}</table>'''
    (OUT/'report.html').write_text(report)
    (OUT/'README.md').write_text('# Production continuous-motion replay\n\nCore60eb607a, option enabled explicitly; default remains off. 135 production outputs plus 135 unchanged original references. See report.html for acceptance, exact-export audit and same-source end-to-end benchmark.\n')
    (OUT/'pairing.json').write_text(json.dumps({'count':135,'curobo_source':RUN.name,'reference_source':'original recorded Barilla','production_core':'60eb607a','continuous_default':False},indent=2))
    print(OUT)
if __name__=='__main__':main()
