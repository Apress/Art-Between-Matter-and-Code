"""
_make_startup.py — Create _scripting_startup.blend (run ONCE)
=============================================================
Chapter 2 · Art Between Matter and Code · Gianpiero Moioli
Apress / Springer Nature, 2025 · CC BY-NC 4.0

HOW TO RUN (one time only):
  1. Open Blender
  2. Click the Scripting workspace tab
  3. In the Text Editor: Text Editor header > Open > select this file
  4. Press Alt+P

Blender saves _scripting_startup.blend next to this file — a minimal
.blend with the Scripting workspace active — then you can close Blender.
Commit _scripting_startup.blend to the repo so readers get it automatically.

The .bat launchers will then always open in Scripting workspace.
"""

import bpy
import os

# ── Find script directory ─────────────────────────────────────────────────────
try:
    # When launched via --python from command line
    script_dir = os.path.dirname(os.path.abspath(__file__))
except NameError:
    # When run from Blender's text editor (Alt+P)
    try:
        space = bpy.context.space_data
        raw = space.text.filepath
        if not raw:
            raise RuntimeError(
                "Text file has no path on disk.\n"
                "Use Text Editor > Open to load this file from disk, then Alt+P."
            )
        script_dir = os.path.dirname(bpy.path.abspath(raw))
    except AttributeError:
        raise RuntimeError("Run this script from Blender's Scripting workspace text editor.")

out = os.path.join(script_dir, "_scripting_startup.blend")
print(f"\n[setup] Saving Scripting workspace startup to:\n  {out}\n")

# ── Clear the default scene for a minimal blend ───────────────────────────────
try:
    bpy.ops.object.mode_set(mode="OBJECT")
except Exception:
    pass
try:
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()
except Exception as e:
    print(f"[setup] Scene clear: {e}")

# ── Save ──────────────────────────────────────────────────────────────────────
# copy=True writes to `out` without changing the current .blend session
bpy.ops.wm.save_as_mainfile(filepath=out, copy=True)

print("[setup] Done.")
print("[setup] You can now close Blender.")
print("[setup] Commit _scripting_startup.blend to the repo —")
print("[setup] readers will download it automatically with the other files.")
