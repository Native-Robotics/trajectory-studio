import sys,json
from pathlib import Path
import numpy as np
sys.path.insert(0,'/home/luke/.codex/worktrees/tp-curobo-core');sys.argv[0]='/home/luke/.codex/worktrees/tp-curobo-core/main.py'
import planner
from serialization.schemas import TaskSchema
from planner.planning_object.common_planning_object_factory import planning_object_by_part
from planner.optimization_core.curobo.validation import _tcp_samples,_derivative_ranges
from nrutils.spline import Spline
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
BASE=Path('/home/luke/.codex/visualizations/2026/09/12/01a0969d-cc8b-77e1-8566-8b3bd1679634')
OUT=BASE/'curobo-shape-timing-task002-20260913';OUT.mkdir(exist_ok=True)
task=TaskSchema().load(json.loads((BASE/'curobo-rnd-numeric-fk-full-20260913/tasks/002.json').read_text()))
COL=Path('/home/luke/.codex/worktrees/studio-barilla-rebuild/collections/barilla-curobo-reference-20260913/Trajectories/traj')
fig=plt.figure(figsize=(13,9));ax=fig.add_subplot(221,projection='3d');speedax=fig.add_subplot(222);accax=fig.add_subplot(223);xy=fig.add_subplot(224)
report={}
for variant,color in [('ref','#ef8b23'),('curobo','#00a6c8')]:
 data=json.loads(next(COL.glob(f'236*-{variant}.traj')).read_text());rows=[];offset=0
 for i,(part,d) in enumerate(zip(task.parts,data['parts'])):
  s=Spline.from_coefficients(d['knots'],d['coeffs']);t=np.linspace(d['knots'][0],d['knots'][-1],3001);q=s(t).T;po=planning_object_by_part(part)
  frames,peaks=_tcp_samples(part,po,q,t);p=frames[:,:3,3];v=np.gradient(p,t,axis=0,edge_order=2);a=np.gradient(v,t,axis=0,edge_order=2);speed=np.linalg.norm(v,axis=1);acc=np.linalg.norm(a,axis=1)
  ranges=_derivative_ranges(s);jp=np.max(np.abs(ranges),axis=-1)
  duration=t[-1]-t[0]
  row={'part':i,'name':['MoveToExit','MoveToNext','MoveToPlace'][i],'duration_s':duration,'tcp_length_m':float(np.linalg.norm(np.diff(p,axis=0),axis=1).sum()),'endpoint_distance_m':float(np.linalg.norm(p[-1]-p[0])),'peak_tcp_speed_m_s':peaks[0],'peak_tcp_acceleration_m_s2':peaks[1],'joint_peak_velocity':jp[1].tolist(),'joint_peak_acceleration':jp[2].tolist(),'joint_peak_jerk':jp[3].tolist(),'start_tcp_speed':float(speed[0]),'end_tcp_speed':float(speed[-1])};rows.append(row)
  ax.plot(*p.T,color=color,label=variant if i==0 else None);xy.plot(p[:,0],p[:,1],color=color,label=variant if i==0 else None)
  speedax.plot(t-t[0]+offset,speed,color=color,label=variant if i==0 else None);accax.plot(t-t[0]+offset,acc,color=color,label=variant if i==0 else None)
  np.savez(OUT/f'{variant}-part{i}.npz',t=t-t[0]+offset,xyz=p,q=q,speed=speed,acceleration=acc);offset+=duration
 report[variant]={'duration_s':offset,'parts':rows}
ax.set(title='Task 2: actual TCP path',xlabel='X (m)',ylabel='Y (m)',zlabel='Z (m)');ax.legend();xy.set(title='Top view',xlabel='X (m)',ylabel='Y (m)');xy.axis('equal');xy.legend()
speedax.set(title='TCP speed',xlabel='Time (s)',ylabel='m/s');speedax.axhline(2,color='gray',ls='--',label='Recorded limit');speedax.legend()
accax.set(title='TCP acceleration magnitude',xlabel='Time (s)',ylabel='m/s²');accax.axhline(1,color='gray',ls='--',label='Recorded limit');accax.legend()
fig.tight_layout();fig.savefig(OUT/'comparison.png',dpi=160);(OUT/'comparison.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
