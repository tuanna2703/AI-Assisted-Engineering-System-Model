# Status

## Allowed Planning States

These are the only allowed status values in the `plan/` system. Do not introduce
additional states without updating this definition and recording the decision.

| Status | Marker | Meaning |
|--------|--------|---------|
| `not-started` | `[ ]` | The item has been defined but execution has not begun. |
| `in-progress` | `[/]` | Execution has begun; some Subtasks are complete; the Completion Condition is not yet satisfied. |
| `complete` | `[x]` | All Subtasks are done; the Completion Condition is satisfied; evidence is recorded. |
| `blocked` | `[!]` | Execution cannot continue until an explicit condition is resolved. The blocking reason must be recorded immediately after the status marker. |

## Distinction: `not-started` vs `in-progress`

- `not-started`: nothing has been done. The item exists in the plan but no
  Subtask has been started.
- `in-progress`: at least one Subtask has been executed. The Work Unit or Task
  has not yet satisfied its Completion Condition.

A Task remains `in-progress` while final acceptance or verification is incomplete,
even if every Work Unit is marked `complete`.

Do not introduce a separate `verification-pending` status unless a demonstrated
need makes the existing `in-progress` state insufficient.

Do not use "current" as a status. The current item is determined by reading
`CURRENT.md` and the active Task file. Status reflects execution state, not
navigation position.

## Prohibited States

The following terms must not appear as status values:

- `current` (use `in-progress`; navigation position is in CURRENT.md)
- `pending` (use `not-started` or `blocked`)
- `done` (use `complete`)
- `wip` (use `in-progress`)

## Status in Task Files

Task-level status applies to the whole Task:

```markdown
Status:
in-progress
```

Work Unit status appears within the Work Units section:

```markdown
### Work Unit Name

Status: in-progress
```

Subtask status uses checkbox markers within the Subtask list:

```markdown
- [x] Inspect existing repository structure — evidence: plan/active/planning-system-restructuring.md; inspection recorded.
- [/] Create planning directory skeleton
- [ ] Write definitions files
```

## Progression

Status must progress forward through the Task file as execution occurs.

An Agent must not:

- Mark a Work Unit `complete` while a Subtask within it is `in-progress` or `not-started`.
- Mark a Task `complete` while a Work Unit within it is not `complete`.
- Mark a Task `complete` while acceptance criteria or required verification remain incomplete.
- Mark any item `complete` without recording evidence of the Completion Condition being satisfied.
- Treat unsupported `[x]` markers as authoritative when their evidence cannot be verified.

## CURRENT.md and Status

`CURRENT.md` reflects the current active item after the Task file records
completion of the previous item. See `plan/README.md` for the work-unit
transition and recovery protocols.

If CURRENT.md and the Task file disagree about what is active, the **Task file wins**.
