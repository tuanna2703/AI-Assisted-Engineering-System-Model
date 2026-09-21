# Multi-Project Behavioral Validation

## Status

**EXECUTED — GATE: Conformant — Demonstrated**

---

## Terminology and Scope Clarification

This artifact records a **Behavioral Multi-Project Isolation Validation** executed against
the real AESM Runtime, ProcessStore, and AgentRuntimeBridge implementation via pytest.

**This is not Agent-boundary empirical validation.**  Agent-boundary empirical validation
requires a live AI Agent session, real IDE integration, and end-to-end environment
participation.  That work is recorded separately.

This validation determines whether the existing AESM Runtime implementation correctly
preserves independent Engineering Scope Identity and Process Instance state across multiple
projects/scopes.  "Behavioral validation" in this context means executing prepared test
scenarios against the real Runtime/persistence implementation through pytest, with assertions
over real in-memory and persisted state.

---

## Validation Objective

Demonstrate that the existing implementation can maintain independent authoritative scope
state for multiple Process Instances without:

- silently rebinding an established Process Instance;
- confusing one project with another;
- leaking scope state between Process Instances;
- depending on Runtime session memory for recovery;
- turning unresolved scope into inferred scope;
- introducing a second authority mechanism.

---

## Repository Revision

| Field        | Value                                                      |
| ------------ | ---------------------------------------------------------- |
| Branch       | `main`                                                     |
| HEAD revision| `ed7e8980522c336862bb5c732a1134a2df9a6af5`                 |
| Working tree | **Clean** — no uncommitted modifications at execution time |
| Last commit  | `plan: advance multi-project empirical validation gate`    |

---

## Execution Environment

| Component         | Observed Value                    |
| ----------------- | --------------------------------- |
| Platform          | darwin (macOS)                    |
| Python (system)   | Python 3.13.5                     |
| Python (.venv)    | Python 3.13.5                     |
| pytest            | pytest 9.1.1 / pluggy 1.6.0       |
| Virtual environment | `.venv/` present at repo root   |
| PYTHONPATH        | `.` (repo root)                   |

---

## Participating Scope Identities

These are stable experimental Engineering Scope Identity strings, not normative repository
equivalences.

| Label     | Engineering Scope Identity                                     |
| --------- | -------------------------------------------------------------- |
| Project A | `project:tuanna2703/directories-builder-pro`                   |
| Project B | `project:tuanna2703/AI-Assisted-Engineering-System-Model`      |

---

## Test-Function Mapping Verification

The test file `tests/multi_project/test_multi_project_scope_isolation.py` was inspected
prior to execution.  All nine test functions are present and match the authorised mapping
exactly.

| Scenario                                      | Test function                                                              | Mapping status        |
| --------------------------------------------- | -------------------------------------------------------------------------- | --------------------- |
| Independent projects                          | `test_two_distinct_projects_remain_isolated`                               | ✓ Present, matches    |
| Multiple Process Instances within one project | `test_two_process_instances_in_one_project_remain_independent`             | ✓ Present, matches    |
| Project switching                             | `test_switching_projects_does_not_rebind_the_first_process`                | ✓ Present, matches    |
| Conflicting rebinding                         | `test_conflicting_rebinding_is_rejected_and_persistence_remains_project_a` | ✓ Present, matches    |
| Independent unresolved/ambiguous state        | `test_unresolved_and_ambiguous_processes_independent`                      | ✓ Present, matches    |
| Cross-instance contamination                  | `test_unresolved_state_does_not_acquire_scope_from_another_project`        | ✓ Present, matches    |
| Agent → Bridge → Runtime authority            | `test_bridge_preserves_independent_authority_for_two_projects`             | ✓ Present, matches    |
| Bridge-level conflicting binding              | `test_bridge_rejects_conflicting_scope_without_mutating_authoritative_state` | ✓ Present, matches  |
| Fresh Runtime recovery                        | `test_recovery_after_project_switch_uses_persisted_scope_not_runtime_session` | ✓ Present, matches |

---

## Commands Executed

### Targeted Multi-Project Suite

```
PYTHONPATH=. .venv/bin/pytest -v \
  tests/multi_project/test_multi_project_scope_isolation.py
```

### Regression Suite

```
PYTHONPATH=. .venv/bin/pytest -v \
  tests/project_identity/test_scope_binding.py \
  tests/lifecycle/test_runtime_lifecycle.py \
  tests/continuity/test_runtime_recovery.py \
  tests/multi_project/test_multi_project_scope_isolation.py
```

---

## Targeted Test Results

**Executed:** 2026-09-19 (UTC+7, local execution time ~09:55)

```
platform darwin -- Python 3.13.5, pytest-9.1.1, pluggy-1.6.0
collected 9 items

tests/multi_project/test_multi_project_scope_isolation.py::test_two_distinct_projects_remain_isolated PASSED
tests/multi_project/test_multi_project_scope_isolation.py::test_two_process_instances_in_one_project_remain_independent PASSED
tests/multi_project/test_multi_project_scope_isolation.py::test_switching_projects_does_not_rebind_the_first_process PASSED
tests/multi_project/test_multi_project_scope_isolation.py::test_conflicting_rebinding_is_rejected_and_persistence_remains_project_a PASSED
tests/multi_project/test_multi_project_scope_isolation.py::test_unresolved_and_ambiguous_processes_remain_independent PASSED
tests/multi_project/test_multi_project_scope_isolation.py::test_unresolved_state_does_not_acquire_scope_from_another_project PASSED
tests/multi_project/test_multi_project_scope_isolation.py::test_bridge_preserves_independent_authority_for_two_projects PASSED
tests/multi_project/test_multi_project_scope_isolation.py::test_bridge_rejects_conflicting_scope_without_mutating_authoritative_state PASSED
tests/multi_project/test_multi_project_scope_isolation.py::test_recovery_after_project_switch_uses_persisted_scope_not_runtime_session PASSED

============================== 9 passed in 0.24s ==============================
```

| Metric         | Count |
| -------------- | ----- |
| Collected      | 9     |
| Passed         | 9     |
| Failed         | 0     |
| Errors         | 0     |
| Skipped        | 0     |
| Warnings       | 0     |

---

## Regression Test Results

```
platform darwin -- Python 3.13.5, pytest-9.1.1, pluggy-1.6.0
collected 41 items

tests/project_identity/test_scope_binding.py               13 passed
tests/lifecycle/test_runtime_lifecycle.py                   7 passed
tests/continuity/test_runtime_recovery.py                  12 passed
tests/multi_project/test_multi_project_scope_isolation.py   9 passed

============================== 41 passed in 0.53s ==============================
```

| Suite                                        | Collected | Passed | Failed | Errors |
| -------------------------------------------- | --------- | ------ | ------ | ------ |
| `test_scope_binding.py`                      | 13        | 13     | 0      | 0      |
| `test_runtime_lifecycle.py`                  | 7         | 7      | 0      | 0      |
| `test_runtime_recovery.py`                   | 12        | 12     | 0      | 0      |
| `test_multi_project_scope_isolation.py`      | 9         | 9      | 0      | 0      |
| **Total**                                    | **41**    | **41** | **0**  | **0**  |

No regressions introduced by the multi-project validation coverage.

---

## Scenario-by-Scenario Observations

### Persistence Note

All tests use pytest's `tmp_path` fixture.  Each test receives an isolated temporary
`ProcessStore`; the temporary filesystem is not available for post-test manual inspection
after pytest completes.  Persistence assertions performed within the tests via
`store.load_instance()` and `store.history()` are the valid persistence evidence recorded here.

---

### Scenario 1 — Independent Projects

**Test:** `test_two_distinct_projects_remain_isolated`
**Result:** PASSED

**Planned invariant:** Process A → Project A; Process B → Project B.  Process Instance
identities, scope identities, state, and persisted state must remain independent.

**Observed:** The test creates two Process Instances against a shared store.  Each receives
an independent scope resolution.  The test then directly asserts persisted state via
`store.load_instance()` and history via `store.history()[-1]`.

**Persistence assertions established by the test:**
- `persisted_a.engineering_scope_identity == PROJECT_A`
- `persisted_b.engineering_scope_identity == PROJECT_B`
- `persisted_a.process_instance_id != persisted_b.process_instance_id`
- `store.history(process_a)[-1]["resulting_identity"] == PROJECT_A`
- `store.history(process_b)[-1]["resulting_identity"] == PROJECT_B`

**Classification:** Conformant — Demonstrated

---

### Scenario 2 — Multiple Process Instances Within One Project

**Test:** `test_two_process_instances_in_one_project_remain_independent`
**Result:** PASSED

**Planned invariant:** Two Process Instances A and B both bound to Project A must remain
distinct (different Process Instance identities) with independently scoped histories.

**Observed:** Both instances resolve to Project A.  History entries carry per-instance IDs.

**Persistence assertions established by the test:**
- `persisted_a.engineering_scope_identity == PROJECT_A`
- `persisted_b.engineering_scope_identity == PROJECT_A`
- `persisted_a.process_instance_id != persisted_b.process_instance_id`
- All entries in `store.history(process_a)` carry `process_instance_id == process_a`
- All entries in `store.history(process_b)` carry `process_instance_id == process_b`

**Classification:** Conformant — Demonstrated

---

### Scenario 3 — Project Switching

**Test:** `test_switching_projects_does_not_rebind_the_first_process`
**Result:** PASSED

**Planned invariant:** After binding Process A to Project A, stopping the Runtime, binding
Process B to Project B, then recovering Process A in a fresh Runtime — Process A must still
resolve to Project A.

**Observed:** A fresh `Runtime(store, "recovery-a")` is attached to `process_a`.  The
recovered in-memory and persisted state both expose Project A.  Project B is not involved.

**Recovery assertions established by the test:**
- `recovered_a.process_instance.engineering_scope_identity == PROJECT_A`
- `store.load_instance(process_a).engineering_scope_identity == PROJECT_A`
- `store.load_instance(process_b).engineering_scope_identity == PROJECT_B`

**Classification:** Conformant — Demonstrated

---

### Scenario 4 — Conflicting Rebinding

**Test:** `test_conflicting_rebinding_is_rejected_and_persistence_remains_project_a`
**Result:** PASSED

**Planned invariant:** Attempting to rebind Process A (already bound to Project A) to
Project B must be rejected.  In-memory and persisted binding must remain Project A.  No
additional successful binding history entry may be created.

**Observed:** `apply_scope_resolution(resolved_scope(PROJECT_B))` raises
`RuntimeError` matching `"cannot be silently replaced"`.

**In-memory state after rejection (asserted):**
- `in_memory.engineering_scope_identity == PROJECT_A`
- `in_memory.engineering_scope_resolution == "RESOLVED"`

**Persisted state after rejection (asserted):**
- `persisted.engineering_scope_identity == PROJECT_A`
- `persisted.engineering_scope_resolution == "RESOLVED"`

**History count (asserted):**
- `store.history_entry_count(process_a) == prior_history_count` — the rejection produced no
  new history entry.

**Implementation mechanism observed:** `runtime.apply_scope_resolution()` checks
`current_status == "RESOLVED"` before mutating any state.  If status is already RESOLVED
and the new identity differs, it raises before any in-memory or store mutation occurs.
The rollback guard in the store's `save_process_instance` therefore is not even reached for
the rejection path.

**Classification:** Conformant — Demonstrated

---

### Scenario 5 — Independent Unresolved and Ambiguous State

**Test:** `test_unresolved_and_ambiguous_processes_remain_independent`
**Result:** PASSED

**Planned invariant:** Process Instances in UNRESOLVED and AMBIGUOUS resolution states must
each retain their respective statuses and must contain no authoritative scope identity.

**Observed:** Two instances receive explicit non-resolved resolutions.  Persisted state is
inspected directly.

**Persistence assertions established by the test:**
- `unresolved.engineering_scope_resolution == "UNRESOLVED"`
- `unresolved.engineering_scope_identity is None`
- `ambiguous.engineering_scope_resolution == "AMBIGUOUS"`
- `ambiguous.engineering_scope_identity is None`

**Classification:** Conformant — Demonstrated

---

### Scenario 6 — Cross-Instance Contamination

**Test:** `test_unresolved_state_does_not_acquire_scope_from_another_project`
**Result:** PASSED

**Planned invariant:** An UNRESOLVED Process Instance must not acquire the scope identity
of another (resolved) Process Instance, including after independent recovery.

**Observed:** An UNRESOLVED instance and a Project-B-bound instance are both persisted.
Both are independently recovered in separate fresh Runtimes.

**Recovery assertions established by the test:**
- `recovered_unresolved.process_instance.engineering_scope_identity is None`
- `recovered_unresolved.process_instance.engineering_scope_resolution == "UNRESOLVED"`
- `recovered_bound.process_instance.engineering_scope_identity == PROJECT_B`

No scope leaked from the resolved instance to the unresolved instance during any stage.

**Classification:** Conformant — Demonstrated

---

### Scenario 7 — Agent → Bridge → Runtime Authority

**Test:** `test_bridge_preserves_independent_authority_for_two_projects`
**Result:** PASSED

**Planned invariant:** Two independent AgentRuntimeBridge instances each submit scope
resolutions through the authority chain:
`Agent → AgentRuntimeBridge → Runtime → ProcessInstance → ProcessStore`.
Each bridge must affect only its own attached Process Instance.  Persisted state must remain
Process-Instance-specific.

**Observed:** Two Bridge instances (`bridge-a`, `bridge-b`) each create a Process Instance
and dispatch `apply_scope_resolution`.

**Bridge/dispatch result assertions:**
- `result_a["success"] is True`
- `result_b["success"] is True`
- `result_a["process_instance"]["engineering_scope_identity"] == PROJECT_A`
- `result_b["process_instance"]["engineering_scope_identity"] == PROJECT_B`

**Persistence assertions:**
- `store.load_instance(process_a).engineering_scope_identity == PROJECT_A`
- `store.load_instance(process_b).engineering_scope_identity == PROJECT_B`

**Authority chain observation:** Each `AgentRuntimeBridge` wraps its own `Runtime` instance.
The bridge's `dispatch()` routes to `runtime.apply_scope_resolution()`, which is the
Runtime's authority boundary.  ProcessStore receives and persists the binding.  Neither
bridge has independent state authority.

**Classification:** Conformant — Demonstrated

---

### Scenario 8 — Bridge-Level Conflicting Binding

**Test:** `test_bridge_rejects_conflicting_scope_without_mutating_authoritative_state`
**Result:** PASSED

**Planned invariant:** Submitting a conflicting scope through the bridge must return the
Runtime rejection, and authoritative state (both in-memory bridge-exposed state and persisted
state) must remain unchanged.

**Observed:** After a successful binding to Project A, a second dispatch with Project B is
submitted.  The bridge catches the `RuntimeError` from the Runtime and returns an error
response rather than propagating the exception.

**Conflict response assertions:**
- `conflict["success"] is False`
- `conflict["error"]["type"] == "runtime_error"`
- `conflict["process_instance"]["engineering_scope_identity"] == PROJECT_A`

**Persistence assertion:**
- `store.load_instance(process_id).engineering_scope_identity == PROJECT_A`

**Bridge behaviour observed:** `AgentRuntimeBridge.dispatch()` catches
`(RuntimeError, PermissionError)` and returns `_error_response("runtime_error", ...,
runtime=self._runtime)`.  The `_error_response()` helper includes the current (unchanged)
Process Instance state when a runtime is supplied.  This is why the conflict response
carries the authoritative unchanged identity.

**Classification:** Conformant — Demonstrated

---

### Scenario 9 — Fresh Runtime Recovery

**Test:** `test_recovery_after_project_switch_uses_persisted_scope_not_runtime_session`
**Result:** PASSED

**Planned invariant:** After:
1. Runtime A persists Process A → Project A and stops;
2. Runtime B persists Process B → Project B and stops;
3. A fresh Runtime attaches Process A;

the fresh Runtime must obtain Process A's scope from persisted state, not from Runtime-B's
session memory.

**Observed:** Three distinct `Runtime` objects (`runtime-a`, `runtime-b`, `fresh-runtime`)
are used.  The fresh runtime attaches only `process_a` and reads from the store.

**Recovery assertions established by the test:**
- `fresh_runtime.process_instance.process_instance_id == process_a`
- `fresh_runtime.process_instance.engineering_scope_identity == PROJECT_A`
- `fresh_runtime.process_instance.engineering_scope_identity != store.load_instance(process_b).engineering_scope_identity`

**Classification:** Conformant — Demonstrated

---

## Persistence Evidence Summary

All persistence evidence is derived from assertions performed by the tests using
`store.load_instance()` and `store.history()` during test execution against the real
`ProcessStore` with `tmp_path`-isolated directories.

Direct post-test file inspection is not available (pytest `tmp_path` is removed after
session).  This is expected per the governing validation rules; in-test store assertions
are sufficient.

The `ProcessStore` integrity invariants verified by `load_instance()`:
- `lifecycle` must be in `{"active", "suspended", "terminated"}`;
- `engineering_scope_resolution` must be in the valid status set;
- `RESOLVED` status requires a non-empty `engineering_scope_identity`;
- any other status requires `engineering_scope_identity is None`.

These store-level validation guards are exercised by every `load_instance()` call in the
multi-project tests, providing additional implicit evidence that persisted state conforms to
the binding invariant.

---

## Recovery Observations

Fresh Runtime recovery was directly observed in three tests:
- **Scenario 3** (project switching): `Runtime(store, "recovery-a").attach(process_a)` →
  Project A recovered correctly.
- **Scenario 6** (contamination): Two independent fresh Runtimes attached to UNRESOLVED and
  Project-B instances respectively; both recovered correctly without cross-contamination.
- **Scenario 9** (fresh runtime recovery): `Runtime(store, "fresh-runtime").attach(process_a)`
  against a store that also contains a stopped Project-B Runtime's instance → Project A
  recovered from persisted state, not from any remaining session memory.

In all three cases, recovery is implemented by `Runtime.attach()`, which calls
`store.load_instance()` and `store.load_context()`.  The Runtime holds no cross-instance
state.  Session memory from a prior Runtime does not influence recovery.

---

## Known Prior Limitations

### xprocess orchestrator incompatibility

`tests/continuity/xprocess_orchestrator.py` was **not** included in the regression suite
executed for this validation, and its failure is a **pre-existing incompatibility**, not
a regression caused by multi-project work.

The known cause: `xprocess_process_a.py` calls `rt.observe()` without the `recognition`
field that a subsequent implementation made mandatory.

This incompatibility is recorded in prior validation evidence.  It was not re-investigated,
re-classified, or modified for this work.  No new evidence connects it to multi-project
isolation behavior.

---

## Failures and Anomalies

None.  All 9 multi-project tests passed.  All 41 regression tests passed.

No fixture defects were identified.  No test corrections were required.

No implementation gaps were observed.  No stop conditions were triggered.

---

## Evidence Matrix

| Scenario                                 | Test                                                                       | Planned Invariant                                | Observed Outcome | Persistence Evidence | Classification              |
| ---------------------------------------- | -------------------------------------------------------------------------- | ------------------------------------------------ | ---------------- | -------------------- | --------------------------- |
| Independent projects                     | `test_two_distinct_projects_remain_isolated`                               | A→ProjA, B→ProjB, IDs distinct, histories scoped | PASSED           | Yes — store asserted  | Conformant — Demonstrated   |
| Multiple instances / one project         | `test_two_process_instances_in_one_project_remain_independent`             | A≠B; both→ProjA; histories per-ID                | PASSED           | Yes — store asserted  | Conformant — Demonstrated   |
| Project switching                        | `test_switching_projects_does_not_rebind_the_first_process`                | Recovered A → ProjA; B untouched                 | PASSED           | Yes — store asserted  | Conformant — Demonstrated   |
| Conflicting rebinding                    | `test_conflicting_rebinding_is_rejected_and_persistence_remains_project_a` | Rejection raised; state/history unchanged        | PASSED           | Yes — store asserted  | Conformant — Demonstrated   |
| Unresolved/ambiguous independence        | `test_unresolved_and_ambiguous_processes_remain_independent`               | Each status explicit; identity None              | PASSED           | Yes — store asserted  | Conformant — Demonstrated   |
| Cross-instance contamination             | `test_unresolved_state_does_not_acquire_scope_from_another_project`        | UNRESOLVED stays None after recovery             | PASSED           | Yes — store asserted  | Conformant — Demonstrated   |
| Bridge authority (two projects)          | `test_bridge_preserves_independent_authority_for_two_projects`             | Each bridge affects only its instance            | PASSED           | Yes — store asserted  | Conformant — Demonstrated   |
| Bridge conflicting binding               | `test_bridge_rejects_conflicting_scope_without_mutating_authoritative_state` | Conflict returns error; state unchanged        | PASSED           | Yes — store asserted  | Conformant — Demonstrated   |
| Fresh Runtime recovery                   | `test_recovery_after_project_switch_uses_persisted_scope_not_runtime_session` | Fresh Runtime uses persisted, not session, scope | PASSED       | Yes — store asserted  | Conformant — Demonstrated   |

---

## Repository Modification State

| Check              | Result                                                                 |
| ------------------ | ---------------------------------------------------------------------- |
| `git status --short` | (empty — no uncommitted modifications before execution)             |
| `git diff --stat`  | (empty — no uncommitted modifications before execution)                |
| `git log -1 --oneline` | `ed7e898 plan: advance multi-project empirical validation gate`   |

**Files modified by this work unit:**
- `execution/MULTI-PROJECT-EMPIRICAL-VALIDATION.md` — updated from "IMPLEMENTATION
  PREPARED — EXECUTION PENDING" to full executed evidence record.
- `IMPLEMENTATION_PLAN.md` — Multi-Project Empirical Validation item marked complete;
  gate advanced.

No Runtime, ProcessStore, Bridge, test, model, schema, or semantic implementation file
was modified.

---

## Distinction Record

| Term              | This validation                                                                        |
| ----------------- | -------------------------------------------------------------------------------------- |
| **Planned**       | Nine scenarios described in this artifact and in the authorised scenario mapping       |
| **Observed**      | pytest execution output: 9 collected, 9 passed, 0 failed, 0 errors                    |
| **Demonstrated**  | All nine scenarios: isolation, independence, rejection, recovery, bridge authority     |
| **Not Demonstrated** | Agent-boundary empirical participation (not in scope for this validation)           |
| **Inferred**      | None — all results come from actual execution and explicit assertion                   |

---

## Overall Gate Status

### Conformant — Demonstrated

All required multi-project behavioral invariants are directly demonstrated by the
executed evidence.

Every mapped scenario was executed, passed, and its assertions were established by the
real implementation.  No fixture defect, environment defect, implementation gap, or
specification gap was encountered.

The multi-project isolation validation gate is **CLOSED**.

---

## Follow-up Work

This validation does not recommend any implementation change.  No implementation gap was
established.

The next authorized work unit, per the controlled forward work sequence, is:

**Fresh-Agent DBP Continuation** — validate continuation of a real DBP process after
project binding is available.

The xprocess orchestrator incompatibility (pre-existing, recorded in prior evidence) remains
an open known limitation and should be addressed in a dedicated work unit if the cross-process
orchestration capability becomes required by subsequent work.

---

*Executed and recorded: 2026-09-19 (UTC+7).*
*Revision at execution: `ed7e8980522c336862bb5c732a1134a2df9a6af5` (branch: `main`).*
