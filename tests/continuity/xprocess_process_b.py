#!/usr/bin/env python3
"""
Cross-Process Continuity Experiment — Process B

Starts as a completely independent Python process.
Discovers the experimental Process Instance by scanning the persistence store
and matching the pre-agreed objective marker.
Reconstructs Process Instance and Execution Context.
Attempts continuation.
Emits structured JSON evidence to stdout.

This script is an EXPERIMENT ARTIFACT. It does not modify production code.
"""
from __future__ import annotations

import json
import os
import sys

# Ensure the project root is on the import path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, PROJECT_ROOT)

from runtime.core import ProcessStore, Runtime
from runtime.core.models import ExecutionContext, ProcessInstance
from runtime.persistence.json_store import JsonStore

# ─── Pre-agreed experimental constants ───────────────────────────────────────
PERSISTENCE_STORE = "/tmp/aesm_xprocess_experiment"
OBJECTIVE_MARKER = "AESM_CROSS_PROCESS_CONTINUITY_EXPERIMENT_20260907_xproc7b3e"

PROCESS_A_PID: int | None = None  # Provided via env var for evidence comparison only


def discover_instance_by_marker(store_root: str, marker: str) -> dict:
    """
    Enumerate all persisted Process Instances and find the one whose
    engineering_objective contains the pre-agreed marker.

    Returns a discovery report dict.
    """
    pi_root = os.path.join(store_root, "process-instance")
    discovery = {
        "store_root": store_root,
        "marker": marker,
        "candidates_found": 0,
        "candidates_inspected": [],
        "matched_instance_id": None,
        "discovery_method": "enumerate persisted process-instance directories, "
                            "load process.json, match engineering_objective contains marker",
    }

    if not os.path.isdir(pi_root):
        discovery["error"] = f"process-instance directory does not exist: {pi_root}"
        return discovery

    candidate_dirs = sorted(os.listdir(pi_root))
    discovery["candidates_found"] = len(candidate_dirs)

    for candidate_id in candidate_dirs:
        candidate_dir = os.path.join(pi_root, candidate_id)
        process_json = os.path.join(candidate_dir, "process.json")

        inspection = {"candidate_id": candidate_id, "has_process_json": False, "objective_matched": False}

        if not os.path.isfile(process_json):
            inspection["note"] = "process.json not found"
            discovery["candidates_inspected"].append(inspection)
            continue

        inspection["has_process_json"] = True

        try:
            data = JsonStore(process_json).load()
            objective = data.get("engineering_objective", "")
            inspection["engineering_objective_preview"] = objective[:120]

            if marker in objective:
                inspection["objective_matched"] = True
                discovery["matched_instance_id"] = candidate_id
        except Exception as exc:
            inspection["load_error"] = str(exc)

        discovery["candidates_inspected"].append(inspection)

    return discovery


def main() -> dict:
    """Execute Process B experimental procedure and return evidence dict."""
    evidence: dict = {}

    # Record process identity
    evidence["pid"] = os.getpid()
    evidence["python_executable"] = sys.executable
    evidence["python_version"] = sys.version
    evidence["project_root"] = PROJECT_ROOT

    # Process A PID for comparison (passed via env var for evidence, NOT for instance discovery)
    process_a_pid_str = os.environ.get("XPROCESS_PROCESS_A_PID")
    if process_a_pid_str:
        evidence["process_a_pid_from_env"] = int(process_a_pid_str)
    evidence["process_b_pid"] = os.getpid()

    # Create store and runtime
    store = ProcessStore(PERSISTENCE_STORE)
    runtime_id = "xprocess-runtime-B"
    rt = Runtime(store, runtime_id)

    evidence["runtime_id"] = runtime_id
    evidence["persistence_store"] = PERSISTENCE_STORE
    evidence["objective_marker"] = OBJECTIVE_MARKER

    # ── Phase 1: Discovery ───────────────────────────────────────────────
    discovery = discover_instance_by_marker(PERSISTENCE_STORE, OBJECTIVE_MARKER)
    evidence["discovery"] = discovery

    matched_id = discovery["matched_instance_id"]
    if matched_id is None:
        evidence["result"] = "DISCOVERY_FAILURE"
        evidence["error"] = "No persisted Process Instance matched the objective marker"
        evidence["exit_code"] = 0  # Not a process error, an experimental result
        return evidence

    evidence["discovered_process_instance_id"] = matched_id

    # ── Phase 2: Reconstruction ──────────────────────────────────────────
    reconstruction: dict = {"process_instance": {}, "execution_context": {}}

    try:
        rt.attach(matched_id)
        reconstruction["attach_success"] = True
    except Exception as exc:
        reconstruction["attach_success"] = False
        reconstruction["attach_error"] = str(exc)
        reconstruction["attach_error_type"] = type(exc).__name__
        evidence["reconstruction"] = reconstruction
        evidence["result"] = "RECONSTRUCTION_FAILURE"
        evidence["exit_code"] = 0
        return evidence

    # ── Phase 3: Record recovered state ──────────────────────────────────
    pi = rt.process_instance
    ctx = rt.context

    reconstruction["process_instance"] = {
        "process_instance_id": pi.process_instance_id,
        "engineering_objective": pi.engineering_objective,
        "lifecycle": pi.lifecycle,
        "execution_context_ref": pi.execution_context_ref,
        "epm": pi.epm,
        "pem": pi.pem,
        "created_at": pi.created_at,
        "updated_at": pi.updated_at,
    }

    reconstruction["execution_context"] = {
        "process_instance_id": ctx.process_instance_id,
        "engineering_objective": ctx.engineering_objective,
        "process_state": ctx.process_state,
        "execution_mode": ctx.execution_mode,
        "version": ctx.version,
        "evidence_count": len(ctx.evidence),
        "evidence": ctx.evidence,
        "engineering_decisions_count": len(ctx.engineering_decisions),
        "engineering_decisions": ctx.engineering_decisions,
        "artifacts_count": len(ctx.artifacts),
        "artifacts": ctx.artifacts,
        "pending_execution_count": len(ctx.pending_execution),
        "pending_execution": ctx.pending_execution,
        "unresolved_matters": ctx.unresolved_matters,
        "verification": ctx.verification,
        "engineering_completion": ctx.engineering_completion,
        "updated_at": ctx.updated_at,
    }

    evidence["reconstruction"] = reconstruction

    # ── Phase 4: History recovery ────────────────────────────────────────
    history = store.history(matched_id)
    evidence["recovered_history_entry_count"] = len(history)
    evidence["recovered_history_event_types"] = [e["type"] for e in history]
    evidence["recovered_history"] = history

    # Check for Process A runtime_id in history
    process_a_runtime_entries = [
        e for e in history if e.get("runtime_id") == "xprocess-runtime-A"
    ]
    evidence["history_contains_process_a_runtime"] = len(process_a_runtime_entries) > 0
    evidence["process_a_runtime_history_count"] = len(process_a_runtime_entries)

    # ── Phase 5: Continuity checks ───────────────────────────────────────
    continuity: dict = {}

    # Identity
    continuity["identity_match"] = (
        pi.process_instance_id == matched_id
        and ctx.process_instance_id == matched_id
    )

    # Runtime boundary
    continuity["runtime_ids_distinct"] = (runtime_id != "xprocess-runtime-A")

    # Objective preserved
    continuity["objective_contains_marker"] = OBJECTIVE_MARKER in ctx.engineering_objective

    # State analysis
    continuity["recovered_process_state"] = ctx.process_state
    continuity["recovered_lifecycle"] = pi.lifecycle

    # Pending execution analysis
    if ctx.pending_execution:
        pending = ctx.pending_execution[0]
        continuity["pending_execution_present"] = True
        continuity["pending_next_action"] = pending.get("next_action")
        continuity["pending_resumption_conditions"] = pending.get("resumption_conditions")
        continuity["pending_status"] = pending.get("status")
    else:
        continuity["pending_execution_present"] = False

    evidence["continuity"] = continuity

    # ── Phase 6: Continuation attempt ────────────────────────────────────
    continuation: dict = {}

    # Determine next legitimate action
    # The recovered state is "implementation" with pending_execution and artifacts.
    # The normal next lifecycle transition from implementation would be:
    #   begin_verification() — but this requires pending_execution == empty
    # OR:
    #   continue setting pending execution / recording artifacts

    continuation["current_state"] = ctx.process_state
    continuation["has_pending_execution"] = bool(ctx.pending_execution)
    continuation["has_artifacts"] = bool(ctx.artifacts)

    if ctx.process_state == "implementation":
        if ctx.pending_execution:
            continuation["next_legitimate_action"] = "begin_verification"
            continuation["guard_analysis"] = (
                "begin_verification() requires pending_execution == empty, "
                "but recovered state has pending_execution entries"
            )

            # Attempt the action to observe the guard
            try:
                rt.begin_verification()
                continuation["begin_verification_result"] = "SUCCESS"
            except RuntimeError as exc:
                continuation["begin_verification_result"] = "BLOCKED_BY_GUARD"
                continuation["guard_message"] = str(exc)
                continuation["guard_type"] = type(exc).__name__

            # Try an alternative legitimate action: record another observation
            # This is valid during implementation and demonstrates runtime operability
            try:
                rt.observe({
                    "source": "process_b_continuation",
                    "fact": "Process B successfully recovered and can operate on the Process Instance",
                    "runtime_id": runtime_id,
                })
                continuation["alternative_action"] = "observe"
                continuation["alternative_result"] = "SUCCESS"
                continuation["post_continuation_version"] = ctx.version
            except Exception as exc:
                continuation["alternative_action"] = "observe"
                continuation["alternative_result"] = "FAILED"
                continuation["alternative_error"] = str(exc)
        else:
            # No pending execution — try begin_verification directly
            continuation["next_legitimate_action"] = "begin_verification"
            try:
                rt.begin_verification()
                continuation["begin_verification_result"] = "SUCCESS"
            except RuntimeError as exc:
                continuation["begin_verification_result"] = "BLOCKED_BY_GUARD"
                continuation["guard_message"] = str(exc)
    else:
        continuation["note"] = f"Unexpected recovered state: {ctx.process_state}"

    evidence["continuation"] = continuation

    # ── Phase 7: Post-continuation history ───────────────────────────────
    post_history = store.history(matched_id)
    evidence["post_continuation_history_count"] = len(post_history)
    evidence["post_continuation_history_types"] = [e["type"] for e in post_history]

    # Check Process B runtime_id in history
    process_b_history_entries = [
        e for e in post_history if e.get("runtime_id") == runtime_id
    ]
    evidence["history_contains_process_b_runtime"] = len(process_b_history_entries) > 0
    evidence["process_b_runtime_history_count"] = len(process_b_history_entries)

    # Final post-continuation state
    evidence["post_continuation_version"] = ctx.version
    evidence["post_continuation_evidence_count"] = len(ctx.evidence)

    # ── Lifecycle vs process_state observation ───────────────────────────
    evidence["lifecycle_process_state_observation"] = {
        "process_instance_lifecycle": pi.lifecycle,
        "execution_context_process_state": ctx.process_state,
        "note": "Recording both values as observed without interpretation",
    }

    evidence["result"] = "EVIDENCE_COLLECTED"
    evidence["exit_code"] = 0

    rt.stop()
    return evidence


if __name__ == "__main__":
    try:
        result = main()
        print(json.dumps(result, indent=2, ensure_ascii=False))
        sys.exit(0)
    except Exception as exc:
        error_evidence = {
            "pid": os.getpid(),
            "error": str(exc),
            "error_type": type(exc).__name__,
            "exit_code": 1,
        }
        print(json.dumps(error_evidence, indent=2, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)
