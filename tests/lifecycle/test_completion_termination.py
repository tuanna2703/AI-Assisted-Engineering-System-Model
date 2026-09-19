"""Focused behavioral coverage for completion/termination boundaries.

These tests verify that engineering completion, Runtime interruption, and
Process Instance lifecycle termination remain distinct. They intentionally
exercise the existing public lifecycle-control surface rather than prescribe a
new Runtime API.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from runtime.core import ActiveRepositoryContext, ProcessStore, Runtime


DECISION = {"recognized": True, "basis": "applicable decision gate satisfied"}
COMPLETION = {
    "recognized": True,
    "basis": "applicable engineering completion conditions satisfied",
}


def build_runtime(tmp_path: Path) -> Runtime:
    ctx = ActiveRepositoryContext(tmp_path)
    runtime = Runtime(ctx, "completion-termination-test")
    runtime.create_process("Completion and termination boundary validation")
    return runtime


def lifecycle_determination(
    runtime: Runtime,
    transition: str,
    *,
    basis: str = "applicable lifecycle condition satisfied",
) -> dict[str, Any]:
    return {
        "target_process_instance_id": runtime.process_instance.process_instance_id,
        "requested_transition": transition,
        "semantic_basis": basis,
        "authority_context": "authorized-controller",
        "actor": "validation-controller",
        "evidence": [{"condition": basis}],
        "occurred_at": "2026-09-16T00:00:00+00:00",
    }


def prepare_verified_completion(runtime: Runtime) -> None:
    runtime.start_investigation()
    runtime.recognize_decision({"id": "D1"}, DECISION)
    runtime.begin_implementation()
    runtime.record_artifact({"path": "completion-termination-validation-artifact"})
    runtime.begin_verification()
    runtime.record_verification({"passed": True, "checks": ["completion precondition"]})


def test_engineering_completion_does_not_terminate_process_instance(tmp_path: Path):
    runtime = build_runtime(tmp_path)
    prepare_verified_completion(runtime)

    runtime.recognize_engineering_completion(COMPLETION)

    process_id = runtime.process_instance.process_instance_id
    assert runtime.context.engineering_completion is True
    assert runtime.context.process_state == Runtime.ENGINEERING_COMPLETE
    assert runtime.process_instance.lifecycle == "active"
    assert runtime.store.load_instance(process_id).lifecycle == "active"


def test_engineering_completion_requires_successful_verification(tmp_path: Path):
    runtime = build_runtime(tmp_path)
    runtime.start_investigation()
    runtime.recognize_decision({"id": "D1"}, DECISION)
    runtime.begin_implementation()
    runtime.record_artifact({"path": "artifact"})
    runtime.begin_verification()
    runtime.record_verification({"passed": False})

    with pytest.raises(RuntimeError):
        runtime.recognize_engineering_completion(COMPLETION)

    assert runtime.context.engineering_completion is False
    assert runtime.context.process_state == Runtime.VERIFICATION
    assert runtime.process_instance.lifecycle == "active"


def test_runtime_stop_does_not_terminate_process_instance(tmp_path: Path):
    ctx = ActiveRepositoryContext(tmp_path)
    runtime = build_runtime(tmp_path)
    process_id = runtime.process_instance.process_instance_id

    runtime.stop()

    recovered = Runtime(ctx, "replacement-runtime")
    recovered.attach(process_id)
    assert recovered.process_instance.lifecycle == "active"


def test_explicit_termination_is_persisted_and_recovered(tmp_path: Path):
    ctx = ActiveRepositoryContext(tmp_path)
    runtime = build_runtime(tmp_path)
    process_id = runtime.process_instance.process_instance_id

    runtime.apply_lifecycle_determination(
        lifecycle_determination(
            runtime,
            "ACTIVE -> TERMINATED",
            basis="Process Instance must no longer continue as the same lifecycle instance",
        )
    )

    assert runtime.process_instance.lifecycle == "terminated"
    assert runtime.store.load_instance(process_id).lifecycle == "terminated"

    recovered = Runtime(ctx, "replacement-runtime")
    recovered.attach(process_id)
    assert recovered.process_instance.lifecycle == "terminated"


def test_terminated_process_instance_rejects_further_lifecycle_transitions(tmp_path: Path):
    runtime = build_runtime(tmp_path)
    runtime.apply_lifecycle_determination(
        lifecycle_determination(
            runtime,
            "ACTIVE -> TERMINATED",
            basis="Process Instance must no longer continue as the same lifecycle instance",
        )
    )

    for transition in ("TERMINATED -> ACTIVE", "TERMINATED -> SUSPENDED"):
        with pytest.raises(RuntimeError):
            runtime.apply_lifecycle_determination(
                lifecycle_determination(runtime, transition)
            )

    assert runtime.process_instance.lifecycle == "terminated"


def test_termination_does_not_require_engineering_completion(tmp_path: Path):
    runtime = build_runtime(tmp_path)

    runtime.apply_lifecycle_determination(
        lifecycle_determination(
            runtime,
            "ACTIVE -> TERMINATED",
            basis="Process Instance must no longer continue as the same lifecycle instance",
        )
    )

    assert runtime.context.engineering_completion is False
    assert runtime.process_instance.lifecycle == "terminated"
