"""Build paired latest-cuRobo/original-reference Studio data without changing trajectories."""
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NAME = 'barilla-curobo-reference-20260913'
CURRENT = ROOT / 'collections/barilla-curobo-rnd-numeric-fk-20260913'
OUT = ROOT / 'collections' / NAME

def read(path):
    return json.loads(path.read_text())


def main():
    refs = {row['task_id']: row for row in read(ROOT / 'trajectories.json')}
    latest = {row['task_id']: row for row in read(CURRENT / 'trajectories.json')}
    assert len(refs) == len(latest) == 135 and refs.keys() == latest.keys()
    OUT.mkdir(exist_ok=True)
    data = OUT / 'Trajectories/traj'
    data.mkdir(parents=True, exist_ok=True)
    rows, evidence = [], []
    for task_id in sorted(refs):
        ref, curobo = refs[task_id], latest[task_id]
        base = ref['id']
        assert curobo['desired_id'] == base and curobo['id'] == base + '-curobo'
        for role, source, row in [('curobo', CURRENT, curobo), ('ref', ROOT, ref)]:
            ident = base + '-' + role
            item = {**row, 'id': ident, 'pair_id': base, 'pair_role': role,
                    'reference_source': 'original recorded Barilla' if role == 'ref' else 'latest verified cuRobo'}
            # Both variants belong to the same original box/pallet cycle.
            for field in ('box_number', 'place_pallet'):
                if field in ref:
                    item[field] = ref[field]
            for suffix in ('.traj', '.repr'):
                src = source / 'Trajectories/traj' / (row['id'] + suffix)
                dst = data / (ident + suffix)
                shutil.copy2(src, dst)
                assert src.read_bytes() == dst.read_bytes()
            rows.append(item)
        evidence.append({'task_id': task_id, 'curobo': base + '-curobo', 'reference': base + '-ref'})
    (OUT / 'trajectories.json').write_text(json.dumps(rows, indent=2))
    for name in ('app.js', 'index.css', 'viewer.js', 'charts.js', 'readers.js', 'robot.js', 'barilla-ui.mjs'):
        shutil.copy2(ROOT / name, OUT / name)
    shutil.copytree(ROOT / 'robots', OUT / 'robots', dirs_exist_ok=True)
    page = (CURRENT / 'index.html').read_text()
    page = page.replace('<title>Trajectory Studio - 6DOF Robot Trajectory Viewer</title>', '<title>cuRobo + Reference pairs · Trajectory Studio</title>')
    page = page.replace('href="report.html"', 'href="../barilla-curobo-rnd-numeric-fk-20260913/report.html"').replace('135-task results →', 'Latest cuRobo benchmark →')
    page = page.replace('<span>↑↓ select</span>', '<span>cuRobo / ref pairs · ↑↓ select</span>')
    page = page.replace('data-sort="compute"', 'title="Sort pairs by cuRobo compute time" data-sort="compute"').replace('data-sort="mileage"', 'title="Sort pairs by cuRobo mileage" data-sort="mileage"')
    (OUT / 'index.html').write_text(page)
    (OUT / 'pairing.json').write_text(json.dumps({'pairs': evidence, 'count':135,
        'curobo_source':CURRENT.name, 'reference_source':'original root Barilla collection',
        'note':'Reference paths are original recorded results, not newly qualified cuRobo outputs. Source trajectory and representation files are copied byte-for-byte; sorting uses cuRobo metrics for each pair.'}, indent=2))
    print(f'Built {len(rows)} entries / {len(evidence)} pairs: http://localhost:8001/collections/{NAME}/index.html')

if __name__ == '__main__':
    main()
