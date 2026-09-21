"""Persistence failure rollback tests for authoritative Runtime mutations."""
from __future__ import annotations

from pathlib import Path

import pytest

from runtime.core import ActiveRepositoryContext, Runtime
from runtime.persistence.json_store import PersistenceError


RECOGNITION = {"recognized": True, "basis": "test recognition"}


def build_runtime(tmp_path: Path) -> Runtime:
    runtime = Runtime(ActiveRepositoryContext(tmp_path), "rollback-test")
    runtime.create_process("Runtime persistence rollback validation")
    return runtime


def fail_context_persistence(runtime: Runtime, monkeypatch: pytest.MonkeyPatch) -> None:
    def failing_save(*args, **kwargs):
        raise PersistenceError("simulated context persistence failure")

    monkeypatch.setattr(runtime.store, "save_context", failing_save)


def assert_recovered_matches(runtime: Runtime, process_instance_id: str, expected: dict) -> None:
    recovered = Runtime(runtime.repository_context, "recovery")
    recovered.attach(process_instance_id)
    assert recovered.context.to_dict() == expected


def test_state_transition_rolls_back_on_persistence_failure(tmp_path: Path, monkeypatch):
    runtime = build_runtime(tmp_path)
    pid = runtime.process_instance.process_instance_id
    before = runtime.context.to_dict()
    history_before = runtime.store.history_entry_count(pid)
    fail_context_persistence(runtime, monkeypatch)

    with pytest.raises(PersistenceError):
        runtime.start_investigation()

    assert runtime.context.to_dict() == before
    assert runtime.store.history_entry_count(pid) == history_before
    assert_recovered_matches(runtime, pid, before)


def test_pending_execution_rolls_back_on_persistence_failure(tmp_path: Path, monkeypatch):
    runtime = build_runtime(tmp_path)
    runtime.start_investigation()
    runtime.recognize_decision({"id": "D1"}, RECOGNITION)
    runtime.begin_implementation()
    pid = runtime.process_instance.process_instance_id
    before = runtime.context.to_dict()
    history_before = runtime.store.history_entry_count(pid)
    fail_context_persistence(runtime, monkeypatch)

    with pytest.raises(PersistenceError):
        runtime.set_pending_execution({"id": "W1"})

    assert runtime.context.to_dict() == before
    assert runtime.store.history_entry_count(pid) == history_before
    assert_recovered_matches(runtime, pid, before)


def test_reconsider_rolls_back_all_context_mutations_on_persistence_failure(tmp_path: Path, monkeypatch):
    runtime = build_runtime(tmp_path)
    runtime.start_investigation()
    runtime.recognize_decision({"id": "D1"}, RECOGNITION)
    runtime.begin_implementation()
    runtime.record_artifact({"path": "artifact"})
    runtime.begin_verification()
    runtime.record_verification({"passed": False})
    pid = runtime.process_instance.process_instance_id
    before = runtime.context.to_dict()
    history_before = runtime.store.history_entry_count(pid)
    fail_context_persistence(runtime, monkeypatch)

    with pytest.raises(PersistenceError):
        runtime.reconsider({"description": "verification evidence requires rework"})

    assert runtime.context.to_dict() == before
    assert runtime.store.history_entry_count(pid) == history_before
    assert_recovered_matches(runtime, pid, before)


def test_engineering_completion_rolls_back_on_persistence_failure(tmp_path: Path, monkeypatch):
    runtime = build_runtime(tmp_path)
    runtime.start_investigation()
    runtime.recognize_decision({"id": "D1"}, RECOGNITION)
    runtime.begin_implementation()
    runtime.record_artifact({"path": "artifact"})
    runtime.begin_verification()
    runtime.record_verification({"passed": True})
    pid = runtime.process_instance.process_instance_id
    before = runtime.context.to_dict()
    history_before = runtime.store.history_entry_count(pid)
    fail_context_persistence(runtime, monkeypatch)

    with pytest.raises(PersistenceError):
        runtime.recognize_engineering_completion(RECOGNITION)

    assert runtime.context.to_dict() == before
    assert runtime.store.history_entry_count(pid) == history_before
    assert_recovered_matches(runtime, pid, before)


def test_begin_implementation_rolls_back_pending_execution_when_state_persistence_fails(
    tmp_path: Path, monkeypatch
):
    runtime = build_runtime(tmp_path)
    runtime.start_investigation()
    runtime.recognize_decision({"id": "D1"}, RECOGNITION)
    pid = runtime.process_instance.process_instance_id
    before = runtime.context.to_dict()
    fail_context_persistence(runtime, monkeypatch)

    with pytest.raises(PersistenceError):
        runtime.begin_implementation()

    assert runtime.context.to_dict() == before
    assert_recovered_matches(runtime, pid, before)


def test_begin_verification_rolls_back_verification_reset_when_state_persistence_fails(
    tmp_path: Path, monkeypatch
):
    runtime = build_runtime(tmp_path)
    runtime.start_investigation()
    runtime.recognize_decision({"id": "D1"}, RECOGNITION)
    runtime.begin_implementation()
    runtime.record_artifact({"path": "artifact"})
    runtime.context.verification = {"previous": "value"}
    runtime.store.save_context(runtime.context, {"type": "test_seed_verification"})
    pid = runtime.process_instance.process_instance_id
    before = runtime.context.to_dict()
    fail_context_persistence(runtime, monkeypatch)

    with pytest.raises(PersistenceError):
        runtime.begin_verification()

    assert runtime.context.to_dict() == before
    assert_recovered_matches(runtime, pid, before)
