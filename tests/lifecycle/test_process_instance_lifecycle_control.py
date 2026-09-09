"""Targeted behavioral validation for Process Instance lifecycle control.

These tests intentionally target semantic behavior rather than a prescribed
Runtime API. The current prototype exposes no lifecycle-control operation;
the adapter below therefore fails explicitly until the implementation exposes
an externally meaningful lifecycle-control mechanism.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

import pytest

from runtime.core import ProcessStore, Runtime


DECISION = {"recognized": True, "basis": "applicable decision gate satisfied"}
COMPLETION = {
    "recognized": True,
    "basis": "applicable engineering completion conditions satisfied",
}


def build_runtime(tmp_path: Path, runtime_id: str = "lifecycle-test") -> Runtime:
    runtime = Runtime(ProcessStore(tmp_path), runtime_id)
    runtime.create_process("Targeted Process Instance lifecycle validation")
    return runtime


def lifecycle_determination(
    runtime: Runtime,
    transition: str,
    *,
    authority: str = "authorized-controller",
    condition: str = "applicable lifecycle condition satisfied",
    actor: str = "validation-agent",
    evidence: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    return {
        "target_process_instance_id": runtime.process_instance.process_instance_id,
        "requested_transition": transition,
        "semantic_basis": condition,
        "authority_context": authority,
        "actor": actor,
        "evidence": evidence or [{"condition": condition}],
        "occurred_at": "2026-09-09T00:00:00+00:00",
    }


def apply_lifecycle_determination(
    runtime: Runtime, determination: dict[str, Any]
) -> Any:
    """Invoke the implementation's public lifecycle-control surface.

    No method name is normative. Until a lifecycle-control mechanism exists,
    fail explicitly so the missing capability is visible in test results.
    """
    candidates = [
        name
        for name in dir(runtime)
        if "lifecycle" in name.lower()
        and not name.startswith("_")
        and callable(getattr(runtime, name))
    ]
    if not candidates:
        pytest.fail(
            "No public lifecycle-control mechanism is exposed by Runtime; "
            "this scenario is an expected implementation gap, not a reason "
            "to weaken the lifecycle test."
        )
    if len(candidates) > 1:
        pytest.fail(
            "Lifecycle test adapter found multiple public lifecycle-control "
            f"candidates {candidates!r}; select the implementation's intended "
            "semantic control surface without changing the scenario oracle."
        )
    return getattr(runtime, candidates[0])(determination)


def reload_runtime(tmp_path: Path, process_instance_id: str, runtime_id: str) -> Runtime:
    runtime = Runtime(ProcessStore(tmp_path), runtime_id)
    runtime.attach(process_instance_id)
    return runtime


def prepare_verified_completion(runtime: Runtime) -> None:
    runtime.start_investigation()
    runtime.recognize_decision({"id": "D1"}, DECISION)
    runtime.begin_implementation()
    runtime.record_artifact({"path": "lifecycle-validation-artifact"})
    runtime.begin_verification()
    runtime.record_verification({"passed": True, "checks": ["lifecycle precondition"]})
    runtime.recognize_engineering_completion(COMPLETION)


def test_lc01_authorized_suspension(tmp_path: Path):
    runtime = build_runtime(tmp_path)
    apply_lifecycle_determination(
        runtime, lifecycle_determination(runtime, "ACTIVE -> SUSPENDED")
    )
    assert runtime.process_instance.lifecycle == "suspended"
    assert runtime.store.load_instance(runtime.process_instance.process_instance_id).lifecycle == "suspended"


def test_lc02_unauthorized_suspension_does_not_mutate_lifecycle(tmp_path: Path):
    runtime = build_runtime(tmp_path)
    determination = lifecycle_determination(
        runtime, "ACTIVE -> SUSPENDED", authority="unauthorized-source"
    )
    with pytest.raises((PermissionError, RuntimeError, ValueError)):
        apply_lifecycle_determination(runtime, determination)
    assert runtime.process_instance.lifecycle == "active"


def test_lc03_suspension_persists_across_runtime_loss(tmp_path: Path):
    runtime = build_runtime(tmp_path)
    process_instance_id = runtime.process_instance.process_instance_id
    apply_lifecycle_determination(
        runtime, lifecycle_determination(runtime, "ACTIVE -> SUSPENDED")
    )
    runtime.stop()
    recovered = reload_runtime(tmp_path, process_instance_id, "replacement-runtime")
    assert recovered.process_instance.lifecycle == "suspended"


def test_lc04_suspension_preserves_continuation_state(tmp_path: Path):
    runtime = build_runtime(tmp_path)
    runtime.start_investigation()
    runtime.recognize_decision({"id": "D1"}, DECISION)
    runtime.begin_implementation()
    runtime.set_pending_execution({"id": "W1", "status": "ready"})
    process_instance_id = runtime.process_instance.process_instance_id
    context_before = runtime.context.to_dict()
    apply_lifecycle_determination(
        runtime,
        lifecycle_determination(
            runtime,
            "ACTIVE -> SUSPENDED",
            condition="continued execution is presently impermissible",
        ),
    )
    recovered = reload_runtime(tmp_path, process_instance_id, "replacement-runtime")
    assert recovered.process_instance.lifecycle == "suspended"
    assert recovered.context.pending_execution == context_before["pending_execution"]
    assert recovered.context.process_state == context_before["process_state"]


def test_lc05_recovery_does_not_resume(tmp_path: Path):
    runtime = build_runtime(tmp_path)
    process_instance_id = runtime.process_instance.process_instance_id
    apply_lifecycle_determination(
        runtime, lifecycle_determination(runtime, "ACTIVE -> SUSPENDED")
    )
    runtime.stop()
    recovered = reload_runtime(tmp_path, process_instance_id, "replacement-runtime")
    assert recovered.process_instance.lifecycle == "suspended"


def test_lc06_resume_requires_valid_reevaluation(tmp_path: Path):
    runtime = build_runtime(tmp_path)
    apply_lifecycle_determination(
        runtime, lifecycle_determination(runtime, "ACTIVE -> SUSPENDED")
    )
    apply_lifecycle_determination(
        runtime,
        lifecycle_determination(
            runtime,
            "SUSPENDED -> ACTIVE",
            condition="suspension condition ceased and continuation is now permissible",
        ),
    )
    assert runtime.process_instance.lifecycle == "active"


def test_lc07_reevaluation_can_keep_process_suspended(tmp_path: Path):
    runtime = build_runtime(tmp_path)
    apply_lifecycle_determination(
        runtime, lifecycle_determination(runtime, "ACTIVE -> SUSPENDED")
    )
    with pytest.raises((PermissionError, RuntimeError, ValueError)):
        apply_lifecycle_determination(
            runtime,
            lifecycle_determination(
                runtime,
                "SUSPENDED -> ACTIVE",
                condition="suspension condition remains applicable",
            ),
        )
    assert runtime.process_instance.lifecycle == "suspended"


def test_lc08_changed_continuation_invalidates_stale_pending_work(tmp_path: Path):
    runtime = build_runtime(tmp_path)
    runtime.start_investigation()
    runtime.recognize_decision({"id": "D1"}, DECISION)
    runtime.begin_implementation()
    runtime.set_pending_execution({"id": "W1", "status": "ready"})
    apply_lifecycle_determination(
        runtime, lifecycle_determination(runtime, "ACTIVE -> SUSPENDED")
    )
    apply_lifecycle_determination(
        runtime,
        lifecycle_determination(
            runtime,
            "SUSPENDED -> ACTIVE",
            condition="W1 is no longer valid; replacement continuation W2 is required",
            evidence=[{"stale_work": "W1"}, {"replacement_work": "W2"}],
        ),
    )
    pending_ids = {work.get("id") for work in runtime.context.pending_execution}
    assert "W1" not in pending_ids
    assert runtime.process_instance.lifecycle == "active"


def test_lc09_active_termination(tmp_path: Path):
    runtime = build_runtime(tmp_path)
    apply_lifecycle_determination(
        runtime,
        lifecycle_determination(
            runtime,
            "ACTIVE -> TERMINATED",
            condition="Process Instance must no longer continue as the same lifecycle instance",
        ),
    )
    assert runtime.process_instance.lifecycle == "terminated"
    assert runtime.store.load_instance(runtime.process_instance.process_instance_id).lifecycle == "terminated"


def test_lc10_suspended_termination(tmp_path: Path):
    runtime = build_runtime(tmp_path)
    apply_lifecycle_determination(
        runtime, lifecycle_determination(runtime, "ACTIVE -> SUSPENDED")
    )
    apply_lifecycle_determination(
        runtime,
        lifecycle_determination(
            runtime,
            "SUSPENDED -> TERMINATED",
            condition="Process Instance must no longer continue as the same lifecycle instance",
        ),
    )
    assert runtime.process_instance.lifecycle == "terminated"


def test_lc11_terminated_instance_is_terminal(tmp_path: Path):
    runtime = build_runtime(tmp_path)
    apply_lifecycle_determination(
        runtime, lifecycle_determination(runtime, "ACTIVE -> TERMINATED")
    )
    for transition in ("TERMINATED -> ACTIVE", "TERMINATED -> SUSPENDED"):
        with pytest.raises((PermissionError, RuntimeError, ValueError)):
            apply_lifecycle_determination(runtime, lifecycle_determination(runtime, transition))
        assert runtime.process_instance.lifecycle == "terminated"


def test_lc12_unauthorized_termination_does_not_mutate_lifecycle(tmp_path: Path):
    runtime = build_runtime(tmp_path)
    with pytest.raises((PermissionError, RuntimeError, ValueError)):
        apply_lifecycle_determination(
            runtime,
            lifecycle_determination(runtime, "ACTIVE -> TERMINATED", authority="unauthorized-source"),
        )
    assert runtime.process_instance.lifecycle == "active"


def test_lc13_lifecycle_history_reconstructs_material_transition_chain(tmp_path: Path):
    runtime = build_runtime(tmp_path)
    process_instance_id = runtime.process_instance.process_instance_id
    apply_lifecycle_determination(
        runtime, lifecycle_determination(runtime, "ACTIVE -> SUSPENDED")
    )
    apply_lifecycle_determination(
        runtime,
        lifecycle_determination(
            runtime,
            "SUSPENDED -> ACTIVE",
            condition="suspension condition ceased",
        ),
    )
    apply_lifecycle_determination(
        runtime,
        lifecycle_determination(
            runtime,
            "ACTIVE -> TERMINATED",
            condition="Process Instance must no longer continue",
        ),
    )
    history = runtime.store.history(process_instance_id)
    lifecycle_events = [event for event in history if "lifecycle" in str(event).lower()]
    assert len(lifecycle_events) >= 3
    serialized = str(lifecycle_events)
    assert "SUSPENDED" in serialized
    assert "ACTIVE" in serialized
    assert "TERMINATED" in serialized


def test_lc14_engineering_completion_does_not_terminate_instance(tmp_path: Path):
    runtime = build_runtime(tmp_path)
    prepare_verified_completion(runtime)
    assert runtime.context.engineering_completion is True
    assert runtime.process_instance.lifecycle == "active"


def test_lc15_runtime_interruption_does_not_change_lifecycle(tmp_path: Path):
    runtime = build_runtime(tmp_path)
    process_instance_id = runtime.process_instance.process_instance_id
    runtime.stop()
    recovered = reload_runtime(tmp_path, process_instance_id, "replacement-runtime")
    assert recovered.process_instance.lifecycle == "active"


def test_lc16_conflicting_conditions_do_not_silently_choose_invalid_transition(tmp_path: Path):
    runtime = build_runtime(tmp_path)
    determination = lifecycle_determination(
        runtime,
        "ACTIVE -> SUSPENDED",
        condition="conflicting suspension and continuation conditions",
        evidence=[
            {"condition": "continued execution impermissible"},
            {"condition": "continued execution permissible"},
            {"conflict": True},
        ],
    )
    with pytest.raises((PermissionError, RuntimeError, ValueError)):
        apply_lifecycle_determination(runtime, determination)
    assert runtime.process_instance.lifecycle == "active"
