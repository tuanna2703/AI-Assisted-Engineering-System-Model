#!/usr/bin/env python3
"""Migrate existing DBP Process Instance from workspace-level .aesm-process-store
to repository-local directories-builder-pro/.aesm directory.

Migration contract:
- Storage relocation ONLY.
- No new PI created.
- PI identity, version, history, lifecycle, evidence, decisions, artifacts: unchanged.
- SHA-256 hashes verified before and after copy.
- Migration is a COPY, not a move. The original files are preserved.

Usage:
    python scripts/migrate_pi_to_repo_local.py

Output:
    directories-builder-pro/.aesm/<PI-ID>/migration_integrity_record.json
"""
from __future__ import annotations

import hashlib
import json
import shutil
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

WORKSPACE_ROOT = Path("/Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins")
DBP_REPO_ROOT = Path("/Volumes/DATA/Workspace/Development/MAMP/htdocs/directories-builder-pro")
PI_ID = "d0640ec8-672e-43bd-bd4b-974d808915a2"

OLD_PI_DIR = WORKSPACE_ROOT / ".aesm-process-store" / "process-instance" / PI_ID
NEW_AESM_ROOT = DBP_REPO_ROOT / ".aesm"
NEW_PI_DIR = NEW_AESM_ROOT / PI_ID

FILES = ["process.json", "context.json", "history.jsonl"]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def is_parseable_json(path: Path) -> bool:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return isinstance(data, dict)
    except Exception:
        return False


def is_parseable_jsonl(path: Path) -> bool:
    try:
        lines = [l for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]
        for line in lines:
            json.loads(line)
        return True
    except Exception:
        return False


def jsonl_line_count(path: Path) -> int:
    return len([l for l in path.read_text(encoding="utf-8").splitlines() if l.strip()])


# ---------------------------------------------------------------------------
# Pre-flight validation
# ---------------------------------------------------------------------------

def validate_source() -> None:
    print(f"[PRE-FLIGHT] Validating source PI directory: {OLD_PI_DIR}")
    if not OLD_PI_DIR.exists():
        print(f"  ERROR: source PI directory does not exist: {OLD_PI_DIR}", file=sys.stderr)
        sys.exit(1)
    for fname in FILES:
        p = OLD_PI_DIR / fname
        if not p.exists():
            print(f"  ERROR: source file missing: {p}", file=sys.stderr)
            sys.exit(1)
    if not DBP_REPO_ROOT.exists() or not DBP_REPO_ROOT.is_dir():
        print(f"  ERROR: DBP repository root does not exist: {DBP_REPO_ROOT}", file=sys.stderr)
        sys.exit(1)
    print("  OK: all source files present, DBP repository root exists.")


# ---------------------------------------------------------------------------
# Build BEFORE record
# ---------------------------------------------------------------------------

def build_before_record() -> dict:
    print("[BEFORE] Computing SHA-256 hashes and metadata...")
    record: dict = {}

    for fname in FILES:
        p = OLD_PI_DIR / fname
        entry: dict = {
            "path": str(p),
            "sha256": sha256(p),
            "size_bytes": p.stat().st_size,
        }
        if fname.endswith(".json"):
            entry["parseable"] = is_parseable_json(p)
            data = json.loads(p.read_text(encoding="utf-8"))
            if fname == "process.json":
                entry["pi_id"] = data.get("process_instance_id", "MISSING")
                entry["lifecycle"] = data.get("lifecycle", "MISSING")
                entry["engineering_scope_resolution"] = data.get("engineering_scope_resolution", "MISSING")
                entry["engineering_scope_identity"] = data.get("engineering_scope_identity")
            elif fname == "context.json":
                entry["process_instance_id"] = data.get("process_instance_id", "MISSING")
                entry["version"] = data.get("version", "MISSING")
                entry["process_state"] = data.get("process_state", "MISSING")
        elif fname.endswith(".jsonl"):
            entry["parseable"] = is_parseable_jsonl(p)
            entry["line_count"] = jsonl_line_count(p)

        record[fname] = entry
        print(f"  {fname}: sha256={entry['sha256'][:16]}...  size={entry['size_bytes']} bytes")

    return record


# ---------------------------------------------------------------------------
# Copy files
# ---------------------------------------------------------------------------

def copy_files() -> None:
    print(f"[COPY] Creating destination: {NEW_PI_DIR}")
    NEW_PI_DIR.mkdir(parents=True, exist_ok=True)
    for fname in FILES:
        src = OLD_PI_DIR / fname
        dst = NEW_PI_DIR / fname
        shutil.copy2(src, dst)
        print(f"  Copied: {src.name} → {dst}")


# ---------------------------------------------------------------------------
# Build AFTER record
# ---------------------------------------------------------------------------

def build_after_record() -> dict:
    print("[AFTER] Computing SHA-256 hashes and metadata...")
    record: dict = {}

    for fname in FILES:
        p = NEW_PI_DIR / fname
        entry: dict = {
            "path": str(p),
            "sha256": sha256(p),
            "size_bytes": p.stat().st_size,
        }
        if fname.endswith(".json"):
            entry["parseable"] = is_parseable_json(p)
            data = json.loads(p.read_text(encoding="utf-8"))
            if fname == "process.json":
                entry["pi_id"] = data.get("process_instance_id", "MISSING")
                entry["lifecycle"] = data.get("lifecycle", "MISSING")
                entry["engineering_scope_resolution"] = data.get("engineering_scope_resolution", "MISSING")
                entry["engineering_scope_identity"] = data.get("engineering_scope_identity")
            elif fname == "context.json":
                entry["process_instance_id"] = data.get("process_instance_id", "MISSING")
                entry["version"] = data.get("version", "MISSING")
                entry["process_state"] = data.get("process_state", "MISSING")
        elif fname.endswith(".jsonl"):
            entry["parseable"] = is_parseable_jsonl(p)
            entry["line_count"] = jsonl_line_count(p)

        record[fname] = entry
        print(f"  {fname}: sha256={entry['sha256'][:16]}...  size={entry['size_bytes']} bytes")

    return record


# ---------------------------------------------------------------------------
# Verify integrity
# ---------------------------------------------------------------------------

def verify_integrity(before: dict, after: dict) -> bool:
    print("[VERIFY] Comparing before/after SHA-256 hashes...")
    all_pass = True
    for fname in FILES:
        b_hash = before[fname]["sha256"]
        a_hash = after[fname]["sha256"]
        b_size = before[fname]["size_bytes"]
        a_size = after[fname]["size_bytes"]
        match = b_hash == a_hash and b_size == a_size
        status = "PASS" if match else "FAIL"
        print(f"  {fname}: {status}  (before={b_hash[:16]}...  after={a_hash[:16]}...)")
        if not match:
            all_pass = False
    return all_pass


# ---------------------------------------------------------------------------
# Write integrity record
# ---------------------------------------------------------------------------

def write_integrity_record(before: dict, after: dict, integrity: str) -> Path:
    from datetime import datetime, timezone
    record = {
        "migration_type": "storage_relocation_only",
        "pi_id": PI_ID,
        "migration_timestamp": datetime.now(timezone.utc).isoformat(),
        "source_root": str(WORKSPACE_ROOT / ".aesm-process-store"),
        "destination_root": str(NEW_AESM_ROOT),
        "pi_identity_preserved": True,
        "version_preserved": True,
        "history_preserved": True,
        "lifecycle_preserved": True,
        "new_pi_created": False,
        "files": {},
        "integrity": integrity,
    }

    for fname in FILES:
        record["files"][fname] = {
            "before": before[fname],
            "after": after[fname],
            "hash_match": before[fname]["sha256"] == after[fname]["sha256"],
        }
        if fname == "context.json":
            record["files"][fname]["version"] = before[fname].get("version")
            record["files"][fname]["process_state"] = before[fname].get("process_state")
        if fname == "history.jsonl":
            record["files"][fname]["line_count"] = before[fname].get("line_count")

    output_path = NEW_PI_DIR / "migration_integrity_record.json"
    output_path.write_text(
        json.dumps(record, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"[RECORD] Migration integrity record written: {output_path}")
    return output_path


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 70)
    print("AESM Process Instance Migration")
    print(f"PI-ID : {PI_ID}")
    print(f"FROM  : {OLD_PI_DIR}")
    print(f"TO    : {NEW_PI_DIR}")
    print("=" * 70)

    validate_source()
    before = build_before_record()
    copy_files()
    after = build_after_record()
    passed = verify_integrity(before, after)
    integrity = "PASS" if passed else "FAIL"
    record_path = write_integrity_record(before, after, integrity)

    print("=" * 70)
    if passed:
        print(f"[RESULT] integrity={integrity}  Migration complete.")
        print(f"[RESULT] Integrity record: {record_path}")
        print("[RESULT] Source files are PRESERVED (migration was a copy, not a move).")
    else:
        print(f"[RESULT] integrity={integrity}  SHA-256 MISMATCH — migration failed.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
