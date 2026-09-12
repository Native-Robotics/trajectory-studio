# Barilla Studio rebuild

Base: `master` / `origin/master` at `aa4e977698d05993fd1b5bdbe8a109c5432a8ce8`.
Branch: `codex/feat/barilla-studio-rebuild`.

This reimplements the Studio requests recovered from the September 9–10
“Fix trajectory planner: logs, issues, tests” session, rather than replaying
the previous Barilla UI commits.

- Import the 135 original Barilla request/result pairs with full DH and hitboxes;
  replace the bundled sample collection.
- Resize side panels and retain widths between visits.
- Navigate trajectories with Up/Down, leaving text inputs and sliders alone.
- Show eight-character IDs and Pick/Wait/Place destination labels.
- Sort by placement cycle, joint mileage, or computation time. A placement is
  followed by its chronological Wait/Pick motions before the next placement.
- Provide the corpus table with right-aligned headers, working deep links,
  mileage definition, and historical flag explanations.
- Omit CAD and the removed report page.

`viewer.js`, `robot.js`, `charts.js`, and `robots/` remain byte-identical to master.
The recorded equipment and scene geometry are unchanged. No SVG fallback or
CuRobo runtime changes are included in this branch.

## Checks

Seven navigation/sorting/flag helper tests and two index-regeneration tests pass.
All 132 available paths were checked against the stored mileage: a 100 Hz
reevaluation differed by at most 0.000367 rad in summed joint travel. An
independent analytic-extrema comparison differed by less than 0.00018 rad per
joint, consistent with rounded sampled historical metadata.

Browser checks use the separate test browser: 135 entries, Box/Compute sorting,
arrow selection, search input retaining arrow keys, corpus table sort and deep
link, playback, explicit unfinished-result status, mouse and keyboard resizing
with persisted widths, and a 390 px mobile table with horizontal scrolling.
A grid-column regression found during browser testing was corrected before
commit; the final desktop panels occupy a single row and the renderer has its
full center-panel width.

The current in-app browser cannot initialize WebGL even with the master
renderer. This is a separate unresolved graphics environment limitation; this
branch does not substitute another renderer or claim that limitation is fixed.

## Local test instance

The instance is served separately at `http://localhost:8001/` from this worktree.
The original Studio/replay instance remains on port 8000.

## Saved cuRobo collection (September 13)

`collections/barilla-curobo-20260912/` now uses this branch's renderer and navigation.
The original 135 output pairs and replay manifest are byte-identical to the
previous collection: 46 solved, 89 failed optimization. Box/pallet metadata is
joined by original request ID; mileage is computed from each saved cubic's
stationary points by `scripts/index_curobo_mileage.py`. Failed paths have unknown
mileage. The default selection is a solved path, and result-modification controls
are hidden because the replay is a saved result set.

After reboot the in-app browser renders the robot and obstacles and playback
advances the timeline and joint values. The earlier WebGL limitation above was
an environment problem observed before reboot. The old `barilla` branch remains
as a backup; this rebuild has not been merged.
