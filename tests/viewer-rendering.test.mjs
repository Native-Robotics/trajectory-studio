import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import vm from 'node:vm';

// Execute the actual viewer; replace only browser scheduling and graphics I/O.
const source = readFileSync(new URL('../viewer.js', import.meta.url), 'utf8')
  .replace(/^import .*;$/gm, '').replace('export class', 'class');
function harness() {
  const queue = [];
  const Viewer = vm.runInNewContext(source + '\nTrajectoryViewer;', {
    requestAnimationFrame: callback => queue.push(callback), THREE: {},
  });
  const viewer = Object.create(Viewer.prototype);
  let renders = 0;
  let cameraChanged = false;
  Object.assign(viewer, {
    scene: {}, camera: { updateProjectionMatrix() {} },
    renderer: { render() { renders++; }, setSize() {} },
    controls: { update() { const changed = cameraChanged; cameraChanged = false; return changed; } },
    container: { clientWidth: 800, clientHeight: 600 },
    linkGroups: [], obstaclesGroup: { visible: true },
  });
  return { viewer, renders: () => renders, changeCamera: () => { cameraChanged = true; },
    tick() { assert.equal(queue.length, 1); queue.shift()(); } };
}

test('a settled viewer draws initially then stops submitting identical frames', () => {
  const h = harness();
  h.viewer.animate();
  for (let i = 0; i < 120; i++) h.tick();
  assert.equal(h.renders(), 1);
});

test('camera damping redraws only while camera changes', () => {
  const h = harness(); h.viewer.animate();
  h.changeCamera(); h.tick();
  assert.equal(h.renders(), 2);
  h.tick(); assert.equal(h.renders(), 2);
});

for (const [name, mutate] of [
  ['resize', viewer => viewer.onResize()],
  ['pose playback or scrubbing', viewer => viewer.updatePose([])],
  ['obstacle visibility', viewer => viewer.setObstaclesVisible(false)],
]) {
  test(`${name} redraws a paused viewer once`, () => {
    const h = harness(); h.viewer.animate();
    mutate(h.viewer); h.tick(); assert.equal(h.renders(), 2);
    h.tick(); assert.equal(h.renders(), 2);
  });
}
