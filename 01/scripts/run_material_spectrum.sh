#!/usr/bin/env bash
# ============================================================
# run_material_spectrum.sh  —  macOS / Linux launcher
# Art Between Matter and Code · Gianpiero Moioli · Apress 2025
# Runs material_spectrum.py in Blender 5.x (or any available version)
#
# Five material states in a row: marble → terracotta → bronze →
# digital glass → wireframe. Maps the material-digital continuum.
#
# Usage: chmod +x run_material_spectrum.sh && ./run_material_spectrum.sh
# ============================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/material_spectrum.py"

# ── Search order for Blender ──────────────────────────────────
BLENDER_CANDIDATES=(
    # macOS — standard install
    "/Applications/Blender.app/Contents/MacOS/Blender"
    # macOS — versioned installs
    "/Applications/Blender 5.1.app/Contents/MacOS/Blender"
    "/Applications/Blender 5.0.app/Contents/MacOS/Blender"
    "/Applications/Blender 4.4.app/Contents/MacOS/Blender"
    "/Applications/Blender 4.3.app/Contents/MacOS/Blender"
    "/Applications/Blender 4.2.app/Contents/MacOS/Blender"
    # Linux — common paths
    "/usr/bin/blender"
    "/usr/local/bin/blender"
    "/snap/bin/blender"
    "/opt/blender/blender"
    "$HOME/.local/bin/blender"
    # Flatpak
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

# Fallback: check PATH
if [ -z "$BLENDER_BIN" ] && command -v blender &>/dev/null; then
    BLENDER_BIN="$(command -v blender)"
fi

if [ -z "$BLENDER_BIN" ]; then
    echo "ERROR: Blender not found."
    echo "Please install Blender from https://www.blender.org/download/"
    echo "or set the BLENDER_BIN environment variable:"
    echo "  export BLENDER_BIN=/path/to/blender"
    echo "  ./run_material_spectrum.sh"
    exit 1
fi

echo "Using Blender: $BLENDER_BIN"
echo "Running: material_spectrum.py"
echo "  → marble | terracotta | bronze | glass | wireframe"
echo "--------------------------------------------"

"$BLENDER_BIN" --python "$PYTHON_SCRIPT"
