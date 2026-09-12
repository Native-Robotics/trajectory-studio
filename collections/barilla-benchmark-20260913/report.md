# cuRobo vs develop: first ten-task comparison

All 20 fresh production-planner runs reported SOLVED. Under a common audit, cuRobo passed 10/10; develop passed 0/10 because its paths exceed the recorded 1 m/s² TCP acceleration limit. All 20 passed the collision audit.

The current cuRobo integration is not a speed/resource improvement on this sample. It gives continuous acceleration and respects the audited limits, but motion is substantially longer. Develop is faster and lighter, but its emitted paths need constraint and part-join fixes.

## Median measurements

| Metric | develop | cuRobo |
|---|---:|---:|
| Planning latency (s) | 9.01 | 12.5 |
| Whole process wall time (s) | 9.52 | 13.1 |
| CPU work (CPU-s) | 9.15 | 12.2 |
| Peak summed process RSS (MiB) | 320 | 1.58e+03 |
| Peak compute GPU memory (MiB) | 0 | 376 |
| Motion duration (s) | 1.92 | 8.44 |
| Joint mileage (rad) | 5.62 | 5.36 |
| Vector RMS jerk (rad/s³; excludes jumps) | 41.1 | 1.48 |
| Normalized jerk (dimensionless; excludes jumps) | 9.91e+03 | 5.86e+04 |
| Maximum acceleration jump (rad/s²) | 4.52 | 1.5e-12 |
| Peak TCP acceleration (m/s²) | 7.48 | 0.601 |

## Per-task comparison

Times below are planning latency and motion duration. CPU seconds, memory, exact polynomial metrics and audit details are included in comparison.json.

| Task | Move | Planning s (dev / GPU) | Motion s (dev / GPU) | TCP acceleration m/s² (dev / GPU) | Overall quality index |
|---|---|---:|---:|---:|---|
| 3 | Wait | 12.23 / 13.13 | 1.80 / 10.13 | 8.64 / 0.54 | N/A: develop fails common audit |
| 4 | Pick | 22.43 / 11.92 | 2.04 / 10.13 | 10.45 / 0.90 | N/A: develop fails common audit |
| 21 | Wait | 9.81 / 11.32 | 2.14 / 6.75 | 9.38 / 0.92 | N/A: develop fails common audit |
| 54 | Wait | 8.11 / 11.72 | 2.06 / 8.44 | 7.11 / 0.46 | N/A: develop fails common audit |
| 59 | Pick | 13.03 / 16.52 | 2.50 / 11.81 | 5.86 / 0.53 | N/A: develop fails common audit |
| 69 | Wait | 12.12 / 13.73 | 2.11 / 8.44 | 6.08 / 0.49 | N/A: develop fails common audit |
| 95 | Wait | 5.12 / 11.62 | 1.77 / 6.75 | 10.68 / 0.90 | N/A: develop fails common audit |
| 118 | Wait | 5.32 / 11.92 | 1.65 / 6.75 | 7.12 / 0.65 | N/A: develop fails common audit |
| 119 | Pick | 7.31 / 14.51 | 1.79 / 10.13 | 6.28 / 0.57 | N/A: develop fails common audit |
| 133 | Wait | 8.21 / 14.41 | 1.70 / 6.75 | 7.83 / 0.64 | N/A: develop fails common audit |

## Quality score and smoothness

Overall quality index is deliberately N/A for every pair: neither faster invalid motion nor slower valid motion earns an honest paired overall ranking. Acceleration continuity is an additional smoothness criterion, not an explicitly requested equality: the original intermediate nodes allow an acceleration range. The planned experimental score is 100 × [(develop duration / candidate duration) × (develop mileage / candidate mileage) × (develop normalized jerk / candidate normalized jerk)]^(1/3), only when both candidates pass the common audit. Develop would be 100, higher is better; equal weights, resources excluded. This is not an industry standard.

Normalized jerk = T⁵ × integral(sum of squared joint jerk) / sum of squared per-joint mileage. It is invariant to uniform slowdown. Physical jerk is much lower for cuRobo, but much of that benefit follows from longer duration. Its normalized jerk is higher. However, develop has acceleration jumps at part joins: ordinary polynomial jerk integrals omit the impulses at those jumps, so normalized jerk alone cannot fairly rank overall smoothness. CuRobo keeps acceleration continuous to numerical precision.

## Offline slowdown diagnostic

Separately slowed each develop path by max(TCP speed ratio, sqrt(TCP acceleration ratio), 1) × 1.02. This is postprocessing, not develop planner output and not included in measured planning time. It preserves spatial paths. All ten then meet the sampled TCP limits, but still fail common acceleration-continuity checks. This demonstrates that slowdown alone does not repair the emitted joins.

| Task | Slowdown | Original / slowed dev / GPU duration s | Slowed dev max acceleration jump rad/s² |
|---|---:|---:|---:|
| 3 | 3.00× | 1.80 / 5.39 / 10.13 | 0.460 |
| 4 | 3.30× | 2.04 / 6.73 / 10.13 | 0.370 |
| 21 | 3.12× | 2.14 / 6.70 / 6.75 | 0.396 |
| 54 | 2.72× | 2.06 / 5.59 / 8.44 | 0.764 |
| 59 | 2.47× | 2.50 / 6.17 / 11.81 | 0.745 |
| 69 | 2.52× | 2.11 / 5.31 / 8.44 | 0.712 |
| 95 | 3.33× | 1.77 / 5.88 / 6.75 | 0.549 |
| 118 | 2.72× | 1.65 / 4.49 / 6.75 | 0.725 |
| 119 | 2.56× | 1.79 / 4.58 / 10.13 | 0.648 |
| 133 | 2.85× | 1.70 / 4.86 / 6.75 | 0.695 |

## Why the earlier corpus failed

- Place: 0/64 solved. Pick: 14/34. Wait: 32/37.
- 88 failures reported no solution for part index 1 (the second part); one rejects changing TCP within a part. All 18 regression-catalog cases failed.
- In the diagnosed task 0, original FCL accepts the endpoints with configured clearance, while the conservative link-6 sphere cover has only 4.05 mm start clearance and penetrates the target box by 0.955 mm. This demonstrates an overly conservative approximation for that case, not the cause of all 88 failures.
- Every saved cuRobo success required whole-task slowdown (2.25×–5.0625×). The adapter also imposes rest at each part boundary and constructs a planner/model per part.

## Method and limitations

- Selection fixed before reruns: 7 Wait and 3 Pick, evenly spaced within the 46 saved successes. IDs: 3, 4, 21, 54, 59, 69, 95, 118, 119, 133. No Place tasks qualify for this sample.
- Local develop 90a41227 versus cuRobo dc33c11e. Both use the production Planner API in fresh processes and the same Python 3.12 runtime/dependencies; one worker, one BLAS/OpenMP thread, alternating backend order. This is not a warm persistent-planner or maximum-throughput benchmark.
- One trial per task/backend, 180-second timeout. No errors/timeouts. Python/NumPy/hash seeds configured; GPU stochastic reproducibility is not guaranteed. Caches may persist between fresh processes.
- RTX 4060 Ti, NVIDIA 610.57.04. Existing desktop/Studio and a background backup remained active; this is a practical local measurement, not an isolated lab benchmark.
- CPU-s includes child CPU work. Process wall time includes startup/shutdown and up to 0.2 s polling tail. Planning time excludes imports and Planner initialization but includes queueing and built-in validation.
- Resource sampling every 0.2 s. Summed RSS may double-count shared pages; peaks may be missed. GPU compute memory is attributed to the process tree. GPU utilization/power are whole-device and include desktop activity, so they are retained in raw data but not called planner energy consumption.
- Common audit uses original recorded constraints plus shared audit bounds: joint acceleration 100 rad/s², jerk 10000 rad/s³, line corridor 2 mm, orientation 0.01 rad and continuity tolerance 0.001. Missing endpoint derivative defaults are not imposed from either backend. The TCP acceleration rejection is against an explicitly recorded 1 m/s² limit.
- Joint extrema, travel, derivative integrals and one-sided jumps are analytic on the emitted cubic coefficients. TCP/dynamics/collision checks are sampled; not continuous-time proofs. Reconstructed splines are checked against the original q/v/a before qualification.
- Six analytic metric tests pass; all output pairs audited. No claim of a whole-corpus winner or statistical significance.

## Next work

1. Fix develop TCP-limit deserialization/enforcement and acceleration continuity at stitched part joins, then repeat this benchmark.
2. Fix cuRobo collision-model conservatism and inspect representative failed Place/Pick/Wait cases.
3. Improve cuRobo timing through planner reuse, better time allocation, selective retiming and compatible blended joins. Then measure persistent warmed runs and multiple repetitions.

Viewer files retain the native SOLVED status for evaluating saved splines; audit_status and collection filter status record common-audit failure. Rejected paths are inspectable with an explicit warning.
Raw evidence: /home/luke/.codex/visualizations/2026/09/12/01a0969d-cc8b-77e1-8566-8b3bd1679634/curobo-benchmark-20260913

## Per-task resources

| Task | CPU-s DEV / GPU | Peak summed RSS MiB DEV / GPU | GPU compute memory MiB DEV / GPU |
|---|---:|---:|---:|
| 3 | 12.18 / 11.88 | 616 / 1581 | 0 / 382 |
| 4 | 22.37 / 12.20 | 451 / 1852 | 0 / 448 |
| 21 | 9.90 / 11.61 | 347 / 1580 | 0 / 374 |
| 54 | 8.15 / 12.05 | 319 / 1838 | 0 / 446 |
| 59 | 13.15 / 16.81 | 329 / 1845 | 0 / 448 |
| 69 | 12.21 / 14.04 | 320 / 1562 | 0 / 374 |
| 95 | 5.24 / 11.86 | 298 / 1557 | 0 / 374 |
| 118 | 5.49 / 12.25 | 290 / 1555 | 0 / 374 |
| 119 | 7.53 / 14.88 | 313 / 1557 | 0 / 378 |
| 133 | 8.40 / 14.73 | 248 / 1589 | 0 / 374 |

## Per-task smoothness

| Task | Mileage rad DEV / GPU | RMS jerk rad/s³ DEV / GPU | Normalized jerk DEV / GPU | Max acceleration jump rad/s² DEV / GPU |
|---|---:|---:|---:|---:|
| 3 | 5.236 / 5.438 | 41.047 / 0.578 | 9835 / 60607 | 4.136 / 6.7e-13 |
| 4 | 5.996 / 5.276 | 48.788 / 1.148 | 23084 / 234326 | 4.024 / 1.5e-12 |
| 21 | 9.177 / 8.673 | 48.027 / 3.392 | 9404 / 47176 | 3.868 / 6.7e-12 |
| 54 | 9.663 / 9.397 | 34.418 / 1.649 | 3022 / 33609 | 5.654 / 1.5e-12 |
| 59 | 10.474 / 10.041 | 41.083 / 1.156 | 11825 / 107593 | 4.543 / 1.5e-12 |
| 69 | 9.037 / 8.796 | 38.458 / 1.529 | 4094 / 26689 | 4.502 / 1.5e-12 |
| 95 | 4.088 / 4.120 | 45.893 / 1.601 | 10316 / 39187 | 6.100 / 2.2e-12 |
| 118 | 4.280 / 4.176 | 43.319 / 2.069 | 8864 / 97392 | 5.367 / 2.2e-12 |
| 119 | 3.847 / 3.522 | 37.486 / 0.841 | 14527 / 264918 | 4.232 / 1e-12 |
| 133 | 3.328 / 3.229 | 37.766 / 1.435 | 9984 / 56542 | 5.667 / 3e-12 |
