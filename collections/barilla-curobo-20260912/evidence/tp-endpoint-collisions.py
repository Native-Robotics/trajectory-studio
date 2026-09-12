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
    for i,p in enumerate(task.parts):
        po=SimplifiedPlanningObjectFactory.create(planning_object_by_part(p))
        detector=SolutionCollisionDetector(po,p.collision_gap,c['TrajectoryPlanner']['Planner']['Collisions']['default_self_collision_min_distance'],200,p.validation_link_id_list)
        print('part',i,'ignored',p.ignore_collisions,'gap',p.collision_gap,'validation',p.validation_link_id_list)
        for label,node,t in [('start',p.start,0.),('target',p.target,1.)]:
            hitbox=po.get_simplified_hitbox_at_state(node.position.value,p.validation_link_id_list)
            obs=detector._detect_obstacle_collisions_at_time(t,0.,1.,hitbox,p.collision_gap,False)
            selfc=detector._detect_self_collisions_at_time(t,0.,1.,hitbox)
            print(label,'obstacle',str(obs),'self',str(selfc))
