"""
_make_startup.py — Create _scripting_startup.blend (run ONCE)
=============================================================
Chapter 2 · Art Between Matter and Code · Gianpiero Moioli
Apress / Springer Nature, 2025 · CC BY-NC 4.0

HOW TO RUN:
  1. Open Blender and click the Scripting workspace tab
  2. Text Editor header > Open > select THIS file from disk
  3. Press Alt+P

Blender saves _scripting_startup.blend in the same folder.
Commit _scripting_startup.blend to the repo — done.
"""

import bpy
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
print("\n[setup] Creating _scripting_startup.blend ...")

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

# ── Save a copy with the current workspace (Scripting) baked in ───────────────
out = os.path.join(script_dir, "_scripting_startup.blend")
bpy.ops.wm.save_as_mainfile(filepath=out, copy=True)

print(f"[setup] Saved: {out}")
print("[setup] Done.")
print("[setup] You can close Blender.")
print("[setup] Then:  git add 02/scripts/_scripting_startup.blend && git commit -m 'add: scripting startup blend'")
