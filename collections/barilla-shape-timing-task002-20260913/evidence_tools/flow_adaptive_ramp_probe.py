"""Offline curvature-aware timing probe on the checked smooth cuRobo path."""
exec(open('/tmp/curobo-rnd/shape_flow_probe.py').read().split('rows=[]\nfor alpha')[0])
from scipy.interpolate import PchipInterpolator
from scipy.optimize import minimize
from scipy.ndimage import gaussian_filter1d
from scipy.integrate import cumulative_trapezoid
import time
OUT=BASE/'curobo-shape-adaptive-ramp-task002-20260913';OUT.mkdir(exist_ok=True)
L=sum(lengths);sb=np.r_[0,np.cumsum(lengths)];s=np.unique(np.r_[np.linspace(0,L,181),sb]);q=np.empty((len(s),6))
for i,path in enumerate(paths):
 mask=(s>=sb[i])&(s<=sb[i+1]);q[mask]=path((s[mask]-sb[i])/lengths[i])
qgeom=CubicSpline(s,q);frames,_=_tcp_samples(task.parts[0],models[0],q,s);pgeom=CubicSpline(s,frames[:,:3,3]);ds=np.diff(s);mid=(s[1:]+s[:-1])/2;g=pgeom(mid,1);h=pgeom(mid,2);qg=qgeom(mid,1);qh=qgeom(mid,2)
n=len(s);D=np.zeros((n-1,n));M=np.zeros_like(D)
for i,step in enumerate(ds):D[i,i]=-1/step;D[i,i+1]=1/step;M[i,i:i+2]=.5
A=g[:,:,None]*D[:,None,:]/2+h[:,:,None]*M[:,None,:];J=qg[:,:,None]*D[:,None,:]/2+qh[:,:,None]*M[:,None,:]
bound=np.minimum(4.,np.min((np.array(equipment['max_velocity'])/np.maximum(np.abs(qgeom(s,1)),1e-10))**2,axis=1));bound[[0,-1]]=0
# Interior speed variables avoid singular endpoint derivatives in the objective.
Af=A[:,:,1:-1];Jf=J[:,:,1:-1]
def objective(y):
 x=np.r_[0,y,0];r=np.sqrt(x);return np.sum(2*ds/(r[:-1]+r[1:]))
def jac(y):
 x=np.r_[0,y,0];r=np.sqrt(x);den=(r[:-1]+r[1:])**2;return -(ds[:-1]/den[:-1]+ds[1:]/den[1:])/r[1:-1]
def con(y):
 a=Af@y;j=Jf@y;return np.r_[.97**2-np.sum(a*a,axis=1),(np.array(equipment['max_acceleration'])-j).ravel(),(np.array(equipment['max_acceleration'])+j).ravel()]
def conjac(y):
 a=Af@y;return np.vstack([-2*np.einsum('ij,ijk->ik',a,Af),-Jf.reshape(-1,n-2),Jf.reshape(-1,n-2)])
started=time.monotonic();res=minimize(objective,np.minimum(bound[1:-1]*.1,.1),jac=jac,bounds=[(1e-8,b) for b in bound[1:-1]],constraints={'type':'ineq','fun':con,'jac':conjac},method='SLSQP',options={'maxiter':150,'ftol':1e-8});print('optimizer',res.success,res.message,'time',time.monotonic()-started,'duration',res.fun,'constraint_min',min(con(res.x)),flush=True)
rows=[]
for ramp in (.4,.8,1.2):
 sigma=1.
 x=np.r_[0,res.x,0];x=gaussian_filter1d(x,sigma,mode='constant');x[[0,-1]]=0
 t=np.r_[0,np.cumsum(2*ds/(np.sqrt(x[:-1])+np.sqrt(x[1:])))];inverse=CubicSpline(t,s,bc_type=((1,0),(1,0)))
 virtual_tb=np.interp(sb,s,t);T=t[-1];total=T+ramp
 def clock(tt):
  tt=np.asarray(tt);left=tt/ramp;right=(total-tt)/ramp
  F=lambda u:u**3-.5*u**4
  return np.where(tt<ramp,ramp*F(left),np.where(tt>total-ramp,T-ramp*F(right),tt-ramp/2))
 from scipy.optimize import brentq
 tb=np.array([0,*[brentq(lambda v:float(clock(v))-target,0,total) for target in virtual_tb[1:-1]],total]);tt=[];qt=[]
 for i in range(3):
  times=np.linspace(tb[i],tb[i+1],181);ss=inverse(clock(times));qq=qgeom(ss);qq[0]=task.parts[i].start.position.value;qq[-1]=task.parts[i].target.position.value
  tt.extend(times if i==0 else times[1:]);qt.extend(qq if i==0 else qq[1:])
 global_sp=Spline.from_states(np.array(tt),np.array(qt),start=np.zeros((6,2)),end=np.zeros((6,2)));sols=[];factor=1.;causes=[]
 for i in range(3):
  knots=np.asarray(global_sp.knots);times=np.r_[tb[i],knots[(knots>tb[i])&(knots<tb[i+1])],tb[i+1]];qq=global_sp(times).T;z=np.zeros_like(qq);sol=Solution(times,qq,global_sp.get_velocity(times).T,global_sp.get_acceleration(times).T,z.copy(),z.copy(),[]);sols.append(sol)
  sp=solution_spline(sol);audit=np.linspace(times[0],times[-1],3001);_,peaks=_tcp_samples(task.parts[i],models[i],sp(audit).T,audit);jr=np.max(np.abs(_derivative_ranges(sp)),axis=-1)
  ratios=[peaks[0]/2,np.sqrt(peaks[1]),np.max(jr[1]/equipment['max_velocity']),np.sqrt(np.max(jr[2]/equipment['max_acceleration'])),np.cbrt(np.max(jr[3]/equipment['max_jerk']))];causes.append(ratios);factor=max(factor,*ratios)
 final=retime_solution(ComplexSolution(sols),factor*1.02);row={'ramp':ramp,'duration_s':float(total*factor*1.02),'time_scales_by_constraint':causes}
 try:
  row['qualification']=qualify_solution(task,models,final,settings)
  with core_override('CuRoboPlanner'):
   report=SolutionValidator().validate(list(zip(task.parts,[active_core().prepare_planning_object(p) for p in models])),final);row['collision_valid']=report.is_valid()
  if row['collision_valid']:
   parts=[]
   for p in final.parts:
    sp=solution_spline(p);parts.append({'knots':list(sp.knots),'coeffs':[v.c.tolist() for v in sp.ppoly]})
   name=f'adaptive-ramp-{ramp:g}.traj';(OUT/name).write_text(json.dumps({'parts':parts}));row['candidate']=name
 except Exception as e:row['error']=str(e)
 rows.append(row);print({k:v for k,v in row.items() if k not in ('qualification','time_scales_by_constraint')},flush=True)
(OUT/'probe.json').write_text(json.dumps({'optimizer':{'success':bool(res.success),'duration':res.fun,'minimum_constraint':min(con(res.x))},'rows':rows},indent=2,default=lambda x:x.tolist() if hasattr(x,'tolist') else str(x)));(OUT/'runner.py').write_bytes(Path(__file__).read_bytes())
