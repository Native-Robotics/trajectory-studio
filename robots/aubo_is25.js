/**
 * aubo_is25.js
 * Aubo iS25 kinematics (DH, limits, hitboxes) from the live OmniPack cell
 * plus visual joint-ring sizes for Trajectory Studio.
 */
import { BaseRobot } from './base.js';

export const AUBO_IS25_EQUIPMENT = {
  "model_name": "aubo-is25",
  "position": [
    0.0,
    0.0,
    1.12
  ],
  "quaternion": [
    0.7114,
    0.0,
    0.0,
    -0.7028
  ],
  "dh_parameters": {
    "a": [
      0.0,
      -0.856,
      -0.719,
      0.0,
      0.0,
      0.0
    ],
    "d": [
      0.2105,
      0.0,
      0.0,
      0.208,
      0.125,
      0.1083
    ],
    "alpha": [
      1.57079637,
      0.0,
      0.0,
      1.57079637,
      -1.57079637,
      0.0
    ],
    "theta": [
      -1.57079637,
      -1.57079637,
      0.0,
      -1.57079637,
      0.0,
      0.0
    ],
    "joint_type": [
      "Revolute",
      "Revolute",
      "Revolute",
      "Revolute",
      "Revolute",
      "Revolute"
    ]
  },
  "range_limits": [
    {
      "type": "Static",
      "joint_id": 0,
      "min_value": -6.2745,
      "max_value": 6.2745
    },
    {
      "type": "Static",
      "joint_id": 1,
      "min_value": -6.2745,
      "max_value": 6.2745
    },
    {
      "type": "Static",
      "joint_id": 2,
      "min_value": -6.2745,
      "max_value": 6.2745
    },
    {
      "type": "Static",
      "joint_id": 3,
      "min_value": -6.2745,
      "max_value": 6.2745
    },
    {
      "type": "Static",
      "joint_id": 4,
      "min_value": -6.2745,
      "max_value": 6.2745
    },
    {
      "type": "Static",
      "joint_id": 5,
      "min_value": -3.4907,
      "max_value": 3.2289
    }
  ],
  "max_velocity": [
    2.5831,
    2.5831,
    3.1067,
    5.1662,
    5.1662,
    5.1662
  ],
  "max_acceleration": [
    2.5831,
    2.5831,
    3.1067,
    5.1662,
    5.1662,
    5.1662
  ],
  "max_jerk": [
    17.2214,
    17.2214,
    20.7123,
    34.4429,
    34.4429,
    34.4429
  ],
  "hitbox": [
    {
      "link": 1,
      "shape": {
        "tag": "shoulder-girdle-base",
        "shape_type": "capsule",
        "position": [
          0.0,
          0.0,
          0.0
        ],
        "quaternion": [
          0.7071,
          -0.7071,
          0.0,
          0.0
        ],
        "radius": 0.11,
        "height": 0.125
      }
    },
    {
      "link": 2,
      "shape": {
        "tag": "shoulder-joint-2",
        "shape_type": "capsule",
        "position": [
          0.0,
          0.0,
          0.235
        ],
        "quaternion": [
          1.0,
          0.0,
          0.0,
          0.0
        ],
        "radius": 0.08,
        "height": 0.125
      }
    },
    {
      "link": 2,
      "shape": {
        "tag": "shoulder-tube",
        "shape_type": "capsule",
        "position": [
          0.41,
          0.0,
          0.246
        ],
        "quaternion": [
          0.7071,
          0.0,
          0.7071,
          0.0
        ],
        "radius": 0.08,
        "height": 0.65
      }
    },
    {
      "link": 2,
      "shape": {
        "tag": "shoulder-joint-1",
        "shape_type": "capsule",
        "position": [
          0.8525,
          0.0,
          0.246
        ],
        "quaternion": [
          1.0,
          0.0,
          0.0,
          0.0
        ],
        "radius": 0.11,
        "height": 0.13
      }
    },
    {
      "link": 2,
      "shape": {
        "tag": "shoulder-joint-1.1",
        "shape_type": "sphere",
        "position": [
          0.78,
          0.0,
          0.246
        ],
        "quaternion": [
          1.0,
          0.0,
          0.0,
          0.0
        ],
        "radius": 0.12
      }
    },
    {
      "link": 3,
      "shape": {
        "tag": "forearm-joint-2",
        "shape_type": "capsule",
        "position": [
          0.0,
          0.0,
          0.09
        ],
        "quaternion": [
          1.0,
          0.0,
          0.0,
          0.0
        ],
        "radius": 0.052,
        "height": 0.1
      }
    },
    {
      "link": 3,
      "shape": {
        "tag": "forearm-tube",
        "shape_type": "capsule",
        "position": [
          0.38,
          0.0,
          0.0825
        ],
        "quaternion": [
          0.7071,
          0.0,
          0.7071,
          0.0
        ],
        "radius": 0.05,
        "height": 0.65
      }
    },
    {
      "link": 3,
      "shape": {
        "tag": "forearm-joint-1",
        "shape_type": "sphere",
        "position": [
          0.72,
          0.0,
          0.115
        ],
        "quaternion": [
          1.0,
          0.0,
          0.0,
          0.0
        ],
        "radius": 0.08
      }
    },
    {
      "link": 4,
      "shape": {
        "tag": "wrist-base-joint",
        "shape_type": "capsule",
        "position": [
          0.0,
          0.0,
          0.005
        ],
        "quaternion": [
          1.0,
          0.0,
          0.0,
          0.0
        ],
        "radius": 0.052,
        "height": 0.08
      }
    },
    {
      "link": 5,
      "shape": {
        "tag": "wrist-joint",
        "shape_type": "capsule",
        "position": [
          0.0,
          0.0,
          -0.01
        ],
        "quaternion": [
          1.0,
          0.0,
          0.0,
          0.0
        ],
        "radius": 0.052,
        "height": 0.06
      }
    },
    {
      "link": 6,
      "shape": {
        "tag": "Cube1",
        "shape_type": "box",
        "position": [
          -0.014,
          -0.0242,
          0.048
        ],
        "quaternion": [
          0.5,
          0.0,
          0.0,
          -0.866
        ],
        "extents": [
          0.197,
          0.137,
          0.07
        ]
      }
    },
    {
      "link": 6,
      "shape": {
        "tag": "gripper-storage.unit",
        "shape_type": "box",
        "position": [
          0.03,
          0.052,
          0.2625
        ],
        "quaternion": [
          0.0,
          0.5,
          -0.866,
          0.0
        ],
        "extents": [
          0.1015,
          0.1485,
          0.1425
        ]
      }
    },
    {
      "link": 6,
      "shape": {
        "tag": "end-effector",
        "shape_type": "sphere",
        "position": [
          0.0,
          0.0,
          -0.01
        ],
        "quaternion": [
          1.0,
          0.0,
          0.0,
          0.0
        ],
        "radius": 0.052
      }
    }
  ]
};

export function createAuboIS25Repr(id) {
  return {
    desired_id: id,
    parts: [{
      start: { position: [0, 0, 0, 0, 0, 0] },
      target: { position: [0, 0, 0, 0, 0, 0] },
      wrist_down: false,
      linear: false,
      ignore_collisions: false,
      start_tcp_position: [0, 0, 0],
      start_tcp_rotation: [1, 0, 0, 0],
      target_tcp_position: [0, 0, 0],
      target_tcp_rotation: [1, 0, 0, 0],
    }],
    scene: { shapes: [] },
    equipment_model: JSON.parse(JSON.stringify(AUBO_IS25_EQUIPMENT)),
  };
}

export class AuboIS25 extends BaseRobot {
  constructor() {
    super();
    this.modelName = "aubo-is25";
    this.pedestalRadius = 0.15;
    this.columnRadius = 0.12;
    this.jointRingRadii = [0.13, 0.13, 0.095, 0.095, 0.075, 0.075];
    this.jointRingHeights = [0.13, 0.13, 0.10, 0.10, 0.08, 0.08];
    this.dh_parameters = AUBO_IS25_EQUIPMENT.dh_parameters;
    this.position = AUBO_IS25_EQUIPMENT.position;
    this.quaternion = AUBO_IS25_EQUIPMENT.quaternion;
    this.range_limits = AUBO_IS25_EQUIPMENT.range_limits;
    this.max_velocity = AUBO_IS25_EQUIPMENT.max_velocity;
  }
}
