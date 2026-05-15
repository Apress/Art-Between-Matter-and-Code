"""
reproduction_matrix.py — The Aura and Its Loss in Blender
==========================================================
Chapter 1 · Art Between Matter and Code · Gianpiero Moioli
Apress / Springer Nature, 2025 · CC BY-NC 4.0

Companion to §1.x (Benjamin's Aura and the Age of Mechanical Reproduction).

Visualises Walter Benjamin's thesis in three dimensions: a row of objects
where each step represents one generation of reproduction. The leftmost
object is the unique original — pristine, with full "aura". Moving right,
Musgrave noise displacement increases progressively; by the last object the
original form has dissolved into a degraded, unrecognisable copy.

Material colour follows the same gradient: warm ochre (aura present) →
cool blue-grey (aura dissolved) — mapping temperature to presence.

Usage:
    Blender 5.x → Scripting workspace → Run Script (Alt+P)
    or: blender --background --python reproduction_matrix.py

Parameters (edit the CONFIG block below):
    NUM_COPIES   — total objects in the matrix (original + N-1 reproductions)
    BASE_FORM    — starting shape: "sphere" | "cube" | "torus"
    MAX_NOISE    — maximum displacement strength on the last copy (0.0 = none)
    SPACING      — distance between objects in Blender units
    SEED         — random seed for reproducible noise variation across copies
    SHOW_LABELS  — add index text above each object (requires font data)
"""

import bpy
import bmesh
import math
import os
import random

# ── CONFIG ────────────────────────────────────────────────────────────────────
NUM_COPIES  = 7        # total objects: 1 original + 6 reproductions
BASE_FORM   = "sphere" # "sphere" | "cube" | "torus"
MAX_NOISE   = 0.55     # displacement strength at the last copy
SPACING     = 1.6      # distance between objects
SEED        = 17
# ──────────────────────────────────────────────────────────────────────────────


def load_into_editor():
    """Load this script into Blender's text editor (no context override needed)."""
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


# ── Colour interpolation ──────────────────────────────────────────────────────

# Warm ochre (original, aura intact) → cool blue-grey (copy, aura dissolved)
COLOUR_ORIGIN = (0.78, 0.62, 0.32)   # warm amber / golden
COLOUR_COPY   = (0.30, 0.38, 0.55)   # cold blue-grey


def lerp_colour(t):
    """Linearly interpolate between COLOUR_ORIGIN and COLOUR_COPY at t ∈ [0,1]."""
    r = COLOUR_ORIGIN[0] + t * (COLOUR_COPY[0] - COLOUR_ORIGIN[0])
    g = COLOUR_ORIGIN[1] + t * (COLOUR_COPY[1] - COLOUR_ORIGIN[1])
    b = COLOUR_ORIGIN[2] + t * (COLOUR_COPY[2] - COLOUR_ORIGIN[2])
    return (r, g, b)


def make_material(index, t):
    """Create a Principled BSDF material interpolated between original and copy."""
    mat  = bpy.data.materials.new(f"Aura_{index:02d}")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    col  = lerp_colour(t)
    bsdf.inputs["Base Color"].default_value = (*col, 1.0)
    # Roughness also increases as the form degrades
    bsdf.inputs["Roughness"].default_value  = 0.25 + t * 0.55
    bsdf.inputs["Metallic"].default_value   = max(0.0, 0.4 - t * 0.4)
    return mat


# ── Base form ─────────────────────────────────────────────────────────────────

def add_base_form(location):
    if BASE_FORM == "cube":
        bpy.ops.mesh.primitive_cube_add(size=0.9, location=location)
    elif BASE_FORM == "torus":
        bpy.ops.mesh.primitive_torus_add(
            major_radius=0.45, minor_radius=0.18, location=location
        )
    else:  # sphere (default)
        bpy.ops.mesh.primitive_uv_sphere_add(
            radius=0.5, segments=32, ring_count=24, location=location
        )
    return bpy.context.active_object


# ── Displacement ──────────────────────────────────────────────────────────────

def add_subdivision(obj, levels):
    """Add Subdivision Surface so displacement has vertices to act on."""
    sub = obj.modifiers.new("Subdiv", type="SUBSURF")
    sub.levels        = levels
    sub.render_levels = levels


def add_noise_displacement(obj, strength, seed_offset):
    """Add a Musgrave displacement that erodes the original form."""
    rng  = random.Random(SEED + seed_offset * 7)
    disp = obj.modifiers.new("AuraDegradation", type="DISPLACE")
    tex  = bpy.data.textures.new(f"AuraNoise_{seed_offset:02d}", type="MUSGRAVE")
    tex.musgrave_type    = "HYBRID_MULTIFRACTAL"
    tex.noise_scale      = 0.6 + rng.uniform(-0.1, 0.2)
    tex.noise_intensity  = 1.0
    tex.octaves          = 6
    disp.texture         = tex
    disp.strength        = strength
    disp.texture_coords  = "LOCAL"
    # Random phase offset so each copy differs from the previous
    disp.texture_coords_object = None


# ── Main construction ─────────────────────────────────────────────────────────

def build_matrix(col):
    """Build the full reproduction matrix and return all objects."""
    total_width = (NUM_COPIES - 1) * SPACING
    objects = []

    for i in range(NUM_COPIES):
        t   = i / max(NUM_COPIES - 1, 1)        # 0.0 = original, 1.0 = last copy
        x   = -total_width / 2.0 + i * SPACING
        loc = (x, 0.0, 0.0)

        obj      = add_base_form(loc)
        obj.name = f"Gen_{i:02d}_{'Original' if i == 0 else f'Copy{i}'}"

        # Subdivision before displacement (more verts = finer noise detail)
        subdiv_levels = 2 if i == 0 else min(2, 1 + (i > NUM_COPIES // 2))
        add_subdivision(obj, subdiv_levels)

        if i > 0:
            # Noise strength grows non-linearly — accelerates toward the end
            strength = MAX_NOISE * (t ** 1.4)
            add_noise_displacement(obj, strength, seed_offset=i)

        obj.data.materials.append(make_material(i, t))

        col.objects.link(obj)
        bpy.context.scene.collection.objects.unlink(obj)
        objects.append(obj)

    return objects


# ── Ground plane ──────────────────────────────────────────────────────────────

def add_ground(col, num, spacing):
    total_width = (num - 1) * spacing
    bpy.ops.mesh.primitive_plane_add(size=total_width + 2.0, location=(0, 0, -0.52))
    ground = bpy.context.active_object
    ground.name = "Ground"
    mat = bpy.data.materials.new("Ground_Mat")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value  = (0.88, 0.86, 0.82, 1.0)
    bsdf.inputs["Roughness"].default_value   = 0.9
    col.objects.link(ground)
    bpy.context.scene.collection.objects.unlink(ground)


# ── Camera & lighting ─────────────────────────────────────────────────────────

def setup_render(num, spacing):
    total_width = (num - 1) * spacing
    cam_dist    = total_width * 0.9 + 2.0

    bpy.ops.object.camera_add(location=(0, -cam_dist, 1.8))
    cam = bpy.context.active_object
    cam.rotation_euler = (math.radians(78), 0, 0)
    bpy.context.scene.camera = cam

    # Key light — warm, from upper-left
    bpy.ops.object.light_add(type="AREA", location=(-total_width * 0.4, -2, 4))
    key = bpy.context.active_object
    key.data.energy = 600
    key.data.size   = 3
    key.data.color  = (1.0, 0.92, 0.78)      # warm
    key.rotation_euler = (math.radians(50), 0, math.radians(-25))

    # Fill light — cold, from right
    bpy.ops.object.light_add(type="AREA", location=(total_width * 0.6, -1, 2))
    fill = bpy.context.active_object
    fill.data.energy = 180
    fill.data.size   = 4
    fill.data.color  = (0.75, 0.85, 1.0)     # cool blue

    # World: neutral gradient
    world = bpy.context.scene.world
    if world is None:
        world = bpy.data.worlds.new("World")
        bpy.context.scene.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes.get("Background")
    if bg:
        bg.inputs["Color"].default_value    = (0.72, 0.72, 0.75, 1.0)
        bg.inputs["Strength"].default_value = 0.4

    bpy.context.scene.render.engine          = "CYCLES"
    bpy.context.scene.cycles.samples         = 128
    bpy.context.scene.render.resolution_x    = 1920
    bpy.context.scene.render.resolution_y    = 600


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    clear_scene()

    col = new_collection("ReproductionMatrix")

    objects = build_matrix(col)
    add_ground(col, NUM_COPIES, SPACING)
    setup_render(NUM_COPIES, SPACING)

    print(f"[reproduction_matrix] Done — {NUM_COPIES} generations, "
          f"form='{BASE_FORM}', max_noise={MAX_NOISE}, spacing={SPACING}")
    print(f"  Gen 00 = pristine original  /  Gen {NUM_COPIES-1:02d} = fully degraded copy")
    print("  Colour: warm amber (aura) → cold blue (no aura)")
    load_into_editor()


if __name__ == "__main__":
    main()
