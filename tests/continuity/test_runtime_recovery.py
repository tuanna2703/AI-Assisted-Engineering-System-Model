from pathlib import Path

import pytest

from runtime.core import ProcessInstance, ProcessStore, Runtime
from runtime.core.models import ExecutionContext
from runtime.persistence.json_store import PersistenceError


DECISION_RECOGNITION = {"recognized": True, "basis": "applicable decision gate satisfied"}
EVIDENCE_RECOGNITION = {"recognized": True, "basis": "workspace inspection established the observation as recordable evidence"}
COMPLETION_RECOGNITION = {"recognized": True, "basis": "applicable engineering completion conditions satisfied"}


def test_process_instance_creation():
    instance = ProcessInstance.create(
        "Implement feature X",
        epm={"id": "example-epm"},
        pem={"id": "example-pem"},
    )

    assert instance.process_instance_id
    assert instance.engineering_objective == "Implement feature X"
    assert instance.lifecycle == "active"
    assert instance.execution_context_ref == (
        f"process-instance/{instance.process_instance_id}/context.json"
    )
    assert instance.epm == {"id": "example-epm"}
    assert instance.pem == {"id": "example-pem"}
    assert instance.created_at
    assert instance.updated_at


def test_execution_context_contains_minimum_authoritative_information():
    instance = ProcessInstance.create(
        "Implement feature X",
        epm={"id": "example-epm", "version": "1.0"},
    )
    context = ExecutionContext.create(instance)

    assert context.process_instance_id == instance.process_instance_id
    assert context.engineering_objective == instance.engineering_objective
    assert context.process_state == "initial"
    assert context.execution_mode == "active"
    assert context.requirements == []
    assert context.constraints == []
    assert context.evidence == []
    assert context.assumptions == []
    assert context.risks == []
    assert context.engineering_decisions == []
    assert context.decision_gates == []
    assert context.artifacts == []
    assert context.verification == {}
    assert context.unresolved_matters == []
    assert context.pending_execution == []
    assert context.execution_determination is None
    assert context.failure_uncertainty == []
    assert context.engineering_completion is False


def test_execution_context_round_trip_preserves_semantic_state():
    instance = ProcessInstance.create("Implement feature X")
    context = ExecutionContext.create(instance)
    context.process_state = "implementation"
    context.evidence = [{"fact": "existing implementation found"}]
    context.engineering_decisions = [{"id": "D1", "conclusion": "use existing extension point"}]
    context.unresolved_matters = ["verification remains outstanding"]
    context.pending_execution = [
        {
            "id": "W1",
            "status": "partial",
            "artifact": "feature.py",
            "next_action": "complete implementation",
            "resumption_conditions": ["required implementation changes are available"],
        }
    ]
    context.failure_uncertainty = [{"kind": "uncertainty", "description": "verification not yet performed"}]
    context.version = 3

    restored = ExecutionContext.from_dict(context.to_dict())

    assert restored.to_dict() == context.to_dict()
    assert restored.process_instance_id == instance.process_instance_id
    assert restored.pending_execution[0]["next_action"] == "complete implementation"
    assert restored.pending_execution[0]["resumption_conditions"] == [
        "required implementation changes are available"
    ]


def test_evidence_requires_explicit_recognition(tmp_path: Path):
    runtime = Runtime(ProcessStore(tmp_path), "runtime-a")
    runtime.create_process("Implement feature X")

    with pytest.raises(TypeError):
        runtime.observe({"fact": "candidate observation"})

    with pytest.raises(RuntimeError):
        runtime.observe({
            "fact": "candidate observation",
            "recognition": {"recognized": False, "basis": "proposal only"},
        })

    with pytest.raises(RuntimeError):
        runtime.observe({
            "fact": "candidate observation",
            "recognition": {"recognized": True},
        })

    assert runtime.context.evidence == []


def test_recognized_evidence_is_recorded_without_process_state_mutation(tmp_path: Path):
    store = ProcessStore(tmp_path)
    runtime = Runtime(store, "runtime-a")
    pid = runtime.create_process("Implement feature X")

    runtime.observe({
        "source": "workspace",
        "fact": "existing implementation found",
        "recognition": EVIDENCE_RECOGNITION,
    })

    assert runtime.context.evidence == [
        {"source": "workspace", "fact": "existing implementation found"}
    ]
    assert runtime.context.process_state == "initial"
    assert runtime.context.engineering_decisions == []
    history = store.history(pid)
    assert history[-1]["type"] == "evidence_recorded"
    assert history[-1]["recognition"] == EVIDENCE_RECOGNITION


def test_assumption_or_claim_is_not_silently_promoted_to_evidence(tmp_path: Path):
    runtime = Runtime(ProcessStore(tmp_path), "runtime-a")
    runtime.create_process("Implement feature X")

    with pytest.raises(RuntimeError):
        runtime.observe({
            "kind": "assumption",
            "statement": "the existing extension point is sufficient",
            "recognition": {"recognized": False, "basis": "unverified assumption"},
        })

    with pytest.raises(RuntimeError):
        runtime.observe({
            "kind": "claim",
            "statement": "the implementation is complete",
            "recognition": {"recognized": False, "basis": "unsupported claim"},
        })

    assert runtime.context.evidence == []


def test_failed_evidence_persistence_restores_in_memory_authoritative_state(tmp_path: Path, monkeypatch):
    store = ProcessStore(tmp_path)
    runtime = Runtime(store, "runtime-a")
    pid = runtime.create_process("Implement feature X")
    prior_version = runtime.context.version

    def fail_save_context(context, event):
        context.version += 1
        raise PersistenceError("simulated evidence persistence failure")

    monkeypatch.setattr(store, "save_context", fail_save_context)

    with pytest.raises(PersistenceError):
        runtime.observe({
            "fact": "new evidence",
            "recognition": EVIDENCE_RECOGNITION,
        })

    assert runtime.context.evidence == []
    assert runtime.context.version == prior_version
    restored = store.load_context(pid)
    assert restored.evidence == []


def test_process_and_context_survive_runtime_replacement(tmp_path: Path):
    store = ProcessStore(tmp_path)
    runtime_a = Runtime(store, "runtime-a")
    pid = runtime_a.create_process("Implement feature X")
    runtime_a.start_investigation()
    runtime_a.observe({
        "source": "workspace",
        "fact": "existing implementation found",
        "recognition": EVIDENCE_RECOGNITION,
    })
    runtime_a.recognize_decision({"id": "D1", "conclusion": "use existing extension point"}, DECISION_RECOGNITION)
    runtime_a.begin_implementation()
    runtime_a.set_pending_execution(
        {
            "id": "W1",
            "status": "partial",
            "artifact": "feature.py",
            "next_action": "complete implementation",
            "resumption_conditions": ["required implementation changes are available"],
        }
    )
    runtime_a.stop()

    runtime_b = Runtime(store, "runtime-b")
    runtime_b.attach(pid)

    assert runtime_b.process_instance.process_instance_id == pid
    assert runtime_b.context.engineering_objective == "Implement feature X"
    assert runtime_b.context.evidence[0]["fact"] == "existing implementation found"
    assert runtime_b.context.engineering_decisions[0]["id"] == "D1"
    assert runtime_b.context.pending_execution[0]["status"] == "partial"
    assert runtime_b.context.pending_execution[0]["next_action"] == "complete implementation"
    assert runtime_b.context.pending_execution[0]["resumption_conditions"] == [
        "required implementation changes are available"
    ]


def test_decision_requires_explicit_recognition(tmp_path: Path):
    store = ProcessStore(tmp_path)
    runtime = Runtime(store, "runtime-a")
    runtime.create_process("Implement feature X")

    with pytest.raises(RuntimeError):
        runtime.recognize_decision({"id": "D1"}, {"recognized": False, "basis": "proposal only"})

    with pytest.raises(RuntimeError):
        runtime.recognize_decision({"id": "D1"}, {"recognized": True})


def test_engineering_completion_requires_explicit_recognition(tmp_path: Path):
    store = ProcessStore(tmp_path)
    runtime = Runtime(store, "runtime-a")
    runtime.create_process("Implement feature X")

    with pytest.raises(RuntimeError):
        runtime.recognize_engineering_completion({"recognized": False, "basis": "verification passed"})

    runtime.record_verification({"passed": True, "command": "pytest"})
    assert runtime.context.engineering_completion is False

    runtime.recognize_engineering_completion(COMPLETION_RECOGNITION)
    assert runtime.context.engineering_completion is True
    assert runtime.context.process_state == "engineering_complete"


def test_missing_context_fails_recovery(tmp_path: Path):
    store = ProcessStore(tmp_path)
    runtime = Runtime(store, "runtime-a")
    pid = runtime.create_process("Implement feature X")
    (tmp_path / "process-instance" / pid / "context.json").unlink()

    with pytest.raises(PersistenceError):
        Runtime(store, "runtime-b").attach(pid)


def test_history_is_preserved(tmp_path: Path):
    store = ProcessStore(tmp_path)
    runtime = Runtime(store, "runtime-a")
    pid = runtime.create_process("Implement feature X")
    runtime.observe({"fact": "A", "recognition": EVIDENCE_RECOGNITION})
    runtime.recognize_decision({"id": "D1"}, DECISION_RECOGNITION)
    runtime.stop()

    history = store.history(pid)
    assert [event["type"] for event in history] == [
        "process_created",
        "evidence_recorded",
        "engineering_decision_recognized",
    ]
