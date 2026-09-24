# Studio idle rendering

The viewer previously submitted a complete Three.js render on every animation
frame, including while paused. It now renders when scene data is dirty, camera
controls change, or custom zoom damping moves the camera. Resize, pose, marker,
visibility, robot/obstacle/path rebuilding, editor changes, and WebGL context
restoration invalidate the frame. The lightweight animation loop still runs to
support damping. This is not an event-only scheduler.

Ported from `curobo-studio` (commit `10ab9a0`), where it was
validated on 2026-09-13:

- `tests/viewer-rendering.test.mjs` (`node --test tests/*.test.mjs`): the idle regression
  failed on the original viewer with 121 render submissions rather than one
  across the initial frame and 120 ticks.
- Real browser, instrumented viewer: settled and paused windows submitted zero
  renders; 30 playback frames submitted 29 renders. Zoom and orbit submitted
  41 and 31 renders then settled. Scrub, resize, entering/leaving edit mode,
  moving an editor handle, and clearing the path each rendered once then settled.

These are render submission counts, not CPU/GPU utilization measurements.
Any new code that mutates the scene outside the viewer's methods must set
`viewer.needsRender = true`.
