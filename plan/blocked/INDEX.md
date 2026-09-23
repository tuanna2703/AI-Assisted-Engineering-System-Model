# Blocked Tasks

This index lists all Tasks currently in `plan/blocked/`. It is a navigation
projection derived from the authoritative Task files. If this index disagrees
with a Task file, the **Task file wins**.

A Task appears here when it has been explicitly placed in the blocked lifecycle:
- It has `Status: blocked` in its Task file.
- It has a `Blocking Condition` section.
- It cannot resume without an explicit reactivation authorization.

A Task is removed from this index when:
- It is reactivated (moved to `plan/active/`), or
- It is superseded (moved to `plan/completed/`).

See `plan/definitions/BLOCKED.md` for the full blocked-Task lifecycle definition.

---

## Index

| Task | Blocked Work Unit | Resume Point | Blocking Condition | Resolution Task | Eligibility |
|------|-------------------|--------------|--------------------|-----------------|-------------|
| repository-scoped-dbp-continuation-validation | Session A — DBP Process Establishment | Establish the active repository context from the controlled DBP repository checkout without relying on conversation history. | The available execution surface provides repository inspection and Git operations but does not provide a live DBP checkout/runtime process in which the AESM Runtime can be invoked. A fresh Session A requires a real DBP checkout environment with Runtime execution capability. The existing Process Instance (`d0640ec8-672e-43bd-bd4b-974d808915a2`) must be deterministically resolved through the Runtime; its existing state must not be manually edited. | resolve-dbp-active-process-instance-disposition | BLOCKED |

---

## Eligibility Values

| Value | Meaning |
|-------|---------|
| `BLOCKED` | The Task remains blocked; the blocker has not been verified as resolved. |
| `ELIGIBLE FOR REACTIVATION` | The recorded blocker has been verified as resolved by an authorized actor; the Task may be considered for explicit reactivation authorization. Does not mean active. |

`ELIGIBLE FOR REACTIVATION` does not authorize execution. A Task enters
`plan/active/` only after an explicit reactivation authorization event is
recorded in the Task file. See `plan/definitions/BLOCKED.md §Reactivation Authorization`.
