"""Offline geometric polishing probe: native cuRobo anchors and tangent-matched joins."""
exec(open('/tmp/curobo-rnd/shape_timing_sweep.py').read().split('rows=[];best=[]')[0])
from scipy.interpolate import make_interp_spline
from planner.optimization_core.curobo.cartesian_refinement import refine_cartesian_part
OUT=BASE/'curobo-shape-join-task002-20260913';OUT.mkdir(exist_ok=True)
paths=[];lengths=[]
for part,d,po in zip(task.parts,data['parts'],models):
 s=Spline.from_coefficients(d['knots'],d['coeffs']);t=np.linspace(d['knots'][0],d['knots'][-1],10001);q=s(t).T;f,_=_tcp_samples(part,po,q,t);arc=np.r_[0,np.cumsum(np.linalg.norm(np.diff(f[:,:3,3],axis=0),axis=1))];keep=np.r_[True,np.diff(arc)>1e-8];keep[-1]=False;ar=np.r_[arc[keep],arc[-1]];qr=np.vstack([q[keep],q[-1]]);paths.append(CubicSpline(ar/ar[-1],qr));lengths.append(ar[-1])
rows=[]
for anchor_count in (3,5,7):
 for tangent_gain in (0.7,1.0):
  anchors=np.linspace(0,1,anchor_count);values=paths[1](anchors);ratio0=lengths[1]/lengths[0]*tangent_gain;ratio1=lengths[1]/lengths[2]*tangent_gain
  # Evaluate derivatives away from numerical endpoint plateaus, at 0.1% arc distance.
  bc=([(1,paths[0](.999,1)*ratio0),(2,paths[0](.999,2)*ratio0**2)],[(1,paths[2](.001,1)*ratio1),(2,paths[2](.001,2)*ratio1**2)])
  curve=make_interp_spline(anchors,values,k=5,bc_type=bc);u=np.linspace(0,1,301);q=curve(u);z=np.zeros_like(q);sol=Solution(u,q,z.copy(),z.copy(),z.copy(),z.copy(),[])
  row={'anchors':anchor_count,'tangent_gain':tangent_gain}
  try:
   corrected,stats=refine_cartesian_part(sol,task.parts[1],models[1]);row['refinement']=stats
   # Reuse already qualified timing-only linear parts, then retime polished middle.
   candidate=json.loads((BASE/'curobo-shape-timing-sweep-task002-20260913/candidate.traj').read_text());solutions=[]
   for i,d in enumerate(candidate['parts']):
    if i==1:
     # Native parameter has matched endpoint tangents; use a beta timing profile.
     qs=CubicSpline(u,corrected.states);t=np.linspace(0,.25,301);q=qs(betainc(2.5,2.5,t/.25));z=np.zeros_like(q);p=Solution(t,q,z.copy(),z.copy(),z.copy(),z.copy(),[])
    else:
     sp=Spline.from_coefficients(d['knots'],d['coeffs']);t=np.array(d['knots']);q=sp(t).T;z=np.zeros_like(q);p=Solution(t,q,sp.get_velocity(t).T,sp.get_acceleration(t).T,z.copy(),z.copy(),[])
    solutions.append(p)
   mid=solutions[1];sp=solution_spline(mid);times=np.linspace(0,.25,3001);_,peaks=_tcp_samples(task.parts[1],models[1],sp(times).T,times);jr=np.max(np.abs(_derivative_ranges(sp)),axis=-1)
   factor=max(peaks[0]/2,np.sqrt(peaks[1]),np.max(jr[1]/equipment['max_velocity']),np.sqrt(np.max(jr[2]/equipment['max_acceleration'])),np.cbrt(np.max(jr[3]/equipment['max_jerk'])))*1.03
   final=retime_rest_parts(ComplexSolution(solutions),[1,factor,1]);row['duration_s']=sum(p.times[-1]-p.times[0] for p in final.parts)
   row['qualification']=qualify_solution(task,models,final,settings)
   with core_override('CuRoboPlanner'):
    report=SolutionValidator().validate(list(zip(task.parts,[active_core().prepare_planning_object(p) for p in models])),final);row['collision_valid']=report.is_valid()
   if row['collision_valid']:
    parts=[]
    for p in final.parts:
     s=solution_spline(p);parts.append({'knots':list(s.knots),'coeffs':[v.c.tolist() for v in s.ppoly]})
    name=f'anchors{anchor_count}-gain{tangent_gain:g}.traj';(OUT/name).write_text(json.dumps({'parts':parts}));row['candidate']=name
  except Exception as e:row['error']=str(e)
  rows.append(row);print({k:v for k,v in row.items() if k not in ('qualification','refinement')},flush=True)
(OUT/'probe.json').write_text(json.dumps(rows,indent=2,default=lambda x:x.tolist() if hasattr(x,'tolist') else str(x)));(OUT/'runner.py').write_bytes(Path(__file__).read_bytes())
