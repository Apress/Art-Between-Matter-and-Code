#!/usr/bin/env bash
# ============================================================
# run_parametric_space.sh  —  macOS / Linux launcher
# Art Between Matter and Code · Gianpiero Moioli · Apress 2025
# Runs parametric_space.py in Blender 5.x (or any available version)
# Usage: chmod +x run_parametric_space.sh && ./run_parametric_space.sh
# ============================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/parametric_space.py"

BLENDER_CANDIDATES=(
    "/Applications/Blender.app/Contents/MacOS/Blender"
    "/Applications/Blender 5.1.app/Contents/MacOS/Blender"
    "/Applications/Blender 5.0.app/Contents/MacOS/Blender"
    "/Applications/Blender 4.4.app/Contents/MacOS/Blender"
    "/Applications/Blender 4.3.app/Contents/MacOS/Blender"
    "/Applications/Blender 4.2.app/Contents/MacOS/Blender"
    "/usr/bin/blender"
    "/usr/local/bin/blender"
    "/snap/bin/blender"
    "/opt/blender/blender"
    "$HOME/.local/bin/blender"
    "/var/lib/flatpak/exports/bin/org.blender.Blender"
    "$HOME/.local/share/flatpak/exports/bin/org.blender.Blender"
)

BLENDER_BIN=""
for candidate in "${BLENDER_CANDIDATES[@]}"; do
    if [ -x "$candidate" ]; then
        BLENDER_BIN="$candidate"
        break
    fi
done

if [ -z "$BLENDER_BIN" ] && command -v blender &>/dev/null; then
    BLENDER_BIN="$(command -v blender)"
fi

if [ -z "$BLENDER_BIN" ]; then
    echo "ERROR: Blender not found."
    echo "Please install Blender from https://www.blender.org/download/"
    echo "or set: export BLENDER_BIN=/path/to/blender && ./run_parametric_space.sh"
    exit 1
fi

echo "Using Blender: $BLENDER_BIN"
echo "Running: parametric_space.py"
echo "--------------------------------------------"

"$BLENDER_BIN" --python "$PYTHON_SCRIPT"
