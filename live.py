"""Read-only live viewer for OmniPack's flat trajectory cache (no sample data)."""
import argparse
import functools
import http.server
import json
import math
from pathlib import Path
from urllib.parse import unquote, urlsplit


def read_json(path, fallback):
    try:
        return json.loads(path.read_text())
    except (OSError, ValueError):
        return fallback


def joint_mileage(data):
    """Exact total variation of each piecewise cubic joint angle, in radians."""
    total = 0.0
    if not data.get('parts'):
        return None
    for part in data['parts']:
        knots, joints = part.get('knots', []), part.get('coeffs', [])
        if not joints or len(knots) < 2:
            return None
        for coeffs in joints:
            for i in range(len(knots)-1):
                span = float(knots[i+1])-float(knots[i])
                if span <= 0:
                    continue
                a, b, c, d = (float(row[i]) for row in coeffs)
                points = [0.0, span]
                # Extrema split the interval into monotone sections, counting out-and-back motion.
                if a != 0:
                    discriminant = b*b-3*a*c
                    if discriminant >= 0:
                        root = math.sqrt(discriminant)
                        points.extend(t for t in ((-b-root)/(3*a), (-b+root)/(3*a)) if 0 < t < span)
                elif b != 0:
                    t = -c/(2*b)
                    if 0 < t < span:
                        points.append(t)
                points.sort()
                values = [((a*t+b)*t+c)*t+d for t in points]
                total += sum(abs(y-x) for x,y in zip(values, values[1:]))
    return total if math.isfinite(total) else None


@functools.lru_cache(maxsize=4096)
def file_mileage(path, mtime_ns, size):
    try:
        return joint_mileage(read_json(Path(path), {}))
    except (ValueError, TypeError, IndexError):
        return None


def carton_dimensions(settings):
    general = read_json(settings/'GeneralSettings/GeneralSettings.json', {})
    preset_id = general.get('presetSettings', {}).get('presetId', '')
    preset = read_json(settings/'PalletizingPresets'/f'{Path(preset_id).name}.json', {})
    margins = {(0., 0., 0.)}
    for storage in preset.get('storages', []):
        for provider in storage.get('collisionProviders', []):
            if provider.get('type') == 'StorageFilling':
                margins.add(tuple(provider.get('additionalSize', [0,0,0])))
    dimensions = set()
    for path in (settings/'PackagingUnits').glob('*.json'):
        unit = read_json(path, {})
        if unit.get('type') != 'Box' or len(unit.get('size', [])) != 3:
            continue
        for margin in margins:
            dimensions.add(tuple(round(float(size)/2+float(extra), 4) for size,extra in zip(unit['size'],margin)))
    return dimensions


def trajectory_identity(rep, metric, dimensions):
    names = metric.get('part_names') or []
    name = ' → '.join(part.removeprefix('MoveTo') for part in names if part)
    if not name:
        name = (metric.get('tag') or '').removeprefix('manipulator-part ')
    cartons = set()
    for shape in rep.get('scene', {}).get('shapes', []):
        extents = shape.get('extents', [])
        if shape.get('shape_type') != 'box' or len(extents) != 3:
            continue
        if any(all(abs(float(a)-b) < .001 for a,b in zip(extents,size)) for size in dimensions):
            cartons.add(tuple(round(float(x),4) for x in shape.get('position', [])))
    last = names[-1] if names else ''
    box = None
    if dimensions and last in ('MoveToPlace', 'MoveToPick', 'MoveToWait'):
        box = len(cartons) + (0 if last == 'MoveToWait' else 1)
        if box == 0:
            box = None
    return dict(name=name or 'Unnamed', tag=metric.get('tag'), box_number=box,
        box_inferred=box is not None, carton_obstacles=len(cartons),
        box_note='Estimate from visible individual carton obstacles matching packaging dimensions; '
                 'grouped layers and multiple pallets can change the actual box sequence. '
                 'Pick/place uses visible count + 1; wait uses visible count.')


def build_index(root, metrics):
    entries = []
    dimensions = carton_dimensions(root.parent)
    for path in sorted(root.glob('*.traj')):
        data = read_json(path, None)
        if not isinstance(data, dict):  # Writer may still be replacing this file.
            continue
        representation = path.with_suffix('.repr')
        rep = read_json(representation, {})
        parts = data.get('parts') or []
        duration = sum(float(p['knots'][-1])-float(p['knots'][0])
                       for p in parts if p.get('knots'))
        metric = metrics.get(path.stem, {})
        stat = path.stat()
        entries.append(dict(**trajectory_identity(rep, metric, dimensions), id=path.stem, format='traj', status=data.get('status', 0),
            model=rep.get('equipment_model', {}).get('model_name', 'unknown'),
            duration=duration, traj_time_s=duration if parts else None,
            mileage_sum_rad=file_mileage(str(path), stat.st_mtime_ns, stat.st_size),
            compute_s=metric.get('compute_s'), compute_kind='active worker time (queue excluded)',
            num_parts=len(rep.get('parts', [])), has_path=bool(parts),
            num_box_obstacles=sum(s.get('shape_type') == 'box' for s in rep.get('scene', {}).get('shapes', [])),
            linear=any(p.get('linear', False) for p in rep.get('parts', [])),
            revision=str(path.stat().st_mtime_ns)+':'+str(representation.stat().st_mtime_ns if representation.exists() else 0)))
    return entries


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, root, metrics, **kwargs):
        self.root, self.metrics = root, metrics
        super().__init__(*args, **kwargs)

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()

    def do_GET(self):
        path = unquote(urlsplit(self.path).path)
        if path == '/trajectories.json':
            payload = json.dumps(build_index(self.root, read_json(self.metrics, {}))).encode()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
        elif path.startswith('/Trajectories/'):
            name = path.removeprefix('/Trajectories/traj/')
            target = self.root / name
            if (Path(name).name != name or target.suffix not in ('.traj', '.repr')
                    or target.resolve().parent != self.root.resolve() or not target.is_file()):
                self.send_error(404)
                return
            payload = target.read_bytes()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
        elif any(p.startswith('.') for p in Path(path).parts):
            self.send_error(404)
        else:
            super().do_GET()

    def do_POST(self):
        self.send_error(405, 'Live settings viewer is read-only')

    def log_message(self, *args):
        pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--trajectories', type=Path, required=True)
    parser.add_argument('--metrics', type=Path, required=True)
    parser.add_argument('--port', type=int, default=8000)
    args = parser.parse_args()
    handler = functools.partial(Handler, root=args.trajectories, metrics=args.metrics,
                                directory=str(Path(__file__).resolve().parent))
    print(f'Live trajectories: {args.trajectories}; http://127.0.0.1:{args.port}', flush=True)
    http.server.ThreadingHTTPServer(('127.0.0.1', args.port), handler).serve_forever()
