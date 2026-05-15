"""
organic_surface.py — Organic Surface with the Displace Modifier
===============================================================
Chapter 3 · Art Between Matter and Code · Gianpiero Moioli
Apress / Springer Nature, 2025 · CC BY-NC 4.0

Companion to §3.6.1.1 and Figure 14.

Transforms a flat plane into a complex organic relief by applying
procedural displacement textures — evoking skin, geological terrain,
or alien membranes.

Pipeline:
    1. Plane base mesh
    2. Subdivision Surface (Levels 1–2) — enough geometry for displacement
    3. Displace modifier with a procedural texture (Musgrave / Clouds / Voronoi)
    4. Second Subdivision Surface (Levels 2–3) — smooth the displaced surface

Usage:
    Blender 5.1 → Scripting → Run Script (Alt+P)
    or: blender --python organic_surface.py

Parameters (edit CONFIG below):
    TEXTURE_TYPE   — "MUSGRAVE" | "CLOUDS" | "VORONOI"
    STRENGTH       — displacement height (0.05 – 0.5)
    MIDLEVEL       — neutral plane offset (0.0 – 1.0)
    NOISE_SIZE     — texture scale
    SUB_PRE        — subdivision levels before displace
    SUB_POST       — subdivision levels after displace (final smoothing)
"""

import bpy
import math
import os

# ── CONFIG ────────────────────────────────────────────────────────────────────
TEXTURE_TYPE = "MUSGRAVE"   # "MUSGRAVE" | "CLOUDS" | "VORONOI"
STRENGTH     = 0.25
MIDLEVEL     = 0.5
NOISE_SIZE   = 1.0
SUB_PRE      = 2            # subdivision before displacement
SUB_POST     = 2            # subdivision after displacement (smoothing)
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


def make_material(name, color=(0.7, 0.65, 0.55), roughness=0.7):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Roughness"].default_value  = roughness
    return mat


def build_organic_surface():
    # Base plane
    bpy.ops.mesh.primitive_plane_add(size=4, location=(0, 0, 0))
    plane = bpy.context.active_object
    plane.name = "OrganicSurface"

    # 1 — Subdivision before displacement (enough geometry)
    sub_pre = plane.modifiers.new("SubPre", type="SUBSURF")
    sub_pre.levels        = SUB_PRE
    sub_pre.render_levels = SUB_PRE

    # 2 — Procedural displacement texture
    tex = bpy.data.textures.new("OrganicTex", type=TEXTURE_TYPE)
    if TEXTURE_TYPE == "MUSGRAVE":
        tex.musgrave_type   = "FBM"
        tex.noise_scale     = NOISE_SIZE
        tex.noise_intensity = 1.0
        tex.octaves         = 6
    elif TEXTURE_TYPE == "CLOUDS":
        tex.noise_scale = NOISE_SIZE
        tex.noise_depth = 4
    elif TEXTURE_TYPE == "VORONOI":
        tex.noise_scale = NOISE_SIZE

    disp = plane.modifiers.new("Displace", type="DISPLACE")
    disp.texture        = tex
    disp.strength       = STRENGTH
    disp.mid_level      = MIDLEVEL
    disp.texture_coords = "LOCAL"

    # 3 — Subdivision after displacement (final smoothing)
    sub_post = plane.modifiers.new("SubPost", type="SUBSURF")
    sub_post.levels        = SUB_POST
    sub_post.render_levels = SUB_POST

    plane.data.materials.append(
        make_material("OrganicMat", color=(0.72, 0.65, 0.55))
    )
    plane.select_set(True)
    bpy.context.view_layer.objects.active = plane
    return plane


def setup_render():
    bpy.ops.object.camera_add(location=(0, -5, 4))
    cam = bpy.context.active_object
    cam.rotation_euler = (math.radians(50), 0, 0)
    bpy.context.scene.camera = cam

    bpy.ops.object.light_add(type="SUN", location=(3, -3, 6))
    sun = bpy.context.active_object
    sun.data.energy = 3.0
    sun.rotation_euler = (math.radians(45), 0, math.radians(30))

    bpy.ops.object.light_add(type="AREA", location=(-3, 2, 4))
    fill = bpy.context.active_object
    fill.data.energy = 60
    fill.data.size   = 3.0

    bpy.context.scene.render.engine       = "CYCLES"
    bpy.context.scene.cycles.samples      = 128
    bpy.context.scene.render.resolution_x = 1920
    bpy.context.scene.render.resolution_y = 1080


def main():
    clear_scene()
    plane = build_organic_surface()
    setup_render()
    print(f"[organic_surface] Scene ready.")
    print(f"  Texture type : {TEXTURE_TYPE}")
    print(f"  Strength     : {STRENGTH}  |  Midlevel: {MIDLEVEL}")
    print(f"  Tip: change TEXTURE_TYPE to CLOUDS or VORONOI and re-run (Alt+P).")
    load_into_editor()


if __name__ == "__main__":
    main()
