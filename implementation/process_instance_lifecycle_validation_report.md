# Process Instance Lifecycle Semantics Validation Report

## 1. Executive Summary

This report documents the results of a controlled validation experiment against the AESM runtime implementation on branch `main` at commit `8c2dd09`. The experiment characterizes the current implementation's actual behavior regarding Process Instance lifecycle semantics through empirical observation—not inference from code structure alone.

### Key Findings

1. **`ProcessInstance.lifecycle` never changes from its initial value `"active"` during any Runtime operation.** No Runtime method writes to `ProcessInstance.lifecycle`. No `ProcessStore` method exists to persist changes to the Process Instance after creation. The lifecycle field is **represented** in the model but **not operationally implemented**.

2. **`ExecutionContext.process_state` is the only field that undergoes managed state transitions** during Runtime operation. Process state progresses through `initial` → `investigation` → `implementation` → `verification` → `engineering_complete`, with reconsideration loops back to `investigation`.

3. **No explicit suspension, resumption, or lifecycle termination operations exist.** The Runtime surface provides no `suspend()`, `resume()`, or `terminate()` methods. Engineering completion changes `process_state` and `engineering_completion` but does **not** change `ProcessInstance.lifecycle`.

4. **Pending execution survives Runtime termination** and is fully recoverable by a new Runtime instance. However, no explicit resumption mechanism exists to process pending work items.

5. **`Runtime.stop()` is a purely in-memory detachment operation.** It clears the Runtime's references but writes nothing to persistence and records no history event. It does not alter `ProcessInstance.lifecycle` or `ExecutionContext.process_state`.

---

## 2. Execution Environment

| Property | Value |
|---|---|
| Repository | AI-Assisted-Engineering-System-Model |
| Branch | `main` |
| Commit SHA | `8c2dd09087e064a029d32452a006cbd2b786e5f2` |
| Commit Message | Merge pull request #3 from tuanna2703/docs/continuity-lifecycle-clarifications |
| Working Tree Status | Clean (no modifications) |
| Python Version | 3.13.5 |
| pytest Version | 9.1.1 |
| OS | macOS (darwin) |

---

## 3. Experimental Objective

Determine what the current implementation **actually demonstrates** about Process Instance lifecycle semantics, distinguishing between:

- Process Instance lifecycle (`ProcessInstance.lifecycle`)
- Execution Context process state (`ExecutionContext.process_state`)
- Engineering completion (`ExecutionContext.engineering_completion`)
- Runtime lifetime (attachment/detachment)
- Pending execution and resumption

---

## 4. Governing Constraints

- No Runtime production code was modified.
- No new Runtime capabilities were created.
- No AESM specifications or normative documentation were modified.
- No existing tests were modified.
- No persisted Process Instance or Execution Context files were manually altered.
- The implementation was not optimized for PASS.
- Absence of capability is recorded as a valid finding.

---

## 5. Initial Implementation Inspection

### 5.1 `runtime/core/models.py`

| Aspect | Finding |
|---|---|
| `ProcessInstance.lifecycle` | Field exists; default value `"active"`; type `str` |
| Lifecycle representation | Single string field; no enum, no constants, no defined state set |
| `ExecutionContext.process_state` | Field exists; default `"initial"`; type `str` |
| `ExecutionContext.execution_mode` | Field exists; default `"active"`; type `str` |
| `ExecutionContext.engineering_completion` | Field exists; default `False`; type `bool` |
| `ExecutionContext.pending_execution` | Field exists; default `[]`; type `list[dict]` |
| Relationship | `ExecutionContext.process_instance_id` references `ProcessInstance.process_instance_id` |

**Implementation observation:** `ProcessInstance` has no class-level constants defining valid lifecycle states. `ExecutionContext` has no class-level constants either—those are on `Runtime`.

### 5.2 `runtime/core/runtime.py`

| Aspect | Finding |
|---|---|
| Process state constants | `INVESTIGATION`, `IMPLEMENTATION`, `VERIFICATION`, `ENGINEERING_COMPLETE` |
| Process state transition methods | `start_investigation()`, `begin_implementation()`, `begin_verification()`, `recognize_engineering_completion()`, `reconsider()` |
| `ProcessInstance.lifecycle` writes | **None.** No method assigns to `self.process_instance.lifecycle` |
| Suspension operation | **Not present.** No `suspend()` or equivalent method |
| Resumption operation | **Not present.** No `resume()`, `resume_pending()`, or `continue_execution()` method |
| Lifecycle termination operation | **Not present.** No `terminate()` or `terminate_process()` method |
| `stop()` behavior | Sets `self.attached = False`, `self.process_instance = None`, `self.context = None`. No persistence write. No history event. |
| `attach()` behavior | Loads persisted `ProcessInstance` and `ExecutionContext` from store; sets `attached = True` |

**Critical implementation observation:** The string `"self.process_instance.lifecycle"` does not appear as a write target anywhere in `runtime.py`. The `_set_state()` method writes only to `self.context.process_state`.

### 5.3 `runtime/core/store.py`

| Aspect | Finding |
|---|---|
| Instance persistence | Written once at `create()`. No `save_instance()` or `update_instance()` method exists. |
| Context persistence | Written at `create()` and updated via `save_context()` on every state transition. |
| History persistence | Append-only JSONL via `save_context()` events and initial `process_created` event. |
| Versioning | `context.version` is incremented on every `save_context()` call. |
| ProcessInstance update | **Not supported.** `ProcessStore` can load instances but has no method to save changes to a `ProcessInstance` after initial creation. |

**Critical structural observation:** Even if `Runtime` were to change `ProcessInstance.lifecycle`, the `ProcessStore` has no mechanism to persist that change. The instance is write-once at creation time.

### 5.4 Available Runtime Methods

Complete enumerated surface (excluding private methods):

```
attach, begin_implementation, begin_verification, create_process, observe,
recognize_decision, recognize_engineering_completion, reconsider,
record_artifact, record_verification, set_pending_execution, start_investigation, stop
```

### 5.5 Existing Test Coverage

#### `tests/continuity/test_runtime_recovery.py` (8 tests)

| Test | Coverage |
|---|---|
| `test_process_instance_creation` | Asserts `lifecycle == "active"` at creation |
| `test_execution_context_contains_minimum_authoritative_information` | Asserts initial context defaults |
| `test_execution_context_round_trip_preserves_semantic_state` | Validates serialization/deserialization fidelity |
| `test_process_and_context_survive_runtime_replacement` | Validates cross-runtime recovery with pending execution |
| `test_decision_requires_explicit_recognition` | Validates decision gating |
| `test_engineering_completion_requires_explicit_recognition` | Validates completion gating and process_state change |
| `test_missing_context_fails_recovery` | Validates error on missing persistence |
| `test_history_is_preserved` | Validates history event recording |

#### `tests/lifecycle/test_runtime_lifecycle.py` (4 tests)

| Test | Coverage |
|---|---|
| `test_required_lifecycle_transitions` | Validates `initial → investigation → implementation → verification → engineering_complete` |
| `test_transition_conditions_are_enforced` | Validates state guards and preconditions |
| `test_failed_verification_preserves_failure_and_reopens_investigation` | Validates reconsideration loop |
| `test_completion_cannot_bypass_verification` | Validates completion requires passed verification |

**Observation about existing tests:** No existing test asserts a change to `ProcessInstance.lifecycle`. The only existing assertion about `lifecycle` is that it equals `"active"` at creation. No test exercises suspension, resumption, or lifecycle termination as distinct operations.

---

## 6. Experimental Procedure

### Phase 1: Process Instance Creation
Create a Process Instance via `Runtime.create_process()`. Capture initial state from both memory and persistence.

### Phase 2: Advance to Controlled Target
Progress the process through `investigation → implementation` with evidence, decisions, artifacts, and pending execution recorded.

### Phase 3: Baseline State Capture
Capture comprehensive state before lifecycle operations.

### Phase 4: Suspension Experiment
Inspect Runtime surface for any suspension-related method or lifecycle mutation operation.

### Phase 5: Runtime Termination Experiment
Execute `Runtime.stop()`. Capture pre/post state from both memory and persistence. Determine what changed.

### Phase 6: Recovery and Resumption Experiment
Create new Runtime, attach to same Process Instance. Verify state recovery. Test for resumption mechanism.

### Phase 7: Engineering Completion Experiment
Complete a full process cycle to `engineering_complete`. Observe lifecycle, process_state, and engineering_completion changes.

### Phase 8: Lifecycle Termination Check
Determine if any explicit lifecycle termination operation exists after engineering completion.

### Phase 9: Static Mutation Analysis
Verify via source inspection whether any code path writes to `ProcessInstance.lifecycle`.

---

## 7. Baseline State

Captured immediately before lifecycle operations, with the process in `implementation` state:

| Field | In-Memory Value | Persisted Value |
|---|---|---|
| `ProcessInstance.lifecycle` | `"active"` | `"active"` |
| `ProcessInstance.process_instance_id` | UUID | Same UUID |
| `ExecutionContext.process_state` | `"implementation"` | `"implementation"` |
| `ExecutionContext.execution_mode` | `"active"` | `"active"` |
| `ExecutionContext.engineering_completion` | `False` | `False` |
| `ExecutionContext.version` | `6` | `6` |
| `pending_execution` | 1 entry with `next_action` and `resumption_conditions` | Same |
| `Runtime.attached` | `True` | N/A |
| History | 7 entries (`process_created` through `pending_execution_recorded`) | Same |

---

## 8. Observed State Transitions

### 8.1 Process State Transitions (Empirically Validated)

| Before | Operation | After | Evidence Type |
|---|---|---|---|
| `initial` | `create_process()` | `initial` | Runtime + Persistence observation |
| `initial` | `start_investigation()` | `investigation` | Runtime + Persistence observation |
| `investigation` | `begin_implementation()` | `implementation` | Runtime + Persistence observation |
| `implementation` | `begin_verification()` | `verification` | Runtime + Persistence observation |
| `verification` | `recognize_engineering_completion()` | `engineering_complete` | Runtime + Persistence observation |
| `verification` (failed) | `reconsider()` | `investigation` | Existing test evidence |

### 8.2 Process Instance Lifecycle Transitions (Not Observed)

| Before | Operation | After | Evidence Type |
|---|---|---|---|
| `"active"` | `create_process()` | `"active"` | Runtime + Persistence observation |
| `"active"` | (any process state transition) | `"active"` | Runtime + Persistence observation |
| `"active"` | `stop()` | `"active"` | Persistence observation |
| `"active"` | `recognize_engineering_completion()` | `"active"` | Runtime + Persistence observation |

**`ProcessInstance.lifecycle` was never observed to change from `"active"` during any Runtime operation.**

### 8.3 Engineering Completion Transitions (Empirically Validated)

| Field | Before | Operation | After |
|---|---|---|---|
| `process_state` | `"verification"` | `recognize_engineering_completion()` | `"engineering_complete"` |
| `engineering_completion` | `False` | `recognize_engineering_completion()` | `True` |
| `lifecycle` | `"active"` | `recognize_engineering_completion()` | `"active"` (unchanged) |

---

## 9. Persistence Evidence

### 9.1 Context Persistence (Validated)

Every `_set_state()` call triggers `store.save_context()`, which:
1. Increments `context.version`
2. Updates `context.updated_at`
3. Persists context to `context.json` via atomic write (tempfile + `os.replace`)
4. Appends a history event to `history.jsonl` via fsync'd append

**Empirically confirmed:** Persisted state matches in-memory state after every state transition.

### 9.2 Instance Persistence (Validated — Write-Once)

`ProcessInstance` is written once during `store.create()`. No subsequent write path exists.

**Empirically confirmed:** `ProcessStore` methods are `create`, `load_instance`, `load_context`, `save_context`, `history`. No `save_instance` or `update_instance` method exists.

### 9.3 History Persistence (Validated)

History is append-only. Observed event types across experiments:

```
process_created, investigation_started, observation_recorded,
engineering_decision_recognized, implementation_started,
artifact_recorded, pending_execution_recorded, verification_started,
verification_recorded, engineering_completion_recognized
```

**Not observed:** No `runtime_stopped`, `runtime_terminated`, `process_suspended`, `process_resumed`, or `lifecycle_changed` history events exist in any experiment run.

---

## 10. Runtime Lifetime Findings

### 10.1 What happens when Runtime.stop() is called

| Aspect | Observation | Evidence Type |
|---|---|---|
| `runtime.attached` | Set to `False` | Runtime observation |
| `runtime.process_instance` | Set to `None` | Runtime observation |
| `runtime.context` | Set to `None` | Runtime observation |
| Persistence write | **None** | Persistence observation (version unchanged) |
| History event | **None** | History observation (no new entries) |
| `ProcessInstance.lifecycle` change | **None** | Persistence observation |
| `ExecutionContext.process_state` change | **None** | Persistence observation |

**Empirical validation:** `Runtime.stop()` is a purely in-memory detachment operation. It does not record any event, does not persist any state change, and does not modify Process Instance lifecycle or Process State.

### 10.2 Does Runtime termination cause a lifecycle transition?

**No. Empirically validated.**

- `ProcessInstance.lifecycle` before `stop()`: `"active"`
- `ProcessInstance.lifecycle` after `stop()` (read from persistence): `"active"`
- No history event recorded
- No persistence write occurred

`Runtime.stop()` ≠ Process Instance suspended. This is empirically established, not merely inferred from code.

---

## 11. Process Instance Lifecycle Findings

### 11.1 Initial lifecycle state

`ProcessInstance.lifecycle` is initialized to `"active"` at creation.

**Evidence:** Runtime observation (in-memory) + Persistence observation (persisted `process.json`).

### 11.2 Suspension operation

**Not demonstrated. No operation exists.**

- `Runtime` has no `suspend()`, `suspend_process()`, or equivalent method.
- No Runtime method writes to `ProcessInstance.lifecycle`.
- The persisted model does not define an enumerated set of lifecycle states.
- `ProcessInstance` has no class-level constants for lifecycle states.

### 11.3 Resumption operation

**Not demonstrated. No operation exists.**

- `Runtime` has no `resume()`, `resume_process()`, or equivalent method.

### 11.4 Lifecycle termination operation

**Not demonstrated. No operation exists.**

- `Runtime` has no `terminate()`, `terminate_process()`, or equivalent method.
- `recognize_engineering_completion()` changes `process_state` to `"engineering_complete"` and `engineering_completion` to `True`, but does **not** change `ProcessInstance.lifecycle`.

### 11.5 Can `ProcessInstance.lifecycle` transition during Runtime operation?

**No. Empirically validated.**

- **Static evidence:** `"self.process_instance.lifecycle"` does not appear as a write target in `runtime.py`.
- **Structural evidence:** `ProcessStore` has no `save_instance()` method, so even an in-memory lifecycle change could not be persisted.
- **Runtime evidence:** `ProcessInstance.lifecycle` remained `"active"` across all operations: creation, investigation, implementation, verification, engineering completion, stop, recovery.

### 11.6 Does the persisted model represent lifecycle states?

The model **represents** a `lifecycle` field (type `str`, default `"active"`), but:

- Does **not** define an enumeration of valid lifecycle states.
- Does **not** provide constants for lifecycle values (unlike `process_state`, which has Runtime class constants).
- Does **not** constrain the field to any particular set of values.

The field's existence implies lifecycle is a modeled concept, but its operational semantics are not implemented.

---

## 12. Process State Findings

### 12.1 How does `process_state` change during normal execution?

`ExecutionContext.process_state` follows a managed state machine:

```
initial → investigation → implementation → verification → engineering_complete
                ↑                                    |
                └──── reconsider (on failed verification)
```

Each transition is guarded by `_require_state()` checks and semantic preconditions (e.g., decisions required before implementation, artifacts before verification, passed verification before completion).

**Evidence type:** Empirical validation across all phases.

### 12.2 Are Process Instance lifecycle and Process State empirically independent?

**Yes. Empirically validated.**

- `ProcessInstance.lifecycle` remained `"active"` throughout all `process_state` transitions.
- `process_state` transitioned through 5 states while `lifecycle` remained constant.
- They exist on different model objects (`ProcessInstance` vs `ExecutionContext`).
- Different persistence paths: instance is write-once; context is updated on every state change.

### 12.3 Does engineering completion modify lifecycle, Process State, or both?

| Field | Changed? | Before | After | Evidence |
|---|---|---|---|---|
| `process_state` | **Yes** | `"verification"` | `"engineering_complete"` | Runtime + Persistence |
| `engineering_completion` | **Yes** | `False` | `True` | Runtime + Persistence |
| `lifecycle` | **No** | `"active"` | `"active"` | Runtime + Persistence |

---

## 13. Engineering Completion Findings

### 13.1 Engineering Completion (Step A)

**Empirically validated.** `recognize_engineering_completion()` was exercised.

| Observation | Result |
|---|---|
| `process_state` before | `"verification"` |
| `process_state` after | `"engineering_complete"` |
| `engineering_completion` before | `False` |
| `engineering_completion` after | `True` |
| `lifecycle` before | `"active"` |
| `lifecycle` after | `"active"` (unchanged) |
| History event recorded | `engineering_completion_recognized` |
| Context version incremented | Yes (7 → 8) |

Engineering completion is an `ExecutionContext` state change. It does **not** constitute a `ProcessInstance` lifecycle transition.

### 13.2 Process Instance Lifecycle Termination (Step B)

**Not demonstrated. No operation exists.**

- No Runtime method transitions `ProcessInstance.lifecycle` to any terminal value.
- `recognize_engineering_completion()` does not change `lifecycle`.
- `Runtime.stop()` does not change `lifecycle`.
- No `ProcessStore` method can persist a `lifecycle` change after creation.

**Conclusion:** Engineering completion (`engineering_complete`) and Process Instance lifecycle termination are distinct concepts. The implementation represents engineering completion but does not implement lifecycle termination.

---

## 14. Recovery and Resumption Findings

### 14.1 Discovery and State Recovery

**Empirically validated.** A new `Runtime("runtime-beta")` successfully attached to the same Process Instance via `runtime_b.attach(pid)`.

| Aspect | Recovered? | Evidence |
|---|---|---|
| Process Instance identity | **Yes** | `process_instance_id` matches original |
| Engineering objective | **Yes** | `"Validate lifecycle semantics"` preserved |
| `lifecycle` | **Yes** | `"active"` (unchanged, but recoverable) |
| `process_state` | **Yes** | `"implementation"` preserved |
| `execution_mode` | **Yes** | `"active"` preserved |
| Evidence observations | **Yes** | 1 entry preserved |
| Engineering decisions | **Yes** | 1 entry preserved |
| Artifacts | **Yes** | 1 entry preserved |
| `pending_execution` | **Yes** | 1 entry with `next_action` and `resumption_conditions` preserved |
| History | **Yes** | All 7 entries available |
| Context version | **Yes** | Version 6 preserved |

### 14.2 Operational Continuity After Recovery

The recovered Runtime can continue operations in the same `process_state`:

- `runtime_b.record_artifact()` succeeded in `implementation` state.
- `runtime_b` recorded a new artifact with version increment (6 → 7).
- `begin_verification()` was correctly blocked by remaining `pending_execution`.

### 14.3 Pending Execution Survival

**Empirically validated.** Pending execution with `next_action` and `resumption_conditions` survives:

1. `Runtime.stop()` (tested — pending execution present in persisted state after stop)
2. New Runtime attachment (tested — pending execution loaded by `runtime_b`)

### 14.4 Pending Execution Resumption

**Not demonstrated. No resumption mechanism exists.**

- `Runtime` has no `resume_pending()`, `continue_execution()`, or `execute_pending()` method.
- Pending execution items remain in the list after recovery. They are not automatically processed.
- The Runtime enforces that `begin_verification()` requires no pending execution, which means pending items must be manually addressed, but the Runtime provides no explicit operation for this.
- Pending execution entries are **recoverable** and **discoverable** but not **resumable** through any Runtime operation.

### 14.5 What happens to `pending_execution` after work is completed?

**Not demonstrated.** The Runtime does not provide an explicit operation to mark a pending execution item as completed or to remove it from the list. The `set_pending_execution()` method only appends new items. The `begin_implementation()` method clears the list when entering implementation state, but this is a state initialization, not a completion acknowledgment.

### 14.6 Distinction: Discovery vs Recovery vs Resumption

| Concept | Demonstrated? | Evidence |
|---|---|---|
| **Discovery** of a Process Instance | **Yes** | `store.load_instance(pid)` successfully returns the persisted instance |
| **Recovery** of persisted state | **Yes** | `runtime_b.attach(pid)` loads complete context including pending execution |
| **Resumption** of pending work | **No** | No Runtime operation exists to process, execute, or clear pending execution items |

---

## 15. Evidence Matrix

| # | Semantic Question | Required Evidence | Observed Evidence | Result | Classification | Notes |
|---|---|---|---|---|---|---|
| 1 | Initial lifecycle state of Process Instance | Runtime + Persistence observation at creation | `lifecycle == "active"` in memory and persisted `process.json` | `"active"` | **Validated** | Confirmed by both experiment and existing test `test_process_instance_creation` |
| 2 | Explicit suspension operation exists | Runtime surface inspection + attempted execution | No `suspend()` method; no method writes `ProcessInstance.lifecycle` | Not present | **Representation Gap** | `lifecycle` field exists but no suspension state or operation is defined |
| 3 | Explicit resumption operation exists | Runtime surface inspection + attempted execution | No `resume()` method | Not present | **Representation Gap** | Pending execution is recoverable but not resumable through any explicit operation |
| 4 | Explicit termination operation exists | Runtime surface inspection + attempted execution | No `terminate()` method; no method writes `ProcessInstance.lifecycle` | Not present | **Representation Gap** | Neither `stop()` nor `recognize_engineering_completion()` changes lifecycle |
| 5 | `ProcessInstance.lifecycle` can transition during Runtime operation | Lifecycle value comparison before/after all operations | `lifecycle` remained `"active"` across 9 distinct operations including creation, all state transitions, stop, and recovery | Cannot transition | **Representation Gap** | Structural cause: no Runtime method writes lifecycle; no ProcessStore method persists instance changes |
| 6 | Persisted model represents required lifecycle states | Model inspection | Single `str` field, default `"active"`, no constants/enum for valid states | Partially represented | **Representation Gap** | The field exists but valid state values are not defined or constrained |
| 7 | `process_state` changes during normal execution | Runtime + Persistence observation across transitions | `initial → investigation → implementation → verification → engineering_complete` all observed and persisted | Full state machine validated | **Validated** | All transitions confirmed with version increments and history events |
| 8 | Lifecycle and Process State are empirically independent | Concurrent observation of both values | `lifecycle` constant while `process_state` changed 5 times | Independent | **Validated** | Different model objects, different persistence mechanisms |
| 9 | Engineering completion modifies lifecycle, process_state, or both | Pre/post comparison of all three fields | `process_state`: changed; `engineering_completion`: changed; `lifecycle`: unchanged | Modifies process_state and engineering_completion only | **Validated** | Engineering completion ≠ lifecycle termination |
| 10 | What happens to Process Instance and Context when Runtime stops | Persistence inspection after `stop()` | Both remain fully persisted; no state changes; no history event | Persisted state unchanged | **Validated** | `stop()` is purely in-memory detachment |
| 11 | Runtime termination causes lifecycle transition | Pre/post lifecycle comparison across `stop()` | `lifecycle == "active"` before and after | No transition | **Validated** | `stop()` ≠ suspension |
| 12 | Another Runtime can recover the same Process Instance | New Runtime attachment + state comparison | `runtime_b.attach(pid)` succeeded; all state recovered | Recovery validated | **Validated** | Identity, context, evidence, decisions, artifacts, pending execution all preserved |
| 13 | Pending execution survives Runtime termination | Persistence inspection after `stop()` | `pending_execution` with `next_action` and `resumption_conditions` present in persisted context | Survives | **Validated** | 1 entry with full structure confirmed |
| 14 | Pending execution can be resumed | Resumption method existence + execution | No `resume_pending()` or equivalent method | Not demonstrated | **Representation Gap** | Pending execution is discoverable and recoverable but not resumable |
| 15 | What happens to `pending_execution` after completion | Post-completion observation | No explicit clear/complete operation; `begin_implementation()` clears list as initialization | No completion mechanism | **Evidence Gap** | Items can be appended but not individually completed or removed |

---

## 16. Gap Classification

### Gap 1: Process Instance Lifecycle Operations Not Implemented

**Expected:** Explicit operations for suspending, resuming, and terminating a Process Instance, operating on `ProcessInstance.lifecycle`.

**Evidence:** The `lifecycle` field exists on `ProcessInstance` with a default of `"active"`. However:
- No Runtime method writes to `ProcessInstance.lifecycle`.
- No `ProcessStore` method persists changes to `ProcessInstance` after creation.
- No constants, enums, or defined set of valid lifecycle states exist.

**Insufficiency:** The `lifecycle` field is represented but inert. Its value is set at construction and never subsequently changed by any operation.

**Layer:** Implementation gap. The model represents the concept; the Runtime does not operationalize it.

**Further validation required:** Determine whether PEM specification defines the expected lifecycle states and transitions. If so, this is a Representation Gap at the implementation level. If not, this is a Model/Specification gap that should be resolved before implementation.

### Gap 2: Pending Execution Resumption Not Implemented

**Expected:** A mechanism to resume, execute, or acknowledge completion of pending work items.

**Evidence:** `pending_execution` entries survive Runtime termination and are fully recoverable. The `begin_verification()` guard correctly blocks advancement when pending items exist. However:
- No method processes or removes individual pending execution items.
- No method marks pending items as completed.
- `set_pending_execution()` only appends.

**Insufficiency:** The lifecycle progression is blocked by pending execution, but no legitimate path to clear it exists within the Runtime surface (other than `begin_implementation()` clearing the entire list when entering implementation state, which is state initialization, not resumption).

**Layer:** Implementation gap. The pending execution data model supports continuity, but the operational semantics for resumption are not implemented.

**Further validation required:** Determine whether the pending execution lifecycle (creation → recovery → resumption → completion) should be explicitly managed by the Runtime or left to external orchestration.

### Gap 3: ProcessInstance Write-Once Persistence

**Expected:** The ability to persist changes to `ProcessInstance` fields (particularly `lifecycle`) after initial creation.

**Evidence:** `ProcessStore.create()` writes both `process.json` and `context.json`. Subsequently, only `save_context()` exists—it saves `context.json` and appends to `history.jsonl`. There is no `save_instance()` or `update_instance()` method.

**Insufficiency:** Even if a Runtime method were to change `ProcessInstance.lifecycle` in memory, the change could not be persisted. This is a structural blocker for any lifecycle transition implementation.

**Layer:** Persistence layer gap, prerequisite for lifecycle implementation.

### Gap 4: Runtime Stop Does Not Record History

**Expected:** `Runtime.stop()` might record a history event indicating Runtime detachment.

**Evidence:** `stop()` sets three in-memory fields and returns. No `store.save_context()` call. No history event appended. The last history event before and after `stop()` is identical.

**Insufficiency:** Runtime attachment and detachment are invisible in the persisted history. A future diagnostic or audit tool cannot determine when Runtime sessions began or ended.

**Layer:** Implementation design consideration. Whether `stop()` should record a history event is a design decision, not necessarily a defect.

---

## 17. Epistemic Assessment

The following statements are established with the evidence type indicated:

### The implementation supports X

- ✅ The implementation supports **process state transitions** through a managed state machine with guards and preconditions. (Empirical validation)
- ✅ The implementation supports **engineering completion recognition** with explicit recognition gating. (Empirical validation)
- ✅ The implementation supports **cross-runtime Process Instance recovery** via `attach()`. (Empirical validation)
- ✅ The implementation supports **pending execution persistence** across Runtime boundaries. (Empirical validation)
- ❌ The implementation does **not** support Process Instance lifecycle state transitions. (Empirical validation — negative)
- ❌ The implementation does **not** support Process Instance suspension, resumption, or lifecycle termination. (Empirical validation — negative)
- ❌ The implementation does **not** support pending execution resumption as an explicit operation. (Empirical validation — negative)

### The implementation represents X

- ✅ The implementation **represents** a Process Instance lifecycle concept via `ProcessInstance.lifecycle`. (Static implementation evidence)
- ✅ The implementation **represents** pending execution with `next_action` and `resumption_conditions`. (Static implementation evidence + Runtime observation)
- ❌ The implementation does **not** represent an enumerated set of valid lifecycle states. (Static implementation evidence — negative)

### The experiment demonstrated X

- ✅ `ProcessInstance.lifecycle` never changes from `"active"` during any observed Runtime operation. (Empirical validation)
- ✅ `Runtime.stop()` does not cause a Process Instance lifecycle transition. (Empirical validation)
- ✅ `Runtime.stop()` does not persist any state or history. (Empirical validation)
- ✅ Engineering completion changes `process_state` and `engineering_completion` but not `lifecycle`. (Empirical validation)
- ✅ Pending execution survives Runtime termination and is recoverable. (Empirical validation)
- ✅ A new Runtime can discover and attach to a persisted Process Instance. (Empirical validation)
- ✅ `begin_verification()` correctly enforces that pending execution must be resolved. (Empirical validation)

### The experiment did NOT demonstrate X

- ❌ Process Instance suspension. (No operation exists)
- ❌ Process Instance resumption. (No operation exists)
- ❌ Process Instance lifecycle termination. (No operation exists)
- ❌ Pending execution resumption. (No operation exists)
- ❌ Pending execution completion acknowledgment. (No operation exists)

---

## 18. Conclusions

### Primary Finding

The AESM implementation distinguishes between **Process Instance lifecycle** and **Execution Context process state** at the model level, but only **process state** is operationally implemented. `ProcessInstance.lifecycle` is a represented-but-inert field that remains `"active"` throughout the entire existence of a Process Instance, regardless of what operations are performed.

### Secondary Findings

1. **The process state machine is well-implemented and validated.** Transitions are guarded, persisted, versioned, and historically recorded. The state machine includes a reconsideration loop for failed verification.

2. **Cross-runtime continuity is operational.** Process Instances survive Runtime termination and are fully recoverable by new Runtime instances, including pending execution, evidence, decisions, artifacts, and history.

3. **Pending execution is a continuity mechanism without resumption semantics.** Items can be recorded, persisted, and recovered, but the Runtime provides no operation to process, resume, or complete them. The `begin_verification()` guard correctly prevents advancement past unresolved pending work.

4. **Engineering completion is an Execution Context state transition, not a Process Instance lifecycle event.** This distinction is empirically demonstrated: `lifecycle` remains `"active"` after `recognize_engineering_completion()`.

5. **`Runtime.stop()` is semantically silent.** It is a pure in-memory cleanup that does not record any event, persist any change, or transition any state. It is not equivalent to suspension.

### Structural Observation

The lifecycle gap has two layers:
- **No Runtime operation modifies `ProcessInstance.lifecycle`.**
- **No `ProcessStore` method can persist changes to `ProcessInstance` after creation.**

Both layers must be addressed to implement lifecycle transitions.

---

## 19. Recommendations

> **Note:** These recommendations arise from experimental findings. They are not implementations or specification changes.

1. **Define the Process Instance lifecycle state set.** The `lifecycle` field exists but has no defined valid states, no constants, and no constraints. Before implementing lifecycle operations, the valid states and their transition rules should be specified.

2. **Add `ProcessStore.save_instance()`.** Lifecycle transitions cannot be persisted without a method to update `ProcessInstance` after creation. This is a structural prerequisite.

3. **Design lifecycle operations as distinct from process state.** The experiment confirms that lifecycle and process state are independent. Suspension should not be conflated with `stop()`, and completion should not be conflated with lifecycle termination.

4. **Design pending execution lifecycle.** Pending execution items need an explicit lifecycle: creation → recovery → resumption → completion. Currently, only creation and recovery are implemented.

5. **Consider recording Runtime attachment/detachment in history.** Currently, `stop()` and `attach()` are invisible in history. Recording these events would provide audit capability and enable diagnostic analysis.

---

## Appendix A: Test Execution Results

### Pre-experiment (baseline)

```
12 passed in 0.17s
```

All tests in `tests/continuity/test_runtime_recovery.py` (8) and `tests/lifecycle/test_runtime_lifecycle.py` (4) passed.

### Post-experiment

```
12 passed in 0.12s
```

All tests passed. No test results changed. No existing tests were modified.

### Experimental artifacts

The experiment was conducted via a temporary script that created Process Instances in `tempfile.TemporaryDirectory` locations. No persistent experiment data remains in the project tree. The experiment script is preserved as an experimental artifact.

---

## Appendix B: Evidence Capture Detail

### B.1 Runtime.stop() Evidence Capture

| Field | Before `stop()` | After `stop()` (Persisted) | Changed? |
|---|---|---|---|
| `ProcessInstance.lifecycle` | `"active"` | `"active"` | No |
| `ExecutionContext.process_state` | `"implementation"` | `"implementation"` | No |
| `ExecutionContext.execution_mode` | `"active"` | `"active"` | No |
| `ExecutionContext.engineering_completion` | `False` | `False` | No |
| `ExecutionContext.version` | `6` | `6` | No |
| `pending_execution` count | 1 | 1 | No |
| History entry count | 7 | 7 | No |
| Last history event type | `pending_execution_recorded` | `pending_execution_recorded` | No |

### B.2 Engineering Completion Evidence Capture

| Field | Before `recognize_engineering_completion()` | After | Changed? |
|---|---|---|---|
| `ProcessInstance.lifecycle` | `"active"` | `"active"` | No |
| `ExecutionContext.process_state` | `"verification"` | `"engineering_complete"` | **Yes** |
| `ExecutionContext.engineering_completion` | `False` | `True` | **Yes** |
| `ExecutionContext.version` | `7` | `8` | **Yes** |
| History entry count | 8 | 9 | **Yes** |
| Last history event type | `verification_recorded` | `engineering_completion_recognized` | **Yes** |

### B.3 Cross-Runtime Recovery Evidence Capture

| Aspect | Original (runtime-alpha) | Recovered (runtime-beta) | Match? |
|---|---|---|---|
| `process_instance_id` | UUID | Same UUID | ✅ |
| `engineering_objective` | `"Validate lifecycle semantics"` | Same | ✅ |
| `lifecycle` | `"active"` | `"active"` | ✅ |
| `process_state` | `"implementation"` | `"implementation"` | ✅ |
| `execution_mode` | `"active"` | `"active"` | ✅ |
| `engineering_completion` | `False` | `False` | ✅ |
| `version` | `6` | `6` | ✅ |
| Evidence count | 1 | 1 | ✅ |
| Decision count | 1 | 1 | ✅ |
| Artifact count | 1 | 1 | ✅ |
| `pending_execution` count | 1 | 1 | ✅ |
| `pending_execution[0].next_action` | `"complete lifecycle validation"` | Same | ✅ |
| `pending_execution[0].resumption_conditions` | `["runtime recovery demonstrated", ...]` | Same | ✅ |
| History count | 7 | 7 | ✅ |
