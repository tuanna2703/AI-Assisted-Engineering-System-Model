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
These are the gate conditions that close the Task.

### Verification Requirements

What must be verified (and how) before the Task may be declared complete.
Verification must be independent of Agent claim or narrative.

### Completion Record

Populated only when the Task is complete:

```text
Completed:           ISO 8601 date
Evidence:            references to runtime/test/artifact evidence
Verification result: summary of what was verified and how
```

## Authority

A Task file is the authoritative record of Task state.

`plan/CURRENT.md` is a navigation projection. If it disagrees with the Task file,
**the Task file wins**.

## Lifecycle

A Task follows this lifecycle:
1. Created in `plan/active/` when authorized.
2. Updated continuously as Work Units progress.
3. Moved to `plan/completed/` when all acceptance criteria and verification are satisfied.
4. Indexed in `plan/completed/INDEX.md`.

A Task is not removed. It transitions to completed and becomes historical context.

See COMPLETION.md for the precise definition of Task completion.
