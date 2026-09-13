"""Sequential four-run benchmark; run only after replay and audits terminate."""
import os,sys,subprocess
from pathlib import Path
for kind,mode in [('warm','control'),('warm','enabled'),('fresh','enabled'),('fresh','control')]:
    env={**os.environ,'CONTINUOUS_MODE':mode,'CONTINUOUS_KIND':kind,'OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1'}
    log=Path('/tmp/curobo-rnd')/f'continuous-production-{mode}-{kind}10.log'
    print('START',kind,mode,flush=True)
    with log.open('w') as out:
        subprocess.run([sys.executable,'/tmp/curobo-rnd/continuous_worker_benchmark.py'],env=env,stdout=out,stderr=subprocess.STDOUT,check=True)
    print('DONE',kind,mode,flush=True)
