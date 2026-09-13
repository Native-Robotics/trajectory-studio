import json,shutil,hashlib
from pathlib import Path
BASE=Path('/home/luke/.codex/visualizations/2026/09/12/01a0969d-cc8b-77e1-8566-8b3bd1679634');ROOT=Path('/home/luke/.codex/worktrees/studio-barilla-rebuild');SRC=ROOT/'collections/barilla-curobo-reference-20260913';OUT=ROOT/'collections/barilla-shape-timing-task002-20260913';OUT.mkdir(exist_ok=True);files=OUT/'Trajectories/traj';files.mkdir(parents=True,exist_ok=True)
rows=json.loads((SRC/'trajectories.json').read_text());original=next(r for r in rows if r['task_id']==2 and r['pair_role']=='curobo');reference=next(r for r in rows if r['task_id']==2 and r['pair_role']=='ref');comparison=json.loads((BASE/'curobo-shape-timing-final-task002-20260913/comparison.json').read_text())
variants=[('baseline-curobo','curobo',SRC/'Trajectories/traj'/f"{original['id']}.traj"),('retimed-curobo','retimed',BASE/'curobo-shape-timing-sweep-task002-20260913/candidate.traj'),('smooth-curobo','smooth-join',BASE/'curobo-shape-join-task002-20260913/anchors3-gain0.7.traj'),('236e7d6c-ref','ref',SRC/'Trajectories/traj'/f"{reference['id']}.traj")]
index=[];evidence=[]
for ident,variant,source in variants:
 data=json.loads(source.read_text());data.setdefault('status',70);data.setdefault('planner_status','Offline R&D prototype' if variant in ('retimed','smooth-join') else 'Recorded result');out=files/(ident+'.traj');out.write_text(json.dumps(data));shutil.copy2(SRC/'Trajectories/traj'/f"{original['id'] if variant!='ref' else reference['id']}.repr",files/(ident+'.repr'))
 row={**(reference if variant=='ref' else original),'id':ident,'duration':comparison[variant]['duration_s'],'tag':variant};row.pop('pair_id',None);row.pop('pair_role',None)
 if variant in ('retimed','smooth-join'):
  # These are offline path/timing probes; do not present baseline compute metrics as measured.
  for key in list(row):
   if key in ('compute_time','computation_time','elapsed_s','compute_s','wall_time'):row[key]=None
 index.append(row);evidence.append({'id':ident,'source':str(source),'sha256':hashlib.sha256(out.read_bytes()).hexdigest()})
(OUT/'trajectories.json').write_text(json.dumps(index,indent=2));(OUT/'provenance.json').write_text(json.dumps(evidence,indent=2))
for name in ('app.js','index.css','viewer.js','charts.js','readers.js','robot.js','barilla-ui.mjs'):shutil.copy2(SRC/name,OUT/name)
shutil.copytree(SRC/'robots',OUT/'robots',dirs_exist_ok=True)
page=(SRC/'index.html').read_text().replace('<title>cuRobo + Reference pairs · Trajectory Studio</title>','<title>Task 2 · shape and timing experiments</title>').replace('href="../barilla-curobo-rnd-numeric-fk-20260913/report.html"','href="report.html"').replace('Latest cuRobo benchmark →','Shape and timing comparison →').replace('cuRobo / ref pairs · ↑↓ select','Task 2 · offline R&D · ↑↓ select');(OUT/'index.html').write_text(page)
shutil.copy2(BASE/'curobo-shape-timing-final-task002-20260913/comparison.png',OUT/'comparison.png');(OUT/'comparison.json').write_text(json.dumps(comparison,indent=2))
body='''<!doctype html><meta charset="utf-8"><title>Task 2: cuRobo shape and travel time</title><style>body{font:17px/1.55 system-ui;background:#111723;color:#e7edf5;max-width:1120px;margin:36px auto;padding:0 24px}h1{line-height:1.2}a{color:#51d4ed}table{border-collapse:collapse;width:100%;margin:24px 0}th,td{text-align:left;padding:12px;border-bottom:1px solid #3b4658}img{width:100%;background:white;border-radius:10px}small{color:#b6c5d5}</style>
<h1>Task 2: a smoother shape and faster travel</h1><p>Comparing <b>236e7d6c</b>, the reference selected in your screenshot. These numbers describe robot travel time, not planning latency.</p>
<p>The reference flows through its waypoints, but reaches <b>2.74 m/s and 9.62 m/s²</b>. Its recorded TCP limits are <b>2 m/s and 1 m/s²</b>. Current cuRobo respects those limits and stops at every part boundary. Its path is shorter, so distance does not explain the slowdown.</p>
<table><tr><th>Trajectory</th><th>Travel time</th><th>Join angles</th><th>Result</th></tr>
<tr><td><a href="index.html#236e7d6c-ref">Original reference</a></td><td>2.57 s</td><td>0.38° / 0.03°</td><td>Exceeds recorded TCP speed and acceleration</td></tr>
<tr><td><a href="index.html#baseline-curobo">Current cuRobo</a></td><td>7.56 s</td><td>54.20° / 23.90°</td><td>Qualified published baseline</td></tr>
<tr><td><a href="index.html#retimed-curobo">Timing prototype</a></td><td><b>7.02 s · 7.2% faster</b></td><td>54.20° / 23.90°</td><td>Same path resampled; constraint and FCL checks pass</td></tr>
<tr><td><a href="index.html#smooth-curobo">Smooth-join prototype</a></td><td>8.29 s</td><td>0.06° / 0.03°</td><td>Smoother geometric joins; constraint and FCL checks pass; slower</td></tr></table>
<img src="comparison.png" alt="TCP paths, speed and acceleration of reference, cuRobo and two prototypes">
<p><b>What needs to change:</b> optimize the connected path and its timing together, allowing speed through compatible waypoints while enforcing Cartesian acceleration and joint jerk. Retiming each rest-to-rest segment cannot recover the reference’s continuous motion.</p>
<p>A first whole-task timing probe on the polished path passed checks but took 11.14 seconds after respecting jerk peaks; it was not promoted. Feeding recorded joint limits into native cuRobo alone also did not improve this case.</p>
<p><b>Scope:</b> one task, three motion parts. The prototypes are offline post-processing of native cuRobo output, not a deployed planner change or a 135-task benchmark. Both prototypes were scaled against the raw recorded joint velocity, acceleration and jerk arrays in addition to the existing qualification checks. Cartesian limits and collisions are sampled checks, not continuous mathematical certification. Join angles use directions measured over approximately 1 mm. Geometry polishing includes constrained wrist-orientation refinement.</p>
<p><a href="../barilla-curobo-reference-20260913/index.html">Back to all 135 cuRobo/reference pairs</a> · <a href="comparison.json">Measured data</a> · <a href="provenance.json">Trajectory provenance</a></p>'''
(OUT/'report.html').write_text(body)
(OUT/'README.md').write_text('Task 2 shape and timing R&D. See report.html for measured results and limitations. Existing 135-pair collection is unchanged.\n')
print(OUT);print(json.dumps(index,indent=2))
