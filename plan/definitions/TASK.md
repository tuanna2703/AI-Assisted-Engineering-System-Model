# Task

## Definition

A **Task** is a bounded engineering objective that constitutes a meaningful,
independently completable unit of work within the AESM planning system.

A Task is the top-level unit in the planning hierarchy:

```text
Task
  └── Work Unit
        └── Subtask
```

## Required Properties

Every Task file must define:

### Identity

```text
Task ID:       unique slug, e.g. runtime-consistency-hardening
Status:        one of the allowed planning states (see STATUS.md)
Created:       ISO 8601 date
Source:        document or decision that authorized this Task
```

### Objective

A concise statement of what completing this Task achieves.
Must be specific enough that completion can be determined objectively.

### Context

Background information required to understand why the Task exists.
Include the engineering condition that made the Task necessary.

### Governing Constraints

Rules that must not be violated during execution of this Task.
Each constraint must be specific enough to test: a future Agent must be able to
determine whether a proposed action violates a constraint.

### Dependencies

Other Tasks or engineering artifacts that must be complete or available before
this Task can be fully executed. State explicitly "None" if there are no dependencies.

### Governing Decisions

Prior decisions that were reviewed and determined to constrain this Task.

Each entry must identify:
- Source Task ID
- Decision summary
- Why the decision applies to this Task

Only applicable decisions belong here. This section is a bounded traceability record,
not a duplicate of the entire completed-task history.

If a prior decision is intentionally changed, record the supersession explicitly,
including the superseded Source Task ID and the new decision.

### Decisions Still in Effect

Decisions made during prior Tasks that remain active constraints during execution
of this Task.

A decision belongs here if: *violating it during future work would constitute an error.*

A decision is historical only if it describes a past condition and violating it
is no longer meaningful under the current system.

### Work Units

A list of all Work Units in this Task, in execution order, each with:
- Name
- Status
- Objective (one sentence)
- Subtasks
- Completion condition

Work Unit names must be the same names used in the Task's authoritative prompt or
source document. Do not rename Work Units opportunistically.

### Acceptance Criteria

Observable outcomes that must be satisfied for this Task to be considered complete.
