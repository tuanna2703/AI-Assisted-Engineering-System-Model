# Resolve Plan–Execution Boundary Governance

## Identity

Task ID:
plan-execution-boundary-governance-resolution

Status:
in-progress

Created:
2026-09-23

Source:
  Authorization date: 2026-09-23
  Authorized by: Human instruction — explicit instruction to carry out all tasks in the approved Plan–Execution Boundary resolution artifact.
  Authorized Task: plan-execution-boundary-governance-resolution
  Authorized scope: Establish, implement, and validate the AESM planning/execution boundary as one bounded Task using semantic Work Units. This includes the normative boundary model, finding classification, bounded investigation, execution-stop semantics, blocked-lifecycle integration, plan-mutation authority, acceptance-based completion, reusable Agent guidance, conformance tests, and fresh-Agent/DBP validation. No Runtime implementation, Process Instance mutation, new DBP engineering scope, or unrelated refactor is authorized.

Concern tags:
planning-governance, execution-boundary, scope-control, findings, blocked-recovery, completion, agent-guidance, conformance

## Objective

Establish a mechanically understandable and evidence-verifiable boundary between authorized planning scope and execution discoveries so that an Agent can continue only within authorized work, perform only bounded acceptance investigation, stop on out-of-scope executable findings, recover through the existing blocked lifecycle, and complete when the authorized acceptance conditions are satisfied without implicit plan mutation or work proliferation.

## Context

The current planning system already defines Tasks, semantic Work Units, Subtasks, authorization records, blocked recovery, and completion. The remaining governance gap is that execution discoveries are not yet represented by a single durable rule set that prevents a Finding from silently becoming new executable work. The resolution must establish the boundary without replacing the existing Task/Work Unit/Subtask hierarchy or creating a parallel blocked lifecycle.

## Governing Constraints

1. The authorized plan is the sole definition of executable planning scope.
2. A discovery is evidence; it is not authorization.
3. A Finding may become a Work Candidate, but a Work Candidate is not executable until explicitly authorized.
4. Semantic relatedness, usefulness, severity, convenience, or implementation simplicity never authorize scope expansion.
5. Investigation outside the authorized scope is permitted only when it is strictly necessary to determine whether an existing acceptance condition can be satisfied and all bounded-investigation conditions are met.
6. An out-of-scope executable Finding requires an Execution Stop Report and must use the existing blocked lifecycle when the Task cannot continue.
7. Resolving a blocker does not authorize new work or automatically reactivate a blocked Task.
8. Planning completion is distinct from AESM engineering completion; Runtime remains authoritative for Process Instance and Execution Context state.
9. The Agent must not directly mutate Runtime-owned authoritative `.aesm/` state.
10. Implementation changes are limited to the approved Change Inventory produced by the Boundary Model Work Unit. Any deviation requires an explicit scope-check record before modification.
11. The DBP continuation case is an analytical governance validation unless a live DBP checkout with Runtime execution is independently available. No DBP Runtime evidence may be fabricated.
12. Work Unit and Task names must be semantic rather than numeric phase labels.
13. Do not introduce new planning status values or a parallel blocked lifecycle.

## Dependencies

- `planning-system-restructuring` (COMPLETE)
- `aesm-planning-authorization-refinement` (COMPLETE)
- `planning-verification-time-boundary-correction` (COMPLETE)
- `resolve-dbp-active-process-instance-disposition` (COMPLETE; provides historical DBP PI disposition evidence only)

## Governing Decisions

### Planning authority and Runtime separation
Source Task: `planning-verification-time-boundary-correction`
Relationship: applies

Planning records govern intent and authorization; Runtime and `.aesm/` remain authoritative for engineering execution state and evidence.

### Existing blocked lifecycle
Source Task: `planning-verification-time-boundary-correction`
Relationship: applies

Use `plan/definitions/BLOCKED.md`, `Blocking Condition`, `Resolution Task`, and explicit `Reactivation Record`; do not create a parallel recovery lifecycle.

### Repository-local persistence
Source Task: `repository-portable-continuation-validation`
Relationship: applies

`.aesm/` is repository-local and Git-portable; this planning Task must not change Runtime persistence semantics.

### DBP Process disposition
Source Task: `resolve-dbp-active-process-instance-disposition`
Relationship: applies

The historical DBP Process Instance disposition was resolved through Runtime. That evidence does not constitute new DBP continuation evidence for this Task.

## Decisions Still in Effect

- The planning Task is authoritative for planning state; `CURRENT.md` is only a navigation projection.
- Backlog Tasks require explicit human authorization before activation.
- A blocked Task remains required unless explicitly superseded.
- Resolution is not authorization.
- `complete` and `superseded` are terminal statuses.
- Planning evidence is not Runtime evidence.

## Normative Boundary Requirements

1. **Authorized scope:** executable work is limited to the authorized Task, Work Unit, and Subtask hierarchy.
2. **Discovery:** execution may observe conditions not known when the plan was written; observation alone never expands authorization.
3. **Finding:** each material discovery is classified as a Finding with an explicit disposition.
4. **Work Candidate:** a proposed new action derived from a Finding is record-only until explicitly authorized.
5. **Acceptance investigation:** investigation outside explicit planned work is allowed only when necessary to determine whether an existing acceptance condition can be satisfied and when all bounded-investigation conditions are true.
6. **Mechanical scope decision:** explicit coverage → bounded acceptance investigation if necessary → otherwise STOP.
7. **Execution stop:** an out-of-scope executable condition produces a structured stop record containing task/work-unit/subtask identity, authorization, observed condition, investigation, scope determination, mutation, current state, required decision, and resume point.
8. **Blocked recovery:** execution stop integrates with the existing blocked lifecycle; blocker resolution does not imply authorization or reactivation.
9. **Plan mutation authority:** execution cannot create, activate, expand, reorder, or reinterpret executable planning work merely because a Finding was discovered.
10. **Completion:** completion is based on authorized acceptance conditions and required verification/evidence, not on absence of additional findings.
11. **Future work:** future-work candidates remain record-only and do not prevent completion of an otherwise satisfied Task.
12. **Authority separation:** planning evidence, Agent evidence, Runtime evidence, persisted evidence, and verification evidence remain distinguishable.
13. **Change inventory:** implementation is limited to explicitly identified artifacts; deviations require a recorded scope decision.

## Work Units

### Establish Boundary Baseline
Status: in-progress

Objective:
Inspect the existing planning system and produce an evidence-backed gap matrix against the normative boundary requirements without changing implementation.

Subtasks:
- [/] Inspect `plan/README.md`, Task/Work Unit/Subtask definitions, authorization rules, blocked lifecycle, completion model, Agent guidance, and relevant tests; record which existing mechanisms map to each normative requirement.
- [ ] Inspect the active/blocked planning state and repair any structural inconsistency encountered without changing substantive historical evidence.
- [ ] Record a gap matrix identifying `satisfied`, `partial`, `missing`, or `conflicting` behavior for every normative requirement.

Completion condition:
A durable gap matrix exists in this Task file, all thirteen normative requirements have an evidence-backed classification, and no implementation change has been made under this Work Unit.

### Define Boundary Model and Change Inventory
Status: not-started

Objective:
Convert the normative requirements and baseline findings into a precise, reusable governance model and a positive implementation Change Inventory.

Subtasks:
- [ ] Define the Finding lifecycle: Discovery/Observation → Finding → Work Candidate → Authorized Work.
- [ ] Define the five Finding dispositions and their required execution behavior: IN_SCOPE, ACCEPTANCE_INVESTIGATION, FUTURE_WORK_CANDIDATE, BLOCKING_FINDING, IRRELEVANT_OBSERVATION.
- [ ] Define the mechanical scope decision and all bounded-investigation conditions, including explicit stopping conditions.
- [ ] Define the Execution Stop Report and its relationship to the existing blocked lifecycle.
- [ ] Define plan-mutation authority, ordering preservation, and acceptance-based completion/non-proliferation rules.
- [ ] Produce the positive Change Inventory listing each expected artifact and the reason it must change; require an explicit scope-check record before any deviation.

Completion condition:
The reusable boundary model is persisted in the designated planning/Agent artifacts and the Change Inventory identifies every implementation artifact allowed for the next Work Unit.

### Implement Governance Boundary
Status: not-started

Objective:
Implement only the approved Change Inventory without modifying Runtime semantics or absorbing unrelated findings.

Subtasks:
- [ ] Update the canonical planning boundary definition and references.
- [ ] Update persistent Agent guidance so fresh Agents apply the same boundary rules without conversation history.
- [ ] Add conformance tests for the canonical scope, finding, stop, recovery, mutation, and completion scenarios.
- [ ] Review the implementation diff against the Change Inventory and record any deviation as a scope-check decision before further edits.

Completion condition:
All artifacts in the Change Inventory are implemented, no unauthorized artifact was modified, and the repository contains executable or independently checkable conformance coverage for the normative boundary.

### Verify Boundary Behavior
Status: not-started

Objective:
Verify the implemented boundary through deterministic conformance scenarios and repository-level checks.

Subtasks:
- [ ] Verify explicit in-scope work produces `IN_SCOPE` and permits continuation.
- [ ] Verify necessary acceptance investigation produces `ACCEPTANCE_INVESTIGATION` and cannot authorize unrelated implementation.
- [ ] Verify an unrelated discovered defect produces `FUTURE_WORK_CANDIDATE` or `IRRELEVANT_OBSERVATION` and does not mutate the plan.
- [ ] Verify an out-of-scope executable requirement produces `BLOCKING_FINDING` and an Execution Stop Report rather than silent scope expansion.
- [ ] Verify blocker resolution does not automatically reactivate work.
- [ ] Verify explicit reactivation is a new authorization event.
- [ ] Verify completion remains possible when future-work candidates exist after all authorized acceptance conditions are satisfied.
- [ ] Run the available repository conformance/test suite and record exact results.

Completion condition:
Every canonical scenario has an independently checkable expected and observed result, and all available automated verification passes or each failure is recorded as an explicit blocker/finding.

### Fresh-Agent and DBP Boundary Validation
Status: not-started

Objective:
Validate that an independent Agent can recover and apply the boundary without relying on conversation history, using the DBP discrepancy as an analytical case unless a live DBP Runtime surface is available.

Subtasks:
- [ ] Start from repository state only and apply the Agent entry protocol to recover this Task and its current Work Unit.
- [ ] Execute the canonical fresh-Agent scenarios without being given hidden conversation context; record the exact expected decision for each.
- [ ] Classify the existing DBP continuation discrepancy using the new boundary without creating a new executable DBP Task or claiming unavailable Runtime evidence.
- [ ] If a live DBP Runtime surface is available, perform only the explicitly bounded DBP validation; otherwise record the analytical classification and the Runtime limitation.
- [ ] Reconcile all evidence categories and determine whether the Task can satisfy its acceptance criteria.

Completion condition:
Fresh-Agent behavior is independently demonstrated or explicitly blocked by the missing execution surface, the DBP case is classified without fabricated Runtime evidence, and every remaining acceptance gap is recorded.

## Canonical Validation Scenarios

| Scenario | Finding | Expected disposition | Expected execution behavior |
|---|---|---|---|
| Explicitly authorized work | Planned implementation is encountered | `IN_SCOPE` | Continue |
| Acceptance uncertainty | Evidence needed to determine an existing acceptance condition | `ACCEPTANCE_INVESTIGATION` | Perform only bounded investigation; no unrelated implementation |
| Unrelated defect | Defect outside authorized scope | `FUTURE_WORK_CANDIDATE` or `IRRELEVANT_OBSERVATION` | Record only; do not mutate plan |
| Unauthorized required implementation | Existing acceptance cannot be satisfied without unplanned executable work | `BLOCKING_FINDING` | Stop; persist Execution Stop Report; use blocked lifecycle |
| Resolved blocker | Blocking condition independently resolves | `BLOCKER_RESOLVED` | Do not reactivate automatically |
| Explicit reactivation | Human authorizes resumed work | `AUTHORIZED_REACTIVATION` | Resume only the recorded scope |
| Future improvement after acceptance | Improvement discovered after authorized acceptance is satisfied | `FUTURE_WORK_CANDIDATE` | Record candidate; Task may complete |

## Change Inventory

| Artifact | Intended change |
|---|---|
| `plan/definitions/PLAN-EXECUTION-BOUNDARY.md` | Canonical reusable scope/finding/investigation/stop/completion model |
| `plan/README.md` | Entry protocol and planning-governance reference to the boundary |
| `plan/PRINCIPLES.md` | Persistent governing principles for discovery, authorization, and completion |
| `AGENTS.md` | Fresh-Agent operating guidance for deterministic scope decisions and stops |
| `tests/planning/test_plan_execution_boundary.py` | Executable conformance checks for the canonical model and scenarios |
| `plan/active/plan-execution-boundary-governance-resolution.md` | Authoritative Task state and evidence |
| `plan/CURRENT.md` | Recoverable navigation projection |
| `plan/blocked/repository-scoped-dbp-continuation-validation.md` | Structural planning-state repair required because live DBP Runtime remains unavailable |
| `plan/blocked/INDEX.md` | Blocked-state navigation projection repair |

No Runtime, bridge, `.aesm/`, or DBP source implementation changes are authorized by this Task.

## Acceptance Criteria

1. The Task's `Source:` field is mechanically sufficient and independently identifies the authorized scope.
2. The normative boundary is persisted in a canonical planning definition.
3. The mechanical scope decision is deterministic and does not use semantic relatedness or usefulness as authorization.
4. Finding, Work Candidate, and Authorized Work are distinct states with distinct authority.
5. Bounded investigation is permitted only for existing acceptance-condition determination and has explicit stop conditions.
6. Execution Stop Report requirements are persistent and integrate with the existing blocked lifecycle.
7. Plan mutation authority is explicitly separated from execution discovery.
8. Completion is acceptance-based and future-work candidates do not prevent completion.
9. Implementation is constrained by a positive Change Inventory and deviations require explicit scope-check records.
10. Canonical validation scenarios have deterministic expected outcomes and executable/independently checkable verification.
11. Existing blocked-task recovery and explicit reactivation semantics remain unchanged except for integration references required by the new boundary.
12. Fresh-Agent application of the boundary does not depend on conversation history, or the limitation is explicitly documented if the required independent execution surface is unavailable.
13. The DBP discrepancy is classified as a governance finding without fabricating Runtime execution or creating an unauthorized DBP follow-up Task.
14. All available verification results are recorded with exact evidence; unsupported PASS claims are prohibited.
15. Planning completion remains explicitly distinct from AESM engineering completion.

## Verification Requirements

- Run repository-level planning/conformance tests available to this Task and record exact counts.
- Review the final diff against the Change Inventory.
- Verify no Runtime-owned authoritative state was edited.
- Verify no new planning status value or parallel blocked lifecycle was introduced.
- Verify canonical scenarios have deterministic expected outcomes.
- Fresh-Agent validation must be performed from persisted repository state, not reconstructed from conversation history.
- DBP validation must distinguish analytical classification from live Runtime evidence.

## Completion Record

Status: pending
Completed: not yet

## Current Execution Boundary

This Task governs the planning/execution boundary only. It does not authorize DBP feature work, DBP continuation Runtime execution, Process Instance creation/mutation, persistence migration, or unrelated planning refactors. If execution discovers work outside this boundary, classify it and stop or record it according to `plan/definitions/PLAN-EXECUTION-BOUNDARY.md`.
