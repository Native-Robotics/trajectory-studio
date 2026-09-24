/**
 * robot.js
 * Kinematics calculations and cubic spline evaluation for n-DOF arms.
 */

// Helper to convert Quaternion [w, x, y, z] to 4x4 transform matrix
export function quatToMatrix(q, pos = [0, 0, 0]) {
  const w = q[0];
  const x = q[1];
  const y = q[2];
  const z = q[3];

  const m00 = 1 - 2*y*y - 2*z*z;
  const m01 = 2*x*y - 2*z*w;
  const m02 = 2*x*z + 2*y*w;

  const m10 = 2*x*y + 2*z*w;
  const m11 = 1 - 2*x*x - 2*z*z;
  const m12 = 2*y*z - 2*x*w;

  const m20 = 2*x*z - 2*y*w;
  const m21 = 2*y*z + 2*x*w;
  const m22 = 1 - 2*x*x - 2*y*y;

  return [
    m00, m01, m02, pos[0],
    m10, m11, m12, pos[1],
    m20, m21, m22, pos[2],
    0,   0,   0,   1
  ];
}

// Matrix multiplication: A * B (4x4 flat arrays)
export function multiplyMatrices(A, B) {
  const C = new Array(16);
  for (let i = 0; i < 4; i++) {
    for (let j = 0; j < 4; j++) {
      let sum = 0;
      for (let k = 0; k < 4; k++) {
        sum += A[i * 4 + k] * B[k * 4 + j];
      }
      C[i * 4 + j] = sum;
    }
  }
  return C;
}

// Convert 4x4 matrix rotation component to Quaternion [w, x, y, z]
export function matrixToQuat(m) {
  // m is 16-element flat array
  const r00 = m[0], r01 = m[1], r02 = m[2];
  const r10 = m[4], r11 = m[5], r12 = m[6];
  const r20 = m[8], r21 = m[9], r22 = m[10];

  const tr = r00 + r11 + r22;
  let w, x, y, z;

  if (tr > 0) {
    const S = Math.sqrt(tr + 1.0) * 2;
    w = 0.25 * S;
    x = (r21 - r12) / S;
    y = (r02 - r20) / S;
    z = (r10 - r01) / S;
  } else if ((r00 > r11) && (r00 > r22)) {
    const S = Math.sqrt(1.0 + r00 - r11 - r22) * 2;
    w = (r21 - r12) / S;
    x = 0.25 * S;
    y = (r01 + r10) / S;
    z = (r02 + r20) / S;
  } else if (r11 > r22) {
    const S = Math.sqrt(1.0 + r11 - r00 - r22) * 2;
    w = (r02 - r20) / S;
    x = (r01 + r10) / S;
    y = 0.25 * S;
    z = (r12 + r21) / S;
  } else {
    const S = Math.sqrt(1.0 + r22 - r00 - r11) * 2;
    w = (r10 - r01) / S;
    x = (r02 + r20) / S;
    y = (r12 + r21) / S;
    z = 0.25 * S;
  }

  // Normalize
  const len = Math.sqrt(w*w + x*x + y*y + z*z);
  return [w/len, x/len, y/len, z/len];
}

// Compute DH matrix for joint index
export function getDHMatrixStandard(theta, d, a, alpha) {
  const c_th = Math.cos(theta);
  const s_th = Math.sin(theta);
  const c_al = Math.cos(alpha);
  const s_al = Math.sin(alpha);

  return [
    c_th, -s_th * c_al,  s_th * s_al, a * c_th,
    s_th,  c_th * c_al, -c_th * s_al, a * s_th,
    0.0,   s_al,         c_al,        d,
    0.0,   0.0,          0.0,         1.0
  ];
}

/**
 * Computes Forward Kinematics for a given joint state and DH parameters
 * @param {Array<number>} q - Joint angles (one per DH row)
 * @param {Object} dh - DH parameters (a, d, alpha, theta offsets)
 * @param {Array<number>} baseTransform - Flat 4x4 matrix of the base pose in the world
 * @returns {Array<Array<number>>} - Link transformations in the world frame (T0, T1, ... Tn);
 *   the last entry is the flange.
 */
export function computeForwardKinematics(q, dh, baseTransform) {
  const a = dh.a;
  const d = dh.d;
  const alpha = dh.alpha;
  const thetaOffsets = dh.theta;
  const numJoints = Math.min(a.length, d.length, alpha.length, thetaOffsets.length);

  const linkTransforms = [baseTransform]; // T_base is index 0
  let T_curr = baseTransform;

  for (let i = 0; i < numJoints; i++) {
    const th = thetaOffsets[i] + (q[i] || 0);
    const Ti = getDHMatrixStandard(th, d[i], a[i], alpha[i]);
    T_curr = multiplyMatrices(T_curr, Ti);
    linkTransforms.push(T_curr); // linkTransforms[i+1] is T_joint_(i+1)_world
  }

  return linkTransforms;
}

/**
 * Number of joints in a trajectory, taken from the spline data
 * (coeffs[joint][order][segment]), else from targetState. Robots can have
 * 5 (Doosan P3020) or 6 joints, so nothing here assumes a fixed count.
 * @param {Object} trajData - The contents of the .traj file
 * @returns {number}
 */
export function getJointCount(trajData) {
  const part = (trajData && trajData.parts || []).find(p => Array.isArray(p.coeffs) && p.coeffs.length > 0);
  if (part) return part.coeffs.length;
  if (trajData && Array.isArray(trajData.targetState) && trajData.targetState.length > 0) {
    return trajData.targetState.length;
  }
  return 6;
}

/**
 * Flattens all parts into their cubic segments, in time order.
 * Knots are absolute times and consecutive parts share their boundary knot.
 * @param {Object} trajData - The contents of the .traj file
 * @returns {Array<{partIndex:number, index:number, t0:number, t1:number, coeffs:Array}>}
 */
export function listSegments(trajData) {
  const segments = [];
  (trajData && trajData.parts || []).forEach((part, partIndex) => {
    const knots = part.knots || [];
    for (let k = 0; k + 1 < knots.length; k++) {
      segments.push({ partIndex, index: k, t0: knots[k], t1: knots[k + 1], coeffs: part.coeffs });
    }
  });
  return segments;
}

/**
 * Evaluates one cubic segment at local time h = t - t0.
 * q = c3 h^3 + c2 h^2 + c1 h + c0, jerk = 6 c3 (constant per segment).
 * Evaluating the left segment at h = t1 - t0 gives the left limit at a knot,
 * evaluating the right segment at h = 0 gives the right limit.
 */
export function evaluateSegment(segment, h, numJoints) {
  const q = new Array(numJoints).fill(0);
  const v = new Array(numJoints).fill(0);
  const a = new Array(numJoints).fill(0);
  const j = new Array(numJoints).fill(0);
  const k = segment.index;
  for (let joint = 0; joint < numJoints; joint++) {
    const c = segment.coeffs[joint];
    if (!c) continue;
    const c3 = c[0][k];
    const c2 = c[1][k];
    const c1 = c[2][k];
    const c0 = c[3][k];
    q[joint] = ((c3 * h + c2) * h + c1) * h + c0;
    v[joint] = (3 * c3 * h + 2 * c2) * h + c1;
    a[joint] = 6 * c3 * h + 2 * c2;
    j[joint] = 6 * c3;
  }
  return { q, v, a, j };
}

/**
 * Evaluates spline parameters at time t
 * @param {Object} trajData - The contents of the .traj file
 * @param {number} t - Time in seconds
 * @returns {Object} - Joint kinematics (q, v, a, j), one entry per joint
 */
export function evaluateSpline(trajData, t) {
  const numJoints = getJointCount(trajData);
  const zeros = () => new Array(numJoints).fill(0);

  // If planning failed or there are no parts, return static targetState
  if (trajData.status !== 70 || !trajData.parts || trajData.parts.length === 0) {
    const targetState = trajData.targetState || zeros();
    return { q: targetState, v: zeros(), a: zeros(), j: zeros() };
  }

  const segments = listSegments(trajData);
  if (segments.length === 0) {
    const targetState = trajData.targetState || zeros();
    return { q: targetState, v: zeros(), a: zeros(), j: zeros() };
  }

  // Clamp to the trajectory time range
  const tStart = segments[0].t0;
  const tEnd = segments[segments.length - 1].t1;
  const tc = Math.min(Math.max(t, tStart), tEnd);

  // First segment that contains t (at a knot this is the left segment)
  let segment = segments[segments.length - 1];
  for (const s of segments) {
    if (tc >= s.t0 && tc <= s.t1) {
      segment = s;
      break;
    }
  }

  return evaluateSegment(segment, tc - segment.t0, numJoints);
}
