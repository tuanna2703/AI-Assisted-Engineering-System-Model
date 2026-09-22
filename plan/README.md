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
plan/CURRENT.md             ← identifies the active Task and current Work Unit
      ↓
plan/active/<task>.md       ← the authoritative Task file
      ↓
current Work Unit section   ← find the in-progress or first not-started Work Unit
      ↓
next executable Subtask     ← the first [ ] Subtask under that Work Unit
```

An Agent must not need to scan `IMPLEMENTATION_PLAN.md`, `implementation/`,
`docs/`, or the full `plan/` tree to discover its current work.

If CURRENT.md and the Task file disagree about what is active, **the Task file wins**.
Read the Task file directly and repair CURRENT.md before proceeding.

---

## Planning / AESM Boundary

```text
Planning intent (plan/)
        ≠
AESM execution authority (Runtime / .aesm/)
```

| Question | Answered by |
|----------|------------|
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
- The currently active Task
- The current Work Unit within that Task
- The path to the Task file

`plan/CURRENT.md` is updated only after the Task file records Work Unit completion.
It is a convenience pointer, not the source of truth.

**Rule:** If CURRENT.md and the active Task file disagree, the **Task file wins**.
Repair CURRENT.md before proceeding.

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

---

## Recovery Protocol

At session start, or when returning to work after an interruption:

1. Read `plan/README.md` (this file).
2. Read `plan/CURRENT.md`.
3. Resolve the referenced Task file path.
4. Read the Task file.
5. Determine the Task's actual state from the Task file.
6. Find the first Work Unit that is not `complete`.
7. Within that Work Unit, find the first Subtask that is not `[x]`.
8. Compare the current Work Unit and Subtask against what CURRENT.md says.
9. If they disagree, the **Task file wins**.
10. Repair CURRENT.md if necessary.
11. Continue from the next executable Subtask.

An Agent must not rely on conversation history, construction knowledge, or
memory of previous sessions. The Task file contains the authoritative record.

---

## Backlog Promotion

Tasks in `plan/backlog/` are candidate future work.

**An Agent must not autonomously select a backlog Task.**

Promotion from backlog to active requires an explicit planning decision — a
human instruction that authorizes the Task. When authorized, the Task file moves
to `plan/active/` and CURRENT.md is updated.

The backlog is a holding area, not a queue. Tasks in the backlog are not
necessarily in priority order.

---

## Historical Navigation

When prior decisions or context are needed:

1. Read `plan/completed/INDEX.md` to identify relevant completed Tasks.
2. Read the specific completed Task file for decisions, constraints, and evidence.
3. Decisions recorded in completed Task files under "Decisions Still in Effect"
   remain active constraints.

The index provides task identity, completion date, purpose, and concern tags.
It does not duplicate complete task contents.

The `IMPLEMENTATION_PLAN.md` in the repository root is a legacy document
superseded by this planning system. Read it only for migration and reconciliation
during the active Planning System Restructuring task.

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
3. CURRENT.md advances only after the Task file records completion.
4. Planning completion ≠ AESM engineering completion.
5. A planning record is not Runtime evidence.
6. Backlog Tasks require explicit authorization before activation.
7. Completed Task files are permanent historical records; they are not deleted.
8. Decisions recorded in completed Tasks under "Decisions Still in Effect" remain binding.
9. If a required answer cannot be found in `plan/`, it is not a planning question — consult `docs/` for AESM semantics or `.aesm/` for authoritative process state.
