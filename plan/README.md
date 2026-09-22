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
Task consistency checks     ← verify authorization, CURRENT, and Task state before execution
      ↓
current Work Unit           ← first Work Unit that is not complete
      ↓
next executable Subtask     ← first Subtask that is not [x] and not [!]
```

An Agent must not need to scan `IMPLEMENTATION_PLAN.md`, `implementation/`,
`docs/`, or the full `plan/` tree to discover its current work.

### Entry Consistency Assertion

Before executing any Subtask, the Agent must establish all of the following from
repository state:

1. There is at most one active Task file.
2. If `CURRENT.md` identifies an active Task, that Task file exists.
3. If an active Task file exists, its `Source:` field contains a mechanically
   sufficient authorization record (see §Authorization Record Requirements).
4. The active Task's status and Work Unit state are internally consistent.
5. The selected Work Unit is not `complete`, and contains at least one Subtask
   that is not `[x]`, unless the Task file first requires a state repair.
6. `CURRENT.md` identifies the same active Task and Work Unit, or is repaired
   before execution begins.
7. If the next unfinished Subtask is `[!]` (blocked), do not execute. Surface
   the blocker to the human instead (see §Blocked-Task Recovery Path).

If these conditions cannot be established without inference, **stop and repair the
planning record or obtain human clarification**. Do not select work heuristically.

If CURRENT.md and the Task file disagree, **the Task file wins**. CURRENT.md is then
repaired from the authoritative Task file before proceeding.

**The Entry Consistency Assertion stops execution when authorization is missing or
structurally insufficient.** An Agent must not infer authorization from Task
location, CURRENT.md, prior conversation, or apparent logical sequence.

---

## Authorization Record Requirements

A mechanically sufficient authorization record in a Task's `Source:` field must
identify all four of the following:

1. **Authorization date** — when the authorization was given.
2. **Nature/source of the instruction** — who or what authorized the Task (e.g.,
   human instruction, authorized engineering prompt, explicit approval).
3. **Authorized Task identity** — the Task being authorized, by name or ID.
4. **Authorized action or scope** — what the Agent is authorized to do.

### Authorization Provenance vs Task Provenance vs Execution Evidence

These three are distinct and must not be conflated:

**Authorization provenance** — why the Task is authorized to execute.
Records the human instruction or approval that grants execution authority.

**Task provenance** — why the Task exists. Records prior work, investigation,
or planning decisions that motivated the Task's creation.

**Execution evidence** — what actually happened while executing the Task.
Records commands run, results observed, tests passed, blockers encountered.

A `Source:` field that conflates task provenance with authorization provenance is
insufficient as an authorization record.

### Invalid Authorization

Authorization is insufficient when the Agent would have to infer it from:

- Task existence in `plan/backlog/`;
- Task existence in `plan/active/`;
- CURRENT.md alone;
- previous conversation context alone;
- apparent logical sequence of tasks;
- another Task's completion or suggestion;
- presumed continuation from prior sessions;
- an ambiguous `Source:` field.

When authorization is insufficient or missing, the Entry Consistency Assertion
requires the Agent to stop and obtain explicit human clarification. The Agent
must not infer or reconstruct authorization.

### Compatibility with Existing Tasks

Existing Tasks may use an older `Source:` format. This is a compatibility rule,
not a retroactive assertion that historical records satisfied the new structure.

If an existing Task's historical `Source:` field identifies a genuine human
authorization instruction — even in abbreviated form — that Task may continue
under the new authorization model without retroactive rewriting.

For such Tasks:
- Preserve the historical Source text exactly.
- Do not invent missing details.
- Do not rewrite historical authorization.
- Treat the genuine human instruction as sufficient historical provenance.
- Apply the new structured authorization requirements to newly created Tasks.

If a historical Task cannot be established as genuinely human-authorized from its
existing record, apply the normal recovery rule: stop and surface the discrepancy.

---

## Blocked-Task Recovery Path

### Blocked vs In-Progress

A blocked state is distinct from ordinary `in-progress`:

| State | Meaning |
|-------|---------|
| `in-progress` | Execution has begun; work can legitimately continue. |
| `blocked` (Work Unit) | A required condition cannot be met; the Work Unit cannot advance until the blocking condition is resolved. |
| `[!]` (Subtask) | This specific Subtask cannot execute; the blocking reason is recorded immediately after the marker. |

A blocked Task or Work Unit is not simply an unfinished one. It contains a
recorded condition that prevents legitimate progress.

### Fresh-Agent Blocked-Subtask Protocol

When a fresh Agent encounters a `[!]` Subtask as the next required Subtask:

1. Identify the blocker by reading the text immediately following the `[!]` marker.
2. Inspect the recorded evidence to understand the blocking condition.
3. Determine whether the blocking condition has actually been resolved since the
   blocker was recorded — from repository state, not from conversation history.
4. If the blocker remains unresolved:
   a. Surface the blocking condition to the human.
   b. Stop execution of that blocked work.
   c. Do not invent a workaround.
   d. Do not silently substitute another Task.
   e. Do not reinterpret the blocker as authorization to change scope.
5. A fresh Agent may resume blocked work only when the blocking condition has been
   explicitly resolved in the planning record and the `[!]` marker updated.

### Blocked Work Units

A Work Unit whose next required Subtask is `[!]` is operationally blocked,
regardless of whether the Work Unit's status field says `not-started` or
`in-progress`. The Work Unit status field must accurately reflect the operational
state:

- If no Subtask has been started: `not-started`.
- If at least one Subtask is `[x]` or `[!]`: `in-progress`.
- If a required condition prevents the remaining Subtasks from proceeding: the
  Work Unit's `Blocked condition:` section must record the blocker.

Structural state (status markers, Work Unit status) must be consistent with
substantive evidence (what actually happened). When they conflict, correct the
structural state from the evidence — do not alter the substantive evidence to
make structural state look consistent.

### Blocked Task

A Task is operationally blocked when its current Work Unit is blocked and no
other Work Unit is available to execute. The Task's overall status remains
`in-progress` (the blocking condition exists within the in-progress execution;
do not invent a separate `blocked` Task-level status). The blocking condition
must be recorded in the affected Work Unit.

---

## CURRENT.md Authority

`plan/CURRENT.md` is a **recoverable navigation projection**.

It identifies:
- The currently active Task, when one exists
- The current Work Unit within that Task
- The path to the Task file
- The next candidate, when explicitly documented

`plan/CURRENT.md` is updated only after the Task file records Work Unit
completion, or when a Task is explicitly activated and its authorization record
exists.

It is a convenience pointer, not the source of truth.

**Rule:** If CURRENT.md and the active Task file disagree, the **Task file wins**.
Repair CURRENT.md before proceeding.

If `plan/active/` contains an active Task while CURRENT.md reports no active Task,
the active Task file is authoritative; verify its authorization record, reconcile
CURRENT.md to it, and do not infer a different Task.

If `plan/active/` contains more than one Task, the state is ambiguous. Do not
choose one. Stop and require explicit human resolution.

---

## Work-Unit Transition Protocol

Use this sequence exactly when completing a Work Unit:

1. Complete all required Subtasks.
2. Verify the Work Unit's Completion Condition.
3. Record required planning evidence in the Task file.
4. Mark the Work Unit `complete` in the Task file.
5. Re-read the Task file.
6. Determine the next executable Work Unit.
7. Update `CURRENT.md` to reflect the new Work Unit (or confirm no change needed
   and record that explicitly).
8. Verify CURRENT.md and Task file agree.
9. Continue.

**Never advance CURRENT.md before step 4 is complete.**

**A Work Unit may not be marked `complete` until CURRENT.md is reconciled** or
explicit evidence states that no projection change is required (e.g., the task
has no subsequent Work Unit).

Acceptable projection-reconciliation evidence identifies:

> `plan/CURRENT.md §Active Task — Work Unit: <name>` updated to `<next-name>`.

or an equivalent independently checkable statement.

A Work Unit whose Subtasks are all `[x]` but whose Completion Condition or
evidence has not been verified is **not complete**. Repair the Work Unit state
before advancing.

### Stale or Missing CURRENT.md

If CURRENT.md is stale, missing, or points to a completed or nonexistent Work
Unit or Task, the Agent must:

1. Use authoritative Task state to identify the actual active Work Unit.
2. Repair CURRENT.md from the Task file.
3. Not repeat completed work merely because navigation is stale.
4. Evidence the repair (e.g., record in Task file progress notes).

**Invariant:** A Work Unit cannot become authoritatively `complete` until its
Task state and navigation projection have been reconciled, or explicitly verified
as requiring no projection change.

---

## Recovery Protocol

At session start, or when returning to work after an interruption:

1. Read `plan/README.md` (this file).
2. Read `plan/CURRENT.md`.
3. Inspect `plan/active/` for active Task files.
4. Resolve any discrepancy between the active directory and CURRENT.md.
5. If more than one active Task exists, stop and obtain explicit human resolution.
6. If an active Task exists, read its `Source:` authorization record.
7. Verify the authorization record is mechanically sufficient (§Authorization Record
   Requirements). If insufficient, stop and obtain human clarification.
8. Read the Task file.
9. Determine the Task's actual state from the Task file.
10. Find the first Work Unit that is not `complete`.
11. Within that Work Unit, find the first Subtask that is not `[x]`.
12. If that Subtask is `[!]` (blocked), follow §Blocked-Task Recovery Path.
13. Confirm that the selected Work Unit contains unfinished, unblocked work. If all
    Subtasks are `[x]` while the Work Unit is not complete, repair the Work Unit
    instead of executing a duplicate Subtask.
14. Compare the resolved Task/Work Unit/Subtask against CURRENT.md.
15. If they disagree, the **Task file wins**.
16. Repair CURRENT.md if necessary.
17. Continue from the next executable Subtask.

### Interrupted Authorization Recovery

Promotion can be interrupted between human authorization, Task-file movement, and
CURRENT.md update. Recover as follows:

| Repository state | Recovery |
|---|---|
| Task remains only in `backlog/` | Authorization has not been recorded as activation; obtain/confirm explicit authorization before promotion. |
| Task is in `active/` with mechanically sufficient `Source:`, CURRENT stale/missing | Treat the active Task as authoritative and repair CURRENT.md. |
| Task is in `active/` without mechanically sufficient authorization in `Source:` | Stop; do not infer authorization from location alone. Obtain human clarification. |
| CURRENT names an active Task whose file is missing | Stop and repair the projection; do not invent or select a replacement Task. |
| More than one Task is in `active/` | Stop; require explicit human resolution. |
| CURRENT points to a completed Task | Read the active directory and Task records; repair CURRENT.md from the actual active state. |
| CURRENT points to a completed Work Unit within the active Task | Repair CURRENT.md from the Task file; do not re-execute the completed Work Unit. |

An Agent must not rely on conversation history, construction knowledge, or memory
of previous sessions.

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
3. The active Task file's `Source:` field records a mechanically sufficient
   authorization record (date, nature, authorized Task identity, authorized scope).

The active Task file is the authorization record **only when its Source field
contains a mechanically sufficient authorization record**. File location alone is
not sufficient evidence if the authorization record is missing or malformed.

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

### Decision Lifecycle

A governing decision made in a completed Task has one of the following
relationships in a later Task:

**Qualified** — The earlier decision remains applicable, but its scope,
interpretation, conditions, or applicability has been narrowed or otherwise
changed. The later Task records: prior Task ID, decision summary, relationship
(`qualified`), what remains applicable, what changed, and why.

**Superseded** — The earlier decision no longer governs the relevant situation
because a later decision replaces it. The later Task records: prior Task ID,
decision summary, relationship (`superseded`), what the new decision is, and why.

When a later Task qualifies or supersedes an earlier decision, that relationship
must be recorded in the later Task's `Governing Decisions` or `Decisions Still in
Effect` section with sufficient detail to allow a future reader to trace the
decision lineage without reading full conversation history.

These relationships are exposed in `plan/completed/INDEX.md` so a fresh Agent
can discover them through index inspection.

### Index Discoverability

`plan/completed/INDEX.md` must expose decision qualifications and supersessions
that are relevant to future planning and recovery. Historical Task records remain
historically accurate; a later qualification or supersession does not rewrite the
earlier Task's content.

A `Governing Decisions` entry must identify:
- Source Task ID
- Decision summary
- Why it applies to the new Task
- Relationship (`qualified` / `superseded`) if applicable

Only decisions that constrain the new Task need to be listed. This is a bounded
traceability requirement, not a requirement to reproduce the entire history.

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

### Explicit Planning/Runtime Separation

The following are **planning-system statements** that do not constitute AESM
engineering evidence or process state:

- A Task file's checkboxes, status fields, or Completion Record.
- Any Subtask evidence recorded in a planning file.
- Git operations, file edits, or test runs performed by an Agent executing a
  planning Task — unless those operations are also Runtime-mediated engineering
  operations under a separately authorized engineering scope.
- CURRENT.md navigation state.

The following require AESM Runtime authority and cannot be substituted by
planning records:

- Creating, attaching to, or mutating a Process Instance.
- Asserting Execution Context state.
- Claiming AESM Engineering Completion.
- Producing persisted `.aesm/` state transitions.

**A planning Task does not itself:**
- Create a Process Instance.
- Attach to a Process Instance.
- Mutate authoritative Execution Context.
- Produce AESM Runtime evidence.
- Constitute AESM Engineering Completion.

Repository inspection, file editing, Git operations, and test execution performed
during a planning Task are **planning operations**. They are not automatically
Runtime participation.

Planning evidence must not be represented as `RUNTIME`, `PERSISTED`, or equivalent
AESM evidence merely because the Agent used tools.

### Exception: Planning Tasks Governing Engineering Work

A planning Task may govern or accompany Runtime-mediated engineering work only
when its authorized scope explicitly includes that engineering work.

Even then:
- Runtime remains authoritative.
- Process Instance state remains Runtime-owned.
- Execution Context remains Runtime-owned.
- Planning records cannot substitute for Runtime evidence.

A Task file is a **planning record**. It is not AESM-governed engineering evidence.

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
    ├── INDEX.md            ← index of completed Tasks with decision qualifications
    └── <task-id>.md       ← completed Task files (historical record)
```

---

## Governing Rules (Summary)

1. A Task file is authoritative. CURRENT.md is a navigation projection.
2. A Work Unit may be marked complete only when its Completion Condition is satisfied.
3. CURRENT.md advances only after the Task file records completion and projection is reconciled.
4. Planning completion ≠ AESM engineering completion.
5. A planning record is not Runtime evidence.
6. Backlog Tasks require explicit, mechanically sufficient authorization before activation.
7. Interrupted promotion is recovered from repository state and the authorization record; ambiguity stops execution.
8. Applicable prior decisions are recorded under Governing Decisions with explicit relationship (qualified/superseded where applicable).
9. Planning evidence must be independently checkable.
10. A Task with incomplete final verification remains in-progress.
11. Completed Task files are permanent historical records; they are not deleted.
12. Decisions recorded in completed Tasks under "Decisions Still in Effect" remain binding unless explicitly superseded.
13. If a required answer cannot be found in `plan/`, it is not a planning question — consult `docs/` for AESM semantics or `.aesm/` for authoritative process state.
14. A blocked Subtask (`[!]`) must be surfaced to the human; it must not be worked around or silently skipped.
15. A planning Task does not create, attach to, or mutate a Process Instance or Execution Context.
16. Work Unit completion requires navigation-projection reconciliation or explicit no-change verification.
