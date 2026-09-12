import sys,json
sys.path.insert(0,'/home/luke/.codex/worktrees/tp-curobo-core');sys.argv[0]='/home/luke/.codex/worktrees/tp-curobo-core/main.py'
from nrutils.config import parse_config
c=parse_config()
import planner
from snippets.replay_curobo import extract_tasks
from pathlib import Path
from serialization.schemas import TaskSchema
from planner.cores import core_override
from planner.planning_object.common_planning_object_factory import planning_object_by_part
from planner.optimization_core.simplified_planning_object_factory import SimplifiedPlanningObjectFactory
from planner.solution_validation.solution_collision_detector import SolutionCollisionDetector
with core_override('CuRoboPlanner'):
    task=TaskSchema().load(extract_tasks(Path('/home/luke/git/TrajectoryPlanner/logs/trajectoryplanner-2026-09-09_14-15-27.log'))[0])
    import tempfile,numpy as np
    from planner.optimization_core.curobo.model import build_model
    from tests.test_curobo_model import urdf_fk
    from scipy.spatial.transform import Rotation
    p=task.parts[1]
    po=SimplifiedPlanningObjectFactory.create(planning_object_by_part(p))
    with tempfile.TemporaryDirectory() as directory:
        robot,scene,names=build_model(p,po,Path(directory))
        cfg=robot['robot_cfg']['kinematics']
        for label,node in [('start',p.start),('target',p.target)]:
            tf=urdf_fk(cfg['urdf_path'],dict(zip(names,node.position.value)))
            spheres=[]
            for link,cover in cfg['collision_spheres'].items():
                for sphere in cover:
                    spheres.append((link,tf[link][:3,:3]@sphere['center']+tf[link][:3,3],sphere['radius']))
            overlaps=[]
            for ix,(la,a,ra) in enumerate(spheres):
                for lb,b,rb in spheres[ix+1:]:
                    if la==lb or lb in cfg['self_collision_ignore'][la]:continue
                    d=float(np.linalg.norm(a-b)-ra-rb)
                    if d<0:overlaps.append((d,la,lb))
            print(label,'cover self overlaps', sorted(overlaps)[:10])
            overlaps=[]
            for key,box in (scene or {}).get('cuboid',{}).items():
                pose=box['pose'];rot=Rotation.from_quat(np.array(pose[3:])[[1,2,3,0]]).as_matrix()
                half=np.array(box['dims'])/2
                for link,a,r in spheres:
                    local=rot.T@(a-np.array(pose[:3]));delta=np.abs(local)-half
                    d=float(np.linalg.norm(np.maximum(delta,0))+min(max(delta),0)-r)
                    if d<0.02: overlaps.append((d,link,key))
            print(label,'cover world overlaps', sorted(overlaps)[:15])
