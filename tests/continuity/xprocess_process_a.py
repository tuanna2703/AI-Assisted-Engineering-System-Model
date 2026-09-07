#!/usr/bin/env python3
"""
Cross-Process Continuity Experiment — Process A

Creates a meaningful Process Instance, advances engineering state through
investigation into implementation, persists all state, emits structured
JSON evidence to stdout, then exits.

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

# ─── Pre-agreed experimental constants ───────────────────────────────────────
PERSISTENCE_STORE = "/tmp/aesm_xprocess_experiment"
OBJECTIVE_MARKER = "AESM_CROSS_PROCESS_CONTINUITY_EXPERIMENT_20260907_xproc7b3e"

ENGINEERING_OBJECTIVE = (
    f"[{OBJECTIVE_MARKER}] Implement cross-process state recovery validation "
    f"for AESM Process Instance lifecycle continuity"
)

DECISION_RECOGNITION = {
    "recognized": True,
    "basis": "engineering investigation completed; applicable decision gate satisfied",
}


def main() -> dict:
    """Execute Process A experimental procedure and return evidence dict."""
    evidence: dict = {}

    # Record process identity
    evidence["pid"] = os.getpid()
    evidence["python_executable"] = sys.executable
    evidence["python_version"] = sys.version
    evidence["project_root"] = PROJECT_ROOT

    # Create store and runtime
    store = ProcessStore(PERSISTENCE_STORE)
    runtime_id = "xprocess-runtime-A"
    rt = Runtime(store, runtime_id)

    evidence["runtime_id"] = runtime_id
    evidence["persistence_store"] = PERSISTENCE_STORE
    evidence["objective_marker"] = OBJECTIVE_MARKER

    # ── Create Process Instance ──────────────────────────────────────────
    process_instance_id = rt.create_process(ENGINEERING_OBJECTIVE)

    evidence["process_instance_id"] = process_instance_id
    evidence["engineering_objective"] = ENGINEERING_OBJECTIVE
    evidence["initial_lifecycle"] = rt.process_instance.lifecycle
    evidence["initial_process_state"] = rt.context.process_state
    evidence["initial_context_version"] = rt.context.version

    # ── Advance to Investigation ─────────────────────────────────────────
    rt.start_investigation()
    evidence["after_start_investigation_state"] = rt.context.process_state

    # ── Record observations ──────────────────────────────────────────────
    observation_1 = {
        "source": "experimental_probe",
        "fact": "cross-process persistence boundary is testable",
        "detail": "JSON persistence store supports independent process access",
    }
    observation_2 = {
        "source": "experimental_probe",
        "fact": "process instance discovery is possible via objective marker",
        "detail": "persisted process.json contains engineering_objective field",
    }
    rt.observe(observation_1)
    rt.observe(observation_2)
    evidence["observations_recorded"] = 2

    # ── Recognize an engineering decision ─────────────────────────────────
    decision = {
        "id": "XPROC-D1",
        "conclusion": "use filesystem persistence store for cross-process handoff",
        "rationale": "JSON store provides durable state accessible to independent processes",
    }
    rt.recognize_decision(decision, DECISION_RECOGNITION)
    evidence["decision_recorded"] = decision["id"]

    # ── Advance to Implementation ────────────────────────────────────────
    rt.begin_implementation()
    evidence["after_begin_implementation_state"] = rt.context.process_state

    # ── Record implementation artifact ───────────────────────────────────
    artifact = {
        "id": "XPROC-A1",
        "type": "experiment_script",
        "path": "tests/continuity/xprocess_process_a.py",
        "description": "Process A experiment script for cross-process continuity validation",
    }
    rt.record_artifact(artifact)
    evidence["artifact_recorded"] = artifact["id"]

    # ── Set pending execution (resumable work for Process B) ─────────────
    pending_work = {
        "id": "XPROC-W1",
        "status": "pending",
        "description": "cross-process recovery and continuation verification",
        "next_action": "discover persisted instance and verify state continuity",
        "resumption_conditions": [
            "Process A has terminated",
            "persistence store contains valid state",
            "Process B discovers instance by objective marker",
        ],
    }
    rt.set_pending_execution(pending_work)
    evidence["pending_execution_set"] = pending_work["id"]

    # ── Capture final state ──────────────────────────────────────────────
    evidence["final_process_state"] = rt.context.process_state
    evidence["final_context_version"] = rt.context.version
    evidence["final_lifecycle"] = rt.process_instance.lifecycle
    evidence["final_evidence_count"] = len(rt.context.evidence)
    evidence["final_decisions_count"] = len(rt.context.engineering_decisions)
    evidence["final_artifacts_count"] = len(rt.context.artifacts)
    evidence["final_pending_execution_count"] = len(rt.context.pending_execution)

    # ── Capture persisted files ──────────────────────────────────────────
    instance_dir = os.path.join(
        PERSISTENCE_STORE, "process-instance", process_instance_id
    )
    persisted_files = []
    if os.path.isdir(instance_dir):
        for fname in sorted(os.listdir(instance_dir)):
            fpath = os.path.join(instance_dir, fname)
            persisted_files.append(
                {"name": fname, "size_bytes": os.path.getsize(fpath)}
            )
    evidence["persisted_files"] = persisted_files

    # ── Capture history ──────────────────────────────────────────────────
    history = store.history(process_instance_id)
    evidence["history_entry_count"] = len(history)
    evidence["history_event_types"] = [e["type"] for e in history]
    evidence["history"] = history

    # ── Stop runtime (detach without destroying persisted state) ──────────
    rt.stop()

    evidence["exit_code"] = 0

    return evidence


if __name__ == "__main__":
    try:
        result = main()
        # Emit structured evidence to stdout as a single JSON object
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
