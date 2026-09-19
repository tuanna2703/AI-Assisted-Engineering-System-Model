# Fresh-Agent DBP Continuation — Human Controller Workbook

This is the contemporaneous experiment-control record.
It is populated by the Human Controller, not generated retrospectively by Session B.

---

## Experiment Identity

| Field                   | Value                                                          |
| ----------------------- | -------------------------------------------------------------- |
| Experiment              | Fresh-Agent DBP Continuation                                   |
| Controller              | *(Human Controller — to be recorded)*                         |
| Date/time started       | *(to be recorded before Session A begins)*                     |
| AESM revision           | `feb369c3c1dac7227b35c140f4de06eac9c0efe3` (main)             |
| DBP revision            | `480bd51798a06b78e3065689db72e254e2953036` (main)             |
| AESM working-tree state | **Clean** — no uncommitted modifications confirmed at setup    |
| DBP working-tree state  | **Clean** — no uncommitted modifications confirmed at setup    |

---

## Pre-Session Gate Closure Record

This section is the execution gate for the current work unit. It is intentionally
recorded before Session A and does not authorize Session A unless every mandatory
gate is explicitly satisfied.

### Gate A — Authorized Target

| Field | Required record |
| ----- | --------------- |
| Approved target | `modules/reviews/forms/edit-review-form.php` / `Edit_Review_Form` / `business_id` |
| Approved change | `Fields_Manager::SELECT` → `Fields_Manager::POST_SELECT`, with `post_type => 'dbp_business'`, `multiple => false` |
| Human approval | *(record Yes/No)* |
| Approval timestamp | *(record exact timestamp)* |
| Controller identity | *(record)* |

**Gate rule:** Session A is blocked unless Human approval is explicitly recorded as
**Yes** with a timestamp.

### Gate B — Separate Agent Session Capability

| Check | Required evidence | Result |
| ----- | ----------------- | ------ |
| Separate Agent session can be started | Fresh-session launch demonstrated | *(record Pass/Fail)* |
| Session identity is independently distinguishable | Conversation/session identifier or equivalent | *(record)* |
| Session A context can be ended without reusing the Agent conversation | Controller observation | *(record Pass/Fail)* |

**Gate rule:** A failure is **Environment Defect** and stops the experiment.

### Gate C — ProcessStore Boundary Persistence

| Check | Required evidence | Result |
| ----- | ----------------- | ------ |
| ProcessStore root is filesystem-persistent across Agent sessions | Controller verifies the same persistence location is available to both sessions | *(record Pass/Fail)* |
| A Process Instance can be written before the boundary | Authoritative `process.json`, `context.json`, `history.jsonl` exist | *(record Pass/Fail)* |
| The persisted Process Instance can be read after the boundary | Independent post-boundary read/recovery | *(record Pass/Fail)* |
| No transcript or copied Execution Context is required for persistence | Controller observation | *(record Pass/Fail)* |

**Gate rule:** A failure is **Environment Defect** and stops the experiment.

### Gate Closure Decision

| Gate | Status | Evidence reference | Closed? |
| ---- | ------ | ------------------ | ------- |
| Authorized target | *(Pending)* | *(record)* | *(Yes/No)* |
| Separate Agent session | *(Pending)* | *(record)* | *(Yes/No)* |
| ProcessStore persistence across boundary | *(Pending)* | *(record)* | *(Yes/No)* |

**Session-A authorization:** *(BLOCKED until all three gates are Yes.)*

> The Human Controller must complete this section from direct observation. The Agent
> must not claim that an environment capability has passed merely because repository
> code or documentation suggests that the capability exists.

---

## Pre-Session Target Approval

### Target Determination

The originally specified target —
`modules/reviews/forms/add-review-form.php` / `Add_Review_Form` / `business_id` /
`Fields_Manager::SELECT` → `Fields_Manager::POST_SELECT` — is **already implemented**
in DBP commit `deaabeb` ("replace business select field with post select and update
business ID lookup logic"). The current file at line 113 uses `Fields_Manager::POST_SELECT`.

Per Section 9 of the experiment protocol: the Human Controller must select the smallest
suitable currently pending DBP change. Do not revert the existing implementation.

### Candidate Target Selected by Pre-Experiment Inspection

| Field                      | Value                                                                              |
| -------------------------- | ---------------------------------------------------------------------------------- |
| DBP engineering target     | Replace `Fields_Manager::SELECT` with `Fields_Manager::POST_SELECT` for the `business_id` field in `Edit_Review_Form` |
| Target file(s)             | `modules/reviews/forms/edit-review-form.php`                                       |
| Class                      | `Edit_Review_Form`                                                                 |
| Field name                 | `business_id`                                                                      |
| Requirement/behavior       | `business_id` in `Edit_Review_Form::register_fields()` currently uses `Fields_Manager::SELECT` (line 178). It must be changed to `Fields_Manager::POST_SELECT` with `post_type => 'dbp_business'` and `multiple => false`, consistent with the already-implemented change in `Add_Review_Form`. The `save()` method's business ID lookup logic should also be inspected for consistency. |
| Why target is suitable     | Smallest currently pending DBP change; directly parallel to the already-implemented add-form fix; single file; mechanically clear; no new infrastructure required |
| Approved before Session A? | *(Human Controller must record Yes/No before Session A begins)*                    |
| Approval timestamp         | *(Human Controller records timestamp of approval)*                                 |

> **BLOCKING GATE:** Session A must NOT start until the Human Controller records
> "Approved before Session A? Yes" and the approval timestamp above.

---

## Environment Baseline

| Capability                                            | Status | Notes                                                               |
| ----------------------------------------------------- | ------ | ------------------------------------------------------------------- |
| AESM repository accessible                            | VERIFY | `/AI-Assisted-Engineering-System-Model` — HEAD `feb369c` confirmed  |
| DBP repository accessible                             | VERIFY | `/wp-content/plugins/directories-builder-pro` — HEAD `480bd51` confirmed |
| Python/runtime available                              | VERIFY | Python 3.13.5 — `.venv/` present in AESM root                      |
| AESM ProcessStore accessible                          | VERIFY | `ProcessStore` at `runtime/core/store.py`; path is a constructor param |
| Established Bridge available                          | VERIFY | `AgentRuntimeBridge` at `bridge/agent_runtime_bridge.py`           |
| Established Runtime available                         | VERIFY | `Runtime` at `runtime/core/runtime.py`                              |
| Ability to start separate Agent session               | *(Human Controller must verify)*                                     |
| Ability to preserve persistence across session boundary | *(Human Controller must verify — ProcessStore root must be filesystem-persistent)* |

If a required capability is absent, classify as **Environment Defect** and stop.

---

## AESM Regression Baseline

| Field            | Value                                          |
| ---------------- | ---------------------------------------------- |
| Command          | `PYTHONPATH=. pytest -q`                       |
| Exact revision   | `feb369c3c1dac7227b35c140f4de06eac9c0efe3`    |
| Test count       | 163                                            |
| Pass/fail result | **163 passed**                                 |
| Failures/errors  | None                                           |
| Platform         | darwin (macOS) / Python 3.13.5 / pytest 9.1.1 |

Baseline established at setup: `2026-09-19T03:48:44Z`.

---

## Pre-Registered Evidence Contract

### Evidence Mechanism Inspection (Current Implementation)

Inspected against AESM revision `feb369c`.

#### Authoritative PI Identity
- **Field:** `process_instance_id` in `process.json`
- **Path:** `{store_root}/process-instance/{pid}/process.json`
- **Type:** UUID string (`uuid4()`)

#### Scope Identity
- **Fields:** `engineering_scope_identity` (string or null), `engineering_scope_resolution` (`RESOLVED`/`UNRESOLVED`/…) in `process.json`

#### Execution Context Representation
- **File:** `{store_root}/process-instance/{pid}/context.json`
- **Key fields:** `process_instance_id`, `process_state`, `version`, `evidence`, `engineering_decisions`, `artifacts`, `verification`, `pending_execution`

#### Version/State Representation
- **Field:** `version` (integer, incremented by `save_context()`) in `context.json`
- **Field:** `process_state` (string: `initial`/`investigation`/`implementation`/`verification`/`engineering_complete`) in `context.json`

#### History/Evidence Representation
- **File:** `{store_root}/process-instance/{pid}/history.jsonl`
- **Format:** JSON Lines; each line is a JSON object with `type`, `runtime_id`, `version` (context events), `at` (ISO timestamp)

#### Bridge Invocation Evidence
- **Every authoritative Runtime operation** writes to `history.jsonl` via `ProcessStore.save_context()` or `save_process_instance()`, embedding `runtime_id` in the event payload
- **Bridge constructs Runtime with:** `Runtime(store, runtime_id)` — `AgentRuntimeBridge.__init__` line 116
- **Default `runtime_id`:** `"bridge"`

#### Runtime Identity
- **Field:** `runtime_id` embedded in every `history.jsonl` event

### Bridge Participation Observable

> **Bridge participation observable:** `history.jsonl → runtime_id` field present in each event record

> **Why this demonstrates Bridge traversal:** Every authoritative Runtime operation writes `runtime_id` to `history.jsonl` via `ProcessStore`. A history entry with `runtime_id` present and `at` timestamp within the session window is operational evidence of Agent → Bridge → Runtime → ProcessStore traversal. Direct file inspection cannot produce this event.

> **Session distinguishability note:** The default `runtime_id` is `"bridge"`. To make Sessions A and B distinguishable at the `runtime_id` level, each session should supply a session-specific `runtime_id` when constructing `AgentRuntimeBridge` (e.g. `runtime_id="session-a"` / `runtime_id="session-b"`). If not done, session distinction relies on event timestamp alone.

**This observable is locked. It must not be redefined after observing Session-B results.**

### Locked Evidence Contract Table

| Property              | Required evidence                               | Observable artifact/field                                  | Session-A baseline value | Session-B required value/result              | Independent check   |
| --------------------- | ----------------------------------------------- | ---------------------------------------------------------- | ------------------------ | -------------------------------------------- | ------------------- |
| Same Process Instance | Same authoritative PI                           | `process.json → process_instance_id`                      | Record after A           | Must match A                                 | Controller compares |
| Same DBP scope        | Same authoritative scope                        | `process.json → engineering_scope_identity`               | Record after A           | Must match A                                 | Controller compares |
| State continuity      | B starts from A persisted state                 | `context.json → process_state` + `version`                | Record after A           | Must match A-terminal state/version          | Controller compares |
| Evidence continuity   | Pre-boundary evidence recoverable               | `history.jsonl` — representative entry type+at from A     | Record representative    | Must be observable in B's recovered history  | Controller verifies |
| Version continuity    | Persisted version/state chain                   | `context.json → version` (integer, monotone)              | Record after A           | Must be >= A-terminal version; chain intact  | Controller compares |
| Fresh Agent session   | Distinguishable execution/session identity      | Conversation ID or session-specific `runtime_id` in history | Record A session ID    | Must be independently distinct from A        | Controller verifies |
| Bridge participation  | Agent → Bridge → Runtime observable             | `history.jsonl → runtime_id` in B-session events          | Identify mechanism       | B events must contain `runtime_id`           | Controller verifies |
| Actual continuation   | New authoritative event caused by B             | New `history.jsonl` entry with `at` > A-terminal `at`     | Record A terminal state  | New B event must exist with later timestamp  | Controller verifies |
| Persistence           | B result survives execution                     | `context.json` + `history.jsonl` after B ends             | Record A state           | B result persisted — readable after B ends   | Controller verifies |
| DBP continuity        | Same approved engineering target                | DBP repo file + PI scope field                            | Approved target          | B work belongs to approved target            | Controller verifies |
| Project isolation     | DBP state remains correctly scoped              | `process.json → engineering_scope_identity`               | Record A                 | Must remain DBP scope identity               | Controller verifies |

---

## Session-A Controller Checkpoint

*(Human Controller completes this table AFTER Session A ends and BEFORE Session B begins.)*

| Value                                    | Session-A recorded value |
| ---------------------------------------- | ------------------------ |
| Process Instance ID                      |                          |
| DBP scope identity                       |                          |
| Execution Context identity/version       |                          |
| Process state                            |                          |
| Persisted version                        |                          |
| Representative prior evidence ID/content |                          |
| Pending execution state                  |                          |
| Session-A identifier                     |                          |
| Runtime/execution identifier             |                          |
| Session-A start timestamp                |                          |
| Session-A end timestamp                  |                          |
| DBP repository revision/state            |                          |

> **BLOCKING GATE:** Session B must NOT start until this checkpoint is fully recorded.

Preserve the raw authoritative artifacts (`process.json`, `context.json`, `history.jsonl`)
at this boundary — copy or snapshot them before Session B begins.

---

## Session Boundary

*(Human Controller records at the session boundary.)*

| Field                              | Value |
| ---------------------------------- | ----- |
| Session-A identifier               |       |
| Execution/runtime ID               |       |
| Start timestamp                    |       |
| End timestamp                      |       |
| Process Instance ID                |       |
| Final authoritative state/version  |       |
| DBP repository state               |       |

---

## Session-B Bootstrap Information

*(Human Controller records exactly what was supplied to Session B.)*

Permitted bootstrap information:
1. AESM ProcessStore root path
2. Process Instance ID

Must NOT be supplied: Session-A transcript, Agent reasoning, prior evidence,
copied Execution Context, manually reconstructed state, implementation summary,
copied continuation instructions.

| Item supplied to Session B            | Value |
| ------------------------------------- | ----- |
| ProcessStore root path                |       |
| Process Instance ID                   |       |
| Any other identifier (if applicable)  |       |

---

## Session-B Freshness Record

*(Human Controller establishes this record — NOT Session B.)*

| Field                                  | Session A | Session B |
| -------------------------------------- | --------- | --------- |
| Session identifier                     |           |           |
| Runtime/execution identifier           |           |           |
| Process identifier (if available)      |           |           |
| Start timestamp                        |           |           |
| End timestamp                          |           |           |
| Conversation identifier (if available) |           |           |

---

## Post-Session-B Controller Checkpoint

*(Human Controller records after Session B ends, from preserved artifacts.)*

| Value                        | Session-B observed value | Matches/relates to Session A? |
| ---------------------------- | ------------------------ | ----------------------------- |
| Process Instance ID          |                          |                               |
| DBP scope identity           |                          |                               |
| Recovered Execution Context  |                          |                               |
| Initial recovered version    |                          |                               |
| Recovered prior evidence     |                          |                               |
| Session-B identifier         |                          |                               |
| Runtime/execution identifier |                          |                               |
| New state/version            |                          |                               |
| New evidence/event           |                          |                               |
| Persisted final state        |                          |                               |
| DBP repository state         |                          |                               |

---

## Controller Notes

*(Free-form field for Human Controller observations, anomalies, deviations,
and any rerun decisions. Each rerun must be recorded as a separate controlled
attempt with the relevant baseline re-recorded.)*

