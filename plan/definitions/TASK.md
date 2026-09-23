# Task

## Definition

A **Task** is a bounded engineering objective that constitutes a meaningful,
independently completable unit of work within the AESM planning system.

A Task is the top-level unit in the planning hierarchy:

```text
Task
  └── Work Unit
        └── Subtask
```

## Required Properties

Every Task file must define:

### Identity

```text
Task ID:       unique slug, e.g. runtime-consistency-hardening
Status:        one of the allowed planning states (see STATUS.md)
Created:       ISO 8601 date
Source:        mechanically sufficient authorization record (see §Authorization)
```

### Objective

A concise statement of what completing this Task achieves.
Must be specific enough that completion can be determined objectively.

### Context

Background information required to understand why the Task exists.
Include the engineering condition that made the Task necessary.

### Governing Constraints

Rules that must not be violated during execution of this Task.
Each constraint must be specific enough to test: a future Agent must be able to
determine whether a proposed action violates a constraint.

### Dependencies

Other Tasks or engineering artifacts that must be complete or available before
this Task can be fully executed. State explicitly "None" if there are no
dependencies.

### Governing Decisions

Prior decisions that were reviewed and determined to constrain this Task.

Each entry must identify:
- Source Task ID
- Decision summary
- Why the decision applies to this Task
- **Relationship** (if applicable): `qualified` or `superseded` — see §Decision Lifecycle

Only applicable decisions belong here. This section is a bounded traceability
record, not a duplicate of the entire completed-task history.

If a prior decision is intentionally changed, record the supersession explicitly,
including the superseded Source Task ID, the relationship (`superseded`), the new
decision, and why the change was made.

### Decisions Still in Effect

Decisions made during prior Tasks that remain active constraints during execution
of this Task.

A decision belongs here if: *violating it during future work would constitute an error.*

A decision is historical only if it describes a past condition and violating it
is no longer meaningful under the current system.

### Work Units

A list of all Work Units in this Task, in execution order, each with:
- Name
- Status
- Objective (one sentence)
- Subtasks
- Completion condition

Work Unit names must be the same names used in the Task's authoritative prompt or
source document. Do not rename Work Units opportunistically.

### Acceptance Criteria

Observable outcomes that must be satisfied for this Task to be considered complete.

### Blocking Condition (required for blocked Tasks)

When a Task's `Status:` is `blocked`, the Task file must contain a `Blocking
Condition` section immediately after the `Identity` section:

```markdown
## Blocking Condition

Status: OPEN
Blocked Work Unit: <semantic Work Unit name>
Resume Point: <exact Subtask text — must match an existing Subtask>
Blocking Reason: <precise factual reason execution cannot currently continue>
Resolution Condition: <condition that must become true before the blocker is considered resolved>
Resolution Task: <Resolution Task ID or NONE>
```

`Status` may be `OPEN` or `RESOLVED`. An Agent must never change `OPEN` to
`RESOLVED` by inference. Only an authorized actor may record the transition.

See `plan/definitions/BLOCKED.md` for the full definition.

### Reactivation Record (required when a blocked Task is reactivated)

When a blocked Task receives an explicit reactivation authorization, the Task
file must record:

```markdown
## Reactivation Record

Date: <YYYY-MM-DD>
Source: <human instruction / authorization source>
Task: <Task ID>
Authorized Action: Reactivate Task
Authorized Scope: <what the Agent is authorized to do upon reactivation>
Resolution Evidence: <reference to evidence establishing that the blocker is resolved>
```

A Reactivation Record is a new authorization event. It does not overwrite the
original `Source:` authorization.

---

## Terminal Statuses: `complete` and `superseded`

Both `complete` and `superseded` are terminal statuses. Both result in the Task
being stored in `plan/completed/`.

- `complete` — the Task's intended work was completed.
- `superseded` — the Task was intentionally replaced or made unnecessary by
  another authorized planning decision.

Supersession must be explicitly recorded in the Task file and in
`plan/completed/INDEX.md`. It must not be inferred from omission, logical sequence,
or another Task's completion.

Neither terminal status may be reactivated as if it were merely blocked.

## Authorization

### Mechanically Sufficient Authorization Record

The `Source:` field of an active Task must contain a mechanically sufficient
authorization record. A fresh Agent must be able to determine authorization from
this field alone — without relying on conversation history, inferred context, or
other documents.

A mechanically sufficient record identifies all four of the following:

1. **Authorization date** — when the authorization was given.
2. **Nature/source of the instruction** — who or what authorized the Task (e.g.,
   human instruction, authorized engineering prompt, explicit approval).
3. **Authorized Task identity** — the Task being authorized, by name or ID.
4. **Authorized action or scope** — what the Agent is authorized to do.

Example of a sufficient record:

```
Source:
  Authorization date: 2026-09-22
  Authorized by: Human instruction (engineering prompt provided directly)
  Authorized Task: planning-verification-time-boundary-correction
  Authorized scope: Correct the historical verification record temporal boundary
    in plan/completed/aesm-planning-authorization-refinement.md; no DBP or
    Runtime changes.
```

An abbreviated form is acceptable when an existing human instruction can be
traced clearly without invented details.

### Authorization Provenance, Task Provenance, and Execution Evidence

These three are distinct and must not appear under the same `Source:` entry
without clear labeling:

**Authorization provenance** — the human instruction granting execution authority.

**Task provenance** — what motivated the Task's creation (prior decisions, context,
investigation).

**Execution evidence** — what happened during execution (commands, results, tests,
blockers).

### Invalid Authorization

A Task is not authorized when the Agent would have to infer authorization from:

- Task location in `plan/backlog/` or `plan/active/`;
- CURRENT.md content;
- prior conversation history alone;
- logical sequence or apparent necessity;
- another Task's completion or suggestion;
- an ambiguous, missing, or fabricated `Source:` field.

The Entry Consistency Assertion in `plan/README.md §Entry Consistency Assertion`
stops execution when authorization is insufficient.

### Compatibility with Existing Tasks

Existing Tasks authorized before the structured authorization format was established
may retain their historical `Source:` text. This is a compatibility rule:

- Preserve historical Source text exactly.
- Do not invent missing details.
- If the existing Source identifies a genuine human authorization instruction, the
  Task may continue without retroactive reformatting.
- Apply the full structured format to newly created Tasks.

---

## Decision Lifecycle

A decision recorded in a completed Task's `Decisions Still in Effect` section
remains a binding constraint for future Tasks unless explicitly superseded or
qualified.

### Qualified

An earlier decision remains applicable, but its scope, interpretation, conditions,
or applicability has been narrowed or otherwise changed.

A qualification must record:
- Prior Task ID and decision summary
- Relationship: `qualified`
- What remains applicable
- What changed
- Why the qualification was made

### Superseded

An earlier decision no longer governs the relevant situation because a later
decision replaces it.

A supersession must record:
- Prior Task ID and decision summary
- Relationship: `superseded`
- The new decision
- Why the supersession was made

### Discoverability

Decision qualifications and supersessions must be exposed in `plan/completed/INDEX.md`
so a fresh Agent can discover them without reading every completed Task file.

Historical Task records remain historically accurate. A later qualification or
supersession does not rewrite the earlier Task's content.
