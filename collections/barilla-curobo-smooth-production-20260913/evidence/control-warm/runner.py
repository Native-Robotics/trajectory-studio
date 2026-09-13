"""Same-source baseline/continuous end-to-end worker benchmark; no monkeypatches."""
import os,sys,json,hashlib
from pathlib import Path
ROOT=Path('/home/luke/.codex/worktrees/tp-curobo-core')
sys.path.insert(0,str(ROOT));sys.argv[0]=str(ROOT/'main.py')
from nrutils.config import parse_config
config=parse_config()['TrajectoryPlanner']['Planner']
config['core']='CuRoboPlanner'
mode=os.environ['CONTINUOUS_MODE'];kind=os.environ['CONTINUOUS_KIND']
assert mode in ('control','enabled') and kind in ('fresh','warm')
config['CuRoboPlanner']['linear_fast_path']=True
config['CuRoboPlanner']['continuous_motion']=mode=='enabled'
from snippets.replay_curobo_warm import main
BASE=Path('/home/luke/.codex/visualizations/2026/09/12/01a0969d-cc8b-77e1-8566-8b3bd1679634')
OUT=BASE/f'curobo-continuous-production-{mode}-{kind}10-20260913'
# Preserve the historical fixed-ten selection, including both gains and fallbacks.
ids=[3,4,21,54,59,69,95,118,119,133]
if kind=='warm':ids=[tid for tid in ids for _ in range(2)]
sys.argv=[str(ROOT/'main.py'),'--output',str(OUT),'--task-ids',','.join(map(str,ids))]+(['--fresh-workers'] if kind=='fresh' else [])
if __name__=='__main__':
    main()
    (OUT/'benchmark-mode.json').write_text(json.dumps({'mode':mode,'kind':kind,'task_ids':[3,4,21,54,59,69,95,118,119,133],'runtime_override':'continuous_motion flag only','wrapper_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2))
    (OUT/'runner.py').write_bytes(Path(__file__).read_bytes())
