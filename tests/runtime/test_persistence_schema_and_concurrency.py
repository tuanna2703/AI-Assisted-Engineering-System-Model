"""Persistence schema and optimistic concurrency validation."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from runtime.core import ActiveRepositoryContext, Runtime
from runtime.core.models import CURRENT_PERSISTED_SCHEMA_VERSION
from runtime.persistence.json_store import PersistenceError


def build_runtime(tmp_path: Path, runtime_id: str) -> Runtime:
    runtime = Runtime(ActiveRepositoryContext(tmp_path), runtime_id)
    runtime.create_process("Persistence schema validation")
    return runtime


def test_new_persistence_records_include_schema_version(tmp_path: Path):
    runtime = build_runtime(tmp_path, "schema-writer")
    pid = runtime.process_instance.process_instance_id
    process_data = json.loads((tmp_path / ".aesm" / pid / "process.json").read_text())
    context_data = json.loads((tmp_path / ".aesm" / pid / "context.json").read_text())
    assert process_data["schema_version"] == CURRENT_PERSISTED_SCHEMA_VERSION
    assert context_data["schema_version"] == CURRENT_PERSISTED_SCHEMA_VERSION


def test_legacy_missing_schema_version_defaults_to_supported_version(tmp_path: Path):
    runtime = build_runtime(tmp_path, "legacy")
    pid = runtime.process_instance.process_instance_id
    process_path = tmp_path / ".aesm" / pid / "process.json"
    context_path = tmp_path / ".aesm" / pid / "context.json"

    process_data = json.loads(process_path.read_text())
    context_data = json.loads(context_path.read_text())
    process_data.pop("schema_version")
    context_data.pop("schema_version")
    process_path.write_text(json.dumps(process_data))
    context_path.write_text(json.dumps(context_data))

    recovered = Runtime(ActiveRepositoryContext(tmp_path), "legacy-recovery")
    recovered.attach(pid)
    assert recovered.context.process_instance_id == pid


def test_unsupported_context_schema_is_rejected(tmp_path: Path):
    runtime = build_runtime(tmp_path, "schema-reject")
    pid = runtime.process_instance.process_instance_id
    path = tmp_path / ".aesm" / pid / "context.json"
    data = json.loads(path.read_text())
    data["schema_version"] = CURRENT_PERSISTED_SCHEMA_VERSION + 1
    path.write_text(json.dumps(data))

    with pytest.raises(PersistenceError, match="unsupported context schema version"):
        Runtime(ActiveRepositoryContext(tmp_path), "schema-reject-reader").attach(pid)


def test_stale_process_instance_write_is_rejected(tmp_path: Path):
    runtime_a = build_runtime(tmp_path, "writer-a")
    pid = runtime_a.process_instance.process_instance_id
    runtime_b = Runtime(ActiveRepositoryContext(tmp_path), "writer-b")
    runtime_b.attach(pid)

    runtime_a.apply_scope_resolution({
        "status": "RESOLVED",
        "engineering_scope_identity": "project:test",
        "recognized": True,
        "basis": "test scope resolution",
        "actor": "test",
        "evidence": [{"source": "test"}],
    })

    runtime_b.process_instance.engineering_scope_resolution = "AMBIGUOUS"
    runtime_b.process_instance.engineering_scope_identity = None
    with pytest.raises(PersistenceError, match="stale Process Instance write"):
        runtime_b.store.save_process_instance(
            runtime_b.process_instance,
            {"type": "test_stale_process_write"},
        )
