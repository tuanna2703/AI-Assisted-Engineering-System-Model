# Planning Principles

These principles govern the `plan/` planning system and its relationship to
AESM engineering execution. They are governing constraints, not suggestions.

Violating any of these principles during future work constitutes an error.

---

## 1. Runtime Authority

The AESM Runtime remains the sole authoritative source for persisted
engineering state.

Authoritative state is:
- `.aesm/<pi-id>/process.json` — Process Instance identity and lifecycle state
- `.aesm/<pi-id>/context.json` — Execution Context; the authoritative operational state
- `.aesm/<pi-id>/history.jsonl` — persisted mutation history

No planning file, checkbox, task-file status, or Agent claim substitutes for
or supersedes Runtime-owned state.

An Agent must not directly edit authoritative state files. Use Runtime-mediated
operations (bridge, dispatch) for authoritative state mutations.

---

## 2. Planning Records

A checkbox, status value, task-file statement, or planning-system entry is a
**planning record**.

A planning record is not:
- AESM Runtime evidence
- proof of engineering execution
- an authoritative Process Instance state transition
- a substitute for Runtime-recognized verification

A planning record answers: *"What did the planning system record about intent
and planning-level completion?"*

A Runtime record answers: *"What did the AESM Runtime recognize as authoritative
engineering state?"*

These are different questions with different answers.

---

## 3. Planning Versus Execution

The planning system governs intended engineering work.

AESM governs engineering execution and authoritative evidence.

```text
plan/                        →  planning intent and governance
docs/                        →  AESM semantic authority
runtime/ + bridge/           →  AESM implementation
.aesm/                       →  authoritative persisted process state
tests/                       →  executable verification and evidence
implementation/              →  durable engineering records (not plan, not state)
```

The planning system must not duplicate, override, or substitute for any of
the above surfaces.

---

## 4. No Implicit Scope

The planning system does not authorize an Agent to infer:
- engineering project scope
- Process Instance scope
- applicable EPM
- repository scope
- Execution Environment scope

Scope is resolved through the AESM scope-resolution mechanism (Runtime-owned),
not through reading a plan file.

A plan file may reference a scope that was established elsewhere, but the plan
file is not the authority for that scope.

---

## 5. No Premature Generalization

Do not introduce planning infrastructure, new directories, new definition types,
or new status values merely because they might eventually be useful.

The planning system must grow only from demonstrated need. A desirable
improvement that is not required for the current task must be recorded as a
backlog item rather than implemented opportunistically.

This principle prevents scope creep within the planning system itself.

---

## 6. Evidence Before Engineering Completion

A Task is not engineering-complete merely because:
- all planning Subtasks are marked `[x]`
- the Task file status is `complete`
- the Task appears in `plan/completed/`

Engineering completion under AESM requires:
- Runtime-mediated recognition of the engineering result
- authoritative Process Instance state transition
- persisted history reflecting the recognized completion

See `plan/definitions/COMPLETION.md` for the precise four-level completion
hierarchy.

---

## 7. One Planning Authority

There must be exactly one active planning authority.

Do not allow two competing planning systems to coexist without an explicit
authority rule.

`IMPLEMENTATION_PLAN.md` is the legacy planning document. It is superseded by
`plan/`. During the transition, `IMPLEMENTATION_PLAN.md` carries an explicit
supersession notice. After migration is verified, it is removed.

Do not create additional top-level planning files that compete with `plan/CURRENT.md`.

---

## 8. Semantic Names, Not Numeric Labels

Work Unit names and Task identities must use semantic names, not numeric phase
labels such as "Phase 1", "Phase 2", "Step 3".

Semantic names make navigation durable across changes in ordering, scope, and
history.

---

## 9. Task File Is the Source of Truth

The Task file in `plan/active/<task-id>.md` is the authoritative record of Task state.

`CURRENT.md` is a recoverable navigation projection derived from the Task file.

If they conflict, **the Task file wins**.

This principle applies even if CURRENT.md was updated more recently.

---

## 10. Completed Tasks Are Permanent Records

A completed Task file is never deleted from `plan/completed/`.

It is the historical record of what was decided, what was verified, and what
decisions remain in effect for future work.

Decisions recorded under "Decisions Still in Effect" in a completed Task file
are active constraints that govern future Tasks unless explicitly superseded
by a later authoritative decision.
