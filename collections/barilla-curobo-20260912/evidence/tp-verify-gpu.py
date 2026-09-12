import sys, tempfile, json
sys.path.insert(0,'/home/luke/.codex/worktrees/tp-curobo-core')
sys.argv[0]='/home/luke/.codex/worktrees/tp-curobo-core/main.py'
import torch
x=torch.arange(1024, device='cuda', dtype=torch.float32)
assert torch.sum(x*x).item()==357389824
print('CUDA tensor passed:',torch.cuda.get_device_name(), torch.__version__,flush=True)
from nrutils.config import parse_config
parse_config()
import planner
from snippets.replay_curobo import extract_tasks
from pathlib import Path
from serialization.schemas import TaskSchema
from planner.cores import core_override
from planner.planning_object.common_planning_object_factory import planning_object_by_part
from planner.optimization_core.simplified_planning_object_factory import SimplifiedPlanningObjectFactory
from planner.optimization_core.curobo.model import build_model
from curobo._src.robot.kinematics.kinematics import Kinematics
from curobo._src.types.robot import RobotCfg
from curobo.types import DeviceCfg, JointState
from scipy.spatial.transform import Rotation
import numpy as np
with core_override('CuRoboPlanner'):
    part=TaskSchema().load(extract_tasks(Path('/home/luke/git/TrajectoryPlanner/logs/trajectoryplanner-2026-09-09_14-15-27.log'))[0]).parts[0]
    po=SimplifiedPlanningObjectFactory.create(planning_object_by_part(part))
    with tempfile.TemporaryDirectory() as out:
        robot,_,names=build_model(part,po,Path(out))
        device=DeviceCfg()
        kin=Kinematics(RobotCfg.create(robot['robot_cfg'],device).kinematics)
        worst=0
        for q in [part.start.position.value,part.target.position.value,*np.random.default_rng(12).uniform(-1,1,(20,part.dof))]:
            state=kin.compute_kinematics(JointState.from_position(device.to_device(np.array(q).reshape(1,-1)),joint_names=names))
            pose=state.tool_poses
            matrix=np.eye(4)
            matrix[:3,3]=pose.position.detach().cpu().numpy().reshape(-1,3)[0]
            wxyz=pose.quaternion.detach().cpu().numpy().reshape(-1,4)[0]
            matrix[:3,:3]=Rotation.from_quat(wxyz[[1,2,3,0]]).as_matrix()
            expected=np.array(po.forward_kinematics(q)[-1].transform_matrix,dtype=float)@part.target_tcp.transform_matrix
            worst=max(worst,float(np.max(np.abs(matrix-expected))))
            np.testing.assert_allclose(matrix,expected,atol=5e-5)
        print('GPU AUBO FK passed 22 poses; max matrix error',worst,flush=True)
