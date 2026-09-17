"""Tests for ProcessStore.history_entry_count() utility.

Covers:
  1. Returns 0 for a Process Instance with no history file yet.
  2. Returns 1 immediately after process creation (one 'process_created' entry).
  3. Count increases correctly as Runtime operations append further history entries.
  4. Count for one Process Instance is unaffected by operations on a second instance.
"""
from __future__ import annotations

import pytest
from pathlib import Path

from runtime.core.store import ProcessStore
from runtime.core.models import ProcessInstance, ExecutionContext


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def store(tmp_path: Path) -> ProcessStore:
    return ProcessStore(tmp_path)


def _make_process(store: ProcessStore, objective: str = "test objective") -> str:
    """Create a minimal Process Instance and return its ID."""
    instance = ProcessInstance.create(objective)
    context = ExecutionContext.create(instance)
    store.create(instance, context)
    return instance.process_instance_id


# ---------------------------------------------------------------------------
# 1. Unknown / empty instance returns 0
# ---------------------------------------------------------------------------

def test_returns_zero_for_empty_instance(store: ProcessStore, tmp_path: Path) -> None:
    """history_entry_count returns 0 when no history file exists."""
    # Manufacture a directory but do NOT write a history.jsonl inside it.
    pid = "00000000-0000-0000-0000-000000000000"
    (tmp_path / "process-instance" / pid).mkdir(parents=True)

    assert store.history_entry_count(pid) == 0


# ---------------------------------------------------------------------------
# 2. One entry after creation
# ---------------------------------------------------------------------------

def test_one_entry_after_creation(store: ProcessStore) -> None:
    """A newly created Process Instance has exactly one history entry."""
    pid = _make_process(store)
    assert store.history_entry_count(pid) == 1


# ---------------------------------------------------------------------------
# 3. Count grows with each save_context call
# ---------------------------------------------------------------------------

def test_count_grows_with_operations(store: ProcessStore) -> None:
    """Each save_context call appends one history entry; count tracks correctly."""
    instance = ProcessInstance.create("growing objective")
    context = ExecutionContext.create(instance)
    store.create(instance, context)
    pid = instance.process_instance_id

    assert store.history_entry_count(pid) == 1  # process_created

    context.process_state = "investigation"
    store.save_context(context, {"type": "investigation_started", "runtime_id": "test"})
    assert store.history_entry_count(pid) == 2

    context.process_state = "implementation"
    store.save_context(context, {"type": "implementation_started", "runtime_id": "test"})
    assert store.history_entry_count(pid) == 3


# ---------------------------------------------------------------------------
# 4. Isolation: one instance does not affect another's count
# ---------------------------------------------------------------------------

def test_isolation_between_instances(store: ProcessStore) -> None:
    """Operations on one Process Instance do not change another's count."""
    pid_a = _make_process(store, "objective A")
    pid_b = _make_process(store, "objective B")

    # Perform extra saves on instance B only.
    context_b = store.load_context(pid_b)
    context_b.process_state = "investigation"
    store.save_context(context_b, {"type": "investigation_started", "runtime_id": "test"})

    # A still has 1 entry; B has 2.
    assert store.history_entry_count(pid_a) == 1
    assert store.history_entry_count(pid_b) == 2
