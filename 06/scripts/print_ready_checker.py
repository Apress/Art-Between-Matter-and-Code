"""
print_ready_checker.py
──────────────────────
Art Between Matter and Code · Gianpiero Moioli · Apress 2025
Chapter 6 — From Virtuality to Matter: 3D Printing and Material Translation

Blender Python script — run inside Blender's Text Editor (Alt+P).

Checks the active mesh object for 3D printability using Blender's built-in
3D Print Toolbox or raw mesh analysis via bmesh. Results are reported in the
Blender System Console and as INFO messages in the header.

Reference: §6.2 (Printing Techniques), §6.2.5 (Mini tutorial: Blender 3D Print Toolbox).

Key checks performed:
  - Non-manifold geometry (edges shared by ≠ 2 faces, or boundary edges)
  - Bounding box dimensions (mm, assuming scene unit = 1 mm)
  - Normals consistency (auto-fix if AUTO_FIX = True)
  - Remove doubles / merge by distance (auto-fix if AUTO_FIX = True)
  - 3D Print Toolbox full diagnostic (if addon is available)

Usage
─────
  1. Open Blender → Scripting workspace
  2. Open this file (or paste into Text Editor)
  3. Select the mesh object you want to check
  4. Press Alt+P to run

Requirements: Blender 4.3+.
"""

import bpy
import bmesh
import math

# ─────────────────────────────────────────────
# CONFIGURATION — edit freely
# ─────────────────────────────────────────────

MIN_WALL_THICKNESS_MM = 2.0   # minimum printable wall (FDM ≥2 mm, resin ≥1 mm, SLS ≥0.8 mm)
MAX_OVERHANG_ANGLE    = 45.0  # degrees from vertical — beyond this angle support is needed
MERGE_THRESHOLD_MM    = 0.01  # threshold for Remove Doubles (merge by distance)
AUTO_FIX              = True  # attempt automatic fixes (remove doubles, recalculate normals)


# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────

def report(msg, level="INFO"):
    """Print to console and display in Blender header."""
    print(f"[print_ready_checker] {msg}")
    # bpy.context.window_manager.popup_menu is modal; use operator report instead
    # (header message is handled by the caller's operator context)


def separator():
    print("─" * 60)


# ─────────────────────────────────────────────
# Main check routine
# ─────────────────────────────────────────────

def run_check():
    separator()
    print("[print_ready_checker]  Chapter 6 — 3D Print Readiness Check")
    print("[print_ready_checker]  Art Between Matter and Code · Gianpiero Moioli · Apress 2025")
    separator()

    # ── 1. Validate selection ────────────────────────────────────────────────
    obj = bpy.context.active_object
    if obj is None:
        print("[ERROR] No active object. Select a mesh and run again.")
        return
    if obj.type != "MESH":
        print(f"[ERROR] Active object '{obj.name}' is not a mesh (type={obj.type}).")
        return

    print(f"[OK]  Object: '{obj.name}'  (vertices: {len(obj.data.vertices)}, "
          f"faces: {len(obj.data.polygons)})")

    # ── 2. Auto-fix: enter Edit Mode, clean geometry, return to Object Mode ──
    if AUTO_FIX:
        print("[FIX]  Running Remove Doubles (merge by distance) ...")
        bpy.ops.object.mode_set(mode="EDIT")
        bpy.ops.mesh.select_all(action="SELECT")
        bpy.ops.mesh.remove_doubles(threshold=MERGE_THRESHOLD_MM / 1000.0)
        print("[FIX]  Recalculating normals (outside) ...")
        bpy.ops.mesh.normals_make_consistent(inside=False)
        bpy.ops.object.mode_set(mode="OBJECT")
        print("[OK]   Auto-fix complete.")
    else:
        print("[INFO] AUTO_FIX is disabled. Skipping Remove Doubles and Normals fix.")

    # ── 3. Enable 3D Print Toolbox if not already active ────────────────────
    addon_module = "object_print3d_utils"
    addon_enabled = addon_module in bpy.context.preferences.addons
    if not addon_enabled:
        try:
            bpy.ops.preferences.addon_enable(module=addon_module)
            addon_enabled = addon_module in bpy.context.preferences.addons
            if addon_enabled:
                print("[OK]  3D Print Toolbox addon enabled successfully.")
            else:
                print("[WARN] Could not enable 3D Print Toolbox. Skipping toolbox checks.")
        except Exception as e:
            print(f"[WARN] Error enabling 3D Print Toolbox: {e}")
    else:
        print("[OK]  3D Print Toolbox addon already active.")

    # ── 4. Run 3D Print Toolbox full check (if available) ───────────────────
    if addon_enabled:
        try:
            bpy.ops.object.mode_set(mode="OBJECT")
            result = bpy.ops.mesh.print3d_check_all()
            print(f"[OK]  3D Print Toolbox check_all returned: {result}")
            print("[INFO] Check the 3D Print Toolbox panel (N-panel → 3D Print) for details.")
        except AttributeError:
            print("[WARN] mesh.print3d_check_all not found — addon version may differ.")
        except Exception as e:
            print(f"[WARN] 3D Print Toolbox check error: {e}")

    # ── 5. BMesh analysis: non-manifold geometry ────────────────────────────
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bm.edges.ensure_lookup_table()

    non_manifold = [e for e in bm.edges if not e.is_manifold]
    bm.free()

    if non_manifold:
        print(f"[FAIL] Non-manifold edges: {len(non_manifold)}")
        print("       Non-manifold geometry must be fixed before printing.")
        print("       In Edit Mode: Mesh → Clean Up → Fill Holes / Delete Loose")
        print("       Or: Select → Select All by Trait → Non-Manifold")
    else:
        print("[OK]  Non-manifold edges: 0  (watertight mesh)")

    # ── 6. Bounding box dimensions ───────────────────────────────────────────
    bb = obj.bound_box  # 8 corners in local space
    xs = [v[0] for v in bb]
    ys = [v[1] for v in bb]
    zs = [v[2] for v in bb]
    # Apply object scale to get world dimensions
    scale = obj.scale
    dim_x = (max(xs) - min(xs)) * abs(scale[0])
    dim_y = (max(ys) - min(ys)) * abs(scale[1])
    dim_z = (max(zs) - min(zs)) * abs(scale[2])
    # Convert Blender units → mm (assuming 1 BU = 1 mm per scene settings)
    unit_scale = bpy.context.scene.unit_settings.scale_length
    # If scene unit_system is METRIC and length_unit is MILLIMETERS, scale_length = 0.001
    # We report raw dimensions and note the assumption
    print(f"[INFO] Bounding box (scene units): "
          f"X={dim_x:.2f}  Y={dim_y:.2f}  Z={dim_z:.2f}")
    print(f"       (Scene unit scale: {unit_scale} — verify units in Scene Properties)")

    # ── 7. Summary ───────────────────────────────────────────────────────────
    separator()
    print("[print_ready_checker]  SUMMARY")
    print(f"  Object           : {obj.name}")
    print(f"  Vertices         : {len(obj.data.vertices)}")
    print(f"  Faces            : {len(obj.data.polygons)}")
    print(f"  Non-manifold     : {len(non_manifold)}")
    print(f"  Dimensions (BU)  : X={dim_x:.2f}  Y={dim_y:.2f}  Z={dim_z:.2f}")
    print(f"  Min wall (FDM)   : {MIN_WALL_THICKNESS_MM} mm  "
          f"(check manually via 3D Print Toolbox → Thickness)")
    print(f"  Max overhang     : {MAX_OVERHANG_ANGLE}°  "
          f"(check manually via 3D Print Toolbox → Overhang)")
    if len(non_manifold) == 0:
        print("  Status           : READY FOR SLICING (no non-manifold edges)")
    else:
        print("  Status           : FIX REQUIRED (non-manifold edges present)")
    separator()


# ─────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────

run_check()
