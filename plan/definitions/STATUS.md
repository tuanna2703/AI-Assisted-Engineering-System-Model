# Status

## Allowed Planning States

These are the only allowed status values in the `plan/` system. Do not introduce
additional states without updating this definition and recording the decision.

### Subtask and Work Unit Status Markers

| Status | Marker | Meaning |
|--------|--------|---------|
| `not-started` | `[ ]` | The item has been defined but execution has not begun. |
| `in-progress` | `[/]` | Execution has begun; some Subtasks are complete; the Completion Condition is not yet satisfied. |
| `complete` | `[x]` | All Subtasks are done; the Completion Condition is satisfied; evidence is recorded. |
| `blocked` | `[!]` | Execution cannot continue until an explicit condition is resolved. The blocking reason must be recorded immediately after the status marker. |

### Task-Level Status Values

Task-level `Status:` fields use text values, not checkbox markers:

| Status | Meaning |
|--------|---------|
| `not-started` | The Task has been defined but no Work Unit has begun. |
| `in-progress` | Execution has begun; Work Units are being executed; the Task is not yet complete. |
| `blocked` | The Task cannot advance and has been durably removed from the active execution position. A `Blocking Condition` section must be present. The Task is stored in `plan/blocked/`. See `plan/definitions/BLOCKED.md`. |
| `complete` | All Work Units are complete; acceptance criteria are satisfied; Completion Record is populated; the Task is in `plan/completed/`. |
| `superseded` | The Task was intentionally replaced or made unnecessary by another authorized planning decision. Terminal. Stored in `plan/completed/`. |

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

## Distinction: `in-progress` vs `blocked` (Work Unit, Subtask, and Task)

| Level | `in-progress` | `blocked` |
|-------|---------------|-----------|
| Subtask | Execution has begun and can continue. | `[!]` marker; blocking reason recorded immediately after; cannot advance. |
| Work Unit | At least one Subtask started; Completion Condition not yet satisfied. | `Blocked condition:` section present; required condition prevents remaining Subtasks from proceeding. |
| Task | Work Units are being executed. | Task-level `Status: blocked`; `Blocking Condition` section present; Task is in `plan/blocked/`; not the active Task. |

**Work Unit blocking:** When a Work Unit's next required Subtask is `[!]`, the
Work Unit is operationally blocked. The Work Unit status remains `in-progress`
if at least one Subtask has started.

**Task-level blocking:** A Task is operationally blocked (Task-level `blocked`)
when its current Work Unit is blocked and no other Work Unit is available to
execute in the same Task. In this case:
- The Task must be moved from `plan/active/` to `plan/blocked/`.
- The Task's `Status:` field is changed to `blocked`.
- A `Blocking Condition` section is added to the Task file.
- The Task is removed from `plan/active/`; there is then no active Task.
- See `plan/definitions/BLOCKED.md` for the full lifecycle definition.

A Work Unit with at least one `[x]` or `[!]` Subtask is `in-progress`, not
`not-started`. The presence of `[!]` does not reset the Work Unit to
`not-started`; it reflects an operational impediment within in-progress
execution.

## Prohibited States

The following terms must not appear as status values:

- `current` (use `in-progress`; navigation position is in CURRENT.md)
- `pending` (use `not-started` or `blocked`)
- `done` (use `complete`)
- `wip` (use `in-progress`)
- `cancelled` (use `superseded` with an explicit supersession record)

## Status in Task Files

Task-level status applies to the whole Task:

```markdown
Status:
in-progress
```

A blocked Task uses:

```markdown
Status:
blocked
```

A superseded Task uses:

```markdown
Status:
superseded
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
- Change a Blocking Condition `Status: OPEN` to `Status: RESOLVED` by inference.
- Infer Task reactivation from Resolution Task completion, `Status: RESOLVED`, or `ELIGIBLE FOR REACTIVATION` alone.

## Terminal Statuses: `complete` vs `superseded`

Both `complete` and `superseded` are terminal statuses. Both are stored in
`plan/completed/`. Neither may be reactivated as if it were merely blocked.

| Status | Meaning | Reactivatable? |
|--------|---------|----------------|
| `complete` | The Task's intended work was completed. | No — terminal. |
| `superseded` | The Task was intentionally replaced or made unnecessary by another authorized planning decision. | No — terminal. |
| `blocked` | The Task cannot advance; blocker is recorded; remains required unless superseded. | Yes — only via explicit reactivation authorization. |

Supersession must be explicitly recorded in the Task file and in
`plan/completed/INDEX.md`. It must not be inferred.

---

## CURRENT.md and Status

`CURRENT.md` reflects the current active item after the Task file records
completion of the previous item. See `plan/README.md` for the work-unit
transition and recovery protocols.

If CURRENT.md and the Task file disagree about what is active, the **Task file wins**.

---

## Structural State vs. Substantive Evidence

These are distinct and must not be conflated when repairing planning records.

**Structural state** is planning metadata describing where work stands:
- `[ ]`, `[x]`, `[!]`, `[/]` markers
- `Status:` fields
- Work Unit status
- Navigation/projection metadata (CURRENT.md Work Unit pointer)

**Substantive evidence** is the recorded content describing what actually happened:
- Observed conditions
- Executed commands and their results
- Test results
- Git results
- Discovered blockers
- Historical findings and decisions
- Verification outcomes

When structural state conflicts with substantive evidence, **correct the structural
state from the evidence**. Do not alter substantive evidence to make structural
state appear consistent. If substantive evidence is missing or ambiguous, do not
manufacture it.
