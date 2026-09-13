"""Exact SOC epigraph of sum 2 ds / (sqrt(x_i)+sqrt(x_{i+1})).
API reference: https://clarabel.org/stable/python/getting_started_py/
Scratch dependency: clarabel 0.11.1; not installed in the planner environment.
"""
import sys
sys.path.insert(0,'/tmp/curobo-rnd/solver-deps')
import clarabel
import numpy as np
from scipy import sparse

def solve(ds,Af,Jf,tcp_acc,acceleration,bounds):
    count=len(bounds);segments=len(ds);size=2*count+segments;blocks=[];rhs=[];cones=[]
    def add(a,b,cone):blocks.append(sparse.csc_matrix(a));rhs.append(np.asarray(b));cones.append(cone)
    # Joint acceleration and explicit speed bounds.
    joint=Jf.reshape(-1,count);nj=len(joint)
    mat=np.zeros((2*nj+3*count,size));vec=np.r_[np.tile(acceleration,segments),np.tile(acceleration,segments),bounds,np.full(count,-1e-8),np.zeros(count)]
    mat[:nj,:count]=joint;mat[nj:2*nj,:count]=-joint
    mat[2*nj:2*nj+count,:count]=np.eye(count)
    mat[2*nj+count:2*nj+2*count,:count]=-np.eye(count)
    mat[2*nj+2*count:,count:2*count]=-np.eye(count)
    add(mat,vec,clarabel.NonnegativeConeT(len(vec)))
    for a in Af:
        mat=np.zeros((4,size));mat[1:,:count]=-a
        add(mat,[tcp_acc*.97,0.,0.,0.],clarabel.SecondOrderConeT(4))
    for i in range(count):
        # ||[2 w, x-1]|| <= x+1  iff w^2 <= x.
        mat=np.zeros((3,size));mat[0,i]=-1;mat[1,count+i]=-2;mat[2,i]=-1
        add(mat,[1.,0.,-1.],clarabel.SecondOrderConeT(3))
    for i,step in enumerate(ds):
        # ||[2 sqrt(2 ds), t-v]|| <= t+v iff t*v >= 2 ds.
        mat=np.zeros((3,size));mat[0,2*count+i]=-1;mat[2,2*count+i]=-1
        for endpoint in (i,i+1):
            if 0<endpoint<segments:
                mat[0,count+endpoint-1]=-1;mat[2,count+endpoint-1]=1
        add(mat,[0.,2*np.sqrt(2*step),0.],clarabel.SecondOrderConeT(3))
    settings=clarabel.DefaultSettings();settings.verbose=False;settings.max_iter=200
    solver=clarabel.DefaultSolver(sparse.csc_matrix((size,size)),np.r_[np.zeros(2*count),np.ones(segments)],sparse.vstack(blocks).tocsc(),np.concatenate(rhs),cones,settings)
    result=solver.solve()
    if str(result.status)!='Solved':raise ValueError('Conic timing failed: '+str(result.status))
    return np.array(result.x[:count])
