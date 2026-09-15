"""Focused tests for the Agent–Runtime Bridge.

These tests establish that the bridge delegates authority to the Runtime
rather than recreating Runtime behavior.  They do not duplicate the full
Runtime test suite.

Test coverage:
  1.  Process Instance creation
  2.  Returned Process Instance identity
  3.  Authoritative Context retrieval
  4.  Known-ID attachment
  5.  Context recovery after attachment
  6.  Supported Runtime dispatch (full lifecycle)
  7.  Authoritative result/state return
  8.  Unknown Process Instance ID
  9.  Unsupported operation
  10. Invalid parameters
  11. Runtime guard rejection
  12. Persistence failure
  13. Unsupported discovery
  14. Bridge recreation + known-ID continuation
  15. Absence of bridge-owned persistence
"""
from __future__ import annotations

import pytest
from pathlib import Path

from bridge.agent_runtime_bridge import AgentRuntimeBridge
from runtime.core.store import ProcessStore


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def store(tmp_path: Path) -> ProcessStore:
    """Provide a fresh ProcessStore rooted in a temp directory."""
    return ProcessStore(tmp_path)


@pytest.fixture
def bridge(store: ProcessStore) -> AgentRuntimeBridge:
    """Provide a fresh bridge with a fresh store."""
    return AgentRuntimeBridge(store, runtime_id="test-bridge")


@pytest.fixture
def bridge_with_process(bridge: AgentRuntimeBridge) -> tuple[AgentRuntimeBridge, str]:
    """Provide a bridge with an already-created Process Instance."""
    result = bridge.create_process("Test engineering objective")
    assert result["success"] is True
    return bridge, result["process_instance_id"]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

RECOGNITION = {"recognized": True, "basis": "Test basis for recognition"}

OBSERVATION = {
    "fact": "The component uses SELECT query type",
    "source": "code inspection",
    "recognition": RECOGNITION,
}

DECISION = {"description": "Change query type from SELECT to POST_SELECT"}

ARTIFACT = {"type": "code_change", "path": "test_file.php", "description": "Changed query type"}

VERIFICATION_PASS = {"passed": True, "method": "manual_review", "details": "Verified correct"}

COMPLETION = {"recognized": True, "basis": "All verification passed"}


# ---------------------------------------------------------------------------
# 1. Process Instance creation
# ---------------------------------------------------------------------------

class TestProcessInstanceCreation:
    def test_create_returns_success(self, bridge: AgentRuntimeBridge) -> None:
        result = bridge.create_process("Build feature X")
        assert result["success"] is True

    def test_create_returns_process_instance_id(self, bridge: AgentRuntimeBridge) -> None:
        result = bridge.create_process("Build feature X")
        assert result["process_instance_id"] is not None
        assert isinstance(result["process_instance_id"], str)
        assert len(result["process_instance_id"]) > 0

    def test_create_returns_authoritative_context(self, bridge: AgentRuntimeBridge) -> None:
        result = bridge.create_process("Build feature X")
        assert result["context"] is not None
        assert result["context"]["engineering_objective"] == "Build feature X"
        assert result["context"]["process_state"] == "initial"

    def test_create_returns_process_instance_state(self, bridge: AgentRuntimeBridge) -> None:
        result = bridge.create_process("Build feature X")
        assert result["process_instance"] is not None
        assert result["process_instance"]["lifecycle"] == "active"

    def test_create_with_empty_objective_fails(self, bridge: AgentRuntimeBridge) -> None:
        result = bridge.create_process("")
        assert result["success"] is False
        assert result["error"]["type"] == "bridge_error"

    def test_create_with_whitespace_objective_fails(self, bridge: AgentRuntimeBridge) -> None:
        result = bridge.create_process("   ")
        assert result["success"] is False
        assert result["error"]["type"] == "bridge_error"


# ---------------------------------------------------------------------------
# 2. Returned Process Instance identity
# ---------------------------------------------------------------------------

class TestProcessInstanceIdentity:
    def test_identity_matches_context(self, bridge: AgentRuntimeBridge) -> None:
        result = bridge.create_process("Identity test")
        assert result["process_instance_id"] == result["context"]["process_instance_id"]

    def test_identity_matches_process_instance(self, bridge: AgentRuntimeBridge) -> None:
        result = bridge.create_process("Identity test")
        assert result["process_instance_id"] == result["process_instance"]["process_instance_id"]


# ---------------------------------------------------------------------------
# 3. Authoritative Context retrieval
# ---------------------------------------------------------------------------

class TestContextRetrieval:
    def test_get_context_returns_success(
        self, bridge_with_process: tuple[AgentRuntimeBridge, str]
    ) -> None:
        bridge, pid = bridge_with_process
        result = bridge.get_context()
        assert result["success"] is True

    def test_get_context_returns_all_fields(
        self, bridge_with_process: tuple[AgentRuntimeBridge, str]
    ) -> None:
        bridge, pid = bridge_with_process
        result = bridge.get_context()
        ctx = result["context"]
        # All 21 EC fields must be present
        expected_fields = {
            "process_instance_id", "engineering_objective", "process_state",
            "execution_mode", "requirements", "constraints", "evidence",
            "assumptions", "risks", "candidate_solutions", "engineering_decisions",
            "decision_gates", "artifacts", "verification", "unresolved_matters",
            "pending_execution", "execution_determination", "failure_uncertainty",
            "engineering_completion", "version", "updated_at",
        }
        assert expected_fields.issubset(ctx.keys())

    def test_get_context_without_attachment_fails(self, bridge: AgentRuntimeBridge) -> None:
        result = bridge.get_context()
        assert result["success"] is False
        assert result["error"]["type"] == "bridge_error"


# ---------------------------------------------------------------------------
# 4. Known-ID attachment
# ---------------------------------------------------------------------------

class TestKnownIdAttachment:
    def test_attach_returns_success(self, store: ProcessStore) -> None:
        # Create via one bridge, attach via another.
        bridge_a = AgentRuntimeBridge(store, runtime_id="bridge-a")
        create_result = bridge_a.create_process("Attach test")
        pid = create_result["process_instance_id"]

        bridge_b = AgentRuntimeBridge(store, runtime_id="bridge-b")
        attach_result = bridge_b.attach(pid)
        assert attach_result["success"] is True

    def test_attach_returns_correct_identity(self, store: ProcessStore) -> None:
        bridge_a = AgentRuntimeBridge(store, runtime_id="bridge-a")
        create_result = bridge_a.create_process("Attach test")
        pid = create_result["process_instance_id"]

        bridge_b = AgentRuntimeBridge(store, runtime_id="bridge-b")
        attach_result = bridge_b.attach(pid)
        assert attach_result["process_instance_id"] == pid

    def test_attach_with_empty_id_fails(self, bridge: AgentRuntimeBridge) -> None:
        result = bridge.attach("")
        assert result["success"] is False
        assert result["error"]["type"] == "bridge_error"


# ---------------------------------------------------------------------------
# 5. Context recovery after attachment
# ---------------------------------------------------------------------------

class TestContextRecovery:
    def test_recovered_context_matches_original(self, store: ProcessStore) -> None:
        bridge_a = AgentRuntimeBridge(store, runtime_id="bridge-a")
        create_result = bridge_a.create_process("Recovery test objective")
        pid = create_result["process_instance_id"]
        original_objective = create_result["context"]["engineering_objective"]

        bridge_b = AgentRuntimeBridge(store, runtime_id="bridge-b")
        attach_result = bridge_b.attach(pid)
        assert attach_result["context"]["engineering_objective"] == original_objective
        assert attach_result["context"]["process_instance_id"] == pid

    def test_recovered_context_reflects_mutations(self, store: ProcessStore) -> None:
        """Mutations made via bridge A must be visible after bridge B attaches."""
        bridge_a = AgentRuntimeBridge(store, runtime_id="bridge-a")
        create_result = bridge_a.create_process("Mutation recovery test")
        pid = create_result["process_instance_id"]

        # Mutate through bridge A.
        bridge_a.dispatch("start_investigation")
        bridge_a.dispatch("observe", {"observation": OBSERVATION})

        # Attach via a fresh bridge B.
        bridge_b = AgentRuntimeBridge(store, runtime_id="bridge-b")
        attach_result = bridge_b.attach(pid)
        assert attach_result["context"]["process_state"] == "investigation"
        assert len(attach_result["context"]["evidence"]) == 1


# ---------------------------------------------------------------------------
# 6. Supported Runtime dispatch (full lifecycle)
# ---------------------------------------------------------------------------

class TestRuntimeDispatch:
    def test_full_lifecycle_dispatch(
        self, bridge_with_process: tuple[AgentRuntimeBridge, str]
    ) -> None:
        """Drive through the entire first vertical slice lifecycle."""
        bridge, pid = bridge_with_process

        # initial → investigation
        r = bridge.dispatch("start_investigation")
        assert r["success"] is True
        assert r["context"]["process_state"] == "investigation"

        # observe
        r = bridge.dispatch("observe", {"observation": OBSERVATION})
        assert r["success"] is True
        assert len(r["context"]["evidence"]) == 1

        # recognize_decision
        r = bridge.dispatch("recognize_decision", {
            "decision": DECISION,
            "recognition": RECOGNITION,
        })
        assert r["success"] is True
        assert len(r["context"]["engineering_decisions"]) == 1

        # investigation → implementation
        r = bridge.dispatch("begin_implementation")
        assert r["success"] is True
        assert r["context"]["process_state"] == "implementation"

        # record_artifact
        r = bridge.dispatch("record_artifact", {"artifact": ARTIFACT})
        assert r["success"] is True
        assert len(r["context"]["artifacts"]) == 1

        # implementation → verification
        r = bridge.dispatch("begin_verification")
        assert r["success"] is True
        assert r["context"]["process_state"] == "verification"

        # record_verification
        r = bridge.dispatch("record_verification", {"result": VERIFICATION_PASS})
        assert r["success"] is True
        assert r["context"]["verification"]["passed"] is True

        # verification → engineering_complete
        r = bridge.dispatch("recognize_engineering_completion", {
            "completion": COMPLETION,
        })
        assert r["success"] is True
        assert r["context"]["process_state"] == "engineering_complete"
        assert r["context"]["engineering_completion"] is True


# ---------------------------------------------------------------------------
# 7. Authoritative result/state return
# ---------------------------------------------------------------------------

class TestAuthoritativeReturn:
    def test_every_dispatch_returns_updated_state(
        self, bridge_with_process: tuple[AgentRuntimeBridge, str]
    ) -> None:
        bridge, pid = bridge_with_process
        r1 = bridge.dispatch("start_investigation")
        v1 = r1["context"]["version"]

        r2 = bridge.dispatch("observe", {"observation": OBSERVATION})
        v2 = r2["context"]["version"]
        assert v2 > v1, "version must increase after mutation"

    def test_result_includes_process_instance_id(
        self, bridge_with_process: tuple[AgentRuntimeBridge, str]
    ) -> None:
        bridge, pid = bridge_with_process
        r = bridge.dispatch("start_investigation")
        assert r["process_instance_id"] == pid


# ---------------------------------------------------------------------------
# 8. Unknown Process Instance ID
# ---------------------------------------------------------------------------

class TestUnknownProcessInstanceId:
    def test_attach_unknown_id_fails(self, bridge: AgentRuntimeBridge) -> None:
        result = bridge.attach("00000000-0000-0000-0000-000000000000")
        assert result["success"] is False
        assert result["error"]["type"] == "persistence_error"

    def test_attach_unknown_id_returns_useful_message(self, bridge: AgentRuntimeBridge) -> None:
        result = bridge.attach("nonexistent-id")
        assert result["success"] is False
        assert result["error"]["message"]  # Must be non-empty


# ---------------------------------------------------------------------------
# 9. Unsupported operation
# ---------------------------------------------------------------------------

class TestUnsupportedOperation:
    def test_unsupported_operation_fails(
        self, bridge_with_process: tuple[AgentRuntimeBridge, str]
    ) -> None:
        bridge, pid = bridge_with_process
        result = bridge.dispatch("nonexistent_operation")
        assert result["success"] is False
        assert result["error"]["type"] == "bridge_error"
        assert "unsupported" in result["error"]["message"].lower()

    def test_empty_operation_fails(
        self, bridge_with_process: tuple[AgentRuntimeBridge, str]
    ) -> None:
        bridge, pid = bridge_with_process
        result = bridge.dispatch("")
        assert result["success"] is False


# ---------------------------------------------------------------------------
# 10. Invalid parameters
# ---------------------------------------------------------------------------

class TestInvalidParameters:
    def test_missing_required_params(
        self, bridge_with_process: tuple[AgentRuntimeBridge, str]
    ) -> None:
        bridge, pid = bridge_with_process
        bridge.dispatch("start_investigation")
        # observe requires 'observation' param
        result = bridge.dispatch("observe", {})
        assert result["success"] is False
        assert result["error"]["type"] == "bridge_error"
        assert "missing" in result["error"]["message"].lower()

    def test_invalid_observation_type(
        self, bridge_with_process: tuple[AgentRuntimeBridge, str]
    ) -> None:
        bridge, pid = bridge_with_process
        bridge.dispatch("start_investigation")
        result = bridge.dispatch("observe", {"observation": "not-a-dict"})
        assert result["success"] is False
        assert result["error"]["type"] == "runtime_error"


# ---------------------------------------------------------------------------
# 11. Runtime guard rejection
# ---------------------------------------------------------------------------

class TestRuntimeGuardRejection:
    def test_begin_implementation_without_decision_rejected(
        self, bridge_with_process: tuple[AgentRuntimeBridge, str]
    ) -> None:
        bridge, pid = bridge_with_process
        bridge.dispatch("start_investigation")
        result = bridge.dispatch("begin_implementation")
        assert result["success"] is False
        assert result["error"]["type"] == "runtime_error"
        assert "decision" in result["error"]["message"].lower()
        # State must remain investigation (bridge does not change it)
        assert result["context"]["process_state"] == "investigation"

    def test_dispatch_without_attachment_rejected(
        self, bridge: AgentRuntimeBridge
    ) -> None:
        result = bridge.dispatch("start_investigation")
        assert result["success"] is False
        assert result["error"]["type"] == "bridge_error"

    def test_wrong_state_transition_rejected(
        self, bridge_with_process: tuple[AgentRuntimeBridge, str]
    ) -> None:
        """Attempting begin_implementation from initial state must fail."""
        bridge, pid = bridge_with_process
        result = bridge.dispatch("begin_implementation")
        assert result["success"] is False
        assert result["error"]["type"] == "runtime_error"


# ---------------------------------------------------------------------------
# 12. Persistence failure
# ---------------------------------------------------------------------------

class TestPersistenceFailure:
    def test_persistence_failure_returns_error(
        self,
        bridge_with_process: tuple[AgentRuntimeBridge, str],
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        bridge, pid = bridge_with_process
        bridge.dispatch("start_investigation")

        # Inject persistence failure.
        def failing_save(*args, **kwargs):
            from runtime.persistence.json_store import PersistenceError
            raise PersistenceError("simulated persistence failure")

        monkeypatch.setattr(bridge._runtime.store, "save_context", failing_save)

        result = bridge.dispatch("observe", {"observation": OBSERVATION})
        assert result["success"] is False
        assert result["error"]["type"] == "persistence_error"
        assert "simulated" in result["error"]["message"]


# ---------------------------------------------------------------------------
# 13. Unsupported discovery
# ---------------------------------------------------------------------------

class TestUnsupportedDiscovery:
    def test_discover_returns_unsupported(self) -> None:
        result = AgentRuntimeBridge.discover("Find existing process for objective X")
        assert result["success"] is False
        assert result["error"]["type"] == "unsupported_capability"
        assert "discovery" in result["error"]["message"].lower()


# ---------------------------------------------------------------------------
# 14. Bridge recreation + known-ID continuation
# ---------------------------------------------------------------------------

class TestBridgeContinuation:
    def test_continuation_across_bridge_instances(self, store: ProcessStore) -> None:
        """Demonstrate that Process Instance continuity belongs to Runtime
        persistence, not bridge memory."""
        # Bridge A creates and mutates.
        bridge_a = AgentRuntimeBridge(store, runtime_id="bridge-a")
        create_result = bridge_a.create_process("Continuation test")
        pid = create_result["process_instance_id"]
        bridge_a.dispatch("start_investigation")
        bridge_a.dispatch("observe", {"observation": OBSERVATION})

        # Bridge A is destroyed.
        del bridge_a

        # Bridge B attaches and continues.
        bridge_b = AgentRuntimeBridge(store, runtime_id="bridge-b")
        attach_result = bridge_b.attach(pid)
        assert attach_result["success"] is True
        assert attach_result["context"]["process_state"] == "investigation"
        assert len(attach_result["context"]["evidence"]) == 1

        # Bridge B can continue dispatching.
        r = bridge_b.dispatch("recognize_decision", {
            "decision": DECISION,
            "recognition": RECOGNITION,
        })
        assert r["success"] is True
        assert len(r["context"]["engineering_decisions"]) == 1


# ---------------------------------------------------------------------------
# 15. Absence of bridge-owned persistence
# ---------------------------------------------------------------------------

class TestNoBridgePersistence:
    def test_bridge_has_no_persistence_attributes(
        self, bridge: AgentRuntimeBridge
    ) -> None:
        """The bridge must not have its own persistence mechanism."""
        # The bridge should not have attributes indicating its own storage.
        bridge_attrs = set(dir(bridge))
        forbidden_patterns = {"_store", "_db", "_cache", "_index", "_registry", "_persist"}
        own_persistence = forbidden_patterns.intersection(bridge_attrs)
        assert own_persistence == set(), (
            f"bridge has persistence-like attributes: {own_persistence}"
        )

    def test_bridge_state_does_not_survive_recreation(
        self, store: ProcessStore
    ) -> None:
        """Creating a new bridge must not carry forward state from a previous
        bridge instance."""
        bridge_a = AgentRuntimeBridge(store, runtime_id="bridge-a")
        bridge_a.create_process("Ephemeral bridge test")

        bridge_b = AgentRuntimeBridge(store, runtime_id="bridge-b")
        # Bridge B must not be attached to anything.
        result = bridge_b.get_context()
        assert result["success"] is False

    def test_destroying_bridge_does_not_destroy_process_instance(
        self, store: ProcessStore
    ) -> None:
        """Destroying a bridge must not destroy the persisted Process Instance."""
        bridge_a = AgentRuntimeBridge(store, runtime_id="bridge-a")
        create_result = bridge_a.create_process("Persistence test")
        pid = create_result["process_instance_id"]
        del bridge_a

        # The Process Instance must still be loadable.
        bridge_b = AgentRuntimeBridge(store, runtime_id="bridge-b")
        attach_result = bridge_b.attach(pid)
        assert attach_result["success"] is True
        assert attach_result["process_instance_id"] == pid
