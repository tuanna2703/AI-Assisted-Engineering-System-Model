"""Process Instance and authoritative Context persistence boundary."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from runtime.core.models import ExecutionContext, ProcessInstance, VALID_LIFECYCLE_VALUES, now
from runtime.persistence.json_store import JsonStore, JsonlStore, PersistenceError


class ProcessStore:
    def __init__(self, root: str | Path) -> None:
        self.root = Path(root)

    def _dir(self, process_instance_id: str) -> Path:
        return self.root / "process-instance" / process_instance_id

    def create(self, instance: ProcessInstance, context: ExecutionContext) -> None:
        directory = self._dir(instance.process_instance_id)
        JsonStore(directory / "process.json").save(instance.to_dict())
        JsonStore(directory / "context.json").save(context.to_dict())
        JsonlStore(directory / "history.jsonl").append({"type": "process_created", "process_instance_id": instance.process_instance_id, "version": context.version, "at": now()})

    def load_instance(self, process_instance_id: str) -> ProcessInstance:
        data = JsonStore(self._dir(process_instance_id) / "process.json").load()
        instance = ProcessInstance(**data)
        if instance.lifecycle not in VALID_LIFECYCLE_VALUES:
            raise PersistenceError(
                f"invalid persisted lifecycle value: {instance.lifecycle!r}"
            )
        return instance

    def load_context(self, process_instance_id: str) -> ExecutionContext:
        data = JsonStore(self._dir(process_instance_id) / "context.json").load()
        try:
            context = ExecutionContext.from_dict(data)
        except (TypeError, ValueError) as exc:
            raise PersistenceError(f"authoritative context is invalid: {process_instance_id}") from exc
        if context.process_instance_id != process_instance_id:
            raise PersistenceError("context identity does not match Process Instance")
        return context

    def save_context(self, context: ExecutionContext, event: dict[str, Any]) -> None:
        directory = self._dir(context.process_instance_id)
        if not directory.exists():
            raise PersistenceError("Process Instance does not exist")

        context_path = directory / "context.json"
        history_path = directory / "history.jsonl"
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
        """Persist a lifecycle transition as one recoverable consistency boundary.

        The JSON stores use atomic file replacement individually, while the
        lifecycle operation spans process state, optional Context mutation, and
        history. Snapshotting the affected files allows the complete operation
        to be rolled back if any write fails, including a partially appended
        history record.
        """
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
            JsonlStore(history_path).append({**event, "at": now()})
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
        return JsonlStore(self._dir(process_instance_id) / "history.jsonl").read_all()
