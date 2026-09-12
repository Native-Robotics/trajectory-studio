"""Index regeneration retains Barilla metadata without rewriting motion inputs."""
import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest

from generate_index import generate_index


class IndexTests(unittest.TestCase):
    def test_corpus_join_preserves_metadata_and_csv(self):
        with tempfile.TemporaryDirectory() as folder, contextlib.chdir(folder):
            trajectory = Path('Trajectories/traj')
            trajectory.mkdir(parents=True)
            content = json.dumps({'status': 70, 'parts': [{'knots': [0, 2]}]})
            (trajectory / 'recorded.traj').write_text(content)
            (trajectory / 'old-demo.traj').write_text(content)
            Path('Trajectories/csv').mkdir()
            Path('Trajectories/csv/demo.csv').write_text('time,q\n0,1\n1,2\n')
            Path('palletize_corpus.json').write_text(json.dumps({'rows': [{
                'desired_id': 'recorded', 'task_id': 4, 'status': 'SOLVED',
                'box_number': 5, 'place_pallet': 'pallet-A',
                'compute_s': 12.5, 'mileage_sum_rad': 8.2, 'flags': []
            }]}))
            with contextlib.redirect_stdout(io.StringIO()):
                generate_index()
            entries = {row['id']: row for row in json.loads(Path('trajectories.json').read_text())}
            self.assertEqual(set(entries), {'recorded', 'demo'})
            self.assertEqual(entries['recorded']['compute_s'], 12.5)
            self.assertEqual(entries['recorded']['mileage_sum_rad'], 8.2)
            self.assertEqual(entries['recorded']['planner_status'], 'SOLVED')
            self.assertEqual((trajectory / 'recorded.traj').read_text(), content)
            self.assertTrue((trajectory / 'old-demo.traj').is_file())

    def test_empty_parts_do_not_claim_motion_path(self):
        with tempfile.TemporaryDirectory() as folder, contextlib.chdir(folder):
            Path('Trajectories/traj').mkdir(parents=True)
            Path('Trajectories/traj/failed.traj').write_text('{"status":40,"parts":[]}')
            with contextlib.redirect_stdout(io.StringIO()):
                generate_index()
            self.assertFalse(json.loads(Path('trajectories.json').read_text())[0]['has_path'])


if __name__ == '__main__':
    unittest.main()
