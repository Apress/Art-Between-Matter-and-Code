"""
kapoor_tall_tree.py — Anish Kapoor: Tall Tree & The Eye (procedural)
=====================================================================
Chapter 3 · Art Between Matter and Code · Gianpiero Moioli
Apress / Springer Nature, 2025 · CC BY-NC 4.0

Companion to §3.6.3.2 and Figure 22.

Procedurally recreates the logic of Anish Kapoor's *Tall Tree and the Eye*
(2009, Guggenheim Bilbao): a vertical column of mirrored spheres whose
repetition, scale variation, and reflective surfaces create an interplay
between structure and environment.

Three methods available via MODE:
    "geonodes"  — Geometry Nodes distributes spheres inside a cylinder
    "python"    — Pure Python loop with random scale/offset variation
    "both"      — side-by-side comparison

Usage:
    Blender 5.1 → Scripting → Run Script (Alt+P)
    or: blender --python kapoor_tall_tree.py

Parameters (edit CONFIG below):
    MODE           — "geonodes" | "python" | "both"
    N_SPHERES      — number of spheres in the column
    COLUMN_HEIGHT  — total height of the column
    RADIUS_BASE    — base radius of each sphere
    RADIUS_VAR     — random variation in sphere radius
    MIRROR_FINISH  — True = near-mirror metallic material
"""

import bpy
import math
import os
import random

# ── CONFIG ────────────────────────────────────────────────────────────────────
MODE          = "geonodes"  # "geonodes" | "python" | "both"
N_SPHERES     = 60
COLUMN_HEIGHT = 5.0
RADIUS_BASE   = 0.30
RADIUS_VAR    = 0.10
MIRROR_FINISH = True
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


def mirror_material(name):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    if MIRROR_FINISH:
        bsdf.inputs["Base Color"].default_value = (0.95, 0.95, 0.95, 1.0)
        bsdf.inputs["Metallic"].default_value   = 1.0
        bsdf.inputs["Roughness"].default_value  = 0.02
    else:
        bsdf.inputs["Base Color"].default_value = (0.8, 0.8, 0.8, 1.0)
        bsdf.inputs["Roughness"].default_value  = 0.4
    return mat


def build_geonodes_column(offset_x=0.0):
    """Geometry Nodes approach: Distribute Points in Volume → Instance on Points."""
    # Cylinder defines the volume
    bpy.ops.mesh.primitive_cylinder_add(
        radius=RADIUS_BASE * 1.5, depth=COLUMN_HEIGHT,
        location=(offset_x, 0, COLUMN_HEIGHT / 2)
    )
    cyl = bpy.context.active_object
    cyl.name = "Kapoor_Column_GN"

    # Module sphere (hidden, used as instance)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=RADIUS_BASE, location=(offset_x + 20, 0, 0))
    sphere = bpy.context.active_object
    sphere.name = "Kapoor_Module_GN"
    sphere.hide_render = True
    sphere.data.materials.append(mirror_material("Mirror_GN"))

    mod = cyl.modifiers.new("GeoNodes_Kapoor", type="NODES")
    ng  = bpy.data.node_groups.new("KapoorColumn", type="GeometryNodeTree")
    mod.node_group = ng

    ng.interface.new_socket("Geometry", in_out="INPUT",  socket_type="NodeSocketGeometry")
    ng.interface.new_socket("Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")

    nodes = ng.nodes
    links = ng.links

    in_n  = nodes.new("NodeGroupInput");  in_n.location  = (-600, 0)
    out_n = nodes.new("NodeGroupOutput"); out_n.location = (600, 0)

    distrib = nodes.new("GeometryNodeDistributePointsInVolume")
    distrib.location = (-200, 0)
    distrib.mode     = "DENSITY_RANDOM"
    distrib.inputs["Density"].default_value = float(N_SPHERES) / (COLUMN_HEIGHT * math.pi * (RADIUS_BASE * 1.5) ** 2)

    obj_info = nodes.new("GeometryNodeObjectInfo"); obj_info.location = (-200, -250)
    obj_info.inputs["Object"].default_value = sphere
    obj_info.transform_space = "RELATIVE"

    rnd_scale = nodes.new("FunctionNodeRandomValue"); rnd_scale.location = (-200, -400)
    rnd_scale.data_type = "FLOAT"
    rnd_scale.inputs["Min"].default_value = 1.0 - RADIUS_VAR / RADIUS_BASE
    rnd_scale.inputs["Max"].default_value = 1.0 + RADIUS_VAR / RADIUS_BASE

    mesh_to_vol = nodes.new("GeometryNodeMeshToVolume"); mesh_to_vol.location = (-400, 0)
    mesh_to_vol.inputs["Density"].default_value    = 1.0
    mesh_to_vol.inputs["Voxel Size"].default_value = 0.1

    instance = nodes.new("GeometryNodeInstanceOnPoints"); instance.location = (200, 0)
    realize  = nodes.new("GeometryNodeRealizeInstances"); realize.location  = (400, 0)

    links.new(in_n.outputs["Geometry"],        mesh_to_vol.inputs["Mesh"])
    links.new(mesh_to_vol.outputs["Volume"],   distrib.inputs["Volume"])
    links.new(distrib.outputs["Points"],       instance.inputs["Points"])
    links.new(obj_info.outputs["Geometry"],    instance.inputs["Instance"])
    links.new(rnd_scale.outputs["Value"],      instance.inputs["Scale"])
    links.new(instance.outputs["Instances"],   realize.inputs["Geometry"])
    links.new(realize.outputs["Geometry"],     out_n.inputs["Geometry"])

    cyl.data.materials.append(mirror_material("Column_Mat"))
    return cyl


def build_python_column(offset_x=0.0):
    """Pure Python loop approach."""
    rng = random.Random(7)
    col = bpy.data.collections.new("Kapoor_Python")
    bpy.context.scene.collection.children.link(col)

    mat = mirror_material("Mirror_Py")
    objs = []
    for i in range(N_SPHERES):
        t = i / max(N_SPHERES - 1, 1)
        z = t * COLUMN_HEIGHT
        r = rng.uniform(RADIUS_BASE - RADIUS_VAR, RADIUS_BASE + RADIUS_VAR)
        # Pack spheres touching — slight overlap for cluster effect
        x_off = rng.uniform(-RADIUS_BASE * 0.5, RADIUS_BASE * 0.5) + offset_x
        y_off = rng.uniform(-RADIUS_BASE * 0.5, RADIUS_BASE * 0.5)

        bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=(x_off, y_off, z))
        sph = bpy.context.active_object
        sph.name = f"Kapoor_Py_{i:03d}"
        sph.data.materials.append(mat)
        for c in list(sph.users_collection):
            c.objects.unlink(sph)
        col.objects.link(sph)
        objs.append(sph)

    return objs


def main():
    clear_scene()

    all_objs = []
    if MODE in ("geonodes", "both"):
        col_gn = build_geonodes_column(offset_x=-3.0 if MODE == "both" else 0.0)
        all_objs.append(col_gn)
    if MODE in ("python", "both"):
        py_objs = build_python_column(offset_x=3.0 if MODE == "both" else 0.0)
        all_objs.extend(py_objs)

    for o in all_objs:
        o.select_set(True)
    if all_objs:
        bpy.context.view_layer.objects.active = all_objs[0]

    # Camera — looking slightly up at the column
    cam_x = 0 if MODE != "both" else 0
    bpy.ops.object.camera_add(location=(cam_x + 6, -4, COLUMN_HEIGHT * 0.6))
    cam = bpy.context.active_object
    cam.rotation_euler = (math.radians(75), 0, math.radians(55))
    bpy.context.scene.camera = cam

    bpy.ops.object.light_add(type="SUN", location=(5, -5, 8))
    sun = bpy.context.active_object
    sun.data.energy = 3.0
    sun.rotation_euler = (math.radians(40), 0, math.radians(20))

    bpy.ops.object.light_add(type="AREA", location=(-4, 3, 5))
    fill = bpy.context.active_object
    fill.data.energy = 150
    fill.data.size   = 6.0

    world = bpy.context.scene.world
    world.use_nodes = True
    bg = world.node_tree.nodes["Background"]
    bg.inputs["Color"].default_value    = (0.9, 0.9, 0.95, 1.0)
    bg.inputs["Strength"].default_value = 1.0

    bpy.context.scene.render.engine       = "CYCLES"
    bpy.context.scene.cycles.samples      = 256
    bpy.context.scene.render.resolution_x = 1920
    bpy.context.scene.render.resolution_y = 1080

    print(f"[kapoor_tall_tree] Scene ready — mode: {MODE}")
    print(f"  Spheres      : {N_SPHERES}  |  Height: {COLUMN_HEIGHT} m")
    print(f"  Radius base  : {RADIUS_BASE}  ±  {RADIUS_VAR}")
    print("  Tip: set MIRROR_FINISH=False for a matte version.")
    load_into_editor()


if __name__ == "__main__":
    main()
