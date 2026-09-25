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

test('Link 1 column cylinder connects towards base for both positive and negative alpha0', () => {
  class MockVec3 {
    constructor(x, y, z) { this.x = x; this.y = y; this.z = z; }
    normalize() {
      const l = Math.sqrt(this.x * this.x + this.y * this.y + this.z * this.z) || 1;
      return new MockVec3(this.x / l, this.y / l, this.z / l);
    }
  }
  class MockQuat {
    constructor() { this.x = 0; this.y = 0; this.z = 0; this.w = 1; }
    set(x, y, z, w) { this.x = x; this.y = y; this.z = z; this.w = w; }
    setFromUnitVectors() {}
  }
  class MockMesh {
    constructor(geo, mat) {
      this.geo = geo;
      this.mat = mat;
      this.position = { x: 0, y: 0, z: 0, set(x, y, z) { this.x = x; this.y = y; this.z = z; } };
      this.quaternion = new MockQuat();
    }
  }
  class MockGroup {
    constructor() {
      this.children = [];
      this.matrix = { identity() {} };
    }
    add(obj) { this.children.push(obj); }
    remove(obj) { const i = this.children.indexOf(obj); if (i >= 0) this.children.splice(i, 1); }
  }
  const MockTHREE = {
    CylinderGeometry: class { rotateX() {} },
    BufferGeometry: class { setFromPoints() { return this; } },
    LineDashedMaterial: class {},
    Line: class { computeLineDistances() {} position = { set() {} }; },
    Mesh: MockMesh,
    Vector3: MockVec3,
    Quaternion: MockQuat,
  };
  const Viewer = vm.runInNewContext(source + '\nTrajectoryViewer;', {
    requestAnimationFrame: () => {}, THREE: MockTHREE,
    getRobotConfig: () => ({ pedestalRadius: 0.15, columnRadius: 0.13, jointRingRadii: [0.1], jointRingHeights: [0.1] })
  });
  const viewer = Object.create(Viewer.prototype);
  viewer.robotGroup = { position: { set() {} }, quaternion: { set() {} } };
  viewer.robotMaterials = { solid: {}, joint: {}, xray: {} };
  viewer.linkGroups = Array.from({ length: 7 }, () => new MockGroup());

  // Test with Doosan (alpha[0] = -pi/2, d[0] = 0.3443)
  viewer.buildRobot({
    equipment_model: {
      model_name: 'doosan-h2017',
      position: [0, 0, 0.95],
      dh_parameters: {
        d: [0.3443, 0, 0, 0.734, 0, 0.121],
        alpha: [-Math.PI / 2, 0, -Math.PI / 2, Math.PI / 2, -Math.PI / 2, 0],
      }
    }
  });

  const doosanCol = viewer.linkGroups[1].children.find(c => c.name === 'hitbox');
  assert.ok(doosanCol, 'Doosan hitbox column cylinder should be created');
  assert.ok(doosanCol.position.y > 0.1, 'Doosan column position.y should be positive towards base');
  assert.equal(doosanCol.position.y.toFixed(4), (0.3443 / 2).toFixed(4));

  // Test with Aubo (alpha[0] = +pi/2, d[0] = 0.2105)
  viewer.buildRobot({
    equipment_model: {
      model_name: 'aubo-is25',
      position: [0, 0, 1.12],
      dh_parameters: {
        d: [0.2105, 0, 0, 0.208, 0.125, 0.1083],
        alpha: [Math.PI / 2, 0, 0, Math.PI / 2, -Math.PI / 2, 0],
      }
    }
  });

  const auboCol = viewer.linkGroups[1].children.find(c => c.name === 'hitbox');
  assert.ok(auboCol, 'Aubo hitbox column cylinder should be created');
  assert.ok(auboCol.position.y < -0.1, 'Aubo column position.y should be negative towards base');
  assert.equal(auboCol.position.y.toFixed(4), (-0.2105 / 2).toFixed(4));
});

