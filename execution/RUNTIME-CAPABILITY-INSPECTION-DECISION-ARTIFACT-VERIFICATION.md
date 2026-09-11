# Runtime Capability Inspection: Decision, Artifact, and Verification Recording

## Purpose

This bounded inspection follows closure of Evidence Recording and tests the next Runtime capability boundary against the current implementation and the first vertical slice.

The inspection is intentionally limited to the existing Runtime recording capabilities for:

- engineering decisions;
- implementation artifacts; and
- verification results.

No new architecture or generalized orchestration mechanism is introduced.

## Baseline

Inspection baseline: `main` after commit `33ae0aeb52f08f277b9c8295ee5bcb6161cc440b1` (`docs: close Evidence Recording in implementation plan`).

The current Runtime implementation is `runtime/core/runtime.py`. The current authoritative Context representation is `runtime/core/models.py`, and persistence is provided by `runtime/core/store.py` and `runtime/persistence/json_store.py`.

## Capability Inventory

### Decision recording

`Runtime.recognize_decision()` already exists. It:

1. requires an attached Process Instance;
2. requires explicit recognition with `recognized=True` and a non-empty basis;
3. restricts recognized engineering decisions to `initial` or `investigation` process states;
4. appends the decision to `context.engineering_decisions`; and
5. persists a `engineering_decision_recognized` history event.

This is consistent with the established boundary that Runtime recognizes a decision without determining its engineering validity.

### Artifact recording

`Runtime.record_artifact()` already exists. It:

1. requires an attached Process Instance;
2. requires active Process Instance lifecycle;
3. requires the slice-specific `implementation` state;
4. appends the artifact to `context.artifacts`; and
5. persists an `artifact_recorded` history event.

The method therefore provides the minimum state association needed to connect implementation work to the Process Instance.

### Verification recording

Two paths currently exist:

- `begin_verification()` moves the slice-specific process state from `implementation` to `verification` after requiring an artifact and no pending execution work.
- `record_verification()` stores a verification result and remains available for the existing continuity path. It requires active lifecycle and permits recording from `initial`, `implementation`, or `verification`.

`recognize_engineering_completion()` already requires the `verification` state and a successful verification result before recognizing engineering completion.

## Findings

### Finding A — Decision recording is implemented but not yet behaviorally closed

The code establishes a clear decision-recording capability, but the current inspected test inventory does not provide dedicated evidence that the capability works end-to-end across its acceptance and rejection conditions.

Therefore this capability should not yet be marked complete in `IMPLEMENTATION_PLAN.md` under the plan's evidence-based completion rule.

### Finding B — Artifact recording is implemented but not yet behaviorally closed

The code establishes artifact recording and its state/lifecycle guards, but dedicated behavioral coverage was not found in the inspected test inventory.

The capability should therefore remain open for targeted behavioral validation.

### Finding C — Verification recording is implemented but has two semantic paths

The current implementation contains both a structured `begin_verification()` path and a legacy-compatible `record_verification()` path. The latter can directly promote `initial` or `implementation` to `verification` and therefore bypasses the stricter artifact/pending-work preconditions enforced by `begin_verification()`.

This is a concrete capability boundary that requires validation before any consolidation or removal is considered. The existence of the legacy path alone is not sufficient evidence for a semantic defect because it is explicitly retained for continuity experiments.

### Finding D — Recording operations are not uniformly rollback-safe in Runtime memory

`observe()` explicitly snapshots and restores the in-memory evidence list/version/timestamp if `save_context()` fails. The inspected decision, artifact, and verification methods mutate the in-memory Context before calling `save_context()` but do not perform the same Runtime-level restoration on failure.

The persistence layer itself snapshots files and restores them on write failure, so persisted state can remain unchanged. However, after a failed decision/artifact/verification save, the current Runtime object can retain the mutation even though the authoritative persisted Context did not.

This is a concrete consistency risk and is the strongest implementation issue exposed by this inspection. It should be addressed by a bounded follow-up rather than by introducing a broader transaction architecture.

## Testability Assessment

The repository currently has lifecycle and continuity tests, but no CI workflow is configured for the inspected commit and no executable test runner is exposed through the connected GitHub interface. Consequently, this round can establish implementation/testability findings through repository inspection, but it cannot honestly claim fresh pytest execution from the repository environment.

The next executable validation should therefore add targeted tests for:

1. recognized decision acceptance and rejection;
2. decision persistence and recovery;
3. artifact recording and state/lifecycle guards;
4. artifact persistence and recovery;
5. structured verification preconditions;
6. verification persistence and recovery;
7. the legacy verification path's intended compatibility boundary; and
8. failure during `save_context()` for decision, artifact, and verification recording, asserting both persisted rollback and Runtime in-memory rollback.

## Decision

The smallest next Runtime capability work is **not** a new Runtime feature. The current Runtime already contains decision, artifact, and verification recording mechanisms.

The correct next bounded work is **behavioral validation and consistency hardening of the existing recording boundary**, beginning with decision recording because it is the first unchecked recording capability in the implementation plan and is directly required by the first vertical slice before implementation can begin.

No EPM, PEM, lifecycle, or Agent–Runtime semantic change is justified by this inspection.

## Proposed Next Work

- Add focused decision-recording tests.
- Add focused artifact-recording tests.
- Add focused verification-path tests.
- Add failure-path tests for Runtime in-memory/persisted consistency.
- Reconcile the results against the first vertical slice and `IMPLEMENTATION_PLAN.md` before changing implementation semantics.

Only after these tests establish the actual gap should implementation changes be made.
