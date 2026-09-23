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
[No active Task?]           ← check plan/blocked/INDEX.md; if blocked Tasks exist,
                              read blocker; surface to human; do not self-activate
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

## Blocked-Task Lifecycle

### Blocking at Three Levels

Blocking may occur at three distinct levels:

| Level | Representation | Location |
|-------|---------------|----------|
| Subtask | `[!]` marker; reason immediately after | Within Work Unit in Task file |
| Work Unit | `Blocked condition:` section | Within Task file |
| Task | `Status: blocked`; `Blocking Condition` section | Task file in `plan/blocked/` |

See `plan/definitions/BLOCKED.md` for the complete lifecycle definition.

### When a Task Becomes Blocked (Task-Level)

A Task is operationally blocked at the Task level when:
- Its current Work Unit is blocked and no other Work Unit can execute, and
- The blocking condition requires external resolution outside the Task's scope.

When a Task becomes blocked at the Task level:
1. The Task's `Status:` is changed to `blocked`.
2. A `Blocking Condition` section is added immediately after the `Identity` section.
3. The Task file is moved from `plan/active/` to `plan/blocked/`.
4. An entry is added to `plan/blocked/INDEX.md`.
5. `CURRENT.md` is updated to reflect no active Task (with reason: work is blocked).

A blocked Task is not an active Task. At most one Task may reside in `plan/active/`;
a blocked Task does not occupy the active slot.

### Blocking Condition Structure

Every blocked Task file must contain:

```markdown
## Blocking Condition

Status: OPEN
Blocked Work Unit: <semantic Work Unit name>
Resume Point: <exact Subtask text — must match an existing Subtask>
Blocking Reason: <precise factual reason execution cannot currently continue>
Resolution Condition: <condition that must become true before the blocker is considered resolved>
Resolution Task: <Resolution Task ID or NONE>
```

### Resolution Task

A Resolution Task is an independent Task in `plan/backlog/` that performs work
toward resolving the blocking condition. It must contain:

```markdown
## Resolution Context

Resolves Task: <blocked Task ID>
Resolves Condition: <specific blocking condition this Task addresses>
```

Completion of a Resolution Task does **not** automatically reactivate the blocked Task.
A Resolution Task is unauthorized while in `plan/backlog/`.

### Resolution Transition (OPEN → RESOLVED)

When the Resolution Task completes and the recorded `Resolution Condition` is
independently verified as true, an authorized actor may record:

```markdown
Blocking Condition

Status: RESOLVED
```

and update the blocked-Task index entry to:

```text
Eligibility: ELIGIBLE FOR REACTIVATION
```

Only an authorized actor may record this transition:
- the human controller, or
- an Agent acting only under explicit human instruction.

An Agent must never change `OPEN` to `RESOLVED` by inference.

### Reactivation Authorization

`ELIGIBLE FOR REACTIVATION` does not mean active. Reactivation requires a new
explicit human authorization event recorded in the Task file:

```markdown
## Reactivation Record

Date: <YYYY-MM-DD>
Source: <human instruction / authorization source>
Task: <Task ID>
Authorized Action: Reactivate Task
Authorized Scope: <what the Agent is authorized to do upon reactivation>
Resolution Evidence: <reference to evidence establishing that the blocker is resolved>
```

After a valid Reactivation Record is present:
1. The Task file moves from `plan/blocked/` to `plan/active/`.
2. The `Blocking Condition` shows `Status: RESOLVED`.
3. The Task's `Status:` is updated to `in-progress`.
4. The Task's row is removed from `plan/blocked/INDEX.md`.
5. `CURRENT.md` is updated to reflect the reactivated Task.

The following do **not** authorize reactivation:
- Completion of the Resolution Task.
- `Status: RESOLVED` in the Blocking Condition.
- `ELIGIBLE FOR REACTIVATION` in the blocked index.
- Chronological order of events.
- Prior conversation instructions.
- Absence of another active Task.

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

### No-Active-Task Recovery

A fresh Agent encountering no active Task must determine why:

| Situation | Indicator | Action |
|-----------|-----------|--------|
| Work is blocked | `plan/blocked/INDEX.md` has entries | Read blocked Task's Blocking Condition; surface to human; do not self-activate |
| Previous Task is complete | `plan/active/` is empty; `plan/completed/INDEX.md` has the last Task | Await explicit authorization for a new Task |
| Awaiting authorization | `plan/backlog/` has candidate Tasks | Do not activate; await human instruction |

A fresh Agent must not autonomously select or activate a backlog Task. It must not
infer authorization from the blocked state, chronology, or any repository observation.

---

## Superseded Task Semantics

`superseded` is a terminal status distinct from `complete`.

| Status | Meaning | Reactivatable? |
|--------|---------|----------------|
| `complete` | The Task's intended work was completed. | No |
| `superseded` | The Task was intentionally replaced or made unnecessary by another authorized planning decision. | No |

Both are stored in `plan/completed/`. Both are distinguished by the `Status`
column in `plan/completed/INDEX.md`. Supersession must be explicitly recorded
in the Task file; it must not be inferred.

---

## CURRENT.md Authority

`plan/CURRENT.md` is a **recoverable navigation projection**.

It identifies:
- The currently active Task, when one exists
- The current Work Unit within that Task
- The path to the Task file
- The no-active-Task state and its reason, when no active Task exists
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

### No-Active-Task CURRENT State

When `plan/active/` contains no Task, `CURRENT.md` must explicitly state:
- that no active Task exists,
- which of the following reasons applies:
  - `Work is blocked` — a Task is in `plan/blocked/`.
  - `Awaiting authorization` — planning is awaiting explicit human authorization.
  - `No work in progress` — the previous Task is complete and no successor is authorized.

A no-active-Task CURRENT.md must not imply that a blocked Task is active.

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
12. If that Subtask is `[!]` (blocked), follow §Blocked-Task Lifecycle.
13. Confirm that the selected Work Unit contains unfinished, unblocked work. If all
    Subtasks are `[x]` while the Work Unit is not complete, repair the Work Unit
    instead of executing a duplicate Subtask.
14. Compare the resolved Task/Work Unit/Subtask against CURRENT.md.
15. If they disagree, the **Task file wins**.
16. Repair CURRENT.md if necessary.
17. Continue from the next executable Subtask.

**If `plan/active/` is empty:**

1. Read `plan/blocked/INDEX.md`.
2. If blocked Tasks exist, read each blocked Task's `Blocking Condition` section.
3. Surface the blocking condition to the human.
4. Do not self-activate any Task.
5. Never infer authorization from repository chronology, prior conversation, or
   Resolution Task completion.
6. If no blocked Tasks exist, read `plan/backlog/` for candidate Tasks.
7. Await explicit human authorization before activating any backlog Task.

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
| `active/` is empty; `blocked/` has entries | Read blocked Task(s); surface blocker to human; do not select work. |
| Blocked Task has `Status: RESOLVED` but no Reactivation Record | Task is eligible but not yet reactivated; do not move it to active; await explicit reactivation authorization. |

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
├── CURRENT.md             ← navigation projection; active Task + Work Unit, or no-active-Task state
├── ROADMAP.md             ← long-term strategic direction
├── PRINCIPLES.md          ← governing principles; Runtime authority boundary
├── definitions/
│   ├── TASK.md            ← what a Task is; blocked/superseded status; Blocking Condition structure
│   ├── WORK-UNIT.md       ← what a Work Unit is
│   ├── SUBTASK.md         ← what a Subtask is
│   ├── STATUS.md          ← allowed planning states; blocked vs in-progress; complete vs superseded
│   ├── BLOCKED.md         ← blocked Task lifecycle; Blocking Condition; Resolution Task; reactivation
│   └── COMPLETION.md      ← completion levels and conditions
├── active/
│   └── <task-id>.md       ← active Task files (authoritative state); at most one
├── backlog/
│   └── <task-id>.md       ← candidate future Tasks; unauthorized until explicitly activated
├── blocked/
│   ├── INDEX.md            ← index of blocked Tasks; schema: Task | Blocked Work Unit | Resume Point | Blocking Condition | Resolution Task | Eligibility
│   └── <task-id>.md       ← blocked Task files; Status: blocked; Blocking Condition section required
└── completed/
    ├── INDEX.md            ← index of completed Tasks; Status column distinguishes complete from superseded
    └── <task-id>.md       ← completed/superseded Task files (historical record; permanent)
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
17. A Task-level `blocked` status means the Task is in `plan/blocked/`, not `plan/active/`.
18. A blocked Task remains required unless explicitly superseded by an authorized planning decision.
19. Resolution is not authorization. Completing a Resolution Task does not automatically reactivate the blocked Task.
20. Reactivation requires: (a) verified Resolution Condition, (b) `Status: RESOLVED` recorded by authorized actor, (c) explicit new Reactivation Record with human authorization.
21. `complete` and `superseded` are both terminal statuses; `plan/completed/INDEX.md` distinguishes them by a `Status` column.
22. A blocked Task leaving `plan/blocked/` must have its row removed from `plan/blocked/INDEX.md`.
23. `CURRENT.md` must explicitly state why no active Task exists (blocked / awaiting authorization / no work in progress) when `plan/active/` is empty.
