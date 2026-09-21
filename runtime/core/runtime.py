"""Minimal Runtime control surface for continuity and lifecycle experiments."""
from __future__ import annotations

from typing import Any

from runtime.core.models import ExecutionContext, ProcessInstance, VALID_LIFECYCLE_VALUES, now
from runtime.core.repository_context import ActiveRepositoryContext
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
    """Small, inspectable Runtime implementation; not a normative semantic layer.

    Architectural contract:

        Execution Environment
                │
                │ establishes repository context
                ▼
        Runtime(repository_context, runtime_id)
                │
                ▼ constructs
        ProcessStore
                │
                ▼
        <repository-root>/.aesm

    The ``repository_context`` is the sole ingress for repository identity.
    It is immutable for the lifetime of this Runtime instance.
    Changing repositories requires a new Runtime/session context.
    """

    INVESTIGATION = "investigation"
    IMPLEMENTATION = "implementation"
    VERIFICATION = "verification"
    ENGINEERING_COMPLETE = "engineering_complete"

    def __init__(self, repository_context: ActiveRepositoryContext, runtime_id: str) -> None:
        self._repository_context = repository_context
        self.store = ProcessStore(repository_context)
        self.runtime_id = runtime_id
        self.process_instance: ProcessInstance | None = None
        self.context: ExecutionContext | None = None
        self.attached = False

    @property
    def repository_context(self) -> ActiveRepositoryContext:
        """Return the active repository context for this Runtime session (read-only)."""
        return self._repository_context

    def create_process(
        self,
        objective: str,
        engineering_scope_identity: str | None = None,
    ) -> str:
        if not objective or not str(objective).strip():
            raise ValueError("objective must be a non-empty string")
        if engineering_scope_identity is not None and not str(engineering_scope_identity).strip():
            raise ValueError("engineering_scope_identity must be non-empty when provided")

        instance = ProcessInstance.create(
            objective,
            engineering_scope_identity=engineering_scope_identity,
        )
        context = ExecutionContext.create(instance)
        self.store.create(instance, context)
        self.process_instance, self.context, self.attached = instance, context, True
        return instance.process_instance_id

    def attach(self, process_instance_id: str) -> None:
        instance = self.store.load_instance(process_instance_id)
        context = self.store.load_context(process_instance_id)
        self.process_instance, self.context, self.attached = instance, context, True

    def apply_scope_resolution(self, resolution: dict[str, Any]) -> None:
        """Record an authoritative Engineering Scope resolution outcome.

        The Runtime is the authority boundary. The Agent may submit evidence or
        a proposed outcome through the bridge, but only a recognized Runtime
        resolution becomes the Process Instance binding.
        """
        self._require_attached()
        if not isinstance(resolution, dict):
            raise TypeError("scope resolution must be a mapping")

        required_fields = {
            "status",
            "recognized",
            "basis",
            "actor",
            "evidence",
        }
        missing = required_fields - resolution.keys()
        if missing:
            raise ValueError(
                f"scope resolution missing required fields: {sorted(missing)}"
            )

        status = resolution["status"]
        if status not in {
            "UNRESOLVED",
            "RESOLVED",
            "AMBIGUOUS",
            "CONFLICTING",
            "INVALID",
        }:
            raise ValueError(f"invalid Engineering Scope resolution status: {status!r}")
        if resolution["recognized"] is not True:
            raise RuntimeError(
                "Engineering Scope resolution must be explicitly recognized by "
                "the governing execution semantics"
            )
        if not resolution["basis"]:
            raise RuntimeError("Engineering Scope resolution requires an explicit basis")
        if not isinstance(resolution["evidence"], list):
            raise TypeError("Engineering Scope resolution evidence must be a list")

        identity = resolution.get("engineering_scope_identity")
        if status == "RESOLVED":
            if not isinstance(identity, str) or not identity.strip():
                raise ValueError(
                    "RESOLVED Engineering Scope requires a non-empty identity"
                )
        elif identity is not None:
            raise ValueError(
                f"{status} Engineering Scope resolution cannot contain an identity"
            )

        current_status = self.process_instance.engineering_scope_resolution
        current_identity = self.process_instance.engineering_scope_identity
        if current_status == "RESOLVED":
            if status != "RESOLVED" or identity != current_identity:
                raise RuntimeError(
                    "an established Engineering Scope binding cannot be silently "
                    "replaced or invalidated"
                )
            return

        prior_status = current_status
        prior_identity = current_identity
        prior_evidence = list(self.process_instance.engineering_scope_evidence)
        prior_updated_at = self.process_instance.updated_at

        self.process_instance.engineering_scope_resolution = status
        self.process_instance.engineering_scope_identity = identity
        self.process_instance.engineering_scope_evidence = list(resolution["evidence"])
        self.process_instance.updated_at = now()

        event = {
            "type": "engineering_scope_resolution",
            "process_instance_id": self.process_instance.process_instance_id,
            "prior_status": prior_status,
            "prior_identity": prior_identity,
            "resulting_status": status,
            "resulting_identity": identity,
            "basis": resolution["basis"],
            "actor": resolution["actor"],
            "evidence": resolution["evidence"],
            "runtime_id": self.runtime_id,
        }

        try:
            self.store.save_process_instance(self.process_instance, event)
        except Exception:
            self.process_instance.engineering_scope_resolution = prior_status
            self.process_instance.engineering_scope_identity = prior_identity
            self.process_instance.engineering_scope_evidence = prior_evidence
            self.process_instance.updated_at = prior_updated_at
            raise

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
        prior_context = self.context.to_dict()
        self.context.pending_execution = []
        try:
            self._set_state(self.IMPLEMENTATION, "implementation_started")
        except Exception:
            self.context = ExecutionContext.from_dict(prior_context)
            raise

    def set_pending_execution(self, work: dict[str, Any]) -> None:
        """Record continuation work without changing Process State implicitly."""
        self._require_attached()
        self._require_active_lifecycle()
        self._require_state(self.IMPLEMENTATION)
        prior_context = self.context.to_dict()
        self.context.pending_execution.append(work)
        try:
            self.store.save_context(self.context, {"type": "pending_execution_recorded", "work": work, "runtime_id": self.runtime_id})
        except Exception:
            self.context = ExecutionContext.from_dict(prior_context)
            raise

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
        prior_context = self.context.to_dict()
        self.context.verification = {}
        try:
            self._set_state(self.VERIFICATION, "verification_started")
        except Exception:
            self.context = ExecutionContext.from_dict(prior_context)
            raise

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
        prior_context = self.context.to_dict()
        self.context.failure_uncertainty.append(reason)
        self.context.unresolved_matters.append(reason["description"])
        try:
            self._set_state(self.INVESTIGATION, "reconsideration_requested", {"reason": reason})
        except Exception:
            self.context = ExecutionContext.from_dict(prior_context)
            raise

    def recognize_engineering_completion(self, completion: dict[str, Any]) -> None:
        self._require_attached()
        self._require_active_lifecycle()
        self._require_recognition(completion, "completion")
        if self.context.process_state != self.VERIFICATION:
            raise RuntimeError("engineering completion requires the verification state")
        if self.context.verification.get("passed") is not True:
            raise RuntimeError("engineering completion requires successful verification")
        prior_context = self.context.to_dict()
        self.context.engineering_completion = True
        try:
            self._set_state(self.ENGINEERING_COMPLETE, "engineering_completion_recognized", {"completion": completion})
        except Exception:
            self.context = ExecutionContext.from_dict(prior_context)
            raise

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
        """Persist a process-state transition atomically from the Runtime view."""
        prior_context = self.context.to_dict()
        self.context.process_state = state
        event = {"type": event_type, "runtime_id": self.runtime_id}
        if extra:
            event.update(extra)
        try:
            self.store.save_context(self.context, event)
        except Exception:
            self.context = ExecutionContext.from_dict(prior_context)
            raise

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
