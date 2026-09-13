import json,hashlib
from pathlib import Path
from urllib.request import urlopen
from urllib.parse import urljoin,urlparse
from html.parser import HTMLParser
BASE=Path('/home/luke/.codex/visualizations/2026/09/12/01a0969d-cc8b-77e1-8566-8b3bd1679634')
ROOT=Path('/home/luke/.codex/worktrees/studio-barilla-rebuild')
OUT=ROOT/'collections/barilla-curobo-continuous-reference-20260913'
PAIRS=ROOT/'collections/barilla-curobo-reference-20260913'
RUN=BASE/'curobo-continuous-conic-full-20260913'
def read(p):return json.loads(p.read_text())
class Links(HTMLParser):
    def __init__(self):super().__init__();self.links=[]
    def handle_starttag(self,tag,attrs):
        for k,v in attrs:
            if k in ('href','src') and v:self.links.append(v)
def main():
    rows=read(OUT/'trajectories.json');comparison=read(OUT/'comparison.json');assert len(rows)==270 and len({r['id'] for r in rows})==270
    byid={r['id']:r for r in rows};compare={r['task_id']:r for r in comparison['rows']}
    count=0
    for row in rows:
        tid=row['task_id'];ident=row['id'];original=PAIRS/'Trajectories/traj'/ident;dst=OUT/'Trajectories/traj'/ident
        assert dst.with_suffix('.repr').read_bytes()==original.with_suffix('.repr').read_bytes();count+=1
        expected=RUN/f'{tid:03}.traj' if row['pair_role']=='curobo' and compare[tid]['selected']=='continuous' else original.with_suffix('.traj')
        assert dst.with_suffix('.traj').read_bytes()==expected.read_bytes();count+=1
        data=read(dst.with_suffix('.traj'))
        duration=sum(p['knots'][-1]-p['knots'][0] for p in data.get('parts',[]))
        # Original reference metadata records milliseconds, whereas cuRobo records full precision.
        tolerance = 0.000501 if row['pair_role']=='ref' else 1e-6
        assert abs(duration-row['duration'])<tolerance,(ident,duration,row['duration'])
        partner=ident.rsplit('-',1)[0]+('-ref' if row['pair_role']=='curobo' else '-curobo')
        assert byid[partner]['pair_id']==row['pair_id']
    for name in ('index.html','report.html','trajectories.json','comparison.json','exact-export-audit.json'):
        local=OUT/name;url='http://localhost:8001/'+str(local.relative_to(ROOT))
        assert urlopen(url).read()==local.read_bytes()
        if name.endswith('.html'):
            parser=Links();parser.feed(local.read_text())
            for link in parser.links:
                full=urljoin(url,link)
                if urlparse(full).netloc=='localhost:8001':
                    with urlopen(full) as response:assert response.status==200,full
    print(f'PASS: {count} source-exact files; 270 durations/IDs (reference metadata rounded to milliseconds); 135 complete pairs; HTTP bytes and local HTML links')
if __name__=='__main__':main()
