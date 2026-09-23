# Resolve DBP Active Process Instance Disposition

## Identity

Task ID:
resolve-dbp-active-process-instance-disposition

Status:
not-started

Created:
2026-09-23

Source:
UNAUTHORIZED — this Task is in plan/backlog/ and has not been explicitly
authorized for execution. It must not be activated without an explicit human
instruction identifying this Task by name and directing its activation.

Concern tags:
dbp, process-instance, disposition, unblocking, continuation, resolution

---

## Resolution Context

Resolves Task: repository-scoped-dbp-continuation-validation
Resolves Condition: A new same-scope Session A cannot be established while the existing active Process Instance (d0640ec8-672e-43bd-bd4b-974d808915a2, scope project:tuanna2703/directories-builder-pro) persists and its disposition has not been explicitly authorized. This Resolution Task performs the work required to establish a legitimate disposition of that Process Instance, enabling the blocked Task to resume its Session A Work Unit.

---

## Objective

Establish an authorized, explicit disposition of the existing active DBP Process
Instance (`d0640ec8-672e-43bd-bd4b-974d808915a2`, scope
`project:tuanna2703/directories-builder-pro`) so that the blocked Task
`repository-scoped-dbp-continuation-validation` can resume its Session A Work Unit
through a legitimate Runtime-owned resolution path.

A "disposition" means one of:

1. **Continue using the existing Process Instance as the Session A baseline.**
   The existing PI is determined to be in a state that permits legitimate
   Runtime-mediated continuation without a new PI creation.

2. **Authorize termination of the existing Process Instance.**
   The existing PI is formally closed through the Runtime-owned termination
   operation, enabling a clean Session A creation in scope
   `project:tuanna2703/directories-builder-pro`.

3. **Authorize an alternative approach** that the human controller specifies.

The specific disposition is not determined by this Task definition. It must be
determined by human controller decision and then executed under Runtime authority
as part of this Task's authorized scope.

---

## Governing Constraints

1. Do not manually edit `.aesm/` files. All Process Instance state mutations
   must be Runtime-mediated.
2. Do not create a new Process Instance under scope
   `project:tuanna2703/directories-builder-pro` without first resolving the
   existing one.
3. Do not terminate the existing Process Instance without explicit human
   authorization. This Task's execution does not itself authorize termination —
   the human must specify the intended disposition when authorizing this Task.
4. Completing this Task does not automatically reactivate
   `repository-scoped-dbp-continuation-validation`. Resolution must be verified
   and a separate explicit reactivation authorization must be recorded.
5. Do not modify `plan/active/`, `plan/blocked/`, or `plan/completed/` Task
   files as part of this Task's engineering scope — those are planning-system
   operations that require separate human instruction.
6. Runtime remains the sole authority for Process Instance state.
7. This Task is an independent Task; it does not supersede or replace
   `repository-scoped-dbp-continuation-validation`.

---

## Dependencies

- repository-scoped-dbp-continuation-validation (BLOCKED — this Task resolves its blocker)

---

## Governing Decisions

### Runtime authority over Process Instance state
Source: aesm-implementation-foundations
Relationship: applies

Runtime is the sole authority for persisted AESM state. No disposition of the
existing PI may be made by direct `.aesm/` editing.

### Repository isolation
Source: engineering-scope-identity-and-scope-resolution
Relationship: applies

Scope resolution is deterministic and Runtime-owned. The DBP repository's
`.aesm/` is the authoritative persistence boundary for scope
`project:tuanna2703/directories-builder-pro`.

### Planning / Runtime boundary
Source: planning-verification-time-boundary-correction
Relationship: applies

This Task is an independent planning Task. Its completion is a planning record,
not automatic AESM engineering completion or automatic reactivation of the
blocked Task.

---

## Work Units

### Inspect Existing Process Instance State
Status: not-started

Objective:
Independently verify the current state of the existing active DBP Process Instance
from the authoritative repository-local `.aesm/` files.

Subtasks:
- [ ] Navigate to the DBP repository root (`tuanna2703/directories-builder-pro` local checkout) and inspect `.aesm/d0640ec8-672e-43bd-bd4b-974d808915a2/`.
- [ ] Read `process.json` and record: PI ID, scope, status, lifecycle state.
- [ ] Read `context.json` and record: current Execution Context state.
- [ ] Read `history.jsonl` and record: last recorded history event and total event count.
- [ ] Determine whether the existing PI is in a state that permits Runtime-mediated continuation without conflict.
- [ ] Record findings as planning evidence in this Task file.

Completion condition:
The existing PI's current state (scope, lifecycle status, context, history) is
documented from authoritative repository-local files, and the findings establish
whether continuation or termination is the appropriate disposition.

### Obtain Human Disposition Decision
Status: not-started

Objective:
Surface the inspection findings to the human controller and obtain an explicit
decision on the intended disposition of the existing Process Instance.

Subtasks:
- [ ] Present the inspection findings to the human controller.
- [ ] Present the available disposition options (continue as Session A baseline, terminate and create fresh, or alternative).
- [ ] Record the human controller's explicit disposition decision in this Task file.

Completion condition:
An explicit human disposition decision is recorded in this Task file, identifying
the authorized action for the existing Process Instance.

### Execute Authorized Disposition
Status: not-started

Objective:
Execute the human-authorized disposition of the existing Process Instance through
Runtime-owned operations.

Subtasks:
- [ ] Execute only the Runtime-mediated operation authorized by the human disposition decision.
- [ ] Record the Runtime response and resulting `.aesm/` state as evidence.
- [ ] Verify that the resulting state is consistent with the authorized disposition.
- [ ] Record any gap or failure explicitly rather than claiming success without evidence.

Completion condition:
The authorized disposition has been executed through Runtime-mediated operations,
and the resulting `.aesm/` state is independently verifiable as consistent with
the disposition decision.

### Record Resolution Evidence for Blocked Task
Status: not-started

Objective:
Record the resolution evidence in a form that enables the authorized actor to
verify the blocked Task's Resolution Condition as satisfied.

Subtasks:
- [ ] Record the specific evidence that establishes the blocked Task's Resolution Condition as satisfied.
- [ ] The Resolution Condition is: "A live DBP checkout with AESM Runtime execution capability is available, the disposition of the existing active Process Instance has been explicitly authorized, and a legitimate Session A can be established through the Runtime-owned resolution path without manual `.aesm/` mutation."
- [ ] Verify that the evidence is independently checkable without relying on conversation history.
- [ ] Do not record `Status: RESOLVED` in the blocked Task file — that transition requires a separate explicit human authorization.
- [ ] Record the evidence reference in this Task's Completion Record.

Completion condition:
The resolution evidence is recorded and independently checkable. The blocked Task's
Resolution Condition can be evaluated from repository state alone.

---

## Acceptance Criteria

1. The existing DBP Process Instance's state is documented from authoritative
   repository-local `.aesm/` files.
2. An explicit human disposition decision is recorded.
3. The authorized disposition is executed through Runtime-mediated operations only.
4. The resulting state is independently verifiable.
5. Resolution evidence sufficient for evaluating the blocked Task's Resolution
   Condition is recorded in this Task's Completion Record.
6. No `.aesm/` files were directly edited (all mutations are Runtime-mediated).
7. The blocked Task `repository-scoped-dbp-continuation-validation` has not been
   reactivated as part of this Task.

---

## Completion Record

Status: pending
Completed: not yet
