"""Process Instance and authoritative Context persistence boundary.

Storage layout (repository-local):

    <repository-root>/.aesm/<process-instance-id>/
        process.json
        context.json
        history.jsonl

The ProcessStore receives an already-established ActiveRepositoryContext.
It never discovers or selects the repository independently.
The workspace-level `.aesm-process-store/` layout is superseded.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from runtime.core.models import (
    ExecutionContext,
    ProcessInstance,
    CURRENT_PERSISTED_SCHEMA_VERSION,
    VALID_LIFECYCLE_VALUES,
    VALID_SCOPE_RESOLUTION_STATUSES,
    now,
)
from runtime.core.repository_context import ActiveRepositoryContext
from runtime.persistence.json_store import JsonStore, JsonlStore, PersistenceError


# ---------------------------------------------------------------------------
# Git conflict marker detection
# ---------------------------------------------------------------------------

_CONFLICT_MARKERS: tuple[bytes, ...] = (b"<<<<<<<", b"=======", b">>>>>>>")


def _check_conflict(path: Path) -> None:
    """Raise PersistenceError if the file contains Git conflict markers.

    An unresolved Git conflict in AESM PI state must not be executed against.
    The caller is required to resolve the conflict before accessing the PI.
    """
    if not path.exists():
        return
    content = path.read_bytes()
    if any(marker in content for marker in _CONFLICT_MARKERS):
        raise PersistenceError(
            f"unresolved Git conflict in PI state: {path}; "
            "resolve conflict before executing this Process Instance"
        )


class ProcessStore:
    """Repository-local Process Instance persistence boundary.

    Receives a validated ``ActiveRepositoryContext`` and resolves all PI
    storage relative to ``context.aesm_root() / <process_instance_id>``.

    The store does not discover the repository independently.  The context
    is the single authoritative source of the persistence root.
    """

    def __init__(self, repository_context: ActiveRepositoryContext) -> None:
        self._repository_context = repository_context
        self.root = repository_context.aesm_root()

    def _dir(self, process_instance_id: str) -> Path:
        """Return the authoritative storage directory for a Process Instance.

        Layout: ``<repository-root>/.aesm/<process-instance-id>/``
        """
        return self.root / process_instance_id

    def create(self, instance: ProcessInstance, context: ExecutionContext) -> None:
        directory = self._dir(instance.process_instance_id)
        JsonStore(directory / "process.json").save(instance.to_dict())
        JsonStore(directory / "context.json").save(context.to_dict())
        JsonlStore(directory / "history.jsonl").append(
            {
                "type": "process_created",
                "process_instance_id": instance.process_instance_id,
                "version": context.version,
                "engineering_scope_resolution": instance.engineering_scope_resolution,
                "engineering_scope_identity": instance.engineering_scope_identity,
                "at": now(),
            }
        )

    def list_instances(self) -> list[ProcessInstance]:
        """Enumerate valid Process Instances in this repository's .aesm boundary.

        Enumeration is strictly repository-local. Filesystem ordering is not
        used as a selection rule; callers must apply explicit deterministic
        resolution semantics.
        """
        if not self.root.exists():
            return []

        instances: list[ProcessInstance] = []
        for directory in sorted(self.root.iterdir(), key=lambda path: path.name):
            if not directory.is_dir():
                continue
            process_path = directory / "process.json"
            if not process_path.exists():
                continue
            instances.append(self.load_instance(directory.name))
        return instances

    def load_instance(self, process_instance_id: str) -> ProcessInstance:
        process_path = self._dir(process_instance_id) / "process.json"
        _check_conflict(process_path)
        data = JsonStore(process_path).load()
        schema_version = data.get("schema_version", 1)
        if schema_version != CURRENT_PERSISTED_SCHEMA_VERSION:
            raise PersistenceError(
                f"unsupported Process Instance schema version: {schema_version!r}; "
                f"supported version is {CURRENT_PERSISTED_SCHEMA_VERSION}"
            )
        try:
            instance = ProcessInstance(**data)
        except (TypeError, ValueError) as exc:
            raise PersistenceError(f"Process Instance is invalid: {process_instance_id}") from exc

        if instance.lifecycle not in VALID_LIFECYCLE_VALUES:
            raise PersistenceError(
                f"invalid persisted lifecycle value: {instance.lifecycle!r}"
            )
        if instance.engineering_scope_resolution not in VALID_SCOPE_RESOLUTION_STATUSES:
            raise PersistenceError(
                "invalid persisted Engineering Scope resolution status: "
                f"{instance.engineering_scope_resolution!r}"
            )
        if instance.engineering_scope_resolution == "RESOLVED":
            if not instance.engineering_scope_identity:
                raise PersistenceError(
                    "resolved Engineering Scope is missing its identity"
                )
        elif instance.engineering_scope_identity is not None:
            raise PersistenceError(
                "unresolved Engineering Scope cannot contain an authoritative identity"
            )
        return instance

    def load_context(self, process_instance_id: str) -> ExecutionContext:
        context_path = self._dir(process_instance_id) / "context.json"
        _check_conflict(context_path)
        data = JsonStore(context_path).load()
        try:
            context = ExecutionContext.from_dict(data)
        except (TypeError, ValueError) as exc:
            raise PersistenceError(f"authoritative context is invalid: {process_instance_id}") from exc
        if context.process_instance_id != process_instance_id:
            raise PersistenceError("context identity does not match Process Instance")
        return context

    def save_process_instance(
        self,
        instance: ProcessInstance,
        event: dict[str, Any],
        *,
        expected_updated_at: str | None = None,
    ) -> None:
        """Persist authoritative Process Instance identity/binding and history."""
        directory = self._dir(instance.process_instance_id)
        if not directory.exists():
            raise PersistenceError("Process Instance does not exist")
        if instance.lifecycle not in VALID_LIFECYCLE_VALUES:
            raise PersistenceError(
                f"invalid lifecycle value: {instance.lifecycle!r}"
            )
        if instance.engineering_scope_resolution not in VALID_SCOPE_RESOLUTION_STATUSES:
            raise PersistenceError(
                "invalid Engineering Scope resolution status: "
                f"{instance.engineering_scope_resolution!r}"
            )
        if instance.engineering_scope_resolution == "RESOLVED":
            if not instance.engineering_scope_identity:
                raise PersistenceError(
                    "resolved Engineering Scope is missing its identity"
                )
        elif instance.engineering_scope_identity is not None:
            raise PersistenceError(
                "unresolved Engineering Scope cannot contain an authoritative identity"
            )

        process_path = directory / "process.json"
        history_path = directory / "history.jsonl"

        # Optimistic stale-write guard for Process Instance state.  The Runtime
        # instance carries the timestamp it loaded; another writer changing the
        # persisted Process Instance must therefore be detected before overwrite.
        if process_path.exists():
            try:
                persisted_data = json.loads(process_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as exc:
                raise PersistenceError("cannot validate Process Instance concurrency state") from exc
            persisted_updated_at = persisted_data.get("updated_at")
            expected = instance.updated_at if expected_updated_at is None else expected_updated_at
            if persisted_updated_at != expected:
                raise PersistenceError(
                    "stale Process Instance write rejected: persisted Process Instance "
                    "has changed since this Runtime loaded it; reload before writing"
                )

        snapshots = {
            process_path: process_path.read_bytes() if process_path.exists() else None,
            history_path: history_path.read_bytes() if history_path.exists() else None,
        }
        prior_updated_at = instance.updated_at

        try:
            instance.updated_at = now()
            JsonStore(process_path).save(instance.to_dict())
            JsonlStore(history_path).append(
                {
                    **event,
                    "at": now(),
                    "process_instance_updated_at": instance.updated_at,
                }
            )
        except Exception:
            instance.updated_at = prior_updated_at
            self._restore_file(process_path, snapshots[process_path])
            self._restore_file(history_path, snapshots[history_path])
            raise

    def save_context(self, context: ExecutionContext, event: dict[str, Any]) -> None:
        directory = self._dir(context.process_instance_id)
        if not directory.exists():
            raise PersistenceError("Process Instance does not exist")

        context_path = directory / "context.json"
        history_path = directory / "history.jsonl"

        # Stale-write guard: reject if persisted state is newer than in-memory state.
        # This protects against a Runtime loaded at version N overwriting a newer
        # version N+1 written by another environment.
        if context_path.exists():
            try:
                persisted_data = json.loads(context_path.read_text(encoding="utf-8"))
                persisted_version = persisted_data.get("version", 0)
            except (OSError, json.JSONDecodeError):
                persisted_version = 0
            if persisted_version > context.version:
                raise PersistenceError(
                    f"stale write rejected: persisted context version {persisted_version} "
                    f"is newer than in-memory version {context.version}; "
                    "reload the Process Instance before writing"
                )

        snapshots = {
            context_path: context_path.read_bytes() if context_path.exists() else None,
            history_path: history_path.read_bytes() if history_path.exists() else None,
        }
        prior_version = context.version
        prior_updated_at = context.updated_at

        try:
            context.version += 1
            context.updated_at = now()
            JsonStore(context_path).save(context.to_dict())
            JsonlStore(history_path).append({**event, "version": context.version, "at": now()})
        except Exception:
            context.version = prior_version
            context.updated_at = prior_updated_at
            self._restore_file(context_path, snapshots[context_path])
            self._restore_file(history_path, snapshots[history_path])
            raise

    def save_lifecycle(
        self,
        instance: ProcessInstance,
        context: ExecutionContext,
        event: dict[str, Any],
        *,
        context_modified: bool = False,
    ) -> None:
        """Persist a lifecycle transition as one recoverable consistency boundary."""
        directory = self._dir(instance.process_instance_id)
        if not directory.exists():
            raise PersistenceError("Process Instance does not exist")
        if instance.lifecycle not in VALID_LIFECYCLE_VALUES:
            raise PersistenceError(
                f"invalid lifecycle value: {instance.lifecycle!r}"
            )

        process_path = directory / "process.json"
        context_path = directory / "context.json"
        history_path = directory / "history.jsonl"

        if process_path.exists():
            try:
                persisted_data = json.loads(process_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as exc:
                raise PersistenceError("cannot validate Process Instance concurrency state") from exc
            if persisted_data.get("updated_at") != instance.updated_at:
                raise PersistenceError(
                    "stale Process Instance lifecycle write rejected: persisted Process Instance "
                    "has changed since this Runtime loaded it; reload before writing"
                )

        snapshots = {
            process_path: process_path.read_bytes() if process_path.exists() else None,
            context_path: context_path.read_bytes() if context_path.exists() else None,
            history_path: history_path.read_bytes() if history_path.exists() else None,
        }
        prior_instance_updated_at = instance.updated_at
        prior_context_version = context.version
        prior_context_updated_at = context.updated_at

        try:
            instance.updated_at = now()
            JsonStore(process_path).save(instance.to_dict())
            if context_modified:
                context.version += 1
                context.updated_at = now()
                JsonStore(context_path).save(context.to_dict())
            JsonlStore(history_path).append(
                {
                    **event,
                    "at": now(),
                    "process_instance_updated_at": instance.updated_at,
                    "context_version": context.version,
                }
            )
        except Exception:
            instance.updated_at = prior_instance_updated_at
            context.version = prior_context_version
            context.updated_at = prior_context_updated_at
            self._restore_file(process_path, snapshots[process_path])
            self._restore_file(context_path, snapshots[context_path])
            self._restore_file(history_path, snapshots[history_path])
            raise

    @staticmethod
    def _restore_file(path: Path, content: bytes | None) -> None:
        if content is None:
            try:
                path.unlink()
            except FileNotFoundError:
                pass
            return
        path.write_bytes(content)

    def history(self, process_instance_id: str) -> list[dict[str, Any]]:
        history_path = self._dir(process_instance_id) / "history.jsonl"
        _check_conflict(history_path)
        return JsonlStore(history_path).read_all()

    def history_entry_count(self, process_instance_id: str) -> int:
        """Return the number of history entries for a Process Instance."""
        return len(self.history(process_instance_id))
