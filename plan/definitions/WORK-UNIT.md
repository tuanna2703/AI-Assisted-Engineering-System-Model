# Work Unit

## Definition

A **Work Unit** is a coherent, bounded portion of a Task. It represents the
smallest division of a Task that has its own completion condition, verification
requirement, and observable outcome.

A Work Unit should also provide a meaningful **recovery boundary**: if execution
stops after the Work Unit completes, a fresh Agent should be able to continue at
the next Work Unit without reconstructing hidden context or re-evaluating the
meaning of the completed work.

Work Units are executed in the order defined in the Task file. A Work Unit may
not be skipped unless the Task file explicitly marks it as inapplicable and
records the reason.

## Position in Hierarchy

```text
Task
  └── Work Unit   ← this level
        └── Subtask
```

## Required Properties

Every Work Unit definition within a Task file must include:

### Name

The exact name of the Work Unit as defined in the Task's authoritative source.

Do not rename a Work Unit after the Task has been authorized. If a name must
change, record the change as a decision in the Task file.

### Status

One of the allowed planning states defined in STATUS.md.

### Objective

A single sentence describing what completing this Work Unit achieves within the
scope of the Task.

### Subtasks

An ordered list of concrete, executable actions. See SUBTASK.md for the full
definition of a Subtask.

### Completion Condition

A precise, observable statement of what must be true for this Work Unit to be
considered complete.

The completion condition must be verifiable independently of Agent claim. An
Agent must be able to read the condition and determine whether it is satisfied
without relying on memory, conversation history, or construction knowledge.

## Granularity Heuristic

A Work Unit is an appropriate boundary when most of the following are true:

- it produces a coherent artifact, decision, implementation result, or verification result;
- it has a distinct completion condition;
- its completion creates a useful recovery point;
- a fresh Agent can understand the next Work Unit from the Task file alone;
- interruption before its completion would leave a meaningfully different state.

A command or trivial file edit that has no independent recovery meaning should
normally remain a Subtask, not become its own Work Unit.

Implementation, validation, and reconciliation may be separate Work Units when
they produce independently meaningful states or when interruption between them
would materially affect recovery. They should not be separated merely to create
more checklist entries.

The heuristic is guidance for new Tasks. Historical Task boundaries are not
rewritten solely for stylistic consistency.

## Execution Protocol

1. Read the Work Unit and all its Subtasks.
2. Execute Subtasks in order unless the Task file specifies otherwise.
3. Verify the Completion Condition after all Subtasks are done.
4. Record required evidence.
5. Mark the Work Unit complete in the Task file.
6. Reconcile `CURRENT.md` or explicitly verify no projection change is required.
7. Evidence the reconciliation (see §Projection Reconciliation).

**Never advance CURRENT.md before the Task file records Work Unit completion.**

**Never mark a Work Unit complete before navigation projection is reconciled.**

## Projection Reconciliation

Navigation reconciliation is a mandatory Work Unit completion obligation.
Do not create a boilerplate reconciliation Subtask within every Work Unit;
instead treat reconciliation as an implicit final step of completion.

A Work Unit may become authoritatively `complete` only when all of the following
are satisfied:

1. Required Subtasks are complete (`[x]`).
2. The Completion Condition is satisfied.
3. Required evidence is recorded in the Task file.
4. The Task file records the Work Unit status as `complete`.
5. `CURRENT.md` is reconciled to reflect the new Work Unit, OR explicit evidence
   states that no projection change is required (e.g., this is the Task's final
   Work Unit and the Task is not yet complete).

Acceptable projection-reconciliation evidence:

> `plan/CURRENT.md §Active Task — Work Unit: <name>` updated to `<next-name>`.

or an equivalent independently checkable statement identifying the new Work Unit
or confirming that no projection change is needed.

**Invariant:** A Work Unit cannot become authoritatively `complete` until its
Task state and navigation projection have been reconciled, or explicitly verified
as requiring no projection change.

## Stale or Missing Navigation (Recovery Behavior)

If CURRENT.md is stale, missing, or points to a completed Work Unit or
non-existent Task:

1. Use the authoritative Task file to identify the actual current Work Unit.
2. Repair CURRENT.md from the Task file.
3. Do not repeat completed work merely because navigation is stale.
4. Record the repair as evidence in the Task file progress notes.

## Authority

The Task file is authoritative for Work Unit state. A Work Unit may be marked
complete only when its Completion Condition is satisfied and the Task file
reflects that state.

An Agent statement that a Work Unit is complete is not authoritative until the
Task file records the completion.

See COMPLETION.md for the precise definition of Work Unit completion.
