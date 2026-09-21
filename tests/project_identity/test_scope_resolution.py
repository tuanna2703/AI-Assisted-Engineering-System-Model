from pathlib import Path

from bridge.agent_runtime_bridge import AgentRuntimeBridge
from runtime.core import ActiveRepositoryContext, Runtime


def resolved_scope(runtime: Runtime, identity: str):
    runtime.apply_scope_resolution(
        {
            "status": "RESOLVED",
            "engineering_scope_identity": identity,
            "recognized": True,
            "basis": "explicit scope authority",
            "actor": "scope-authority",
            "evidence": [{"kind": "explicit_scope_identity", "value": identity}],
        }
    )


def test_one_applicable_process_instance_resolves_deterministically(tmp_path: Path):
    runtime = Runtime(ActiveRepositoryContext(tmp_path), "runtime-a")
    pid = runtime.create_process("Implement X")
    resolved_scope(runtime, "scope:one")

    result = runtime.resolve_process_instance("scope:one")

    assert result.status == "RESOLVED"
    assert result.process_instance_id == pid


def test_no_applicable_process_instance_requires_explicit_creation(tmp_path: Path):
    runtime = Runtime(ActiveRepositoryContext(tmp_path), "runtime-a")
    runtime.create_process("Unscoped work")

    result = runtime.resolve_process_instance("scope:missing")

    assert result.status == "NO_APPLICABLE_PROCESS_INSTANCE"
    assert result.process_instance_id is None


def test_multiple_applicable_process_instances_are_ambiguous(tmp_path: Path):
    runtime = Runtime(ActiveRepositoryContext(tmp_path), "runtime-a")
    first = runtime.create_process("Work A")
    resolved_scope(runtime, "scope:shared")

    second_runtime = Runtime(ActiveRepositoryContext(tmp_path), "runtime-b")
    second = second_runtime.create_process("Work B")
    resolved_scope(second_runtime, "scope:shared")

    result = runtime.resolve_process_instance("scope:shared")

    assert result.status == "AMBIGUOUS"
    assert result.candidate_process_instance_ids == tuple(sorted((first, second)))


def test_explicit_process_instance_id_resolves_one_candidate(tmp_path: Path):
    context = ActiveRepositoryContext(tmp_path)
    runtime = Runtime(context, "runtime-a")
    first = runtime.create_process("Work A")
    resolved_scope(runtime, "scope:shared")

    second_runtime = Runtime(context, "runtime-b")
    second = second_runtime.create_process("Work B")
    resolved_scope(second_runtime, "scope:shared")

    result = runtime.resolve_process_instance(
        "scope:shared",
        process_instance_id=second,
    )

    assert result.status == "RESOLVED"
    assert result.process_instance_id == second
    assert first != second


def test_explicit_process_instance_from_other_scope_is_rejected(tmp_path: Path):
    context = ActiveRepositoryContext(tmp_path)
    runtime = Runtime(context, "runtime-a")
    first = runtime.create_process("Work A")
    resolved_scope(runtime, "scope:first")

    result = runtime.resolve_process_instance(
        "scope:second",
        process_instance_id=first,
    )

    assert result.status == "INVALID"


def test_resolution_is_repository_local(tmp_path: Path):
    repo_a = tmp_path / "repo-a"
    repo_b = tmp_path / "repo-b"
    repo_a.mkdir()
    repo_b.mkdir()

    runtime_a = Runtime(ActiveRepositoryContext(repo_a, "repo:a"), "runtime-a")
    pid_a = runtime_a.create_process("Work A")
    resolved_scope(runtime_a, "scope:a")

    runtime_b = Runtime(ActiveRepositoryContext(repo_b, "repo:b"), "runtime-b")
    result = runtime_b.resolve_process_instance("scope:a")

    assert result.status == "NO_APPLICABLE_PROCESS_INSTANCE"
    assert result.process_instance_id is None
    assert runtime_b.resolve_process_instance("scope:a").candidate_process_instance_ids == ()


def test_repository_identity_is_distinct_from_repository_root(tmp_path: Path):
    repo_a = tmp_path / "repo-a"
    repo_b = tmp_path / "repo-b"
    repo_a.mkdir()
    repo_b.mkdir()

    context_a = ActiveRepositoryContext(repo_a, "github:example/project")
    context_b = ActiveRepositoryContext(repo_b, "github:example/project")

    assert context_a.identity() == context_b.identity()
    assert context_a.aesm_root() != context_b.aesm_root()


def test_bridge_exposes_resolution_without_owning_binding(tmp_path: Path):
    context = ActiveRepositoryContext(tmp_path, "repo:one")
    bridge = AgentRuntimeBridge(context, "bridge-runtime")
    created = bridge.create_process("Work X")
    pid = created["process_instance_id"]

    bridge.dispatch(
        "apply_scope_resolution",
        {
            "resolution": {
                "status": "RESOLVED",
                "engineering_scope_identity": "scope:one",
                "recognized": True,
                "basis": "explicit scope authority",
                "actor": "scope-authority",
                "evidence": [{"kind": "explicit_scope_identity"}],
            }
        },
    )

    result = bridge.dispatch(
        "resolve_process_instance",
        {"engineering_scope_identity": "scope:one"},
    )

    assert result["success"] is True
    assert result["process_instance_id"] == pid
    assert not hasattr(bridge, "store")
