/**
 * series.js
 * Chart series and discontinuity detection for piecewise cubic trajectories.
 * Pure functions (no DOM), so they can be tested under node.
 */

import { getJointCount, listSegments, evaluateSegment } from './robot.js?v=37';

const METRIC_KEYS = { position: 'q', velocity: 'v', acceleration: 'a', jerk: 'j' };

/** Segments with positive length, in time order. */
function spans(trajData) {
  return listSegments(trajData).filter(s => s.t1 > s.t0);
}

/**
 * Builds one {x, y} series per joint for a metric.
 *
 * Position, velocity and acceleration are sampled at both ends of every
 * segment plus a uniform grid of `gridCount` points over the whole
 * trajectory. Each knot therefore appears twice: the left limit (end of the
 * previous segment) and the right limit (start of the next one), so an
 * acceleration step is drawn as a vertical edge and 7 ms edge segments are
 * never skipped.
 *
 * Jerk is constant per segment (6 c3), so it is drawn as exact steps: two
 * points per segment at its start and end knots, with vertical transitions
 * between segments. No interpolation.
 *
 * @param {Object} trajData - The contents of the .traj file
 * @param {string} metric - 'position' | 'velocity' | 'acceleration' | 'jerk'
 * @param {number} [gridCount=400] - Dense grid size over the full duration
 * @returns {Array<Array<{x:number, y:number}>>}
 */
export function buildMetricSeries(trajData, metric, gridCount = 400) {
  const key = METRIC_KEYS[metric] || 'q';
  const numJoints = getJointCount(trajData);
  const series = Array.from({ length: numJoints }, () => []);
  const segments = spans(trajData);
  if (segments.length === 0) return series;

  const push = (t, values) => {
    for (let j = 0; j < numJoints; j++) series[j].push({ x: t, y: values[j] });
  };

  if (key === 'j') {
    for (const seg of segments) {
      const { j } = evaluateSegment(seg, 0, numJoints);
      push(seg.t0, j);
      push(seg.t1, j);
    }
    return series;
  }

  const tStart = segments[0].t0;
  const tEnd = segments[segments.length - 1].t1;
  const dt = (tEnd - tStart) / Math.max(1, gridCount - 1);
  const eps = 1e-9;

  for (const seg of segments) {
    const times = [seg.t0];
    let i = Math.max(0, Math.floor((seg.t0 - tStart) / dt));
    for (; tStart + i * dt < seg.t1 - eps; i++) {
      const t = tStart + i * dt;
      if (t > seg.t0 + eps) times.push(t);
    }
    times.push(seg.t1);
    for (const t of times) {
      push(t, evaluateSegment(seg, t - seg.t0, numJoints)[key]);
    }
  }
  return series;
}

/**
 * Finds acceleration steps: times where the left and right limits of a joint's
 * acceleration differ by more than `tolerance`. At such a step the jerk is an
 * impulse of size `step` (rad/s^2).
 *
 * Checked at every inner knot ('knot'), at part junctions ('junction'), and
 * at the trajectory start/end ('start'/'end') for joints that are at rest
 * there (|v| <= restTolerance), where the acceleration outside the trajectory
 * is 0.
 *
 * @param {Object} trajData - The contents of the .traj file
 * @param {Object} [options]
 * @param {number} [options.tolerance=1e-3] - Minimum |step| in rad/s^2
 * @param {number} [options.restTolerance=1e-3] - Max |v| in rad/s to count as at rest
 * @returns {Array<{t:number, joint:number, before:number, after:number, step:number, kind:string}>}
 */
export function detectAccelerationSteps(trajData, { tolerance = 1e-3, restTolerance = 1e-3 } = {}) {
  const segments = spans(trajData);
  const steps = [];
  if (segments.length === 0 || (trajData.status !== undefined && trajData.status !== 70)) return steps;
  const numJoints = getJointCount(trajData);

  const add = (t, joint, before, after, kind) => {
    const step = after - before;
    if (Math.abs(step) > tolerance) steps.push({ t, joint, before, after, step, kind });
  };

  const first = segments[0];
  const start = evaluateSegment(first, 0, numJoints);
  for (let j = 0; j < numJoints; j++) {
    if (Math.abs(start.v[j]) <= restTolerance) add(first.t0, j, 0, start.a[j], 'start');
  }

  for (let s = 0; s + 1 < segments.length; s++) {
    const left = segments[s];
    const right = segments[s + 1];
    const before = evaluateSegment(left, left.t1 - left.t0, numJoints).a;
    const after = evaluateSegment(right, 0, numJoints).a;
    const kind = left.partIndex !== right.partIndex ? 'junction' : 'knot';
    for (let j = 0; j < numJoints; j++) add(right.t0, j, before[j], after[j], kind);
  }

  const last = segments[segments.length - 1];
  const end = evaluateSegment(last, last.t1 - last.t0, numJoints);
  for (let j = 0; j < numJoints; j++) {
    if (Math.abs(end.v[j]) <= restTolerance) add(last.t1, j, end.a[j], 0, 'end');
  }
  return steps;
}

/**
 * Groups steps that happen at the same time, largest |step| first.
 * @returns {Array<{t:number, kind:string, steps:Array}>}
 */
export function groupStepsByTime(steps, timeTolerance = 1e-9) {
  const groups = [];
  for (const step of steps) {
    let group = groups.find(g => Math.abs(g.t - step.t) <= timeTolerance);
    if (!group) {
      group = { t: step.t, kind: step.kind, steps: [] };
      groups.push(group);
    }
    group.steps.push(step);
  }
  groups.forEach(g => g.steps.sort((a, b) => Math.abs(b.step) - Math.abs(a.step)));
  return groups.sort((a, b) => a.t - b.t);
}
