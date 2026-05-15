"""
material_spectrum.py — The Material-Digital Continuum in Blender
================================================================
Chapter 1 · Art Between Matter and Code · Gianpiero Moioli
Apress / Springer Nature, 2025 · CC BY-NC 4.0

Companion to §1.2 (From Neoclassical Chisels to Digital Code).

The same sculptural form rendered across five material states,
from the physical to the purely digital:

    1. White marble   — Neoclassical origin: translucent, carved, luminous
    2. Terracotta     — the bozzetto, the sketch in clay before the final cast
    3. Bronze         — the monumental cast, metallic permanence
    4. Digital glass  — the virtual object: transparent, weightless, exact
    5. Wireframe      — pure structure: code without matter, geometry without surface

Left to right, the row maps the arc from Canova's studio to a 3D printer —
the central argument of Chapter 1.

Usage:
    Blender 5.x → Scripting workspace → Run Script (Alt+P)
    or: blender --background --python material_spectrum.py

Parameters (edit CONFIG below):
    BASE_FORM  — sculpted shape: "sphere" | "cube" | "torus"
    SPACING    — distance between objects in Blender units
    SEED       — random seed for marble / terracotta surface variation
"""

import bpy
import bmesh
import math
import os
import random

# ── CONFIG ────────────────────────────────────────────────────────────────────
BASE_FORM = "sphere"   # "sphere" | "cube" | "torus"
SPACING   = 1.8        # distance between objects
SEED      = 7
# ──────────────────────────────────────────────────────────────────────────────

# Material definitions: (name, base_color, roughness, metallic)
# extended properties set individually in make_material()
SPECTRUM = [
    ("Marble",     (0.92, 0.90, 0.88), 0.22, 0.0),
    ("Terracotta", (0.68, 0.33, 0.20), 0.92, 0.0),
    ("Bronze",     (0.40, 0.26, 0.12), 0.38, 1.0),
    ("Glass",      (0.86, 0.92, 0.96), 0.04, 0.0),
    ("Wireframe",  (0.20, 0.55, 1.00), 0.0,  0.0),
]


def load_into_editor():
    try:
        filepath = os.path.abspath(__file__)
    except NameError:
        return
    name = os.path.basename(filepath)
    text = bpy.data.texts[name] if name in bpy.data.texts else bpy.data.texts.load(filepath)
    for ws in bpy.data.workspaces:
        for screen in ws.screens:
            for area in screen.areas:
                if area.type == 'TEXT_EDITOR':
                    area.spaces.active.text = text
    for ws in bpy.data.workspaces:
        if "Script" in ws.name:
            bpy.context.window.workspace = ws
            break


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()
    for col in list(bpy.data.collections):
        bpy.data.collections.remove(col)


def new_collection(name):
    col = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(col)
    return col


# ── Principled BSDF helper (Blender 4/5 renamed some inputs) ─────────────────

def bsdf_set(bsdf, key_new, key_old, value):
    if key_new in bsdf.inputs:
        bsdf.inputs[key_new].default_value = value
    elif key_old in bsdf.inputs:
        bsdf.inputs[key_old].default_value = value


# ── Base form ─────────────────────────────────────────────────────────────────

def add_base_form(location):
    if BASE_FORM == "cube":
        bpy.ops.mesh.primitive_cube_add(size=0.85, location=location)
    elif BASE_FORM == "torus":
        bpy.ops.mesh.primitive_torus_add(
            major_radius=0.42, minor_radius=0.17, location=location
        )
    else:  # sphere
        bpy.ops.mesh.primitive_uv_sphere_add(
            radius=0.5, segments=48, ring_count=32, location=location
        )
    return bpy.context.active_object


# ── Material builders ─────────────────────────────────────────────────────────

def make_marble(name, color):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Roughness"].default_value  = 0.22
    # Subsurface scattering — gives marble its inner luminosity
    bsdf_set(bsdf, "Subsurface Weight", "Subsurface", 0.12)
    bsdf_set(bsdf, "Subsurface Radius", "Subsurface Radius",
             (0.80, 0.60, 0.50))
    return mat


def make_terracotta(name, color):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Roughness"].default_value  = 0.92
    return mat


def make_bronze(name, color):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Roughness"].default_value  = 0.38
    bsdf.inputs["Metallic"].default_value   = 1.0
    return mat


def make_glass(name, color):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Roughness"].default_value  = 0.04
    bsdf_set(bsdf, "Transmission Weight", "Transmission", 1.0)
    bsdf_set(bsdf, "IOR", "IOR", 1.52)
    return mat


def make_wireframe_mat(name, color):
    """Emission material for the wireframe object."""
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    out  = nodes.new("ShaderNodeOutputMaterial")
    emit = nodes.new("ShaderNodeEmission")
    emit.inputs["Color"].default_value    = (*color, 1.0)
    emit.inputs["Strength"].default_value = 2.0
    links.new(emit.outputs["Emission"], out.inputs["Surface"])
    return mat


MATERIAL_BUILDERS = [make_marble, make_terracotta, make_bronze, make_glass, make_wireframe_mat]


# ── Surface variation (marble veining, terracotta roughness) ──────────────────

def add_displacement(obj, strength, scale, seed_offset):
    rng  = random.Random(SEED + seed_offset)
    sub  = obj.modifiers.new("Subdiv", type="SUBSURF")
    sub.levels = 3

    disp = obj.modifiers.new("SurfaceVariation", type="DISPLACE")
    tex  = bpy.data.textures.new(f"SurfNoise_{seed_offset}", type="MUSGRAVE")
    tex.musgrave_type  = "FBM"
    tex.noise_scale    = scale
    tex.octaves        = 5
    disp.texture       = tex
    disp.strength      = strength
    disp.texture_coords = "LOCAL"


def add_wireframe_mod(obj, thickness):
    wf = obj.modifiers.new("Wireframe", type="WIREFRAME")
    wf.thickness       = thickness
    wf.use_even_offset = True
    wf.use_relative_offset = False


# ── Ground ────────────────────────────────────────────────────────────────────

def add_ground(col, total_width):
    bpy.ops.mesh.primitive_plane_add(size=total_width + 2.0, location=(0, 0, -0.52))
    ground      = bpy.context.active_object
    ground.name = "Ground"
    mat  = bpy.data.materials.new("Ground_Mat")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (0.88, 0.86, 0.82, 1.0)
    bsdf.inputs["Roughness"].default_value  = 0.85
    ground.data.materials.append(mat)
    col.objects.link(ground)
    bpy.context.scene.collection.objects.unlink(ground)


# ── Camera & lighting ─────────────────────────────────────────────────────────

def setup_render(total_width):
    cam_dist = total_width * 0.6 + 2.5

    bpy.ops.object.camera_add(location=(0, -cam_dist, 1.0))
    cam = bpy.context.active_object
    cam.rotation_euler = (math.radians(82), 0, 0)
    bpy.context.scene.camera = cam

    # Key — warm, upper left (studio light)
    bpy.ops.object.light_add(type="AREA", location=(-total_width * 0.4, -2, 4))
    key = bpy.context.active_object
    key.data.energy = 700
    key.data.size   = 4
    key.data.color  = (1.0, 0.94, 0.82)
    key.rotation_euler = (math.radians(48), 0, math.radians(-20))

    # Fill — cooler, right side
    bpy.ops.object.light_add(type="AREA", location=(total_width * 0.5, -1.5, 2))
    fill = bpy.context.active_object
    fill.data.energy = 200
    fill.data.size   = 5
    fill.data.color  = (0.80, 0.88, 1.0)

    # World background: dark, near-black — makes wireframe and glass pop
    world = bpy.context.scene.world
    if world is None:
        world = bpy.data.worlds.new("World")
        bpy.context.scene.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes.get("Background")
    if bg:
        bg.inputs["Color"].default_value    = (0.06, 0.06, 0.07, 1.0)
        bg.inputs["Strength"].default_value = 0.2

    bpy.context.scene.render.engine       = "CYCLES"
    bpy.context.scene.cycles.samples      = 128
    bpy.context.scene.render.resolution_x = 1920
    bpy.context.scene.render.resolution_y = 600


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    clear_scene()
    col = new_collection("MaterialSpectrum")

    n = len(SPECTRUM)
    total_width = (n - 1) * SPACING

    for i, (mat_name, color, roughness, metallic) in enumerate(SPECTRUM):
        x   = -total_width / 2.0 + i * SPACING
        obj = add_base_form((x, 0.0, 0.0))
        obj.name = f"{i+1:02d}_{mat_name}"

        # Build material with the appropriate builder
        mat = MATERIAL_BUILDERS[i](mat_name, color)
        obj.data.materials.append(mat)

        # Per-material modifiers
        if mat_name == "Marble":
            add_displacement(obj, strength=0.012, scale=0.25, seed_offset=i)
        elif mat_name == "Terracotta":
            add_displacement(obj, strength=0.032, scale=0.55, seed_offset=i)
        elif mat_name == "Wireframe":
            add_wireframe_mod(obj, thickness=0.012)

        col.objects.link(obj)
        bpy.context.scene.collection.objects.unlink(obj)

    add_ground(col, total_width)
    setup_render(total_width)

    labels = " → ".join(name for name, *_ in SPECTRUM)
    print(f"[material_spectrum] Done — {n} states: {labels}")
    print(f"  form='{BASE_FORM}', spacing={SPACING}")
    load_into_editor()


if __name__ == "__main__":
    main()
