from pathlib import Path
import json,hashlib,collections,statistics
out=Path('/home/luke/git/trajectory-studio/collections/barilla-curobo-20260912');root=Path('/home/luke/.codex/worktrees/tp-curobo-core')
m=json.loads((out/'manifest.json').read_text());idx=json.loads((out/'trajectories.json').read_text());rows=m['rows']
assert len(rows)==len(idx)==135
assert sorted(r['task_id'] for r in rows)==list(range(135))
assert len(list((out/'Trajectories/traj').glob('*.traj')))==135
assert len(list((out/'Trajectories/traj').glob('*.repr')))==135
for row,item in zip(rows,idx):
 assert row['desired_id']==item['desired_id']
 traj=json.loads((out/'Trajectories/traj'/f"{item['id']}.traj").read_text())
 payload=json.loads((out/'Trajectories/traj'/f"{item['id']}.repr").read_text())
 assert traj['planner_status']==row['status'] and payload['desired_id']==row['desired_id']
 if row['status']=='SOLVED':
  assert row['validation']['constraints_valid'] and row['validation']['collision_valid']
  assert len(traj['parts'])==len(payload['parts']) and traj['parts']
changed=[p for p,h in m['source_evidence']['sha256_by_path'].items() if hashlib.sha256((root/p).read_bytes()).hexdigest()!=h]
assert not changed,changed
cat=json.loads(Path('/tmp/tp-review-integration/tests/fixtures/palletize_catalog.json').read_text());subset=[]
for r in cat:
 row=rows[r['task_id']];assert row['desired_id']==r['desired_id'];subset.append(row)
def timing(rs):
 a=[r['elapsed_s'] for r in rs];return {'min_s':min(a),'median_s':statistics.median(a),'mean_s':statistics.mean(a),'max_s':max(a),'sum_s':sum(a)}
summary={'counts':dict(collections.Counter(r['status'] for r in rows)), 'catalog_counts':dict(collections.Counter(r['status'] for r in subset)), 'catalog_task_ids':[r['task_id'] for r in subset], 'timing':timing(rows),'solved_timing':timing([r for r in rows if r['status']=='SOLVED']), 'errors':dict(collections.Counter(r.get('error') or r.get('stats',{}).get('error') for r in rows if r['status']!='SOLVED')), 'source_hashes_verified':len(m['source_evidence']['sha256_by_path']), 'dependencies':m['source_evidence']['dependency_versions'],'source_sha256':m['source_sha256']}
(out/'evidence'/'replay-summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
