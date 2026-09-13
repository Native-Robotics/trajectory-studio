"""Fixed-input alternating CPU timing benchmark; excludes native planning and validation."""
import json,time,statistics
from pathlib import Path
import numpy as np
from scipy.optimize import minimize
from unittest.mock import patch
import continuous_motion_conic as experiment
import conic_speed
OUT=experiment.BASE/'curobo-timing-solver-benchmark-20260913'

def slsqp(ds,Af,Jf,tcp_acc,acceleration,bounds):
    n=len(bounds)
    def objective(y):
        r=np.sqrt(np.r_[0,y,0]);return np.sum(2*ds/(r[:-1]+r[1:]))
    def jac(y):
        r=np.sqrt(np.r_[0,y,0]);den=(r[:-1]+r[1:])**2;return -(ds[:-1]/den[:-1]+ds[1:]/den[1:])/r[1:-1]
    def con(y):
        a=Af@y;j=Jf@y;return np.r_[(tcp_acc*.97)**2-np.sum(a*a,axis=1),(acceleration-j).ravel(),(acceleration+j).ravel()]
    def conjac(y):return np.vstack([-2*np.einsum('ij,ijk->ik',Af@y,Af),-Jf.reshape(-1,n),Jf.reshape(-1,n)])
    seed=np.minimum(bounds*.1,.1);a=Af@seed;j=Jf@seed
    ratio=max(float(np.max(np.linalg.norm(a,axis=1)/(tcp_acc*.97))),float(np.max(np.abs(j)/acceleration)),1.)
    seed=np.maximum(1e-8,seed/(ratio*1.05))
    result=minimize(objective,seed,jac=jac,bounds=[(1e-8,b) for b in bounds],constraints={'type':'ineq','fun':con,'jac':conjac},method='SLSQP',options={'maxiter':150,'ftol':1e-8})
    assert result.success and min(con(result.x))>=-1e-5,result.message
    return result.x

def check(args,x):
    ds,A,J,ta,ja,bounds=args
    assert np.max(np.linalg.norm(A@x,axis=1))<=ta*.97+1e-6
    assert np.all(np.abs(J@x)<=ja+1e-6)
    assert np.all(x<=bounds+1e-6) and np.all(x>0)
    r=np.sqrt(np.r_[0,x,0]);return float(np.sum(2*ds/(r[:-1]+r[1:])))

def main():
    OUT.mkdir(exist_ok=False);rows=[]
    source=experiment.BASE/'curobo-rnd-numeric-fk-full-20260913'
    native=conic_speed.solve
    for tid in (2,21,59):
        captured=[]
        def capture(*args):
            captured.append(tuple(a.copy() if hasattr(a,'copy') else a for a in args))
            return native(*args)
        payload=json.loads((source/'tasks'/f'{tid:03}.json').read_text())
        task=experiment.TaskSchema().load(payload);models=[experiment.planning_object_by_part(p) for p in task.parts]
        data=json.loads((source/'tasks'/f'{tid:03}-{tid:03}.result.json').read_text())
        paths,lengths,_=experiment.polish(task,models,data['parts'])
        with patch.object(conic_speed,'solve',side_effect=capture):experiment.adaptive(task,models,paths,lengths)
        # Both algorithms see identical bounds, including second solve's join caps.
        for stage,args in enumerate(captured):
            np.savez(OUT/f'{tid:03}-{stage}.npz',**dict(zip(('ds','Af','Jf','tcp_acc','acceleration','bounds'),args)))
            for solver in (slsqp,native): check(args,solver(*args))
            for repeat in range(5):
                order=(('slsqp',slsqp),('conic',native)) if repeat%2==0 else (('conic',native),('slsqp',slsqp))
                for name,solver in order:
                    wall=time.perf_counter();cpu=time.process_time();x=solver(*args);cpu=time.process_time()-cpu;wall=time.perf_counter()-wall
                    rows.append({'task_id':tid,'stage':stage,'repeat':repeat,'solver':name,'wall_s':wall,'cpu_s':cpu,'objective_s':check(args,x)})
        (OUT/'measurements.json').write_text(json.dumps(rows,indent=2));print('Benchmarked',tid,flush=True)
    summary={'scope':'Fixed-input timing optimization only; 6 problems, 5 measured repetitions per solver after warmup, alternating order, single-thread BLAS. Excludes native planning, polishing and validation. Observational local benchmark, not a confidence interval.','median_wall_s':{n:statistics.median(r['wall_s'] for r in rows if r['solver']==n) for n in ('slsqp','conic')},'median_cpu_s':{n:statistics.median(r['cpu_s'] for r in rows if r['solver']==n) for n in ('slsqp','conic')}}
    summary['median_wall_ratio']=summary['median_wall_s']['slsqp']/summary['median_wall_s']['conic']
    deltas=[]
    for tid in (2,21,59):
        for stage in (0,1):
            sub=[r for r in rows if r['task_id']==tid and r['stage']==stage]
            a=statistics.median(r['objective_s'] for r in sub if r['solver']=='slsqp');b=statistics.median(r['objective_s'] for r in sub if r['solver']=='conic');deltas.append(abs(a-b))
    summary['maximum_objective_delta_s']=max(deltas)
    (OUT/'summary.json').write_text(json.dumps(summary,indent=2));(OUT/'benchmark.py').write_bytes(Path(__file__).read_bytes());print(json.dumps(summary,indent=2),flush=True)
if __name__=='__main__':main()
