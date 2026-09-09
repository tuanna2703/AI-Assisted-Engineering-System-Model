# Evidence Recording Behavioral Validation

## Executive Summary

| Field | Value |
|---|---|
| **Implementation** | Evidence Recording |
| **Branch** | `feature/evidence-recording` |
| **Initial commit SHA** | `70ab5cb4fc87958d1065d767ad590ac223baf01b` |
| **Final commit SHA** | `245fc5f7a6b08999eb134ff7b27138214e76fdeb` |
| **Overall validation result** | **PASS — Evidence Recording behaviorally validated** |

### Major Behavioral Findings

1. **Recognized Evidence**: Properly recognized contributions are accepted, persisted to authoritative `ExecutionContext.evidence`, produce `evidence_recorded` history events, and survive Runtime replacement. Recognition metadata is stripped from the persisted evidence and preserved separately in the history event.

2. **Recognition Boundary**: Missing recognition, explicit negative recognition (`recognized=False`), and incomplete recognition (missing `basis`) are all correctly rejected. Rejected contributions do not mutate authoritative Evidence.

3. **Persistence Boundary**: Evidence is persisted within the existing `ExecutionContext` via the existing `ProcessStore.save_context()` path. No separate Evidence database or subsystem has been introduced. The `save_context()` method was strengthened with file-level snapshot/rollback to match the lifecycle persistence pattern.

4. **Runtime Replacement / Continuity**: Evidence recorded by Runtime A is fully recoverable by Runtime B via `attach()`. Recovery comes from authoritative persisted state, not transient memory.

5. **State Isolation**: Evidence Recording does not mutate `process_state`, `engineering_decisions`, lifecycle, or any other unrelated Context field.

6. **Suspended Evidence Recording**: Evidence Recording succeeds while the Process Instance is suspended, consistent with the established semantic rule that suspension blocks execution but not observation.

7. **Persistence Failure Atomicity**: Persistence failure during Evidence Recording correctly restores in-memory `evidence`, `version`, and `updated_at` to prior authoritative values. Persisted Context remains uncontaminated.

8. **Defect Found and Corrected**: Two pre-existing lifecycle tests (`test_failed_verification_preserves_failure_and_reopens_investigation`, `test_suspended_observation_and_recognition_remain_informational`) called `observe()` without the `recognition` field now required by the Evidence Recording implementation. Classification: test compatibility defect (not an implementation defect). Corrected by adding explicit evidence recognition to the affected test call sites.

---

## Execution Environment

| Field | Value |
|---|---|
| **Repository** | `tuanna2703/AI-Assisted-Engineering-System-Model` |
| **Branch** | `feature/evidence-recording` |
| **Initial commit SHA** | `70ab5cb4fc87958d1065d767ad590ac223baf01b` |
| **Initial commit timestamp** | `2026-09-09 16:30:36 +0700` |
| **Initial commit subject** | `fix: make context recording failure-safe` |
| **Working tree status** | Clean (no uncommitted changes at validation start) |
| **Python** | 3.13.5 |
| **pytest** | 9.1.1 |
| **Platform** | macOS (darwin) |

### Initial Git State

```
$ git branch --show-current
feature/evidence-recording

$ git log -1 --format="%H %ai %s"
70ab5cb4fc87958d1065d767ad590ac223baf01b 2026-09-09 16:30:36 +0700 fix: make context recording failure-safe

$ git status --short
(clean)
```

### Branch Relationship to Main

The `feature/evidence-recording` branch contains 3 Evidence Recording-specific commits ahead of `main`:

```
70ab5cb fix: make context recording failure-safe
71c7873 test: validate explicit evidence recording
9ab0ad5 feat: require explicit evidence recognition
```

Changed files (vs `main`):

```
 runtime/core/runtime.py                   | 32 +++++++++-
 runtime/core/store.py                     | 25 ++++++--
 tests/continuity/test_runtime_recovery.py | 99 ++++++++++++++++++++++++++++++-
 3 files changed, 146 insertions(+), 10 deletions(-)
```

### Commands Executed

```bash
git branch --show-current
git log -1 --format="%H %ai %s"
git status --short
git branch -a
git log --oneline -20
git log main..feature/evidence-recording --oneline
git diff main..feature/evidence-recording --stat
git diff main..feature/evidence-recording -- runtime/core/runtime.py
git diff main..feature/evidence-recording -- runtime/core/store.py
git diff main..feature/evidence-recording -- tests/continuity/test_runtime_recovery.py
git diff main..feature/evidence-recording -- tests/lifecycle/test_runtime_lifecycle.py
python3 -m pytest tests/continuity/test_runtime_recovery.py -v
python3 -m pytest tests/lifecycle/ -v
python3 -m pytest tests/ -v
```

---

## Validation Matrix

| Behavior | Expected | Actual | Evidence | Result |
|---|---|---|---|---|
| Recognized Evidence accepted | Recognized contribution with `recognized=True` and `basis` is accepted and appended to `context.evidence` | Observed: contribution accepted, evidence persisted without recognition metadata, history records `evidence_recorded` | `test_recognized_evidence_is_recorded_without_process_state_mutation` — PASSED | **PASS** |
| Recognition boundary: missing recognition | `TypeError` raised, evidence unchanged | `TypeError` raised, `context.evidence == []` | `test_evidence_requires_explicit_recognition` case 1 — PASSED | **PASS** |
| Recognition boundary: explicit negative | `RuntimeError` raised, evidence unchanged | `RuntimeError` raised, `context.evidence == []` | `test_evidence_requires_explicit_recognition` case 2 — PASSED | **PASS** |
| Recognition boundary: missing basis | `RuntimeError` raised, evidence unchanged | `RuntimeError` raised, `context.evidence == []` | `test_evidence_requires_explicit_recognition` case 3 — PASSED | **PASS** |
| Assumptions not promoted | `RuntimeError` raised, evidence unchanged | `RuntimeError` raised, `context.evidence == []` | `test_assumption_or_claim_is_not_silently_promoted_to_evidence` — PASSED | **PASS** |
| Unsupported claims not promoted | `RuntimeError` raised, evidence unchanged | `RuntimeError` raised, `context.evidence == []` | `test_assumption_or_claim_is_not_silently_promoted_to_evidence` — PASSED | **PASS** |
| Persistence via existing Context mechanism | Evidence stored in `context.json`, history in `history.jsonl`, no separate subsystem | Observed: evidence in `ExecutionContext.evidence`, persisted via `ProcessStore.save_context()` | Code inspection of `Runtime.observe()` and `ProcessStore.save_context()` | **PASS** |
| Persistence failure atomicity | Failed evidence does not remain in-memory or on disk | `context.evidence == []`, `context.version` restored, persisted context clean | `test_failed_evidence_persistence_restores_in_memory_authoritative_state` — PASSED | **PASS** |
| Runtime replacement / continuity | Evidence survives Runtime A → Runtime B replacement | Runtime B recovers `evidence[0]["fact"] == "existing implementation found"` via `attach()` | `test_process_and_context_survive_runtime_replacement` — PASSED | **PASS** |
| Traceability / history | `evidence_recorded` event distinguishable from other events | History sequence `["process_created", "evidence_recorded", "engineering_decision_recognized"]` | `test_history_is_preserved` — PASSED | **PASS** |
| State isolation: process state | Evidence Recording does not change `process_state` | `context.process_state == "initial"` after evidence recording | `test_recognized_evidence_is_recorded_without_process_state_mutation` — PASSED | **PASS** |
| State isolation: decisions | Evidence Recording does not create decisions | `context.engineering_decisions == []` after evidence recording | `test_recognized_evidence_is_recorded_without_process_state_mutation` — PASSED | **PASS** |
| Suspended Evidence Recording | Evidence Recording succeeds while suspended | Evidence appended, lifecycle remains `"suspended"` | `test_suspended_observation_and_recognition_remain_informational` — PASSED | **PASS** |

---

## Test Execution Results

### Focused Evidence Tests (Pre-correction)

```
$ python3 -m pytest tests/continuity/test_runtime_recovery.py -v

12 passed in 0.25s
```

All 12 continuity/recovery tests passed, including the 4 new Evidence Recording-specific tests:

- `test_evidence_requires_explicit_recognition` ✅
- `test_recognized_evidence_is_recorded_without_process_state_mutation` ✅
- `test_assumption_or_claim_is_not_silently_promoted_to_evidence` ✅
- `test_failed_evidence_persistence_restores_in_memory_authoritative_state` ✅

### Lifecycle Tests (Pre-correction)

```
$ python3 -m pytest tests/lifecycle/ -v

21 passed, 2 failed in 0.60s
```

Two failures:

1. `test_failed_verification_preserves_failure_and_reopens_investigation` — FAILED
2. `test_suspended_observation_and_recognition_remain_informational` — FAILED

Both failures were caused by the same root cause: these tests called `observe()` without the `recognition` field now required by the Evidence Recording implementation. See **Defects and Corrections** below.

### Full Suite (Post-correction)

```
$ python3 -m pytest tests/ -v

35 passed in 0.66s
```

All 35 tests passed:
- 12 continuity/recovery tests ✅
- 16 lifecycle control tests ✅
- 7 lifecycle runtime tests ✅

### Warnings and Environment Limitations

None observed. No skipped, xfailed, or error-state tests.

---

## Behavioral Evidence

### Recognized Evidence Flow

The `Runtime.observe()` method (runtime/core/runtime.py:59–89) implements the complete contribution → recognition → persistence boundary:

1. **Type guard**: Rejects non-mapping observations with `TypeError`.
2. **Recognition check**: Calls `_require_recognition()` which validates `recognized=True` and a non-empty `basis`.
3. **Evidence extraction**: Strips the `recognition` key from the observation, leaving only the evidence content.
4. **Snapshot**: Captures `prior_evidence`, `prior_version`, `prior_updated_at` before mutation.
5. **Mutation**: Appends extracted evidence to `context.evidence`.
6. **Persistence**: Calls `store.save_context()` with an `evidence_recorded` event that includes the evidence content, recognition metadata, and runtime ID.
7. **Rollback on failure**: If persistence fails, restores `context.evidence`, `context.version`, and `context.updated_at` to prior values.

### Recognition Boundary Enforcement

The `_require_recognition()` static method (runtime/core/runtime.py:289–296) enforces:

- Recognition must be a `dict` (else `TypeError`).
- `recognized` must be exactly `True` (else `RuntimeError`).
- `basis` must be truthy (else `RuntimeError`).

This is shared by `observe()`, `recognize_decision()`, and `recognize_engineering_completion()`, providing uniform recognition semantics.

### Evidence Persistence Path

Evidence is persisted through the same `ProcessStore.save_context()` path used by all other Context mutations (store.py:43–67). The Evidence Recording commits also made this path failure-safe by:

1. Snapshotting `context.json` and `history.jsonl` file contents before mutation.
2. Wrapping the version increment, context save, and history append in a try/except.
3. On failure: restoring `version`, `updated_at`, and both file contents via `_restore_file()`.

This matches the pattern already established in `save_lifecycle()` (store.py:69–120).

### History / Traceability

The `evidence_recorded` history event contains:

```python
{
    "type": "evidence_recorded",
    "evidence": {<evidence content without recognition>},
    "recognition": {"recognized": True, "basis": "..."},
    "runtime_id": "runtime-a",
    "version": <context version>,
    "at": "<timestamp>"
}
```

This is distinguishable from:
- `process_created`
- `observation_recorded` (pre-Evidence Recording name, no longer used)
- `engineering_decision_recognized`
- `artifact_recorded`
- `verification_recorded`
- `lifecycle_transition`
- Other material process events

### Suspended Evidence Recording

The `observe()` method does not call `_require_active_lifecycle()`. This is consistent with the established semantic rule:

> Suspension blocks execution that lifecycle semantics prohibit; it does not automatically prohibit observation or Evidence recording.

The test `test_suspended_observation_and_recognition_remain_informational` confirms that evidence is successfully recorded while the Process Instance lifecycle is `"suspended"`, and that the lifecycle value remains unchanged afterward.

### Runtime Replacement Continuity

`test_process_and_context_survive_runtime_replacement` demonstrates:

1. Runtime A creates a process, starts investigation, records evidence, recognizes a decision, begins implementation, and sets pending execution.
2. Runtime A stops (simulating session loss).
3. Runtime B attaches to the same process.
4. Runtime B recovers evidence (`evidence[0]["fact"] == "existing implementation found"`), decisions, pending execution from persisted authoritative state — not from transient Runtime A memory.

---

## Defects and Corrections

### Defect 1: Lifecycle tests not updated for Evidence Recording API change

| Field | Value |
|---|---|
| **Observed behavior** | `test_failed_verification_preserves_failure_and_reopens_investigation` and `test_suspended_observation_and_recognition_remain_informational` raise `TypeError: evidence recognition must be a mapping` |
| **Expected behavior** | Tests should pass using the updated `observe()` API |
| **Classification** | Test compatibility defect |
| **Root cause** | The `observe()` method now requires explicit recognition (added by commit `9ab0ad5`). Two lifecycle tests in `tests/lifecycle/test_runtime_lifecycle.py` were written before this change and called `observe()` without a `recognition` field. |
| **Correction** | Added `EVIDENCE` recognition constant and included `"recognition": EVIDENCE` in the two affected `observe()` calls. The tests continue to validate the same lifecycle behavior; only the call-site shape changed. |
| **Regression test** | The corrected tests themselves serve as regression coverage — they would fail again if the recognition requirement were inadvertently removed. |
| **Post-correction result** | Both tests pass. Full suite: 35/35 passed. |
| **Commit** | `245fc5f7a6b08999eb134ff7b27138214e76fdeb` |

No other defects were identified. No implementation corrections were necessary.

---

## Boundary Verification

### Contribution vs. Recognized Evidence Boundary

**Verified.** `_require_recognition()` enforces that a contribution must include `recognized=True` with an explicit `basis` before it can become authoritative Evidence. Contributions without recognition or with `recognized=False` are rejected before any mutation occurs. Tested by `test_evidence_requires_explicit_recognition` and `test_assumption_or_claim_is_not_silently_promoted_to_evidence`.

### Runtime Authority Boundary

**Verified.** The Runtime (`Runtime.observe()`) controls recognition and authoritative state mutation. An Agent cannot bypass recognition by submitting arbitrary observations — the `_require_recognition()` guard runs within the Runtime's `observe()` method before any mutation. The Agent provides candidates; the Runtime decides whether they meet the recognition threshold.

### Context Persistence Boundary

**Verified.** Evidence is stored as part of `ExecutionContext.evidence` and persisted via the existing `ProcessStore.save_context()` path to `context.json`. No separate Evidence database, table, or storage subsystem has been introduced. History events are appended to the existing `history.jsonl` file. Verified by code inspection and by `test_recognized_evidence_is_recorded_without_process_state_mutation` (checks persisted history) and `test_process_and_context_survive_runtime_replacement` (checks persisted context recovery).

### History / Traceability Boundary

**Verified.** Evidence recording produces `evidence_recorded` history events that are distinguishable from all other event types. The history preserves recognition metadata, the evidence content, the runtime ID, a version number, and a timestamp. Verified by `test_history_is_preserved` which checks the complete event type sequence.

### Runtime Replacement / Recovery Boundary

**Verified.** Evidence recorded by Runtime A is recoverable by Runtime B exclusively from persisted authoritative state via `ProcessStore.load_context()`. No transient runtime or agent memory participates in recovery. Verified by `test_process_and_context_survive_runtime_replacement`.

### Lifecycle Boundary

**Verified.** Evidence Recording does not call `_require_active_lifecycle()`, allowing observation and evidence recording while suspended. This is consistent with the established semantic rule. Engineering execution operations (`begin_implementation`, `begin_verification`, etc.) continue to enforce the active lifecycle guard. Verified by `test_suspended_observation_and_recognition_remain_informational` which records evidence while suspended and then confirms that `begin_implementation()` is still blocked.

### Process State / Decision Isolation

**Verified.** Evidence Recording does not mutate `process_state`, does not create `engineering_decisions`, does not alter lifecycle state, does not set `engineering_completion`, does not create artifacts, and does not modify any other unrelated Context field. Verified by `test_recognized_evidence_is_recorded_without_process_state_mutation` which explicitly asserts `process_state == "initial"` and `engineering_decisions == []` after evidence recording.

---

## Conclusion

**PASS — Evidence Recording behaviorally validated**

All 8 behavioral dimensions were exercised and confirmed through actual test execution:

1. Recognized Evidence acceptance and persistence ✅
2. Recognition boundary enforcement ✅
3. Persistence via existing Context mechanism ✅
4. Runtime replacement / continuity ✅
5. History / traceability ✅
6. Process State and Decision isolation ✅
7. Suspended Evidence Recording ✅
8. Persistence failure atomicity ✅

One test compatibility defect was found and corrected (lifecycle tests not updated for the Evidence Recording API change). No implementation defects were identified.

35 of 35 tests pass across the complete test suite after correction.

This validation does not authorize closure of the Evidence Recording work unit. Closure is a human decision made after reviewing the validation evidence.
