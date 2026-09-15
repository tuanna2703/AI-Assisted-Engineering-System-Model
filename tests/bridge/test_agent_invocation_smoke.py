"""Agent-facing invocation smoke test for the Agent–Runtime Bridge.

This test demonstrates that the bridge entry point is executable through a
concrete Agent-facing invocation surface.  It exercises the same path an
Agent would invoke:

    Agent-side invocation → Bridge entry point → Runtime →
    persistent Process Instance → authoritative Context/result →
    Bridge response

The test performs:
  1. Create a Process Instance via bridge
  2. Capture its ID
  3. Terminate the first bridge/harness instance
  4. Create a second bridge/harness instance
  5. Attach using the known ID
  6. Obtain Context
  7. Dispatch a supported Runtime operation
  8. Verify the resulting authoritative state

IMPORTANT: This smoke test is implementation evidence.  It does not
establish that a particular IDE, MCP implementation, or other Execution
Environment mechanism is the normative AESM architecture.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from bridge.agent_runtime_bridge import AgentRuntimeBridge
from runtime.core.store import ProcessStore


RECOGNITION = {"recognized": True, "basis": "Smoke test engineering basis"}


class TestAgentInvocationSmokeTest:
    """End-to-end Agent-facing invocation demonstration."""

    def test_agent_invocation_lifecycle(self, tmp_path: Path) -> None:
        """Simulate an Agent invoking the bridge entry point end-to-end."""

        # ── Step 1: Agent creates a Process Instance ──────────────────────
        store = ProcessStore(tmp_path)
        bridge_1 = AgentRuntimeBridge(store, runtime_id="agent-session-1")

        create_result = bridge_1.create_process(
            "Change business_id query type from SELECT to POST_SELECT in Add_Review_Form"
        )
        assert create_result["success"] is True, (
            f"Process creation failed: {create_result['error']}"
        )

        # ── Step 2: Capture the Process Instance ID ───────────────────────
        pid = create_result["process_instance_id"]
        assert pid is not None
        assert isinstance(pid, str)
        assert len(pid) > 0

        # Verify initial authoritative state.
        assert create_result["context"]["process_state"] == "initial"
        assert create_result["process_instance"]["lifecycle"] == "active"

        # ── Step 3: Terminate the first bridge instance ───────────────────
        # (Simulates Agent session ending — the bridge is disposable)
        del bridge_1

        # ── Step 4: Create a second bridge instance ───────────────────────
        bridge_2 = AgentRuntimeBridge(store, runtime_id="agent-session-2")

        # ── Step 5: Attach using the known ID ─────────────────────────────
        attach_result = bridge_2.attach(pid)
        assert attach_result["success"] is True, (
            f"Attachment failed: {attach_result['error']}"
        )
        assert attach_result["process_instance_id"] == pid

        # ── Step 6: Obtain Context ────────────────────────────────────────
        context_result = bridge_2.get_context()
        assert context_result["success"] is True
        assert context_result["context"]["process_state"] == "initial"
        assert context_result["context"]["engineering_objective"] == (
            "Change business_id query type from SELECT to POST_SELECT in Add_Review_Form"
        )

        # ── Step 7: Dispatch supported Runtime operations ─────────────────
        # Start investigation.
        r = bridge_2.dispatch("start_investigation")
        assert r["success"] is True
        assert r["context"]["process_state"] == "investigation"

        # Record evidence.
        r = bridge_2.dispatch("observe", {
            "observation": {
                "fact": "AddReviewForm uses SELECT query type for business_id",
                "source": "code_inspection",
                "recognition": RECOGNITION,
            },
        })
        assert r["success"] is True
        assert len(r["context"]["evidence"]) == 1

        # Recognize a decision.
        r = bridge_2.dispatch("recognize_decision", {
            "decision": {
                "description": "Change query type from SELECT to POST_SELECT",
                "rationale": "POST_SELECT allows post-submission data access",
            },
            "recognition": RECOGNITION,
        })
        assert r["success"] is True

        # Begin implementation.
        r = bridge_2.dispatch("begin_implementation")
        assert r["success"] is True

        # Record artifact.
        r = bridge_2.dispatch("record_artifact", {
            "artifact": {
                "type": "code_change",
                "path": "includes/AddReviewForm.php",
                "description": "Changed business_id from SELECT to POST_SELECT",
            },
        })
        assert r["success"] is True

        # Begin verification.
        r = bridge_2.dispatch("begin_verification")
        assert r["success"] is True

        # Record verification.
        r = bridge_2.dispatch("record_verification", {
            "result": {
                "passed": True,
                "method": "functional_test",
                "details": "business_id now correctly uses POST_SELECT",
            },
        })
        assert r["success"] is True

        # Recognize engineering completion.
        r = bridge_2.dispatch("recognize_engineering_completion", {
            "completion": {
                "recognized": True,
                "basis": "All verification criteria passed",
            },
        })
        assert r["success"] is True

        # ── Step 8: Verify resulting authoritative state ──────────────────
        final = bridge_2.get_context()
        assert final["success"] is True
        assert final["process_instance_id"] == pid
        assert final["context"]["process_state"] == "engineering_complete"
        assert final["context"]["engineering_completion"] is True
        assert len(final["context"]["evidence"]) == 1
        assert len(final["context"]["engineering_decisions"]) == 1
        assert len(final["context"]["artifacts"]) == 1
        assert final["context"]["verification"]["passed"] is True
        assert final["process_instance"]["lifecycle"] == "active"

    def test_discovery_is_explicitly_deferred(self) -> None:
        """An Agent attempt at objective-based discovery returns a clear
        unsupported-capability response rather than silently failing."""
        result = AgentRuntimeBridge.discover(
            "Find existing process for business_id change"
        )
        assert result["success"] is False
        assert result["error"]["type"] == "unsupported_capability"
        assert "discovery" in result["error"]["message"].lower()
        assert "create_process" in result["error"]["message"]
        assert "attach" in result["error"]["message"]
