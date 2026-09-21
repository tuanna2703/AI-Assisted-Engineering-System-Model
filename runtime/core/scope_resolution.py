"""Deterministic Engineering Scope and Process Instance resolution.

This module contains selection semantics only. It does not persist state and
does not create Process Instances. Runtime remains the authority boundary.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from runtime.core.models import ProcessInstance

ResolutionStatus = Literal[
    "RESOLVED",
    "NO_APPLICABLE_PROCESS_INSTANCE",
    "AMBIGUOUS",
    "INVALID",
]


@dataclass(frozen=True)
class ProcessResolution:
    status: ResolutionStatus
    process_instance_id: str | None = None
    candidate_process_instance_ids: tuple[str, ...] = ()


def resolve_process_instance(
    instances: list[ProcessInstance],
    *,
    engineering_scope_identity: str,
    process_instance_id: str | None = None,
) -> ProcessResolution:
    """Resolve one applicable PI without implicit objective/path heuristics.

    An explicit PI ID is accepted only when it belongs to the active repository
    candidate set and has the requested resolved scope identity. Otherwise the
    result is INVALID rather than a silent fallback.
    """
    if not isinstance(engineering_scope_identity, str) or not engineering_scope_identity.strip():
        return ProcessResolution("INVALID")

    candidates = [
        instance
        for instance in instances
        if instance.engineering_scope_resolution == "RESOLVED"
        and instance.engineering_scope_identity == engineering_scope_identity
    ]
    candidates.sort(key=lambda instance: instance.process_instance_id)

    if process_instance_id is not None:
        matches = [instance for instance in candidates if instance.process_instance_id == process_instance_id]
        if len(matches) != 1:
            return ProcessResolution(
                "INVALID",
                candidate_process_instance_ids=tuple(
                    instance.process_instance_id for instance in candidates
                ),
            )
        return ProcessResolution("RESOLVED", process_instance_id=matches[0].process_instance_id)

    if not candidates:
        return ProcessResolution("NO_APPLICABLE_PROCESS_INSTANCE")

    if len(candidates) > 1:
        return ProcessResolution(
            "AMBIGUOUS",
            candidate_process_instance_ids=tuple(
                instance.process_instance_id for instance in candidates
            ),
        )

    return ProcessResolution("RESOLVED", process_instance_id=candidates[0].process_instance_id)
