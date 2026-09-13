# cuRobo and reference pairs

Open `http://localhost:8001/collections/barilla-curobo-reference-20260913/index.html`.

This collection contains 135 latest verified cuRobo trajectories and the 135 original recorded Barilla references. Each pair shares its base identifier: `…-curobo`, then `…-ref`. Suffixes remain visible in the sidebar. Box, compute and mileage sorting keep pairs together; metric sorting uses the cuRobo value.

The cuRobo source is `barilla-curobo-rnd-numeric-fk-20260913` (135 successful tasks). The reference source is the original root collection (132 successes, three recorded failures). Reference paths are not newly qualified results. All 540 trajectory/representation files are exact copies of their sources; only filenames and index metadata identify the pair.

Rebuild with `python scripts/build_curobo_reference_pairs.py` from the Studio repository. `pairing.json` records every source pairing. Browser verification in Chrome covered paired labels, cuRobo and reference selection, 3D geometry and charts. The nine UI tests and full 135-pair sorting checks pass.
