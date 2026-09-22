# Current Planning State

## Navigation Entry Point

This file identifies the currently active Task and Work Unit.

It is a recoverable navigation projection. If it disagrees with the Task file,
**the Task file wins**.

For the full navigation protocol, read `plan/README.md`.

---

## Active Task

Task ID:
repository-scoped-dbp-continuation-validation

Task File:
plan/active/repository-scoped-dbp-continuation-validation.md

Status:
in-progress

Active Work Unit:
Session A — DBP Process Establishment

Execution Status:
BLOCKED — requires a live DBP checkout with AESM Runtime execution capability

---

## Next Candidate

None recorded while an active Task exists.

---

## Recovery Note

If this file appears inconsistent with repository state, do not select work from this
file by heuristic.

1. Read `plan/README.md`.
2. Inspect `plan/active/`.
3. If exactly one active Task exists, read its `Source:` authorization and reconcile
   this projection to the authoritative Task file.
4. If `CURRENT.md` and the Task file disagree, the Task file wins.
5. If more than one active Task exists, stop and obtain explicit human resolution.

The Task file is authoritative. This file is a navigation projection.
