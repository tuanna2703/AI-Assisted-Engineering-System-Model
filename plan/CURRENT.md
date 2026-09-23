# Current Planning State

## Navigation Entry Point

This file identifies the currently active Task and Work Unit.

It is a recoverable navigation projection. If it disagrees with the Task file,
**the Task file wins**.

For the full navigation protocol, read `plan/README.md`.

---

## Active Task

Task:
resolve-dbp-active-process-instance-disposition

Task File:
plan/active/resolve-dbp-active-process-instance-disposition.md

Status:
in-progress

Current Work Unit:
Inspect Existing Process Instance State

---

## Reason No Active Task Exists

**A Resolution Task is active while the DBP continuation Task remains blocked.** One Task remains in `plan/blocked/`:

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

Resolution Task:
resolve-dbp-active-process-instance-disposition

Resolution Task File:
plan/active/resolve-dbp-active-process-instance-disposition.md

Resolution Task Authorization:
Explicit human authorization given on 2026-09-23 to activate and execute the planned scope.

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

None. The Resolution Task is now active and its current Work Unit is `Inspect Existing Process Instance State`.

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
