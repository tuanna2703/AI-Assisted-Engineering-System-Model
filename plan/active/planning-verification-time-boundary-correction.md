# Planning Verification Time-Boundary Correction

## Identity

Task ID:
planning-verification-time-boundary-correction

Status:
in-progress

Created:
2026-09-22

Source:
Human instruction — review the planning system against the previously agreed authorization model and correct the historical verification record identified during that review.

---

## Objective

Correct the completed planning-authorization verification record so that its navigation answers are explicitly time-bounded to the verification snapshot, while preserving the historical evidence and leaving the live planning state unchanged.

---

## Context

The live planning architecture now correctly distinguishes:
- no active Task;
- a next candidate;
- explicit human authorization;
- active Task state;
- non-binding successor suggestions.

The completed `aesm-planning-authorization-refinement` record, however, contains verification questions phrased as present-tense questions such as “What task is currently active?” even though the recorded answer describes the refinement Task while it was being verified.

This creates an avoidable ambiguity between historical verification evidence and the current planning state represented by `plan/CURRENT.md`.

The correction must clarify the temporal boundary of the historical verification without rewriting the historical result or introducing a new planning mechanism.

---

## Governing Constraints

1. Do not introduce `SEQUENCE.md`, a task queue, automatic task chaining, or any new planning primitive.
2. Do not change the backlog authorization model.
3. Do not change the live meaning of `plan/CURRENT.md`.
4. Do not change AESM Runtime authority or `.aesm/` semantics.
5. Do not execute or activate the DBP continuation validation Task.
6. Preserve the historical verification result; only clarify its temporal scope.
7. Use semantic Work Unit names.
8. Keep this correction bounded to planning documentation.

---

## Dependencies

- `aesm-planning-authorization-refinement` (COMPLETE)
- `planning-system-restructuring` (COMPLETE)
- `plan/README.md`
- `plan/CURRENT.md`
- `plan/completed/aesm-planning-authorization-refinement.md`
- `plan/definitions/TASK.md`
- `plan/definitions/STATUS.md`

---

## Decisions Still in Effect

1. Backlog presence does not authorize execution.
2. Explicit human authorization is required before backlog promotion.
3. `CURRENT.md` is a recoverable navigation projection, not an authority.
4. The active Task file is authoritative for Task state.
5. Planning records are not AESM Runtime evidence.
6. No task-sequencing artifact is to be introduced without demonstrated need.
7. The DBP continuation validation remains inactive until explicitly authorized.

---

## Work Units

### Historical Verification Boundary Review

Status: complete

Objective:
Inspect the completed verification record and identify every present-tense statement that could be confused with the live planning state.

Subtasks:
- [x] Inspect `plan/completed/aesm-planning-authorization-refinement.md` verification section.
- [x] Compare its navigation claims with the current `plan/CURRENT.md`.
- [x] Confirm the defect is historical wording, not a defect in the live authorization model.

Completion condition:
The correction scope is limited to temporal clarification of historical verification evidence.

---

### Historical Verification Wording Correction

Status: in-progress

Objective:
Make the historical verification questions explicitly refer to the planning state at verification time.

Subtasks:
- [ ] Revise the 10-question verification headings/questions so present-tense navigation claims are explicitly time-bounded.
- [ ] Preserve the recorded verification answers and their source references.
- [ ] Add a concise note distinguishing the historical verification snapshot from the live planning state.

Completion condition:
A reader can distinguish historical verification state from current repository planning state without changing the historical result.

---

### Planning Consistency Verification

Status: not-started

Objective:
Verify that the correction introduces no contradiction or new planning authority.

Subtasks:
- [ ] Re-read the corrected completed task and current planning documents.
- [ ] Verify `plan/CURRENT.md` still reports no active Task and the DBP Task as NOT AUTHORIZED.
- [ ] Verify no sequencing artifact or new status value was introduced.
- [ ] Run `.venv/bin/pytest tests/ -q` and record the actual result.
- [ ] Run `git diff --check` and review the complete diff.
- [ ] Verify the DBP continuation validation remains inactive.

Completion condition:
The historical record is temporally unambiguous, the live planning state is unchanged, and repository verification passes.

---

## Acceptance Criteria

1. Historical verification questions are explicitly time-bounded.
2. Historical verification answers remain intact except for necessary temporal clarification.
3. The live `plan/CURRENT.md` state remains authoritative and unchanged in meaning.
4. The backlog authorization boundary remains unchanged.
5. No sequencing artifact or new planning authority is introduced.
6. No DBP engineering execution occurs.
7. Regression tests pass.
8. `git diff --check` passes.
9. The final diff contains only the bounded planning-record correction plus this Task's lifecycle record.

---

## Verification Requirements

1. Inspect the corrected historical verification section.
2. Re-read `plan/CURRENT.md`, `plan/README.md`, and the completed correction Task.
3. Confirm the historical/current distinction is explicit.
4. Run `.venv/bin/pytest tests/ -q`.
5. Run `git diff --check`.
6. Review the complete diff and confirm no production/AESM Runtime changes.

---

## Completion Record

To be populated when all acceptance criteria and verification requirements are satisfied.
