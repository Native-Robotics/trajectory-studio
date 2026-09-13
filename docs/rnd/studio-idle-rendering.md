# Studio idle rendering

The viewer previously submitted a complete Three.js render on every animation
frame, including while paused. It now renders when scene data is dirty, camera
controls change, or custom zoom damping moves the camera. Resize, pose, marker,
visibility, robot/obstacle/path rebuilding, editor changes, and WebGL context
restoration invalidate the frame. The lightweight animation loop still runs to
support damping. This is not an event-only scheduler.

Applied to the root viewer and the fast and smoother production collections.
Their app and viewer import URLs are versioned together. Motion data is unchanged.

Validation on 2026-09-13:

- Node tests: 14 passed. The new idle regression failed on the original viewer
  with 121 render submissions rather than one across the initial and 120 ticks.
- Real browser, instrumented actual viewer: settled and paused windows submitted
  zero renders; 30 playback frames submitted 29 renders. Zoom and orbit submitted
  41 and 31 renders then settled. Scrub, resize, entering/leaving edit mode,
  moving an editor handle, and clearing the path each rendered once then settled.
- No browser page errors in that run. See `tests/viewer-browser-check.js` for the
  repeatable Playwright probe. It instruments a disposable test page only.
- Uninstrumented served smoother collection loaded viewer.js?v=idle-render-1.
  Existing Chrome Studio tab was refreshed and its robot, path, and charts were
  visually verified.

These are render submission counts, not CPU/GPU utilization or planner timing
measurements. Do not derive planner speedup claims from them. Busy-period planner
measurements remain excluded; fresh uncontended benchmarks are still needed.
