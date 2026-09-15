# Runtime API Inspection

## 1. Inspection Scope

### Inspected

| Source | Purpose |
|---|---|
| [`runtime/core/models.py`](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/runtime/core/models.py) | ProcessInstance and ExecutionContext data models |
| [`runtime/core/runtime.py`](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/runtime/core/runtime.py) | Runtime control surface — all public operations |
| [`runtime/core/store.py`](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/runtime/core/store.py) | ProcessStore — persistence boundary |
| [`runtime/core/__init__.py`](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/runtime/core/__init__.py) | Public API exports |
| [`runtime/persistence/json_store.py`](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/runtime/persistence/json_store.py) | JsonStore / JsonlStore — atomic file persistence |
| [`runtime/README.md`](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/runtime/README.md) | Runtime scope and limitations documentation |
| [`tests/lifecycle/test_runtime_lifecycle.py`](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/tests/lifecycle/test_runtime_lifecycle.py) | Lifecycle transition and guard tests (7 tests) |
| [`tests/lifecycle/test_process_instance_lifecycle_control.py`](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/tests/lifecycle/test_process_instance_lifecycle_control.py) | Lifecycle determination authority tests (16 tests) |
| [`tests/continuity/test_runtime_recovery.py`](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/tests/continuity/test_runtime_recovery.py) | Recovery, persistence, and continuity tests (12 tests) |
| [`tests/recording/test_runtime_recording.py`](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/tests/recording/test_runtime_recording.py) | Decision, artifact, verification recording and rollback tests (53 tests) |
| [`tests/continuity/xprocess_orchestrator.py`](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/tests/continuity/xprocess_orchestrator.py) | Cross-process continuity experiment |
| [`execution/AGENT-RUNTIME-EXECUTION-BRIDGE-INSPECTION.md`](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/execution/AGENT-RUNTIME-EXECUTION-BRIDGE-INSPECTION.md) | Prior bridge inspection (authorized this work) |

### Intentionally Excluded

| Item | Reason |
|---|---|
| `docs/` architecture documents | Inspected in prior bridge inspection; this task focuses on implementation evidence |
| `IMPLEMENTATION_PLAN.md` | Not modified; implementation plan is upstream context, not the subject of this inspection |
| `schemas/`, `scripts/` | No schema or script modifications are in scope |
| `apply_lifecycle_determination()` | Lifecycle control exists but is not required for the first vertical slice's engineering process flow; excluded from the adapter surface (see §5 for justification) |
| `reconsider()` | Reconsideration exists but the first vertical slice's happy path does not require it; excluded from minimal surface |

### Verification Evidence

**Test suite (freshly executed):**

```
88 passed in 1.01s (Python 3.13.5, pytest, macOS)
```

All tests passed without modification. No Runtime or test source was changed.

**Executable Runtime verification (freshly executed):**

60 behavioral checks covering: Process Instance creation, known-identifier recovery, Execution Context access, full first-vertical-slice dispatch, three guard-rejection scenarios, persistence after mutation, cross-Runtime recovery, and rollback consistency. All 60 checks passed. Temporary verification state was cleaned up.

---

## 2. Runtime Evidence

### Architecture

The Runtime is a Python library consisting of four core modules:

| Module | Lines | Role |
|---|---|---|
| `models.py` | 75 | `ProcessInstance` and `ExecutionContext` dataclasses |
| `runtime.py` | 393 | `Runtime` class — the control surface |
| `store.py` | 134 | `ProcessStore` — persistence with rollback |
| `json_store.py` | 63 | `JsonStore` / `JsonlStore` — atomic file I/O |

### Public Runtime API Surface

| Method | Purpose | Evidence Source |
|---|---|---|
| `create_process(objective)` | Creates PI + EC, persists, attaches | [runtime.py:41–46](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/runtime/core/runtime.py#L41-L46) |
| `attach(process_instance_id)` | Loads PI + EC from store, attaches | [runtime.py:48–51](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/runtime/core/runtime.py#L48-L51) |
| `start_investigation()` | initial → investigation | [runtime.py:53–57](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/runtime/core/runtime.py#L53-L57) |
| `observe(observation)` | Records recognized evidence | [runtime.py:59–89](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/runtime/core/runtime.py#L59-L89) |
| `recognize_decision(decision, recognition)` | Records recognized engineering decision | [runtime.py:91–107](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/runtime/core/runtime.py#L91-L107) |
| `begin_implementation()` | investigation → implementation | [runtime.py:109–116](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/runtime/core/runtime.py#L109-L116) |
| `set_pending_execution(work)` | Records continuation work | [runtime.py:118–124](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/runtime/core/runtime.py#L118-L124) |
| `record_artifact(artifact)` | Records implementation artifact | [runtime.py:126–140](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/runtime/core/runtime.py#L126-L140) |
| `begin_verification()` | implementation → verification | [runtime.py:142–151](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/runtime/core/runtime.py#L142-L151) |
| `record_verification(result)` | Records verification result | [runtime.py:153–173](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/runtime/core/runtime.py#L153-L173) |
| `reconsider(reason)` | verification → investigation (on failure) | [runtime.py:175–185](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/runtime/core/runtime.py#L175-L185) |
| `recognize_engineering_completion(completion)` | verification → engineering_complete | [runtime.py:187–196](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/runtime/core/runtime.py#L187-L196) |
| `apply_lifecycle_determination(determination)` | Lifecycle transitions (suspend/resume/terminate) | [runtime.py:200–296](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/runtime/core/runtime.py#L200-L296) |
| `stop()` | Detaches Runtime, clears in-memory state | [runtime.py:300–303](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/runtime/core/runtime.py#L300-L303) |

### Public ProcessStore API Surface

| Method | Purpose |
|---|---|
| `create(instance, context)` | Persists new PI + EC + initial history event |
| `load_instance(pid)` | Loads ProcessInstance from `process.json` |
| `load_context(pid)` | Loads ExecutionContext from `context.json` |
| `save_context(context, event)` | Persists context mutation + history event with rollback |
| `save_lifecycle(instance, context, event)` | Persists lifecycle transition with multi-file rollback |
| `history(pid)` | Reads history.jsonl |

### Authoritative State Attributes

| Attribute | Access Path | Type |
|---|---|---|
| `runtime.process_instance` | Direct attribute | `ProcessInstance` |
| `runtime.context` | Direct attribute | `ExecutionContext` |
| `runtime.attached` | Direct attribute | `bool` |
| `runtime.runtime_id` | Direct attribute | `str` |
| `runtime.store` | Direct attribute | `ProcessStore` |

---

## 3. Process Instance Access

### A. Creation

**Capability:** `Runtime.create_process(objective: str) → str`

**Evidence classification:** Observed — freshly executed.

**Behavior established:**

1. Generates UUID (`str(uuid4())`).
2. Creates `ProcessInstance` with lifecycle `"active"`, engineering objective set to the supplied argument.
3. Creates `ExecutionContext` linked to the ProcessInstance.
4. Persists both to `<store_root>/process-instance/<uuid>/process.json` and `context.json`.
5. Appends `process_created` event to `history.jsonl`.
6. Sets `runtime.attached = True`, `runtime.process_instance`, `runtime.context`.
7. Returns the UUID string.

**Required inputs:** `objective` (string).

**Verification:** Executable verification check 1 — PASSED. Process Instance created with UUID, lifecycle `"active"`, state `"initial"`, correct objective.

### B. Recovery / Attach

**Capability:** `Runtime.attach(process_instance_id: str) → None`

**Evidence classification:** Observed — freshly executed.

**Behavior established:**

1. Calls `store.load_instance(process_instance_id)` — loads `process.json`, validates lifecycle value.
2. Calls `store.load_context(process_instance_id)` — loads `context.json`, validates required fields, validates identity match.
3. Sets `runtime.process_instance`, `runtime.context`, `runtime.attached = True`.
4. Raises `PersistenceError` if `process.json` or `context.json` is missing or corrupt.
5. Works across different `Runtime` instances with different `runtime_id` values.
6. Works from a fresh `ProcessStore` pointing to the same filesystem root.

**Required inputs:** `process_instance_id` (UUID string).

**Verification:** Executable verification checks 2 and 9 — PASSED. Both same-store recovery and fresh-store recovery demonstrated.

### C. Objective-to-Instance Discovery

**Capability:** **Not present.**

**Evidence classification:** Missing / Unresolved.

**Assessment:**

The existing Runtime provides no mechanism to discover a Process Instance from:
- An engineering objective string
- A repository path or file reference
- Any identifier other than the UUID

The persistence store uses UUID-based directory naming (`process-instance/<uuid>/`). There is no index, registry, search, or mapping capability.

`attach()` requires the exact UUID. It does not solve the problem of: *"Given that a human requests 'Change business_id to POST_SELECT in Add_Review_Form', which existing Process Instance (if any) corresponds to that request?"*

**Impact on first vertical slice:** The first implementation slice can operate by:
- Creating a new Process Instance for each new engineering request; or
- Accepting an explicitly provided UUID for continuation.

Both paths use existing Runtime capabilities. Neither requires objective-to-instance discovery for the first slice.

Objective-to-instance discovery is a **separate architectural/design decision** that does not block bridge implementation design for the first vertical slice.

---

## 4. Execution Context Access

### Authoritative Access Path

**Capability:** `runtime.context` (direct attribute access after `create_process()` or `attach()`).

**Evidence classification:** Observed — freshly executed.

**Behavior established:**

The `runtime.context` attribute is the authoritative `ExecutionContext` instance. It contains all 18 semantic fields documented in [`models.py:38–74`](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/runtime/core/models.py#L38-L74):

| Field | Type | Purpose |
|---|---|---|
| `process_instance_id` | `str` | Identity link |
| `engineering_objective` | `str` | What the engineering process is about |
| `process_state` | `str` | Current state: initial/investigation/implementation/verification/engineering_complete |
| `execution_mode` | `str` | Active/passive (currently always "active") |
| `requirements` | `list[dict]` | Engineering requirements |
| `constraints` | `list[str]` | Engineering constraints |
| `evidence` | `list[dict]` | Recognized evidence |
| `assumptions` | `list[str]` | Recorded assumptions |
| `risks` | `list[str]` | Recorded risks |
| `candidate_solutions` | `list[dict]` | Candidate solutions |
| `engineering_decisions` | `list[dict]` | Recognized engineering decisions |
| `decision_gates` | `list[dict]` | Decision gates |
| `artifacts` | `list[dict]` | Recorded implementation artifacts |
| `verification` | `dict` | Verification result |
| `unresolved_matters` | `list[str]` | Unresolved matters |
| `pending_execution` | `list[dict]` | Continuation work |
| `execution_determination` | `dict | None` | Execution determination |
| `failure_uncertainty` | `list[dict]` | Failure/uncertainty records |
| `engineering_completion` | `bool` | Whether engineering is complete |
| `version` | `int` | Monotonically increasing version counter |

**Context is backed by the same Process Instance state:** `runtime.context.process_instance_id == runtime.process_instance.process_instance_id`. Both are loaded from the same persisted state via `ProcessStore`.

**No duplicate representation required:** The Agent can receive `runtime.context.to_dict()` as a single authoritative state snapshot. No second context model is needed.

**Verification:** Executable verification check 3 — PASSED. All expected context fields are present and correctly typed.

---

## 5. Runtime Dispatch Surface

### First Vertical Slice Operations

The DBP Add_Review_Form first vertical slice requires the following engineering process flow:

```
initial → investigation → implementation → verification → engineering_complete
```

with evidence recording, decision recognition, artifact recording, and verification recording along the way.

### Included Operations — Detailed Inventory

#### `create_process(objective: str) → str`

| Attribute | Value |
|---|---|
| **Engineering purpose** | Create a new Process Instance for the engineering request |
| **Required inputs** | `objective` (string describing the engineering task) |
| **Guards/preconditions** | None — can be called on any Runtime |
| **Resulting state changes** | New PI created with lifecycle `"active"`, new EC with state `"initial"`, Runtime attached |
| **Return value** | UUID string (process_instance_id) |
| **Persistence behavior** | Creates `process.json`, `context.json`, `history.jsonl` |
| **Rollback behavior** | None — creation is atomic via ProcessStore |
| **Why the adapter needs it** | Bridge responsibility 1 — Process Instance access (creation path) |
| **Appropriate for direct dispatch** | Yes — direct delegation |

#### `attach(process_instance_id: str) → None`

| Attribute | Value |
|---|---|
| **Engineering purpose** | Recover an existing Process Instance from persistent state |
| **Required inputs** | `process_instance_id` (UUID string) |
| **Guards/preconditions** | PI must exist in store; `process.json` and `context.json` must be valid |
| **Resulting state changes** | Runtime loads PI and EC, sets `attached = True` |
| **Return value** | None |
| **Persistence behavior** | Read-only |
| **Rollback behavior** | Not applicable (no mutation) |
| **Why the adapter needs it** | Bridge responsibility 1 — Process Instance access (recovery path) |
| **Appropriate for direct dispatch** | Yes — direct delegation |

#### `start_investigation() → None`

| Attribute | Value |
|---|---|
| **Engineering purpose** | Begin the investigation phase |
| **Required inputs** | None |
| **Guards/preconditions** | Attached; active lifecycle; state must be `"initial"` |
| **Resulting state changes** | `process_state` → `"investigation"` |
| **Return value** | None |
| **Persistence behavior** | Saves context, appends `investigation_started` history event |
| **Rollback behavior** | Implicit — `_set_state()` calls `save_context()` which has rollback |
| **Why the adapter needs it** | Bridge responsibility 3 — the first operation in any engineering process |
| **Appropriate for direct dispatch** | Yes — direct delegation |

#### `observe(observation: dict) → None`

| Attribute | Value |
|---|---|
| **Engineering purpose** | Record recognized evidence discovered during investigation |
| **Required inputs** | `observation` dict with a `recognition` key (`{"recognized": True, "basis": "..."}`) |
| **Guards/preconditions** | Attached; recognition validation (`recognized=True`, `basis` non-empty) |
| **Resulting state changes** | Evidence appended to `context.evidence` (sans `recognition` key) |
| **Return value** | None |
| **Persistence behavior** | Saves context, appends `evidence_recorded` history event |
| **Rollback behavior** | Explicit — restores `evidence`, `version`, `updated_at` on persistence failure |
| **Why the adapter needs it** | Bridge responsibility 3 — investigation findings must reach authoritative state |
| **Appropriate for direct dispatch** | Yes — direct delegation |

#### `recognize_decision(decision: dict, recognition: dict) → None`

| Attribute | Value |
|---|---|
| **Engineering purpose** | Record a recognized engineering decision |
| **Required inputs** | `decision` (any dict), `recognition` (`{"recognized": True, "basis": "..."}`) |
| **Guards/preconditions** | Attached; recognition validation; state must be `"initial"` or `"investigation"` |
| **Resulting state changes** | Decision appended to `context.engineering_decisions` |
| **Return value** | None |
| **Persistence behavior** | Saves context, appends `engineering_decision_recognized` history event |
| **Rollback behavior** | Explicit — restores `engineering_decisions`, `version`, `updated_at` on failure |
| **Why the adapter needs it** | Bridge responsibility 3 — required before implementation can begin |
| **Appropriate for direct dispatch** | Yes — direct delegation |

#### `begin_implementation() → None`

| Attribute | Value |
|---|---|
| **Engineering purpose** | Transition to implementation phase |
| **Required inputs** | None |
| **Guards/preconditions** | Attached; active lifecycle; state `"investigation"`; at least one engineering decision |
| **Resulting state changes** | `process_state` → `"implementation"`; `pending_execution` cleared |
| **Return value** | None |
| **Persistence behavior** | Saves context, appends `implementation_started` history event |
| **Rollback behavior** | Implicit via `_set_state()` |
| **Why the adapter needs it** | Bridge responsibility 3 — required state transition |
| **Appropriate for direct dispatch** | Yes — direct delegation |

#### `record_artifact(artifact: dict) → None`

| Attribute | Value |
|---|---|
| **Engineering purpose** | Record an implementation artifact |
| **Required inputs** | `artifact` (any dict) |
| **Guards/preconditions** | Attached; active lifecycle; state `"implementation"` |
| **Resulting state changes** | Artifact appended to `context.artifacts` |
| **Return value** | None |
| **Persistence behavior** | Saves context, appends `artifact_recorded` history event |
| **Rollback behavior** | Explicit — restores `artifacts`, `version`, `updated_at` on failure |
| **Why the adapter needs it** | Bridge responsibility 3 — records what was implemented |
| **Appropriate for direct dispatch** | Yes — direct delegation |

#### `begin_verification() → None`

| Attribute | Value |
|---|---|
| **Engineering purpose** | Transition to verification phase |
| **Required inputs** | None |
| **Guards/preconditions** | Attached; active lifecycle; state `"implementation"`; at least one artifact; no pending execution |
| **Resulting state changes** | `process_state` → `"verification"`; `verification` cleared to `{}` |
| **Return value** | None |
| **Persistence behavior** | Saves context, appends `verification_started` history event |
| **Rollback behavior** | Implicit via `_set_state()` |
| **Why the adapter needs it** | Bridge responsibility 3 — required state transition |
| **Appropriate for direct dispatch** | Yes — direct delegation |

#### `record_verification(result: dict) → None`

| Attribute | Value |
|---|---|
| **Engineering purpose** | Record verification result |
| **Required inputs** | `result` (dict, should include `{"passed": True/False}`) |
| **Guards/preconditions** | Attached; active lifecycle; state must be `"initial"`, `"implementation"`, or `"verification"` |
| **Resulting state changes** | `context.verification` set to `result`; state promoted to `"verification"` if not already |
| **Return value** | None |
| **Persistence behavior** | Saves context, appends `verification_recorded` history event |
| **Rollback behavior** | Explicit — restores `verification`, `process_state`, `version`, `updated_at` on failure |
| **Why the adapter needs it** | Bridge responsibility 3 — records verification outcome |
| **Appropriate for direct dispatch** | Yes — direct delegation |

#### `recognize_engineering_completion(completion: dict) → None`

| Attribute | Value |
|---|---|
| **Engineering purpose** | Recognize that engineering is complete |
| **Required inputs** | `completion` dict with recognition (`{"recognized": True, "basis": "..."}`) |
| **Guards/preconditions** | Attached; active lifecycle; recognition validation; state `"verification"`; `verification.passed` is `True` |
| **Resulting state changes** | `engineering_completion` → `True`; `process_state` → `"engineering_complete"` |
| **Return value** | None |
| **Persistence behavior** | Saves context, appends `engineering_completion_recognized` history event |
| **Rollback behavior** | Implicit via `_set_state()` |
| **Why the adapter needs it** | Bridge responsibility 3 — terminal operation of a successful engineering process |
| **Appropriate for direct dispatch** | Yes — direct delegation |

### Excluded Operations — Justification

| Operation | Reason for Exclusion |
|---|---|
| `set_pending_execution()` | The first vertical slice's happy path (SELECT→POST_SELECT change) is a single-artifact, single-session change. Pending execution is for multi-step continuation work. Not required for the first slice. |
| `reconsider()` | Reconsideration handles failed verification. The first vertical slice's happy path succeeds verification. If verification fails, the Agent can re-enter investigation via existing adapter operations rather than through a dedicated reconsideration adapter operation. |
| `apply_lifecycle_determination()` | Lifecycle control (suspend/resume/terminate) is an authorized-controller operation, not an Agent engineering operation. The first vertical slice does not require lifecycle transitions. |
| `stop()` | Detachment is a Runtime-internal cleanup operation. The adapter manages Runtime lifetime, not the Agent. |

> **Note:** These operations exist and are well-tested. They are excluded only because the first vertical slice does not require them. If a future vertical slice requires continuation work (`set_pending_execution`), reconsideration, or lifecycle control, the adapter surface can be extended at that time with separate authorization.

---

## 6. Authoritative Result / State Return

### What Runtime Operations Return

All Runtime engineering operations return `None`. They communicate results through mutation of `runtime.context` and `runtime.process_instance`, both of which are in-memory objects backed by persistent state.

### How Resulting State Can Be Obtained

After any Runtime operation, the authoritative state is available through:

| Access Path | Returns | Authoritative? |
|---|---|---|
| `runtime.context` | `ExecutionContext` instance | Yes — this is the authoritative in-memory state |
| `runtime.context.to_dict()` | Full context as `dict[str, Any]` | Yes — serializable snapshot |
| `runtime.process_instance` | `ProcessInstance` instance | Yes |
| `runtime.process_instance.to_dict()` | Full PI as `dict[str, Any]` | Yes — serializable snapshot |
| `store.load_context(pid)` | Fresh load from persistence | Yes — represents persisted state |
| `store.history(pid)` | Event history as `list[dict]` | Yes — append-only record |

### Adapter Result Model Assessment

**An adapter does not need to construct a new result model.** The existing `context.to_dict()` and `process_instance.to_dict()` provide complete, serializable snapshots of authoritative state. The adapter can return these directly.

For bridge responsibility 4 (authoritative result/state return), the adapter pattern is:

```text
Agent dispatches operation → adapter calls Runtime method → 
  on success: return context.to_dict() + process_instance.to_dict()
  on guard rejection: return error type + message + unchanged state
```

**Evidence classification:** Established — the existing Runtime provides all necessary state access without requiring adapter-level state construction.

**Verification:** Executable verification check 8 — PASSED. After a complete vertical slice dispatch, all state was correctly persisted and recoverable.

---

## 7. Guard, Error, and Rollback Semantics

### Guard Types

The Runtime uses three categories of guards:

| Guard | Method | Behavior |
|---|---|---|
| **Attachment guard** | `_require_attached()` | Raises `RuntimeError` if not attached |
| **Lifecycle guard** | `_require_active_lifecycle()` | Raises `RuntimeError` if lifecycle is not `"active"` |
| **State guard** | `_require_state(expected)` | Raises `RuntimeError` if `process_state` != expected |
| **Recognition guard** | `_require_recognition(rec, kind)` | Raises `TypeError` (not dict) or `RuntimeError` (not recognized, no basis) |
| **Precondition guard** | Various inline checks | Raises `RuntimeError` (e.g., no decisions before implementation, no artifacts before verification) |

### Executable Guard-Rejection Evidence

Three guard-rejection scenarios were freshly executed:

#### Scenario 1: `begin_implementation` without recognized decision

- **Initial state:** `process_state = "investigation"`, `engineering_decisions = []`
- **Attempted operation:** `begin_implementation()`
- **Result:** `RuntimeError("implementation requires a recognized engineering decision")`
- **State after rejection:** `process_state` remains `"investigation"` — **CONSISTENT**
- **Evidence classification:** Observed

#### Scenario 2: `begin_verification` with pending execution

- **Initial state:** `process_state = "implementation"`, `artifacts = [...]`, `pending_execution = [{"id": "W1", ...}]`
- **Attempted operation:** `begin_verification()`
- **Result:** `RuntimeError("verification requires no pending execution work")`
- **State after rejection:** `process_state` remains `"implementation"` — **CONSISTENT**
- **Evidence classification:** Observed

#### Scenario 3: `recognize_engineering_completion` without passing verification

- **Initial state:** `process_state = "verification"`, `verification = {"passed": False, ...}`
- **Attempted operation:** `recognize_engineering_completion(COMPLETION_REC)`
- **Result:** `RuntimeError("engineering completion requires successful verification")`
- **State after rejection:** `process_state` remains `"verification"` — **CONSISTENT**
- **Evidence classification:** Observed

### Rollback Behavior

Rollback behavior varies by operation:

| Operation | Rollback on persistence failure? | Evidence |
|---|---|---|
| `observe()` | **Yes** — explicit caller-level rollback | [runtime.py:85–89](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/runtime/core/runtime.py#L85-L89), test `test_failed_evidence_persistence_restores_in_memory_authoritative_state` |
| `recognize_decision()` | **Yes** — explicit caller-level rollback | [runtime.py:103–107](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/runtime/core/runtime.py#L103-L107), test `test_decision_and_evidence_rollback_symmetry` |
| `record_artifact()` | **Yes** — explicit caller-level rollback | [runtime.py:136–140](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/runtime/core/runtime.py#L136-L140), test `test_artifact_and_evidence_rollback_symmetry` |
| `record_verification()` | **Yes** — explicit caller-level rollback | [runtime.py:167–173](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/runtime/core/runtime.py#L167-L173), test `test_verification_and_evidence_rollback_symmetry` |
| `apply_lifecycle_determination()` | **Yes** — explicit caller-level rollback | [runtime.py:293–296](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/runtime/core/runtime.py#L293-L296), test `test_lifecycle_persistence_failure_restores_files_and_authoritative_in_memory_state` |
| State transitions (`_set_state()`) | **Implicit** — `save_context()` has store-level rollback | [store.py:57–67](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/runtime/core/store.py#L57-L67) |

**Key finding:** All recording operations (`observe`, `recognize_decision`, `record_artifact`, `record_verification`) have symmetric caller-level rollback. This was confirmed by the cross-capability consistency tests (4 tests, all PASSED).

### Rollback Path Verification

**Executable evidence:** Guard rejection in verification check 10 — after an `observe()` call with invalid recognition (`recognized: False`), the `RuntimeError` was raised at the recognition guard level (before any mutation), and both in-memory state (version, evidence) and persisted state were verified to be unchanged. **PASSED.**

**Test-suite evidence:** The recording tests include dedicated persistence-failure injection tests using `monkeypatch` to replace `save_context()` with a failing stub. All 4 cross-capability symmetry tests PASSED, confirming that all recording operations roll back consistently.

**Lifecycle rollback limitation:** Lifecycle rollback was not independently exercised in the executable verification because it requires `monkeypatch`-level injection that is only practical within the test framework. However, the test suite's `test_lifecycle_persistence_failure_restores_files_and_authoritative_in_memory_state` provides comprehensive evidence (including file-level snapshot verification). This test PASSED.

---

## 8. Cross-Process / Persistence Behavior

### Persistence Model

| File | Purpose | Write Mechanism |
|---|---|---|
| `process-instance/<uuid>/process.json` | ProcessInstance state | Atomic file replacement via `NamedTemporaryFile` + `os.replace()` |
| `process-instance/<uuid>/context.json` | ExecutionContext state | Atomic file replacement |
| `process-instance/<uuid>/history.jsonl` | Append-only event log | File append with `fsync` |

### When State is Persisted

| Event | Persistence trigger |
|---|---|
| `create_process()` | `store.create()` — writes all three files |
| Any `_set_state()` call | `store.save_context()` — writes `context.json` + appends `history.jsonl` |
| `observe()`, `recognize_decision()`, `record_artifact()`, `record_verification()` | `store.save_context()` |
| `set_pending_execution()` | `store.save_context()` |
| `apply_lifecycle_determination()` | `store.save_lifecycle()` — writes `process.json` + optionally `context.json` + appends `history.jsonl` |

**Every mutation persists immediately.** There is no deferred/batched persistence. This means:

1. After any successful Runtime operation, the persisted state is up to date.
2. After a Runtime crash, the persisted state reflects the last successful operation.
3. The adapter does not need to perform persistence itself.

### Cross-Runtime Recovery Evidence

**Executable verification check 9 — PASSED:**

1. A `ProcessStore` was created with a store root directory.
2. Runtime A (`"inspection-rt-1"`) created a Process Instance and drove it through the full engineering lifecycle.
3. Runtime A was stopped (detached).
4. A **fresh** `ProcessStore` was created pointing to the same directory.
5. Runtime B (`"session-b-runtime"`) attached to the same `process_instance_id`.
6. Runtime B successfully recovered the full state: `engineering_complete`, evidence, decisions, artifacts, verification.

**Test-suite evidence:**
- `test_process_and_context_survive_runtime_replacement` — PASSED
- `test_lc03_suspension_persists_across_runtime_loss` — PASSED
- `test_lc05_recovery_does_not_resume` — PASSED
- `test_lc15_runtime_interruption_does_not_change_lifecycle` — PASSED
- Cross-process experiments (`xprocess_orchestrator.py`) demonstrate persistence across OS process boundaries.

### Adapter Persistence Responsibility

**The adapter does not need to perform persistence.** The chain is:

```
Agent → Adapter → Runtime method → ProcessStore → filesystem
```

Every Runtime mutation method calls `store.save_context()` or `store.save_lifecycle()` internally. The adapter calls Runtime methods; the Runtime handles persistence.

---

## 9. Minimal Adapter Surface

### Adapter Contract

| # | Bridge Responsibility | Existing Runtime Capability | Proposed Adapter Operation | Required Inputs | Authoritative Output | Necessity / Omission Test | Classification |
|---|---|---|---|---|---|---|---|
| 1 | Process Instance access (create) | `Runtime.create_process(objective)` | `create_process(objective)` | `objective: str` | `{process_instance_id, context}` | If omitted, no new Process Instance can be created; the Agent cannot begin any engineering process that does not have a pre-existing PI. No other adapter operation provides creation. | **Direct delegation** |
| 2 | Process Instance access (recover) | `Runtime.attach(pid)` | `attach(process_instance_id)` | `process_instance_id: str` | `{process_instance, context}` | If omitted, the Agent cannot recover an existing Process Instance; continuation after session loss is impossible. `create_process` cannot substitute because it creates a new PI rather than recovering existing state. | **Direct delegation** |
| 3 | Execution Context access | `runtime.context` (after create/attach) | `get_context()` | None (operates on attached PI) | `context.to_dict()` | If omitted, the Agent has no way to obtain the current authoritative state; it cannot determine what process state it is in, what evidence has been recorded, what decisions exist, or what work remains. `create_process` and `attach` establish context internally but do not *present* it to the Agent in isolation. | **Thin translation** |
| 4 | Runtime dispatch | `start_investigation()`, `observe()`, `recognize_decision()`, `begin_implementation()`, `record_artifact()`, `begin_verification()`, `record_verification()`, `recognize_engineering_completion()` | `dispatch(operation, params)` | `operation: str`, `params: dict` | `{success, context, error?}` | If omitted, the Agent has no way to invoke any Runtime engineering operation. The Agent's investigation findings, decisions, artifacts, and verification results cannot reach authoritative state. No other adapter operation provides Runtime dispatch. | **Thin translation** |
| 5 | Authoritative result/state return | `runtime.context.to_dict()`, `runtime.process_instance.to_dict()` | *(Integrated into operations 1–4 return values)* | — | — | Not a separate operation. Every adapter operation (create, attach, get_context, dispatch) returns the resulting authoritative state. A separate operation would be redundant because state is always returned as part of the operation response. | **Eliminated** |

### Operation Count: 4

The adapter surface consists of exactly **four operations**, which is below the five-operation review trigger.

### Minimality Verification

| Operation | Canonical Responsibility | Concrete Failure if Omitted | Could Another Operation Cover It? | Verdict |
|---|---|---|---|---|
| `create_process` | 1. Process Instance access | Cannot begin a new engineering process | No — `attach` requires existing PI | **Retained** |
| `attach` | 1. Process Instance access | Cannot resume an existing engineering process | No — `create_process` creates new, does not recover | **Retained** |
| `get_context` | 2. Execution Context access | Agent cannot see authoritative state without re-dispatching an operation | `create_process` and `attach` return context, but if the Agent needs a state refresh (e.g., after a failed dispatch), a separate read-only context access is necessary; however, `dispatch` also returns context. **Borderline.** | **Retained** — a stateless read is architecturally distinct from a mutating dispatch |
| `dispatch` | 3. Runtime dispatch | Agent contributions never reach authoritative state | No — no other operation invokes Runtime engineering methods | **Retained** |

### `get_context` Retention Justification

`get_context` could theoretically be folded into `dispatch` by adding a no-op dispatch that returns state. However, this would:

1. Conflate read-only state access with mutating operations.
2. Require inventing a pseudo-operation within the dispatch vocabulary.
3. Make it impossible for the Agent to inspect state without dispatching.

A read-only state access that does not trigger any Runtime mutation or guard is architecturally cleaner and prevents misuse. It also directly maps to bridge responsibility 2 (Execution Context access) as a distinct concern from bridge responsibility 3 (Runtime dispatch).

---

## 10. Direct Delegation vs Translation

| Adapter Operation | Classification | Rationale |
|---|---|---|
| `create_process(objective)` | **Direct delegation** | The adapter calls `runtime.create_process(objective)` and returns the resulting state. No input or output transformation is required. |
| `attach(process_instance_id)` | **Direct delegation** | The adapter calls `runtime.attach(pid)` and returns the resulting state. No transformation required. |
| `get_context()` | **Thin translation** | The adapter reads `runtime.context.to_dict()` and `runtime.process_instance.to_dict()` and returns a combined representation. The translation is packaging two existing API results into a single response — no new semantics. |
| `dispatch(operation, params)` | **Thin translation** | The adapter maps an operation name string to a Runtime method, unpacks `params` into method arguments, calls the method, and returns the resulting state (or error). The translation is: `{"operation": "observe", "params": {"fact": "...", "recognition": {...}}}` → `runtime.observe({"fact": "...", "recognition": {...}})`. No new semantics are introduced; the adapter routes and unpacks. |

### No operations require new semantics

Every adapter operation either directly calls an existing Runtime method or performs mechanical input/output packaging. The adapter introduces no:

- New guard logic
- New validation
- New state mutation
- New persistence
- New lifecycle semantics
- New recognition requirements

---

## 11. Missing Capabilities

| Capability | Status | Impact on First Vertical Slice |
|---|---|---|
| **Objective-to-Process-Instance discovery** | **Missing** — the Runtime has no mechanism to find a PI from an engineering objective, repository path, or any non-UUID identifier. | The first vertical slice can operate with explicit UUID (for continuation) or new creation (for new requests). Discovery is a **separate design decision** that does not block the adapter surface definition. |
| **Process Instance listing / search** | **Missing** — `ProcessStore` has no `list()` or `search()` method. | Not required for the first vertical slice. If discovery is eventually needed, a listing capability would support it, but that is outside this inspection's scope. |
| **Agent identity tracking** | **Absent from adapter** — the Runtime records `runtime_id` on events but has no concept of Agent identity beyond that. | Not required for the first vertical slice. Agent identity could be passed as part of the `runtime_id` or as metadata in contributions. This is an implementation detail, not a missing capability. |

### Objective-to-Process-Instance Discovery — Explicit Classification

**Status:** Missing / Unresolved.

**Nature of the gap:** The Runtime can create Process Instances and recover them by UUID. It cannot answer: *"Does a Process Instance already exist for this engineering objective?"*

**Why this does not block the adapter surface:**

1. The adapter surface is defined in terms of `create_process(objective)` and `attach(process_instance_id)`.
2. The first vertical slice can use `create_process` for a new request or `attach` with an externally-provided UUID.
3. Discovery would be a mechanism *above* or *alongside* the adapter — not inside it.

**Recommended treatment:** If objective-to-instance discovery is needed, it should be treated as a **separate architectural/design decision** with its own authorization. Options include:
- A simple index file maintained by the adapter
- An objective-matching heuristic
- An explicit "active process instance" marker in the repository

None of these options modify Runtime behavior or the adapter's four-operation surface. They add a *pre-adapter* lookup capability.

---

## 12. Boundary Risks or Contradictions

### Risk 1: Process Instance Accumulation

**Observation:** Without objective-to-instance discovery, repeated engineering requests for the same objective may create multiple Process Instances rather than continuing an existing one.

**Assessment:** This is an operational inconvenience, not an architectural contradiction. The AESM model does not prohibit multiple Process Instances for similar objectives. Each PI is a distinct engineering process.

**Recommendation:** Address in the discovery design decision, not in the adapter.

### Risk 2: Adapter as Implicit Orchestrator

**Observation:** The `dispatch` operation routes Agent requests to Runtime methods. If the adapter begins making sequencing decisions (e.g., automatically calling `start_investigation()` before `observe()`), it would become an implicit orchestration engine.

**Assessment:** The adapter must be a **pass-through dispatcher**, not a sequencer. The Agent decides which operations to request; the Runtime enforces guards. The adapter must not make sequencing decisions.

**Constraint for implementation:** The adapter must not perform implicit state transitions or pre-flight sequencing.

### Risk 3: Recognition Responsibility

**Observation:** Several Runtime operations require `recognition` dicts with `{"recognized": True, "basis": "..."}`. The question arises: who constructs these?

**Assessment:** The Agent constructs recognition records as part of its engineering process. The adapter passes them through. The Runtime validates them. The adapter must not auto-generate recognition records.

**Constraint for implementation:** The adapter must not fabricate or modify recognition records.

### No architectural contradictions identified

The four-part bridge boundary is consistent with the Runtime's existing architecture. No AESM semantic boundary needs to be changed.

---

## 13. Implementation Constraints

A future bridge implementation must obey these constraints:

### Semantic Preservation

1. The adapter must not modify Runtime behavior. All state mutation flows through existing Runtime methods.
2. The adapter must not bypass Runtime guards. If the Runtime rejects an operation, the adapter must propagate the rejection.
3. The adapter must not introduce new guard logic. Validation is the Runtime's responsibility.
4. The adapter must not introduce new persistence. The Runtime handles persistence via ProcessStore.
5. The adapter must not introduce new authoritative state models. `runtime.context` and `runtime.process_instance` are the authoritative representations.

### Operational Constraints

6. The adapter must not perform implicit state transitions. The Agent decides operation sequencing; the Runtime enforces preconditions.
7. The adapter must not fabricate or modify recognition records. Recognition is the Agent's (or governing execution semantics') responsibility.
8. The adapter must not assume a specific Execution Environment (no VS Code, MCP, or CLI dependency at the adapter level).
9. The adapter must return authoritative Runtime state after every operation. The Agent must always receive the resulting state, not a stale or constructed representation.
10. The adapter must propagate Runtime errors (type, message) to the Agent without swallowing or transforming them beyond serialization.

### Architectural Constraints

11. The adapter is not a replacement Runtime, Process Store, or orchestration engine.
12. The adapter does not solve objective-to-Process-Instance discovery. That is a separate design decision.
13. The adapter does not perform lifecycle control for the first vertical slice. Lifecycle operations can be added in a future extension.
14. The Runtime's existing rollback behavior is authoritative. The adapter must not introduce a second rollback mechanism.

---

## 14. Inspection Conclusion

### **READY FOR BRIDGE IMPLEMENTATION DESIGN**

**Justification:**

| Readiness Criterion | Status |
|---|---|
| All four bridge responsibilities have a concrete Runtime mapping | **Yes** — §9 maps each responsibility to specific Runtime capabilities |
| Minimum adapter surface can be stated concretely | **Yes** — four operations: `create_process`, `attach`, `get_context`, `dispatch` |
| Every proposed adapter operation passes the omission test | **Yes** — §9 minimality verification |
| No Runtime semantic modification is required | **Yes** — the adapter delegates entirely to existing Runtime methods |
| No new persistence mechanism is required | **Yes** — the Runtime handles all persistence |
| No new authoritative state model is required | **Yes** — `context.to_dict()` and `process_instance.to_dict()` are sufficient |
| No unresolved architectural contradiction blocks implementation design | **Yes** — §12 identifies no contradictions |

### Known Limitation: Objective-to-Process-Instance Discovery

Objective-to-Process-Instance discovery is **absent** from the current Runtime. This is explicitly recorded as a **separate design decision** that does not block bridge implementation design because:

1. The first vertical slice can operate from a newly created Process Instance or an explicitly provided UUID.
2. Discovery is architecturally above/alongside the adapter, not inside it.
3. The adapter surface (`create_process` + `attach`) provides both paths.

If a future vertical slice requires automatic discovery, that will require a separate authorization and design decision.

---

## Appendix A: Test Suite Execution Record

**Freshly executed** during this inspection on 2026-09-14:

```
$ .venv/bin/python -m pytest -v --tb=short
88 passed in 1.01s (Python 3.13.5, pytest, macOS)
```

| Test File | Tests | Result |
|---|---|---|
| `tests/continuity/test_runtime_recovery.py` | 12 | PASSED |
| `tests/lifecycle/test_process_instance_lifecycle_control.py` | 16 | PASSED |
| `tests/lifecycle/test_runtime_lifecycle.py` | 7 | PASSED |
| `tests/recording/test_runtime_recording.py` | 53 | PASSED |

## Appendix B: Executable Verification Record

**Freshly executed** during this inspection on 2026-09-14:

60 behavioral checks across 10 categories:

| Category | Checks | Result |
|---|---|---|
| 1. Process Instance Creation | 7 | ALL PASSED |
| 2. Known-Identifier Attach/Recovery | 5 | ALL PASSED |
| 3. Execution Context Access | 7 | ALL PASSED |
| 4. First Vertical Slice Dispatch | 10 | ALL PASSED |
| 5. Guard Rejection — no decision | 2 | ALL PASSED |
| 6. Guard Rejection — pending execution | 2 | ALL PASSED |
| 7. Guard Rejection — no passing verification | 2 | ALL PASSED |
| 8. Persistence After Mutation | 16 | ALL PASSED |
| 9. Cross-Runtime Recovery | 4 | ALL PASSED |
| 10. Rollback Consistency | 5 | ALL PASSED |

Temporary verification state was created in a system temp directory and cleaned up after execution.

## Appendix C: Evidence Classification Key

| Classification | Meaning |
|---|---|
| **Observed** | Directly verified from source code, tests, or executable behavior during this inspection |
| **Established** | A conclusion supported by observed implementation evidence |
| **Recommended** | A bounded adapter recommendation derived from established Runtime capabilities |
| **Missing / Unresolved** | A capability or fact that cannot currently be established |
