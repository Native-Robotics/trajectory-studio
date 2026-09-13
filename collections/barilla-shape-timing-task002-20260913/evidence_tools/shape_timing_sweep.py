"""Offline experimental retiming of an existing cuRobo path, without weakening limits."""
exec(open('/tmp/curobo-rnd/shape_timing_compare.py').read().split('fig=plt.figure')[0])
from scipy.interpolate import CubicSpline
from scipy.special import betainc
from planner.optimization_core.solution import Solution,ComplexSolution
from planner.optimization_core.curobo.validation import required_time_scale,qualify_solution,solution_spline
from planner.optimization_core.curobo.core import retime_rest_parts
from planner.cores import core_override,active_core
from planner.solution_validation.solution_validator import SolutionValidator
from nrutils.config import parse_config
OUT=BASE/'curobo-shape-timing-sweep-task002-20260913';OUT.mkdir(exist_ok=True)
settings=parse_config()['TrajectoryPlanner']['Planner']['CuRoboPlanner'];models=[planning_object_by_part(p) for p in task.parts]
raw=json.loads((BASE/'curobo-rnd-numeric-fk-full-20260913/tasks/002.json').read_text());equipment=raw['equipment_model'];data=json.loads(next(COL.glob('236*-curobo.traj')).read_text())
rows=[];best=[]
for i,(part,d,po) in enumerate(zip(task.parts,data['parts'],models)):
 s=Spline.from_coefficients(d['knots'],d['coeffs']);t=np.linspace(d['knots'][0],d['knots'][-1],10001);q=s(t).T;f,_=_tcp_samples(part,po,q,t);xyz=f[:,:3,3]
 arc=np.r_[0,np.cumsum(np.linalg.norm(np.diff(xyz,axis=0),axis=1))];keep=np.r_[True,np.diff(arc)>1e-8];keep[-1]=False;ar=np.r_[arc[keep],arc[-1]];qr=np.vstack([q[keep],q[-1]])
 qs=CubicSpline(ar/ar[-1],qr,axis=0);candidates=[]
 for alpha,beta in [(2.25,2.25),(2.5,2.5),(2.75,2.75),(3,3),(3,2.5),(2.5,3),(3.5,2.5),(2.5,3.5),(4,4)]:
  u=np.linspace(0,1,301);q=qs(betainc(alpha,beta,u));q[0]=part.start.position.value;q[-1]=part.target.position.value;z=np.zeros_like(q);sol=Solution(u*.25,q,z.copy(),z.copy(),z.copy(),z.copy(),[])
  spline=solution_spline(sol);times=np.linspace(0,.25,3001);_,peaks=_tcp_samples(part,po,spline(times).T,times);jr=np.max(np.abs(_derivative_ranges(spline)),axis=-1)
  factor=max(peaks[0]/equipment['max_linear_speed'],np.sqrt(peaks[1]/equipment['max_linear_acceleration']),np.max(jr[1]/equipment['max_velocity']),np.sqrt(np.max(jr[2]/equipment['max_acceleration'])),np.cbrt(np.max(jr[3]/equipment['max_jerk'])))*1.02
  candidates.append((factor*.25,alpha,beta,sol,factor));rows.append({'part':i,'alpha':alpha,'beta':beta,'duration':factor*.25})
 winner=min(candidates,key=lambda x:x[0]);best.append(winner);print('part',i,'best',winner[:3],flush=True)
scaled=retime_rest_parts(ComplexSolution([b[3] for b in best]),[b[4] for b in best]);report={'prototype':'Offline cuRobo path arc-length beta timing sweep; recorded TCP and raw joint v/a/jerk caps included','rows':rows,'selected':[{'duration':b[0],'alpha':b[1],'beta':b[2]} for b in best]}
try:
 report['qualification']=qualify_solution(task,models,scaled,settings)
 with core_override('CuRoboPlanner'):
  prepared=[active_core().prepare_planning_object(p) for p in models];collision=SolutionValidator().validate(list(zip(task.parts,prepared)),scaled);report['collision_valid']=collision.is_valid();report['collision_counts']=[{'obstacles':len(p.obstacle_collisions),'self':len(p.self_collisions)} for p in collision.part_reports]
except Exception as e: report['error']=str(e)
parts=[]
for p in scaled.parts:
 s=solution_spline(p);parts.append({'knots':list(s.knots),'coeffs':[v.c.tolist() for v in s.ppoly]})
report['duration_s']=sum(p.times[-1]-p.times[0] for p in scaled.parts)
(OUT/'probe.json').write_text(json.dumps(report,indent=2,default=lambda x:x.tolist() if hasattr(x,'tolist') else str(x)));(OUT/'candidate.traj').write_text(json.dumps({'parts':parts}));(OUT/'runner.py').write_bytes(Path(__file__).read_bytes());print('RESULT',report.get('error'),report.get('collision_valid'),report['duration_s'],flush=True)
