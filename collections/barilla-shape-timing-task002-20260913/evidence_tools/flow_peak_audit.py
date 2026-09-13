exec(open('/tmp/curobo-rnd/shape_timing_sweep.py').read().split('rows=[];best=[]')[0])
data=json.loads((BASE/'curobo-shape-flow-task002-20260913/flow-3.traj').read_text())
for i,d in enumerate(data['parts']):
 s=Spline.from_coefficients(d['knots'],d['coeffs']);t=np.linspace(d['knots'][0],d['knots'][-1],20001);f,pk=_tcp_samples(task.parts[i],models[i],s(t).T,t);v=np.gradient(f[:,:3,3],t,axis=0,edge_order=2);a=np.linalg.norm(np.gradient(v,t,axis=0,edge_order=2),axis=1);j=np.stack([p.derivative(3)(t) for p in s.ppoly],axis=1)
 ind=np.unravel_index(np.argmax(np.abs(j)/np.array(equipment['max_jerk'])),j.shape)
 print(i,'duration',t[-1]-t[0],'acc',max(a),'acc at',(t[np.argmax(a)]-t[0])/(t[-1]-t[0]),'jerk',j[ind],'joint',ind[1],'at',(t[ind[0]]-t[0])/(t[-1]-t[0]))
 print('jerk95',np.quantile(np.abs(j),.95,axis=0),'peak',np.max(np.abs(j),axis=0))
