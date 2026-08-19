"""Process Instance and authoritative Context persistence boundary."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from runtime.core.models import ExecutionContext, ProcessInstance, now
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
        return ProcessInstance(**data)

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
        context.version += 1
        context.updated_at = now()
        JsonStore(directory / "context.json").save(context.to_dict())
        JsonlStore(directory / "history.jsonl").append({**event, "version": context.version, "at": now()})

    def history(self, process_instance_id: str) -> list[dict[str, Any]]:
        return JsonlStore(self._dir(process_instance_id) / "history.jsonl").read_all()
