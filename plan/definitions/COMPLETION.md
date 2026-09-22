# Completion

## Overview

This document defines the four distinct levels of completion in the `plan/`
system and the specific conditions required for each.

These are not equivalent. Satisfy each level's requirements before advancing
to the next level.

---

## Subtask Completion

A Subtask is complete when:

1. The concrete action described by the Subtask has been executed.
2. The result exists in the repository, test output, or a referenced artifact
   — not solely in Agent memory or conversation history.
3. The Task file records the Subtask as `[x]` with an independently checkable
   evidence reference.

**An Agent claim is not Subtask completion.**

If no persistent evidence exists after the action, record that explicitly as a
finding or block the Subtask rather than marking it complete without evidence.

---

## Work Unit Completion

A Work Unit is complete when:

1. **All Subtasks are marked `[x]` in the Task file.**
2. **The Work Unit's Completion Condition is satisfied** — verifiable from the
   repository or referenced artifacts, independently of Agent claim.
3. **Required planning evidence is recorded** in the Task file.
4. **The Task file records the Work Unit status as `complete`.**
5. **Navigation projection is reconciled:** `CURRENT.md` is updated to reflect
   the current Work Unit, OR explicit evidence states that no projection change
   is required (e.g., this is the last Work Unit in the Task).

Only after step 4 and step 5 may CURRENT.md be considered authoritative for the
new navigation state.

**Never advance CURRENT.md before the Task file records Work Unit completion.**

If all Subtasks are `[x]` but the Completion Condition or evidence is not verified,
the Work Unit is not complete. The state must be repaired before execution advances.

---

## Task Completion

A Task is complete when:

1. **All Work Units are `complete`** per the Task file.
2. **All acceptance criteria are satisfied** — observable from repository state,
   not from Task-file checkboxes alone.
3. **Required verification is complete** — verification must be independent of
   Agent claim. It must reference executable test results, repository state,
   or other persisted evidence.
4. **Completion evidence is recorded** in the Task file's Completion Record.
5. **The Completion Record is populated with the actual verification result.**
6. **The Task file status is updated to `complete`.**
7. **The Task file is moved to `plan/completed/`.**
8. **`plan/completed/INDEX.md` is updated** with the Task entry.

A Task with all Work Units marked `complete` but without a complete and supported
Completion Record remains `in-progress`. This is a verification-pending condition
within the existing status model; it is not a new status.

---

## Engineering Completion

**Planning completion does not itself constitute AESM engineering completion.**

This statement is a governing principle of the `plan/` system.

A Task in `plan/completed/` means:

> The planning system records that the intended engineering work was performed
> and that planning-level acceptance criteria were satisfied.

It does **not** mean:

> The AESM Runtime has recognized the corresponding engineering results as
> authoritative evidence of Process Instance completion or state transition.

Engineering completion under AESM requires:

- Authoritative Process Instance / Execution Context state recognized by Runtime.
- Runtime-mediated evidence recording, state mutation, and verification.
- Persisted history under `.aesm/` reflecting the recognized completion.

A completed Task file is a **planning record**. A planning record is not a
substitute for AESM-governed engineering completion.

---

## Distinction Table

| Level | Satisfied by | Not satisfied by |
|-------|-------------|-----------------|
| Subtask | Action performed; independently checkable evidence recorded | Agent statement; checkbox alone |
| Work Unit | All Subtasks `[x]`; Completion Condition met; evidence recorded; Task file updated; navigation projection reconciled | Subtasks checked without verification; CURRENT.md advanced prematurely; projection not reconciled |
| Task | All Work Units complete; criteria met; verification complete; Completion Record populated; Task moved to completed/ | Work Units checked alone; unsupported Completion Record; missing verification |
| Engineering | Runtime-mediated recognition; persisted `.aesm/` state | Plan completion; checkbox state; Agent claim; planning evidence alone |
