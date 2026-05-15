"""
scan_cleanup.py — Photogrammetry Mesh Cleanup in Blender
=========================================================
Chapter 2 · Art Between Matter and Code · Gianpiero Moioli
Apress / Springer Nature, 2025 · CC BY-NC 4.0

Companion to §2.1.2.1.2–3 (3D Acquisition and Post-Processing) and
§2.5.2.1 (3D Scan and Digital Transformation).

Automates the post-processing pipeline for imported scan meshes:
    1. Remove doubles / merge by distance
    2. Recalculate normals
    3. Fill small holes
    4. Optional: Voxel Remesh for uniform topology
    5. Optional: Subdivision Surface for smooth preview
    6. Optional: Displacement for artistic transformation

Works on the currently selected object. Import your scan first
(File > Import > OBJ/FBX/PLY), select it, then run this script.

Usage:
    Blender 5.1 → select the scan mesh → Scripting → Run Script (Alt+P)

Parameters:
    MERGE_DISTANCE  — threshold for merging duplicate vertices (scan noise)
    VOXEL_REMESH    — True = rebuild topology as uniform voxel grid
    VOXEL_SIZE      — voxel size (smaller = more detail, heavier mesh)
    SUBDIVIDE       — add subdivision for smooth sculpt-ready preview
    SUB_LEVELS      — subdivision levels
    ADD_ARTISTIC    — add displacement modifier for experimental variation
"""

import bpy
import bmesh
import os

# ── CONFIG ────────────────────────────────────────────────────────────────────
MERGE_DISTANCE = 0.0005   # 0.5 mm — typical scan noise threshold
VOXEL_REMESH   = True     # rebuild as uniform voxel grid
VOXEL_SIZE     = 0.003    # voxel size in scene units
SUBDIVIDE      = True     # add Subdivision Surface modifier
SUB_LEVELS     = 1        # subdivision level (1-3 for scans)
ADD_ARTISTIC   = False    # add noise displacement for artistic variation
NOISE_STRENGTH = 0.015    # displacement strength if ADD_ARTISTIC=True
# ──────────────────────────────────────────────────────────────────────────────


def load_into_editor():
    """Load this script into the Scripting workspace text editor.

    The workspace switch is handled by the .bat launcher (which opens
    _scripting_startup.blend).  This function only needs to make the
    script text appear in the text-editor area so the CONFIG block is
    immediately visible and editable.
    """
    try:
        filepath = os.path.abspath(__file__)
    except NameError:
        return   # running from the text editor — already loaded
    name = os.path.basename(filepath)
    text = bpy.data.texts.get(name) or bpy.data.texts.load(filepath)

    def _set_text():
        for ws in bpy.data.workspaces:
            for screen in ws.screens:
                for area in screen.areas:
                    if area.type == 'TEXT_EDITOR':
                        area.spaces.active.text = text
        return None  # one-shot

    bpy.app.timers.register(_set_text, first_interval=0.5)


def get_active_mesh():
    obj = bpy.context.active_object
    if obj is None or obj.type != "MESH":
        raise RuntimeError(
            "No mesh object selected. Select your scan mesh and run again."
        )
    return obj


def apply_transforms(obj):
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    print(f"  [cleanup] Transforms applied on '{obj.name}'")


def merge_by_distance(obj, threshold):
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    before = len(bm.verts)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=threshold)
    after = len(bm.verts)
    bm.to_mesh(obj.data)
    bm.free()
    obj.data.update()
    print(f"  [cleanup] Merged by distance {threshold*1000:.1f}mm: {before} -> {after} verts "
          f"({before - after} removed)")


def recalculate_normals(obj):
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(obj.data)
    bm.free()
    obj.data.update()
    print("  [cleanup] Normals recalculated (outside-facing).")


def fill_holes(obj, max_hole_verts=50):
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    boundary_edges = [e for e in bm.edges if e.is_boundary]
    if boundary_edges:
        bmesh.ops.holes_fill(bm, edges=boundary_edges, sides=max_hole_verts)
    bm.to_mesh(obj.data)
    bm.free()
    obj.data.update()
    print(f"  [cleanup] Holes filled (max {max_hole_verts} verts per hole).")


def apply_voxel_remesh(obj, voxel_size):
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.mode_set(mode="OBJECT")   # voxel_remesh requires Object Mode
    obj.data.remesh_voxel_size = voxel_size
    bpy.ops.object.voxel_remesh()
    print(f"  [cleanup] Voxel remesh applied (size={voxel_size*1000:.1f}mm).")


def add_subdivision(obj, levels):
    sub = obj.modifiers.new("ScanSubdiv", type="SUBSURF")
    sub.levels        = levels
    sub.render_levels = levels
    print(f"  [cleanup] Subdivision Surface added (levels={levels}).")


def add_noise_displacement(obj, strength):
    disp = obj.modifiers.new("ArtisticVariation", type="DISPLACE")
    tex  = bpy.data.textures.new("ScanNoise", type="MUSGRAVE")
    tex.musgrave_type  = "FBM"
    tex.noise_scale    = 0.8
    tex.noise_intensity = 1.0
    disp.texture       = tex
    disp.strength      = strength
    disp.texture_coords = "LOCAL"
    print(f"  [cleanup] Artistic noise displacement added (strength={strength}).")


def report_mesh_stats(obj):
    m = obj.data
    print(f"  [cleanup] Final mesh: {len(m.vertices)} verts, "
          f"{len(m.edges)} edges, {len(m.polygons)} faces.")


def main():
    load_into_editor()   # always show script first so CONFIG is readable
    try:
        obj = get_active_mesh()
    except RuntimeError:
        print("[scan_cleanup] No mesh selected.")
        print("  1. File > Import > OBJ / FBX / PLY — import your scan")
        print("  2. Click on the mesh in the 3D viewport to select it")
        print("  3. Press Alt+P here to run the cleanup")
        return
    print(f"[scan_cleanup] Processing: '{obj.name}'")

    apply_transforms(obj)
    merge_by_distance(obj, MERGE_DISTANCE)
    recalculate_normals(obj)
    fill_holes(obj)

    if VOXEL_REMESH:
        apply_voxel_remesh(obj, VOXEL_SIZE)
        # Recalculate normals after remesh
        recalculate_normals(obj)

    if SUBDIVIDE:
        add_subdivision(obj, SUB_LEVELS)

    if ADD_ARTISTIC:
        add_noise_displacement(obj, NOISE_STRENGTH)

    report_mesh_stats(obj)
    print("[scan_cleanup] Done. The mesh is ready for sculpting, texturing, or export.")
    print("  Tip: switch to Sculpt Mode to add gestural detail on top of the clean base.")


if __name__ == "__main__":
    main()
