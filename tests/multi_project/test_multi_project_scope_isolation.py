"""Empirical multi-project scope-isolation scenarios.

These tests exercise the existing Runtime, ProcessStore, and AgentRuntimeBridge
without adding a multi-project orchestration mechanism. They are intended to
be run against the real repository/runtime environment and provide executable
evidence for the multi-project validation work unit.
"""
from pathlib import Path

import pytest

from bridge.agent_runtime_bridge import AgentRuntimeBridge
from runtime.core import ProcessStore, Runtime


PROJECT_A = "project:tuanna2703/directories-builder-pro"
PROJECT_B = "project:tuanna2703/AI-Assisted-Engineering-System-Model"


def resolved_scope(identity: str, actor: str = "scope-authority") -> dict:
    return {
        "status": "RESOLVED",
        "engineering_scope_identity": identity,
        "recognized": True,
        "basis": "explicit project identity supplied for the empirical experiment",
        "actor": actor,
        "evidence": [
            {
                "source": "empirical-experiment",
                "kind": "explicit_project_identity",
                "value": identity,
            }
        ],
    }


def nonresolved_scope(status: str, *, evidence: dict) -> dict:
    return {
        "status": status,
        "recognized": True,
        "basis": f"empirical experiment produced {status} scope resolution",
        "actor": "scope-authority",
        "evidence": [evidence],
    }


def test_two_distinct_projects_remain_isolated(tmp_path: Path):
    store = ProcessStore(tmp_path)
    runtime = Runtime(store, "multi-project-a")

    process_a = runtime.create_process("Implement the controlled DBP change")
    runtime.apply_scope_resolution(resolved_scope(PROJECT_A))
    runtime.stop()

    process_b = runtime.create_process("Validate AESM multi-project behavior")
    runtime.apply_scope_resolution(resolved_scope(PROJECT_B))

    persisted_a = store.load_instance(process_a)
    persisted_b = store.load_instance(process_b)

    assert persisted_a.engineering_scope_identity == PROJECT_A
    assert persisted_b.engineering_scope_identity == PROJECT_B
    assert persisted_a.process_instance_id != persisted_b.process_instance_id

    assert store.history(process_a)[-1]["resulting_identity"] == PROJECT_A
    assert store.history(process_b)[-1]["resulting_identity"] == PROJECT_B


def test_two_process_instances_in_one_project_remain_independent(tmp_path: Path):
    store = ProcessStore(tmp_path)
    runtime = Runtime(store, "same-project-a")

    process_a = runtime.create_process("DBP objective A")
    runtime.apply_scope_resolution(resolved_scope(PROJECT_A))
    runtime.stop()

    process_b = runtime.create_process("DBP objective B")
    runtime.apply_scope_resolution(resolved_scope(PROJECT_A))

    persisted_a = store.load_instance(process_a)
    persisted_b = store.load_instance(process_b)

    assert persisted_a.engineering_scope_identity == PROJECT_A
    assert persisted_b.engineering_scope_identity == PROJECT_A
    assert persisted_a.process_instance_id != persisted_b.process_instance_id

    history_a = store.history(process_a)
    history_b = store.history(process_b)
    assert all(entry["process_instance_id"] == process_a for entry in history_a)
    assert all(entry["process_instance_id"] == process_b for entry in history_b)


def test_switching_projects_does_not_rebind_the_first_process(tmp_path: Path):
    store = ProcessStore(tmp_path)
    runtime = Runtime(store, "switching-runtime")

    process_a = runtime.create_process("Work in Project A")
    runtime.apply_scope_resolution(resolved_scope(PROJECT_A))

    runtime.stop()

    process_b = runtime.create_process("Work in Project B")
    runtime.apply_scope_resolution(resolved_scope(PROJECT_B))

    recovered_a = Runtime(store, "recovery-a")
    recovered_a.attach(process_a)

    assert recovered_a.process_instance.engineering_scope_identity == PROJECT_A
    assert store.load_instance(process_a).engineering_scope_identity == PROJECT_A
    assert store.load_instance(process_b).engineering_scope_identity == PROJECT_B


def test_conflicting_rebinding_is_rejected_and_persistence_remains_project_a(
    tmp_path: Path,
):
    store = ProcessStore(tmp_path)
    runtime = Runtime(store, "conflict-runtime")

    process_a = runtime.create_process("Bound to Project A")
    runtime.apply_scope_resolution(resolved_scope(PROJECT_A))

    prior_history_count = store.history_entry_count(process_a)

    with pytest.raises(RuntimeError, match="cannot be silently replaced"):
        runtime.apply_scope_resolution(resolved_scope(PROJECT_B))

    in_memory = runtime.process_instance
    persisted = store.load_instance(process_a)

    assert in_memory.engineering_scope_identity == PROJECT_A
    assert in_memory.engineering_scope_resolution == "RESOLVED"
    assert persisted.engineering_scope_identity == PROJECT_A
    assert persisted.engineering_scope_resolution == "RESOLVED"
    assert store.history_entry_count(process_a) == prior_history_count


def test_unresolved_and_ambiguous_processes_remain_independent(tmp_path: Path):
    store = ProcessStore(tmp_path)
    runtime = Runtime(store, "resolution-runtime")

    unresolved_id = runtime.create_process("Scope remains unresolved")
    runtime.apply_scope_resolution(
        nonresolved_scope("UNRESOLVED", evidence={"reason": "insufficient evidence"})
    )
    runtime.stop()

    ambiguous_id = runtime.create_process("Scope remains ambiguous")
    runtime.apply_scope_resolution(
        nonresolved_scope("AMBIGUOUS", evidence={"candidate_count": 2})
    )

    unresolved = store.load_instance(unresolved_id)
    ambiguous = store.load_instance(ambiguous_id)

    assert unresolved.engineering_scope_resolution == "UNRESOLVED"
    assert unresolved.engineering_scope_identity is None
    assert ambiguous.engineering_scope_resolution == "AMBIGUOUS"
    assert ambiguous.engineering_scope_identity is None


def test_unresolved_state_does_not_acquire_scope_from_another_project(
    tmp_path: Path,
):
    store = ProcessStore(tmp_path)
    runtime = Runtime(store, "contamination-runtime")

    unresolved_id = runtime.create_process("Unresolved process")
    runtime.apply_scope_resolution(
        nonresolved_scope("UNRESOLVED", evidence={"reason": "not enough evidence"})
    )
    runtime.stop()

    bound_id = runtime.create_process("Bound process")
    runtime.apply_scope_resolution(resolved_scope(PROJECT_B))

    runtime.stop()

    recovered_unresolved = Runtime(store, "recovery-unresolved")
    recovered_unresolved.attach(unresolved_id)

    recovered_bound = Runtime(store, "recovery-bound")
    recovered_bound.attach(bound_id)

    assert recovered_unresolved.process_instance.engineering_scope_identity is None
    assert recovered_unresolved.process_instance.engineering_scope_resolution == "UNRESOLVED"
    assert recovered_bound.process_instance.engineering_scope_identity == PROJECT_B


def test_bridge_preserves_independent_authority_for_two_projects(tmp_path: Path):
    store = ProcessStore(tmp_path)
    bridge_a = AgentRuntimeBridge(store, "bridge-a")
    bridge_b = AgentRuntimeBridge(store, "bridge-b")

    created_a = bridge_a.create_process("Agent request for Project A")
    created_b = bridge_b.create_process("Agent request for Project B")

    process_a = created_a["process_instance_id"]
    process_b = created_b["process_instance_id"]

    result_a = bridge_a.dispatch(
        "apply_scope_resolution",
        {"resolution": resolved_scope(PROJECT_A, actor="agent-submitted-resolution")},
    )
    result_b = bridge_b.dispatch(
        "apply_scope_resolution",
        {"resolution": resolved_scope(PROJECT_B, actor="agent-submitted-resolution")},
    )

    assert result_a["success"] is True
    assert result_b["success"] is True
    assert result_a["process_instance"]["engineering_scope_identity"] == PROJECT_A
    assert result_b["process_instance"]["engineering_scope_identity"] == PROJECT_B

    assert store.load_instance(process_a).engineering_scope_identity == PROJECT_A
    assert store.load_instance(process_b).engineering_scope_identity == PROJECT_B


def test_bridge_rejects_conflicting_scope_without_mutating_authoritative_state(
    tmp_path: Path,
):
    store = ProcessStore(tmp_path)
    bridge = AgentRuntimeBridge(store, "bridge-conflict")

    created = bridge.create_process("Agent request for Project A")
    process_id = created["process_instance_id"]

    bound = bridge.dispatch(
        "apply_scope_resolution",
        {"resolution": resolved_scope(PROJECT_A)},
    )
    assert bound["success"] is True

    conflict = bridge.dispatch(
        "apply_scope_resolution",
        {"resolution": resolved_scope(PROJECT_B)},
    )

    assert conflict["success"] is False
    assert conflict["error"]["type"] == "runtime_error"
    assert conflict["process_instance"]["engineering_scope_identity"] == PROJECT_A
    assert store.load_instance(process_id).engineering_scope_identity == PROJECT_A


def test_recovery_after_project_switch_uses_persisted_scope_not_runtime_session(
    tmp_path: Path,
):
    store = ProcessStore(tmp_path)

    runtime_a = Runtime(store, "runtime-a")
    process_a = runtime_a.create_process("Continue Project A work")
    runtime_a.apply_scope_resolution(resolved_scope(PROJECT_A))
    runtime_a.stop()

    runtime_b = Runtime(store, "runtime-b")
    process_b = runtime_b.create_process("Work on Project B")
    runtime_b.apply_scope_resolution(resolved_scope(PROJECT_B))
    runtime_b.stop()

    fresh_runtime = Runtime(store, "fresh-runtime")
    fresh_runtime.attach(process_a)

    assert fresh_runtime.process_instance.process_instance_id == process_a
    assert fresh_runtime.process_instance.engineering_scope_identity == PROJECT_A
    assert fresh_runtime.process_instance.engineering_scope_identity != (
        store.load_instance(process_b).engineering_scope_identity
    )
