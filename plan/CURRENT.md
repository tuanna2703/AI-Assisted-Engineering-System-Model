# Current Planning State

## Navigation Entry Point

This file identifies the currently active Task and Work Unit.

It is a recoverable navigation projection. If it disagrees with the Task file,
**the Task file wins**.

For the full navigation protocol, read `plan/README.md`.

---

## Active Task

Task ID:
planning-verification-time-boundary-correction

Task File:
plan/active/planning-verification-time-boundary-correction.md

Status:
in-progress

The most recently completed task was:

Task ID:
aesm-planning-authorization-refinement

Task File:
plan/completed/aesm-planning-authorization-refinement.md

Completed:
2026-09-22

---

## Next Candidate

Task ID:
repository-scoped-dbp-continuation-validation

Task File:
plan/backlog/repository-scoped-dbp-continuation-validation.md

Authorization Status:
NOT AUTHORIZED

Required Action:
Obtain explicit human authorization before activation.
A next candidate is not an authorized task.
See `plan/README.md` §Backlog Promotion for the authorization protocol.

---

## Recovery Note

If this file appears inconsistent with repository state, do not select work from this
file by heuristic.

1. Read `plan/README.md`.
2. Inspect `plan/active/`.
3. If exactly one active Task exists, read its `Source:` authorization and reconcile
   this projection to the authoritative Task file.
4. If `plan/active/` is empty, there is no authorized active Task; do not infer one
   from the backlog or from this file's Next Candidate.
5. If more than one active Task exists, stop and obtain explicit human resolution.
6. If this file names a missing or completed Task, repair it from the authoritative
   active Task state before proceeding.

The Task file is authoritative. This file is a navigation projection.
