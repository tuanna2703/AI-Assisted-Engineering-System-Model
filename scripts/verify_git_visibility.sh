#!/usr/bin/env bash
# AESM Git Visibility Verification
# Verifies that repository-local .aesm PI files are Git-trackable in the DBP repository.
set -euo pipefail

PI_ID="d0640ec8-672e-43bd-bd4b-974d808915a2"
DBP_REPO="/Volumes/DATA/Workspace/Development/MAMP/htdocs/directories-builder-pro"

echo "======================================================================"
echo "AESM Git Visibility Verification"
echo "Repository: ${DBP_REPO}"
echo "PI-ID     : ${PI_ID}"
echo "======================================================================"

cd "${DBP_REPO}"

echo ""
echo "--- git check-ignore (exit 0 = IGNORED, exit 1 = NOT IGNORED = trackable) ---"
for FILE in "process.json" "context.json" "history.jsonl" "migration_integrity_record.json"; do
    TARGET=".aesm/${PI_ID}/${FILE}"
    if git check-ignore -v "${TARGET}" 2>/dev/null; then
        echo "  IGNORED: ${TARGET}"
    else
        echo "  TRACKABLE (not ignored): ${TARGET}"
    fi
done

echo ""
echo "--- git status --short .aesm/ ---"
git status --short .aesm/ || echo "  (no output)"

echo ""
echo "--- git ls-files .aesm/ ---"
git ls-files .aesm/ || echo "  (no tracked files in .aesm/ yet)"

echo ""
echo "--- DBP .gitignore contents ---"
if [ -f ".gitignore" ]; then
    cat .gitignore
else
    echo "  (no .gitignore found)"
fi

echo ""
echo "======================================================================"
echo "Verification complete."
echo "======================================================================"
