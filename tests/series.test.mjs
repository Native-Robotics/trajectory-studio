import test from 'node:test';
import assert from 'node:assert/strict';
import { existsSync, readFileSync } from 'node:fs';
import { evaluateSpline, getJointCount } from '../robot.js';
import { buildMetricSeries, detectAccelerationSteps, groupStepsByTime } from '../series.js';

// coeffs[joint][order][segment], order 0..3 = c3, c2, c1, c0 on h = t - knot.
function part(knots, perJoint) {
  return { knots, coeffs: perJoint };
}

// 5-DOF, two parts. Part 0: one segment [0, 1] with a = 2*c2 + 6*c3*h.
// Part 1: segments [1, 1.007] and [1.007, 2]. J3 jumps in acceleration at the
// junction t = 1; the 7 ms segment has its own jerk.
const J = 5;
const fiveDof = {
  status: 70,
  parts: [
    part([0, 1], Array.from({ length: J }, (_, j) => [[j === 2 ? 1 : 0], [0], [0], [0]])),
    part([1, 1.007, 2], Array.from({ length: J }, (_, j) => j === 2
      ? [[-2, 0.5], [3 + 4, 0], [3, 0.1], [1, 1.02]]
      : [[0, 0], [0, 0], [0, 0], [0, 0]])),
  ],
};

test('joint count comes from the data, not a fixed 6', () => {
  assert.equal(getJointCount(fiveDof), 5);
  const state = evaluateSpline(fiveDof, 0.5);
  assert.equal(state.q.length, 5);
  assert.equal(buildMetricSeries(fiveDof, 'position').length, 5);
  assert.equal(getJointCount({ status: 1, targetState: [0, 0, 0, 0, 0] }), 5);
});

test('jerk is drawn as exact steps: two points per segment, constant between knots', () => {
  const series = buildMetricSeries(fiveDof, 'jerk')[2];
  assert.deepEqual(series.map(p => p.x), [0, 1, 1, 1.007, 1.007, 2]);
  assert.deepEqual(series.map(p => p.y), [6, 6, -12, -12, 3, 3]);
});

test('acceleration is sampled on both sides of every knot, including 7 ms segments', () => {
  const series = buildMetricSeries(fiveDof, 'acceleration', 50)[2];
  const at = t => series.filter(p => Math.abs(p.x - t) < 1e-12).map(p => p.y);
  // Junction: left limit 6 (end of part 0), right limit 14 (start of part 1)
  assert.deepEqual(at(1), [6, 14]);
  const inner = at(1.007);
  assert.equal(inner.length, 2);
  assert.ok(Math.abs(inner[0] - (14 - 12 * 0.007)) < 1e-9);
  assert.equal(inner[1], 0);
  // Times never go backwards, so Chart.js draws a function of time
  for (let i = 1; i < series.length; i++) assert.ok(series[i].x >= series[i - 1].x);
});

test('acceleration steps are detected at knots, junctions and from rest', () => {
  const steps = detectAccelerationSteps(fiveDof);
  const j3 = steps.filter(s => s.joint === 2);
  assert.deepEqual(j3.map(s => [s.t, s.kind]), [[1, 'junction'], [1.007, 'knot']]);
  assert.ok(Math.abs(j3[0].step - 8) < 1e-12);
  assert.ok(Math.abs(j3[1].step - (0 - (14 - 12 * 0.007))) < 1e-9);
  // J3 starts at rest with a = 0 and ends moving: no start/end step. Other joints never move.
  assert.equal(steps.filter(s => s.joint !== 2).length, 0);
  assert.equal(groupStepsByTime(steps).length, 2);
});

test('small differences below the tolerance are not steps', () => {
  const smooth = {
    status: 70,
    parts: [part([0, 1, 2], [[[0, 0], [1, 1 + 4e-4], [0, 2], [0, 1]]])],
  };
  assert.deepEqual(detectAccelerationSteps(smooth, { restTolerance: -1 }), []);
});

const LIVE = '/usr/share/robot/OmniPack/Trajectories/'
  + '25386f497e68bf2528496d2eb69a0fc5810e7d184124118eed9b6fd396d0ce5d.traj';

test('live trajectory 25386f49 shows the 8.83 rad/s^2 J6 step at t = 0.424 s', { skip: !existsSync(LIVE) }, () => {
  const traj = JSON.parse(readFileSync(LIVE, 'utf8'));
  const step = detectAccelerationSteps(traj).find(s => s.joint === 5 && Math.abs(s.t - 0.4242) < 1e-3);
  assert.ok(step, 'J6 step at the part junction');
  assert.equal(step.kind, 'junction');
  assert.ok(Math.abs(step.step - 8.83) < 5e-3, `step ${step.step}`);
  const group = groupStepsByTime(detectAccelerationSteps(traj)).find(g => g.t === step.t);
  assert.equal(group.steps[0].joint, 5, 'J6 is the largest step at the junction');
  const jerk = buildMetricSeries(traj, 'jerk')[5];
  const knots = traj.parts.flatMap(p => p.knots);
  assert.ok(jerk.every(p => knots.includes(p.x)), 'jerk points only at knots');
});

test('a joint at rest at the start or end steps from/to zero acceleration', () => {
  const rest = { status: 70, parts: [part([0, 1], [[[-1], [1.5], [0], [0]]])] };
  // a(0) = 3 from rest; at t = 1: v = -3 + 3 = 0, a = -6 + 3 = -3 back to rest.
  const steps = detectAccelerationSteps(rest);
  assert.deepEqual(steps.map(s => [s.t, s.kind, s.step]), [[0, 'start', 3], [1, 'end', 3]]);
});
