"""Behavioral validation of Decision, Artifact, and Verification Recording.

This test module establishes the actual behavior of the existing recording
capabilities, including their persistence-failure consistency properties.

Tests use the established save_context failure-injection pattern from
tests/continuity/test_runtime_recovery.py:
test_failed_evidence_persistence_restores_in_memory_authoritative_state
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from runtime.core import ProcessStore, Runtime
from runtime.core.models import ExecutionContext
from runtime.persistence.json_store import PersistenceError


# --- Shared recognition constants ---

EVIDENCE_RECOGNITION = {
    "recognized": True,
    "basis": "workspace inspection established the observation as recordable evidence",
}
DECISION_RECOGNITION = {
    "recognized": True,
    "basis": "applicable decision gate satisfied",
}
COMPLETION_RECOGNITION = {
    "recognized": True,
    "basis": "applicable engineering completion conditions satisfied",
}


# --- Helpers ---


def build_runtime(tmp_path: Path, runtime_id: str = "recording-test") -> Runtime:
    """Create a new Runtime with a fresh Process Instance."""
    runtime = Runtime(ProcessStore(tmp_path), runtime_id)
    runtime.create_process("Recording behavioral validation")
    return runtime


def advance_to_investigation(runtime: Runtime) -> None:
    """Move the process to the INVESTIGATION state."""
    runtime.start_investigation()


def advance_to_implementation(runtime: Runtime) -> None:
    """Move the process to IMPLEMENTATION with the minimum prerequisites."""
    advance_to_investigation(runtime)
    runtime.observe({
        "fact": "implementation prerequisite evidence",
        "recognition": EVIDENCE_RECOGNITION,
    })
    runtime.recognize_decision(
        {"id": "D1", "conclusion": "proceed with implementation"},
        DECISION_RECOGNITION,
    )
    runtime.begin_implementation()


def advance_to_verification(runtime: Runtime) -> None:
    """Move the process to VERIFICATION with minimum prerequisites."""
    advance_to_implementation(runtime)
    runtime.record_artifact({"path": "test-artifact.py", "type": "implementation"})
    runtime.begin_verification()


def fail_save_context(context: ExecutionContext, event: dict[str, Any]) -> None:
    """Established persistence-failure injection pattern.

    Simulates failure at the actual persistence boundary after the caller
    has already changed the Context, to determine whether the caller
    restores the in-memory mutation.
    """
    context.version += 1
    raise PersistenceError("simulated persistence failure")


# =============================================================================
# DECISION RECORDING TESTS
# =============================================================================


class TestDecisionRecordingSuccess:
    """Test successful decision recording behavior."""

    def test_decision_is_recorded_in_context(self, tmp_path: Path):
        """A recognized decision is appended to engineering_decisions."""
        runtime = build_runtime(tmp_path)
        advance_to_investigation(runtime)

        decision = {"id": "D1", "conclusion": "use existing extension point"}
        runtime.recognize_decision(decision, DECISION_RECOGNITION)

        assert len(runtime.context.engineering_decisions) == 1
        assert runtime.context.engineering_decisions[0] == decision

    def test_decision_is_persisted(self, tmp_path: Path):
        """A recognized decision survives reload from persistence."""
        store = ProcessStore(tmp_path)
        runtime = Runtime(store, "recording-test")
        pid = runtime.create_process("Recording behavioral validation")
        advance_to_investigation(runtime)

        decision = {"id": "D1", "conclusion": "use existing extension point"}
        runtime.recognize_decision(decision, DECISION_RECOGNITION)
        runtime.stop()

        runtime_b = Runtime(store, "recording-test-b")
        runtime_b.attach(pid)
        assert runtime_b.context.engineering_decisions == [decision]

    def test_decision_generates_history_event(self, tmp_path: Path):
        """Decision recording produces an engineering_decision_recognized event."""
        store = ProcessStore(tmp_path)
        runtime = Runtime(store, "recording-test")
        pid = runtime.create_process("Recording behavioral validation")
        advance_to_investigation(runtime)

        decision = {"id": "D1", "conclusion": "use existing extension point"}
        runtime.recognize_decision(decision, DECISION_RECOGNITION)

        history = store.history(pid)
        decision_events = [e for e in history if e["type"] == "engineering_decision_recognized"]
        assert len(decision_events) == 1
        assert decision_events[0]["decision"] == decision
        assert decision_events[0]["recognition"] == DECISION_RECOGNITION

    def test_decision_does_not_change_process_state(self, tmp_path: Path):
        """Decision recording does not mutate process_state."""
        runtime = build_runtime(tmp_path)
        advance_to_investigation(runtime)
        prior_state = runtime.context.process_state

        runtime.recognize_decision(
            {"id": "D1", "conclusion": "proceed"},
            DECISION_RECOGNITION,
        )
        assert runtime.context.process_state == prior_state

    def test_decision_increments_context_version(self, tmp_path: Path):
        """Decision recording increments the context version via save_context."""
        runtime = build_runtime(tmp_path)
        advance_to_investigation(runtime)
        prior_version = runtime.context.version

        runtime.recognize_decision(
            {"id": "D1", "conclusion": "proceed"},
            DECISION_RECOGNITION,
        )
        assert runtime.context.version == prior_version + 1

    def test_multiple_decisions_accumulate(self, tmp_path: Path):
        """Multiple decisions can be recorded in sequence."""
        runtime = build_runtime(tmp_path)
        advance_to_investigation(runtime)

        d1 = {"id": "D1", "conclusion": "first decision"}
        d2 = {"id": "D2", "conclusion": "second decision"}
        runtime.recognize_decision(d1, DECISION_RECOGNITION)
        runtime.recognize_decision(d2, DECISION_RECOGNITION)

        assert runtime.context.engineering_decisions == [d1, d2]

    def test_decision_allowed_from_initial_state(self, tmp_path: Path):
        """Decision recording is permitted from the initial process state."""
        runtime = build_runtime(tmp_path)
        assert runtime.context.process_state == "initial"

        decision = {"id": "D1", "conclusion": "initial-state decision"}
        runtime.recognize_decision(decision, DECISION_RECOGNITION)
        assert runtime.context.engineering_decisions == [decision]


class TestDecisionRecordingGuards:
    """Test decision recording state and recognition guards."""

    def test_decision_rejected_without_recognition(self, tmp_path: Path):
        """Decision recording requires explicit recognition."""
        runtime = build_runtime(tmp_path)
        with pytest.raises(TypeError):
            runtime.recognize_decision({"id": "D1"}, "not a dict")

    def test_decision_rejected_when_not_recognized(self, tmp_path: Path):
        """Decision recording requires recognized=True."""
        runtime = build_runtime(tmp_path)
        with pytest.raises(RuntimeError):
            runtime.recognize_decision(
                {"id": "D1"},
                {"recognized": False, "basis": "proposal only"},
            )

    def test_decision_rejected_without_basis(self, tmp_path: Path):
        """Decision recording requires an explicit basis."""
        runtime = build_runtime(tmp_path)
        with pytest.raises(RuntimeError):
            runtime.recognize_decision(
                {"id": "D1"},
                {"recognized": True},
            )

    def test_decision_rejected_from_implementation_state(self, tmp_path: Path):
        """Decision recording is rejected from IMPLEMENTATION state."""
        runtime = build_runtime(tmp_path)
        advance_to_implementation(runtime)

        with pytest.raises(RuntimeError, match="investigation"):
            runtime.recognize_decision(
                {"id": "D2", "conclusion": "late decision"},
                DECISION_RECOGNITION,
            )

    def test_decision_rejected_from_verification_state(self, tmp_path: Path):
        """Decision recording is rejected from VERIFICATION state."""
        runtime = build_runtime(tmp_path)
        advance_to_verification(runtime)

        with pytest.raises(RuntimeError, match="investigation"):
            runtime.recognize_decision(
                {"id": "D2", "conclusion": "verification-state decision"},
                DECISION_RECOGNITION,
            )

    def test_decision_rejected_from_engineering_complete_state(self, tmp_path: Path):
        """Decision recording is rejected from ENGINEERING_COMPLETE state."""
        runtime = build_runtime(tmp_path)
        advance_to_verification(runtime)
        runtime.record_verification({"passed": True, "checks": ["unit tests"]})
        runtime.recognize_engineering_completion(COMPLETION_RECOGNITION)

        with pytest.raises(RuntimeError, match="investigation"):
            runtime.recognize_decision(
                {"id": "D2", "conclusion": "post-completion decision"},
                DECISION_RECOGNITION,
            )

    def test_decision_rejected_when_not_attached(self, tmp_path: Path):
        """Decision recording requires an attached Runtime."""
        runtime = build_runtime(tmp_path)
        runtime.stop()
        with pytest.raises(RuntimeError):
            runtime.recognize_decision(
                {"id": "D1"},
                DECISION_RECOGNITION,
            )


class TestDecisionRecordingPersistenceFailure:
    """Test decision recording behavior when persistence fails."""

    def test_failed_decision_persistence_leaves_live_state_inconsistent(
        self, tmp_path: Path, monkeypatch
    ):
        """Determine whether failed decision persistence restores in-memory state.

        This is the critical test. The hypothesis from the capability inspection
        is that recognize_decision() mutates context.engineering_decisions
        before calling save_context() and does NOT restore on failure.

        This test empirically establishes the actual behavior.
        """
        store = ProcessStore(tmp_path)
        runtime = Runtime(store, "recording-test")
        pid = runtime.create_process("Recording behavioral validation")
        advance_to_investigation(runtime)

        # Establish pre-failure baseline
        prior_decisions = list(runtime.context.engineering_decisions)
        prior_version = runtime.context.version
        prior_state = runtime.context.process_state

        # Capture persisted baseline
        persisted_before = store.load_context(pid)
        persisted_decisions_before = list(persisted_before.engineering_decisions)
        persisted_version_before = persisted_before.version

        # Install controlled failure
        monkeypatch.setattr(store, "save_context", fail_save_context)

        # Attempt decision recording — expect failure
        with pytest.raises(PersistenceError, match="simulated persistence failure"):
            runtime.recognize_decision(
                {"id": "D-failed", "conclusion": "this should not persist"},
                DECISION_RECOGNITION,
            )

        # --- Inspect live in-memory state after failure ---
        # The critical question: was the in-memory mutation rolled back?
        live_decisions = runtime.context.engineering_decisions
        live_version = runtime.context.version
        live_state = runtime.context.process_state

        # --- Inspect persisted state (file-level) ---
        # Remove monkeypatch to allow normal loading
        monkeypatch.undo()
        persisted_after = store.load_context(pid)
        persisted_decisions_after = list(persisted_after.engineering_decisions)
        persisted_version_after = persisted_after.version

        # --- Inspect fresh Runtime recovery ---
        fresh_runtime = Runtime(store, "recording-test-fresh")
        fresh_runtime.attach(pid)
        fresh_decisions = list(fresh_runtime.context.engineering_decisions)
        fresh_version = fresh_runtime.context.version

        # === Persisted state assertions ===
        # The persistence layer's own rollback should keep persisted files unchanged.
        assert persisted_decisions_after == persisted_decisions_before, (
            "Persisted decisions should be unchanged after failed save_context"
        )
        assert persisted_version_after == persisted_version_before, (
            "Persisted version should be unchanged after failed save_context"
        )

        # === Fresh Runtime assertions ===
        assert fresh_decisions == persisted_decisions_before, (
            "Fresh Runtime should see the pre-failure authoritative state"
        )
        assert fresh_version == persisted_version_before, (
            "Fresh Runtime version should match pre-failure persisted version"
        )

        # === Live in-memory state assertions ===
        # This is where the defect is expected to manifest.
        # If recognize_decision() does NOT roll back the in-memory mutation,
        # the live Runtime will have a decision that was never persisted.

        # Record actual observed behavior for the evidence report:
        live_has_failed_decision = any(
            d.get("id") == "D-failed" for d in live_decisions
        )
        live_version_incremented = live_version > prior_version

        # The CORRECT behavior would be:
        #   live_decisions == prior_decisions (no unpersisted mutation)
        #   live_version == prior_version (version not incremented)
        # The DEFECTIVE behavior would be:
        #   live_decisions contains D-failed (unpersisted mutation retained)
        #   live_version > prior_version (version incremented by fail_save_context)

        # Assert the CORRECT behavior. If this fails, the defect is confirmed.
        assert live_decisions == prior_decisions, (
            f"CONSISTENCY DEFECT: Live Runtime retains unpersisted decision mutation. "
            f"Live decisions: {live_decisions}, expected: {prior_decisions}"
        )
        assert live_version == prior_version, (
            f"CONSISTENCY DEFECT: Live Runtime version was mutated by failed persistence. "
            f"Live version: {live_version}, expected: {prior_version}"
        )
        assert live_state == prior_state, (
            f"CONSISTENCY DEFECT: Live process state changed after failed persistence. "
            f"Live state: {live_state}, expected: {prior_state}"
        )


# =============================================================================
# ARTIFACT RECORDING TESTS
# =============================================================================


class TestArtifactRecordingSuccess:
    """Test successful artifact recording behavior."""

    def test_artifact_is_recorded_in_context(self, tmp_path: Path):
        """A recorded artifact is appended to the artifacts list."""
        runtime = build_runtime(tmp_path)
        advance_to_implementation(runtime)

        artifact = {"path": "src/feature.py", "type": "implementation"}
        runtime.record_artifact(artifact)

        assert len(runtime.context.artifacts) == 1
        assert runtime.context.artifacts[0] == artifact

    def test_artifact_is_persisted(self, tmp_path: Path):
        """A recorded artifact survives reload from persistence."""
        store = ProcessStore(tmp_path)
        runtime = Runtime(store, "recording-test")
        pid = runtime.create_process("Recording behavioral validation")
        advance_to_implementation(runtime)

        artifact = {"path": "src/feature.py", "type": "implementation"}
        runtime.record_artifact(artifact)
        runtime.stop()

        runtime_b = Runtime(store, "recording-test-b")
        runtime_b.attach(pid)
        assert runtime_b.context.artifacts == [artifact]

    def test_artifact_generates_history_event(self, tmp_path: Path):
        """Artifact recording produces an artifact_recorded event."""
        store = ProcessStore(tmp_path)
        runtime = Runtime(store, "recording-test")
        pid = runtime.create_process("Recording behavioral validation")
        advance_to_implementation(runtime)

        artifact = {"path": "src/feature.py", "type": "implementation"}
        runtime.record_artifact(artifact)

        history = store.history(pid)
        artifact_events = [e for e in history if e["type"] == "artifact_recorded"]
        assert len(artifact_events) == 1
        assert artifact_events[0]["artifact"] == artifact

    def test_artifact_does_not_change_process_state(self, tmp_path: Path):
        """Artifact recording does not mutate process_state."""
        runtime = build_runtime(tmp_path)
        advance_to_implementation(runtime)
        prior_state = runtime.context.process_state

        runtime.record_artifact({"path": "src/feature.py"})
        assert runtime.context.process_state == prior_state

    def test_artifact_increments_context_version(self, tmp_path: Path):
        """Artifact recording increments the context version via save_context."""
        runtime = build_runtime(tmp_path)
        advance_to_implementation(runtime)
        prior_version = runtime.context.version

        runtime.record_artifact({"path": "src/feature.py"})
        assert runtime.context.version == prior_version + 1

    def test_multiple_artifacts_accumulate(self, tmp_path: Path):
        """Multiple artifacts can be recorded in sequence."""
        runtime = build_runtime(tmp_path)
        advance_to_implementation(runtime)

        a1 = {"path": "src/feature.py"}
        a2 = {"path": "src/helper.py"}
        runtime.record_artifact(a1)
        runtime.record_artifact(a2)

        assert runtime.context.artifacts == [a1, a2]


class TestArtifactRecordingGuards:
    """Test artifact recording state guards."""

    def test_artifact_rejected_from_initial_state(self, tmp_path: Path):
        """Artifact recording requires IMPLEMENTATION state."""
        runtime = build_runtime(tmp_path)
        assert runtime.context.process_state == "initial"
        with pytest.raises(RuntimeError):
            runtime.record_artifact({"path": "src/feature.py"})

    def test_artifact_rejected_from_investigation_state(self, tmp_path: Path):
        """Artifact recording is rejected from INVESTIGATION state."""
        runtime = build_runtime(tmp_path)
        advance_to_investigation(runtime)
        with pytest.raises(RuntimeError):
            runtime.record_artifact({"path": "src/feature.py"})

    def test_artifact_rejected_from_verification_state(self, tmp_path: Path):
        """Artifact recording is rejected from VERIFICATION state."""
        runtime = build_runtime(tmp_path)
        advance_to_verification(runtime)
        with pytest.raises(RuntimeError):
            runtime.record_artifact({"path": "src/new-artifact.py"})

    def test_artifact_rejected_when_not_attached(self, tmp_path: Path):
        """Artifact recording requires an attached Runtime."""
        runtime = build_runtime(tmp_path)
        runtime.stop()
        with pytest.raises(RuntimeError):
            runtime.record_artifact({"path": "src/feature.py"})

    def test_artifact_rejected_when_lifecycle_not_active(self, tmp_path: Path):
        """Artifact recording requires an active lifecycle."""
        runtime = build_runtime(tmp_path)
        advance_to_implementation(runtime)
        # Suspend the process
        runtime.apply_lifecycle_determination({
            "target_process_instance_id": runtime.process_instance.process_instance_id,
            "requested_transition": "ACTIVE -> SUSPENDED",
            "semantic_basis": "execution temporarily paused",
            "authority_context": "authorized-controller",
            "actor": "test-controller",
            "evidence": [{"condition": "execution temporarily paused"}],
            "occurred_at": "2026-09-09T00:00:00+00:00",
        })
        with pytest.raises(RuntimeError, match="lifecycle"):
            runtime.record_artifact({"path": "src/feature.py"})


class TestArtifactRecordingPersistenceFailure:
    """Test artifact recording behavior when persistence fails."""

    def test_failed_artifact_persistence_leaves_live_state_inconsistent(
        self, tmp_path: Path, monkeypatch
    ):
        """Determine whether failed artifact persistence restores in-memory state.

        Same hypothesis as decision recording: record_artifact() mutates
        context.artifacts before calling save_context() and does NOT restore
        on failure.
        """
        store = ProcessStore(tmp_path)
        runtime = Runtime(store, "recording-test")
        pid = runtime.create_process("Recording behavioral validation")
        advance_to_implementation(runtime)

        # Establish pre-failure baseline
        prior_artifacts = list(runtime.context.artifacts)
        prior_version = runtime.context.version
        prior_state = runtime.context.process_state

        # Capture persisted baseline
        persisted_before = store.load_context(pid)
        persisted_artifacts_before = list(persisted_before.artifacts)
        persisted_version_before = persisted_before.version

        # Install controlled failure
        monkeypatch.setattr(store, "save_context", fail_save_context)

        # Attempt artifact recording — expect failure
        with pytest.raises(PersistenceError, match="simulated persistence failure"):
            runtime.record_artifact(
                {"path": "src/should-not-persist.py", "type": "phantom"}
            )

        # --- Inspect live in-memory state ---
        live_artifacts = runtime.context.artifacts
        live_version = runtime.context.version
        live_state = runtime.context.process_state

        # --- Inspect persisted state ---
        monkeypatch.undo()
        persisted_after = store.load_context(pid)
        persisted_artifacts_after = list(persisted_after.artifacts)
        persisted_version_after = persisted_after.version

        # --- Fresh Runtime recovery ---
        fresh_runtime = Runtime(store, "recording-test-fresh")
        fresh_runtime.attach(pid)
        fresh_artifacts = list(fresh_runtime.context.artifacts)
        fresh_version = fresh_runtime.context.version

        # === Persisted state assertions ===
        assert persisted_artifacts_after == persisted_artifacts_before
        assert persisted_version_after == persisted_version_before

        # === Fresh Runtime assertions ===
        assert fresh_artifacts == persisted_artifacts_before
        assert fresh_version == persisted_version_before

        # === Live in-memory state assertions ===
        assert live_artifacts == prior_artifacts, (
            f"CONSISTENCY DEFECT: Live Runtime retains unpersisted artifact mutation. "
            f"Live artifacts: {live_artifacts}, expected: {prior_artifacts}"
        )
        assert live_version == prior_version, (
            f"CONSISTENCY DEFECT: Live Runtime version was mutated by failed persistence. "
            f"Live version: {live_version}, expected: {prior_version}"
        )
        assert live_state == prior_state, (
            f"CONSISTENCY DEFECT: Live process state changed after failed artifact persistence. "
            f"Live state: {live_state}, expected: {prior_state}"
        )


# =============================================================================
# VERIFICATION RECORDING TESTS
# =============================================================================


class TestVerificationStructuredPathSuccess:
    """Test the structured begin_verification() -> record_verification() path."""

    def test_structured_verification_records_result(self, tmp_path: Path):
        """Verification result is recorded in context.verification."""
        runtime = build_runtime(tmp_path)
        advance_to_verification(runtime)

        result = {"passed": True, "checks": ["unit tests", "lint"]}
        runtime.record_verification(result)

        assert runtime.context.verification == result

    def test_structured_verification_is_persisted(self, tmp_path: Path):
        """Verification result survives reload from persistence."""
        store = ProcessStore(tmp_path)
        runtime = Runtime(store, "recording-test")
        pid = runtime.create_process("Recording behavioral validation")
        advance_to_verification(runtime)

        result = {"passed": True, "checks": ["unit tests"]}
        runtime.record_verification(result)
        runtime.stop()

        runtime_b = Runtime(store, "recording-test-b")
        runtime_b.attach(pid)
        assert runtime_b.context.verification == result

    def test_structured_verification_generates_history_event(self, tmp_path: Path):
        """Verification recording produces a verification_recorded event."""
        store = ProcessStore(tmp_path)
        runtime = Runtime(store, "recording-test")
        pid = runtime.create_process("Recording behavioral validation")
        advance_to_verification(runtime)

        result = {"passed": True, "checks": ["unit tests"]}
        runtime.record_verification(result)

        history = store.history(pid)
        ver_events = [e for e in history if e["type"] == "verification_recorded"]
        assert len(ver_events) == 1
        assert ver_events[0]["result"] == result

    def test_structured_verification_preserves_verification_state(self, tmp_path: Path):
        """When already in VERIFICATION, record_verification keeps the state."""
        runtime = build_runtime(tmp_path)
        advance_to_verification(runtime)
        assert runtime.context.process_state == Runtime.VERIFICATION

        runtime.record_verification({"passed": True})
        assert runtime.context.process_state == Runtime.VERIFICATION

    def test_structured_verification_increments_version(self, tmp_path: Path):
        """Verification recording increments the context version."""
        runtime = build_runtime(tmp_path)
        advance_to_verification(runtime)
        prior_version = runtime.context.version

        runtime.record_verification({"passed": True})
        assert runtime.context.version == prior_version + 1

    def test_failed_verification_can_trigger_reconsideration(self, tmp_path: Path):
        """A failed verification result enables reconsideration."""
        runtime = build_runtime(tmp_path)
        advance_to_verification(runtime)
        runtime.record_verification({"passed": False, "failure": "tests failed"})

        runtime.reconsider({
            "description": "implementation must be reconsidered after failed verification"
        })

        assert runtime.context.process_state == Runtime.INVESTIGATION
        assert len(runtime.context.failure_uncertainty) > 0


class TestVerificationStructuredPathGuards:
    """Test begin_verification() guards."""

    def test_begin_verification_requires_implementation_state(self, tmp_path: Path):
        """begin_verification() requires IMPLEMENTATION state."""
        runtime = build_runtime(tmp_path)
        advance_to_investigation(runtime)
        with pytest.raises(RuntimeError):
            runtime.begin_verification()

    def test_begin_verification_requires_artifacts(self, tmp_path: Path):
        """begin_verification() requires at least one artifact."""
        runtime = build_runtime(tmp_path)
        advance_to_implementation(runtime)
        assert runtime.context.artifacts == []
        with pytest.raises(RuntimeError, match="artifact"):
            runtime.begin_verification()

    def test_begin_verification_requires_no_pending_execution(self, tmp_path: Path):
        """begin_verification() requires no pending execution work."""
        runtime = build_runtime(tmp_path)
        advance_to_implementation(runtime)
        runtime.record_artifact({"path": "src/feature.py"})
        runtime.set_pending_execution({"id": "W1", "status": "partial"})

        with pytest.raises(RuntimeError, match="pending"):
            runtime.begin_verification()

    def test_begin_verification_transitions_to_verification_state(self, tmp_path: Path):
        """begin_verification() sets process_state to VERIFICATION."""
        runtime = build_runtime(tmp_path)
        advance_to_implementation(runtime)
        runtime.record_artifact({"path": "src/feature.py"})
        runtime.begin_verification()
        assert runtime.context.process_state == Runtime.VERIFICATION

    def test_begin_verification_initializes_verification_dict(self, tmp_path: Path):
        """begin_verification() sets context.verification to an empty dict."""
        runtime = build_runtime(tmp_path)
        advance_to_implementation(runtime)
        runtime.record_artifact({"path": "src/feature.py"})
        runtime.begin_verification()
        assert runtime.context.verification == {}


class TestVerificationDirectPathSuccess:
    """Test the direct/legacy record_verification() path.

    The current implementation permits record_verification() from states:
    initial, implementation, and verification — without requiring
    begin_verification() to be called first.
    """

    def test_direct_verification_from_initial_state(self, tmp_path: Path):
        """Direct record_verification() works from initial state."""
        runtime = build_runtime(tmp_path)
        assert runtime.context.process_state == "initial"

        result = {"passed": True, "command": "pytest"}
        runtime.record_verification(result)

        assert runtime.context.verification == result
        # Direct path transitions to VERIFICATION state
        assert runtime.context.process_state == Runtime.VERIFICATION

    def test_direct_verification_from_implementation_state(self, tmp_path: Path):
        """Direct record_verification() works from implementation state."""
        runtime = build_runtime(tmp_path)
        advance_to_implementation(runtime)
        assert runtime.context.process_state == Runtime.IMPLEMENTATION

        result = {"passed": True, "command": "pytest"}
        runtime.record_verification(result)

        assert runtime.context.verification == result
        # Direct path transitions to VERIFICATION state
        assert runtime.context.process_state == Runtime.VERIFICATION

    def test_direct_verification_does_not_enforce_artifact_guard(self, tmp_path: Path):
        """Direct record_verification() does NOT require artifacts."""
        runtime = build_runtime(tmp_path)
        assert runtime.context.artifacts == []

        # This succeeds even without artifacts — unlike begin_verification()
        result = {"passed": True, "command": "pytest"}
        runtime.record_verification(result)
        assert runtime.context.verification == result

    def test_direct_verification_does_not_enforce_pending_execution_guard(
        self, tmp_path: Path
    ):
        """Direct record_verification() does NOT check pending_execution."""
        runtime = build_runtime(tmp_path)
        advance_to_implementation(runtime)
        runtime.record_artifact({"path": "src/feature.py"})
        runtime.set_pending_execution({"id": "W1", "status": "partial"})

        # This succeeds even with pending execution — unlike begin_verification()
        result = {"passed": True, "command": "pytest"}
        runtime.record_verification(result)
        assert runtime.context.verification == result

    def test_direct_verification_rejected_from_engineering_complete(self, tmp_path: Path):
        """Direct record_verification() is rejected from ENGINEERING_COMPLETE."""
        runtime = build_runtime(tmp_path)
        advance_to_verification(runtime)
        runtime.record_verification({"passed": True})
        runtime.recognize_engineering_completion(COMPLETION_RECOGNITION)
        assert runtime.context.process_state == Runtime.ENGINEERING_COMPLETE

        with pytest.raises(RuntimeError, match="completion"):
            runtime.record_verification({"passed": True, "command": "re-check"})

    def test_direct_verification_rejected_from_investigation_state(self, tmp_path: Path):
        """Direct record_verification() is rejected from INVESTIGATION state."""
        runtime = build_runtime(tmp_path)
        advance_to_investigation(runtime)
        assert runtime.context.process_state == Runtime.INVESTIGATION

        with pytest.raises(RuntimeError, match="completion"):
            runtime.record_verification({"passed": True, "command": "pytest"})


class TestVerificationPathDifferences:
    """Document and test the observable differences between structured and direct paths."""

    def test_structured_path_enforces_artifact_guard_direct_does_not(self, tmp_path: Path):
        """Structured path requires artifacts; direct path does not."""
        # Structured path
        runtime_s = build_runtime(tmp_path / "structured")
        advance_to_implementation(runtime_s)
        with pytest.raises(RuntimeError, match="artifact"):
            runtime_s.begin_verification()

        # Direct path from initial state with no artifacts
        runtime_d = build_runtime(tmp_path / "direct")
        assert runtime_d.context.artifacts == []
        runtime_d.record_verification({"passed": True})
        assert runtime_d.context.verification == {"passed": True}

    def test_structured_path_enforces_pending_guard_direct_does_not(self, tmp_path: Path):
        """Structured path requires no pending execution; direct path does not."""
        # Structured path
        runtime_s = build_runtime(tmp_path / "structured")
        advance_to_implementation(runtime_s)
        runtime_s.record_artifact({"path": "src/feature.py"})
        runtime_s.set_pending_execution({"id": "W1", "status": "partial"})
        with pytest.raises(RuntimeError, match="pending"):
            runtime_s.begin_verification()

        # Direct path — pending execution is ignored
        runtime_d = build_runtime(tmp_path / "direct")
        advance_to_implementation(runtime_d)
        runtime_d.record_artifact({"path": "src/feature.py"})
        runtime_d.set_pending_execution({"id": "W1", "status": "partial"})
        runtime_d.record_verification({"passed": True})
        assert runtime_d.context.verification == {"passed": True}

    def test_direct_path_accepts_initial_state_structured_does_not(self, tmp_path: Path):
        """Direct path allows recording from initial; structured requires IMPLEMENTATION."""
        # Structured path requires IMPLEMENTATION state
        runtime_s = build_runtime(tmp_path / "structured")
        with pytest.raises(RuntimeError):
            runtime_s.begin_verification()

        # Direct path works from initial
        runtime_d = build_runtime(tmp_path / "direct")
        runtime_d.record_verification({"passed": True})
        assert runtime_d.context.process_state == Runtime.VERIFICATION


class TestVerificationRecordingPersistenceFailure:
    """Test verification recording behavior when persistence fails."""

    def test_failed_verification_persistence_from_verification_state(
        self, tmp_path: Path, monkeypatch
    ):
        """Test persistence failure of record_verification() from VERIFICATION state.

        When already in VERIFICATION state, record_verification() only mutates
        context.verification (not process_state). Test whether this mutation
        is rolled back on persistence failure.
        """
        store = ProcessStore(tmp_path)
        runtime = Runtime(store, "recording-test")
        pid = runtime.create_process("Recording behavioral validation")
        advance_to_verification(runtime)

        # Establish pre-failure baseline
        prior_verification = dict(runtime.context.verification)
        prior_version = runtime.context.version
        prior_state = runtime.context.process_state
        assert prior_state == Runtime.VERIFICATION

        # Capture persisted baseline
        persisted_before = store.load_context(pid)
        persisted_verification_before = dict(persisted_before.verification)
        persisted_version_before = persisted_before.version

        # Install controlled failure
        monkeypatch.setattr(store, "save_context", fail_save_context)

        # Attempt verification recording
        with pytest.raises(PersistenceError, match="simulated persistence failure"):
            runtime.record_verification({"passed": True, "checks": ["phantom"]})

        # --- Inspect live in-memory state ---
        live_verification = runtime.context.verification
        live_version = runtime.context.version
        live_state = runtime.context.process_state

        # --- Inspect persisted state ---
        monkeypatch.undo()
        persisted_after = store.load_context(pid)
        persisted_verification_after = dict(persisted_after.verification)
        persisted_version_after = persisted_after.version

        # --- Fresh Runtime recovery ---
        fresh_runtime = Runtime(store, "recording-test-fresh")
        fresh_runtime.attach(pid)

        # === Persisted state assertions ===
        assert persisted_verification_after == persisted_verification_before
        assert persisted_version_after == persisted_version_before

        # === Fresh Runtime assertions ===
        assert dict(fresh_runtime.context.verification) == persisted_verification_before
        assert fresh_runtime.context.version == persisted_version_before

        # === Live in-memory state assertions ===
        assert live_verification == prior_verification, (
            f"CONSISTENCY DEFECT: Live Runtime retains unpersisted verification mutation. "
            f"Live verification: {live_verification}, expected: {prior_verification}"
        )
        assert live_version == prior_version, (
            f"CONSISTENCY DEFECT: Live Runtime version was mutated by failed persistence. "
            f"Live version: {live_version}, expected: {prior_version}"
        )
        assert live_state == prior_state, (
            f"CONSISTENCY DEFECT: Live process state changed after failed verification persistence. "
            f"Live state: {live_state}, expected: {prior_state}"
        )

    def test_failed_verification_persistence_with_state_transition(
        self, tmp_path: Path, monkeypatch
    ):
        """Test persistence failure of record_verification() when it also changes process_state.

        When called from IMPLEMENTATION or initial state, record_verification()
        also mutates process_state to VERIFICATION. Test whether BOTH mutations
        (verification result AND state transition) are rolled back.
        """
        store = ProcessStore(tmp_path)
        runtime = Runtime(store, "recording-test")
        pid = runtime.create_process("Recording behavioral validation")
        advance_to_implementation(runtime)

        # Establish pre-failure baseline
        prior_verification = dict(runtime.context.verification)
        prior_version = runtime.context.version
        prior_state = runtime.context.process_state
        assert prior_state == Runtime.IMPLEMENTATION

        # Capture persisted baseline
        persisted_before = store.load_context(pid)

        # Install controlled failure
        monkeypatch.setattr(store, "save_context", fail_save_context)

        # Attempt direct verification recording from IMPLEMENTATION state
        with pytest.raises(PersistenceError, match="simulated persistence failure"):
            runtime.record_verification({"passed": True, "checks": ["phantom"]})

        # --- Inspect live in-memory state ---
        live_verification = runtime.context.verification
        live_version = runtime.context.version
        live_state = runtime.context.process_state

        # --- Inspect persisted state ---
        monkeypatch.undo()
        persisted_after = store.load_context(pid)

        # --- Fresh Runtime recovery ---
        fresh_runtime = Runtime(store, "recording-test-fresh")
        fresh_runtime.attach(pid)

        # === Persisted state assertions ===
        assert dict(persisted_after.verification) == dict(persisted_before.verification)
        assert persisted_after.version == persisted_before.version
        assert persisted_after.process_state == persisted_before.process_state

        # === Fresh Runtime assertions ===
        assert fresh_runtime.context.process_state == persisted_before.process_state

        # === Live in-memory state assertions ===
        assert live_verification == prior_verification, (
            f"CONSISTENCY DEFECT: Live verification mutated. "
            f"Live: {live_verification}, expected: {prior_verification}"
        )
        assert live_version == prior_version, (
            f"CONSISTENCY DEFECT: Live version mutated. "
            f"Live: {live_version}, expected: {prior_version}"
        )
        assert live_state == prior_state, (
            f"CONSISTENCY DEFECT: Live process state mutated from {prior_state!r} "
            f"to {live_state!r} after failed persistence"
        )


# =============================================================================
# CROSS-CAPABILITY CONSISTENCY
# =============================================================================


class TestCrossCapabilityConsistency:
    """Compare persistence-failure behavior across recording operations."""

    def test_evidence_recording_has_caller_level_rollback(
        self, tmp_path: Path, monkeypatch
    ):
        """Baseline: observe() correctly rolls back on persistence failure.

        This reconfirms the existing evidence recording rollback behavior
        as the reference standard for comparing decision/artifact/verification.
        """
        store = ProcessStore(tmp_path)
        runtime = Runtime(store, "recording-test")
        pid = runtime.create_process("Cross-capability validation")

        prior_evidence = list(runtime.context.evidence)
        prior_version = runtime.context.version

        monkeypatch.setattr(store, "save_context", fail_save_context)

        with pytest.raises(PersistenceError):
            runtime.observe({
                "fact": "phantom evidence",
                "recognition": EVIDENCE_RECOGNITION,
            })

        # Evidence recording DOES roll back (established behavior)
        assert runtime.context.evidence == prior_evidence
        assert runtime.context.version == prior_version

    def test_decision_and_evidence_rollback_symmetry(
        self, tmp_path: Path, monkeypatch
    ):
        """Compare whether decision recording has the same rollback property as evidence.

        If this test fails, it confirms asymmetric rollback behavior between
        observe() and recognize_decision().
        """
        store = ProcessStore(tmp_path)
        runtime = Runtime(store, "recording-test")
        runtime.create_process("Cross-capability validation")

        prior_decisions = list(runtime.context.engineering_decisions)
        prior_version = runtime.context.version

        monkeypatch.setattr(store, "save_context", fail_save_context)

        with pytest.raises(PersistenceError):
            runtime.recognize_decision(
                {"id": "D-phantom"},
                DECISION_RECOGNITION,
            )

        # This asserts symmetric behavior with evidence recording.
        # If it fails, the asymmetry is the defect.
        assert runtime.context.engineering_decisions == prior_decisions, (
            "ASYMMETRY: Decision recording does NOT roll back like evidence recording"
        )
        assert runtime.context.version == prior_version, (
            "ASYMMETRY: Decision recording version NOT rolled back like evidence recording"
        )

    def test_artifact_and_evidence_rollback_symmetry(
        self, tmp_path: Path, monkeypatch
    ):
        """Compare whether artifact recording has the same rollback property as evidence."""
        store = ProcessStore(tmp_path)
        runtime = Runtime(store, "recording-test")
        runtime.create_process("Cross-capability validation")
        advance_to_implementation(runtime)

        prior_artifacts = list(runtime.context.artifacts)
        prior_version = runtime.context.version

        monkeypatch.setattr(store, "save_context", fail_save_context)

        with pytest.raises(PersistenceError):
            runtime.record_artifact({"path": "phantom.py"})

        assert runtime.context.artifacts == prior_artifacts, (
            "ASYMMETRY: Artifact recording does NOT roll back like evidence recording"
        )
        assert runtime.context.version == prior_version, (
            "ASYMMETRY: Artifact recording version NOT rolled back like evidence recording"
        )

    def test_verification_and_evidence_rollback_symmetry(
        self, tmp_path: Path, monkeypatch
    ):
        """Compare whether verification recording has the same rollback property as evidence."""
        store = ProcessStore(tmp_path)
        runtime = Runtime(store, "recording-test")
        runtime.create_process("Cross-capability validation")
        advance_to_verification(runtime)

        prior_verification = dict(runtime.context.verification)
        prior_version = runtime.context.version

        monkeypatch.setattr(store, "save_context", fail_save_context)

        with pytest.raises(PersistenceError):
            runtime.record_verification({"passed": True, "checks": ["phantom"]})

        assert runtime.context.verification == prior_verification, (
            "ASYMMETRY: Verification recording does NOT roll back like evidence recording"
        )
        assert runtime.context.version == prior_version, (
            "ASYMMETRY: Verification recording version NOT rolled back like evidence recording"
        )
