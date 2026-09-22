# Planning System Hardening

## Identity

Task ID:
planning-system-hardening

Status:
not-started

Created:
2026-09-22

Source:
Human review of the `plan/` planning system and identified weaknesses/risks (2026-09-22).

---

## Objective

Harden the `plan/` system so that fresh-Agent recovery, prior-decision application, planning evidence, Work Unit boundaries, authorization promotion, and Task closure remain deterministic and independently verifiable even when planning records are stale, partially updated, or resumed after session interruption.

This Task is limited to planning governance. It must not alter AESM Runtime authority, Process Instance semantics, repository-local `.aesm/` persistence, or engineering execution behavior.

---

## Context

The current planning system already establishes:

- Task files as authoritative planning records;
- `CURRENT.md` as a recoverable navigation projection;
- explicit human authorization before backlog promotion;
- permanent completed Task records;
- separation between planning records and Runtime evidence;
- executable verification requirements;
- semantic Work Unit names.

The review identified six residual risks:

1. `CURRENT.md` can be stale at the fresh-Agent entry point.
2. Prior decisions require manual propagation into each new Task.
3. Subtask evidence is free-form and can degenerate into unsupported Agent assertions.
4. Work Unit granularity is inconsistent.
5. Backlog promotion can be interrupted between file activation and `CURRENT.md` update.
6. Task/Work Unit completion can become ambiguous when checkboxes are complete but final verification/Completion Record state is incomplete.

The hardening work should address these risks without creating a second planning authority, task queue, automatic promotion mechanism, or generalized planning database.

---

## Governing Constraints

1. Preserve `plan/` as the single planning authority.
2. Preserve the rule that the active Task file is authoritative and `CURRENT.md` is a projection.
3. Preserve explicit human authorization as the only basis for backlog activation.
4. Preserve the distinction between planning records and AESM Runtime evidence.
5. Do not make Agent narrative authoritative evidence.
6. Do not introduce automatic task sequencing, a task queue, or a generalized planning index unless a demonstrated requirement cannot be met by the existing structure.
7. Do not change AESM Runtime, `.aesm/`, lifecycle semantics, scope-resolution semantics, or engineering execution behavior.
8. Use semantic Work Unit names rather than numeric phase labels.
9. Preserve completed Task files as permanent historical records.
10. Any new validation mechanism must be independently executable or structurally checkable where practical.

---

## Dependencies

- `plan/README.md`
- `plan/CURRENT.md`
- `plan/PRINCIPLES.md`
- `plan/definitions/TASK.md`
- `plan/definitions/WORK-UNIT.md`
- `plan/definitions/SUBTASK.md`
- `plan/definitions/STATUS.md`
- `plan/definitions/COMPLETION.md`
- `plan/completed/INDEX.md`
- `plan/completed/planning-system-restructuring.md`
- `plan/completed/aesm-planning-authorization-refinement.md`
- `plan/active/planning-verification-time-boundary-correction.md`

---

## Decisions Still in Effect

1. **Task file is the planning source of truth** — `CURRENT.md` never supersedes the active Task file.
2. **Runtime authority is separate** — planning records cannot substitute for Runtime evidence.
3. **Explicit authorization is required** — backlog presence, successor suggestions, roadmap order, or Agent inference do not authorize work.
4. **No automatic sequencing primitive** — the planning system must not become a queue.
5. **Completed records are permanent** — historical Task files remain available for decision and evidence traceability.
6. **Repository scope is not inferred from plan files** — planning references do not become Runtime scope authority.
7. **No premature generalization** — only mechanisms required by demonstrated planning risks should be introduced.
8. **Verification must be independent of Agent claim** — executable or repository-checkable evidence is preferred.

---

## Work Units

### Recovery Consistency and Stale Projection Handling

Status:
not-started

Objective:
Make fresh-Agent recovery explicitly detect and safely repair inconsistent navigation state before selecting executable work.

Subtasks:

- [ ] Define a consistency matrix covering: valid `CURRENT.md` + valid Task state; stale Work Unit; stale Task ID; empty `plan/active/` with a populated CURRENT entry; active Task present while CURRENT reports no active Task; multiple active Task files; and a Task whose referenced Work Unit has no unfinished Subtask.
- [ ] Add a recovery assertion requiring the identified executable Work Unit to contain at least one unfinished Subtask unless its completion condition is already satisfied and the Task file is repaired first.
- [ ] Define the explicit recovery procedure for an active Task existing while `CURRENT.md` says there is no active Task.
- [ ] Define the explicit recovery procedure for multiple active Task files, including the condition under which the Agent must stop rather than select heuristically.
- [ ] Update `plan/README.md`, `plan/CURRENT.md`, and the relevant definition documents so the recovery rules are internally consistent.
- [ ] Add executable or structurally checkable verification for the documented consistency cases.
- [ ] Record the verification evidence in the Task completion record.

Completion condition:

A fresh Agent can detect each identified navigation inconsistency before executing a Subtask, repair only projection state where permitted, and stop on ambiguity rather than selecting work heuristically.

---

### Governing Decision Traceability

Status:
not-started

Objective:
Make prior decisions that constrain a new Task explicit and auditable without creating a second planning authority.

Subtasks:

- [ ] Define a `Governing Decisions` section for active Task files that records the prior Task ID, decision identifier/summary, and applicability to the new Task.
- [ ] Distinguish required governing decisions from historical context so new Tasks do not need to enumerate unrelated history.
- [ ] Define the minimum review obligation for a new Task: identify applicable decisions from `plan/completed/INDEX.md` and relevant completed Task records before execution begins.
- [ ] Define an explicit supersession rule for when a new authorized decision intentionally changes a prior governing decision.
- [ ] Update `plan/definitions/TASK.md`, `plan/README.md`, and `plan/completed/INDEX.md` only as necessary to support this traceability model.
- [ ] Add a validation example using at least one existing persistence/runtime decision and one planning-governance decision.
- [ ] Verify that the mechanism remains advisory for scope authority and does not make planning files authoritative for Runtime state.

Completion condition:

Every newly authorized Task can show which prior decisions govern it, while unrelated historical decisions remain discoverable without requiring a full-history scan.

---

### Verifiable Planning Evidence

Status:
not-started

Objective:
Raise the minimum quality of Subtask completion evidence so that evidence references point to checkable repository state, executable results, or durable artifacts rather than unsupported assertions.

Subtasks:

- [ ] Define evidence-reference categories appropriate to planning records, such as file path/property, executable command/result, test result, Git diff/commit, or explicit absence/finding.
- [ ] Define when a file path alone is insufficient and a checkable property or verification result is required.
- [ ] Define how blocked verification is recorded without allowing the Subtask to be marked complete.
- [ ] Update `plan/definitions/SUBTASK.md` and `plan/definitions/COMPLETION.md` with the minimum evidence contract.
- [ ] Review representative completed Task records for weak evidence wording and determine whether historical records require correction or should remain immutable with a finding.
- [ ] Add a lightweight validation mechanism for newly completed Subtasks where practical; do not claim it proves the underlying engineering result.
- [ ] Verify the planning evidence contract remains distinct from Runtime evidence taxonomy (`CONTROLLER`, `RUNTIME`, `PERSISTED`, `VERIFICATION`, `AGENT`).

Completion condition:

A new Subtask cannot legitimately be considered complete on the basis of a generic assertion such as `verified` or `file created`; its evidence identifies where or how the result can be independently checked.

---

### Work Unit Boundary and Granularity Contract

Status:
not-started

Objective:
Make Work Unit boundaries semantically consistent so recovery points correspond to coherent, independently verifiable portions of work.

Subtasks:

- [ ] Define a granularity heuristic: a Work Unit should represent a coherent bounded outcome or decision/verification gate that provides a meaningful recovery boundary.
- [ ] Explicitly distinguish Work Units from individual commands, trivial file edits, and arbitrary checklist groupings.
- [ ] Define when implementation, validation, and reconciliation should be separate Work Units because interruption between them creates a meaningful recovery boundary.
- [ ] Review representative existing Task files and classify any boundary patterns that violate the heuristic.
- [ ] Correct only demonstrated structural defects; do not reorganize historical Tasks merely for stylistic consistency.
- [ ] Update `plan/definitions/WORK-UNIT.md` and related completion guidance.
- [ ] Add a validation checklist/example showing how a new Task author determines Work Unit boundaries.

Completion condition:

The planning system provides a reproducible rule for deciding Work Unit boundaries, and a fresh Agent can understand why the current boundary is a meaningful recovery point.

---

### Atomic Backlog Promotion and Authorization Recovery

Status:
not-started

Objective:
Make backlog activation recoverable when a session ends between authorization, Task-file promotion, and `CURRENT.md` projection update.

Subtasks:

- [ ] Define the authoritative intermediate state during backlog promotion, including which artifact proves explicit human authorization occurred.
- [ ] Define the recovery procedure for: backlog file only; active Task file only; active Task plus stale CURRENT; CURRENT updated but Task promotion incomplete; and multiple active Tasks.
- [ ] Preserve the rule that merely finding a file under `plan/active/` proves activation only when its authorization/source record is present and valid.
- [ ] Define how an Agent handles an active Task whose authorization record is missing or malformed: stop and request human clarification rather than infer authorization.
- [ ] Update `plan/README.md`, `plan/definitions/TASK.md`, and `plan/CURRENT.md` as required.
- [ ] Add an executable/structural verification scenario for interruption at each promotion boundary.
- [ ] Verify that the recovery protocol does not create autonomous promotion or task sequencing.

Completion condition:

A fresh Agent can safely recover every interrupted promotion state without losing explicit authorization, creating duplicate activation, or inferring authorization from repository state.

---

### Partial Completion and Task Closure Semantics

Status:
not-started

Objective:
Make partial completion and Task closure unambiguous by requiring Task-level verification and Completion Record state before a Task can be treated as complete.

Subtasks:

- [ ] Define the relationship between Work Unit completion, Task status, Completion Record, and movement to `plan/completed/`.
- [ ] Require Task status to remain `in-progress` until the Completion Record is populated with required verification evidence.
- [ ] Define an explicit verification-pending condition without introducing a new status value unless demonstrated necessary; prefer existing `in-progress` semantics where possible.
- [ ] Clarify `[/]` semantics so an in-progress Work Unit cannot be treated as complete merely because some Subtasks are checked.
- [ ] Define how a Task with all Work Units complete but missing acceptance/verification evidence is recovered.
- [ ] Define how stale or unsupported `[x]` claims are treated when their evidence cannot be verified.
- [ ] Update `plan/definitions/STATUS.md`, `TASK.md`, and `COMPLETION.md`.
- [ ] Add structural validation for illegal closure combinations, including complete Task without Completion Record and complete Work Unit with unfinished Subtasks.

Completion condition:

No Task can be treated as planning-complete solely because its Work Units contain `[x]` markers; closure requires the defined verification and Completion Record conditions.

---

### Cross-System Planning Consistency Verification

Status:
not-started

Objective:
Verify that all hardening changes form one deterministic planning protocol without weakening AESM authority boundaries.

Subtasks:

- [ ] Re-read all modified planning definitions and confirm terminology is internally consistent.
- [ ] Validate fresh-Agent recovery from clean state, stale CURRENT state, interrupted promotion, partial completion, and ambiguous active-task state.
- [ ] Validate governing-decision traceability against representative completed Tasks.
- [ ] Validate evidence requirements against representative Subtasks and completion records.
- [ ] Run the repository test suite and any planning-specific validation introduced by this Task.
- [ ] Run `git diff --check` and review the complete diff.
- [ ] Confirm no changes to `docs/`, Runtime, bridge, tests unrelated to planning validation, or `.aesm/` semantics unless explicitly required by a planning-specific verification harness.
- [ ] Confirm the DBP continuation validation remains inactive and unauthorized.
- [ ] Record exact commands, results, commit SHA, and working-tree state.

Completion condition:

The planning system passes the defined recovery, authorization, evidence, granularity, and closure checks with no competing authority or unintended AESM engineering changes.

---

## Acceptance Criteria

1. Fresh-Agent recovery explicitly detects stale or contradictory `CURRENT.md`/Task state before executing work.
2. The identified Work Unit must contain executable unfinished work unless the Task file is first repaired to reflect its actual completion.
3. Applicable prior decisions are explicitly traceable in new Task files through a bounded `Governing Decisions` mechanism.
4. Subtask evidence references are independently checkable and cannot legitimately consist only of unsupported assertions.
5. Work Unit granularity has a documented semantic heuristic and representative validation.
6. Interrupted backlog promotion is recoverable without autonomous promotion or loss of authorization.
7. Task closure requires all Work Units, acceptance criteria, verification, and Completion Record conditions; checked boxes alone are insufficient.
8. Ambiguous or contradictory planning state causes explicit stop/recovery rather than heuristic selection.
9. Existing planning authority and AESM Runtime authority boundaries remain unchanged.
10. No new task queue, automatic chaining mechanism, workspace-wide Process Instance index, or second persistence/planning authority is introduced.
11. Existing historical records are preserved; corrections are limited to demonstrated defects and do not rewrite valid historical evidence.
12. Planning-specific validation and the repository regression suite pass, with exact evidence recorded.

---

## Verification Requirements

Verification must be independent of Agent narrative wherever practical.

Required evidence:

- planning-definition review;
- recovery-state matrix validation;
- interrupted-promotion validation;
- partial-completion/closure validation;
- governing-decision traceability example;
- evidence-quality validation;
- Work Unit granularity review;
- repository regression test result;
- `git diff --check` result;
- complete diff review;
- final Git commit SHA and working-tree state.

---

## Completion Record

Not complete. This file is a proposed backlog Task created from the 2026-09-22 planning-system review. It is not authorized for execution until explicitly activated by the human.

