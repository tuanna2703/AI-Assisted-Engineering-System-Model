from pathlib import Path

import pytest

from runtime.core import ProcessStore, Runtime


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
