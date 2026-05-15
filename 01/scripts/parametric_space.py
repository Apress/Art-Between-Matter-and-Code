"""
parametric_space.py — Space as Generative Field in Blender
===========================================================
Chapter 1 · Art Between Matter and Code · Gianpiero Moioli
Apress / Springer Nature, 2025 · CC BY-NC 4.0

Companion script to fig_01_spazialismo_fontana.blend.

The chapter describes space not as a container but as an active, generative
field — energy that propagates, bends, and responds. This script builds that
concept procedurally: a grid of points deformed by a sinusoidal field, whose
parameters can be tuned to shift from ordered geometry to organic expansion.

Conceptual mapping:
    GRID_DENSITY    → resolution of the "spatial fabric"
    WAVE_AMPLITUDE  → intensity of spatial energy
    WAVE_FREQUENCY  → frequency of spatial oscillation
    FIELD_PROFILE   → "radial" (concentric, Fontana-like) |
                      "linear" (directional, like a cut) |
                      "turbulent" (procedural noise)
    EMIT_PARTICLES  → add particle system for energy propagation effect
    SOLIDIFY        → thicken the surface (for 3D printing / fabrication)

Usage:
    Blender 5.x → Scripting workspace → Run Script (Alt+P)
    or: blender --background my_scene.blend --python parametric_space.py

    To use with the existing Spazio.blend:
        1. Open fig_01_spazialismo_fontana.blend
        2. Load this script in the Scripting workspace
        3. Run — it adds a new "ParametricSpace" object without touching
           the existing scene geometry.
"""

import bpy
import bmesh
import math
import os
import mathutils

# ── CONFIG ────────────────────────────────────────────────────────────────────
GRID_DENSITY   = 40          # vertices per side (40 = 1600 points)
GRID_SIZE      = 4.0         # total extent in Blender units
WAVE_AMPLITUDE = 0.35        # height of field deformation
WAVE_FREQUENCY = 2.5         # oscillation cycles across the grid
FIELD_PROFILE  = "radial"    # "radial" | "linear" | "turbulent"
NOISE_SCALE    = 1.8         # turbulence detail scale (used when FIELD_PROFILE="turbulent")
NOISE_DEPTH    = 4           # octaves of noise detail
SOLIDIFY       = True        # add thickness for fabrication / printing
SOLIDIFY_THICK = 0.02        # solidify thickness in Blender units
EMIT_PARTICLES = False       # particle system for energy-propagation visualization
# ──────────────────────────────────────────────────────────────────────────────


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
        pass   # already running from the text editor — nothing to do


def remove_defaults():
    """Remove only Blender's startup defaults (Cube, Camera, Light).
    Any other geometry already in the scene (e.g. FontanaCanvas from
    fontana_cut.py) is preserved — this script is designed to add to
    an existing scene, not replace it."""
    for name in ("Cube", "Camera", "Light"):
        if name in bpy.data.objects:
            obj = bpy.data.objects[name]
            bpy.data.objects.remove(obj, do_unlink=True)


def remove_existing(name):
    """Remove a previous run's ParametricSpace object so re-running is clean."""
    if name in bpy.data.objects:
        obj = bpy.data.objects[name]
        bpy.data.meshes.remove(obj.data, do_unlink=True)


def field_z(x, y, profile, amplitude, frequency, noise_scale, noise_depth):
    """Return the Z displacement for a given (x, y) point."""
    if profile == "radial":
        r = math.sqrt(x ** 2 + y ** 2)
        return amplitude * math.cos(r * frequency * math.pi)

    elif profile == "linear":
        return amplitude * math.sin(x * frequency * math.pi)

    else:  # turbulent
        vec = mathutils.Vector((x * noise_scale, y * noise_scale, 0.0))
        raw = mathutils.noise.fractal(vec, 2.0, 0.5, noise_depth)
        return amplitude * raw


def build_mesh(density, size, profile, amplitude, frequency, noise_scale, noise_depth):
    bm = bmesh.new()

    half = size / 2.0
    step = size / (density - 1)

    verts = []
    for row in range(density):
        row_verts = []
        for col in range(density):
            x = -half + col * step
            y = -half + row * step
            z = field_z(x, y, profile, amplitude, frequency, noise_scale, noise_depth)
            row_verts.append(bm.verts.new((x, y, z)))
        verts.append(row_verts)

    for row in range(density - 1):
        for col in range(density - 1):
            v00 = verts[row][col]
            v10 = verts[row + 1][col]
            v11 = verts[row + 1][col + 1]
            v01 = verts[row][col + 1]
            bm.faces.new([v00, v10, v11, v01])

    bm.normal_update()
    return bm


def make_material(profile):
    mat = bpy.data.materials.new("ParametricSpace_Mat")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    nodes.clear()

    output  = nodes.new("ShaderNodeOutputMaterial")
    bsdf    = nodes.new("ShaderNodeBsdfPrincipled")
    geo     = nodes.new("ShaderNodeNewGeometry")
    mapping = nodes.new("ShaderNodeMapping")
    ramp    = nodes.new("ShaderNodeValToRGB")

    # Map Z-normal to colour: deep = blue-violet, crest = warm white
    ramp.color_ramp.elements[0].color = (0.05, 0.07, 0.35, 1.0)
    ramp.color_ramp.elements[1].color = (0.92, 0.88, 0.78, 1.0)

    links.new(geo.outputs["Normal"],   mapping.inputs["Vector"])
    links.new(mapping.outputs["Vector"], ramp.inputs["Fac"])
    links.new(ramp.outputs["Color"],   bsdf.inputs["Base Color"])
    bsdf.inputs["Metallic"].default_value   = 0.0
    bsdf.inputs["Roughness"].default_value  = 0.4
    bsdf.inputs["Specular IOR Level"].default_value = 0.3
    links.new(bsdf.outputs["BSDF"],    output.inputs["Surface"])

    output.location  = (600, 0)
    bsdf.location    = (300, 0)
    geo.location     = (-300, 0)
    mapping.location = (-100, 0)
    ramp.location    = (50, 0)

    return mat


def add_solidify(obj, thickness):
    mod = obj.modifiers.new("Solidify", type="SOLIDIFY")
    mod.thickness = thickness
    mod.offset = 0.0


def add_particles(obj):
    mod = obj.modifiers.new("SpaceField_Particles", type="PARTICLE_SYSTEM")
    ps  = mod.particle_system.settings
    ps.count          = 500
    ps.lifetime       = 60
    ps.emit_from      = "FACE"
    ps.normal_factor  = 0.8
    ps.use_rotations  = True
    ps.render_type    = "HALO"
    ps.particle_size  = 0.02


def add_camera_and_light(size):
    cam_loc = (0, -size * 2.0, size * 1.2)
    bpy.ops.object.camera_add(location=cam_loc)
    cam = bpy.context.active_object
    cam.rotation_euler = (math.radians(60), 0, 0)
    bpy.context.scene.camera = cam

    bpy.ops.object.light_add(type="SUN", location=(size, -size, size * 2))
    sun = bpy.context.active_object
    sun.data.energy = 3.0
    sun.rotation_euler = (math.radians(45), 0, math.radians(30))


def main():
    remove_defaults()            # remove startup Cube/Camera/Light only
    obj_name = "ParametricSpace"
    remove_existing(obj_name)    # remove previous run if re-executing

    bm = build_mesh(
        GRID_DENSITY, GRID_SIZE,
        FIELD_PROFILE, WAVE_AMPLITUDE, WAVE_FREQUENCY,
        NOISE_SCALE, NOISE_DEPTH,
    )

    mesh = bpy.data.meshes.new(obj_name)
    bm.to_mesh(mesh)
    bm.free()

    obj = bpy.data.objects.new(obj_name, mesh)
    bpy.context.scene.collection.objects.link(obj)
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

    mat = make_material(FIELD_PROFILE)
    obj.data.materials.append(mat)

    if SOLIDIFY:
        add_solidify(obj, SOLIDIFY_THICK)

    if EMIT_PARTICLES:
        add_particles(obj)

    if not bpy.context.scene.camera:
        add_camera_and_light(GRID_SIZE)

    print(f"[parametric_space] Done — profile='{FIELD_PROFILE}', "
          f"grid={GRID_DENSITY}×{GRID_DENSITY}, "
          f"amplitude={WAVE_AMPLITUDE}, frequency={WAVE_FREQUENCY}")
    load_into_editor()   # open script in Scripting tab so CONFIG is editable


if __name__ == "__main__":
    main()
