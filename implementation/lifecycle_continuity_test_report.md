# AESM Lifecycle and Continuity Validation Test Report

> **Report type:** Validation experiment — empirical baseline of current AESM implementation
> **Report date:** 2026-09-05T16:05 +07:00 (UTC: 2026-09-05T09:05Z)
> **Report author:** Automated validation agent

---

## Execution Context

| Item | Value |
| ---- | ----- |
| Repository | `AI-Assisted-Engineering-System-Model` |
| Commit | `ef6c9afcdad703b376b0f0b63cbc41366e0e74de` |
| Commit message | `Add Runtime lifecycle conformance tests` |
| Commit date | `2026-09-05 15:27:40 +0700` |
| Working-tree status | Clean (no uncommitted changes) |
| Python version | 3.13.5 |
| pytest version | 9.1.1 |
| Virtual environment | `.venv/bin/python` |
| Package configuration | No `pyproject.toml`, `requirements.txt`, or `setup.py` present; imports work from repo root via `.venv` |
| Test date/time | 2026-09-05T09:13:26 UTC |
| Experiment evidence store | `/var/folders/_v/.../T/aesm_experiment_u_u2ju53/` (copied to artifact scratch) |
| Process Instance ID | `dedf4bfa-65b7-4065-86c8-da3ae70ed1a2` |

### Commands/tools used

```text
git log -n 1 --format="%H %ai %s"
git status --short
python3 --version
.venv/bin/python -m pytest -v
.venv/bin/python scratch/lifecycle_continuity_experiment.py
```

---

## Baseline

### Existing test-suite command

```text
.venv/bin/python -m pytest -v
```

### Complete baseline result

```text
12 passed in 0.18s
```

| Test file | Tests | Result |
| --------- | ----- | ------ |
| `tests/continuity/test_runtime_recovery.py` | 8 | All PASSED |
| `tests/lifecycle/test_runtime_lifecycle.py` | 4 | All PASSED |

### Pre-existing failures

None. All 12 tests pass on the current commit.

### Impact on experiment

No pre-existing failures affect the lifecycle/continuity experiment.

---

## Test Basis

### Relevant normative AESM documents

| Document | Role |
| -------- | ---- |
| `docs/05-Process-Instance-and-Execution-Context.md` | Defines Process Instance and Execution Context concepts |
| `docs/04-Execution-Model.md` | Defines Process Execution Model (PEM) |
| `docs/07-Runtime-and-Conformance.md` | Defines Runtime conformance requirements |
| `docs/08-Continuity-Traceability-and-Reconsideration.md` | Defines continuity requirements |
| `docs/13-Runtime-Implementer-Guide.md` | Runtime implementation guidance |

### Existing lifecycle/continuity tests

| File | Purpose |
| ---- | ------- |
| `tests/continuity/test_runtime_recovery.py` | Process Instance creation, ExecutionContext round-trip, Runtime replacement recovery, decision/completion recognition, missing-context failure, history preservation |
| `tests/lifecycle/test_runtime_lifecycle.py` | Required lifecycle transitions, transition-condition enforcement, failed-verification reconsideration, completion-bypass prevention |

### Relevant implementation components

| Component | File | Purpose |
| --------- | ---- | ------- |
| ProcessInstance | `runtime/core/models.py` | Process Instance dataclass with `create()`, `to_dict()` |
| ExecutionContext | `runtime/core/models.py` | Execution Context dataclass with `create()`, `to_dict()`, `from_dict()` |
| Runtime | `runtime/core/runtime.py` | Lifecycle state machine with attach/detach, transitions, and guard conditions |
| ProcessStore | `runtime/core/store.py` | Filesystem persistence for Process Instance, ExecutionContext, and history |
| JsonStore | `runtime/persistence/json_store.py` | Atomic JSON file persistence (temp-file + rename) |
| JsonlStore | `runtime/persistence/json_store.py` | Append-only JSONL history persistence |

### Interpretations required

1. The `Runtime.stop()` method constitutes a "controlled interruption" for the purposes of this experiment. It clears in-memory state without modifying persisted state.
2. A "fresh Runtime" is simulated by creating a new `Runtime` instance with a different `runtime_id` and calling `attach()` — this loads all state exclusively from the filesystem.
3. The experiment runs within a single Python process but uses separate `Runtime` instances to simulate the execution boundary. This is explicitly acknowledged as a limitation (Section 11).

---

## Existing Test Results

### Tests executed

All 12 tests in the repository's test suite.

### Tests passed: 12 / 12

### Tests failed: 0

### What existing tests actually demonstrate

| Test | Demonstrates |
| ---- | ------------ |
| `test_process_instance_creation` | ProcessInstance creation with UUID, objective, lifecycle="active", context_ref, EPM/PEM, timestamps |
| `test_execution_context_contains_minimum_authoritative_information` | ExecutionContext initial state: all fields populated with correct defaults |
| `test_execution_context_round_trip_preserves_semantic_state` | `to_dict()` → `from_dict()` preserves all semantic state including pending_execution with next_action and resumption_conditions |
| `test_process_and_context_survive_runtime_replacement` | Runtime A creates and modifies state → stop → Runtime B attaches and reads identical state from persistence |
| `test_decision_requires_explicit_recognition` | Decisions without `recognized: true` or without `basis` are rejected |
| `test_engineering_completion_requires_explicit_recognition` | Completion requires verification state, passed verification, and explicit recognition |
| `test_missing_context_fails_recovery` | Missing context.json raises PersistenceError on attach |
| `test_history_is_preserved` | History records process_created, observation_recorded, engineering_decision_recognized in order |
| `test_required_lifecycle_transitions` | Full lifecycle: initial → investigation → implementation → verification → engineering_complete |
| `test_transition_conditions_are_enforced` | Guard conditions prevent invalid transitions |
| `test_failed_verification_preserves_failure_and_reopens_investigation` | Reconsideration cycle: failed verification → investigation with failure_uncertainty and unresolved_matters |
| `test_completion_cannot_bypass_verification` | Completion blocked without verification state and without passed verification |

### Coverage gaps relative to this validation

| Gap | Description |
| --- | ----------- |
| Process Instance discoverability | No existing test demonstrates listing/discovering persisted instances from the filesystem |
| Explicit continuity information classification | No existing test separates persisted vs. conversational-only information |
| Full history timeline verification | `test_history_is_preserved` checks 3 events; the full lifecycle (11 events across multiple runtimes) is not tested |
| Cross-runtime history attribution | No existing test verifies that `runtime_id` in history events correctly attributes actions to different Runtime instances |
| ProcessInstance `lifecycle` field update | The `lifecycle` field on ProcessInstance remains "active" throughout and is never updated to reflect completion — only `process_state` on ExecutionContext changes |
| Process termination/disposal | No test addresses instance termination or cleanup |

---

## Scenario Results

### Scenario 8: Process Instance Creation and Initial State

**Objective:** Determine whether a Process Instance can be created and assigned an identifiable initial state.

**Setup:** `ProcessStore` initialized with a temporary directory; `Runtime` created with `runtime_id="runtime-experiment-a"`.

**Expected behavior:** A Process Instance is created with a UUID, persisted to the filesystem as `process.json`, `context.json`, and `history.jsonl`, and is reloadable.

**PASS criteria:**
- [x] Process Instance created successfully
- [x] Receives a stable, non-empty UUID identifier (`dedf4bfa-65b7-4065-86c8-da3ae70ed1a2`)
- [x] Identifier locates the persisted instance at `process-instance/<id>/process.json`
- [x] Subsequent `load_instance()` returns the same Process Instance
- [x] Initial state (`process_state: "initial"`, `lifecycle: "active"`) is persisted
- [x] Initial Execution Context is persisted with all default fields
- [x] Creation event recorded in `history.jsonl` as `process_created`

**Action:** `runtime_a.create_process("Validate AESM lifecycle continuity across execution boundaries")`

**Observed behavior:** Exactly matches expected behavior.

**Evidence:**

| Evidence | Value |
| -------- | ----- |
| `process_instance_id` | `dedf4bfa-65b7-4065-86c8-da3ae70ed1a2` |
| `initial_lifecycle_state` | `active` |
| `initial_process_state` | `initial` |
| `process.json` exists | `True` |
| `context.json` exists | `True` |
| `history.jsonl` exists | `True` |
| Reload ID matches | `True` |
| History event type | `process_created` |

**Result: PASS**

---

### Scenario 9: Controlled Lifecycle Progression

**Objective:** Advance the Process Instance through meaningful supported execution transitions and verify each is persisted.

**Setup:** Continuing from Scenario 8 with the same `runtime_a`.

**Expected behavior:** The Process Instance progresses through `initial → investigation → implementation` with each transition recorded in `history.jsonl`.

**PASS criteria:**
- [x] Supported transitions actually executed
- [x] Resulting state observable after each transition
- [x] Each transition represented in persisted history
- [x] Process Instance loadable after transitions
- [x] ExecutionContext reflects resulting state

**Action sequence:**

1. `start_investigation()` — initial → investigation
2. `observe(...)` — record observation
3. `recognize_decision(...)` — record engineering decision
4. `begin_implementation()` — investigation → implementation
5. `record_artifact(...)` — record implementation artifact
6. `set_pending_execution(...)` — record pending work with `next_action` and `resumption_conditions`

**Observed behavior:**

| Transition | Pre-state | Post-state | Recorded in history |
| ---------- | --------- | ---------- | ------------------- |
| `start_investigation()` | `initial` | `investigation` | `investigation_started` (v1) |
| `observe(...)` | `investigation` | `investigation` | `observation_recorded` (v2) |
| `recognize_decision(...)` | `investigation` | `investigation` | `engineering_decision_recognized` (v3) |
| `begin_implementation()` | `investigation` | `implementation` | `implementation_started` (v4) |
| `record_artifact(...)` | `implementation` | `implementation` | `artifact_recorded` (v5) |
| `set_pending_execution(...)` | `implementation` | `implementation` | `pending_execution_recorded` (v6) |

**Evidence:** `history.jsonl` contains 7 entries (including `process_created`) with monotonically increasing version numbers (0–6) and UTC timestamps. All event types match expected sequence.

**Result: PASS**

---

### Scenario 10: Controlled Interruption

**Objective:** Interrupt execution without losing the state required for continuation.

**Setup:** Process Instance at `implementation` state with 1 observation, 1 decision, 1 artifact, 1 pending execution item, version 6.

**Expected behavior:** `Runtime.stop()` clears in-memory state. Persisted files remain unchanged.

**PASS criteria:**
- [x] Runtime detached (`attached = False`)
- [x] In-memory `context` and `process_instance` set to `None`
- [x] Persisted `process.json`, `context.json`, `history.jsonl` all intact
- [x] Persisted `process_state` remains `implementation`
- [x] Persisted version remains `6`
- [x] History count remains `7`

**Action:** `runtime_a.stop()`

**Observed behavior:** Exactly matches expected behavior.

**Evidence:**

| Evidence | Value |
| -------- | ----- |
| `runtime_a.attached` after stop | `False` |
| `runtime_a.context` after stop | `None` |
| `process.json` exists after stop | `True` |
| `context.json` exists after stop | `True` |
| Persisted `process_state` | `implementation` |
| Persisted version | `6` |

**Result: PASS**

---

### Scenario 11: Continuity Simulation Protocol

**Objective:** Determine whether continuation requires conversational memory or can be accomplished from persisted state alone.

**Setup:** After `runtime_a.stop()`, classify all information as persisted vs. conversational-only, then recover using a fresh `Runtime` instance.

**Expected behavior:** All information required for continuation is persisted. No conversational-only information is required.

**PASS criteria:**
- [x] All required state recovered from persistence
- [x] No conversational-only information required for continuation
- [x] Process Instance discoverable from filesystem (without knowing the ID from conversation)
- [x] All continuity checks pass (8/8)

**Action:** Created `Runtime("runtime-experiment-b")`, called `attach(pid)` where `pid` was discovered by listing the `process-instance/` directory.

**Information Recovery Table:**

| Information | Persisted? | Recoverable? | Required for continuation? |
| ----------- | ---------- | ------------ | -------------------------- |
| `process_instance_id` | ✅ Yes | ✅ Yes | ✅ Yes |
| `lifecycle_state (process_state)` | ✅ Yes | ✅ Yes | ✅ Yes |
| `engineering_objective` | ✅ Yes | ✅ Yes | ✅ Yes |
| `evidence (observations)` | ✅ Yes | ✅ Yes | ✅ Yes |
| `engineering_decisions` | ✅ Yes | ✅ Yes | ✅ Yes |
| `artifacts` | ✅ Yes | ✅ Yes | ✅ Yes |
| `pending_execution` (incl. `next_action`, `resumption_conditions`) | ✅ Yes | ✅ Yes | ✅ Yes |
| `context_version` | ✅ Yes | ✅ Yes | ✅ Yes |
| `history (event timeline)` | ✅ Yes | ✅ Yes | ✅ Yes |
| `runtime_id` of previous execution | ✅ Yes (in history) | ✅ Yes | ❌ No |
| In-memory variable names/flow | ❌ No | ❌ No | ❌ No |

**Continuity checks (all 8/8 passed):**

| Check | Result |
| ----- | ------ |
| `pid_match` | `true` |
| `state_match` | `true` |
| `objective_match` | `true` |
| `evidence_match` | `true` |
| `decisions_match` | `true` |
| `artifacts_match` | `true` |
| `pending_match` | `true` |
| `version_match` | `true` |

**Limitation noted:** The continuity simulation occurred within a single Python process. True cross-process continuity was simulated by using separate `Runtime` instances with different `runtime_id` values. The persisted filesystem state is genuinely independent — `runtime_b` loads exclusively from the filesystem — but the `pid` variable was passed within the same process rather than being independently discovered via a separate process invocation.

**Result: PASS** (with noted simulation limitation)

---

### Scenario 12: Recovery

**Objective:** Recover an interrupted Process Instance from persisted state and verify completeness.

**Setup:** Fresh `Runtime("runtime-experiment-b")` attached to the Process Instance via `attach(pid)`.

**Expected behavior:** All Execution Context fields recovered exactly as persisted before interruption.

**PASS criteria:**
- [x] Same Process Instance identified from persisted state
- [x] Previous lifecycle state recovered (`implementation`)
- [x] Full Execution Context recovered (evidence, decisions, artifacts, pending_execution)
- [x] Recovery did not require information from previous conversation
- [x] Recovered state consistent with persisted history (version 6, 7 history entries)
- [x] Fresh execution can determine continuation state

**Evidence:**

| Recovered field | Value |
| --------------- | ----- |
| `process_instance_id` | `dedf4bfa-65b7-4065-86c8-da3ae70ed1a2` |
| `process_state` | `implementation` |
| `engineering_objective` | `Validate AESM lifecycle continuity across execution boundaries` |
| `evidence` count | `1` |
| `engineering_decisions` count | `1` |
| `artifacts` count | `1` |
| `pending_execution[0].next_action` | `begin_verification` |
| `pending_execution[0].resumption_conditions` | `["implementation artifact recorded", "no pending execution"]` |
| `context_version` | `6` |
| History consistent with context | `True` |

**Result: PASS**

---

### Scenario 13: Continuation After Recovery

**Objective:** Continue the Process Instance using only recovered/persisted state, without requiring conversational memory.

**Setup:** `runtime_b` attached to recovered Process Instance in `implementation` state with pending execution.

**Expected behavior:** The recovered `pending_execution` contains `next_action: "begin_verification"` and `resumption_conditions`. After clearing pending work, the transition `implementation → verification` succeeds.

**PASS criteria:**
- [x] Recovered Process Instance used (not a new instance)
- [x] Next action determined from persisted state (`pending_execution[0].next_action`)
- [x] No conversational-only information required
- [x] Expected transition executed (`implementation → verification`)
- [x] Resulting state persisted (version incremented)
- [x] History records the continuation events

**Action:**
1. Cleared pending execution (recorded as `pending_execution_cleared`, version 7)
2. Called `begin_verification()` (recorded as `verification_started`, version 8)
3. Called `record_verification({"passed": True, ...})` (recorded as `verification_recorded`, version 9)

**Observed behavior:** All transitions succeeded. The `runtime_id` in the history events correctly shows `runtime-experiment-b`, distinguishing post-recovery actions from pre-interruption actions.

**Result: PASS**

---

### Scenario 14: Completion Boundary

**Objective:** Determine whether the current implementation supports Process Instance completion.

**Setup:** Process Instance in `verification` state with `passed: True` verification result.

**Expected behavior:** `recognize_engineering_completion()` transitions to `engineering_complete` state.

**PASS criteria:**
- [x] Terminal state exists (`engineering_complete`)
- [x] Completion transition executed
- [x] Completion persisted (`engineering_completion: true`, `process_state: "engineering_complete"`)
- [x] A later fresh Runtime (`runtime-experiment-c`) recognizes the completed instance
- [ ] Formal Process Instance termination/disposal — **NOT IMPLEMENTED** (known baseline limitation)

**Action:** `runtime_b.recognize_engineering_completion(COMPLETION_RECOGNITION)`

**Evidence:**

| Evidence | Value |
| -------- | ----- |
| `process_state` after completion | `engineering_complete` |
| `engineering_completion` flag | `True` |
| Persisted `process_state` | `engineering_complete` |
| Fresh Runtime C sees completion state | `engineering_complete` |
| Fresh Runtime C sees completion flag | `True` |
| History event | `engineering_completion_recognized` (v10) |

**Interpretation:** The `engineering_complete` state is implemented as a persisted, recognizable state. However:
1. It is a **prototype implementation state**, not a validated universal AESM EPM state.
2. There is no Process Instance **termination** or disposal mechanism — the instance remains in `engineering_complete` indefinitely.
3. The `ProcessInstance.lifecycle` field remains `"active"` even after engineering completion — only `ExecutionContext.process_state` changes.

**Result: PASS** (completion transition) / **NOT TESTABLE** (formal termination/disposal)

---

## Lifecycle Evidence

### Chronological lifecycle timeline from `history.jsonl`

The following timeline is derived entirely from the persisted `history.jsonl` file.

| # | Version | Timestamp (UTC) | Event | Runtime | Semantic State |
| - | ------- | --------------- | ----- | ------- | -------------- |
| 0 | 0 | `09:13:26.386717` | `process_created` | — | initial |
| 1 | 1 | `09:13:26.388898` | `investigation_started` | `runtime-experiment-a` | investigation |
| 2 | 2 | `09:13:26.390210` | `observation_recorded` | `runtime-experiment-a` | investigation |
| 3 | 3 | `09:13:26.391443` | `engineering_decision_recognized` | `runtime-experiment-a` | investigation |
| 4 | 4 | `09:13:26.392664` | `implementation_started` | `runtime-experiment-a` | implementation |
| 5 | 5 | `09:13:26.393950` | `artifact_recorded` | `runtime-experiment-a` | implementation |
| 6 | 6 | `09:13:26.395253` | `pending_execution_recorded` | `runtime-experiment-a` | implementation |
| — | — | — | **EXECUTION BOUNDARY** | `stop()` called | — |
| 7 | 7 | `09:13:26.397990` | `pending_execution_cleared` | `runtime-experiment-b` | implementation |
| 8 | 8 | `09:13:26.403003` | `verification_started` | `runtime-experiment-b` | verification |
| 9 | 9 | `09:13:26.404252` | `verification_recorded` | `runtime-experiment-b` | verification |
| 10 | 10 | `09:13:26.405508` | `engineering_completion_recognized` | `runtime-experiment-b` | engineering_complete |

**Observation:** The `runtime_id` field in history events clearly distinguishes actions performed by different Runtime instances. Events 0–6 are attributed to `runtime-experiment-a` (pre-interruption). Events 7–10 are attributed to `runtime-experiment-b` (post-recovery). This provides traceable evidence of cross-execution continuity.

---

## Continuity Evidence

### State before interruption

| Field | Value |
| ----- | ----- |
| `process_state` | `implementation` |
| `context_version` | `6` |
| Evidence count | `1` |
| Decisions count | `1` |
| Artifacts count | `1` |
| Pending execution count | `1` |
| History entries | `7` |

### Persisted state

All of the above persisted to:
- `process-instance/<id>/process.json`
- `process-instance/<id>/context.json`
- `process-instance/<id>/history.jsonl`

### Execution boundary

`Runtime.stop()` — clears `attached`, `context`, and `process_instance` in memory. No filesystem modification.

### State available after the boundary

All state available via `ProcessStore.load_instance()`, `ProcessStore.load_context()`, and `ProcessStore.history()`. The Process Instance ID is discoverable by listing the `process-instance/` directory.

### Recovered state

Identical to pre-interruption persisted state. All 8 continuity checks passed.

### Information that was unavailable

Only non-required, in-memory information:
- Variable names used in the previous script execution
- The specific `runtime_id` of the previous Runtime (available in history but not needed)
- Script flow/ordering decisions

### Whether continuation required conversational memory

**No.** All information required for continuation was available from persisted state. The `pending_execution` field contained explicit `next_action` and `resumption_conditions` that a fresh execution could use to determine how to proceed.

---

## Findings

### Confirmed capabilities

1. **Process Instance creation** — Fully functional. UUID-based identity, filesystem persistence, atomic writes (temp-file + rename), immediate reloadability.

2. **Execution Context persistence** — Complete round-trip preservation of all 20+ ExecutionContext fields including nested structures (evidence, decisions, artifacts, pending_execution with resumption_conditions).

3. **Lifecycle state machine** — Five implemented states (`initial`, `investigation`, `implementation`, `verification`, `engineering_complete`) with enforced guard conditions preventing invalid transitions.

4. **History/audit trail** — Append-only JSONL history with versioned, timestamped, runtime-attributed events. Provides complete lifecycle traceability.

5. **Cross-execution recovery** — A fresh Runtime instance recovers all authoritative state from the filesystem without requiring any information from the previous execution.

6. **Continuation from persisted state** — The `pending_execution` mechanism with `next_action` and `resumption_conditions` provides explicit, persisted continuation directives that enable a fresh execution to determine the next valid action.

7. **Reconsideration cycle** — Failed verification triggers reconsideration back to investigation, preserving failure_uncertainty and unresolved_matters (verified by existing tests).

8. **Decision/completion recognition protocol** — Explicit `recognized: true` with `basis` prevents unauthorized state transitions.

### Confirmed failures

None identified. All implemented mechanisms operated as designed.

### Known baseline limitations (confirmed, not newly discovered)

1. **Process Instance termination** — Not implemented. A Process Instance in `engineering_complete` state remains in the store indefinitely. There is no disposal, archival, or terminal lifecycle state beyond `engineering_complete`.

2. **`engineering_complete` is a prototype state** — The string `"engineering_complete"` is a current implementation identifier, not a validated universal AESM EPM lifecycle state. It should not be treated as a finalized specification term.

3. **Artifact association** — No explicit Runtime operation for artifact association. `record_artifact()` appends metadata to the Execution Context but does not establish a formal association lifecycle.

4. **ProcessInstance `lifecycle` field divergence** — The `ProcessInstance.lifecycle` field remains `"active"` throughout the entire lifecycle including after `engineering_complete`. Only `ExecutionContext.process_state` tracks the actual lifecycle progression. This creates a semantic inconsistency: the Process Instance claims to be "active" even when the engineering work is complete.

### Newly discovered implementation gaps

1. **No instance enumeration API** — `ProcessStore` has no method to list all Process Instances. Discovery requires manual filesystem traversal of the `process-instance/` directory. This is sufficient for the current prototype but would be a barrier for a production Runtime that needs to manage multiple instances.

2. **No `stop` event in history** — `Runtime.stop()` does not record an event in `history.jsonl`. The execution boundary is invisible in the audit trail. A fresh Runtime cannot determine from history alone that an interruption occurred between events 6 and 7 — it can only infer this from the change in `runtime_id`.

3. **No ProcessInstance update on lifecycle progression** — `ProcessStore.create()` writes `process.json` once. Subsequent lifecycle transitions update only `context.json` and `history.jsonl`. The `process.json` file retains its initial values (e.g., `lifecycle: "active"`, original timestamps) regardless of how far the Process Instance progresses.

4. **Pending execution is a manual/convention mechanism** — The `pending_execution` field relies on the caller to structure it with `next_action` and `resumption_conditions`. There is no enforcement or schema validation by the Runtime. Continuation instructions exist only if the previous execution explicitly recorded them.

### Environmental limitations

1. **Single-process simulation** — The continuity experiment ran within a single Python process using separate Runtime instances. True cross-process continuity was not tested (e.g., running the experiment script twice with a shared store). The filesystem-based persistence mechanism makes cross-process continuity architecturally feasible, but it has not been empirically demonstrated by this experiment.

### Specification ambiguities

1. **Relationship between `ProcessInstance.lifecycle` and `ExecutionContext.process_state`** — The normative model defines both concepts but the implementation does not establish a clear correspondence. `lifecycle` appears to be an instance-level attribute while `process_state` is a context-level attribute, but the implementation uses only `process_state` for lifecycle progression.

2. **Formal definition of "continuation"** — The AESM normative documents describe continuity as a requirement, but the implementation's `pending_execution` mechanism is a convention rather than a formally specified continuation protocol.

### Test/procedure limitations

1. The continuity simulation occurs within a single Agent conversation, which means the `pid` is technically available via Python variable rather than being independently discovered. The experiment compensated by demonstrating filesystem discoverability, but a fully rigorous test would require two independent process invocations.

2. The timestamps in `history.jsonl` are sub-second apart because all transitions were performed programmatically. This does not diminish the evidence but means the timeline does not reflect realistic human-paced engineering work.

---

## Overall Assessment

| Dimension | Assessment | Basis |
| --------- | ---------- | ----- |
| **Lifecycle integrity** | ✅ **PASS** | Five-state machine with enforced guard conditions operates correctly through all supported transitions including reconsideration. |
| **Execution Context persistence** | ✅ **PASS** | Complete round-trip of all 20+ fields via atomic JSON writes. No data loss observed. |
| **Process Instance persistence** | ✅ **PASS** (with gap) | Process Instance is persisted at creation and reloadable. Gap: `process.json` is not updated after creation. |
| **Recovery** | ✅ **PASS** | Full state recovered from filesystem by a fresh Runtime. No missing required fields. |
| **Cross-execution continuity** | ✅ **PASS** (simulated) | Demonstrated via separate Runtime instances. True cross-process continuity not empirically tested but architecturally supported. |
| **Continuation after recovery** | ✅ **PASS** | `pending_execution` with `next_action` and `resumption_conditions` enabled a fresh Runtime to determine and execute the correct next action. |
| **Independence from conversational memory** | ✅ **PASS** | All required continuation information persisted. No conversational-only information needed. |
| **Lifecycle observability** | ✅ **PASS** (with gap) | `history.jsonl` provides full event timeline with versions, timestamps, and runtime attribution. Gap: no `stop`/interruption event recorded. |
| **Evidence traceability** | ✅ **PASS** | Every lifecycle transition produces a versioned, timestamped history entry. Cross-runtime attribution via `runtime_id` field. |
| **Process termination** | ⚠️ **NOT TESTABLE** | Known baseline limitation. No termination/disposal mechanism exists. |

---

## Evidence Index

| # | Evidence | Path/Identifier | Supports claim |
| - | -------- | --------------- | -------------- |
| 1 | `process.json` (initial) | `<store>/process-instance/dedf4bfa.../process.json` | Scenario 8: Process Instance creation and persistence |
| 2 | `context.json` (initial) | `<store>/process-instance/dedf4bfa.../context.json` | Scenario 8: ExecutionContext initial state persistence |
| 3 | `history.jsonl` (initial, 1 entry) | `<store>/process-instance/dedf4bfa.../history.jsonl` | Scenario 8: Creation event recorded |
| 4 | `context.json` (after progression, v6) | Same path, version 6 | Scenario 9: Lifecycle transitions persisted |
| 5 | `history.jsonl` (7 entries, v0–v6) | Same path | Scenario 9: Complete transition history |
| 6 | Persisted files unchanged after `stop()` | Filesystem inspection | Scenario 10: Interruption preserves state |
| 7 | `runtime_b` continuity checks (8/8 pass) | Experiment output | Scenario 11: Cross-execution continuity |
| 8 | Filesystem directory listing | `process-instance/` directory | Scenario 11: PID discoverability without conversational memory |
| 9 | `pending_execution[0].next_action` | `context.json` field | Scenario 12–13: Recovery provides continuation directives |
| 10 | `history.jsonl` (11 entries, v0–v10) | Same path, final state | Scenario 9–14: Complete lifecycle timeline with cross-runtime attribution |
| 11 | `context.json` (final, `engineering_complete`) | Same path, version 10 | Scenario 14: Completion state persisted |
| 12 | `runtime-experiment-c` reads completion state | Experiment output | Scenario 14: Completion recognizable by fresh execution |
| 13 | Baseline test suite (12/12 passed) | `pytest -v` output | Baseline: no pre-existing failures |
| 14 | Full experiment output | `scratch/experiment_full_output.txt` | All scenarios: complete execution transcript |
| 15 | Evidence store copy | `scratch/evidence_store/` | All scenarios: preserved filesystem evidence |
