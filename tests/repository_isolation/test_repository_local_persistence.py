"""Repository isolation tests — full required test matrix.

These tests verify the repository-local persistence invariants introduced
by the ActiveRepositoryContext migration.

Invariant under test:

    Active Repository Context
            +
    Process Instance Identity
            ↓
    exactly one repository-local persistence boundary

with no workspace-level fallback.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from runtime.core import ActiveRepositoryContext, ProcessStore, Runtime
from runtime.persistence.json_store import PersistenceError


EVIDENCE = {
    "recognized": True,
    "basis": "workspace inspection established the observation as recordable evidence",
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_runtime(repo_path: Path, runtime_id: str = "test-runtime") -> Runtime:
    ctx = ActiveRepositoryContext(repo_path)
    return Runtime(ctx, runtime_id)


def make_minimal_pi_files(pi_dir: Path, pi_id: str, version: int = 0) -> None:
    """Write minimal valid PI files for use in isolation/anti-regression tests."""
    pi_dir.mkdir(parents=True, exist_ok=True)
    process_data = {
        "process_instance_id": pi_id,
        "engineering_objective": "test objective",
        "lifecycle": "active",
        "execution_context_ref": f"process-instance/{pi_id}/context.json",
        "epm": {},
        "pem": {},
        "engineering_scope_identity": None,
        "engineering_scope_resolution": "UNRESOLVED",
        "engineering_scope_evidence": [],
        "created_at": "2026-01-01T00:00:00+00:00",
        "updated_at": "2026-01-01T00:00:00+00:00",
    }
    context_data = {
        "process_instance_id": pi_id,
        "engineering_objective": "test objective",
        "process_state": "initial",
        "execution_mode": "active",
        "requirements": [],
        "constraints": [],
        "evidence": [],
        "assumptions": [],
        "risks": [],
        "candidate_solutions": [],
        "engineering_decisions": [],
        "decision_gates": [],
        "artifacts": [],
        "verification": {},
        "unresolved_matters": [],
        "pending_execution": [],
        "execution_determination": None,
        "failure_uncertainty": [],
        "engineering_completion": False,
        "version": version,
        "updated_at": "2026-01-01T00:00:00+00:00",
    }
    (pi_dir / "process.json").write_text(
        json.dumps(process_data, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (pi_dir / "context.json").write_text(
        json.dumps(context_data, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (pi_dir / "history.jsonl").write_text(
        json.dumps({"type": "process_created", "process_instance_id": pi_id,
                    "version": version, "at": "2026-01-01T00:00:00+00:00"}) + "\n",
        encoding="utf-8",
    )


# ---------------------------------------------------------------------------
# Storage path tests
# ---------------------------------------------------------------------------

def test_pi_stored_in_repo_aesm_not_old_layout(tmp_path: Path):
    """Create PI → verify files land in <repo>/.aesm/<PI-ID>/, not process-instance/."""
    runtime = make_runtime(tmp_path)
    pid = runtime.create_process("Isolation test")

    pi_dir = tmp_path / ".aesm" / pid
    assert pi_dir.exists(), f"Expected PI dir at {pi_dir}"
    assert (pi_dir / "process.json").exists()
    assert (pi_dir / "context.json").exists()
    assert (pi_dir / "history.jsonl").exists()

    # Old layout must NOT exist.
    assert not (tmp_path / "process-instance").exists()


def test_pi_recovery_in_same_repo(tmp_path: Path):
    """Create PI and recover it using the same repository context."""
    ctx = ActiveRepositoryContext(tmp_path)
    runtime_a = Runtime(ctx, "creator")
    pid = runtime_a.create_process("Recovery test")
    runtime_a.stop()

    runtime_b = Runtime(ctx, "recoverer")
    runtime_b.attach(pid)

    assert runtime_b.process_instance.process_instance_id == pid
    assert runtime_b.process_instance.lifecycle == "active"


def test_cross_repo_isolation(tmp_path: Path):
    """PI in repo-A cannot be recovered from repo-B context."""
    repo_a = tmp_path / "repo-a"
    repo_b = tmp_path / "repo-b"
    repo_a.mkdir()
    repo_b.mkdir()

    ctx_a = ActiveRepositoryContext(repo_a)
    runtime_a = Runtime(ctx_a, "writer-a")
    pid = runtime_a.create_process("Repo A work")
    runtime_a.stop()

    # PI is in repo_a/.aesm/<pid>/ — repo_b knows nothing of it.
    ctx_b = ActiveRepositoryContext(repo_b)
    runtime_b = Runtime(ctx_b, "reader-b")

    with pytest.raises(PersistenceError):
        runtime_b.attach(pid)


def test_same_pi_id_in_two_repos_resolved_independently(tmp_path: Path):
    """If two repos happen to have the same PI ID, they are independent storage locations."""
    repo_a = tmp_path / "repo-a"
    repo_b = tmp_path / "repo-b"
    repo_a.mkdir()
    repo_b.mkdir()

    fixed_id = "00000000-0000-0000-0000-000000000001"

    make_minimal_pi_files(repo_a / ".aesm" / fixed_id, fixed_id, version=1)
    make_minimal_pi_files(repo_b / ".aesm" / fixed_id, fixed_id, version=5)

    ctx_a = ActiveRepositoryContext(repo_a)
    ctx_b = ActiveRepositoryContext(repo_b)

    store_a = ProcessStore(ctx_a)
    store_b = ProcessStore(ctx_b)

    inst_a = store_a.load_context(fixed_id)
    inst_b = store_b.load_context(fixed_id)

    # Same ID, independent state.
    assert inst_a.version == 1
    assert inst_b.version == 5


# ---------------------------------------------------------------------------
# Invalid / missing context tests
# ---------------------------------------------------------------------------

def test_missing_repository_context_raises_on_nonexistent_path(tmp_path: Path):
    """ActiveRepositoryContext rejects a path that does not exist."""
    with pytest.raises(ValueError, match="does not exist"):
        ActiveRepositoryContext(tmp_path / "nonexistent")


def test_invalid_repository_context_raises_on_file_path(tmp_path: Path):
    """ActiveRepositoryContext rejects a path that is a file, not a directory."""
    some_file = tmp_path / "not_a_dir.txt"
    some_file.write_text("not a directory")
    with pytest.raises(ValueError, match="not a directory"):
        ActiveRepositoryContext(some_file)


def test_repository_context_is_frozen(tmp_path: Path):
    """ActiveRepositoryContext is immutable after construction."""
    ctx = ActiveRepositoryContext(tmp_path)
    with pytest.raises((AttributeError, TypeError)):
        ctx.repository_root = tmp_path / "other"  # type: ignore[misc]


def test_runtime_context_property_is_readable(tmp_path: Path):
    """runtime.repository_context exposes the active context for inspection."""
    ctx = ActiveRepositoryContext(tmp_path)
    runtime = Runtime(ctx, "test")
    assert runtime.repository_context is ctx
    assert runtime.repository_context.repository_root == tmp_path


# ---------------------------------------------------------------------------
# observe() persists to repo .aesm
# ---------------------------------------------------------------------------

def test_observe_persists_in_repo_aesm(tmp_path: Path):
    """observe() records evidence and persists it under <repo>/.aesm."""
    ctx = ActiveRepositoryContext(tmp_path)
    runtime = Runtime(ctx, "observer")
    pid = runtime.create_process("Evidence persistence test")

    runtime.observe({"fact": "repository-local evidence", "recognition": EVIDENCE})

    # Reload from disk via a fresh store.
    recovered = ProcessStore(ctx).load_context(pid)
    assert len(recovered.evidence) == 1
    assert recovered.evidence[0]["fact"] == "repository-local evidence"

    # Verify the context.json is under .aesm, not anywhere else.
    assert (tmp_path / ".aesm" / pid / "context.json").exists()


# ---------------------------------------------------------------------------
# Stale-write guard
# ---------------------------------------------------------------------------

def test_stale_write_rejected(tmp_path: Path):
    """A Runtime with in-memory version N cannot overwrite persisted version N+1."""
    ctx = ActiveRepositoryContext(tmp_path)
    store = ProcessStore(ctx)
    runtime = Runtime(ctx, "writer")
    pid = runtime.create_process("Stale write test")

    # Record current in-memory version before simulating external advance.
    in_memory_version = runtime.context.version

    # Simulate another environment writing a newer version directly to disk.
    context_path = tmp_path / ".aesm" / pid / "context.json"
    data = json.loads(context_path.read_text(encoding="utf-8"))
    data["version"] = in_memory_version + 5  # much newer
    context_path.write_text(json.dumps(data) + "\n", encoding="utf-8")

    # Now runtime tries to write based on its stale in-memory version.
    with pytest.raises(PersistenceError, match="stale write rejected"):
        runtime.observe({"fact": "new obs", "recognition": EVIDENCE})


# ---------------------------------------------------------------------------
# Git conflict guard
# ---------------------------------------------------------------------------

def test_git_conflict_blocks_load_instance(tmp_path: Path):
    """Presence of Git conflict markers in process.json blocks load_instance."""
    ctx = ActiveRepositoryContext(tmp_path)
    runtime = Runtime(ctx, "conflict-test")
    pid = runtime.create_process("Conflict test")
    runtime.stop()

    process_path = tmp_path / ".aesm" / pid / "process.json"
    conflicted = "<<<<<<< HEAD\n" + process_path.read_text() + "=======\n{}\n>>>>>>> branch\n"
    process_path.write_text(conflicted)

    store = ProcessStore(ctx)
    with pytest.raises(PersistenceError, match="unresolved Git conflict"):
        store.load_instance(pid)


def test_git_conflict_blocks_load_context(tmp_path: Path):
    """Presence of Git conflict markers in context.json blocks load_context."""
    ctx = ActiveRepositoryContext(tmp_path)
    runtime = Runtime(ctx, "conflict-test")
    pid = runtime.create_process("Conflict test")
    runtime.stop()

    context_path = tmp_path / ".aesm" / pid / "context.json"
    conflicted = "<<<<<<< HEAD\n" + context_path.read_text() + "=======\n{}\n>>>>>>> branch\n"
    context_path.write_text(conflicted)

    store = ProcessStore(ctx)
    with pytest.raises(PersistenceError, match="unresolved Git conflict"):
        store.load_context(pid)
