from pathlib import Path

import pytest

from runtime.core import ProcessStore, Runtime
from runtime.core.store import JsonlStore


DECISION = {"recognized": True, "basis": "applicable decision gate satisfied"}
COMPLETION = {"recognized": True, "basis": "applicable engineering completion conditions satisfied"}


def build_runtime(tmp_path: Path) -> Runtime:
    runtime = Runtime(ProcessStore(tmp_path), "runtime-test")
    runtime.create_process("Implement Add_Review_Form business_id conversion")
    return runtime


def prepare_verification(runtime: Runtime) -> None:
    runtime.start_investigation()
    runtime.observe({"fact": "POST_SELECT returns a WordPress post ID; reviews store a custom business-table ID"})
    runtime.recognize_decision({"id": "D1", "conclusion": "translate WP post ID through Business_Repository::find_by_post_id"}, DECISION)
    runtime.begin_implementation()
    runtime.record_artifact({"path": "modules/reviews/forms/add-review-form.php"})
    runtime.begin_verification()


def lifecycle_determination(runtime: Runtime, transition: str, *, basis: str = "applicable lifecycle condition", evidence=None):
    return {
        "target_process_instance_id": runtime.process_instance.process_instance_id,
        "requested_transition": transition,
        "semantic_basis": basis,
        "authority_context": "authorized-controller",
        "actor": "test-controller",
        "evidence": evidence or [],
        "occurred_at": "2026-09-09T00:00:00+00:00",
    }


def test_required_lifecycle_transitions(tmp_path: Path):
    runtime = build_runtime(tmp_path)

    runtime.start_investigation()
    assert runtime.context.process_state == Runtime.INVESTIGATION

    runtime.recognize_decision({"id": "D1"}, DECISION)
    runtime.begin_implementation()
    assert runtime.context.process_state == Runtime.IMPLEMENTATION

    runtime.record_artifact({"path": "add-review-form.php"})
    runtime.begin_verification()
    assert runtime.context.process_state == Runtime.VERIFICATION

    runtime.record_verification({"passed": True, "checks": ["php -l", "structural inspection"]})
    runtime.recognize_engineering_completion(COMPLETION)
    assert runtime.context.process_state == Runtime.ENGINEERING_COMPLETE
    assert runtime.context.engineering_completion is True


def test_transition_conditions_are_enforced(tmp_path: Path):
    runtime = build_runtime(tmp_path)

    with pytest.raises(RuntimeError):
        runtime.begin_implementation()

    runtime.start_investigation()
    with pytest.raises(RuntimeError):
        runtime.begin_implementation()

    runtime.recognize_decision({"id": "D1"}, DECISION)
    runtime.begin_implementation()

    with pytest.raises(RuntimeError):
        runtime.begin_verification()

    runtime.record_artifact({"path": "add-review-form.php"})
    runtime.set_pending_execution({"id": "W1", "status": "partial"})
    with pytest.raises(RuntimeError):
        runtime.begin_verification()


def test_failed_verification_preserves_failure_and_reopens_investigation(tmp_path: Path):
    runtime = build_runtime(tmp_path)
    prepare_verification(runtime)
    runtime.record_verification({"passed": False, "failure": "verification check failed"})

    runtime.reconsider({"description": "implementation must be reconsidered after failed verification"})

    assert runtime.context.process_state == Runtime.INVESTIGATION
    assert runtime.context.failure_uncertainty[-1]["description"].startswith("implementation must")
    assert runtime.context.unresolved_matters[-1].startswith("implementation must")


def test_completion_cannot_bypass_verification(tmp_path: Path):
    runtime = build_runtime(tmp_path)
    runtime.start_investigation()
    runtime.recognize_decision({"id": "D1"}, DECISION)
    runtime.begin_implementation()
    runtime.record_artifact({"path": "add-review-form.php"})

    with pytest.raises(RuntimeError):
        runtime.recognize_engineering_completion(COMPLETION)

    runtime.begin_verification()
    runtime.record_verification({"passed": False})
    with pytest.raises(RuntimeError):
        runtime.recognize_engineering_completion(COMPLETION)


def test_pending_execution_cannot_bypass_decision_gate(tmp_path: Path):
    runtime = build_runtime(tmp_path)
    runtime.start_investigation()

    with pytest.raises(RuntimeError):
        runtime.set_pending_execution({"id": "W1", "status": "partial"})

    assert runtime.context.process_state == Runtime.INVESTIGATION
    assert runtime.context.pending_execution == []


def test_suspended_observation_and_recognition_remain_informational(tmp_path: Path):
    runtime = build_runtime(tmp_path)
    runtime.apply_lifecycle_determination(
        lifecycle_determination(runtime, "ACTIVE -> SUSPENDED", basis="execution temporarily paused")
    )

    runtime.observe({"fact": "new evidence arrived while suspended"})
    runtime.recognize_decision({"id": "D-suspended"}, DECISION)

    assert runtime.process_instance.lifecycle == "suspended"
    assert runtime.context.evidence[-1]["fact"] == "new evidence arrived while suspended"
    assert runtime.context.engineering_decisions[-1]["id"] == "D-suspended"

    with pytest.raises(RuntimeError):
        runtime.begin_implementation()


def test_lifecycle_persistence_failure_restores_files_and_authoritative_in_memory_state(tmp_path: Path, monkeypatch):
    runtime = build_runtime(tmp_path)
    runtime.context.process_state = Runtime.IMPLEMENTATION
    runtime.set_pending_execution({"id": "W1", "status": "partial"})
    runtime.apply_lifecycle_determination(
        lifecycle_determination(runtime, "ACTIVE -> SUSPENDED", basis="execution temporarily paused")
    )

    process_id = runtime.process_instance.process_instance_id
    process_path = runtime.store._dir(process_id) / "process.json"
    context_path = runtime.store._dir(process_id) / "context.json"
    history_path = runtime.store._dir(process_id) / "history.jsonl"
    before = {path: path.read_bytes() for path in (process_path, context_path, history_path)}
    prior_lifecycle = runtime.process_instance.lifecycle
    prior_context = runtime.context.to_dict()

    original_append = JsonlStore.append

    def failing_append(self, event):
        if self.path == history_path and event.get("type") == "lifecycle_transition":
            raise RuntimeError("injected lifecycle history failure")
        return original_append(self, event)

    monkeypatch.setattr(JsonlStore, "append", failing_append)

    with pytest.raises(RuntimeError, match="injected lifecycle history failure"):
        runtime.apply_lifecycle_determination(
            lifecycle_determination(
                runtime,
                "SUSPENDED -> ACTIVE",
                basis="suspension condition ceased",
                evidence=[{"stale_work": "W1"}],
            )
        )

    assert runtime.process_instance.lifecycle == prior_lifecycle
    assert runtime.context.to_dict() == prior_context
    assert {path: path.read_bytes() for path in (process_path, context_path, history_path)} == before
    assert runtime.store.load_instance(process_id).lifecycle == prior_lifecycle
    assert runtime.store.load_context(process_id).to_dict() == prior_context
