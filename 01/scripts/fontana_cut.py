"""
fontana_cut.py — Procedural Fontana Cut in Blender
===================================================
Chapter 1 · Art Between Matter and Code · Gianpiero Moioli
Apress / Springer Nature, 2025 · CC BY-NC 4.0

Reinterpretation of Lucio Fontana's "Concetto Spaziale" as a parametric
boolean operation. Each cut is a modular aperture — the canvas becomes a
field of controlled voids, echoing Fontana's idea that the cut opens space
rather than destroying the surface.

Usage:
    Open Blender (4.x), go to the Scripting workspace, paste or load this
    file, then press Run Script (Alt+P).

    Alternatively, from the terminal:
        blender --background --python fontana_cut.py

Parameters (edit the CONFIG block below):
    NUM_CUTS    — number of cuts (Fontana typically used 1–7)
    CUT_ANGLE   — rotation of each cut from horizontal, in degrees
    CUT_DEPTH   — depth of the cut into the canvas plane (Z extrusion)
    CUT_WIDTH   — thickness of each cutting blade
    CUT_LENGTH  — length of each cut relative to canvas width (0.0–1.0)
    CANVAS_SIZE — size of the canvas plane in Blender units
    SPACING     — spacing mode: "even" | "random" | "golden"
    SEED        — random seed for reproducible randomised layouts
"""

import bpy
import bmesh
import math
import random
from mathutils import Vector, Euler

# ── CONFIG ────────────────────────────────────────────────────────────────────
NUM_CUTS    = 5
CUT_ANGLE   = 10.0      # degrees from horizontal, applied as slight tilt
CUT_DEPTH   = 0.08      # depth the blade protrudes through the canvas
CUT_WIDTH   = 0.015     # blade thickness (thin = sharp Fontana cut)
CUT_LENGTH  = 0.72      # fraction of canvas width (0.0–1.0)
CANVAS_SIZE = 2.0       # canvas plane half-extent (total: 2 × CANVAS_SIZE)
SPACING     = "even"    # "even" | "random" | "golden"
SEED        = 42
# ──────────────────────────────────────────────────────────────────────────────


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()
    for col in bpy.data.collections:
        bpy.data.collections.remove(col)


def new_collection(name):
    col = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(col)
    return col


def make_canvas(col, size):
    # Use a thin box, not a plane: boolean DIFFERENCE requires closed (manifold) geometry.
    # A flat plane has zero volume and produces only edge artefacts, not real cuts.
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
    canvas = bpy.context.active_object
    canvas.name = "FontanaCanvas"
    canvas.dimensions = (size * 2, size * 2, 0.025)   # thin but solid
    col.objects.link(canvas)
    bpy.context.scene.collection.objects.unlink(canvas)

    mat = bpy.data.materials.new("Canvas_Material")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (0.92, 0.88, 0.78, 1.0)  # raw linen
    bsdf.inputs["Roughness"].default_value = 0.85
    canvas.data.materials.append(mat)
    return canvas


def cut_positions(num, size, mode, seed):
    """Return Y positions for each cut along the canvas height."""
    half = size * 0.9
    if mode == "even":
        step = (2 * half) / (num + 1)
        return [-half + step * (i + 1) for i in range(num)]
    elif mode == "golden":
        phi = (1 + math.sqrt(5)) / 2
        positions = []
        for i in range(num):
            y = -half + (2 * half) * ((i * phi) % 1.0)
            positions.append(y)          # fix: must be inside the loop
        return sorted(positions)
    else:  # random
        random.seed(seed)
        return sorted([random.uniform(-half, half) for _ in range(num)])


def make_blade_mesh(half_len, width, depth, curve_amp, rng):
    """
    Build a bmesh cutter that mimics a real Fontana cut:
      - Spine follows a gentle sine curve (the cut is never perfectly straight)
      - Width tapers with a sine envelope (thin at the tips, wider at centre)
      - Left and right edges carry independent noise (the 'slabbrato' / frayed look)
    The result is a closed manifold volume suitable for Boolean DIFFERENCE.
    """
    bm  = bmesh.new()
    N   = 32                          # segments along the cut
    phi = rng.uniform(0, math.pi)     # random phase for the spine curve

    tl, tr, bl, br = [], [], [], []   # top-left / top-right / bottom-left / bottom-right

    for i in range(N + 1):
        t = i / N                                           # 0 → 1 along the cut
        x = -half_len + t * 2 * half_len

        # --- spine: gentle sine that shifts the whole cut sideways ---
        spine = curve_amp * math.sin(t * math.pi * 2 + phi)

        # --- width: zero at both tips, maximum at centre ---
        taper = math.sin(t * math.pi)                      # 0 at tips, 1 at centre
        w     = width * (0.12 + 0.88 * taper)

        # --- edge noise: proportional to local width so tips stay sharp ---
        fray  = (w / 2) * 0.80                             # max ±80 % of half-width
        nl    = rng.uniform(-fray, fray)
        nr    = rng.uniform(-fray, fray)

        yl = spine - w / 2 + nl
        yr = spine + w / 2 + nr
        if yr < yl + 0.001:                                # guarantee left stays left
            yr = yl + 0.001

        tl.append(bm.verts.new((x, yl,  depth)))
        tr.append(bm.verts.new((x, yr,  depth)))
        bl.append(bm.verts.new((x, yl, -depth)))
        br.append(bm.verts.new((x, yr, -depth)))

    bm.verts.ensure_lookup_table()

    for i in range(N):
        # face winding chosen so normals point outward on every side
        bm.faces.new([tl[i], tl[i+1], tr[i+1], tr[i]])   # top    (+Z)
        bm.faces.new([bl[i], br[i], br[i+1], bl[i+1]])   # bottom (-Z)
        bm.faces.new([tl[i], bl[i], bl[i+1], tl[i+1]])   # left   (-Y)
        bm.faces.new([tr[i], tr[i+1], br[i+1], br[i]])   # right  (+Y)

    bm.faces.new([tl[0], tr[0], br[0], bl[0]])            # start cap (-X)
    bm.faces.new([tl[N], bl[N], br[N], tr[N]])            # end cap   (+X)

    bm.normal_update()
    return bm


def make_blade(col, index, y_pos, canvas_size, length, width, depth, angle_deg):
    """Create an organic Fontana-cut cutter: curved, tapered, frayed."""
    rng        = random.Random(SEED + index * 13)
    half_len   = canvas_size * length
    curve_amp  = canvas_size * rng.uniform(0.025, 0.07)  # 2.5–7 % of canvas → visible arc

    bm   = make_blade_mesh(half_len, width, depth, curve_amp, rng)
    mesh = bpy.data.meshes.new(f"Cut_{index:02d}_mesh")
    bm.to_mesh(mesh)
    bm.free()

    blade                = bpy.data.objects.new(f"Cut_{index:02d}", mesh)
    blade.location       = (0, y_pos, 0)
    blade.rotation_euler = Euler((0, 0, math.radians(angle_deg)), "XYZ")

    col.objects.link(blade)                        # keep it in Fontana_Cuts collection

    mat = bpy.data.materials.new(f"Blade_{index:02d}")
    mat.use_nodes = True
    mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0, 0, 0, 1)
    blade.data.materials.append(mat)
    return blade


def apply_boolean_cut(canvas, blade):
    mod = canvas.modifiers.new(name=f"Bool_{blade.name}", type="BOOLEAN")
    mod.operation = "DIFFERENCE"
    mod.object = blade
    mod.solver = "EXACT"    # FAST/FLOAT is unreliable on thin geometry; EXACT gives clean cuts

    # modifier_apply requires the object to be BOTH active AND selected
    bpy.ops.object.select_all(action="DESELECT")
    bpy.context.view_layer.objects.active = canvas
    canvas.select_set(True)
    bpy.ops.object.mode_set(mode="OBJECT")
    bpy.ops.object.modifier_apply(modifier=mod.name)


def add_canvas_material_displacement(canvas):
    """Subtle surface displacement to simulate fabric texture."""
    mod = canvas.modifiers.new("FabricTexture", type="DISPLACE")
    tex = bpy.data.textures.new("FabricNoise", type="MUSGRAVE")
    tex.musgrave_type = "FBM"
    tex.noise_scale = 0.3
    tex.noise_intensity = 0.5
    mod.texture = tex
    mod.strength = 0.004
    mod.texture_coords = "LOCAL"


def add_camera_and_light(canvas_size):
    bpy.ops.object.camera_add(location=(0, -canvas_size * 3.5, canvas_size * 0.8))
    cam = bpy.context.active_object
    cam.rotation_euler = Euler((math.radians(75), 0, 0), "XYZ")
    bpy.context.scene.camera = cam

    bpy.ops.object.light_add(type="AREA", location=(canvas_size, -canvas_size, canvas_size * 2))
    light = bpy.context.active_object
    light.data.energy = 400
    light.data.size = canvas_size * 2
    light.rotation_euler = Euler((math.radians(45), 0, math.radians(30)), "XYZ")


def main():
    clear_scene()

    col_canvas = new_collection("Fontana_Canvas")
    col_cuts   = new_collection("Fontana_Cuts")

    canvas = make_canvas(col_canvas, CANVAS_SIZE)

    positions = cut_positions(NUM_CUTS, CANVAS_SIZE, SPACING, SEED)

    blades = []
    for i, y in enumerate(positions):
        blade = make_blade(
            col_cuts, i,
            y_pos      = y,
            canvas_size = CANVAS_SIZE,
            length      = CUT_LENGTH,
            width       = CUT_WIDTH,
            depth       = CUT_DEPTH,
            angle_deg   = CUT_ANGLE if i % 2 == 0 else -CUT_ANGLE,
        )
        blades.append(blade)

    for blade in blades:
        apply_boolean_cut(canvas, blade)

    for blade in blades:
        bpy.data.objects.remove(blade, do_unlink=True)

    add_canvas_material_displacement(canvas)
    add_camera_and_light(CANVAS_SIZE)

    bpy.context.scene.render.engine = "CYCLES"
    bpy.context.scene.cycles.samples = 128

    print(f"[fontana_cut] Done — {NUM_CUTS} parametric cuts applied.")
    print(f"  spacing={SPACING}, angle=±{CUT_ANGLE}°, length={CUT_LENGTH*100:.0f}% of canvas")


if __name__ == "__main__":
    main()
