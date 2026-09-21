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

    runtime.stop()
    attached = runtime.resolve_and_attach_process_instance("scope:one")
    assert attached.status == "RESOLVED"
    assert runtime.attached is True
    assert runtime.process_instance.process_instance_id == pid


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
    assert result["resolution"]["status"] == "RESOLVED"
    assert result["resolution"]["process_instance_id"] == pid
    assert not hasattr(bridge, "store")



def test_same_repository_identity_recovers_from_new_repository_path(tmp_path: Path):
    original_root = tmp_path / "original"
    relocated_root = tmp_path / "relocated"
    original_root.mkdir()
    relocated_root.mkdir()

    first_runtime = Runtime(
        ActiveRepositoryContext(original_root, "github:example/project"),
        "runtime-a",
    )
    pid = first_runtime.create_process("Portable work")
    resolved_scope(first_runtime, "scope:portable")
    first_runtime.stop()

    # Model a relocated checkout carrying the same repository-local .aesm state.
    import shutil
    shutil.copytree(original_root / ".aesm", relocated_root / ".aesm")

    second_runtime = Runtime(
        ActiveRepositoryContext(relocated_root, "github:example/project"),
        "runtime-b",
    )
    result = second_runtime.resolve_and_attach_process_instance("scope:portable")

    assert result.status == "RESOLVED"
    assert result.process_instance_id == pid
    assert second_runtime.process_instance.process_instance_id == pid


def test_runtime_context_is_immutable_and_does_not_retarget_store(tmp_path: Path):
    repo_a = tmp_path / "repo-a"
    repo_b = tmp_path / "repo-b"
    repo_a.mkdir()
    repo_b.mkdir()

    context = ActiveRepositoryContext(repo_a, "repo:a")
    runtime = Runtime(context, "runtime-a")
    pid = runtime.create_process("Bound work")
    resolved_scope(runtime, "scope:a")

    assert runtime.repository_context.repository_root == repo_a
    assert runtime.repository_context.identity() == "repo:a"
    assert runtime.store.context.repository_root == repo_a

    try:
        context.repository_root = repo_b
        raise AssertionError("ActiveRepositoryContext must be immutable")
    except (AttributeError, TypeError):
        pass

    assert runtime.repository_context.repository_root == repo_a
    assert runtime.store.context.repository_root == repo_a
    assert runtime.resolve_process_instance("scope:a").process_instance_id == pid
    assert runtime.resolve_process_instance("scope:b").status == "NO_APPLICABLE_PROCESS_INSTANCE"


def test_explicit_process_instance_from_another_repository_is_rejected(tmp_path: Path):
    repo_a = tmp_path / "repo-a"
    repo_b = tmp_path / "repo-b"
    repo_a.mkdir()
    repo_b.mkdir()

    runtime_a = Runtime(ActiveRepositoryContext(repo_a, "repo:a"), "runtime-a")
    pid_a = runtime_a.create_process("Work A")
    resolved_scope(runtime_a, "scope:a")

    runtime_b = Runtime(ActiveRepositoryContext(repo_b, "repo:b"), "runtime-b")
    result = runtime_b.resolve_process_instance("scope:a", process_instance_id=pid_a)

    assert result.status == "INVALID"
    assert result.process_instance_id is None


def test_terminated_process_instance_is_not_applicable(tmp_path: Path):
    runtime = Runtime(ActiveRepositoryContext(tmp_path), "runtime-a")
    pid = runtime.create_process("Finished work")
    resolved_scope(runtime, "scope:finished")

    runtime.apply_lifecycle_determination(
        {
            "target_process_instance_id": pid,
            "requested_transition": "ACTIVE -> TERMINATED",
            "semantic_basis": "engineering process ended",
            "authority_context": "authorized-controller",
            "actor": "controller",
            "evidence": [],
            "occurred_at": "2026-09-21T08:00:00+00:00",
        }
    )
    runtime.stop()

    fresh = Runtime(ActiveRepositoryContext(tmp_path), "runtime-b")
    result = fresh.resolve_process_instance("scope:finished")

    assert result.status == "NO_APPLICABLE_PROCESS_INSTANCE"
    assert result.candidate_process_instance_ids == ()
