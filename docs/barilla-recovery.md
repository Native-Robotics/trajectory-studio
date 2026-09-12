# Barilla Studio recovery

This branch saves the local Studio work from September 9–10, 2026 so it can be
found in Git history and PyCharm. Studio was still on `master` at `aa4e977`;
the relevant changes had remained uncommitted in its working directory.

Session provenance: Grok task **Fix trajectory planner: logs, issues, tests**,
ID `01a085db-bbb7-7f53-b24d-698d7d239b56`, September 9–10, 2026. That session
reported that planner documentation changes were pushed to
`emmrk/wip/palletize-session`, while Studio's other local edits were not pushed.

The recovered Studio changes include:

- All 135 historical Barilla request/result pairs and their matching collection
  index and corpus metadata.
- The sortable corpus table, destination and box labels, compute and mileage
  sorting, keyboard selection, and links to individual trajectories.
- Resizable viewer panels, the updated AUBO iS25 representation, and related
  viewer and index-generation changes.

The original session explicitly removed the HTML review report from the site
and removed the CAD presentation. Those choices remain intact: no report page
or CAD assets were restored. The session referenced planner commits `e662173d`
(report deletion) and `5c36bf0d` (Markdown handover); these are historical
provenance, not Studio commits.

Earlier bundled samples remain recoverable from the parent commit. This branch
preserves their existing removal in favor of the Barilla collection. Local IDE
settings and new backend replay collections are ignored. No current CuRobo
results are included in this historical snapshot.
