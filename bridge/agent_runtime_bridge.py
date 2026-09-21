"""Agent–Runtime Bridge: thin adapter/access boundary.

This module implements the authorized Agent–Runtime Bridge — a minimal adapter
that enables an AI Agent to create persistent Process Instances, recover them
by known ID, obtain the Runtime-authoritative Execution Context, dispatch
already-supported Runtime operations, and receive authoritative results/state.

The bridge delegates all authority to the existing Runtime.  It does not own
Process Instance identity, Execution Context semantics, persistence, lifecycle
authority, engineering semantics, or generalized Agent orchestration.

Discovery of an existing Process Instance from an engineering objective is an
explicitly deferred capability.  The bridge does not search for, index,
select, or independently persist Process Instances.
"""
from __future__ import annotations

from typing import Any

from runtime.core.repository_context import ActiveRepositoryContext
from runtime.core.runtime import Runtime
from runtime.persistence.json_store import PersistenceError


# ---------------------------------------------------------------------------
# Supported dispatch operations
# ---------------------------------------------------------------------------
# Maps operation name → (runtime_method_name, param_keys).
# param_keys is a tuple of the keyword argument names expected in `params`.
# An empty tuple means the Runtime method takes no arguments beyond self.
#
# `reconsider` is explicitly authorized as an Agent-facing bridge capability.
# `set_pending_execution` is intentionally absent: it remains a Runtime-owned
# execution-state operation outside the Agent–Runtime Bridge boundary.

_DISPATCH_TABLE: dict[str, tuple[str, tuple[str, ...]]] = {
    "resolve_process_instance": ("resolve_process_instance", ("engineering_scope_identity",)),
    "apply_scope_resolution": ("apply_scope_resolution", ("resolution",)),
    "start_investigation": ("start_investigation", ()),
    "observe": ("observe", ("observation",)),
    "recognize_decision": ("recognize_decision", ("decision", "recognition")),
    "begin_implementation": ("begin_implementation", ()),
    "record_artifact": ("record_artifact", ("artifact",)),
    "begin_verification": ("begin_verification", ()),
    "record_verification": ("record_verification", ("result",)),
    "reconsider": ("reconsider", ("reason",)),
    "recognize_engineering_completion": (
        "recognize_engineering_completion",
        ("completion",),
    ),
}


# ---------------------------------------------------------------------------
# Response helpers
# ---------------------------------------------------------------------------

def _success_response(
    runtime: Runtime,
    *,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build a success response from the current authoritative Runtime state."""
    response: dict[str, Any] = {
        "success": True,
        "process_instance_id": runtime.process_instance.process_instance_id,
        "process_instance": runtime.process_instance.to_dict(),
        "context": runtime.context.to_dict(),
        "error": None,
    }
    if extra:
        response.update(extra)
    return response


def _error_response(
    error_type: str,
    message: str,
    *,
    runtime: Runtime | None = None,
) -> dict[str, Any]:
    """Build an error response, optionally including current state."""
    response: dict[str, Any] = {
        "success": False,
        "process_instance_id": None,
        "process_instance": None,
        "context": None,
        "error": {
            "type": error_type,
            "message": message,
        },
    }
    if runtime is not None and runtime.attached and runtime.process_instance is not None:
        response["process_instance_id"] = runtime.process_instance.process_instance_id
        response["process_instance"] = runtime.process_instance.to_dict()
        response["context"] = runtime.context.to_dict() if runtime.context else None
    return response


# ---------------------------------------------------------------------------
# AgentRuntimeBridge
# ---------------------------------------------------------------------------

class AgentRuntimeBridge:
    """Thin adapter/access boundary between Agent and Runtime.

    The bridge is intentionally disposable.  Destroying or recreating it does
    not destroy Process Instance continuity — continuity belongs to Runtime
    persistence, not bridge memory.

    The bridge holds a reference to a Runtime instance only for the duration
    of an interaction session.  It does not maintain independent authoritative
    state, its own persistence, or a process state machine.
    """

    def __init__(self, repository_context: ActiveRepositoryContext, runtime_id: str = "bridge") -> None:
        self._runtime = Runtime(repository_context, runtime_id)

    # -- Bridge responsibility 1: Process Instance access (creation) --------

    def create_process(self, objective: str) -> dict[str, Any]:
        """Create a new Process Instance through the Runtime.

        Delegates entirely to ``Runtime.create_process(objective)``.
        Returns the authoritative Process Instance identity and initial
        Execution Context.
        """
        if not objective or not str(objective).strip():
            return _error_response("bridge_error", "objective must be a non-empty string")

        try:
            self._runtime.create_process(objective)
        except PersistenceError as exc:
            return _error_response("persistence_error", str(exc))
        except Exception as exc:
            return _error_response("runtime_error", str(exc))

        return _success_response(self._runtime)

    # -- Bridge responsibility 1: Process Instance access (recovery) --------

    def attach(self, process_instance_id: str) -> dict[str, Any]:
        """Recover an existing Process Instance by known ID.

        Delegates entirely to ``Runtime.attach(process_instance_id)``.
        Returns the authoritative recovered state and Execution Context.
        """
        if not process_instance_id or not str(process_instance_id).strip():
            return _error_response(
                "bridge_error",
                "process_instance_id must be a non-empty string",
            )

        try:
            self._runtime.attach(process_instance_id)
        except PersistenceError as exc:
            return _error_response("persistence_error", str(exc))
        except Exception as exc:
            return _error_response("runtime_error", str(exc))

        return _success_response(self._runtime)

    # -- Bridge responsibility 2: Execution Context access ------------------

    def get_context(self) -> dict[str, Any]:
        """Obtain the authoritative current Execution Context.

        This is a read-only state access.  It does not trigger any Runtime
        mutation or guard.  The returned context is a snapshot of
        Runtime-owned state.
        """
        if not self._runtime.attached or self._runtime.context is None:
            return _error_response(
                "bridge_error",
                "no Process Instance is currently attached; "
                "call create_process() or attach() first",
            )

        return _success_response(self._runtime)

    # -- Bridge responsibility 3: Runtime dispatch --------------------------

    def dispatch(self, operation: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Dispatch a supported Runtime operation.

        The bridge routes the operation name to an existing Runtime method,
        unpacks params into method arguments, calls the method, and returns
        the authoritative resulting state (or error).

        The bridge does not reproduce Runtime guards, perform implicit state
        transitions, or fabricate recognition records.  A Runtime rejection
        is authoritative and is returned as-is.
        """
        if not self._runtime.attached or self._runtime.context is None:
            return _error_response(
                "bridge_error",
                "no Process Instance is currently attached; "
                "call create_process() or attach() first",
            )

        if not operation or not isinstance(operation, str):
            return _error_response("bridge_error", "operation must be a non-empty string")

        if operation not in _DISPATCH_TABLE:
            return _error_response(
                "bridge_error",
                f"unsupported operation: {operation!r}; "
                f"supported operations are: {sorted(_DISPATCH_TABLE.keys())}",
            )

        method_name, param_keys = _DISPATCH_TABLE[operation]
        params = params or {}

        # Validate that required params are present.
        missing = [k for k in param_keys if k not in params]
        if missing:
            return _error_response(
                "bridge_error",
                f"operation {operation!r} requires parameters: {list(param_keys)}; "
                f"missing: {missing}",
            )

        # Build the positional arguments for the Runtime method.
        method = getattr(self._runtime, method_name)
        call_args = [params[k] for k in param_keys]
        if operation == "resolve_process_instance" and "process_instance_id" in params:
            call_args.append(params["process_instance_id"])

        try:
            method(*call_args)
        except PersistenceError as exc:
            return _error_response("persistence_error", str(exc), runtime=self._runtime)
        except (RuntimeError, PermissionError) as exc:
            return _error_response("runtime_error", str(exc), runtime=self._runtime)
        except (TypeError, ValueError) as exc:
            return _error_response("runtime_error", str(exc), runtime=self._runtime)

        return _success_response(self._runtime)

    # -- Explicitly unsupported: discovery ----------------------------------

    @staticmethod
    def discover(objective: str) -> dict[str, Any]:
        """Objective-to-Process-Instance discovery — explicitly deferred.

        Discovery is a known deferred capability.  The current Runtime does
        not expose an objective-to-instance search operation.  This method
        exists to provide a deterministic, informative response rather than
        silently failing or implementing bridge-owned discovery.
        """
        return _error_response(
            "unsupported_capability",
            "objective-to-Process-Instance discovery is not currently available; "
            "use create_process() for new requests or attach() with a known "
            "Process Instance ID for continuation",
        )
