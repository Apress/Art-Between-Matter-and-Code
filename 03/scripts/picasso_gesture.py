"""
picasso_gesture.py — Picasso's Procedural Gesture
==================================================
Chapter 3 · Art Between Matter and Code · Gianpiero Moioli
Apress / Springer Nature, 2025 · CC BY-NC 4.0

Companion to §3.6.2.

A Bézier curve drawn freely by hand is transformed through Geometry
Nodes into a three-dimensional volumetric object — a direct digital
echo of Picasso's 1949 light drawings with Gjon Mili.

The Trim Curve function animates the unfolding of the line, as if
it were being traced in real time. The gesture becomes sculpture:
from an immediate stroke, a fluid structure emerges.

This script creates a simplified version of the Picasso.blend scene.
(The .blend includes the Starlight Atmosphere add-on for environment;
this script uses standard Cycles world nodes instead.)

Usage:
    Blender 5.1 → Scripting → Run Script (Alt+P)
    or: blender --python picasso_gesture.py

Parameters (edit CONFIG below):
    BEVEL_DEPTH    — thickness of the curve profile (volumetric line)
    ANIMATE        — True = animate the Trim Curve (line draws itself)
    LIGHT_COLOR    — emissive color of the gesture (RGB 0–1)
    EMISSION_STR   — emission strength (glowing light trace)
    CURVE_POINTS   — number of points defining the gesture path
"""

import bpy
import math
import os
import random

# ── CONFIG ────────────────────────────────────────────────────────────────────
BEVEL_DEPTH  = 0.04
ANIMATE      = True
LIGHT_COLOR  = (1.0, 0.85, 0.4)   # warm white-gold, like a torch
EMISSION_STR = 8.0
CURVE_POINTS = 12   # control points of the gesture curve
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


def make_emissive_material(name, color, strength):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    out   = nodes.new("ShaderNodeOutputMaterial"); out.location   = (300, 0)
    emit  = nodes.new("ShaderNodeEmission");       emit.location  = (0, 0)
    emit.inputs["Color"].default_value    = (*color, 1.0)
    emit.inputs["Strength"].default_value = strength
    links.new(emit.outputs["Emission"], out.inputs["Surface"])
    return mat


def build_gesture_curve():
    """Create a freehand Bézier curve simulating a light drawing."""
    rng = random.Random(1949)   # reference to Picasso's year
    curve_data = bpy.data.curves.new("GesturePath", type="CURVE")
    curve_data.dimensions    = "3D"
    curve_data.bevel_depth   = BEVEL_DEPTH
    curve_data.bevel_mode    = "ROUND"
    curve_data.use_fill_caps = True

    spline = curve_data.splines.new("BEZIER")
    spline.bezier_points.add(CURVE_POINTS - 1)

    # Generate a looping, expressive gesture in 3D space
    for i, bp in enumerate(spline.bezier_points):
        t     = i / max(CURVE_POINTS - 1, 1)
        angle = t * math.pi * 3.5
        r     = 0.8 + 0.6 * math.sin(t * math.pi * 2)
        x     = r * math.cos(angle) + rng.uniform(-0.2, 0.2)
        y     = r * math.sin(angle) + rng.uniform(-0.2, 0.2)
        z     = t * 1.5 + rng.uniform(-0.1, 0.1)
        bp.co = (x, y, z)
        # Auto handles
        bp.handle_left_type  = "AUTO"
        bp.handle_right_type = "AUTO"

    obj = bpy.data.objects.new("PicassoGesture", curve_data)
    bpy.context.scene.collection.objects.link(obj)
    obj.data.materials.append(
        make_emissive_material("LightTrace", LIGHT_COLOR, EMISSION_STR)
    )

    # Trim Curve geometry node for animation (draws itself)
    if ANIMATE:
        mod = obj.modifiers.new("TrimCurve", type="NODES")
        ng  = bpy.data.node_groups.new("TrimGesture", type="GeometryNodeTree")
        mod.node_group = ng

        ng.interface.new_socket("Geometry", in_out="INPUT",  socket_type="NodeSocketGeometry")
        ng.interface.new_socket("Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")

        nodes = ng.nodes
        links = ng.links
        in_n  = nodes.new("NodeGroupInput");  in_n.location  = (-400, 0)
        out_n = nodes.new("NodeGroupOutput"); out_n.location = (200, 0)
        trim  = nodes.new("GeometryNodeTrimCurve"); trim.location = (0, 0)
        trim.mode = "FACTOR"
        trim.inputs["Start"].default_value = 0.0
        trim.inputs["End"].default_value   = 1.0

        links.new(in_n.outputs["Geometry"],  trim.inputs["Curve"])
        links.new(trim.outputs["Curve"],     out_n.inputs["Geometry"])

        # Animate End from 0 → 1 over 80 frames
        scene = bpy.context.scene
        scene.frame_start = 1
        scene.frame_end   = 80
        scene.frame_set(1)
        trim.inputs["End"].default_value = 0.0
        trim.inputs["End"].keyframe_insert("default_value", frame=1)
        scene.frame_set(80)
        trim.inputs["End"].default_value = 1.0
        trim.inputs["End"].keyframe_insert("default_value", frame=80)
        scene.frame_set(1)

    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    return obj


def setup_dark_world():
    """Dark world — simulate the darkened room of Picasso's experiment."""
    world = bpy.context.scene.world
    world.use_nodes = True
    bg = world.node_tree.nodes["Background"]
    bg.inputs["Color"].default_value    = (0.01, 0.01, 0.02, 1.0)
    bg.inputs["Strength"].default_value = 1.0


def main():
    clear_scene()
    obj = build_gesture_curve()
    setup_dark_world()

    bpy.ops.object.camera_add(location=(3, -3, 2))
    cam = bpy.context.active_object
    cam.rotation_euler = (math.radians(65), 0, math.radians(45))
    bpy.context.scene.camera = cam

    # Minimal point light — the trace itself is emissive
    bpy.ops.object.light_add(type="POINT", location=(0, 0, 3))
    pt = bpy.context.active_object
    pt.data.energy = 5.0
    pt.data.color  = LIGHT_COLOR

    bpy.context.scene.render.engine       = "CYCLES"
    bpy.context.scene.cycles.samples      = 256
    bpy.context.scene.render.resolution_x = 1920
    bpy.context.scene.render.resolution_y = 1080

    print("[picasso_gesture] Scene ready.")
    print(f"  Curve points : {CURVE_POINTS}  |  Bevel: {BEVEL_DEPTH}")
    if ANIMATE:
        print("  Animation    : 80 frames — the gesture draws itself.")
        print("  Press Space to watch the light trace unfold.")
    print("  Tip: open Picasso.blend for the full atmospheric version.")
    load_into_editor()


if __name__ == "__main__":
    main()
