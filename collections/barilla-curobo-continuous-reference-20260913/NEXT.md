# Continuous-motion R&D checkpoint

The task-2 example is an offline prototype. `adaptive-curobo` takes 6.322853 s versus 7.564003 s for the original cuRobo path. Exact-export checks in `verification.json` cover sampled Cartesian constraints, analytic joint extrema, recorded caps, and original FCL. It is not integrated production functionality.

Since this pilot, planner commit `482b8ac533c3b9163aa45ac7c697299565fbf77e` fixed deserialization and enforcement of recorded joint velocity, acceleration and jerk arrays. The corrected production replay solved all 135 tasks with those checks. Its source collection is `barilla-curobo-joint-limits-20260913`; the existing `barilla-curobo-reference-20260913` pairs now use that baseline.

A generic offline runner now handles compatible fixed-TCP motion parts. It uses a quintic geometry polish, wrist refinement, arc-length parameterization, constrained squared-speed timing, speed reduction around joins, and continuous endpoint ramps. A conic timing solver replaces the slower SLSQP experiment. Changing TCPs, required waypoint velocities and incompatible joins remain guarded cases. Rejected or slower candidates must retain the corrected baseline.

Next integration work:

1. Extract readable production modules with optional dependency/configuration, no artifact paths or task IDs, and an explicit compatibility predicate. Preserve mandatory waypoint derivatives and collision-policy boundaries.
2. Apply continuous timing as an opt-in candidate, accept only after emitted-spline qualification and original FCL, and retain the fully qualified baseline when it fails or is slower. Do not alter CPU planner defaults.
3. Add meaningful analytical timing, endpoint/continuity, constraint rejection and fallback tests. Replay the full corpus through the actual worker after integration.
4. Benchmark end-to-end planning and CPU/GPU resources separately from motion duration and the timing optimizer's local speed.
5. Investigate collision-rejected geometry with more path anchors or obstacle-aware refinement; do not promote a candidate solely for shorter duration.

Core worktree: `/home/luke/.codex/worktrees/tp-curobo-core`. Studio worktree: `/home/luke/.codex/worktrees/studio-barilla-rebuild`. Unrelated self-collider reuse work is parked under `/tmp/curobo-rnd/pending-self-collider-reuse.patch` and must not be bundled accidentally.
