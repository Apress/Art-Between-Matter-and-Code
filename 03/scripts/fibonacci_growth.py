"""
fibonacci_growth.py — Fibonacci-Based Organic Growth
======================================================
Chapter 3 · Art Between Matter and Code · Gianpiero Moioli
Apress / Springer Nature, 2025 · CC BY-NC 4.0

Companion to §3.3 and Figure 10.

Generates a Fibonacci / phyllotaxis spiral by placing mesh instances
along a golden-angle distribution — the mathematical principle found
in sunflower seeds, pinecones, and nautilus shells.

Each element is rotated by the golden angle (≈ 137.5°) and scaled
according to its radial distance, producing a self-organizing spiral
that expands organically in 3D space.

Usage:
    Blender 5.1 → Scripting → Run Script (Alt+P)
    or: blender --python fibonacci_growth.py

Parameters (edit CONFIG below):
    N_ELEMENTS     — number of instances in the spiral
    SCALE_BASE     — base scale of each element
    HEIGHT_FACTOR  — vertical rise per element
    NOISE_AMOUNT   — random jitter added to positions (0 = pure math)
    MODULE         — "SPHERE" | "CUBE" | "CONE"
"""

import bpy
import bmesh
import math
import os

# ── CONFIG ────────────────────────────────────────────────────────────────────
N_ELEMENTS    = 120
SCALE_BASE    = 0.08
HEIGHT_FACTOR = 0.04
NOISE_AMOUNT  = 0.015   # positional jitter (0 = perfect Fibonacci)
MODULE        = "SPHERE" # "SPHERE" | "CUBE" | "CONE"
# ──────────────────────────────────────────────────────────────────────────────

GOLDEN_ANGLE = math.pi * (3.0 - math.sqrt(5.0))   # ≈ 2.39994 rad ≈ 137.508°


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


def make_material(name, color, roughness=0.4, metallic=0.1):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Roughness"].default_value  = roughness
    bsdf.inputs["Metallic"].default_value   = metallic
    return mat


def add_module(index, location, scale, col):
    """Add a single module instance at the given location."""
    if MODULE == "SPHERE":
        bpy.ops.mesh.primitive_uv_sphere_add(radius=scale, location=location)
    elif MODULE == "CUBE":
        bpy.ops.mesh.primitive_cube_add(size=scale * 1.8, location=location)
    elif MODULE == "CONE":
        bpy.ops.mesh.primitive_cone_add(radius1=scale, depth=scale * 2, location=location)
    obj = bpy.context.active_object
    obj.name = f"Fib_{index:04d}"
    # Rotate each element by its golden-angle step
    obj.rotation_euler.z = index * GOLDEN_ANGLE

    # Gradient colour: warm centre → cool outer
    t = index / max(N_ELEMENTS - 1, 1)
    color = (0.9 - t * 0.5, 0.6 - t * 0.2, 0.3 + t * 0.5)
    obj.data.materials.append(make_material(f"FibMat_{index}", color))

    for c in list(obj.users_collection):
        c.objects.unlink(obj)
    col.objects.link(obj)
    return obj


def build_fibonacci_spiral():
    col = bpy.data.collections.new("FibonacciGrowth")
    bpy.context.scene.collection.children.link(col)

    import random
    rng = random.Random(42)

    all_objs = []
    for i in range(N_ELEMENTS):
        angle  = i * GOLDEN_ANGLE
        radius = math.sqrt(i / max(N_ELEMENTS, 1)) * 2.5
        x = radius * math.cos(angle) + rng.uniform(-NOISE_AMOUNT, NOISE_AMOUNT)
        y = radius * math.sin(angle) + rng.uniform(-NOISE_AMOUNT, NOISE_AMOUNT)
        z = i * HEIGHT_FACTOR

        # Scale grows with radius
        scale = SCALE_BASE * (0.4 + 0.6 * (i / N_ELEMENTS))

        obj = add_module(i, (x, y, z), scale, col)
        all_objs.append(obj)

    return all_objs, col


def main():
    clear_scene()

    objs, col = build_fibonacci_spiral()

    # Select all for framing
    for o in objs:
        o.select_set(True)
    if objs:
        bpy.context.view_layer.objects.active = objs[-1]

    # Camera
    bpy.ops.object.camera_add(location=(4, -4, 4))
    cam = bpy.context.active_object
    cam.rotation_euler = (math.radians(55), 0, math.radians(45))
    bpy.context.scene.camera = cam

    bpy.ops.object.light_add(type="SUN", location=(3, -4, 6))
    sun = bpy.context.active_object
    sun.data.energy = 3.5
    sun.rotation_euler = (math.radians(40), 0, math.radians(30))

    bpy.ops.object.light_add(type="AREA", location=(-3, 2, 5))
    fill = bpy.context.active_object
    fill.data.energy = 100
    fill.data.size   = 5.0

    bpy.context.scene.render.engine       = "CYCLES"
    bpy.context.scene.cycles.samples      = 128
    bpy.context.scene.render.resolution_x = 1920
    bpy.context.scene.render.resolution_y = 1080

    print(f"[fibonacci_growth] Spiral built: {N_ELEMENTS} elements.")
    print(f"  Golden angle : {math.degrees(GOLDEN_ANGLE):.3f}°")
    print(f"  Module       : {MODULE}")
    print("  Tip: increase N_ELEMENTS or change HEIGHT_FACTOR and re-run (Alt+P).")
    load_into_editor()


if __name__ == "__main__":
    main()
