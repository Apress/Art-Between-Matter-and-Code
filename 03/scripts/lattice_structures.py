"""
lattice_structures.py — Hollow and Lattice Structures
======================================================
Chapter 3 · Art Between Matter and Code · Gianpiero Moioli
Apress / Springer Nature, 2025 · CC BY-NC 4.0

Companion to §3.6.1.3 and Figure 16.

Converts solid forms into lightweight open frameworks using the
Wireframe and Remesh modifiers — recalling bone, coral, or
architectural trusses.

Two methods are demonstrated (select via MODE):
    "wireframe" — Wireframe modifier on a subdivided sphere
    "remesh"    — Voxel Remesh + optional Decimate for organic variation
    "both"      — side-by-side comparison

Usage:
    Blender 5.1 → Scripting → Run Script (Alt+P)
    or: blender --python lattice_structures.py

Parameters (edit CONFIG below):
    MODE            — "wireframe" | "remesh" | "both"
    WIRE_THICKNESS  — strut width for Wireframe modifier
    VOXEL_SIZE      — voxel resolution for Remesh (smaller = finer)
    DECIMATE_RATIO  — Decimate ratio after remesh (1.0 = no decimation)
"""

import bpy
import math
import os

# ── CONFIG ────────────────────────────────────────────────────────────────────
MODE           = "both"    # "wireframe" | "remesh" | "both"
WIRE_THICKNESS = 0.03
VOXEL_SIZE     = 0.08
DECIMATE_RATIO = 0.5       # 1.0 = no decimation
# ──────────────────────────────────────────────────────────────────────────────


def load_into_editor():
    try:
        filepath = os.path.abspath(__file__)
    except NameError:
        return
    name = os.path.basename(filepath)
    text = bpy.data.texts.get(name) or bpy.data.texts.load(filepath)

    def _set_text():
        for ws in bpy.data.workspaces:
            for screen in ws.screens:
                for area in screen.areas:
                    if area.type == 'TEXT_EDITOR':
                        area.spaces.active.text = text
        wm = bpy.context.window_manager
        win = wm.windows[0] if wm.windows else None
        for screen in bpy.data.screens:
            for area in screen.areas:
                if area.type != 'VIEW_3D':
                    continue
                for region in area.regions:
                    if region.type != 'WINDOW':
                        continue
                    try:
                        with bpy.context.temp_override(
                            window=win, screen=screen, area=area, region=region
                        ):
                            bpy.ops.view3d.view_selected()
                    except Exception:
                        pass
        return None

    bpy.app.timers.register(_set_text, first_interval=0.5)


def clear_scene():
    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj, do_unlink=True)


def make_material(name, color, roughness=0.6, metallic=0.0):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Roughness"].default_value  = roughness
    bsdf.inputs["Metallic"].default_value   = metallic
    return mat


def build_wireframe(location=(0, 0, 0)):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=4, radius=1.0, location=location)
    obj = bpy.context.active_object
    obj.name = "Lattice_Wireframe"

    wf = obj.modifiers.new("Wireframe", type="WIREFRAME")
    wf.thickness       = WIRE_THICKNESS
    wf.use_even_offset = True
    wf.use_relative_offset = False

    obj.data.materials.append(
        make_material("Wire_Mat", (0.6, 0.65, 0.7), roughness=0.4, metallic=0.3)
    )
    return obj


def build_remesh(location=(2.5, 0, 0)):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=3, radius=1.0, location=location)
    obj = bpy.context.active_object
    obj.name = "Lattice_Remesh"
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

    obj.data.remesh_voxel_size = VOXEL_SIZE
    bpy.ops.object.voxel_remesh()

    if DECIMATE_RATIO < 1.0:
        dec = obj.modifiers.new("Decimate", type="DECIMATE")
        dec.ratio = DECIMATE_RATIO

    obj.data.materials.append(
        make_material("Remesh_Mat", (0.75, 0.60, 0.50), roughness=0.8)
    )
    return obj


def main():
    clear_scene()

    objs = []
    if MODE in ("wireframe", "both"):
        loc = (-1.5, 0, 0) if MODE == "both" else (0, 0, 0)
        objs.append(build_wireframe(location=loc))
    if MODE in ("remesh", "both"):
        loc = (1.5, 0, 0) if MODE == "both" else (0, 0, 0)
        objs.append(build_remesh(location=loc))

    # Select all built objects
    for o in objs:
        o.select_set(True)
    if objs:
        bpy.context.view_layer.objects.active = objs[0]

    # Camera
    bpy.ops.object.camera_add(location=(0, -5, 3))
    cam = bpy.context.active_object
    cam.rotation_euler = (math.radians(55), 0, 0)
    bpy.context.scene.camera = cam

    bpy.ops.object.light_add(type="SUN", location=(3, -4, 6))
    sun = bpy.context.active_object
    sun.data.energy = 3.0
    sun.rotation_euler = (math.radians(45), 0, math.radians(30))

    bpy.ops.object.light_add(type="AREA", location=(-3, 2, 4))
    fill = bpy.context.active_object
    fill.data.energy = 80
    fill.data.size   = 4.0

    bpy.context.scene.render.engine       = "CYCLES"
    bpy.context.scene.cycles.samples      = 128
    bpy.context.scene.render.resolution_x = 1920
    bpy.context.scene.render.resolution_y = 1080

    print(f"[lattice_structures] Scene ready — mode: {MODE}")
    print(f"  Wireframe thickness : {WIRE_THICKNESS}")
    print(f"  Voxel size          : {VOXEL_SIZE}  |  Decimate: {DECIMATE_RATIO}")
    load_into_editor()


if __name__ == "__main__":
    main()
