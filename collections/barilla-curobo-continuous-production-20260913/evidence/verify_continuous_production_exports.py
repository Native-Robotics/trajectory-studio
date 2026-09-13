"""Re-open exact candidate exports and independently recheck before publication."""
import json
import hashlib
import math
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
import numpy as np
import continuous_motion_conic as experiment
from planner.optimization_core.curobo import validation
from planner.planning_object import planning_object_collision_checker as checker

BASE = experiment.BASE
OUT = BASE / 'curobo-continuous-production-full-20260913'
SOURCE = BASE / 'curobo-recorded-joint-limits-full-20260913'

def read(path):
    return json.loads(path.read_text())

def independent_peaks(part, order):
    peaks = []
    for joint in np.asarray(part['coeffs']):
        values = []
        for column, width in zip(joint.T, np.diff(part['knots'])):
            derivative = np.polyder(column, order)
            roots = np.roots(np.polyder(derivative))
            times = [0., width, *[float(r.real) for r in roots if abs(r.imag) < 1e-10 and 0 < r.real < width]]
            values.extend(np.abs(np.polyval(derivative, times)))
        peaks.append(max(values))
    return np.asarray(peaks)

def main():
    records = read(OUT / 'manifest.json')['rows']
    by_id = {r['task_id']: r['id'] for r in read(OUT / 'trajectories.json')}
    assert len(records) == 135 and {r['task_id'] for r in records} == set(range(135))
    rows = []
    for record in records:
        assert record['status']=='SOLVED',record['task_id']
        tid = record['task_id']
        filename = OUT / 'Trajectories/traj' / (by_id[tid] + '.traj')
        data = read(filename)
        payload = read(SOURCE / 'tasks' / f'{tid:03}.json')
        task = experiment.TaskSchema().load(payload)
        models = [experiment.planning_object_by_part(p) for p in task.parts]
        splines = [experiment.Spline.from_coefficients(p['knots'], p['coeffs']) for p in data['parts']]
        assert len(splines) == len(task.parts)
        sols = [SimpleNamespace(times=np.array(s.knots), states=s(s.knots).T,
                    velocities=s.get_velocity(s.knots).T, accelerations=s.get_acceleration(s.knots).T) for s in splines]
        mapping = {id(sol):s for sol,s in zip(sols,splines)}
        solution = SimpleNamespace(parts=sols)
        with patch.object(validation, 'solution_spline', side_effect=lambda sol: mapping[id(sol)]):
            qualification = experiment.qualify_solution(task, models, solution, {**experiment.SETTINGS, 'validation_frequency':1200})
        assert qualification['constraints_valid']
        ratios = []
        for part in data['parts']:
            per_part = {}
            for order, field in enumerate(('max_velocity','max_acceleration','max_jerk'),1):
                cap = payload['equipment_model'].get(field)
                if cap is not None:
                    ratio = float(np.max(independent_peaks(part,order) / cap))
                    assert math.isfinite(ratio) and ratio <= 1 + 1e-6, (tid, field, ratio)
                    per_part[field] = ratio
            ratios.append(per_part)
        joins = []
        for left, right in zip(splines,splines[1:]):
            delta = [float(np.max(np.abs(left.ppoly[j](left.knots[-1],nu=k)-right.ppoly[j](right.knots[0],nu=k)))) for k in range(3) for j in range(task.parts[0].dof)]
            assert max(delta) < 1e-6, (tid, max(delta))
            joins.append(max(delta))
        original = checker.check_hitbox_on_self_collisions
        def original_checker(*args, **kwargs):
            kwargs.pop('reuse_numeric_colliders',None)
            return original(*args, **kwargs)
        def exact_spline(times, *args, **kwargs):
            matches = [s for s in splines if np.array_equal(times,s.knots)]
            assert len(matches) == 1
            return matches[0]
        with experiment.core_override('CuRoboPlanner'), patch.object(experiment.Spline,'from_states',side_effect=exact_spline), patch('planner.solution_validation.solution_collision_detector.check_hitbox_on_self_collisions',original_checker):
            collision = experiment.SolutionValidator().validate(list(zip(task.parts,[experiment.active_core().prepare_planning_object(m) for m in models])),solution)
        assert collision.is_valid(), tid
        rows.append({'task_id':tid, 'sha256':hashlib.sha256(filename.read_bytes()).hexdigest(),
            'qualification_1200hz':qualification, 'independent_raw_cap_ratios':ratios,
            'join_max_qva_delta':joins, 'original_FCL_valid':True})
        (OUT/'exact-export-audit.json').write_text(json.dumps({'complete':False,'rows':rows},indent=2))
        print(f'PASS {tid:03}: exact export, TCP/waypoints, raw joint caps, C2 joins, original FCL',flush=True)
    (OUT/'exact-export-audit.json').write_text(json.dumps({'complete':True,'valid_exports':len(rows),'rows':rows},indent=2))
    print(f'PASS: all {len(rows)} valid exports independently rechecked',flush=True)
if __name__ == '__main__':
    main()
