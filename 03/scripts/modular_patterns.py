"""
modular_patterns.py — Repeating Patterns with Geometry Nodes
=============================================================
Chapter 3 · Art Between Matter and Code · Gianpiero Moioli
Apress / Springer Nature, 2025 · CC BY-NC 4.0

Companion to §3.6.1.2 and Figure 15.

Uses Geometry Nodes instancing to distribute a module object across a
surface with procedural density control (noise-driven), random scale
and rotation — producing results from ordered grids to organic clusters.

Node graph built via Python:
    Group Input (Geometry)
    → Distribute Points on Faces  (density driven by Noise Texture)
    → Instance on Points          (module = Sphere, random scale/rotation)
    → Realize Instances
    → Group Output

Usage:
    Blender 5.1 → Scripting → Run Script (Alt+P)
    or: blender --python modular_patterns.py

Parameters (edit CONFIG below):
    DENSITY_MAX    — maximum instance density (points per m²)
    SCALE_MIN      — minimum random scale of each instance
    SCALE_MAX      — maximum random scale
    NOISE_SCALE    — noise texture scale for density variation
    MODULE_RADIUS  — radius of the instanced sphere module
"""

import bpy
import math
import os

# ── CONFIG ────────────────────────────────────────────────────────────────────
DENSITY_MAX   = 2.0    # max points per m²
SCALE_MIN     = 0.08
SCALE_MAX     = 0.22
NOISE_SCALE   = 0.3    # spatial frequency of density noise
MODULE_RADIUS = 0.12   # radius of the sphere module
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


def make_material(name, color, roughness=0.5, metallic=0.0):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Roughness"].default_value  = roughness
    bsdf.inputs["Metallic"].default_value   = metallic
    return mat


def build_geometry_nodes(grid, sphere):
    """Build the Geometry Nodes modifier on the grid."""
    mod = grid.modifiers.new("GeoNodes_Patterns", type="NODES")
    ng  = bpy.data.node_groups.new("ModularPatterns", type="GeometryNodeTree")
    mod.node_group = ng

    # Interface
    ng.interface.new_socket("Geometry", in_out="INPUT",  socket_type="NodeSocketGeometry")
    ng.interface.new_socket("Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")

    nodes = ng.nodes
    links = ng.links

    # I/O
    in_node  = nodes.new("NodeGroupInput");  in_node.location  = (-800, 0)
    out_node = nodes.new("NodeGroupOutput"); out_node.location = (600, 0)

    # Position → Vector Math (scale for noise)
    pos  = nodes.new("GeometryNodeInputPosition"); pos.location = (-800, -200)
    vmath = nodes.new("ShaderNodeVectorMath")
    vmath.operation = "SCALE"; vmath.location = (-600, -200)
    vmath.inputs["Scale"].default_value = NOISE_SCALE

    # Noise Texture → Map Range → density
    noise = nodes.new("ShaderNodeTexNoise"); noise.location = (-400, -200)
    noise.inputs["Scale"].default_value  = 1.0
    noise.inputs["Detail"].default_value = 4.0

    mrange = nodes.new("ShaderNodeMapRange"); mrange.location = (-200, -200)
    mrange.inputs["From Min"].default_value = 0.0
    mrange.inputs["From Max"].default_value = 1.0
    mrange.inputs["To Min"].default_value   = 0.0
    mrange.inputs["To Max"].default_value   = DENSITY_MAX

    # Distribute Points on Faces
    distrib = nodes.new("GeometryNodeDistributePointsOnFaces")
    distrib.location = (0, 0)
    distrib.distribute_method = "RANDOM"

    # Object Info (module sphere)
    obj_info = nodes.new("GeometryNodeObjectInfo"); obj_info.location = (-200, -400)
    obj_info.inputs["Object"].default_value = sphere
    obj_info.transform_space = "RELATIVE"

    # Random scale
    rnd_scale = nodes.new("FunctionNodeRandomValue"); rnd_scale.location = (-200, -550)
    rnd_scale.data_type = "FLOAT"
    rnd_scale.inputs["Min"].default_value = SCALE_MIN
    rnd_scale.inputs["Max"].default_value = SCALE_MAX

    # Instance on Points
    instance = nodes.new("GeometryNodeInstanceOnPoints"); instance.location = (200, 0)

    # Realize Instances
    realize = nodes.new("GeometryNodeRealizeInstances"); realize.location = (400, 0)

    # Links
    links.new(in_node.outputs["Geometry"],      distrib.inputs["Mesh"])
    links.new(pos.outputs["Position"],          vmath.inputs[0])
    links.new(vmath.outputs["Vector"],          noise.inputs["Vector"])
    links.new(noise.outputs["Fac"],             mrange.inputs["Value"])
    links.new(mrange.outputs["Result"],         distrib.inputs["Density"])
    links.new(distrib.outputs["Points"],        instance.inputs["Points"])
    links.new(obj_info.outputs["Geometry"],     instance.inputs["Instance"])
    links.new(rnd_scale.outputs["Value"],       instance.inputs["Scale"])
    links.new(instance.outputs["Instances"],    realize.inputs["Geometry"])
    links.new(realize.outputs["Geometry"],      out_node.inputs["Geometry"])


def main():
    clear_scene()

    # Module sphere (hidden from render, used as instance source)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=MODULE_RADIUS, location=(10, 0, 0))
    sphere = bpy.context.active_object
    sphere.name = "Module_Sphere"
    sphere.hide_render = True
    sphere.data.materials.append(
        make_material("Module_Mat", (0.4, 0.55, 0.8), roughness=0.3, metallic=0.2)
    )

    # Base grid surface
    bpy.ops.mesh.primitive_grid_add(x_subdivisions=20, y_subdivisions=20,
                                    size=4, location=(0, 0, 0))
    grid = bpy.context.active_object
    grid.name = "Pattern_Grid"
    grid.data.materials.append(
        make_material("Grid_Mat", (0.85, 0.82, 0.75), roughness=0.8)
    )

    build_geometry_nodes(grid, sphere)

    grid.select_set(True)
    bpy.context.view_layer.objects.active = grid

    # Camera & light
    bpy.ops.object.camera_add(location=(0, -6, 5))
    cam = bpy.context.active_object
    cam.rotation_euler = (math.radians(50), 0, 0)
    bpy.context.scene.camera = cam

    bpy.ops.object.light_add(type="SUN", location=(4, -4, 7))
    sun = bpy.context.active_object
    sun.data.energy = 4.0
    sun.rotation_euler = (math.radians(40), 0, math.radians(20))

    bpy.context.scene.render.engine       = "CYCLES"
    bpy.context.scene.cycles.samples      = 128
    bpy.context.scene.render.resolution_x = 1920
    bpy.context.scene.render.resolution_y = 1080

    print("[modular_patterns] Scene ready.")
    print(f"  Density max  : {DENSITY_MAX}  |  Scale: {SCALE_MIN} – {SCALE_MAX}")
    print(f"  Noise scale  : {NOISE_SCALE}")
    print("  Tip: increase DENSITY_MAX or change NOISE_SCALE and re-run (Alt+P).")
    load_into_editor()


if __name__ == "__main__":
    main()
