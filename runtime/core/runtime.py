"""Minimal Runtime control surface for continuity and lifecycle experiments."""
from __future__ import annotations

from typing import Any

from runtime.core.models import ExecutionContext, ProcessInstance
from runtime.core.store import ProcessStore


class Runtime:
    """Small, inspectable Runtime implementation; not a normative semantic layer."""

    INVESTIGATION = "investigation"
    IMPLEMENTATION = "implementation"
    VERIFICATION = "verification"
    ENGINEERING_COMPLETE = "engineering_complete"

    def __init__(self, store: ProcessStore, runtime_id: str) -> None:
        self.store = store
        self.runtime_id = runtime_id
        self.process_instance: ProcessInstance | None = None
        self.context: ExecutionContext | None = None
        self.attached = False

    def create_process(self, objective: str) -> str:
        instance = ProcessInstance.create(objective)
        context = ExecutionContext.create(instance)
        self.store.create(instance, context)
        self.process_instance, self.context, self.attached = instance, context, True
        return instance.process_instance_id

    def attach(self, process_instance_id: str) -> None:
        instance = self.store.load_instance(process_instance_id)
        context = self.store.load_context(process_instance_id)
        self.process_instance, self.context, self.attached = instance, context, True

    def start_investigation(self) -> None:
        """Enter investigation from a newly created Process Instance."""
        self._require_attached()
        self._require_state("initial")
        self._set_state(self.INVESTIGATION, "investigation_started")

    def observe(self, observation: dict[str, Any]) -> None:
        self._require_attached()
        self.context.evidence.append(observation)
        self.store.save_context(self.context, {"type": "observation_recorded", "observation": observation, "runtime_id": self.runtime_id})

    def recognize_decision(self, decision: dict[str, Any], recognition: dict[str, Any]) -> None:
        """Record a recognized decision without defining its engineering validity."""
        self._require_attached()
        self._require_recognition(recognition, "decision")
        if self.context.process_state not in {self.INVESTIGATION, "initial"}:
            raise RuntimeError("engineering decisions can only be recognized during investigation")
        self.context.engineering_decisions.append(decision)
        self.store.save_context(self.context, {"type": "engineering_decision_recognized", "decision": decision, "recognition": recognition, "runtime_id": self.runtime_id})

    def begin_implementation(self) -> None:
        """Move investigation to implementation after a recognized decision exists."""
        self._require_attached()
        self._require_state(self.INVESTIGATION)
        if not self.context.engineering_decisions:
            raise RuntimeError("implementation requires a recognized engineering decision")
        self.context.pending_execution = []
        self._set_state(self.IMPLEMENTATION, "implementation_started")

    def set_pending_execution(self, work: dict[str, Any]) -> None:
        self._require_attached()
        self._require_state(self.IMPLEMENTATION)
        self.context.pending_execution.append(work)
        self.store.save_context(self.context, {"type": "pending_execution_recorded", "work": work, "runtime_id": self.runtime_id})

    def record_artifact(self, artifact: dict[str, Any]) -> None:
        self._require_attached()
        self._require_state(self.IMPLEMENTATION)
        self.context.artifacts.append(artifact)
        self.store.save_context(self.context, {"type": "artifact_recorded", "artifact": artifact, "runtime_id": self.runtime_id})

    def begin_verification(self) -> None:
        """Move implementation to verification when recorded work is complete."""
        self._require_attached()
        self._require_state(self.IMPLEMENTATION)
        if not self.context.artifacts:
            raise RuntimeError("verification requires at least one recorded implementation artifact")
        if self.context.pending_execution:
            raise RuntimeError("verification requires no pending execution work")
        self.context.verification = {}
        self._set_state(self.VERIFICATION, "verification_started")

    def record_verification(self, result: dict[str, Any]) -> None:
        self._require_attached()
        self._require_state(self.VERIFICATION)
        self.context.verification = result
        self.store.save_context(self.context, {"type": "verification_recorded", "result": result, "runtime_id": self.runtime_id})

    def reconsider(self, reason: dict[str, Any]) -> None:
        """Preserve failed/uncertain verification and return to investigation."""
        self._require_attached()
        self._require_state(self.VERIFICATION)
        if self.context.verification.get("passed") is True:
            raise RuntimeError("successful verification does not require reconsideration")
        if not isinstance(reason, dict) or not reason.get("description"):
            raise ValueError("reconsideration requires a descriptive reason")
        self.context.failure_uncertainty.append(reason)
        self.context.unresolved_matters.append(reason["description"])
        self._set_state(self.INVESTIGATION, "reconsideration_requested", {"reason": reason})

    def recognize_engineering_completion(self, completion: dict[str, Any]) -> None:
        """Record completion only after successful verification and recognition."""
        self._require_attached()
        self._require_recognition(completion, "completion")
        self._require_state(self.VERIFICATION)
        if self.context.verification.get("passed") is not True:
            raise RuntimeError("engineering completion requires successful verification")
        self.context.engineering_completion = True
        self._set_state(self.ENGINEERING_COMPLETE, "engineering_completion_recognized", {"completion": completion})

    def stop(self) -> None:
        self.attached = False
        self.process_instance = None
        self.context = None

    def _set_state(self, state: str, event_type: str, extra: dict[str, Any] | None = None) -> None:
        self.context.process_state = state
        event = {"type": event_type, "runtime_id": self.runtime_id}
        if extra:
            event.update(extra)
        self.store.save_context(self.context, event)

    def _require_state(self, expected: str) -> None:
        if self.context.process_state != expected:
            raise RuntimeError(
                f"invalid lifecycle transition from {self.context.process_state!r}; expected {expected!r}"
            )

    @staticmethod
    def _require_recognition(recognition: dict[str, Any], kind: str) -> None:
        if not isinstance(recognition, dict):
            raise TypeError(f"{kind} recognition must be a mapping")
        if recognition.get("recognized") is not True:
            raise RuntimeError(f"{kind} must be explicitly recognized by the governing execution semantics")
        if not recognition.get("basis"):
            raise RuntimeError(f"{kind} recognition requires an explicit basis")

    def _require_attached(self) -> None:
        if not self.attached or self.context is None:
            raise RuntimeError("Runtime is not attached to a Process Instance")
