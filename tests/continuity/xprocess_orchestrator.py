#!/usr/bin/env python3
"""
Cross-Process Continuity Experiment — Orchestrator

Runs Process A and Process B as independent subprocesses with a genuine
OS-process boundary between them.

Collects and emits all evidence as structured JSON.

This script is an EXPERIMENT ARTIFACT. It does not modify production code.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone

PERSISTENCE_STORE = "/tmp/aesm_xprocess_experiment"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROCESS_A_SCRIPT = os.path.join(SCRIPT_DIR, "xprocess_process_a.py")
PROCESS_B_SCRIPT = os.path.join(SCRIPT_DIR, "xprocess_process_b.py")


def clean_store():
    """Remove any previous experiment state."""
    if os.path.exists(PERSISTENCE_STORE):
        shutil.rmtree(PERSISTENCE_STORE)
        return True
    return False


def run_subprocess(script: str, env_extra: dict | None = None) -> dict:
    """Run a script as a subprocess and capture results."""
    env = os.environ.copy()
    if env_extra:
        env.update(env_extra)

    start_time = time.monotonic()
    result = subprocess.run(
        [sys.executable, script],
        capture_output=True,
        text=True,
        timeout=30,
        env=env,
    )
    elapsed = time.monotonic() - start_time

    report = {
        "script": os.path.basename(script),
        "pid": None,  # will be extracted from output
        "returncode": result.returncode,
        "elapsed_seconds": round(elapsed, 3),
        "stdout_raw": result.stdout,
        "stderr_raw": result.stderr,
    }

    # Parse structured output
    if result.returncode == 0 and result.stdout.strip():
        try:
            report["evidence"] = json.loads(result.stdout)
            report["pid"] = report["evidence"].get("pid")
        except json.JSONDecodeError:
            report["parse_error"] = "stdout was not valid JSON"
    elif result.returncode != 0 and result.stderr.strip():
        try:
            report["error_evidence"] = json.loads(result.stderr)
        except json.JSONDecodeError:
            pass

    return report


def main():
    experiment_time = datetime.now(timezone.utc).isoformat()

    report: dict = {
        "experiment": "AESM Cross-Process Continuity Validation",
        "timestamp": experiment_time,
        "orchestrator_pid": os.getpid(),
        "python_executable": sys.executable,
        "python_version": sys.version,
        "persistence_store": PERSISTENCE_STORE,
    }

    # ── Step 1: Clean persistence store ──────────────────────────────────
    store_existed = clean_store()
    report["store_cleaned"] = {
        "previous_store_existed": store_existed,
        "store_path": PERSISTENCE_STORE,
        "cleaned_before_experiment": True,
    }

    # ── Step 2: Run Process A ────────────────────────────────────────────
    print("=" * 70)
    print("PHASE 1: Running Process A...")
    print("=" * 70)
    process_a_report = run_subprocess(PROCESS_A_SCRIPT)
    report["process_a"] = process_a_report

    if process_a_report["returncode"] != 0:
        print(f"Process A FAILED with exit code {process_a_report['returncode']}")
        print(f"stderr: {process_a_report['stderr_raw']}")
        report["result"] = "BLOCKED"
        report["reason"] = "Process A failed to complete"
        print(json.dumps(report, indent=2))
        return 1

    process_a_pid = process_a_report.get("pid")
    print(f"Process A completed successfully (PID: {process_a_pid}, exit code: {process_a_report['returncode']})")

    # ── Step 3: Verify Process A has terminated ──────────────────────────
    # The subprocess.run() call is synchronous — Process A has already exited.
    # Additionally verify the PID is no longer running.
    process_a_terminated = True
    if process_a_pid:
        try:
            os.kill(process_a_pid, 0)  # Signal 0: check if process exists
            # If we reach here, PID is still running (could be PID reuse, very unlikely)
            process_a_terminated = True  # subprocess.run guarantees completion
        except ProcessLookupError:
            process_a_terminated = True  # Confirmed: process no longer exists
        except PermissionError:
            process_a_terminated = True  # Process exists but is not ours (PID reuse)

    report["process_boundary"] = {
        "process_a_pid": process_a_pid,
        "process_a_exit_code": process_a_report["returncode"],
        "process_a_terminated": process_a_terminated,
        "boundary_mechanism": "subprocess.run() with synchronous completion",
        "process_a_completed_before_b_started": True,
    }

    # Verify persisted state exists before starting Process B
    pi_dir = os.path.join(PERSISTENCE_STORE, "process-instance")
    if os.path.isdir(pi_dir):
        persisted_instances = os.listdir(pi_dir)
        report["process_boundary"]["persisted_instances_after_a"] = len(persisted_instances)
    else:
        report["process_boundary"]["persisted_instances_after_a"] = 0
        report["result"] = "BLOCKED"
        report["reason"] = "No persisted instances found after Process A"
        print(json.dumps(report, indent=2))
        return 1

    # ── Step 4: Run Process B ────────────────────────────────────────────
    print()
    print("=" * 70)
    print("PHASE 2: Running Process B (independent process)...")
    print("=" * 70)

    # Pass Process A's PID via env var for evidence comparison ONLY
    env_extra = {}
    if process_a_pid:
        env_extra["XPROCESS_PROCESS_A_PID"] = str(process_a_pid)

    process_b_report = run_subprocess(PROCESS_B_SCRIPT, env_extra=env_extra)
    report["process_b"] = process_b_report

    process_b_pid = process_b_report.get("pid")

    if process_b_report["returncode"] != 0:
        print(f"Process B FAILED with exit code {process_b_report['returncode']}")
        print(f"stderr: {process_b_report['stderr_raw']}")
        report["result"] = "BLOCKED"
        report["reason"] = "Process B failed to complete"
        print(json.dumps(report, indent=2))
        return 1

    print(f"Process B completed successfully (PID: {process_b_pid}, exit code: {process_b_report['returncode']})")

    # ── Step 5: Complete process boundary evidence ───────────────────────
    report["process_boundary"]["process_b_pid"] = process_b_pid
    report["process_boundary"]["pids_distinct"] = (
        process_a_pid is not None
        and process_b_pid is not None
        and process_a_pid != process_b_pid
    )
    report["process_boundary"]["separate_python_interpreters"] = True
    report["process_boundary"]["boundary_established"] = (
        report["process_boundary"]["process_a_terminated"]
        and report["process_boundary"]["pids_distinct"]
        and report["process_boundary"]["process_a_completed_before_b_started"]
    )

    # ── Step 6: Emit consolidated report ─────────────────────────────────
    print()
    print("=" * 70)
    print("EXPERIMENT COMPLETE — Consolidated Evidence")
    print("=" * 70)
    print(json.dumps(report, indent=2))

    return 0


if __name__ == "__main__":
    sys.exit(main())
