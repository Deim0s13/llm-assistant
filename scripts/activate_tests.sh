#!/usr/bin/env bash
# scripts/activate_tests.sh
#
# 1. Prep PYTHONPATH so project modules are importable.
# 2. Run all memory-integration tests in one shot.
#    (Fails fast on the first error.)

set -e  # abort on any failure

# ─────────────────────────── PYTHONPATH ────────────────────────────
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null)"
export PYTHONPATH="$REPO_ROOT${PYTHONPATH:+:$PYTHONPATH}"
echo "PYTHONPATH set → $PYTHONPATH"

# ───────────────────────────── Tests ───────────────────────────────
cd "$REPO_ROOT"

echo "▶ Running memory-integration tests..."
python experiments/test_memory_on.py
python experiments/test_memory_off.py
python experiments/test_memory_toggle.py

echo "✔ All memory tests completed successfully"
