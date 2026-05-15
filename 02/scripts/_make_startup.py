"""
_make_startup.py — One-time setup: creates _scripting_startup.blend
====================================================================
Chapter 2 · Art Between Matter and Code · Gianpiero Moioli
Apress / Springer Nature, 2025 · CC BY-NC 4.0

Run automatically by the .bat files on first launch, OR manually
from Blender's text editor (Alt+P) if you need to regenerate it.

Creates _scripting_startup.blend in the same directory: a minimal
Blender file saved with the Scripting workspace active.  The .bat
launchers open this file so Blender always starts in Scripting.
"""

import bpy
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
print("\n[setup] Creating _scripting_startup.blend ...")

# ── Switch to Scripting workspace ────────────────────────────────────────────
ws = next((w for w in bpy.data.workspaces if "Script" in w.name), None)
if ws:
    for window in bpy.context.window_manager.windows:
        window.workspace = ws
    print(f"[setup] Workspace set to: '{ws.name}'")
else:
    available = [w.name for w in bpy.data.workspaces]
    print(f"[setup] WARNING: no Scripting workspace found.")
    print(f"[setup] Available workspaces: {available}")
    print("[setup] Add the Scripting workspace in Blender and re-run this script.")

# ── Clear the default scene so the saved blend is minimal ────────────────────
try:
    bpy.ops.object.mode_set(mode="OBJECT")
except Exception:
    pass
try:
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()
except Exception as e:
    print(f"[setup] Scene clear skipped: {e}")

# ── Save ─────────────────────────────────────────────────────────────────────
out = os.path.join(script_dir, "_scripting_startup.blend")
bpy.ops.wm.save_as_mainfile(filepath=out, copy=True)
print(f"[setup] Saved: {out}")
print("[setup] Done — .bat launchers will now open directly in Scripting workspace.\n")

# ── Quit so the .bat can proceed immediately ──────────────────────────────────
bpy.ops.wm.quit_blender()
