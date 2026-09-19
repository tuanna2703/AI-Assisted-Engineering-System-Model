from pathlib import Path

import pytest

from bridge.agent_runtime_bridge import AgentRuntimeBridge
from runtime.core import ActiveRepositoryContext, ProcessStore, Runtime
from runtime.persistence.json_store import PersistenceError


RECOGNITION = {
    "recognized": True,
    "basis": "applicable scope authority established the submitted outcome",
}


def resolved_scope(identity="project:directories-builder-pro"):
    return {
        "status": "RESOLVED",
        "engineering_scope_identity": identity,
        "recognized": True,
        "basis": "human-confirmed project identity",
        "actor": "scope-authority",
        "evidence": [
            {
                "source": "human",
                "kind": "explicit_project_identity",
                "value": identity,
            }
        ],
    }


def test_new_process_starts_with_explicit_unresolved_scope(tmp_path: Path):
    ctx = ActiveRepositoryContext(tmp_path)
    runtime = Runtime(ctx, "runtime-a")
    pid = runtime.create_process("Implement feature X")

    instance = runtime.store.load_instance(pid)
    assert instance.engineering_scope_identity is None
    assert instance.engineering_scope_resolution == "UNRESOLVED"


def test_scope_resolution_binds_identity_and_persists(tmp_path: Path):
    ctx = ActiveRepositoryContext(tmp_path)
    store = ProcessStore(ctx)
    runtime = Runtime(ctx, "runtime-a")
    pid = runtime.create_process("Implement feature X")

    runtime.apply_scope_resolution(resolved_scope())

    persisted = store.load_instance(pid)
    assert persisted.engineering_scope_identity == "project:directories-builder-pro"
    assert persisted.engineering_scope_resolution == "RESOLVED"
    assert persisted.engineering_scope_evidence[0]["kind"] == "explicit_project_identity"

    history = store.history(pid)
    assert history[-1]["type"] == "engineering_scope_resolution"
    assert history[-1]["resulting_status"] == "RESOLVED"


def test_scope_binding_survives_runtime_replacement(tmp_path: Path):
    ctx = ActiveRepositoryContext(tmp_path)
    store = ProcessStore(ctx)
    runtime_a = Runtime(ctx, "runtime-a")
    pid = runtime_a.create_process("Implement feature X")
    runtime_a.apply_scope_resolution(resolved_scope())
    runtime_a.stop()

    runtime_b = Runtime(ctx, "runtime-b")
    runtime_b.attach(pid)

    assert runtime_b.process_instance.engineering_scope_resolution == "RESOLVED"
    assert runtime_b.process_instance.engineering_scope_identity == (
        "project:directories-builder-pro"
    )


@pytest.mark.parametrize(
    "status",
    ["UNRESOLVED", "AMBIGUOUS", "CONFLICTING", "INVALID"],
)
def test_nonresolved_scope_outcomes_remain_explicit(tmp_path: Path, status: str):
    ctx = ActiveRepositoryContext(tmp_path)
    runtime = Runtime(ctx, "runtime-a")
    runtime.create_process("Implement feature X")

    runtime.apply_scope_resolution(
        {
            "status": status,
            "recognized": True,
            "basis": f"scope resolution produced {status}",
            "actor": "scope-authority",
            "evidence": [{"status": status}],
        }
    )

    assert runtime.process_instance.engineering_scope_resolution == status
    assert runtime.process_instance.engineering_scope_identity is None


def test_nonresolved_scope_outcome_survives_recovery(tmp_path: Path):
    ctx = ActiveRepositoryContext(tmp_path)
    store = ProcessStore(ctx)
    runtime = Runtime(ctx, "runtime-a")
    pid = runtime.create_process("Implement feature X")
    runtime.apply_scope_resolution(
        {
            "status": "AMBIGUOUS",
            "recognized": True,
            "basis": "two explicit project identities remain possible",
            "actor": "scope-authority",
            "evidence": [{"candidate_count": 2}],
        }
    )
    runtime.stop()

    recovered = Runtime(ctx, "runtime-b")
    recovered.attach(pid)

    assert recovered.process_instance.engineering_scope_resolution == "AMBIGUOUS"
    assert recovered.process_instance.engineering_scope_identity is None


def test_established_scope_cannot_be_silently_rebound(tmp_path: Path):
    ctx = ActiveRepositoryContext(tmp_path)
    runtime = Runtime(ctx, "runtime-a")
    runtime.create_process("Implement feature X")
    runtime.apply_scope_resolution(resolved_scope("project:first"))

    with pytest.raises(RuntimeError):
        runtime.apply_scope_resolution(resolved_scope("project:second"))

    assert runtime.process_instance.engineering_scope_identity == "project:first"


def test_invalid_resolution_does_not_mutate_binding(tmp_path: Path):
    ctx = ActiveRepositoryContext(tmp_path)
    runtime = Runtime(ctx, "runtime-a")
    runtime.create_process("Implement feature X")

    with pytest.raises(ValueError):
        runtime.apply_scope_resolution(
            {
                "status": "RESOLVED",
                "recognized": True,
                "basis": "missing identity",
                "actor": "scope-authority",
                "evidence": [],
            }
        )

    assert runtime.process_instance.engineering_scope_resolution == "UNRESOLVED"
    assert runtime.process_instance.engineering_scope_identity is None


def test_scope_resolution_requires_explicit_recognition(tmp_path: Path):
    ctx = ActiveRepositoryContext(tmp_path)
    runtime = Runtime(ctx, "runtime-a")
    runtime.create_process("Implement feature X")

    with pytest.raises(RuntimeError):
        runtime.apply_scope_resolution(
            {
                "status": "RESOLVED",
                "engineering_scope_identity": "project:first",
                "recognized": False,
                "basis": "proposal only",
                "actor": "agent",
                "evidence": [],
            }
        )

    assert runtime.process_instance.engineering_scope_resolution == "UNRESOLVED"


def test_bridge_can_submit_scope_resolution_without_owning_binding(tmp_path: Path):
    ctx = ActiveRepositoryContext(tmp_path)
    bridge = AgentRuntimeBridge(ctx, "bridge-runtime")
    created = bridge.create_process("Implement feature X")
    pid = created["process_instance_id"]

    result = bridge.dispatch("apply_scope_resolution", {"resolution": resolved_scope()})

    assert result["success"] is True
    assert result["process_instance_id"] == pid
    assert result["process_instance"]["engineering_scope_identity"] == (
        "project:directories-builder-pro"
    )

    recovered = ProcessStore(ctx).load_instance(pid)
    assert recovered.engineering_scope_identity == "project:directories-builder-pro"


def test_store_rejects_corrupt_scope_binding(tmp_path: Path):
    ctx = ActiveRepositoryContext(tmp_path)
    store = ProcessStore(ctx)
    runtime = Runtime(ctx, "runtime-a")
    pid = runtime.create_process("Implement feature X")

    process_path = tmp_path / ".aesm" / pid / "process.json"
    data = process_path.read_text()
    data = data.replace('"engineering_scope_resolution": "UNRESOLVED"', '"engineering_scope_resolution": "RESOLVED"')
    process_path.write_text(data)

    with pytest.raises(PersistenceError):
        store.load_instance(pid)
