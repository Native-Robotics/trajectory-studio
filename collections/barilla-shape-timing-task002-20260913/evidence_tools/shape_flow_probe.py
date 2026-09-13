"""Offline whole-task timing with nonzero speed at geometrically polished joins."""
exec(open('/tmp/curobo-rnd/shape_timing_sweep.py').read().split('rows=[];best=[]')[0])
from scipy.special import betaincinv
from planner.optimization_core.curobo.core import retime_solution
OUT=BASE/'curobo-shape-flow-task002-20260913';OUT.mkdir(exist_ok=True)
data=json.loads((BASE/'curobo-shape-join-task002-20260913/anchors3-gain0.7.traj').read_text());paths=[];lengths=[]
for part,d,po in zip(task.parts,data['parts'],models):
 sp=Spline.from_coefficients(d['knots'],d['coeffs']);t=np.linspace(d['knots'][0],d['knots'][-1],10001);q=sp(t).T;f,_=_tcp_samples(part,po,q,t);arc=np.r_[0,np.cumsum(np.linalg.norm(np.diff(f[:,:3,3],axis=0),axis=1))];keep=np.r_[True,np.diff(arc)>1e-8];keep[-1]=False;ar=np.r_[arc[keep],arc[-1]];qr=np.vstack([q[keep],q[-1]]);paths.append(CubicSpline(ar/ar[-1],qr));lengths.append(ar[-1])
rows=[]
for alpha in (2.5,3,3.5):
 bounds=np.r_[0,np.cumsum(lengths)]/sum(lengths);tb=betaincinv(alpha,alpha,bounds);qt=[];tt=[]
 for i,path in enumerate(paths):
  t=np.linspace(tb[i],tb[i+1],301);progress=(betainc(alpha,alpha,t)-bounds[i])/(bounds[i+1]-bounds[i]);q=path(progress);q[0]=task.parts[i].start.position.value;q[-1]=task.parts[i].target.position.value
  tt.extend(t if i==0 else t[1:]);qt.extend(q if i==0 else q[1:])
 # One shared cubic interpolation defines derivative continuity across both joins.
 global_spline=Spline.from_states(np.array(tt),np.array(qt),start=np.zeros((6,2)),end=np.zeros((6,2)))
 sols=[]
 for i in range(3):
  times=np.r_[tb[i],np.asarray(global_spline.knots)[(np.asarray(global_spline.knots)>tb[i])&(np.asarray(global_spline.knots)<tb[i+1])],tb[i+1]]
  q=global_spline(times).T;v=global_spline.get_velocity(times).T;a=global_spline.get_acceleration(times).T;z=np.zeros_like(q);sols.append(Solution(times,q,v,a,z.copy(),z.copy(),[]))
 factor=1.
 for part,po,sol in zip(task.parts,models,sols):
  sp=solution_spline(sol);times=np.linspace(sol.times[0],sol.times[-1],3001);_,peaks=_tcp_samples(part,po,sp(times).T,times);jr=np.max(np.abs(_derivative_ranges(sp)),axis=-1)
  factor=max(factor,peaks[0]/2,np.sqrt(peaks[1]),np.max(jr[1]/equipment['max_velocity']),np.sqrt(np.max(jr[2]/equipment['max_acceleration'])),np.cbrt(np.max(jr[3]/equipment['max_jerk'])))
 final=retime_solution(ComplexSolution(sols),factor*1.02);row={'alpha':alpha,'duration_s':factor*1.02}
 try:
  row['qualification']=qualify_solution(task,models,final,settings)
  with core_override('CuRoboPlanner'):
   report=SolutionValidator().validate(list(zip(task.parts,[active_core().prepare_planning_object(p) for p in models])),final);row['collision_valid']=report.is_valid()
  if row['collision_valid']:
   parts=[]
   for p in final.parts:
    sp=solution_spline(p);parts.append({'knots':list(sp.knots),'coeffs':[v.c.tolist() for v in sp.ppoly]})
   name=f'flow-{alpha:g}.traj';(OUT/name).write_text(json.dumps({'parts':parts}));row['candidate']=name
 except Exception as e:row['error']=str(e)
 rows.append(row);print({k:v for k,v in row.items() if k!='qualification'},flush=True)
(OUT/'probe.json').write_text(json.dumps(rows,indent=2,default=lambda x:x.tolist() if hasattr(x,'tolist') else str(x)));(OUT/'runner.py').write_bytes(Path(__file__).read_bytes())
