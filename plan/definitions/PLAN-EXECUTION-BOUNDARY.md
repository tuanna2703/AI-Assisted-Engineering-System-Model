# Plan–Execution Boundary

## Purpose

This definition establishes the boundary between planning authority and execution discovery in AESM's `plan/` system.

The planning system answers what work is authorized. Execution may discover conditions that were not known when the plan was written, but discovery does not create execution authority.

This definition is normative for planning Tasks and complements `TASK.md`, `WORK-UNIT.md`, `SUBTASK.md`, `BLOCKED.md`, and `COMPLETION.md`. It does not replace AESM Runtime authority.

## Authority Model

```
Authorized Plan
     |
     v
Task → Work Unit → Subtask
     |
     v
Execution
     |
     +--> Observation / Discovery
              |
              v
           Finding
              |
              v
        Work Candidate
              |
              v
     Explicit Authorization
              |
              v
       Authorized Work
```

The transitions are not interchangeable:

- Observation/Discovery is evidence.
- A Finding is a classified observation.
- A Work Candidate is a proposed future action.
- Authorized Work is executable planning scope.

Only explicit planning authorization creates executable work.

## Authorized Scope

An Agent may execute only work that is covered by the authorized Task, its Work Unit, and its Subtasks.

The following are not authorization criteria:

- semantic relatedness;
- usefulness;
- severity alone;
- convenience;
- implementation simplicity;
- the Agent's belief that the work is necessary to improve the result;
- chronological proximity to the authorized work;
- discovery during an already-authorized Subtask.

A Finding does not alter the authorized Task, Work Unit, Subtask list, ordering, or acceptance conditions.

## Mechanical Scope Decision

For every material Finding that could cause additional action, apply this procedure in order:

1. **Explicit coverage:** Is the required action explicitly covered by an existing authorized Subtask or by the stated completion condition of the current Work Unit?
   - Yes → `IN_SCOPE`; continue.
2. **Acceptance investigation:** If not explicitly covered, is the investigation strictly necessary to determine whether an existing acceptance condition can be satisfied?
   - Yes → `ACCEPTANCE_INVESTIGATION`; perform only the bounded investigation permitted below.
3. **Stop:** If neither condition is true, the action is out of scope.
   - Classify the Finding and do not execute the unplanned action.
   - If the out-of-scope condition prevents satisfaction of existing acceptance, classify it as `BLOCKING_FINDING` and produce an Execution Stop Report.
   - Otherwise record it as future work or an irrelevant observation as appropriate.

The Agent must not replace this procedure with a judgment that the discovery is "related", "useful", "small", or "obviously required".

## Bounded Acceptance Investigation

An acceptance investigation outside explicit planned work is permitted only when all conditions are true:

1. An existing acceptance condition is already declared by the authorized plan.
2. The Finding creates a factual uncertainty about whether that acceptance condition can be satisfied.
3. The proposed investigation is strictly necessary to resolve that uncertainty.
4. The investigation does not change the acceptance condition.
5. The investigation does not create, activate, expand, reorder, or reinterpret executable planning work.
6. The investigation has a bounded stopping condition tied to the existing acceptance condition.
7. Any resulting new implementation or other executable action is separately classified and is not authorized merely because the investigation was allowed.

If any condition is false, stop the investigation and classify the Finding normally.

## Finding Dispositions

Every material Finding receives one of these dispositions:

| Disposition | Meaning | Execution authority |
|---|---|---|
| `IN_SCOPE` | Action is explicitly covered by authorized work | Continue within existing scope |
| `ACCEPTANCE_INVESTIGATION` | Bounded investigation is necessary to determine an existing acceptance condition | Investigate only within the stated boundary |
| `FUTURE_WORK_CANDIDATE` | Potential useful work outside current authorization | Record only; no execution |
| `BLOCKING_FINDING` | Out-of-scope condition prevents satisfying an existing acceptance condition | Stop; record blocker and use blocked lifecycle |
| `IRRELEVANT_OBSERVATION` | Observation does not affect current authorized acceptance or execution | Record only when durable value exists |

A Finding may be reclassified only by an explicit planning decision. The Agent's classification is evidence, not authority to expand the plan.

## Execution Stop Report

When execution cannot legitimately continue, persist an `EXECUTION STOPPED` record containing:

```
Task:
Work Unit:
Subtask:
Authorization:
Observed Condition:
Finding:
Plan Coverage:
Acceptance Relevance:
Investigation Performed:
Investigation Result:
Scope Determination:
Mutation Already Performed:
Current Persisted Planning State:
Required Human / Planning Decision:
Resume Point:
Execution Status: BLOCKED
```

The stop report must identify what has already changed and what has not changed. It must not convert the Finding into authorization.

When the stop prevents the Task from advancing, use the existing Task/Work Unit/Subtask blocked lifecycle. Do not create a parallel stop status.

## Blocked Recovery

Execution stop and blocked recovery are connected but distinct:

1. A Finding can cause execution to stop.
2. The existing blocked lifecycle records why work cannot continue.
3. A Resolution Task may address the blocker.
4. Resolution of the blocker does not authorize new work.
5. `Status: RESOLVED` does not itself reactivate the blocked Task.
6. Reactivation requires the existing explicit Reactivation Record and human authorization.

Nothing in this boundary changes the existing `BLOCKED.md` lifecycle.

## Plan Mutation Authority

Execution must not, merely because of a Finding:

- create a new executable Task;
- add or remove an executable Work Unit;
- add, remove, reorder, or reinterpret Subtasks;
- change acceptance conditions;
- change Task objective or authorized scope;
- activate a backlog Task;
- reactivate a blocked Task;
- reinterpret a blocker as authorization;
- modify Runtime-owned authoritative state.

A Finding may produce a Work Candidate. A Work Candidate becomes executable only through explicit planning authorization.

## Change Inventory

Implementation of a boundary-resolution Task must use a positive Change Inventory.

Before implementation begins, the Task must identify:

- artifact path;
- intended change;
- reason the change is required by the boundary;
- preserved behavior/authority;
- verification method.

An artifact not in the Change Inventory is outside implementation scope until an explicit scope-check decision adds it.

The Agent must not use a broad statement such as "modify whatever is necessary" as implementation authorization.

## Completion and Non-Proliferation

Completion is based on the authorized acceptance conditions and required verification/evidence.

The following is not a completion condition:

> No additional issues were discovered.

A future-work candidate may remain recorded when all authorized acceptance conditions are satisfied. Its existence does not prevent Task completion.

Completion hierarchy remains:

- Subtask: authorized action performed + evidence.
- Work Unit: authorized Subtasks complete + Work Unit condition + evidence + navigation reconciliation.
- Task: all authorized Work Units complete + acceptance criteria + verification + Completion Record.

Planning completion remains distinct from AESM engineering completion. Runtime remains authoritative for engineering state.

## Canonical Validation Scenarios

| Scenario | Starting condition | Finding | Expected result |
|---|---|---|---|
| Explicit scope | Action is listed in current Subtask | Planned implementation encountered | `IN_SCOPE`; continue |
| Acceptance investigation | Acceptance condition exists; factual uncertainty blocks verification | Evidence is required only to determine that condition | `ACCEPTANCE_INVESTIGATION`; bounded investigation only |
| Unrelated defect | Authorized work is otherwise executable | Defect lies outside authorized scope | `FUTURE_WORK_CANDIDATE` or `IRRELEVANT_OBSERVATION`; no plan mutation |
| Blocking discovery | Acceptance cannot be satisfied without unplanned executable action | Unplanned implementation is required | `BLOCKING_FINDING`; stop and persist Execution Stop Report |
| Blocker resolved | Existing blocker is independently resolved | Resolution evidence becomes available | Record `RESOLVED`; no automatic reactivation |
| Explicit reactivation | Human provides a new authorization | Blocked Task is explicitly reactivated | Resume only authorized scope |
| Future improvement after acceptance | All authorized acceptance conditions are already satisfied | Improvement is discovered | Record future candidate; Task remains completable |

## Evidence Separation

The boundary preserves the existing evidence taxonomy:

- `CONTROLLER` — authorization and human planning decisions.
- `AGENT` — Agent observations, classifications, and independent session behavior.
- `RUNTIME` — authoritative Runtime responses.
- `PERSISTED` — persisted `.aesm/` state and history when applicable.
- `VERIFICATION` — executable or independently checkable verification.

Planning records are not Runtime evidence. A planning Task may be completed without creating a Process Instance unless its explicit authorized scope separately includes Runtime-mediated engineering work.

## Fresh-Agent Requirement

A fresh Agent must be able to apply this boundary from repository-persisted planning artifacts without relying on conversation history.

If a validation requires a separate execution environment that is unavailable, the Agent must record the limitation and must not claim the unavailable evidence.

## DBP Validation Rule

The DBP continuation discrepancy is a validation case for classification and scope control.

Without a live DBP checkout in which the AESM Runtime can be invoked, the Agent may:

- inspect the persisted planning/task evidence;
- classify the discrepancy under this boundary;
- identify whether the existing acceptance conditions permit bounded investigation;
- identify the required stop/block behavior.

It may not:

- claim a new DBP Runtime interaction;
- fabricate Session A or Session B evidence;
- manually mutate `.aesm/` state;
- create an executable DBP follow-up Task merely because the discrepancy exists.
