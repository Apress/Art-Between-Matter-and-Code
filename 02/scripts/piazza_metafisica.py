"""
piazza_metafisica.py — Piazza Metafisica: Hybrid Sculpture in Blender
======================================================================
Chapter 2 · Art Between Matter and Code · Gianpiero Moioli
Apress / Springer Nature, 2025 · CC BY-NC 4.0

Companion script to Figures 15–17 (Object Mode, Edit Mode, Sculpt Mode).

Demonstrates the three-stage manual modeling workflow described in §2.5.1:
    Stage 1 (Object Mode)  — volumetric composition with primitives
    Stage 2 (Edit Mode)    — mesh refinement, edge loops, extrusions
    Stage 3 (Sculpt Mode)  — gestural surface detailing

The resulting form is a hybrid architectural-sculptural structure evoking
the metaphysical atmosphere of De Chirico's piazze: geometric arcades,
displaced volumes, and Mediterranean light.

Usage:
    Blender 5.1 → Scripting workspace → Run Script (Alt+P)
    or: blender --python piazza_metafisica.py

Parameters (edit CONFIG below):
    MODE          — "object" | "edit" | "sculpt" | "all"
    APPLY_BOOLEAN — apply boolean cuts on the arcade
    SUBDIVISIONS  — base subdivision level for sculpt-ready mesh
"""

import bpy
import bmesh
import math
import os
from mathutils import Vector

# ── CONFIG ────────────────────────────────────────────────────────────────────
MODE          = "all"    # "object" | "edit" | "sculpt" | "all"
APPLY_BOOLEAN = True
SUBDIVISIONS  = 2        # subdivision surface level before sculpt stage
# ──────────────────────────────────────────────────────────────────────────────


def load_into_editor():
    try:
        filepath = os.path.abspath(__file__)
    except NameError:
        return
    name = os.path.basename(filepath)
    text = bpy.data.texts[name] if name in bpy.data.texts else bpy.data.texts.load(filepath)

    def _switch():
        for ws in bpy.data.workspaces:
            for screen in ws.screens:
                for area in screen.areas:
                    if area.type == 'TEXT_EDITOR':
                        area.spaces.active.text = text
        script_ws = next((ws for ws in bpy.data.workspaces if "Script" in ws.name), None)
        if script_ws:
            for window in bpy.context.window_manager.windows:
                window.workspace = script_ws

    bpy.app.timers.register(_switch, first_interval=0.5)


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()


def move_to_collection(obj, col):
    """Move obj into col, removing it from every collection it currently belongs to.
    Works regardless of which collection Blender chose as the active one."""
    for c in list(obj.users_collection):
        c.objects.unlink(obj)
    col.objects.link(obj)


def make_material(name, color, roughness=0.6, metallic=0.0):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Roughness"].default_value  = roughness
    bsdf.inputs["Metallic"].default_value   = metallic
    return mat


# ── STAGE 1: Object Mode — Volumetric Composition ────────────────────────────

def build_piazza_base(col):
    """Ground plane: polished stone floor."""
    bpy.ops.mesh.primitive_plane_add(size=6, location=(0, 0, 0))
    floor = bpy.context.active_object
    floor.name = "Piazza_Floor"
    floor.data.materials.append(make_material("Floor_Mat", (0.85, 0.82, 0.75), roughness=0.3))
    move_to_collection(floor, col)
    return floor


def build_arcade(col):
    """Three arched openings — the central element of the Piazza."""
    arches = []
    for i, x in enumerate([-1.5, 0.0, 1.5]):
        # Pillar
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x - 0.3, 0, 0.75))
        p1 = bpy.context.active_object
        p1.name = f"Pillar_L_{i}"
        p1.dimensions = (0.25, 0.4, 1.5)
        p1.data.materials.append(make_material(f"Pillar_{i}", (0.90, 0.86, 0.78), roughness=0.7))
        move_to_collection(p1, col)

        bpy.ops.mesh.primitive_cube_add(size=1, location=(x + 0.3, 0, 0.75))
        p2 = bpy.context.active_object
        p2.name = f"Pillar_R_{i}"
        p2.dimensions = (0.25, 0.4, 1.5)
        p2.data.materials.append(make_material(f"Pillar_{i}R", (0.90, 0.86, 0.78), roughness=0.7))
        move_to_collection(p2, col)

        # Arch lintel
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x, 0, 1.55))
        lintel = bpy.context.active_object
        lintel.name = f"Lintel_{i}"
        lintel.dimensions = (0.85, 0.4, 0.15)
        lintel.data.materials.append(make_material(f"Lintel_{i}", (0.92, 0.88, 0.80)))
        move_to_collection(lintel, col)

        arches.extend([p1, p2, lintel])

    # Entablature (top frieze)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 1.75))
    frieze = bpy.context.active_object
    frieze.name = "Frieze"
    frieze.dimensions = (4.5, 0.45, 0.3)
    frieze.data.materials.append(make_material("Frieze_Mat", (0.93, 0.90, 0.82), roughness=0.5))
    move_to_collection(frieze, col)
    arches.append(frieze)
    return arches


def build_displaced_volumes(col):
    """Floating / displaced geometric volumes — the surrealist element."""
    objs = []

    # Sphere hovering above-left
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.4, location=(-2, -0.5, 1.8))
    sphere = bpy.context.active_object
    sphere.name = "Floating_Sphere"
    sphere.data.materials.append(make_material("Sphere_Mat", (0.4, 0.5, 0.8), roughness=0.2, metallic=0.3))
    move_to_collection(sphere, col)
    objs.append(sphere)

    # Tilted cube — right side
    bpy.ops.mesh.primitive_cube_add(size=0.6, location=(2.2, 0.3, 0.8))
    cube = bpy.context.active_object
    cube.name = "Tilted_Cube"
    cube.rotation_euler = (0.3, 0.15, 0.8)
    cube.data.materials.append(make_material("Cube_Mat", (0.7, 0.3, 0.25), roughness=0.6))
    move_to_collection(cube, col)
    objs.append(cube)

    # Tall obelisk — back-left
    bpy.ops.mesh.primitive_cube_add(size=1, location=(-2.5, 1.0, 1.2))
    obelisk = bpy.context.active_object
    obelisk.name = "Obelisk"
    obelisk.dimensions = (0.2, 0.2, 2.4)
    obelisk.data.materials.append(make_material("Obelisk_Mat", (0.85, 0.80, 0.65), roughness=0.8))
    move_to_collection(obelisk, col)
    objs.append(obelisk)

    return objs


# ── STAGE 2: Edit Mode — Mesh Refinement ─────────────────────────────────────

def refine_floor_mesh(floor_obj):
    """Add edge loops and slight wave displacement to the floor."""
    bpy.ops.object.select_all(action="DESELECT")
    bpy.context.view_layer.objects.active = floor_obj
    floor_obj.select_set(True)          # mode_set requires active + selected
    bpy.ops.object.mode_set(mode="EDIT")

    bm = bmesh.from_edit_mesh(floor_obj.data)
    # Subdivide for more resolution
    bmesh.ops.subdivide_edges(bm, edges=bm.edges, cuts=6, use_grid_fill=True)
    # Slight elevation variation — wave pattern
    import math as m
    for v in bm.verts:
        v.co.z += 0.012 * m.sin(v.co.x * 3.0) * m.cos(v.co.y * 2.5)
    bmesh.update_edit_mesh(floor_obj.data)

    bpy.ops.object.mode_set(mode="OBJECT")


# ── STAGE 3: Sculpt — Surface Gesture ────────────────────────────────────────

def prepare_sphere_for_sculpt(sphere_obj):
    """Add subdivision to the sphere so it can be sculpted."""
    bpy.context.view_layer.objects.active = sphere_obj
    sphere_obj.select_set(True)

    sub = sphere_obj.modifiers.new("Subdiv_Sculpt", type="SUBSURF")
    sub.levels         = SUBDIVISIONS
    sub.render_levels  = SUBDIVISIONS

    # Add a displacement modifier simulating gestural sculpt marks
    disp = sphere_obj.modifiers.new("DisplaceGesture", type="DISPLACE")
    tex  = bpy.data.textures.new("SculptNoise", type="CLOUDS")
    tex.noise_scale   = 0.5
    tex.noise_depth   = 3
    disp.texture      = tex
    disp.strength     = 0.06
    disp.texture_coords = "LOCAL"


# ── CAMERA & LIGHTING ─────────────────────────────────────────────────────────

def setup_render():
    # Camera — isometric-ish view
    bpy.ops.object.camera_add(location=(5, -5, 4.5))
    cam = bpy.context.active_object
    cam.rotation_euler = (math.radians(58), 0, math.radians(45))
    bpy.context.scene.camera = cam

    # Sun light (Mediterranean)
    bpy.ops.object.light_add(type="SUN", location=(3, -4, 6))
    sun = bpy.context.active_object
    sun.data.energy = 4.0
    sun.data.angle  = math.radians(3)
    sun.rotation_euler = (math.radians(40), 0, math.radians(30))

    # Fill light
    bpy.ops.object.light_add(type="AREA", location=(-3, 2, 3))
    fill = bpy.context.active_object
    fill.data.energy = 80
    fill.data.size   = 4.0

    # World background — pale sky
    world = bpy.context.scene.world
    world.use_nodes = True
    bg = world.node_tree.nodes["Background"]
    bg.inputs["Color"].default_value    = (0.82, 0.88, 0.96, 1.0)
    bg.inputs["Strength"].default_value = 0.8

    # Render settings
    bpy.context.scene.render.engine         = "CYCLES"
    bpy.context.scene.cycles.samples        = 128
    bpy.context.scene.render.resolution_x   = 1920
    bpy.context.scene.render.resolution_y   = 1080


def main():
    clear_scene()

    col = bpy.data.collections.new("PiazzaMetafisica")
    bpy.context.scene.collection.children.link(col)

    # Initialise to None so stages 2–3 can check safely even if stage 1 was skipped
    floor   = None
    arcade  = None
    volumes = None

    if MODE in ("object", "all"):
        floor   = build_piazza_base(col)
        arcade  = build_arcade(col)
        volumes = build_displaced_volumes(col)
        print("[piazza_metafisica] Stage 1 (Object Mode) — composition built.")

    if MODE in ("edit", "all") and floor is not None:
        refine_floor_mesh(floor)
        print("[piazza_metafisica] Stage 2 (Edit Mode) — floor mesh refined.")

    if MODE in ("sculpt", "all") and volumes is not None:
        sphere = next((o for o in volumes if "Sphere" in o.name), None)
        if sphere:
            prepare_sphere_for_sculpt(sphere)
            print("[piazza_metafisica] Stage 3 (Sculpt) — sphere prepared for gestural sculpting.")

    setup_render()

    # Ensure we always finish in Object Mode regardless of which stages ran
    try:
        bpy.ops.object.mode_set(mode="OBJECT")
    except Exception:
        pass

    print("[piazza_metafisica] Scene ready. Use Blender's Sculpt Mode to add brush detail.")
    load_into_editor()


if __name__ == "__main__":
    main()
