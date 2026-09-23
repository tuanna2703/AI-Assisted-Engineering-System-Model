# Blocked Task

## Overview

A **blocked Task** is a Task whose execution cannot legitimately continue because
a specific, recorded condition prevents progress. A blocked Task is not complete,
not superseded, and not abandoned. It remains a required planning item unless
explicitly superseded by an authorized planning decision.

A Task-level `blocked` status is distinct from:
- a **blocked Work Unit** (`Blocked condition:` section within a Work Unit)
- a **blocked Subtask** (`[!]` marker within a Work Unit)

All three blocking representations may coexist. A Task-level `blocked` status
captures the fact that the Task as a whole cannot advance and has been durably
removed from the active execution position.

---

## When a Task Becomes Blocked

A Task becomes `blocked` (Task-level status) when:

1. Its current Work Unit is blocked and no other Work Unit in the Task is
   eligible for execution.
2. The blocking condition requires external resolution that is outside the
   Task's own authorized scope.
3. The human controller explicitly records the Task as blocked (for example, by
   authorizing this planning migration).

A blocked Task must be moved to `plan/blocked/` and removed from `plan/active/`.

**A blocked Task is not an active Task.**
At most one Task may reside in `plan/active/`. A blocked Task in `plan/blocked/`
does not occupy the active slot. Multiple Tasks may be blocked simultaneously.

---

## Task-Level Blocked Status

```text
Status:
blocked
```

This is a distinct status value, different from `in-progress`, `complete`, and
`superseded`. It is not simply `in-progress` with a note. It means:

- The Task has been explicitly placed in the blocked lifecycle.
- The Task file is located in `plan/blocked/`.
- The Task's `Blocking Condition` section records the authoritative blocker.
- The Task may not be resumed without a separate explicit reactivation authorization.

---

## Required Blocking Condition Section

Every blocked Task file must contain a `Blocking Condition` section immediately
after the `Identity` section:

```markdown
## Blocking Condition

Status: OPEN
Blocked Work Unit: <semantic Work Unit name>
Resume Point: <exact Subtask text or Subtask identifier — must match an existing Subtask>
Blocking Reason: <precise factual reason execution cannot currently continue>
Resolution Condition: <condition that must become true before the blocker is considered resolved>
Resolution Task: <Task ID of the Resolution Task, or NONE>
```

### Field Rules

**Status:** Either `OPEN` or `RESOLVED`. An Agent must never change `OPEN` to
`RESOLVED` by inference. Only an authorized actor may record this transition
(see §Resolution Transition below).

**Blocked Work Unit:** The exact semantic name of the Work Unit in which
execution is blocked. Must match the Work Unit name in the Task file.

**Resume Point:** The exact text of the Subtask at which execution must resume.
Must identify an existing Subtask in the blocked Work Unit. Vague descriptions
such as "continue implementation" are not permitted.

**Blocking Reason:** A precise factual statement of why execution cannot
continue. Must not be vague (e.g., "needs more work"). Must describe the
specific missing condition, resource, or authority.

**Resolution Condition:** The observable condition that must become true before
the blocker can be considered resolved. Must be independently verifiable without
relying on conversation history.

**Resolution Task:** The Task ID of the Resolution Task that performs work
toward resolving the blocker, or `NONE` if no separate Resolution Task exists.

---

## Resolution Task

A **Resolution Task** is an independent Task whose objective is to perform work
toward resolving the blocking condition of one or more blocked Tasks.

A Resolution Task is always a distinct Task. It does not become the blocked Task.
It does not authorize reactivation of the blocked Task upon its completion.
Completing a Resolution Task does not automatically change any other Task's
Blocking Condition status.

### Resolution Context Section

Every Resolution Task must contain a `Resolution Context` section:

```markdown
## Resolution Context

Resolves Task: <Task ID of the blocked Task>
Resolves Condition: <the specific blocking condition this Task addresses>
```

Multiple blocked Tasks may reference the same Resolution Task. In that case,
the Resolution Task's `Resolution Context` must identify all blocked Tasks and
their respective blocking conditions.

A Resolution Task must not silently replace the blocked Task. Its completion
is an engineering result, not a planning reactivation.

A Resolution Task in `plan/backlog/` is **unauthorized** and may not be executed
until explicitly activated by human authorization.

---

## Resolution Transition

When a Resolution Task completes and the blocked Task's recorded `Resolution
Condition` has been independently verified as true, an authorized actor may
record the transition:

```markdown
## Blocking Condition

Status: RESOLVED
```

This transition must also update the blocked-Task index entry:

```text
Eligibility: ELIGIBLE FOR REACTIVATION
```

### Who May Record the Transition

- The **human controller**, or
- An **Agent acting only under explicit human instruction** that authorizes
  recording the verified resolution.

An Agent must not infer resolution solely from:
- Chronological order of events.
- Apparent completion of a referenced Resolution Task.
- Conversation history or prior session output.
- The `ELIGIBLE FOR REACTIVATION` flag alone.
- The `Status: RESOLVED` field alone.

**Resolution is not authorization.**

---

## Eligibility for Reactivation

After `Status: RESOLVED` is recorded and the index entry updated to
`ELIGIBLE FOR REACTIVATION`, the blocked Task is **eligible for reactivation**.
It is still in `plan/blocked/`. It is not yet active. It may not be executed.

`ELIGIBLE FOR REACTIVATION` means:
- The recorded blocking condition has been verified as resolved.
- The Task may be considered for reactivation authorization.

`ELIGIBLE FOR REACTIVATION` does not mean:
- The Task is active.
- The Task may be moved to `plan/active/` without further action.
- An Agent may resume execution.

---

## Reactivation Authorization

Reactivation of a blocked Task requires a new, separate, explicit human
authorization event. This event is distinct from the original Task authorization.

The authorization must be recorded in the Task file as a `Reactivation Record`:

```markdown
## Reactivation Record

Date: <YYYY-MM-DD>
Source: <human instruction / authorization source>
Task: <Task ID>
Authorized Action: Reactivate Task
Authorized Scope: <what the Agent is authorized to do upon reactivation>
Resolution Evidence: <reference to evidence establishing that the blocker is resolved>
```

### After Authorization

Once a valid Reactivation Record is present:

1. The Task file is moved from `plan/blocked/` to `plan/active/`.
2. The Task's `Blocking Condition` section must show `Status: RESOLVED`.
3. The Task's `Status:` field is updated from `blocked` to `in-progress`.
4. The Task's row is removed from `plan/blocked/INDEX.md`.
5. `CURRENT.md` is updated to reflect the reactivated Task.

### What Does Not Constitute Reactivation Authorization

The following do not authorize reactivation, individually or combined:

- Completion of the Resolution Task.
- `Status: RESOLVED` in the Blocking Condition.
- `ELIGIBLE FOR REACTIVATION` in the blocked index.
- Chronological order of events.
- Prior conversation instructions.
- An Agent deciding reactivation is logically appropriate.
- The absence of another active Task.

---

## Superseded Task (Terminal Status)

A blocked Task may be **superseded** rather than reactivated if another
authorized planning decision makes the original Task no longer required.

`superseded` is a terminal status, distinct from `complete`.

| Status | Meaning |
|--------|---------|
| `complete` | The Task's intended work was completed. |
| `superseded` | The Task was intentionally replaced or made unnecessary by another authorized planning decision. |

Both are terminal statuses. Both are stored under `plan/completed/`.
Neither may be reactivated as though it were merely blocked.
Supersession must be explicitly recorded; it must not be inferred.

When a blocked Task is superseded:
1. Its `Status:` is changed to `superseded`.
2. It is moved to `plan/completed/`.
3. Its row is removed from `plan/blocked/INDEX.md`.
4. `plan/completed/INDEX.md` is updated with `Status: superseded`.
5. The superseding decision is recorded in the Task file.

---

## Storage Location Rules

| Task State | Location |
|------------|----------|
| Unauthorized candidate | `plan/backlog/` |
| Actively executing | `plan/active/` |
| Blocked (required, not terminal) | `plan/blocked/` |
| Complete (terminal) | `plan/completed/` |
| Superseded (terminal) | `plan/completed/` |

A blocked Task must not remain in `plan/active/`. A blocked Task in
`plan/blocked/` must have a corresponding entry in `plan/blocked/INDEX.md`.

---

## Blocked-Task Recovery Protocol

A fresh Agent encountering a repository with no active Task must:

1. Inspect `CURRENT.md`.
2. If `CURRENT.md` shows no active Task, determine why:
   - Is there a Task in `plan/blocked/`? → Read `plan/blocked/INDEX.md`.
   - Is the previous Task `complete`? → Read `plan/completed/INDEX.md`.
   - Is the planning system awaiting authorization? → Read `plan/backlog/`.
3. Inspect the relevant blocked Task's `Blocking Condition` section.
4. Inspect referenced Resolution Tasks (if any) from `plan/backlog/`.
5. **Never infer authorization** from repository chronology, Task completion,
   or conversation history.
6. Surface unresolved blockers to the human and stop.
7. Do not select work from `plan/backlog/` without explicit human authorization.
