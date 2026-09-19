"""Dedicated continuity demonstration for the Agent–Runtime Bridge.

This test demonstrates that Process Instance continuity belongs to
Runtime persistence, not bridge memory, by exercising the full sequence:

    Bridge A → create Process Instance → Runtime persists →
    Bridge A destroyed → Bridge B → attach(pid) → Runtime recovers →
    get_context → dispatch → verify resulting authoritative state

The test must pass without any bridge-owned persistence mechanism.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from bridge.agent_runtime_bridge import AgentRuntimeBridge
from runtime.core import ActiveRepositoryContext
from runtime.core.store import ProcessStore


RECOGNITION = {"recognized": True, "basis": "Continuity demonstration basis"}


class TestContinuityDemonstration:
    """End-to-end continuity across separate bridge instances."""

    def test_full_continuity_sequence(self, tmp_path: Path) -> None:
        """The canonical continuity demonstration required by the contract."""
        ctx = ActiveRepositoryContext(tmp_path)

        # ── Bridge A: create and advance ──────────────────────────────────
        bridge_a = AgentRuntimeBridge(ctx, runtime_id="continuity-bridge-a")

        create_result = bridge_a.create_process(
            "Demonstrate cross-bridge continuity"
        )
        assert create_result["success"] is True
        pid = create_result["process_instance_id"]

        # Advance through investigation.
        r = bridge_a.dispatch("start_investigation")
        assert r["success"] is True

        r = bridge_a.dispatch("observe", {
            "observation": {
                "fact": "Component uses SELECT query type",
                "source": "code review",
                "recognition": RECOGNITION,
            },
        })
        assert r["success"] is True

        r = bridge_a.dispatch("recognize_decision", {
            "decision": {
                "description": "Change to POST_SELECT",
                "rationale": "POST_SELECT is the correct query type",
            },
            "recognition": RECOGNITION,
        })
        assert r["success"] is True

        # Record the state before Bridge A ends.
        state_after_a = bridge_a.get_context()
        assert state_after_a["success"] is True
        assert state_after_a["context"]["process_state"] == "investigation"
        assert len(state_after_a["context"]["evidence"]) == 1
        assert len(state_after_a["context"]["engineering_decisions"]) == 1

        # ── Bridge A is destroyed ─────────────────────────────────────────
        del bridge_a

        # ── Bridge B: recover and continue ────────────────────────────────
        bridge_b = AgentRuntimeBridge(ctx, runtime_id="continuity-bridge-b")

        # Attach using the known Process Instance ID.
        attach_result = bridge_b.attach(pid)
        assert attach_result["success"] is True
        assert attach_result["process_instance_id"] == pid

        # Verify that the recovered state matches what Bridge A produced.
        recovered_ctx = attach_result["context"]
        assert recovered_ctx["process_state"] == "investigation"
        assert recovered_ctx["engineering_objective"] == "Demonstrate cross-bridge continuity"
        assert len(recovered_ctx["evidence"]) == 1
        assert len(recovered_ctx["engineering_decisions"]) == 1

        # Continue the engineering process through Bridge B.
        r = bridge_b.dispatch("begin_implementation")
        assert r["success"] is True
        assert r["context"]["process_state"] == "implementation"

        r = bridge_b.dispatch("record_artifact", {
            "artifact": {
                "type": "code_change",
                "path": "includes/AddReviewForm.php",
                "description": "Changed business_id query from SELECT to POST_SELECT",
            },
        })
        assert r["success"] is True

        r = bridge_b.dispatch("begin_verification")
        assert r["success"] is True

        r = bridge_b.dispatch("record_verification", {
            "result": {"passed": True, "method": "code_review", "details": "Correct"},
        })
        assert r["success"] is True

        r = bridge_b.dispatch("recognize_engineering_completion", {
            "completion": {"recognized": True, "basis": "All verification passed"},
        })
        assert r["success"] is True
        assert r["context"]["process_state"] == "engineering_complete"
        assert r["context"]["engineering_completion"] is True

        # ── Final authoritative state verification ────────────────────────
        final = bridge_b.get_context()
        assert final["success"] is True
        assert final["process_instance_id"] == pid
        assert final["context"]["process_state"] == "engineering_complete"
        assert final["context"]["engineering_completion"] is True
        assert len(final["context"]["evidence"]) == 1
        assert len(final["context"]["engineering_decisions"]) == 1
        assert len(final["context"]["artifacts"]) == 1
        assert final["context"]["verification"]["passed"] is True

    def test_continuity_with_fresh_store_instance(self, tmp_path: Path) -> None:
        """Demonstrate that even a fresh ActiveRepositoryContext (pointing to
        the same filesystem root) can recover the Process Instance, proving
        continuity belongs to the filesystem, not in-memory objects."""
        ctx_a = ActiveRepositoryContext(tmp_path)
        bridge_a = AgentRuntimeBridge(ctx_a, runtime_id="store-a-bridge")

        create_result = bridge_a.create_process("Fresh store continuity test")
        pid = create_result["process_instance_id"]
        bridge_a.dispatch("start_investigation")
        del bridge_a

        # Create an entirely fresh context and bridge.
        ctx_b = ActiveRepositoryContext(tmp_path)
        bridge_b = AgentRuntimeBridge(ctx_b, runtime_id="store-b-bridge")

        attach_result = bridge_b.attach(pid)
        assert attach_result["success"] is True
        assert attach_result["context"]["process_state"] == "investigation"
        assert attach_result["context"]["engineering_objective"] == "Fresh store continuity test"
