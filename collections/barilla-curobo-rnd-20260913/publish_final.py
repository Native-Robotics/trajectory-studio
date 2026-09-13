"""Publish final R&D evidence with the previous strict version as primary comparator."""
import html
import json
import statistics
import sys
from pathlib import Path

ROOT = Path('/home/luke/.codex/worktrees/tp-curobo-core')
sys.path.insert(0, str(ROOT))
from snippets import curobo_improvement_report as report

BASE = Path('/home/luke/.codex/visualizations/2026/09/12/01a0969d-cc8b-77e1-8566-8b3bd1679634')
FINAL = BASE / 'curobo-rnd-final-20260913'
COLD = BASE / 'curobo-rnd-buffer256-fresh10-20260913'
WARM = BASE / 'curobo-rnd-buffer256-warm-validation-20260913'


def main():
    manifest = report.read(FINAL / 'manifest.json')
    if manifest['run_status'] != 'complete' or len(manifest['rows']) != 135:
        raise SystemExit('Final replay must be terminal with exactly 135 measured requests')
    manifest, final = report.measurements(FINAL)
    _, previous = report.measurements(BASE / 'curobo-improved-20260913')
    _, cold_old = report.measurements(BASE / 'curobo-improved-fresh10-20260913')
    _, cold_new = report.measurements(COLD)
    _, warm_old = report.measurements(BASE / 'curobo-improved-warm10-20260913')
    _, warm_new = report.measurements(WARM)
    groups = []
    for label, section, key in [
        ('Fresh planning latency (s)', None, 'planning_s'),
        ('Fresh whole-process CPU (s)', 'resources', 'cpu_s'),
        ('Fresh sampled GPU memory (MiB)', 'resources', 'peak_gpu_memory_mb'),
        ('Fresh sampled summed RSS (MiB)', 'resources', 'peak_tree_rss_mb'),
    ]:
        pairs = []
        for tid in report.FIXED_IDS:
            a = next(r for r in cold_old if r['task_id'] == tid)
            b = next(r for r in cold_new if r['task_id'] == tid)
            av, bv = ((r.get(section) or {}).get(key) if section else r.get(key) for r in (a,b))
            if av is not None and bv is not None:
                pairs.append((av,bv))
        groups.append(dict(metric=label, pairs=len(pairs), previous=statistics.median(a for a,b in pairs), current=statistics.median(b for a,b in pairs)))
    warm_summaries = [report.warm_second_observations(r) for r in (warm_old,warm_new)]
    for label,key in [('Retained-worker request latency (s)','elapsed_s'),('Retained-worker sampled GPU memory (MiB)','peak_gpu_compute_mb')]:
        groups.append(dict(metric=label,pairs=10,previous=warm_summaries[0]['metrics'][key]['median'],current=warm_summaries[1]['metrics'][key]['median']))
    old_by_id = {r['task_id']:r for r in previous}
    motion_rows=[]
    for row in final:
        old=old_by_id[row['task_id']]
        motion_rows.append({'task_id':row['task_id'],'status':row['status'],'previous':old['motion'],'current':row['motion']})
    for label,key in [('Full corpus motion duration (s)','duration_s'),('Full corpus RMS jerk (rad/s³)','rms_jerk_rad_s3'),('Full corpus normalized jerk','normalized_jerk'),('Full corpus joint mileage (rad)','total_mileage_rad'),('Full corpus maximum acceleration jump (rad/s²)','max_acceleration_jump_rad_s2')]:
        matched=[r for r in motion_rows if r['status']=='SOLVED' and r['previous'] and r['current'] and r['previous'].get(key) is not None and r['current'].get(key) is not None]
        groups.append(dict(metric=label,pairs=len(matched),previous=statistics.median(r['previous'][key] for r in matched),current=statistics.median(r['current'][key] for r in matched),increased_tasks=[r['task_id'] for r in matched if r['current'][key]>r['previous'][key]*1.001 + (1e-8 if key=='max_acceleration_jump_rad_s2' else 0)]))
    report.NAME='barilla-curobo-rnd-20260913'
    sys.argv=['publish_final.py','--replay',str(FINAL),'--cold',str(COLD),'--warm',str(WARM),'--note','Final integrated R&D replay. Primary comparison below uses the previous strict validated cuRobo version. Historical develop and original GPU comparisons are retained separately and do not establish equal validity.']
    report.main()
    folder=report.STUDIO/'collections'/report.NAME
    evidence={'baseline':'curobo-improved-20260913','candidate':FINAL.name,'metrics':groups,'warm_summaries':warm_summaries,'motion_rows':motion_rows}
    report.write(folder/'strict-comparison.json',evidence)
    def display(value):
        return f'{value:.2e}' if value and abs(value)<0.001 else report.number(value)
    table_rows=[[html.escape(r['metric']),str(r['pairs']),display(r['previous']),display(r['current']),('Below 1e-8' if r['metric']=='Full corpus maximum acceleration jump (rad/s²)' and max(r['previous'],r['current'])<1e-8 else f"{100*(r['current']/r['previous']-1):+.1f}%") if r['previous'] else '—',str(len(r['increased_tasks'])) if 'increased_tasks' in r else '—'] for r in groups]
    section='<h2>R&D versus previous strict validated cuRobo</h2><p>Both versions enforce the recorded original constraints and retain original FCL checks. Fresh comparisons use the same ten tasks and fresh-process timing method; retained-worker comparisons use second requests from ten consecutive pairs. Each is one observation per task, not a confidence interval. Full-corpus motion medians are paired separately. Lower jerk integrals do not capture acceleration discontinuities; maximum acceleration jumps are shown separately. Acceleration-jump increases also require an absolute difference above 1e-8 rad/s², to avoid counting floating-point noise as a regression.</p>'
    section+=report.table(['Metric','Paired tasks','Previous strict','Current R&D','Change','Tasks increased >0.1%'],table_rows)
    section+='<p>Cache reuse is measured, not assumed: '+html.escape(str(warm_summaries[1]['cache_labels']))+'. Memory is sampled and summed RSS may count shared pages more than once. Constraint and FCL checks are sampled, not continuous-time proofs. No composite quality score is assigned.</p><p><a href="strict-comparison.json">Exact strict comparison and per-task motion metrics</a></p><h2>Historical comparisons and detailed replay</h2>'
    page=folder/'report.html'
    page.write_text(page.read_text().replace('</h1>','</h1>'+section,1))
    md=folder/'report.md'
    md.write_text('# R&D versus previous strict validated cuRobo\n\n'+ '\n'.join(f"- {r['metric']}: {r['previous']:.6g} → {r['current']:.6g} ({r['pairs']} paired tasks)" for r in groups)+'\n\nSee strict-comparison.json for regressions and per-task metrics.\n\n'+md.read_text())
    report.write(FINAL/'strict-comparison.json',evidence)
    print(json.dumps(groups,indent=2))

if __name__=='__main__':
    main()
