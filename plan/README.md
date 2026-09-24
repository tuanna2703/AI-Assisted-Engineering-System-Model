# AESM Planning System

## Purpose

`plan/` answers: **What engineering work is currently intended?**

It does not answer how work is executed, governed, persisted, or verified.
That is answered by AESM — the Runtime, `.aesm/` state, and `docs/` semantics.
Planning governs **intent**. AESM governs **execution authority**.

## Navigation

A fresh Agent reads three things to reach executable work:

1. **`plan/README.md`** — this file; governance and rules.
2. **`plan/CURRENT.md`** — active task + work unit, or reason none exists.
3. **Active task file** — `plan/active/<task-id>.md`; authoritative state.

Within the task file, find the first Work Unit that is not complete, then find
the first Subtask that is not `[x]` and not `[!]`.

Before executing, verify three preconditions:

1. The task file's `Source:` field contains a mechanically sufficient
   authorization record (see §Authorization).
2. An active task file exists in `plan/active/` (at most one).
3. The next Subtask is not `[!]` (blocked). If it is, surface the blocker
   to the human and stop.

If CURRENT.md and the task file disagree, **the task file wins**. Repair
CURRENT.md before proceeding.

## Authorization

A task's `Source:` field must identify all four of the following:

1. **Date** — when authorization was given.
2. **Source** — who authorized it (e.g., human instruction).
3. **Task identity** — which task is authorized, by name or ID.
4. **Scope** — what the Agent is authorized to do.

Authorization is **not** established by: task location, CURRENT.md, prior
conversation, logical sequence, another task's completion, or an ambiguous
`Source:` field. When authorization is missing, stop and obtain human
clarification.

Existing tasks with older `Source:` formats may continue if a genuine human
authorization instruction is identifiable. Apply the full structured format
to newly created tasks.

**Backlog promotion:** Tasks in `plan/backlog/` are candidates. A backlog task
becomes executable only after an explicit human instruction that identifies
the task by name and directs activation. An Agent must not autonomously
activate a backlog task.

## Task Structure

```
Task → Work Unit → Subtask
```

**Task** — a bounded engineering objective. File in `plan/active/` (at most
one) or `plan/completed/`. Contains identity, objective, constraints,
governing decisions, work units, acceptance criteria, and completion record.

**Work Unit** — a coherent portion of a task with its own completion condition.
Executed in order. Complete when all Subtasks are `[x]`, Condition is
satisfied, evidence is recorded, and CURRENT.md is reconciled.

**Subtask** — a concrete, executable action. Must specify what to change and
how to verify. Completed Subtasks require independently checkable evidence.

### Status Markers

| Context | Marker / Value | Meaning |
|---------|----------------|---------|
| Subtask | `[ ]` | Not yet done |
| Subtask | `[x]` | Complete — evidence required |
| Subtask | `[!]` | Blocked — reason required immediately after |
| Task | `active` | In execution (file in `active/`) |
| Task | `blocked` | In `active/`; halted; requires human instruction to resume |
| Task | `complete` | In `completed/`; terminal |
| Task | `superseded` | In `completed/`; terminal; explicitly replaced |

Completed and superseded are both terminal. Neither may be reactivated.
Supersession must be explicitly recorded; it must not be inferred.

## Blocked Tasks

A blocked task stays in `plan/active/` with `Status: blocked`. Its task file
contains a `## Blocked` section with three fields:

```
## Blocked
Reason:    <why execution cannot continue>
Resume At: <exact subtask text>
Condition: <what must be true before resuming>
```

**To block:** Add `## Blocked` section → set `Status: blocked` → update CURRENT.md.

**To resume:** Human provides explicit instruction → Agent removes `## Blocked`
→ sets `Status: active` → updates CURRENT.md → continues from Resume At.

A fresh Agent encountering a `[!]` Subtask must surface the blocker to the
human and stop. Do not invent workarounds or silently substitute another task.

## Scope Control

For any execution discovery that could cause additional action:

1. **In scope** — the action is explicitly covered by the current authorized
   Subtask or Work Unit condition. Continue.
2. **Out of scope** — not explicitly covered. Record as a note (future work
   or observation). Do not execute.
3. **Blocking** — an out-of-scope condition prevents an existing acceptance
   criterion from being satisfied. Add `[!]` with reason. Surface to human. Stop.

Semantic relatedness, usefulness, severity, or convenience are not
authorization criteria. A discovery is evidence, not authorization.

## Completion

**Subtask:** Action performed + independently checkable evidence recorded.

**Work Unit:** All Subtasks `[x]` + Condition satisfied + evidence recorded +
CURRENT.md reconciled (or explicitly verified as requiring no change).

**Task:** All Work Units complete + acceptance criteria satisfied + Completion
Record populated + task moved to `plan/completed/` + INDEX.md updated.

**Planning completion ≠ AESM engineering completion.** A completed task file
is a planning record. It does not prove Runtime state, Process Instance
transitions, or engineering completion under AESM. Runtime remains
authoritative for `.aesm/` state. Planning evidence is not Runtime evidence.

## Planning Boundary

A planning task does not create, attach to, or mutate a Process Instance or
Execution Context. Repository inspection, file editing, Git operations, and
test execution during a planning task are planning operations — not Runtime
participation. A task may govern engineering work only when its authorized
scope explicitly includes it; even then, Runtime remains authoritative.

## Governing Rules

1. The task file is authoritative. CURRENT.md is a navigation projection.
2. A Work Unit is complete only when its Condition is satisfied and
   CURRENT.md is reconciled.
3. Planning completion ≠ AESM engineering completion.
4. A planning record is not Runtime evidence.
5. Backlog tasks require explicit human authorization before activation.
6. Prior governing decisions are recorded under Governing Decisions with
   explicit relationship (qualified / superseded).
7. Completed task files are permanent historical records; never deleted.
8. A blocked Subtask (`[!]`) must be surfaced to the human; not skipped.
9. Execution discoveries do not create authorization.
10. No work executes without explicit human authorization.

## Directory Reference

```
plan/
├── README.md           ← this file; single governance document
├── CURRENT.md          ← active task + work unit; or no-task reason
├── active/
│   └── <task-id>.md   ← at most one; blocked tasks stay here (Status: blocked)
├── backlog/
│   └── <task-id>.md   ← candidate tasks; not authorized for execution
└── completed/
    ├── INDEX.md        ← compact task registry + active decisions table
    ├── TEMPLATE.md     ← format template for future tasks
    └── <task-id>.md   ← completed tasks; permanent historical records
```
