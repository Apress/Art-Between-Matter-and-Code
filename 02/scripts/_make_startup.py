"""
_make_startup.py — Create _scripting_startup.blend (run ONCE)
=============================================================
Chapter 2 · Art Between Matter and Code · Gianpiero Moioli
Apress / Springer Nature, 2025 · CC BY-NC 4.0

HOW TO RUN:
  1. Open Blender and click the Scripting workspace tab
  2. Text Editor header > Open > select THIS file from disk
  3. Set OUTPUT_PATH below (copy the path of this folder)
  4. Press Alt+P

Blender saves _scripting_startup.blend in that folder.
Commit _scripting_startup.blend to the repo — done.
"""

import bpy
import os

# ── CONFIG ────────────────────────────────────────────────────────────────────
# Paste the full path to the 02/scripts folder here (keep the r prefix):
OUTPUT_PATH = r""
# Example — Windows:
#   OUTPUT_PATH = r"D:\TEORIA\Art_Matter_Code\Art-Between-Matter-and-Code\02\scripts"
# Example — macOS / Linux:
#   OUTPUT_PATH = r"/Users/yourname/Art-Between-Matter-and-Code/02/scripts"
# ──────────────────────────────────────────────────────────────────────────────


def _get_script_dir():
    # 1. OUTPUT_PATH set manually — most reliable
    if OUTPUT_PATH.strip():
        d = OUTPUT_PATH.strip()
        if not os.path.isdir(d):
            raise RuntimeError(f"OUTPUT_PATH does not exist: {d}")
        return d

    # 2. Running via --python from command line (__file__ is available)
    try:
        return os.path.dirname(os.path.abspath(__file__))
    except NameError:
        pass

    # 3. Running from text editor — use the text block's filepath
    try:
        raw = bpy.context.space_data.text.filepath
    except AttributeError:
        raise RuntimeError("Run from the Scripting workspace text editor.")

    if not raw:
        raise RuntimeError(
            "Text file has no path — use Text Editor > Open to load it from disk."
        )

    # Try absolute path as-is first, then Blender's resolver
    candidates = [raw, bpy.path.abspath(raw)]
    for fp in candidates:
        d = os.path.dirname(os.path.abspath(fp))
        if os.path.isdir(d) and d not in ("", "C:\\", "C:/", "/"):
            return d

    raise RuntimeError(
        f"Could not resolve script directory from: {raw!r}\n"
        "Set OUTPUT_PATH manually at the top of this script."
    )


script_dir = _get_script_dir()
out = os.path.join(script_dir, "_scripting_startup.blend")
print(f"\n[setup] Saving to: {out}")

# Clear the default scene for a minimal blend
try:
    bpy.ops.object.mode_set(mode="OBJECT")
except Exception:
    pass
try:
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()
except Exception as e:
    print(f"[setup] Scene clear: {e}")

# Save a copy with the current workspace (Scripting) baked in
bpy.ops.wm.save_as_mainfile(filepath=out, copy=True)

print("[setup] Done.")
print("[setup] You can close Blender.")
print("[setup] Then:  git add 02/scripts/_scripting_startup.blend && git commit -m 'add: scripting startup blend'")
