"""Offline R&D: generic native-path polishing and continuous timing; never acceptance by itself."""
import sys,json,time,argparse
from pathlib import Path
import numpy as np
from scipy.interpolate import CubicSpline,make_interp_spline
from scipy.optimize import minimize,brentq
from scipy.ndimage import gaussian_filter1d
ROOT=Path('/home/luke/.codex/worktrees/tp-curobo-core');sys.path.insert(0,str(ROOT));sys.argv[0]=str(ROOT/'main.py')
import planner
from serialization.schemas import TaskSchema
from planner.planning_object.common_planning_object_factory import planning_object_by_part
from planner.optimization_core.solution import Solution,ComplexSolution
from planner.optimization_core.curobo.cartesian_refinement import refine_cartesian_part
from planner.optimization_core.curobo.validation import _tcp_samples,_derivative_ranges,solution_spline,qualify_solution,joint_derivative_limits
from planner.optimization_core.curobo.core import retime_solution
from planner.solution_validation.solution_validator import SolutionValidator
from planner.cores import core_override,active_core
from nrutils.spline import Spline
from nrutils.config import parse_config
BASE=Path('/home/luke/.codex/visualizations/2026/09/12/01a0969d-cc8b-77e1-8566-8b3bd1679634')
CONFIG=parse_config()['TrajectoryPlanner']['Planner'];SETTINGS=CONFIG['CuRoboPlanner']


def arc_path(part,model,spline):
    t=np.linspace(spline.knots[0],spline.knots[-1],10001)
    q=spline(t).T;frames,_=_tcp_samples(part,model,q,t)
    arc=np.r_[0,np.cumsum(np.linalg.norm(np.diff(frames[:,:3,3],axis=0),axis=1))]
    if arc[-1]<1e-5:raise ValueError('Near-stationary TCP needs a separate joint-space parameterization')
    keep=np.r_[True,np.diff(arc)>1e-8];keep[-1]=False
    return CubicSpline(np.r_[arc[keep],arc[-1]]/arc[-1],np.vstack([q[keep],q[-1]])),arc[-1]


def polish(task,models,parts,anchor_count=3):
    if not all(np.array_equal(p.start_tcp.transform_matrix,task.parts[0].start_tcp.transform_matrix) and np.array_equal(p.target_tcp.transform_matrix,task.parts[0].start_tcp.transform_matrix) for p in task.parts):
        raise ValueError('Changing TCP requires separate motion blocks')
    for a,b in zip(task.parts,task.parts[1:]):
        if a.linear and b.linear:raise ValueError('Consecutive linear constraints require a join compatibility test')
        for node in (a.target,b.start):
            if node.velocity is not None and node.velocity.strict:raise ValueError('Explicit waypoint velocity requires constrained timing')
    paths=[];lengths=[]
    for part,model,data in zip(task.parts,models,parts):
        path,length=arc_path(part,model,Spline.from_coefficients(data['knots'],data['coeffs']));paths.append(path);lengths.append(length)
    result=[];diagnostics=[]
    for i,(part,model,path) in enumerate(zip(task.parts,models,paths)):
        if part.linear:result.append(path);diagnostics.append(None);continue
        if (i and not task.parts[i-1].linear) or (i+1<len(paths) and not task.parts[i+1].linear):raise ValueError('Consecutive free segments require shared tangent optimization')
        left=paths[i-1] if i else path;right=paths[i+1] if i+1<len(paths) else path
        lpos=.999 if i else .001;rpos=.001 if i+1<len(paths) else .999
        lscale=lengths[i]/lengths[i-1]*.7 if i else 1.;rscale=lengths[i]/lengths[i+1]*.7 if i+1<len(paths) else 1.
        bc=([(1,left(lpos,1)*lscale),(2,left(lpos,2)*lscale*lscale)],[(1,right(rpos,1)*rscale),(2,right(rpos,2)*rscale*rscale)])
        anchors=np.linspace(0,1,anchor_count);curve=make_interp_spline(anchors,path(anchors),k=5,bc_type=bc);u=np.linspace(0,1,301);q=curve(u);z=np.zeros_like(q)
        corrected,stats=refine_cartesian_part(Solution(u,q,z.copy(),z.copy(),z.copy(),z.copy(),[]),part,model)
        polished,length=arc_path(part,model,solution_spline(corrected));result.append(polished);diagnostics.append(stats);lengths[i]=length
    return result,lengths,diagnostics


def adaptive(task,models,paths,lengths):
    L=sum(lengths);sb=np.r_[0,np.cumsum(lengths)];s=np.unique(np.r_[np.linspace(0,L,181),sb]);q=np.empty((len(s),task.parts[0].dof))
    for i,path in enumerate(paths):
        mask=(s>=sb[i])&(s<=sb[i+1]);q[mask]=path((s[mask]-sb[i])/lengths[i])
    qgeom=CubicSpline(s,q);frames,_=_tcp_samples(task.parts[0],models[0],q,s);pgeom=CubicSpline(s,frames[:,:3,3]);ds=np.diff(s);mid=(s[1:]+s[:-1])/2;n=len(s)
    D=np.zeros((n-1,n));M=np.zeros_like(D)
    for i,step in enumerate(ds):D[i,i]=-1/step;D[i,i+1]=1/step;M[i,i:i+2]=.5
    A=pgeom(mid,1)[:,:,None]*D[:,None,:]/2+pgeom(mid,2)[:,:,None]*M[:,None,:]
    J=qgeom(mid,1)[:,:,None]*D[:,None,:]/2+qgeom(mid,2)[:,:,None]*M[:,None,:]
    caps=[joint_derivative_limits(p,m,SETTINGS,CONFIG) for p,m in zip(task.parts,models)]
    velocity=np.min([np.broadcast_to(c[0],(task.parts[0].dof,)) for c in caps],axis=0)
    acceleration=np.min([np.broadcast_to(c[1],(task.parts[0].dof,)) for c in caps],axis=0)
    tcp_speed=min(getattr(p.equipment,'max_linear_speed',None) or 2. for p in task.parts)
    tcp_acc=min(getattr(p.equipment,'max_linear_acceleration',None) or 1. for p in task.parts)
    bound=np.minimum(tcp_speed**2,np.min((velocity/np.maximum(np.abs(qgeom(s,1)),1e-10))**2,axis=1));bound[[0,-1]]=0;Af=A[:,:,1:-1];Jf=J[:,:,1:-1]
    def objective(y):
        r=np.sqrt(np.r_[0,y,0]);return np.sum(2*ds/(r[:-1]+r[1:]))
    def jac(y):
        r=np.sqrt(np.r_[0,y,0]);den=(r[:-1]+r[1:])**2;return -(ds[:-1]/den[:-1]+ds[1:]/den[1:])/r[1:-1]
    def con(y):
        a=Af@y;j=Jf@y;return np.r_[(tcp_acc*.97)**2-np.sum(a*a,axis=1),(acceleration-j).ravel(),(acceleration+j).ravel()]
    def conjac(y):return np.vstack([-2*np.einsum('ij,ijk->ik',Af@y,Af),-Jf.reshape(-1,n-2),Jf.reshape(-1,n-2)])
    def solve(bounds,seed):
        from conic_speed import solve as conic_solve
        from types import SimpleNamespace
        values=conic_solve(ds,Af,Jf,tcp_acc,acceleration,bounds)
        if min(con(values)) < -1e-5 or np.any(values>bounds+1e-6) or np.any(values<=0):raise ValueError('Conic solution failed independent timing constraints')
        return SimpleNamespace(x=values)
    started=time.monotonic();res=solve(bound[1:-1],np.minimum(bound[1:-1]*.1,.1));profile=np.ones_like(s)
    for boundary in sb[1:-1]:profile*=1-(1-.7**2)*np.exp(-((s-boundary)/.10)**2)
    local=np.minimum(bound[1:-1],res.x*profile[1:-1]);res=solve(local,np.minimum(res.x,local));optimizer_s=time.monotonic()-started
    regular_s=np.linspace(0,L,1801);xx=gaussian_filter1d(np.interp(regular_s,s,np.r_[0,res.x,0]),10,mode='constant');x=np.interp(s,regular_s,xx);x[[0,-1]]=0
    t=np.r_[0,np.cumsum(2*ds/(np.sqrt(x[:-1])+np.sqrt(x[1:])))];inverse=CubicSpline(t,s,bc_type=((1,0),(1,0)));virtual_tb=np.interp(sb,s,t);T=t[-1];ramp=.4;total=T+ramp
    def clock(v):
        v=np.asarray(v);F=lambda u:u**3-.5*u**4
        return np.where(v<ramp,ramp*F(v/ramp),np.where(v>total-ramp,T-ramp*F((total-v)/ramp),v-ramp/2))
    tb=np.array([0,*[brentq(lambda v:float(clock(v))-target,0,total) for target in virtual_tb[1:-1]],total]);tt=[];qt=[]
    for i in range(len(paths)):
        times=np.linspace(tb[i],tb[i+1],181);qq=qgeom(inverse(clock(times)));qq[0]=task.parts[i].start.position.value;qq[-1]=task.parts[i].target.position.value
        tt.extend(times if i==0 else times[1:]);qt.extend(qq if i==0 else qq[1:])
    global_sp=Spline.from_states(np.array(tt),np.array(qt),start=np.zeros((q.shape[1],2)),end=np.zeros((q.shape[1],2)));sols=[];factor=1.
    for i,part in enumerate(task.parts):
        knots=np.asarray(global_sp.knots);times=np.r_[tb[i],knots[(knots>tb[i])&(knots<tb[i+1])],tb[i+1]];qq=global_sp(times).T;z=np.zeros_like(qq);sol=Solution(times,qq,global_sp.get_velocity(times).T,global_sp.get_acceleration(times).T,z.copy(),z.copy(),[]);sols.append(sol)
        sp=solution_spline(sol);audit=np.linspace(times[0],times[-1],3001);_,peaks=_tcp_samples(part,models[i],sp(audit).T,audit);jr=np.max(np.abs(_derivative_ranges(sp)),axis=-1)
        factor=max(factor,peaks[0]/tcp_speed,np.sqrt(peaks[1]/tcp_acc),*[float(np.max(jr[order]/cap))**(1/order) for order,cap in enumerate(caps[i],1)])
    return retime_solution(ComplexSolution(sols),factor*1.02),{'optimizer_s':optimizer_s,'retime_factor':factor*1.02}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--tasks',default=','.join(map(str,range(135))));parser.add_argument('--output',type=Path,required=True);parser.add_argument('--anchors',type=int,default=3);args=parser.parse_args();args.output.mkdir(exist_ok=False);rows=[]
    source=BASE/'curobo-rnd-numeric-fk-full-20260913'
    for tid in map(int,args.tasks.split(',')):
        start=time.monotonic();payload=json.loads((source/'tasks'/f'{tid:03}.json').read_text());task=TaskSchema().load(payload);result=json.loads((source/'tasks'/f'{tid:03}-{tid:03}.result.json').read_text());models=[planning_object_by_part(p) for p in task.parts];row={'task_id':tid,'baseline_duration_s':sum(p['knots'][-1]-p['knots'][0] for p in result['parts'])}
        try:
            paths,lengths,stats=polish(task,models,result['parts'],args.anchors);candidate,timing=adaptive(task,models,paths,lengths);row['timing']=timing;row['duration_s']=sum(p.times[-1]-p.times[0] for p in candidate.parts)
            row['qualification']=qualify_solution(task,models,candidate,{**SETTINGS,'validation_frequency':1200})
            with core_override('CuRoboPlanner'):
                report=SolutionValidator().validate(list(zip(task.parts,[active_core().prepare_planning_object(p) for p in models])),candidate)
            row['collision_valid']=report.is_valid()
            if not report.is_valid():raise ValueError('Original FCL rejected polished path')
            parts=[]
            for p in candidate.parts:
                sp=solution_spline(p);parts.append({'knots':list(sp.knots),'coeffs':[v.c.tolist() for v in sp.ppoly]})
            (args.output/f'{tid:03}.traj').write_text(json.dumps({'status':70,'parts':parts}));row['valid']=True
        except Exception as e:row['valid']=False;row['error']=str(e)
        row['elapsed_s']=time.monotonic()-start;rows.append(row);print({k:v for k,v in row.items() if k not in ('qualification','timing')},flush=True);(args.output/'results.json').write_text(json.dumps(rows,indent=2,default=lambda x:x.tolist() if hasattr(x,'tolist') else str(x)))
    (args.output/'runner.py').write_bytes(Path(__file__).read_bytes())
if __name__=='__main__':main()
