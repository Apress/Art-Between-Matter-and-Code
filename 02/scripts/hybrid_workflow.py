"""
hybrid_workflow.py — The Four-Phase Hybrid Workflow in Blender
==============================================================
Chapter 2 · Art Between Matter and Code · Gianpiero Moioli
Apress / Springer Nature, 2025 · CC BY-NC 4.0

Companion to §2.3 (Hybrid Modeling Workflows) and Figure 11.

Demonstrates the cyclical hybrid workflow described in the chapter:
    Phase 1  Manual / Traditional  — physical maquette (simulated as clay-like mesh)
    Phase 2  Digital / Computational — procedural refinement (Geometry Nodes style)
    Phase 3  AI Integration         — noise-driven generative variation
    Phase 4  Digital Fabrication    — export-ready mesh (manifold, scaled, print-ready)

Each phase builds on the previous, showing how the same initial form evolves
through the four nodes of the hybrid cycle.

Usage:
    Blender 5.1 → Scripting → Run Script (Alt+P)
    or: blender --python hybrid_workflow.py

Parameters:
    START_PHASE   — 1 | 2 | 3 | 4  (run from this phase onward)
    END_PHASE     — 1 | 2 | 3 | 4  (run until this phase)
    EXPORT_STL    — True = export Phase 4 result as STL for 3D printing
    EXPORT_PATH   — output path for STL (uses script directory by default)
"""

import bpy
import bmesh
import math
import os

# ── CONFIG ────────────────────────────────────────────────────────────────────
START_PHASE = 1
END_PHASE   = 4
EXPORT_STL  = False
EXPORT_PATH = ""    # leave empty → file saved next to the .blend; or set a full path
# ──────────────────────────────────────────────────────────────────────────────

PHASE_COLORS = {
    1: (0.72, 0.55, 0.40),  # clay warm
    2: (0.35, 0.55, 0.75),  # digital blue
    3: (0.55, 0.35, 0.75),  # generative violet
    4: (0.30, 0.70, 0.45),  # fabrication green
}


def load_into_editor():
    """Open this file in Blender's Scripting workspace so the CONFIG block
    is immediately visible and editable after the launcher runs the script."""
    try:
        filepath = os.path.abspath(__file__)
        name     = os.path.basename(filepath)
        if name not in bpy.data.texts:
            bpy.ops.text.open(filepath=filepath)
        for ws in bpy.data.workspaces:
            if "Script" in ws.name:
                bpy.context.window.workspace = ws
                break
    except (NameError, Exception):
        pass


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()


def make_material(name, color, roughness=0.7):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Roughness"].default_value  = roughness
    return mat


# ── PHASE 1: Manual — Clay Maquette Simulation ───────────────────────────────

def phase1_maquette():
    """Simulate the starting physical maquette: a lumpy, hand-made base form."""
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0, segments=24, ring_count=16,
                                          location=(0, 0, 0))
    obj = bpy.context.active_object
    obj.name = "Phase1_Maquette"

    # Add organic irregularity via displacement (simulates hand-press marks)
    disp = obj.modifiers.new("ClayTexture", type="DISPLACE")
    tex  = bpy.data.textures.new("ClayNoise", type="CLOUDS")
    tex.noise_scale = 0.6
    tex.noise_depth = 2
    disp.texture    = tex
    disp.strength   = 0.18
    disp.texture_coords = "LOCAL"

    # Flatten base (simulate resting on surface)
    bpy.ops.object.mode_set(mode="EDIT")
    bm = bmesh.from_edit_mesh(obj.data)
    for v in bm.verts:
        if v.co.z < -0.7:
            v.co.z = -0.7
    bmesh.update_edit_mesh(obj.data)
    bpy.ops.object.mode_set(mode="OBJECT")

    obj.data.materials.append(make_material("Clay_Mat", PHASE_COLORS[1]))
    print("[hybrid_workflow] Phase 1 (Manual): clay maquette created.")
    return obj


# ── PHASE 2: Digital — Procedural Refinement ─────────────────────────────────

def phase2_digital(source_obj):
    """Apply digital refinement: subdivision, retopology simulation, precision."""
    source_obj.select_set(True)
    bpy.context.view_layer.objects.active = source_obj

    # Apply existing modifiers (bake phase 1 clay texture)
    for mod in list(source_obj.modifiers):
        bpy.ops.object.modifier_apply(modifier=mod.name)

    # Voxel remesh — simulates retopology to clean uniform mesh
    source_obj.data.remesh_voxel_size = 0.06
    bpy.ops.object.voxel_remesh()

    # Subdivision for smooth digital surface
    sub = source_obj.modifiers.new("DigitalSubdiv", type="SUBSURF")
    sub.levels = 2

    # Update material for phase 2
    source_obj.data.materials.clear()
    source_obj.data.materials.append(
        make_material("Digital_Mat", PHASE_COLORS[2], roughness=0.35)
    )
    source_obj.name = "Phase2_Digital"
    print("[hybrid_workflow] Phase 2 (Digital): remeshed and subdivided.")
    return source_obj


# ── PHASE 3: AI — Generative Variation ───────────────────────────────────────

def phase3_generative(source_obj):
    """Add AI-inspired unpredictable variation: multi-frequency noise layers."""
    # Layer 1: medium-scale undulation
    d1 = source_obj.modifiers.new("GenVar_Low", type="DISPLACE")
    t1 = bpy.data.textures.new("GenNoise_Low", type="MUSGRAVE")
    t1.musgrave_type   = "HYBRID_MULTIFRACTAL"
    t1.noise_scale     = 1.2
    t1.noise_intensity = 0.8
    d1.texture = t1; d1.strength = 0.08; d1.texture_coords = "LOCAL"

    # Layer 2: fine-scale detail
    d2 = source_obj.modifiers.new("GenVar_High", type="DISPLACE")
    t2 = bpy.data.textures.new("GenNoise_High", type="CLOUDS")
    t2.noise_scale = 0.25; t2.noise_depth = 4
    d2.texture = t2; d2.strength = 0.025; d2.texture_coords = "LOCAL"

    source_obj.data.materials.clear()
    source_obj.data.materials.append(
        make_material("Generative_Mat", PHASE_COLORS[3], roughness=0.5)
    )
    source_obj.name = "Phase3_Generative"
    print("[hybrid_workflow] Phase 3 (AI/Generative): multi-layer variation applied.")
    return source_obj


# ── PHASE 4: Fabrication — Print-Ready Export ─────────────────────────────────

def phase4_fabrication(source_obj):
    """Prepare for 3D printing: apply all modifiers, ensure manifold mesh."""
    bpy.context.view_layer.objects.active = source_obj
    source_obj.select_set(True)

    # Apply all modifiers
    for mod in list(source_obj.modifiers):
        try:
            bpy.ops.object.modifier_apply(modifier=mod.name)
        except Exception as e:
            print(f"  [warn] Could not apply '{mod.name}': {e}")

    # Merge doubles (remove_doubles was renamed in Blender 4.x)
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.mesh.merge_by_distance(threshold=0.001)
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.object.mode_set(mode="OBJECT")

    # Scale to real-world: 20cm diameter
    target_scale = 0.20 / max(source_obj.dimensions)
    source_obj.scale = (target_scale,) * 3
    bpy.ops.object.transform_apply(scale=True)

    source_obj.data.materials.clear()
    source_obj.data.materials.append(
        make_material("Fabrication_Mat", PHASE_COLORS[4], roughness=0.9)
    )
    source_obj.name = "Phase4_FabReady"
    print(f"[hybrid_workflow] Phase 4 (Fabrication): mesh ready. "
          f"Dimensions: {[round(d*100,1) for d in source_obj.dimensions]} cm")

    if EXPORT_STL:
        # Resolve export path: use EXPORT_PATH if set, otherwise next to .blend
        path = EXPORT_PATH.strip() if EXPORT_PATH.strip() else os.path.join(
            bpy.path.abspath("//") or os.path.expanduser("~"),
            "hybrid_workflow_output.stl"
        )
        try:
            # Blender 4.x / 5.x built-in STL exporter
            bpy.ops.wm.stl_export(filepath=path, export_selected_objects=True)
        except AttributeError:
            # Blender 3.x fallback
            bpy.ops.export_mesh.stl(filepath=path, use_selection=True)
        print(f"  STL exported: {path}")

    return source_obj


# ── SETUP ─────────────────────────────────────────────────────────────────────

def setup_render():
    bpy.ops.object.camera_add(location=(3, -3, 2.5))
    cam = bpy.context.active_object
    cam.rotation_euler = (math.radians(55), 0, math.radians(45))
    bpy.context.scene.camera = cam

    bpy.ops.object.light_add(type="AREA", location=(2, -2, 4))
    light = bpy.context.active_object
    light.data.energy = 300
    light.data.size   = 3

    bpy.context.scene.render.engine = "CYCLES"
    bpy.context.scene.cycles.samples = 64


def main():
    print(f"[hybrid_workflow] Running phases {START_PHASE} → {END_PHASE}")
    clear_scene()

    obj = None
    if START_PHASE <= 1 <= END_PHASE:
        obj = phase1_maquette()
    if START_PHASE <= 2 <= END_PHASE and obj:
        obj = phase2_digital(obj)
    if START_PHASE <= 3 <= END_PHASE and obj:
        obj = phase3_generative(obj)
    if START_PHASE <= 4 <= END_PHASE and obj:
        obj = phase4_fabrication(obj)

    setup_render()
    print("[hybrid_workflow] Complete. Each phase is visible as a modifier stack state.")
    print("  To inspect individual phases: set END_PHASE=1, 2, 3, or 4 and re-run.")
    load_into_editor()


if __name__ == "__main__":
    main()
