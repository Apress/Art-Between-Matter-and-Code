#!/usr/bin/env bash
# ============================================================
# run_aura_transition.sh  —  macOS / Linux launcher
# Art Between Matter and Code · Gianpiero Moioli · Apress 2025
# Runs aura_transition.py — generates the aura/reproducibility
# diagram as SVG and opens it in the default browser.
# Pure Python, no external libraries required.
# Usage: chmod +x run_aura_transition.sh && ./run_aura_transition.sh
# ============================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/aura_transition.py"

# ── Search order for Python ───────────────────────────────────
PYTHON_BIN=""

# 1. Try python3 in PATH
if command -v python3 &>/dev/null; then
    PYTHON_BIN="$(command -v python3)"
fi

# 2. Try python in PATH (some systems)
if [ -z "$PYTHON_BIN" ] && command -v python &>/dev/null; then
    PYTHON_BIN="$(command -v python)"
fi

# 3. Try Blender's bundled Python as fallback
BLENDER_PYTHON_CANDIDATES=(
    "/Applications/Blender.app/Contents/Resources/4.4/python/bin/python3.11"
    "/Applications/Blender.app/Contents/Resources/4.3/python/bin/python3.11"
    "/Applications/Blender 5.1.app/Contents/Resources/5.1/python/bin/python3.11"
    "/Applications/Blender 5.0.app/Contents/Resources/5.0/python/bin/python3.11"
)

if [ -z "$PYTHON_BIN" ]; then
    for candidate in "${BLENDER_PYTHON_CANDIDATES[@]}"; do
        if [ -x "$candidate" ]; then
            PYTHON_BIN="$candidate"
            break
        fi
    done
fi

if [ -z "$PYTHON_BIN" ]; then
    echo "ERROR: Python 3 not found."
    echo "Install Python from https://www.python.org/downloads/"
    echo "or install Blender (its bundled Python will be used as fallback)."
    exit 1
fi

echo "Using Python: $PYTHON_BIN"
echo "Running: aura_transition.py"
echo "--------------------------------------------"

"$PYTHON_BIN" "$PYTHON_SCRIPT"
