# AESM Planning System

## Purpose

`plan/` is the AESM planning governance surface. It answers the question:

> **What engineering work is currently intended?**

`plan/` does **not** answer:

> How is that engineering work executed, governed, persisted, or verified?

That question is answered by AESM — the Engineering Process Model (EPM),
Process Execution Model (PEM), Runtime, and persisted `.aesm/` state.

The planning system governs **intent**. AESM governs **execution authority**.

---

## Agent Entry Protocol

A fresh Agent follows this navigation sequence exactly:

```text
plan/README.md              ← you are here
      ↓
plan/CURRENT.md             ← navigation projection
      ↓
plan/active/<task>.md       ← authoritative Task file, if one exists
      ↓
Task consistency checks     ← verify CURRENT and Task state before execution
      ↓
current Work Unit           ← first Work Unit that is not complete
      ↓
next executable Subtask     ← first Subtask that is not [x]
```

An Agent must not need to scan `IMPLEMENTATION_PLAN.md`, `implementation/`,
`docs/`, or the full `plan/` tree to discover its current work.

### Entry Consistency Assertion

Before executing any Subtask, the Agent must establish all of the following from
repository state:

1. There is at most one active Task file.
2. If `CURRENT.md` identifies an active Task, that Task file exists.
3. If an active Task file exists, its `Source:` field records explicit authorization.
4. The active Task's status and Work Unit state are internally consistent.
5. The selected Work Unit is not `complete`, and contains at least one Subtask that is
   not `[x]`, unless the Task file first requires a state repair.
6. `CURRENT.md` identifies the same active Task and Work Unit, or is repaired before
   execution begins.

If these conditions cannot be established without inference, **stop and repair the
planning record or obtain human clarification**. Do not select work heuristically.

If CURRENT.md and the Task file disagree, **the Task file wins**. CURRENT.md is then
repaired from the authoritative Task file before proceeding.

---

## Planning / AESM Boundary

```text
Planning intent (plan/)
        ≠
AESM execution authority (Runtime / .aesm/)
```

| Question | Answered by |
|----------|-------------|
| What work is intended? | `plan/` |
| What work has been authorized? | Task acceptance criteria + human approval |
| What work was executed? | Runtime evidence + `.aesm/` state |
| What is the current authoritative process state? | `.aesm/<pi-id>/context.json` |
| What proves an engineering result? | Runtime-mediated evidence (tests, persisted history) |
| What proves a planning record? | Task file + Completion Record |

A Task file is a **planning record**. It is not AESM-governed engineering evidence.

---

## CURRENT.md Authority

`plan/CURRENT.md` is a **recoverable navigation projection**.

It identifies:
- The currently active Task, when one exists
- The current Work Unit within that Task
- The path to the Task file
- The next candidate, when explicitly documented

`plan/CURRENT.md` is updated only after the Task file records Work Unit completion,
or when a Task is explicitly activated and its authorization record exists.

It is a convenience pointer, not the source of truth.

**Rule:** If CURRENT.md and the active Task file disagree, the **Task file wins**.
Repair CURRENT.md before proceeding.

If `plan/active/` contains an active Task while CURRENT.md reports no active Task,
the active Task file is authoritative; verify its authorization record, reconcile
CURRENT.md to it, and do not infer a different Task.

If `plan/active/` contains more than one Task, the state is ambiguous. Do not choose
one. Stop and require explicit human resolution.

---

## Work-Unit Transition Protocol

Use this sequence exactly when completing a Work Unit:

1. Complete all required Subtasks.
2. Verify the Work Unit's Completion Condition.
3. Record required planning evidence in the Task file.
4. Mark the Work Unit `complete` in the Task file.
5. Re-read the Task file.
6. Determine the next executable Work Unit.
7. Update `CURRENT.md`.
8. Verify CURRENT.md and Task file agree.
9. Continue.

**Never advance CURRENT.md before step 4 is complete.**

A Work Unit whose Subtasks are all `[x]` but whose Completion Condition or evidence
has not been verified is **not complete**. Repair the Work Unit state before advancing.

---

## Recovery Protocol

At session start, or when returning to work after an interruption:

1. Read `plan/README.md` (this file).
2. Read `plan/CURRENT.md`.
3. Inspect `plan/active/` for active Task files.
4. Resolve any discrepancy between the active directory and CURRENT.md.
5. If more than one active Task exists, stop and obtain explicit human resolution.
6. If an active Task exists, read its `Source:` authorization record.
7. Read the Task file.
8. Determine the Task's actual state from the Task file.
9. Find the first Work Unit that is not `complete`.
10. Within that Work Unit, find the first Subtask that is not `[x]`.
11. Confirm that the selected Work Unit contains unfinished work. If all Subtasks are
    `[x]` while the Work Unit is not complete, repair the Work Unit instead of
    executing a duplicate Subtask.
12. Compare the resolved Task/Work Unit/Subtask against CURRENT.md.
13. If they disagree, the **Task file wins**.
14. Repair CURRENT.md if necessary.
15. Continue from the next executable Subtask.

### Interrupted Authorization Recovery

Promotion can be interrupted between human authorization, Task-file movement, and
CURRENT.md update. Recover as follows:

| Repository state | Recovery |
|---|---|
| Task remains only in `backlog/` | Authorization has not been recorded as activation; obtain/confirm explicit authorization before promotion. |
| Task is in `active/` with valid `Source:`, CURRENT stale/missing | Treat the active Task as authoritative and repair CURRENT.md. |
| Task is in `active/` without valid authorization in `Source:` | Stop; do not infer authorization from location alone. Obtain human clarification. |
| CURRENT names an active Task whose file is missing | Stop and repair the projection; do not invent or select a replacement Task. |
| More than one Task is in `active/` | Stop; require explicit human resolution. |
| CURRENT points to a completed Task | Read the active directory and Task records; repair CURRENT.md from the actual active state. |

An Agent must not rely on conversation history, construction knowledge, or memory of
previous sessions.

---

## Backlog Promotion

Tasks in `plan/backlog/` are candidate future work.

A file under `plan/backlog/` represents a **candidate**. Its presence does
not authorize execution.

### What Constitutes Authorization

A backlog Task becomes executable only after **explicit human authorization**:
an unambiguous human instruction that identifies the intended Task by name
and directs the Agent to activate it.

Acceptable form (example):

> Activate `repository-scoped-dbp-continuation-validation`.

Equivalent wording is acceptable when the intended Task and the instruction
to activate it are unmistakable.

### What Does NOT Constitute Authorization

The following do **not** constitute authorization, individually or combined:

- the Task being listed in `plan/backlog/`;
- the Task being described as "next" in any document;
- a previous Task suggesting it as a successor;
- `plan/CURRENT.md` listing it as a Next Candidate;
- `plan/ROADMAP.md` naming it as a strategic next step;
- the Agent deciding it is logically next;
- the absence of another active Task;
- the Agent inferring authorization from repository state.

### Authorization Record

Once the human authorizes a Task:

1. The Task file moves from `plan/backlog/` to `plan/active/`.
2. `plan/CURRENT.md` is updated to reference it as the Active Task.
3. The active Task file's `Source:` field records the authorization.

The active Task file is the authorization record **only when its Source field contains
the explicit authorization record**. File location alone is not sufficient evidence
if the authorization record is missing or malformed.

### No Autonomous Promotion

**An Agent must not autonomously select or activate a backlog Task.**

An Agent must not activate a backlog Task merely because it appears to be the
logically next task, because no other task is active, or because any planning
document describes it as "next" or "candidate."

The backlog is a holding area, not a queue. Tasks in the backlog are not
necessarily in priority order.

---

## Historical Navigation and Governing Decisions

When prior decisions or context are needed:

1. Read `plan/completed/INDEX.md` to identify relevant completed Tasks.
2. Read the specific completed Task file for decisions, constraints, and evidence.
3. For a new Task, record applicable prior decisions under **Governing Decisions**.
4. If a prior decision is intentionally changed, record the supersession explicitly
   in the new Task rather than silently omitting the older decision.

A `Governing Decisions` entry should identify:
- Source Task ID
- Decision summary
- Why it applies to the new Task

Only decisions that constrain the new Task need to be listed. This is a bounded
traceability requirement, not a requirement to reproduce the entire history.

The index provides task identity, completion date, purpose, and concern tags.
It does not duplicate complete task contents.

The `IMPLEMENTATION_PLAN.md` in the repository root is a legacy document
superseded by this planning system. Read it only for migration and reconciliation
during the active Planning System Restructuring task.

---

## Planning Evidence Contract

Planning evidence must make a completed Subtask independently checkable.

Acceptable evidence normally identifies at least one of:
- a repository path plus the relevant property/result;
- an executable command plus its observed result;
- a test name/count plus its pass result;
- a Git diff/commit reference;
- an explicit blocked/finding record explaining why verification could not occur.

Generic assertions such as `verified`, `done`, or `file created` are not sufficient
by themselves.

If required evidence cannot be obtained, record the finding or block the Subtask;
do not convert the absence of evidence into a completion claim.

Planning evidence remains distinct from AESM Runtime evidence. A planning evidence
reference does not prove Runtime state or engineering completion.

---

## Task Closure

A Task remains `in-progress` until its Completion Record contains the required
verification evidence and the Task's acceptance criteria are satisfied.

Having every Work Unit marked `complete` is necessary but not sufficient.

A Task with all Work Units complete but a missing, incomplete, or unsupported
Completion Record is **verification-pending within `in-progress`**, not complete.

A Task may move to `plan/completed/` only after:
- all Work Units are complete;
- acceptance criteria are satisfied;
- required verification is complete;
- Completion Record evidence is populated;
- Task status is `complete`.

---

## Directory Reference

```text
plan/
├── README.md              ← this file; Agent entry point
├── CURRENT.md             ← navigation projection; active Task + Work Unit
├── ROADMAP.md             ← long-term strategic direction
├── PRINCIPLES.md          ← governing principles; Runtime authority boundary
├── definitions/
│   ├── TASK.md            ← what a Task is
│   ├── WORK-UNIT.md       ← what a Work Unit is
│   ├── SUBTASK.md         ← what a Subtask is
│   ├── STATUS.md          ← allowed planning states
│   └── COMPLETION.md      ← completion levels and conditions
├── active/
│   └── <task-id>.md       ← active Task files (authoritative state)
├── backlog/
│   └── <task-id>.md       ← candidate future Tasks
└── completed/
    ├── INDEX.md            ← index of completed Tasks
    └── <task-id>.md       ← completed Task files (historical record)
```

---

## Governing Rules (Summary)

1. A Task file is authoritative. CURRENT.md is a projection.
2. A Work Unit may be marked complete only when its Completion Condition is satisfied.
3. CURRENT.md advances only after the Task file records completion, except for explicit Task activation.
4. Planning completion ≠ AESM engineering completion.
5. A planning record is not Runtime evidence.
6. Backlog Tasks require explicit authorization before activation.
7. Interrupted promotion is recovered from repository state and the authorization record; ambiguity stops execution.
8. Applicable prior decisions are recorded under Governing Decisions.
9. Planning evidence must be independently checkable.
10. A Task with incomplete final verification remains in-progress.
11. Completed Task files are permanent historical records; they are not deleted.
12. Decisions recorded in completed Tasks under "Decisions Still in Effect" remain binding unless explicitly superseded.
13. If a required answer cannot be found in `plan/`, it is not a planning question — consult `docs/` for AESM semantics or `.aesm/` for authoritative process state.
