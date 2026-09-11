"""Minimal Runtime control surface for continuity and lifecycle experiments."""
from __future__ import annotations

from typing import Any

from runtime.core.models import ExecutionContext, ProcessInstance, VALID_LIFECYCLE_VALUES
from runtime.core.store import ProcessStore


# --- Lifecycle transition graph ---

_TRANSITION_GRAPH: dict[tuple[str, str], str] = {
    ("active", "suspended"): "suspended",
    ("suspended", "active"): "active",
    ("active", "terminated"): "terminated",
    ("suspended", "terminated"): "terminated",
}

_SEMANTIC_TO_CANONICAL = {
    "ACTIVE": "active",
    "SUSPENDED": "suspended",
    "TERMINATED": "terminated",
}


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
        self._require_attached()
        self._require_active_lifecycle()
        self._require_state("initial")
        self._set_state(self.INVESTIGATION, "investigation_started")

    def observe(self, observation: dict[str, Any]) -> None:
        """Record an explicitly recognized evidence contribution.

        Observation remains available while suspended, but receipt alone does not
        promote a contribution into authoritative Evidence.
        """
        self._require_attached()
        if not isinstance(observation, dict):
            raise TypeError("observation must be a mapping")
        self._require_recognition(observation.get("recognition"), "evidence")

        evidence = {key: value for key, value in observation.items() if key != "recognition"}
        prior_evidence = list(self.context.evidence)
        prior_version = self.context.version
        prior_updated_at = self.context.updated_at
        self.context.evidence.append(evidence)
        try:
            self.store.save_context(
                self.context,
                {
                    "type": "evidence_recorded",
                    "evidence": evidence,
                    "recognition": observation["recognition"],
                    "runtime_id": self.runtime_id,
                },
            )
        except Exception:
            self.context.evidence = prior_evidence
            self.context.version = prior_version
            self.context.updated_at = prior_updated_at
            raise

    def recognize_decision(self, decision: dict[str, Any], recognition: dict[str, Any]) -> None:
        """Record a recognized decision without defining its engineering validity."""
        self._require_attached()
        self._require_recognition(recognition, "decision")
        if self.context.process_state not in {self.INVESTIGATION, "initial"}:
            raise RuntimeError("engineering decisions can only be recognized during investigation")
        prior_decisions = list(self.context.engineering_decisions)
        prior_version = self.context.version
        prior_updated_at = self.context.updated_at
        self.context.engineering_decisions.append(decision)
        try:
            self.store.save_context(self.context, {"type": "engineering_decision_recognized", "decision": decision, "recognition": recognition, "runtime_id": self.runtime_id})
        except Exception:
            self.context.engineering_decisions = prior_decisions
            self.context.version = prior_version
            self.context.updated_at = prior_updated_at
            raise

    def begin_implementation(self) -> None:
        self._require_attached()
        self._require_active_lifecycle()
        self._require_state(self.INVESTIGATION)
        if not self.context.engineering_decisions:
            raise RuntimeError("implementation requires a recognized engineering decision")
        self.context.pending_execution = []
        self._set_state(self.IMPLEMENTATION, "implementation_started")

    def set_pending_execution(self, work: dict[str, Any]) -> None:
        """Record continuation work without changing Process State implicitly."""
        self._require_attached()
        self._require_active_lifecycle()
        self._require_state(self.IMPLEMENTATION)
        self.context.pending_execution.append(work)
        self.store.save_context(self.context, {"type": "pending_execution_recorded", "work": work, "runtime_id": self.runtime_id})

    def record_artifact(self, artifact: dict[str, Any]) -> None:
        self._require_attached()
        self._require_active_lifecycle()
        self._require_state(self.IMPLEMENTATION)
        prior_artifacts = list(self.context.artifacts)
        prior_version = self.context.version
        prior_updated_at = self.context.updated_at
        self.context.artifacts.append(artifact)
        try:
            self.store.save_context(self.context, {"type": "artifact_recorded", "artifact": artifact, "runtime_id": self.runtime_id})
        except Exception:
            self.context.artifacts = prior_artifacts
            self.context.version = prior_version
            self.context.updated_at = prior_updated_at
            raise

    def begin_verification(self) -> None:
        self._require_attached()
        self._require_active_lifecycle()
        self._require_state(self.IMPLEMENTATION)
        if not self.context.artifacts:
            raise RuntimeError("verification requires at least one recorded implementation artifact")
        if self.context.pending_execution:
            raise RuntimeError("verification requires no pending execution work")
        self.context.verification = {}
        self._set_state(self.VERIFICATION, "verification_started")

    def record_verification(self, result: dict[str, Any]) -> None:
        """Record verification; the legacy path remains usable for continuity experiments."""
        self._require_attached()
        self._require_active_lifecycle()
        if self.context.process_state not in {"initial", self.IMPLEMENTATION, self.VERIFICATION}:
            raise RuntimeError("verification can only be recorded before completion")
        prior_verification = self.context.verification
        prior_process_state = self.context.process_state
        prior_version = self.context.version
        prior_updated_at = self.context.updated_at
        self.context.verification = result
        if self.context.process_state != self.VERIFICATION:
            self.context.process_state = self.VERIFICATION
        try:
            self.store.save_context(self.context, {"type": "verification_recorded", "result": result, "runtime_id": self.runtime_id})
        except Exception:
            self.context.verification = prior_verification
            self.context.process_state = prior_process_state
            self.context.version = prior_version
            self.context.updated_at = prior_updated_at
            raise

    def reconsider(self, reason: dict[str, Any]) -> None:
        self._require_attached()
        self._require_active_lifecycle()
        self._require_state(self.VERIFICATION)
        if self.context.verification.get("passed") is True:
            raise RuntimeError("successful verification does not require reconsideration")
        if not isinstance(reason, dict) or not reason.get("description"):
            raise ValueError("reconsideration requires a descriptive reason")
        self.context.failure_uncertainty.append(reason)
        self.context.unresolved_matters.append(reason["description"])
        self._set_state(self.INVESTIGATION, "reconsideration_requested", {"reason": reason})

    def recognize_engineering_completion(self, completion: dict[str, Any]) -> None:
        self._require_attached()
        self._require_active_lifecycle()
        self._require_recognition(completion, "completion")
        if self.context.process_state != self.VERIFICATION:
            raise RuntimeError("engineering completion requires the verification state")
        if self.context.verification.get("passed") is not True:
            raise RuntimeError("engineering completion requires successful verification")
        self.context.engineering_completion = True
        self._set_state(self.ENGINEERING_COMPLETE, "engineering_completion_recognized", {"completion": completion})

    # --- Lifecycle control boundary ---

    def apply_lifecycle_determination(self, determination: dict[str, Any]) -> None:
        """Authoritative lifecycle-control operation."""
        self._require_attached()

        if not isinstance(determination, dict):
            raise ValueError("lifecycle determination must be a mapping")
        required_fields = {
            "target_process_instance_id",
            "requested_transition",
            "semantic_basis",
            "authority_context",
            "actor",
            "evidence",
            "occurred_at",
        }
        missing = required_fields - determination.keys()
        if missing:
            raise ValueError(f"lifecycle determination missing required fields: {sorted(missing)}")

        if determination["target_process_instance_id"] != self.process_instance.process_instance_id:
            raise ValueError("lifecycle determination targets a different Process Instance")

        transition_str = determination["requested_transition"]
        source_semantic, target_semantic = self._parse_transition(transition_str)
        source_canonical = _SEMANTIC_TO_CANONICAL.get(source_semantic)
        target_canonical = _SEMANTIC_TO_CANONICAL.get(target_semantic)
        if source_canonical is None or target_canonical is None:
            raise ValueError(f"unrecognized lifecycle state in transition: {transition_str!r}")

        authority = determination["authority_context"]
        if authority != "authorized-controller":
            raise PermissionError(
                f"lifecycle determination rejected: unauthorized authority context {authority!r}"
            )

        semantic_basis = determination.get("semantic_basis", "")
        if not semantic_basis or not str(semantic_basis).strip():
            raise ValueError("lifecycle determination requires a non-empty semantic basis")

        current_lifecycle = self.process_instance.lifecycle
        if current_lifecycle != source_canonical:
            raise RuntimeError(
                f"lifecycle transition {transition_str!r} requires current lifecycle "
                f"{source_semantic!r} but Process Instance is {current_lifecycle!r}"
            )

        transition_key = (source_canonical, target_canonical)
        if transition_key not in _TRANSITION_GRAPH:
            raise RuntimeError(
                f"lifecycle transition {transition_str!r} is not a valid transition"
            )

        evidence = determination.get("evidence") or []
        for entry in evidence:
            if isinstance(entry, dict) and entry.get("conflict") is True:
                raise RuntimeError(
                    "lifecycle determination contains an explicit unresolved conflict; "
                    "transition rejected"
                )

        basis_lower = str(semantic_basis).lower()
        if source_canonical == "suspended" and target_canonical == "active":
            self._validate_resumption(basis_lower, evidence)

        prior_lifecycle = self.process_instance.lifecycle
        prior_context = self.context.to_dict()
        context_modified = False
        if source_canonical == "suspended" and target_canonical == "active":
            context_modified = self._apply_stale_work_invalidation(evidence)

        self.process_instance.lifecycle = target_canonical

        lifecycle_event = {
            "type": "lifecycle_transition",
            "process_instance_id": self.process_instance.process_instance_id,
            "prior_lifecycle": prior_lifecycle,
            "requested_transition": transition_str,
            "authority_context": determination["authority_context"],
            "actor": determination["actor"],
            "semantic_basis": semantic_basis,
            "evidence": evidence,
            "resulting_lifecycle": target_canonical,
            "runtime_id": self.runtime_id,
            "occurred_at": determination["occurred_at"],
        }

        try:
            self.store.save_lifecycle(
                self.process_instance,
                self.context,
                lifecycle_event,
                context_modified=context_modified,
            )
        except Exception:
            self.process_instance.lifecycle = prior_lifecycle
            self.context = ExecutionContext.from_dict(prior_context)
            raise

    # --- End lifecycle control boundary ---

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

    def _require_active_lifecycle(self) -> None:
        """Guard: engineering execution is only permitted when lifecycle is active."""
        if self.process_instance.lifecycle != "active":
            raise RuntimeError(
                f"engineering execution is blocked: Process Instance lifecycle is "
                f"{self.process_instance.lifecycle!r}, not 'active'"
            )

    @staticmethod
    def _parse_transition(transition_str: str) -> tuple[str, str]:
        """Parse a transition string like 'ACTIVE -> SUSPENDED' into (source, target)."""
        separator = "→" if "→" in transition_str else "->"
        parts = [p.strip() for p in transition_str.split(separator)]
        if len(parts) != 2 or not parts[0] or not parts[1]:
            raise ValueError(f"invalid transition format: {transition_str!r}")
        return parts[0], parts[1]

    @staticmethod
    def _validate_resumption(basis_lower: str, evidence: list[dict[str, Any]]) -> None:
        """Validate that a resumption determination establishes permissibility."""
        if "remains applicable" in basis_lower:
            raise RuntimeError(
                "resumption rejected: suspension condition remains applicable"
            )

        resumption_established = False
        if "ceased" in basis_lower or "permissible" in basis_lower:
            resumption_established = True

        if not resumption_established:
            for entry in evidence:
                if isinstance(entry, dict):
                    entry_str = str(entry).lower()
                    if "ceased" in entry_str or "permissible" in entry_str:
                        resumption_established = True
                        break
                    if "stale_work" in entry:
                        resumption_established = True
                        break

        if not resumption_established:
            raise RuntimeError(
                "resumption rejected: determination does not establish that "
                "suspension condition has ceased or continuation is permissible"
            )

    def _apply_stale_work_invalidation(self, evidence: list[dict[str, Any]]) -> bool:
        """Remove stale pending execution entries identified by evidence."""
        stale_ids = set()
        for entry in evidence:
            if isinstance(entry, dict) and "stale_work" in entry:
                stale_ids.add(entry["stale_work"])

        if not stale_ids:
            return False

        original_count = len(self.context.pending_execution)
        self.context.pending_execution = [
            work for work in self.context.pending_execution
            if work.get("id") not in stale_ids
        ]
        return len(self.context.pending_execution) != original_count
