"""Validate the minimum Execution Environment mechanism prerequisites.

This is a mechanism-readiness probe, not an AI-Agent participation test.
It intentionally validates only observable repository/runtime capabilities:

- common persistent-instruction surfaces;
- optional skill and tool/MCP configuration surfaces;
- the existing Agent–Runtime bridge surface;
- Process Instance creation and known-ID recovery through fresh bridge objects;
- authoritative Execution Context access.

The probe uses a temporary ProcessStore so it cannot mutate the repository's
normal persisted process state.
"""
from __future__ import annotations

import importlib
import json
import tempfile
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


def _surface_status(paths: list[Path]) -> list[str]:
    return [str(path.relative_to(REPOSITORY_ROOT)) for path in paths if path.exists()]


def main() -> int:
    print("Environment Mechanism Readiness Probe")
    print("=" * 40)
    print(f"repository: {REPOSITORY_ROOT}")

    instruction_candidates = [
        REPOSITORY_ROOT / ".agents" / "rules",
        REPOSITORY_ROOT / ".github" / "copilot-instructions.md",
        REPOSITORY_ROOT / "AGENTS.md",
        REPOSITORY_ROOT / "CLAUDE.md",
    ]
    skill_candidates = [
        REPOSITORY_ROOT / ".agents" / "skills",
        REPOSITORY_ROOT / "skills",
    ]
    tool_candidates = [
        REPOSITORY_ROOT / ".mcp.json",
        REPOSITORY_ROOT / "mcp.json",
        REPOSITORY_ROOT / ".vscode" / "mcp.json",
    ]

    print("persistent_instruction_surfaces:", _surface_status(instruction_candidates) or "none")
    print("skill_surfaces:", _surface_status(skill_candidates) or "none")
    print("tool_mcp_surfaces:", _surface_status(tool_candidates) or "none")

    bridge_module = importlib.import_module("bridge.agent_runtime_bridge")
    runtime_module = importlib.import_module("runtime.core.store")
    bridge_class = getattr(bridge_module, "AgentRuntimeBridge")
    store_class = getattr(runtime_module, "ProcessStore")

    required_bridge = ("create_process", "attach", "get_context", "dispatch")
    missing = [name for name in required_bridge if not hasattr(bridge_class, name)]
    if missing:
        raise AssertionError(f"missing bridge capabilities: {missing}")
    print("bridge_surface: PASS", list(required_bridge))

    with tempfile.TemporaryDirectory(prefix="aesm-mechanism-probe-") as temp_dir:
        store = store_class(temp_dir)
        first = bridge_class(store, runtime_id="mechanism-probe-A")
        created = first.create_process("Environment mechanism readiness probe")
        assert created["success"] is True, json.dumps(created, indent=2)
        process_id = created["process_instance_id"]
        assert process_id, "Runtime did not return an authoritative Process Instance ID"
        assert created["context"]["process_instance_id"] == process_id
        print("process_creation: PASS", process_id)

        second = bridge_class(store, runtime_id="mechanism-probe-B")
        recovered = second.attach(process_id)
        assert recovered["success"] is True, json.dumps(recovered, indent=2)
        assert recovered["process_instance_id"] == process_id
        assert recovered["context"]["process_instance_id"] == process_id
        context = second.get_context()
        assert context["success"] is True, json.dumps(context, indent=2)
        assert context["context"]["process_instance_id"] == process_id
        print("known_id_recovery: PASS")
        print("authoritative_context_access: PASS")

    print()
    print("RESULT: MECHANISM READINESS DEMONSTRATED")
    print("This result does not prove that an AI Agent received or followed AESM guidance.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
