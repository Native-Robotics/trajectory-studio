# cuRobo and reference pairs

Open http://localhost:8001/collections/barilla-curobo-reference-20260913/index.html.

This collection contains 135 corrected cuRobo trajectories and the 135 original recorded Barilla references. Each pair shares its base identifier: `…-curobo`, then `…-ref`. Box, compute and mileage sorting keep pairs together; metric sorting uses the cuRobo value.

The cuRobo source is `barilla-curobo-joint-limits-20260913`: 135 successful tasks, audited with retained recorded joint velocity, acceleration and jerk caps (`strict-original-v2-recorded-joint-caps`). The reference source is the original root collection (132 successes and three recorded failures). Reference recordings are not newly qualified results. All 540 trajectory/representation files are exact copies of their sources; filenames and index metadata identify each pair.

`recorded-joint-limits-audit.json` describes the OLD numeric-FK collection, not the corrected cuRobo trajectories now displayed. Historical results had incomplete joint jerk enforcement. See the corrected collection's report and independent audit for the replacement data.

Rebuild with `python scripts/build_curobo_reference_pairs.py` from the Studio repository. `pairing.json` records every source pairing. Separate continuous-motion R&D lives in `barilla-curobo-continuous-reference-20260913`; it is not an integrated production planner replay.
