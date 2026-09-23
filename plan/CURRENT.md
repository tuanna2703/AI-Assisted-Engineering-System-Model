# Current Planning State

## Navigation Entry Point

This file identifies the currently active Task and Work Unit.

It is a recoverable navigation projection. If it disagrees with the Task file,
**the Task file wins**.

For the full navigation protocol, read `plan/README.md`.

---

## Active Task

None.

The previously active Task `repository-scoped-dbp-continuation-validation` has
been migrated to `plan/blocked/` as part of the Blocked Task Lifecycle and
Recovery Model planning-system implementation (2026-09-23). There is currently
no active Task.

---

## Reason No Active Task Exists

**Work is blocked.** One Task remains in `plan/blocked/`:

Task:
repository-scoped-dbp-continuation-validation

Task File:
plan/blocked/repository-scoped-dbp-continuation-validation.md

Task Status:
blocked

Blocked Work Unit:
Session A — DBP Process Establishment

Blocking Condition:
OPEN — live DBP Runtime execution environment required; existing Process Instance
disposition not yet authorized. See Blocking Condition section in Task file.

Resolution Task (unauthorized, in backlog):
resolve-dbp-active-process-instance-disposition

Resolution Task File:
plan/backlog/resolve-dbp-active-process-instance-disposition.md

---

## No-Active-Task State Semantics

This section is required by the planning model to distinguish between
three distinct no-active-Task situations:

| Reason | This State? |
|--------|-------------|
| No active Task because work is blocked | **YES** — see plan/blocked/ |
| No active Task because the previous Task is complete | No |
| No active Task because planning is awaiting explicit authorization | No |

A fresh Agent must not infer an active Task from this file's absence of one.
A fresh Agent must not autonomously activate any backlog Task.

---

## Next Candidate

None. The Resolution Task (`resolve-dbp-active-process-instance-disposition`) is
in `plan/backlog/` and **unauthorized**. It must not be activated without an
explicit human instruction identifying it by name.

---

## Recovery Note

If this file appears inconsistent with repository state, do not select work from
this file by heuristic.

1. Read `plan/README.md`.
2. Inspect `plan/active/`. If it contains a Task, that Task file is authoritative.
3. If `plan/active/` is empty, inspect `plan/blocked/INDEX.md`.
4. If blocked Tasks exist, read each blocked Task's `Blocking Condition` section.
5. If `CURRENT.md` and the Task file disagree, the Task file wins.
6. If more than one active Task exists, stop and obtain explicit human resolution.
7. Never infer authorization from repository chronology, blocker resolution, or
   conversation history.

The Task file is authoritative. This file is a navigation projection.
