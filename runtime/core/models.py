"""Implementation representations of Process Instance and Execution Context."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class ProcessInstance:
    process_instance_id: str
    engineering_objective: str
    lifecycle: str = "active"
    execution_context_ref: str = ""
    epm: dict[str, str] = field(default_factory=dict)
    pem: dict[str, str] = field(default_factory=dict)
    created_at: str = field(default_factory=now)
    updated_at: str = field(default_factory=now)

    @classmethod
    def create(cls, objective: str, epm: dict[str, str] | None = None, pem: dict[str, str] | None = None) -> "ProcessInstance":
        pid = str(uuid4())
        return cls(pid, objective, execution_context_ref=f"process-instance/{pid}/context.json", epm=epm or {}, pem=pem or {})

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ExecutionContext:
    process_instance_id: str
    engineering_objective: str
    process_state: str = "initial"
    execution_mode: str = "active"
    requirements: list[dict[str, Any]] = field(default_factory=list)
    constraints: list[str] = field(default_factory=list)
    evidence: list[dict[str, Any]] = field(default_factory=list)
    assumptions: list[str] = field(default_factory=list)
    risks: list[str] = field(default_factory=list)
    candidate_solutions: list[dict[str, Any]] = field(default_factory=list)
    engineering_decisions: list[dict[str, Any]] = field(default_factory=list)
    decision_gates: list[dict[str, Any]] = field(default_factory=list)
    artifacts: list[dict[str, Any]] = field(default_factory=list)
    verification: dict[str, Any] = field(default_factory=dict)
    unresolved_matters: list[str] = field(default_factory=list)
    pending_execution: list[dict[str, Any]] = field(default_factory=list)
    execution_determination: dict[str, Any] | None = None
    failure_uncertainty: list[dict[str, Any]] = field(default_factory=list)
    engineering_completion: bool = False
    version: int = 0
    updated_at: str = field(default_factory=now)

    @classmethod
    def create(cls, instance: ProcessInstance) -> "ExecutionContext":
        return cls(instance.process_instance_id, instance.engineering_objective)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ExecutionContext":
        required = {"process_instance_id", "engineering_objective", "process_state", "version"}
        missing = required - data.keys()
        if missing:
            raise ValueError(f"context missing required fields: {sorted(missing)}")
        return cls(**data)
