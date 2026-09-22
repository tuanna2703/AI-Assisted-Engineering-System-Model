# Work Unit

## Definition

A **Work Unit** is a coherent, bounded portion of a Task. It represents the
smallest division of a Task that has its own completion condition, verification
requirement, and observable outcome.

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

## Execution Protocol

1. Read the Work Unit and all its Subtasks.
2. Execute Subtasks in order unless the Task file specifies otherwise.
3. Verify the Completion Condition after all Subtasks are done.
4. Record required evidence.
5. Mark the Work Unit complete in the Task file.
6. Only then advance CURRENT.md.

**Never advance CURRENT.md before the Task file records Work Unit completion.**

## Authority

The Task file is authoritative for Work Unit state. A Work Unit may be marked
complete only when its Completion Condition is satisfied and the Task file
reflects that state.

An Agent statement that a Work Unit is complete is not authoritative until the
Task file records the completion.

See COMPLETION.md for the precise definition of Work Unit completion.
