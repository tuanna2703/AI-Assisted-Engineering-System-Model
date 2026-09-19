"""Targeted bridge validation for the authorized ``reconsider`` capability.

These tests verify the bridge boundary only. Runtime semantics remain owned by
``runtime.core.runtime.Runtime.reconsider`` and are not duplicated here.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from bridge.agent_runtime_bridge import AgentRuntimeBridge
from runtime.core import ActiveRepositoryContext
from runtime.core.store import ProcessStore


RECOGNITION = {"recognized": True, "basis": "targeted bridge test"}
DECISION = {"description": "Targeted bridge reconsideration decision"}
ARTIFACT = {"type": "test_artifact", "path": "tests/bridge/test_reconsider_dispatch.py"}
FAILED_VERIFICATION = {
    "passed": False,
    "method": "targeted_test",
    "details": "The targeted verification intentionally failed to exercise reconsideration.",
}
RECONSIDERATION_REASON = {
    "description": "Verification identified unresolved behavior requiring renewed investigation.",
    "source": "targeted bridge validation",
}


@pytest.fixture
def store(tmp_path: Path) -> ActiveRepositoryContext:
    return ActiveRepositoryContext(tmp_path)


@pytest.fixture
def verification_ready_bridge(store: ActiveRepositoryContext) -> AgentRuntimeBridge:
    bridge = AgentRuntimeBridge(store, runtime_id="reconsider-test")
    assert bridge.create_process("Test reconsider bridge dispatch")["success"] is True
    assert bridge.dispatch("start_investigation")["success"] is True
    assert bridge.dispatch(
        "recognize_decision",
        {"decision": DECISION, "recognition": RECOGNITION},
    )["success"] is True
    assert bridge.dispatch("begin_implementation")["success"] is True
    assert bridge.dispatch("record_artifact", {"artifact": ARTIFACT})["success"] is True
    assert bridge.dispatch("begin_verification")["success"] is True
    assert bridge.dispatch(
        "record_verification", {"result": FAILED_VERIFICATION}
    )["success"] is True
    return bridge


def test_reconsider_is_dispatchable_and_preserves_runtime_semantics(
    verification_ready_bridge: AgentRuntimeBridge,
) -> None:
    result = verification_ready_bridge.dispatch(
        "reconsider", {"reason": RECONSIDERATION_REASON}
    )

    assert result["success"] is True
    assert result["context"]["process_state"] == "investigation"
    assert RECONSIDERATION_REASON in result["context"]["failure_uncertainty"]
    assert RECONSIDERATION_REASON["description"] in result["context"]["unresolved_matters"]


def test_reconsider_argument_is_propagated_to_runtime(
    verification_ready_bridge: AgentRuntimeBridge,
) -> None:
    result = verification_ready_bridge.dispatch(
        "reconsider", {"reason": RECONSIDERATION_REASON}
    )

    assert result["success"] is True
    assert result["context"]["failure_uncertainty"][-1] == RECONSIDERATION_REASON


def test_successful_verification_rejection_is_propagated(
    store: ProcessStore,
) -> None:
    bridge = AgentRuntimeBridge(store, runtime_id="reconsider-rejection-test")
    assert bridge.create_process("Test successful verification rejection")["success"] is True
    assert bridge.dispatch("start_investigation")["success"] is True
    assert bridge.dispatch(
        "recognize_decision",
        {"decision": DECISION, "recognition": RECOGNITION},
    )["success"] is True
    assert bridge.dispatch("begin_implementation")["success"] is True
    assert bridge.dispatch("record_artifact", {"artifact": ARTIFACT})["success"] is True
    assert bridge.dispatch("begin_verification")["success"] is True
    assert bridge.dispatch(
        "record_verification",
        {"result": {"passed": True, "method": "targeted_test"}},
    )["success"] is True

    result = bridge.dispatch(
        "reconsider", {"reason": RECONSIDERATION_REASON}
    )

    assert result["success"] is False
    assert result["error"]["type"] == "runtime_error"
    assert "successful verification" in result["error"]["message"]
    assert result["context"]["process_state"] == "verification"


def test_invalid_reconsideration_reason_is_rejected_by_runtime_without_mutation(
    verification_ready_bridge: AgentRuntimeBridge,
    store: ProcessStore,
) -> None:
    before = verification_ready_bridge.get_context()
    assert before["success"] is True
    process_instance_id = before["process_instance_id"]
    persisted_before = store.load_context(process_instance_id).to_dict()
    history_before = store.history(process_instance_id)

    result = verification_ready_bridge.dispatch(
        "reconsider", {"reason": {"source": "missing description"}}
    )

    assert result["success"] is False
    assert result["error"]["type"] == "runtime_error"
    assert "descriptive reason" in result["error"]["message"]
    assert result["context"]["process_state"] == "verification"
    assert result["context"] == before["context"]
    assert store.load_context(process_instance_id).to_dict() == persisted_before
    assert store.history(process_instance_id) == history_before


def test_set_pending_execution_remains_outside_bridge_boundary(
    verification_ready_bridge: AgentRuntimeBridge,
) -> None:
    result = verification_ready_bridge.dispatch(
        "set_pending_execution", {"work": {"id": "SHOULD-NOT-BE-EXPOSED"}}
    )

    assert result["success"] is False
    assert result["error"]["type"] == "bridge_error"
    assert "unsupported operation" in result["error"]["message"]
    assert result["context"] is None
    assert result["process_instance"] is None
    assert result["process_instance_id"] is None
