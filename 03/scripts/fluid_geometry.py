"""
fluid_geometry.py — Fluid Simulation in Blender's Geometry Nodes
=================================================================
Chapter 3 · Art Between Matter and Code · Gianpiero Moioli
Apress / Springer Nature, 2025 · CC BY-NC 4.0

Companion to §3.6.1.5 and Figure 18.

Simulates continuous, flowing deformation within a procedural system.
A Scene Time node drives noise-based displacement, producing animated
ripples and distortions that evoke organic movement or molten material.

The resulting form exists between digital sculpture and dynamic
performance — like a digital echo of traditional casting or fluid
modeling. Inspired by the dynamic energy of Breath of Fire (Ch. 8).

Usage:
    Blender 5.1 → Scripting → Run Script (Alt+P)
    or: blender --python fluid_geometry.py

Parameters (edit CONFIG below):
    NOISE_SCALE    — spatial frequency of the fluid deformation
    NOISE_STRENGTH — amplitude of the displacement
    SPEED          — animation speed (noise offset per frame)
    SUBDIVISIONS   — icosphere subdivision level (mesh density)
    EXPORT_GLB     — True = export as GLB for virtual exhibition platforms
    EXPORT_PATH    — output path (empty = next to .blend)
"""

import bpy
import math
import os

# ── CONFIG ────────────────────────────────────────────────────────────────────
NOISE_SCALE    = 1.5
NOISE_STRENGTH = 0.35
SPEED          = 0.02    # noise W offset per frame
SUBDIVISIONS   = 4
EXPORT_GLB     = False
EXPORT_PATH    = ""
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


def make_material(name, color=(0.3, 0.55, 0.8), roughness=0.2, metallic=0.4):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Roughness"].default_value  = roughness
    bsdf.inputs["Metallic"].default_value   = metallic
    return mat


def build_fluid_nodes(obj):
    """Build a noise-based fluid deformation in Geometry Nodes."""
    mod = obj.modifiers.new("FluidGeo", type="NODES")
    ng  = bpy.data.node_groups.new("FluidGeometry", type="GeometryNodeTree")
    mod.node_group = ng

    ng.interface.new_socket("Geometry", in_out="INPUT",  socket_type="NodeSocketGeometry")
    ng.interface.new_socket("Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")

    nodes = ng.nodes
    links = ng.links

    in_n  = nodes.new("NodeGroupInput");  in_n.location  = (-800, 0)
    out_n = nodes.new("NodeGroupOutput"); out_n.location = (600, 0)

    # Position → noise input
    pos   = nodes.new("GeometryNodeInputPosition"); pos.location   = (-600, -200)

    # Scene Time → W offset (drives animation)
    time  = nodes.new("GeometryNodeInputSceneTime"); time.location  = (-600, -400)
    fmul  = nodes.new("ShaderNodeMath");             fmul.location  = (-400, -400)
    fmul.operation = "MULTIPLY"
    fmul.inputs[1].default_value = SPEED

    # 4D Noise Texture
    noise = nodes.new("ShaderNodeTexNoise"); noise.location = (-200, -200)
    noise.noise_dimensions = "4D"
    noise.inputs["Scale"].default_value   = NOISE_SCALE
    noise.inputs["Detail"].default_value  = 6.0
    noise.inputs["Roughness"].default_value = 0.6

    # Map range: remap noise 0–1 → -0.5–0.5 (bidirectional displacement)
    mrange = nodes.new("ShaderNodeMapRange"); mrange.location = (0, -200)
    mrange.inputs["From Min"].default_value = 0.0
    mrange.inputs["From Max"].default_value = 1.0
    mrange.inputs["To Min"].default_value   = -0.5
    mrange.inputs["To Max"].default_value   = 0.5

    # Normal → displacement direction
    normal = nodes.new("GeometryNodeInputNormal"); normal.location = (0, -400)

    # Scale normal by noise value
    vscale = nodes.new("ShaderNodeVectorMath"); vscale.location = (200, -200)
    vscale.operation = "SCALE"

    # Set Position
    set_pos = nodes.new("GeometryNodeSetPosition"); set_pos.location = (400, 0)

    # Offset = normal * noise_amplitude
    offset_scale = nodes.new("ShaderNodeVectorMath"); offset_scale.location = (200, -350)
    offset_scale.operation = "SCALE"
    offset_scale.inputs["Scale"].default_value = NOISE_STRENGTH

    links.new(in_n.outputs["Geometry"],         set_pos.inputs["Geometry"])
    links.new(pos.outputs["Position"],           noise.inputs["Vector"])
    links.new(time.outputs["Frame"],             fmul.inputs[0])
    links.new(fmul.outputs["Value"],             noise.inputs["W"])
    links.new(noise.outputs["Fac"],              mrange.inputs["Value"])
    links.new(normal.outputs["Normal"],          offset_scale.inputs[0])
    links.new(mrange.outputs["Result"],          offset_scale.inputs["Scale"])
    links.new(offset_scale.outputs["Vector"],    set_pos.inputs["Offset"])
    links.new(set_pos.outputs["Geometry"],       out_n.inputs["Geometry"])


def main():
    clear_scene()

    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=SUBDIVISIONS, radius=1.2,
                                          location=(0, 0, 0))
    obj = bpy.context.active_object
    obj.name = "FluidForm"
    obj.data.materials.append(make_material("Fluid_Mat"))

    build_fluid_nodes(obj)

    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj

    # Animation range
    bpy.context.scene.frame_start = 1
    bpy.context.scene.frame_end   = 120

    # Camera
    bpy.ops.object.camera_add(location=(3.5, -3.5, 2.5))
    cam = bpy.context.active_object
    cam.rotation_euler = (math.radians(60), 0, math.radians(45))
    bpy.context.scene.camera = cam

    bpy.ops.object.light_add(type="SUN", location=(4, -4, 6))
    sun = bpy.context.active_object
    sun.data.energy = 3.0
    sun.rotation_euler = (math.radians(45), 0, math.radians(30))

    bpy.ops.object.light_add(type="AREA", location=(-3, 2, 4))
    fill = bpy.context.active_object
    fill.data.energy = 100
    fill.data.size   = 4.0

    world = bpy.context.scene.world
    world.use_nodes = True
    bg = world.node_tree.nodes["Background"]
    bg.inputs["Color"].default_value    = (0.05, 0.06, 0.1, 1.0)
    bg.inputs["Strength"].default_value = 0.5

    bpy.context.scene.render.engine       = "CYCLES"
    bpy.context.scene.cycles.samples      = 128
    bpy.context.scene.render.resolution_x = 1920
    bpy.context.scene.render.resolution_y = 1080

    if EXPORT_GLB:
        path = EXPORT_PATH.strip() if EXPORT_PATH.strip() else os.path.join(
            bpy.path.abspath("//") or os.path.expanduser("~"),
            "fluid_geometry.glb"
        )
        bpy.ops.export_scene.gltf(filepath=path, export_selected=True,
                                  export_format="GLB")
        print(f"  GLB exported: {path}")

    print("[fluid_geometry] Scene ready — 120 frames animation.")
    print(f"  Noise scale  : {NOISE_SCALE}  |  Strength: {NOISE_STRENGTH}")
    print(f"  Speed        : {SPEED} (noise W offset per frame)")
    print("  Press Space to play the fluid deformation.")
    print("  Tip: set EXPORT_GLB=True to export for virtual exhibitions.")
    load_into_editor()


if __name__ == "__main__":
    main()
