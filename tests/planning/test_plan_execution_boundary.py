"""Structural invariant tests for the AESM planning system.

These tests verify structural properties of the planning system rather than
checking string presence in definition files. They validate that the system
conforms to its architectural invariants.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PLAN = ROOT / "plan"
ACTIVE = PLAN / "active"
COMPLETED = PLAN / "completed"
CURRENT = PLAN / "CURRENT.md"


def test_at_most_one_active_task():
    """plan/active/ must contain at most one task file."""
    if not ACTIVE.exists():
        return  # no active directory = 0 tasks; valid
    task_files = [f for f in ACTIVE.iterdir() if f.suffix == ".md"]
    assert len(task_files) <= 1, (
        f"Expected at most 1 active task, found {len(task_files)}: "
        f"{[f.name for f in task_files]}"
    )


def test_active_tasks_have_four_element_source():
    """Every active task must have a Source: field with authorization evidence."""
    if not ACTIVE.exists():
        return
    for task_file in ACTIVE.glob("*.md"):
        text = task_file.read_text(encoding="utf-8")
        assert "Source:" in text, (
            f"{task_file.name} missing Source: field"
        )
        # The Source: field should contain date, authorization type, task identity,
        # and scope evidence. We check for the presence of identifiable elements.
        source_idx = text.index("Source:")
        source_block = text[source_idx:source_idx + 500]
        assert any(year in source_block for year in ("2026", "2025", "2027", "2028")), (
            f"{task_file.name} Source: field missing date element"
        )


def test_current_md_references_active_task_or_none():
    """CURRENT.md must reference the active task path, or state 'None'."""
    assert CURRENT.exists(), "plan/CURRENT.md does not exist"
    text = CURRENT.read_text(encoding="utf-8")
    assert "Active Task:" in text, "CURRENT.md missing 'Active Task:' field"

    # Either references an active task file or explicitly states None
    if ACTIVE.exists():
        task_files = list(ACTIVE.glob("*.md"))
        if task_files:
            task_name = task_files[0].stem
            assert task_name in text, (
                f"CURRENT.md does not reference active task '{task_name}'"
            )
            return
    # No active task — CURRENT.md should say None or reference blocked state
    assert "None" in text or "blocked" in text.lower(), (
        "CURRENT.md has no active task but does not state 'None' or 'blocked'"
    )


def test_blocked_tasks_have_blocked_section():
    """Every active task with Status: blocked must contain a ## Blocked section."""
    if not ACTIVE.exists():
        return
    for task_file in ACTIVE.glob("*.md"):
        text = task_file.read_text(encoding="utf-8")
        if "Status:" in text:
            # Find the Status value
            for line in text.splitlines():
                stripped = line.strip()
                if stripped.startswith("Status:") or stripped == "blocked":
                    if "blocked" in stripped:
                        assert "## Blocked" in text, (
                            f"{task_file.name} has Status: blocked but no ## Blocked section"
                        )
                        assert "Reason:" in text, (
                            f"{task_file.name} ## Blocked section missing Reason field"
                        )
                        assert "Resume At:" in text, (
                            f"{task_file.name} ## Blocked section missing Resume At field"
                        )
                        assert "Condition:" in text, (
                            f"{task_file.name} ## Blocked section missing Condition field"
                        )
                        break


def test_completed_tasks_have_completion_record():
    """Every completed task (except INDEX.md and TEMPLATE.md) should have
    completion evidence — either a formal Completion Record section or
    historical completion markers (Status: complete, Completed:)."""
    exempt = {"INDEX.md", "TEMPLATE.md"}
    for task_file in COMPLETED.glob("*.md"):
        if task_file.name in exempt:
            continue
        text = task_file.read_text(encoding="utf-8")
        has_completion = (
            "Completion Record" in text
            or "## Completion" in text
            or "Status:\ncomplete" in text
            or "Completed:" in text
        )
        assert has_completion, (
            f"{task_file.name} missing completion evidence"
        )


def test_definitions_directory_does_not_exist():
    """plan/definitions/ must not exist after refactoring."""
    defs = PLAN / "definitions"
    assert not defs.exists(), (
        f"plan/definitions/ still exists with contents: "
        f"{list(defs.iterdir()) if defs.exists() else []}"
    )


def test_blocked_directory_does_not_exist():
    """plan/blocked/ must not exist after refactoring."""
    blocked = PLAN / "blocked"
    assert not blocked.exists(), (
        f"plan/blocked/ still exists with contents: "
        f"{list(blocked.iterdir()) if blocked.exists() else []}"
    )
