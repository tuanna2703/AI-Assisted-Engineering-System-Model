from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BOUNDARY = ROOT / "plan" / "definitions" / "PLAN-EXECUTION-BOUNDARY.md"
TASK = ROOT / "plan" / "active" / "plan-execution-boundary-governance-resolution.md"

def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")

def test_boundary_definition_contains_required_authority_rules():
    text = read(BOUNDARY)
    required = [
        "## Authority Model",
        "## Authorized Scope",
        "## Mechanical Scope Decision",
        "## Bounded Acceptance Investigation",
        "## Finding Dispositions",
        "## Execution Stop Report",
        "## Blocked Recovery",
        "## Plan Mutation Authority",
        "## Change Inventory",
        "## Completion and Non-Proliferation",
        "## Evidence Separation",
        "## Fresh-Agent Requirement",
        "## DBP Validation Rule",
    ]
    for section in required:
        assert section in text, section

def test_scope_decision_is_ordered_and_non_inferential():
    text = read(BOUNDARY)
    assert "1. **Explicit coverage:**" in text
    assert "2. **Acceptance investigation:**" in text
    assert "3. **Stop:**" in text
    assert "semantic relatedness" in text
    assert "usefulness" in text

def test_finding_lifecycle_separates_observation_candidate_and_authorized_work():
    text = read(BOUNDARY)
    for term in ("Observation/Discovery", "Finding", "Work Candidate", "Authorized Work"):
        assert term in text
    assert "Only explicit planning authorization creates executable work." in text

def test_all_five_finding_dispositions_are_defined():
    text = read(BOUNDARY)
    for disposition in (
        "`IN_SCOPE`",
        "`ACCEPTANCE_INVESTIGATION`",
        "`FUTURE_WORK_CANDIDATE`",
        "`BLOCKING_FINDING`",
        "`IRRELEVANT_OBSERVATION`",
    ):
        assert disposition in text

def test_execution_stop_report_contains_recovery_identity():
    text = read(BOUNDARY)
    for field in (
        "Task:",
        "Work Unit:",
        "Subtask:",
        "Authorization:",
        "Observed Condition:",
        "Scope Determination:",
        "Mutation Already Performed:",
        "Current Persisted Planning State:",
        "Required Human / Planning Decision:",
        "Resume Point:",
    ):
        assert field in text

def test_boundary_preserves_existing_blocked_lifecycle():
    text = read(BOUNDARY)
    assert "Do not create a parallel stop status." in text
    assert "Resolution of the blocker does not authorize new work." in text
    assert "Reactivation requires the existing explicit Reactivation Record" in text

def test_completion_is_acceptance_based():
    text = read(BOUNDARY)
    assert "No additional issues were discovered." in text
    assert "future-work candidate may remain recorded" in text

def test_task_is_mechanically_authorized_and_has_semantic_work_units():
    text = read(TASK)
    for field in (
        "Task ID:",
        "Status:",
        "Created:",
        "Source:",
        "Authorized by:",
        "Authorized Task:",
        "Authorized scope:",
        "## Objective",
        "## Governing Constraints",
        "## Work Units",
        "## Acceptance Criteria",
        "## Completion Record",
    ):
        assert field in text
    assert "### Establish Boundary Baseline" in text
    assert "### Define Boundary Model and Change Inventory" in text
    assert "### Implement Governance Boundary" in text
    assert "### Verify Boundary Behavior" in text
    assert "### Fresh-Agent and DBP Boundary Validation" in text
    assert "Phase 1" not in text
    assert "Phase 2" not in text

def test_canonical_scenarios_are_persisted():
    text = read(TASK)
    for scenario in (
        "Explicitly authorized work",
        "Acceptance uncertainty",
        "Unrelated defect",
        "Unauthorized required implementation",
        "Resolved blocker",
        "Explicit reactivation",
        "Future improvement after acceptance",
    ):
        assert scenario in text
