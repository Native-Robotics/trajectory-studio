exec(open('/tmp/curobo-rnd/shape_timing_sweep.py').read().split('rows=[];best=[]')[0])
from unittest.mock import patch
from types import SimpleNamespace
from planner.optimization_core.curobo import validation
from planner.planning_object import planning_object_collision_checker as checker
from snippets.benchmark_metrics import trajectory_metrics
OUT=Path('/home/luke/.codex/worktrees/studio-barilla-rebuild/collections/barilla-shape-timing-task002-20260913');allrows=[]
for ident in ('retimed-curobo','smooth-curobo','adaptive-curobo'):
 d=json.loads((OUT/'Trajectories/traj'/f'{ident}.traj').read_text());splines=[Spline.from_coefficients(p['knots'],p['coeffs']) for p in d['parts']];sols=[SimpleNamespace(times=np.array(s.knots),states=s(s.knots).T,velocities=s.get_velocity(s.knots).T,accelerations=s.get_acceleration(s.knots).T) for s in splines];mapping={id(sol):s for sol,s in zip(sols,splines)};complex=SimpleNamespace(parts=sols)
 with patch.object(validation,'solution_spline',side_effect=lambda sol:mapping[id(sol)]): report=qualify_solution(task,models,complex,{**settings,'validation_frequency':1200})
 for p in report['parts']:
  for key,limit in [('joint_peak_velocity','max_velocity'),('joint_peak_acceleration','max_acceleration'),('joint_peak_jerk','max_jerk')]:assert np.all(np.array(p[key])<=np.array(equipment[limit])+1e-6),(ident,key)
 original=checker.check_hitbox_on_self_collisions
 def unchanged_checker(*args,**kw):kw.pop('reuse_numeric_colliders',None);return original(*args,**kw)
 def exact_spline(times,*args,**kw):return next(s for s in splines if np.array_equal(times,s.knots))
 with core_override('CuRoboPlanner'),patch.object(Spline,'from_states',side_effect=exact_spline),patch('planner.solution_validation.solution_collision_detector.check_hitbox_on_self_collisions',unchanged_checker):
  collision=SolutionValidator().validate(list(zip(task.parts,[active_core().prepare_planning_object(p) for p in models])),complex)
 assert collision.is_valid(),ident
 allrows.append({'id':ident,'qualification_1200hz':report,'raw_recorded_joint_caps_valid':True,'original_fcl_valid':True,'metrics':trajectory_metrics(d['parts'])})
rows=json.loads((OUT/'trajectories.json').read_text())
for r in rows:
 if r['id'] in ('retimed-curobo','smooth-curobo','adaptive-curobo'):
  r['reference_source']='offline R&D path/timing prototype';r['planner_status']='QUALIFIED_OFFLINE_PROTOTYPE';r.pop('mileage_sum_rad',None)
(OUT/'trajectories.json').write_text(json.dumps(rows,indent=2));(OUT/'verification.json').write_text(json.dumps(allrows,indent=2,default=lambda x:x.tolist() if hasattr(x,'tolist') else str(x)));print('PASS: three exact exported splines; 1200 Hz Cartesian audit, analytic joint extrema, raw recorded v/a/jerk caps, original FCL')
