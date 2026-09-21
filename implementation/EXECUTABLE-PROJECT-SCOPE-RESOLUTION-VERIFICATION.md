# Executable Project / Scope Resolution Verification

**Evidence type: executable verification — 2026-09-21**

This document is the authoritative evidence record for the
`verify/executable-project-scope-resolution` work unit.

---

## Execution Identity

| Field | Value |
|---|---|
| Repository | `tuanna2703/AI-Assisted-Engineering-System-Model` |
| Remote | `https://github.com/tuanna2703/AI-Assisted-Engineering-System-Model` |
| Branch | `verify/executable-project-scope-resolution` |
| HEAD SHA (baseline) | `67f68ccceba20e7833338ef673ba0aa37a5010ae` |
| Baseline commit message | `Merge pull request #17 from tuanna2703/verify/project-scope-resolution` |
| Working tree state | Clean at branch creation; two test files modified before first commit |
| Python | 3.13.5 |
| pytest | 9.1.1 |
| `.aesm/` state | Repository-local committed PI under `.aesm/f713278b-cb74-4a49-a6a1-b6713f058b56/` — not touched |

---

## Baseline Inspection Summary

### Merged implementation surface

- `runtime/core/repository_context.py` — `ActiveRepositoryContext` frozen dataclass; immutable after construction; `aesm_root()` → `<repo>/.aesm`
- `runtime/core/store.py` — `ProcessStore` receives context at construction; `root = context.aesm_root()`; `list_instances()` enumerates only `root.iterdir()`
- `runtime/core/scope_resolution.py` — pure, stateless; filters candidates by lifecycle != "terminated" AND scope == RESOLVED AND identity match; deterministic sort; handles INVALID empty identity
- `runtime/core/runtime.py` — `resolve_process_instance()` delegates to `store.list_instances()` then `scope_resolution.resolve_process_instance()`; `resolve_and_attach_process_instance()` calls `attach()` only on RESOLVED; no implicit creation
- `bridge/agent_runtime_bridge.py` — delegates entirely to Runtime; Bridge does not own binding; no `store` attribute on Bridge

### Repository `.aesm/` state

The repository contains one committed Process Instance:

```
.aesm/f713278b-cb74-4a49-a6a1-b6713f058b56/
    process.json
    context.json
    history.jsonl
```

All targeted tests use `tmp_path` isolation. The committed PI was not read or modified.

### Existing coverage mapping

| Required behavior | Existing test |
|---|---|
| Unique applicable PI | `test_one_applicable_process_instance_resolves_deterministically` |
| No applicable PI | `test_no_applicable_process_instance_requires_explicit_creation` |
| Ambiguous | `test_multiple_applicable_process_instances_are_ambiguous` |
| Explicit PI selection | `test_explicit_process_instance_id_resolves_one_candidate` |
| Wrong-scope explicit PI | `test_explicit_process_instance_from_other_scope_is_rejected` |
| Repository-local resolution | `test_resolution_is_repository_local` *(strengthened — see Changes Made)* |
| Repository relocation | `test_same_repository_identity_recovers_from_new_repository_path` |
| Immutable Runtime context | `test_runtime_context_is_immutable_and_does_not_retarget_store` *(defect fixed — see Changes Made)* |
| Cross-repository PI rejection | `test_explicit_process_instance_from_another_repository_is_rejected` |
| Terminated PI exclusion | `test_terminated_process_instance_is_not_applicable` |
| Bridge without Bridge-owned binding | `test_bridge_exposes_resolution_without_owning_binding` |

---

## Changes Made

### 1. Test defect correction — `test_runtime_context_is_immutable_and_does_not_retarget_store`

**File:** `tests/project_identity/test_scope_resolution.py`

**Defect classification:** Test defect — `runtime.store.context` does not exist on `ProcessStore`.
`ProcessStore` exposes its persistence root as `store.root` (a `Path` object: `<repo>/.aesm`).
The private attribute is `_repository_context`; there is no public `.context` attribute.

**Minimal correction:** Replace `runtime.store.context.repository_root == repo_a`
with `runtime.store.root == repo_a / ".aesm"`.

This tests the same behavioral property (the store writes to the correct repository root)
using the actual public API.

No production code was modified.

### 2. Isolation test strengthened — `test_resolution_is_repository_local`

**File:** `tests/project_identity/test_scope_resolution.py`

**Prior state:** Repository A had PI-A (scope:a). Repository B was empty.
An empty second repository is insufficient isolation evidence: if both repos shared
the same `.aesm/` root, the test would still pass (B has no PI to contaminate A with).

**Strengthened form:** Both repository A and repository B now have a named PI bound to
a distinct scope identity (scope:a and scope:b respectively). The test verifies in both
directions that each repository cannot observe the other's PI. An auditability comment
explains exactly why the test would fail if both stores shared the same `.aesm/` root.

### 3. Isolation test strengthened — `test_cross_repo_isolation`

**File:** `tests/repository_isolation/test_repository_local_persistence.py`

**Prior state:** Repository A had PI-A. Repository B was empty. Only A→B direction tested.

**Strengthened form:** Both repositories now have a PI with a distinct ID. Both
cross-attachment directions are tested (A cannot load PI-B; B cannot load PI-A).
An auditability comment explains why the bidirectional test would fail if both
repositories shared the same `.aesm/` root.

---

## Verification Commands

### Command 1 — Targeted scope resolution and scope binding suites

```
.venv/bin/python -m pytest tests/project_identity/test_scope_resolution.py tests/project_identity/test_scope_binding.py -v
```

**Purpose:** Verify all required Project / Scope Resolution behaviors.

**Result (first run — before fixes):**

```
collected 25 items
24 passed, 1 FAILED
FAILED: test_runtime_context_is_immutable_and_does_not_retarget_store
  AttributeError: 'ProcessStore' object has no attribute 'context'
```

**Result (second run — after defect correction):**

```
platform darwin -- Python 3.13.5, pytest-9.1.1
collected 25 items
25 passed in 0.29s
```

| Behavior | Test | Result |
|---|---|---|
| Unique applicable PI → RESOLVED | `test_one_applicable_process_instance_resolves_deterministically` | PASS |
| No applicable PI → NO_APPLICABLE_PROCESS_INSTANCE | `test_no_applicable_process_instance_requires_explicit_creation` | PASS |
| Ambiguous → AMBIGUOUS, no selection | `test_multiple_applicable_process_instances_are_ambiguous` | PASS |
| Explicit PI selection | `test_explicit_process_instance_id_resolves_one_candidate` | PASS |
| Wrong-scope PI → INVALID | `test_explicit_process_instance_from_other_scope_is_rejected` | PASS |
| Repository-local isolation (bidirectional) | `test_resolution_is_repository_local` | PASS |
| Repository identity ≠ repository root | `test_repository_identity_is_distinct_from_repository_root` | PASS |
| Bridge exposes resolution without owning binding | `test_bridge_exposes_resolution_without_owning_binding` | PASS |
| Repository relocation | `test_same_repository_identity_recovers_from_new_repository_path` | PASS |
| Immutable Runtime context / store root unchanged | `test_runtime_context_is_immutable_and_does_not_retarget_store` | PASS |
| Cross-repository PI → INVALID | `test_explicit_process_instance_from_another_repository_is_rejected` | PASS |
| Terminated PI excluded from resolution | `test_terminated_process_instance_is_not_applicable` | PASS |
| Scope binding persistence | `test_scope_resolution_binds_identity_and_persists` | PASS |
| Scope binding survival across Runtime replacement | `test_scope_binding_survives_runtime_replacement` | PASS |
| Non-resolved outcomes explicit (4 statuses) | `test_nonresolved_scope_outcomes_remain_explicit[*]` | 4 PASS |
| Non-resolved outcome survives recovery | `test_nonresolved_scope_outcome_survives_recovery` | PASS |
| Established scope cannot be silently rebound | `test_established_scope_cannot_be_silently_rebound` | PASS |
| Invalid resolution does not mutate binding | `test_invalid_resolution_does_not_mutate_binding` | PASS |
| Resolution requires explicit recognition | `test_scope_resolution_requires_explicit_recognition` | PASS |
| Bridge submits resolution without owning binding | `test_bridge_can_submit_scope_resolution_without_owning_binding` | PASS |
| Store rejects corrupt scope binding | `test_store_rejects_corrupt_scope_binding` | PASS |

### Command 2 — Multi-project and repository isolation suites

```
.venv/bin/python -m pytest tests/multi_project/ tests/repository_isolation/ -v
```

**Purpose:** Verify multi-project isolation and repository-boundary behaviors.

**Result:**

```
platform darwin -- Python 3.13.5, pytest-9.1.1
collected 24 items
24 passed in 0.28s
```

| Behavior | Test | Result |
|---|---|---|
| Two distinct projects remain isolated | `test_two_distinct_projects_remain_isolated` | PASS |
| Two PIs in one project remain independent | `test_two_process_instances_in_one_project_remain_independent` | PASS |
| Switching projects does not rebind first | `test_switching_projects_does_not_rebind_the_first_process` | PASS |
| Conflicting rebinding rejected, persistence preserved | `test_conflicting_rebinding_is_rejected_and_persistence_remains_project_a` | PASS |
| Unresolved and ambiguous remain independent | `test_unresolved_and_ambiguous_processes_remain_independent` | PASS |
| Unresolved state does not acquire scope from another project | `test_unresolved_state_does_not_acquire_scope_from_another_project` | PASS |
| Bridge preserves independent authority for two projects | `test_bridge_preserves_independent_authority_for_two_projects` | PASS |
| Bridge rejects conflicting scope without mutating state | `test_bridge_rejects_conflicting_scope_without_mutating_authoritative_state` | PASS |
| Recovery uses persisted scope, not runtime session | `test_recovery_after_project_switch_uses_persisted_scope_not_runtime_session` | PASS |
| Old store PI not discovered by repo context | `test_old_store_pi_not_discovered_by_repo_context` | PASS |
| Repo with empty .aesm sees no PI if old store has one | `test_repo_with_empty_aesm_has_no_pi_even_if_old_store_has_pi` | PASS |
| Old store co-existence does not affect repo-local PI | `test_old_store_co_existence_does_not_affect_repo_local_pi` | PASS |
| PI stored in repo .aesm, not old layout | `test_pi_stored_in_repo_aesm_not_old_layout` | PASS |
| PI recovery in same repo | `test_pi_recovery_in_same_repo` | PASS |
| Cross-repo isolation (bidirectional) | `test_cross_repo_isolation` | PASS |
| Same PI ID in two repos resolved independently | `test_same_pi_id_in_two_repos_resolved_independently` | PASS |
| Missing context raises on nonexistent path | `test_missing_repository_context_raises_on_nonexistent_path` | PASS |
| Invalid context raises on file path | `test_invalid_repository_context_raises_on_file_path` | PASS |
| Context is frozen | `test_repository_context_is_frozen` | PASS |
| Context property is readable | `test_runtime_context_property_is_readable` | PASS |
| observe() persists to repo .aesm | `test_observe_persists_in_repo_aesm` | PASS |
| Stale write rejected | `test_stale_write_rejected` | PASS |
| Git conflict blocks load_instance | `test_git_conflict_blocks_load_instance` | PASS |
| Git conflict blocks load_context | `test_git_conflict_blocks_load_context` | PASS |

---

## Behavioral Verification

### Unique applicable Process Instance

`test_one_applicable_process_instance_resolves_deterministically` (PASS):
Creates one PI with scope:one. `resolve_process_instance("scope:one")` → RESOLVED.
`resolve_and_attach_process_instance("scope:one")` → RESOLVED; runtime attached; PI ID matches.

### No applicable Process Instance — no implicit creation

`test_no_applicable_process_instance_requires_explicit_creation` (PASS):
Creates a PI with no matching scope. `resolve_process_instance("scope:missing")` →
`NO_APPLICABLE_PROCESS_INSTANCE`, `process_instance_id = None`.
No new PI is created. The store is not mutated.

### Ambiguous — no arbitrary selection

`test_multiple_applicable_process_instances_are_ambiguous` (PASS):
Two PIs both resolved to `scope:shared`. `resolve_process_instance("scope:shared")` →
`AMBIGUOUS`, `candidate_process_instance_ids = tuple(sorted((first, second)))`.
No arbitrary selection occurs.

### Explicit Process Instance selection

`test_explicit_process_instance_id_resolves_one_candidate` (PASS):
Two PIs on `scope:shared`. Explicit `process_instance_id=second` → RESOLVED with `second`.

### Wrong-scope explicit PI

`test_explicit_process_instance_from_other_scope_is_rejected` (PASS):
PI-A resolved to `scope:first`. `resolve_process_instance("scope:second", process_instance_id=pid_a)` → INVALID.

### Repository relocation

`test_same_repository_identity_recovers_from_new_repository_path` (PASS):
PI created under `original_root`. `.aesm/` copied to `relocated_root` (authorized test setup).
Second runtime at `relocated_root` with same identity → `resolve_and_attach_process_instance` → RESOLVED; same PI ID recovered.

### Repository isolation (bidirectional)

`test_resolution_is_repository_local` (PASS, strengthened):
- repo_a has PI-A (scope:a); repo_b has PI-B (scope:b).
- `runtime_b.resolve_process_instance("scope:a")` → NO_APPLICABLE_PROCESS_INSTANCE.
- `runtime_a.resolve_process_instance("scope:b")` → NO_APPLICABLE_PROCESS_INSTANCE.
- Auditability comment confirms test would fail if both stores shared the same `.aesm/` root.

`test_cross_repo_isolation` (PASS, strengthened):
- Both repos have a PI with a distinct ID.
- `reader_b.attach(pid_a)` → `PersistenceError`.
- `reader_a.attach(pid_b)` → `PersistenceError`.
- Auditability comment confirms test would fail if both stores shared the same `.aesm/` root.

### Immutable Runtime context

`test_runtime_context_is_immutable_and_does_not_retarget_store` (PASS, defect corrected):
- `ActiveRepositoryContext(repo_a)` is frozen; attempted mutation raises `AttributeError`/`TypeError`.
- After failed mutation: `runtime.repository_context.repository_root == repo_a` ✓
- After failed mutation: `runtime.store.root == repo_a / ".aesm"` ✓ (store root unchanged)
- Resolution still finds PI under scope:a; scope:b → NO_APPLICABLE_PROCESS_INSTANCE.

### Cross-repository explicit Process Instance

`test_explicit_process_instance_from_another_repository_is_rejected` (PASS):
PI-A created in repo_a. `runtime_b.resolve_process_instance("scope:a", process_instance_id=pid_a)` → INVALID; `process_instance_id = None`.

### Terminated Process Instance exclusion

`test_terminated_process_instance_is_not_applicable` (PASS):
PI created and resolved to scope:finished. Lifecycle determination ACTIVE→TERMINATED applied.
Fresh runtime: `resolve_process_instance("scope:finished")` → NO_APPLICABLE_PROCESS_INSTANCE; `candidate_process_instance_ids == ()`.

### Bridge exposes resolution without Bridge-owned binding

`test_bridge_exposes_resolution_without_owning_binding` (PASS):
Bridge creates PI, dispatches `apply_scope_resolution`, dispatches `resolve_process_instance`.
`result["resolution"]["status"] == "RESOLVED"` ✓. `not hasattr(bridge, "store")` ✓.
Bridge delegates to Runtime and returns authoritative state; it has no independent binding.

---

## Full Regression

```
.venv/bin/python -m pytest tests/ -v
```

**Purpose:** Full AESM regression suite — all lifecycle, persistence, scope, bridge, isolation, recording, and continuity behaviors.

**Result:**

```
platform darwin -- Python 3.13.5, pytest-9.1.1, pluggy-1.6.0
collected 204 items

...

============================= 204 passed in 2.11s ==============================
```

**204 passed. 0 failed. 0 skipped. Exit code 0.**

---

## Evidence Reconciliation

### CONTROLLER

Demonstrated by `apply_lifecycle_determination` tests and the terminated PI exclusion test.
The Runtime enforces the `authorized-controller` authority context; unauthorized callers are rejected.
Lifecycle transitions require semantic basis and follow the defined transition graph.
A terminated PI is excluded from scope resolution (scope_resolution.py filter on `lifecycle != "terminated"`).

### RUNTIME

Demonstrated by the full scope resolution and scope binding suites.
- `resolve_process_instance` is Runtime-owned; it loads only from the Runtime's `store.root`.
- `resolve_and_attach_process_instance` attaches only after RESOLVED; no implicit creation on NO_APPLICABLE_PROCESS_INSTANCE or AMBIGUOUS.
- `apply_scope_resolution` enforces recognition, basis, status validity, and no-rebind of an established scope.
- The Runtime's `_repository_context` is set at construction from `ActiveRepositoryContext` and is never retargeted.
- `store.root` remains `repo_a/.aesm` throughout the lifetime of the Runtime.

### PERSISTED

Demonstrated by scope binding, persistence hardening, and schema/concurrency suites.
- PI files land in `<repo>/.aesm/<pid>/` (not the old `process-instance/` layout).
- Scope identity and resolution status survive Runtime replacement (reload from disk via fresh Runtime).
- Stale-write guards reject writes at outdated version or timestamp.
- Git conflict markers block load.

### VERIFICATION

Demonstrated by the full regression suite (204 passed, 0 failed) and the targeted suites.
- All 11 required behavioral scenarios are covered by executable tests.
- No source inspection was used as a substitute for test execution.
- Test defect (`runtime.store.context`) was classified as a test defect and corrected; production code was not modified.
- Two isolation tests were strengthened from single-direction/empty-B to bidirectional/populated-B with auditability comments.

### AGENT

Demonstrated by the Bridge tests.
- The Bridge delegates all authority to the Runtime.
- The Bridge has no `store` attribute and does not independently select or create Process Instances.
- Bridge scope resolution dispatch returns Runtime-authoritative state.
- Bridge conflict rejection (`test_bridge_rejects_conflicting_scope_without_mutating_authoritative_state`) confirms Bridge does not override Runtime rejection.

---

## Failures and Limitations

### Test defect corrected

**`test_runtime_context_is_immutable_and_does_not_retarget_store`** — Pre-correction failure:

```
AttributeError: 'ProcessStore' object has no attribute 'context'
```

Classification: **Test defect.** `ProcessStore` uses `_repository_context` (private); the public accessor is `store.root`.
Correction: replaced `runtime.store.context.repository_root` with `runtime.store.root`. No production code changed.

### Remaining limitations

None. All 11 required behavioral scenarios are covered by passing, executable tests.

The remote Git push and PR merge are separate operations not required by the evidence gate.

---

## Verification Conclusion

**VERIFICATION GATE: CLOSED**

All 11 required behavioral scenarios are covered by executable, passing tests:

1. Unique applicable PI → RESOLVED ✓
2. No applicable PI → NO_APPLICABLE_PROCESS_INSTANCE, no implicit creation ✓
3. Ambiguous → AMBIGUOUS, no arbitrary selection ✓
4. Explicit PI selection ✓
5. Wrong-scope PI → INVALID ✓
6. Repository-local resolution (bidirectional) ✓
7. Repository relocation ✓
8. Immutable Runtime context ✓
9. Cross-repository PI → INVALID ✓
10. Terminated PI exclusion ✓
11. Bridge exposes resolution without owning binding ✓

Full regression: **204 passed in 2.11s. Exit code 0.**

All tests executed against the actual implementation. No source inspection was counted as PASS.
No implicit Process Instance creation was introduced. The committed `.aesm/` Process Instance was not modified.
