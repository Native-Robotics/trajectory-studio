"""Calculate joint travel from cubic extrema in saved cuRobo trajectories."""
import json
import math
from pathlib import Path

root = Path(__file__).resolve().parents[1]
collection = root / 'collections/barilla-curobo-20260912'
index = collection / 'trajectories.json'
rows = json.loads(index.read_text())
for row in rows:
    trajectory = json.loads((collection / 'Trajectories/traj' / (row['id'] + '.traj')).read_text())
    travel = [0.0] * 6
    for part in trajectory.get('parts', []):
        for joint, coeffs in enumerate(part['coeffs']):
            for i, (start, end) in enumerate(zip(part['knots'], part['knots'][1:])):
                a, b, c, d = [axis[i] for axis in coeffs]
                duration = end - start
                points = [0.0, duration]
                if a != 0:
                    discriminant = 4*b*b - 12*a*c
                    if discriminant >= 0:
                        points += [r for r in ((-2*b-math.sqrt(discriminant))/(6*a), (-2*b+math.sqrt(discriminant))/(6*a)) if 0 < r < duration]
                elif b != 0 and 0 < -c/(2*b) < duration:
                    points.append(-c/(2*b))
                values = [((a*t+b)*t+c)*t+d for t in sorted(points)]
                travel[joint] += sum(abs(y-x) for x,y in zip(values,values[1:]))
    row['mileage_rad'] = travel if row['has_path'] else None
    row['mileage_sum_rad'] = sum(travel) if row['has_path'] else None
index.write_text(json.dumps(rows, indent=2)+'\n')
