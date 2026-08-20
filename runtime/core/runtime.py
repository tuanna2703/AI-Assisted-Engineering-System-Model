"""Minimal Runtime control surface for continuity and conformance experiments."""
from __future__ import annotations

from typing import Any

from runtime.core.models import ExecutionContext, ProcessInstance
from runtime.core.store import ProcessStore


class Runtime:
    """Small, inspectable Runtime implementation; not a normative semantic layer."""

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

    def observe(self, observation: dict[str, Any]) -> None:
        self._require_attached()
        self.context.evidence.append(observation)
        self.store.save_context(self.context, {"type": "observation_recorded", "observation": observation, "runtime_id": self.runtime_id})

    def recognize_decision(self, decision: dict[str, Any], recognition: dict[str, Any]) -> None:
        """Record a recognized decision without defining its engineering validity."""
        self._require_attached()
        self._require_recognition(recognition, "decision")
        self.context.engineering_decisions.append(decision)
        self.store.save_context(self.context, {"type": "engineering_decision_recognized", "decision": decision, "recognition": recognition, "runtime_id": self.runtime_id})

    def set_pending_execution(self, work: dict[str, Any]) -> None:
        self._require_attached()
        self.context.pending_execution.append(work)
        self.context.process_state = "implementation"
        self.store.save_context(self.context, {"type": "pending_execution_recorded", "work": work, "runtime_id": self.runtime_id})

    def record_verification(self, result: dict[str, Any]) -> None:
        self._require_attached()
        self.context.verification = result
        if result.get("passed") is True:
            self.context.pending_execution = []
        self.store.save_context(self.context, {"type": "verification_recorded", "result": result, "runtime_id": self.runtime_id})

    def recognize_engineering_completion(self, completion: dict[str, Any]) -> None:
        """Record completion recognized under applicable EPM/PEM conditions."""
        self._require_attached()
        self._require_recognition(completion, "completion")
        self.context.engineering_completion = True
        self.context.process_state = "engineering_complete"
        self.store.save_context(self.context, {"type": "engineering_completion_recognized", "completion": completion, "runtime_id": self.runtime_id})

    def stop(self) -> None:
        self.attached = False
        self.process_instance = None
        self.context = None

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
