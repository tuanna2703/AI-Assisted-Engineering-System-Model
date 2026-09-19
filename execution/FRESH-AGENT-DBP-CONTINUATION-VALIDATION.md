# Fresh-Agent DBP Continuation — Validation Artifact

---

## Result

*(To be completed after independent evidence reconstruction.)*

---

## Baseline

### Repositories

| Repository | Path                                                           | Revision                                     | Working Tree |
| ---------- | -------------------------------------------------------------- | -------------------------------------------- | ------------ |
| AESM       | `AI-Assisted-Engineering-System-Model/`                        | `feb369c3c1dac7227b35c140f4de06eac9c0efe3`  | Clean        |
| DBP        | `wp-content/plugins/directories-builder-pro/`                 | `480bd51798a06b78e3065689db72e254e2953036`  | Clean        |

### Environment

| Component   | Value                     |
| ----------- | ------------------------- |
| Platform    | darwin (macOS)            |
| Python      | 3.13.5                    |
| pytest      | 9.1.1                     |
| PYTHONPATH  | `.` (AESM repo root)      |

### AESM Test Suite Baseline

| Command         | Revision  | Tests | Result          |
| --------------- | --------- | ----- | --------------- |
| `PYTHONPATH=. pytest -q` | `feb369c` | 163 | **163 passed** |

---

## Pre-Registered Target

### Original Target — Already Implemented

| Item     | Value                                                      |
| -------- | ---------------------------------------------------------- |
| File     | `modules/reviews/forms/add-review-form.php`               |
| Class    | `Add_Review_Form`                                         |
| Field    | `business_id`                                             |
| Change   | `Fields_Manager::SELECT` → `Fields_Manager::POST_SELECT` |
| Status   | **Already implemented** in DBP commit `deaabeb`           |

The `business_id` field in `Add_Review_Form` currently uses `Fields_Manager::POST_SELECT`
(line 113 of `add-review-form.php`). The original target was not reverted.

### Approved Session Target

| Item     | Value                                                      |
| -------- | ---------------------------------------------------------- |
| File     | `modules/reviews/forms/edit-review-form.php`              |
| Class    | `Edit_Review_Form`                                        |
| Field    | `business_id`                                             |
| Change   | `Fields_Manager::SELECT` → `Fields_Manager::POST_SELECT` with `post_type => 'dbp_business'`, `multiple => false` |
| Status at baseline | `Fields_Manager::SELECT` at line 178            |

*(Human Controller must record approval before Session A.)*

---

## Evidence Contract

### Bridge Participation Observable (Locked Pre-Session)

> **Observable:** `history.jsonl → runtime_id` field present in each event record

> **Rationale:** Every authoritative Runtime operation writes `runtime_id` to `history.jsonl`
> via `ProcessStore`. A `history.jsonl` entry with `runtime_id` present and `at` timestamp
> within the session window demonstrates Agent → Bridge → Runtime → ProcessStore traversal.
> Direct file inspection cannot produce this event.

### Evidence Contract Table (Locked Pre-Session)

| Property              | Observable artifact/field                              |
| --------------------- | ------------------------------------------------------ |
| Same Process Instance | `process.json → process_instance_id`                  |
| Same DBP scope        | `process.json → engineering_scope_identity`           |
| State continuity      | `context.json → process_state` + `version`            |
| Evidence continuity   | `history.jsonl` representative entry from Session A   |
| Version continuity    | `context.json → version` (monotone integer)           |
| Fresh Agent session   | Conversation/session ID or session-specific `runtime_id` |
| Bridge participation  | `history.jsonl → runtime_id` in B-session events      |
| Actual continuation   | New `history.jsonl` entry with `at` > A-terminal `at` |
| Persistence           | `context.json` + `history.jsonl` after B ends         |
| DBP continuity        | DBP repo file + PI scope field                        |
| Project isolation     | `process.json → engineering_scope_identity`           |

---

## Session A

*(Human Controller records after Session A completes.)*

| Value                             | Session-A recorded value |
| --------------------------------- | ------------------------ |
| Process Instance ID               |                          |
| DBP scope identity                |                          |
| Process state at end              |                          |
| Context version at end            |                          |
| Representative history entry      |                          |
| Pending execution state           |                          |
| Session-A identifier              |                          |
| Runtime/execution identifier      |                          |
| Session-A start/end timestamps    |                          |
| DBP repository state after A      |                          |

---

## Session Boundary

*(Human Controller records at boundary.)*

| Field                              | Value |
| ---------------------------------- | ----- |
| Session-A identifier               |       |
| Session-A end timestamp            |       |
| Process Instance ID preserved      |       |
| Artifacts snapshot taken?          |       |
| Bootstrap information supplied     |       |

---

## Session B

*(Human Controller records after Session B completes.)*

| Value                             | Session-B observed value |
| --------------------------------- | ------------------------ |
| Process Instance ID recovered     |                          |
| DBP scope identity recovered      |                          |
| Initial recovered version         |                          |
| Recovered prior evidence visible? |                          |
| Session-B identifier              |                          |
| Runtime/execution identifier      |                          |
| Session-B start/end timestamps    |                          |
| New history entry type            |                          |
| New history entry `at`            |                          |
| New history entry `runtime_id`    |                          |
| Final context version             |                          |
| DBP repository state after B      |                          |

---

## Independent Reconstruction

*(Human Controller reconstructs from preserved artifacts.)*

### Identity
Did Session B recover the same authoritative Process Instance?

*(To be completed from artifacts.)*

### Scope
Did the persisted scope remain the approved DBP scope?

*(To be completed from artifacts.)*

### State
Does Session-B recovery correspond to Session-A final authoritative state/version?

*(To be completed from artifacts.)*

### Evidence
Can Session-A evidence be independently observed after the boundary?

*(To be completed from artifacts.)*

### Freshness
Can Session A and Session B be independently distinguished?

*(To be completed from artifacts.)*

### Bridge
Does the pre-registered observable demonstrate Agent → Bridge → Runtime participation for Session B?

*(To be completed from history.jsonl inspection.)*

### Continuation
Did Session B create a new authoritative state/evidence event?

*(To be completed from artifacts.)*

### Persistence
Did that event survive Session B termination?

*(To be completed from artifacts.)*

### DBP Work
Did Session B perform additional work belonging to the approved target?

*(To be completed from DBP repository state.)*

---

## Classification

| Property              | Required evidence                    | Observed result | Classification |
| --------------------- | ------------------------------------ | --------------- | -------------- |
| Same Process Instance | PI identity comparison               |                 |                |
| Same DBP scope        | Scope identity comparison            |                 |                |
| State continuity      | A final state/version vs B recovery  |                 |                |
| Evidence continuity   | Pre-boundary evidence recovered      |                 |                |
| Version continuity    | Authoritative state/version chain    |                 |                |
| Fresh Agent session   | Independent A/B execution identities |                 |                |
| Bridge participation  | Pre-registered Bridge observable     |                 |                |
| Actual continuation   | New B authoritative event            |                 |                |
| Persistence           | B result persisted                   |                 |                |
| DBP continuity        | Same approved target                 |                 |                |
| Project isolation     | Scope remains DBP                    |                 |                |

Classification values:
- Conformant — Demonstrated
- Conformant — Evidence Incomplete
- Implementation Gap — Semantically Required
- Specification / Applicability Decision Required
- Test / Fixture Defect
- Environment Defect

---

## Limitations

*(What was not demonstrated, and why.)*

*(To be completed after independent reconstruction.)*

---

## Final Gate

*(To be completed after independent reconstruction.)*

The following mandatory rows must all be **Conformant — Demonstrated** for the overall
success gate to be demonstrated:

1. Same Process Instance
2. Same DBP scope
3. State continuity
4. Evidence continuity
5. Fresh Agent session
6. Bridge participation
7. Actual continuation
8. Persistence
9. DBP continuity

**Overall Fresh-Agent DBP Continuation gate:** *(not yet determined)*

---

## Next Authorized Work

*(Only evidence-supported next work, to be completed after the gate determination.)*

