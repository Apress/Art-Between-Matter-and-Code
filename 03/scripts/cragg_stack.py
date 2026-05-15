"""
cragg_stack.py — Tony Cragg: Stack (procedural stratified surfaces)
====================================================================
Chapter 3 · Art Between Matter and Code · Gianpiero Moioli
Apress / Springer Nature, 2025 · CC BY-NC 4.0

Companion to §3.6.3.1 and Figure 20.

Procedurally generates stratified, torsional surfaces inspired by
Tony Cragg's *Stack* (2011) — layered volumes that appear to solidify
a "frozen moment of movement."

A Subdivision Surface + animated Displace modifier produces
undulating rhythms and organic torsion. Each keyframe captures
a different state of the evolving form — demonstrating how Cragg's
sculptural language can be understood as the crystallisation of a
generative process.

Usage:
    Blender 5.1 → Scripting → Run Script (Alt+P)
    or: blender --python cragg_stack.py

Parameters (edit CONFIG below):
    STRENGTH       — displacement amplitude (layering depth)
    NOISE_SCALE    — spatial frequency of the displacement texture
    SUB_LEVELS     — subdivision levels (detail)
    TORSION        — twist angle applied to the top of the form (degrees)
    ANIMATE        — True = add keyframes showing the growth over 60 frames
"""

import bpy
import bmesh
import math
import os

# ── CONFIG ────────────────────────────────────────────────────────────────────
STRENGTH    = 0.40
NOISE_SCALE = 0.8
SUB_LEVELS  = 3
TORSION     = 35.0   # degrees of twist (top vs bottom)
ANIMATE     = True   # add keyframes
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


def make_material(name, color=(0.7, 0.65, 0.55), roughness=0.6, metallic=0.0):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Roughness"].default_value  = roughness
    bsdf.inputs["Metallic"].default_value   = metallic
    return mat


def build_cragg_stack():
    # Tall rectangular base — proportions recall Cragg's towers
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 1.5))
    obj = bpy.context.active_object
    obj.name = "Cragg_Stack"
    obj.dimensions = (1.0, 1.0, 3.0)

    # Apply torsion via bmesh — twist vertices by height
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    torsion_rad = math.radians(TORSION)
    max_z = max(v.co.z for v in bm.verts)
    min_z = min(v.co.z for v in bm.verts)
    span_z = max_z - min_z if max_z != min_z else 1.0
    for v in bm.verts:
        t     = (v.co.z - min_z) / span_z   # 0 at base, 1 at top
        angle = t * torsion_rad
        x, y  = v.co.x, v.co.y
        v.co.x = x * math.cos(angle) - y * math.sin(angle)
        v.co.y = x * math.sin(angle) + y * math.cos(angle)
    bm.to_mesh(obj.data)
    bm.free()
    obj.data.update()

    # Subdivision Surface
    sub = obj.modifiers.new("Subdivision", type="SUBSURF")
    sub.levels        = SUB_LEVELS
    sub.render_levels = SUB_LEVELS

    # Displace modifier — stratified layering
    tex = bpy.data.textures.new("CraggTex", type="MUSGRAVE")
    tex.musgrave_type   = "HYBRID_MULTIFRACTAL"
    tex.noise_scale     = NOISE_SCALE
    tex.octaves         = 6
    tex.noise_intensity = 1.2

    disp = obj.modifiers.new("Displace", type="DISPLACE")
    disp.texture         = tex
    disp.strength        = STRENGTH
    disp.texture_coords  = "LOCAL"
    disp.direction       = "NORMAL"

    obj.data.materials.append(make_material("Cragg_Mat", (0.72, 0.68, 0.60)))

    # Animate: strength grows from 0 to STRENGTH over 60 frames
    if ANIMATE:
        scene = bpy.context.scene
        scene.frame_start = 1
        scene.frame_end   = 60
        scene.frame_set(1)
        disp.strength = 0.0
        disp.keyframe_insert("strength", frame=1)
        scene.frame_set(30)
        disp.strength = STRENGTH * 0.5
        disp.keyframe_insert("strength", frame=30)
        scene.frame_set(60)
        disp.strength = STRENGTH
        disp.keyframe_insert("strength", frame=60)
        scene.frame_set(1)

    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    return obj


def main():
    clear_scene()
    obj = build_cragg_stack()

    bpy.ops.object.camera_add(location=(4, -4, 3))
    cam = bpy.context.active_object
    cam.rotation_euler = (math.radians(65), 0, math.radians(45))
    bpy.context.scene.camera = cam

    bpy.ops.object.light_add(type="SUN", location=(4, -3, 7))
    sun = bpy.context.active_object
    sun.data.energy = 4.0
    sun.rotation_euler = (math.radians(40), 0, math.radians(25))

    bpy.ops.object.light_add(type="AREA", location=(-3, 2, 4))
    fill = bpy.context.active_object
    fill.data.energy = 80
    fill.data.size   = 5.0

    bpy.context.scene.render.engine       = "CYCLES"
    bpy.context.scene.cycles.samples      = 128
    bpy.context.scene.render.resolution_x = 1920
    bpy.context.scene.render.resolution_y = 1080

    print(f"[cragg_stack] Scene ready.")
    print(f"  Displacement : {STRENGTH}  |  Noise scale: {NOISE_SCALE}")
    print(f"  Torsion      : {TORSION}°  |  Subdivisions: {SUB_LEVELS}")
    if ANIMATE:
        print("  Animation    : 60 frames — strength grows from 0 to max.")
        print("  Press Space to play the growth sequence.")
    load_into_editor()


if __name__ == "__main__":
    main()
