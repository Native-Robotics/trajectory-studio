"""Full production travel comparison; compute claims belong to isolated A/B."""
import json,sys,statistics
from pathlib import Path
ROOT=Path('/home/luke/.codex/worktrees/tp-curobo-core');sys.path.insert(0,str(ROOT))
from snippets.benchmark_metrics import trajectory_metrics
BASE=Path('/home/luke/.codex/visualizations/2026/09/12/01a0969d-cc8b-77e1-8566-8b3bd1679634')
CURRENT=BASE/'curobo-continuous-production-full-20260913';OLD=BASE/'curobo-recorded-joint-limits-full-20260913'
def read(p):return json.loads(p.read_text())
def main():
    m=read(CURRENT/'manifest.json');assert m['run_status']=='complete' and len(m['rows'])==135
    old={r['task_id']:r for r in read(OLD/'trajectories.json')};new={r['task_id']:r for r in read(CURRENT/'trajectories.json')}
    rows=[]
    for r in m['rows']:
        tid=r['task_id'];c=r['stats']['continuous_motion'];a=read(OLD/'Trajectories/traj'/f"{old[tid]['id']}.traj")['parts'];b=read(CURRENT/'Trajectories/traj'/f"{new[tid]['id']}.traj")['parts']
        metrics=[trajectory_metrics(parts) for parts in (a,b)]
        rows.append({'task_id':tid,'id':new[tid]['id'],'continuous_accepted':c['accepted'],'reason':c.get('reason'), 'old_duration_s':metrics[0]['duration_s'],'new_duration_s':metrics[1]['duration_s'],'previous_baseline_exact_match':a==b,'motion_metrics_old_new':metrics,'continuous_stats':c})
        (CURRENT/'motion-comparison.json').write_text(json.dumps({'complete':False,'rows':rows},indent=2))
    summary={'complete':True,'tasks':135,'continuous_accepted':sum(r['continuous_accepted'] for r in rows),'baseline_retained':sum(not r['continuous_accepted'] for r in rows),'shorter_than_previous':sum(r['new_duration_s']<r['old_duration_s']-1e-6 for r in rows),'longer_than_previous':sum(r['new_duration_s']>r['old_duration_s']+1e-6 for r in rows),'median_reduction_pct':statistics.median(100*(1-r['new_duration_s']/r['old_duration_s']) for r in rows),'sum_old_s':sum(r['old_duration_s'] for r in rows),'sum_new_s':sum(r['new_duration_s'] for r in rows),'rows':rows,'scope':'Motion quality vs previous corrected replay. Within-request acceptance requires improvement over that request baseline; previous replay differences are reported separately. No whole-replay compute speedup claim.'}
    (CURRENT/'motion-comparison.json').write_text(json.dumps(summary,indent=2));print(json.dumps({k:v for k,v in summary.items() if k!='rows'},indent=2))
if __name__=='__main__':main()
