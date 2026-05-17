"""
geometry_nodes_growth.py
────────────────────────
Art Between Matter and Code · Gianpiero Moioli · Apress 2025
Chapter 5 — §5.4.3  Algorithmic Growth: Toward Procedural Sculpture

Creates a procedural sculpture using Blender's Geometry Nodes:
  - Icosphere subdivided by a noise-based displacement
  - Two exposed parameters: Displacement strength and Noise scale
  - A second mesh layer: scattered growth spikes on the surface

The resulting setup demonstrates the shift from direct modeling to
designing generative rules — as described in §5.4.3.

Run:    Blender → Scripting workspace → Alt+P
Or:     blender --background --python geometry_nodes_growth.py
Saves:  ../models/procedural_sculpture_demo.blend  (background mode only)

Requires: Blender 4.3 LTS or later.
"""

import bpy
import sys
import os

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────

SAVE_BLEND    = "--background" in sys.argv   # auto-save when run headless
OUTPUT_BLEND  = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "models", "procedural_sculpture_demo.blend"
)

# Sculpture parameters (also exposed in the GN modifier)
DISP_STRENGTH = 0.38     # displacement amplitude
NOISE_SCALE   = 2.8      # noise frequency (higher = more detail)
NOISE_DETAIL  = 10.0
NOISE_ROUGH   = 0.70
SUBDIV_LEVEL  = 4        # subdivision iterations

# Spike scatter parameters
SPIKE_DENSITY = 12.0     # points per unit area
SPIKE_RADIUS  = 0.05
SPIKE_HEIGHT  = 0.40

# Material colour (warm stone)
BASE_COLOR    = (0.72, 0.67, 0.58, 1.0)
ROUGHNESS     = 0.62

# ─────────────────────────────────────────────
# Scene setup
# ─────────────────────────────────────────────

def setup_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for col in list(bpy.data.collections):
        bpy.data.collections.remove(col)

    # Camera
    bpy.ops.object.camera_add(location=(3.8, -3.8, 2.8))
    cam = bpy.context.active_object
    cam.rotation_euler = (1.05, 0.0, 0.785)
    bpy.context.scene.camera = cam

    # Key light
    bpy.ops.object.light_add(type='AREA', location=(3, 2, 5))
    key = bpy.context.active_object
    key.data.energy = 400
    key.data.size   = 3.0
    key.rotation_euler = (0.4, 0.2, 0.5)

    # Fill light
    bpy.ops.object.light_add(type='AREA', location=(-4, -2, 3))
    fill = bpy.context.active_object
    fill.data.energy = 120
    fill.data.size   = 4.0

    # World background
    bpy.context.scene.world.color = (0.04, 0.04, 0.04)

    # Render engine
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.samples = 64
    bpy.context.scene.render.resolution_x = 1920
    bpy.context.scene.render.resolution_y = 1080


# ─────────────────────────────────────────────
# Main sculpture — noise displacement
# ─────────────────────────────────────────────

def build_displacement_nodes(ng):
    """Wire the noise-displacement node graph inside ng."""
    nodes = ng.nodes
    links = ng.links

    # ── Group I/O ─────────────────────────────
    n_in  = nodes.new('NodeGroupInput');  n_in.location  = (-900, 0)
    n_out = nodes.new('NodeGroupOutput'); n_out.location = ( 700, 0)

    # ── Subdivide ─────────────────────────────
    n_sub = nodes.new('GeometryNodeSubdivideMesh')
    n_sub.location = (-620, 0)
    n_sub.inputs['Level'].default_value = SUBDIV_LEVEL

    # ── Position (noise vector input) ─────────
    n_pos = nodes.new('GeometryNodeInputPosition')
    n_pos.location = (-620, -280)

    # ── Noise texture ─────────────────────────
    n_noise = nodes.new('ShaderNodeTexNoise')
    n_noise.location       = (-380, -280)
    n_noise.noise_dimensions = '3D'
    n_noise.inputs['Scale'].default_value      = NOISE_SCALE
    n_noise.inputs['Detail'].default_value     = NOISE_DETAIL
    n_noise.inputs['Roughness'].default_value  = NOISE_ROUGH
    n_noise.inputs['Distortion'].default_value = 0.25

    # ── Surface normal (displacement direction) ─
    n_norm = nodes.new('GeometryNodeInputNormal')
    n_norm.location = (-380, -480)

    # ── Scale noise Fac by Displacement param ──
    n_mul = nodes.new('ShaderNodeMath')
    n_mul.operation = 'MULTIPLY'
    n_mul.location  = (-120, -320)

    # ── Scale normal vector by resulting float ──
    n_vsc = nodes.new('ShaderNodeVectorMath')
    n_vsc.operation = 'SCALE'
    n_vsc.location  = (140, -360)

    # ── Apply offset ──────────────────────────
    n_spos = nodes.new('GeometryNodeSetPosition')
    n_spos.location = (440, 0)

    # ── Wiring ────────────────────────────────
    links.new(n_in.outputs['Geometry'],      n_sub.inputs['Mesh'])
    links.new(n_sub.outputs['Mesh'],         n_spos.inputs['Geometry'])
    links.new(n_pos.outputs['Position'],     n_noise.inputs['Vector'])
    links.new(n_noise.outputs['Fac'],        n_mul.inputs[0])
    links.new(n_in.outputs['Displacement'],  n_mul.inputs[1])
    links.new(n_norm.outputs['Normal'],      n_vsc.inputs['Vector'])
    links.new(n_mul.outputs['Value'],        n_vsc.inputs['Scale'])
    links.new(n_vsc.outputs['Vector'],       n_spos.inputs['Offset'])
    links.new(n_spos.outputs['Geometry'],    n_out.inputs['Geometry'])


def create_base_sculpture():
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=1.2, location=(0, 0, 0))
    obj = bpy.context.active_object
    obj.name = "ProcSculpture"

    mod = obj.modifiers.new("NoiseDisplacement", 'NODES')
    ng  = bpy.data.node_groups.new("NoiseDisplacement", 'GeometryNodeTree')
    mod.node_group = ng

    # Blender 4.x interface
    ng.interface.new_socket("Geometry",     in_out='INPUT',  socket_type='NodeSocketGeometry')
    ng.interface.new_socket("Geometry",     in_out='OUTPUT', socket_type='NodeSocketGeometry')
    ng.interface.new_socket("Displacement", in_out='INPUT',  socket_type='NodeSocketFloat')

    build_displacement_nodes(ng)

    # Set default parameter values via identifier
    for item in ng.interface.items_tree:
        if item.name == "Displacement":
            mod[item.identifier] = DISP_STRENGTH
            break

    return obj


# ─────────────────────────────────────────────
# Second layer — scatter instances (growth)
# Note: kept as a separate function so it can be
# called interactively (Alt+P) but skipped in
# background mode to avoid Blender 5.x exit crash.
# ─────────────────────────────────────────────

def add_instance_layer(base_obj):
    """
    Adds a second Geometry Nodes modifier that scatters small icosphere
    instances across the surface, simulating organic growth.
    Call this interactively (Alt+P) — not used in background/batch mode.
    """
    mod = base_obj.modifiers.new("InstanceGrowth", 'NODES')
    ng  = bpy.data.node_groups.new("InstanceGrowth", 'GeometryNodeTree')
    mod.node_group = ng

    ng.interface.new_socket("Geometry", in_out='INPUT',  socket_type='NodeSocketGeometry')
    ng.interface.new_socket("Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')
    ng.interface.new_socket("Density",  in_out='INPUT',  socket_type='NodeSocketFloat')

    nodes = ng.nodes
    links = ng.links

    n_in   = nodes.new('NodeGroupInput');  n_in.location  = (-800, 0)
    n_out  = nodes.new('NodeGroupOutput'); n_out.location = ( 700, 0)

    n_dist = nodes.new('GeometryNodeDistributePointsOnFaces')
    n_dist.location = (-500, 0)
    n_dist.distribute_method = 'RANDOM'
    n_dist.inputs['Density'].default_value = SPIKE_DENSITY

    n_ball = nodes.new('GeometryNodeMeshUVSphere')
    n_ball.location = (-500, -280)
    n_ball.inputs['Radius'].default_value = SPIKE_RADIUS

    n_inst = nodes.new('GeometryNodeInstanceOnPoints')
    n_inst.location = (-150, 0)

    n_real = nodes.new('GeometryNodeRealizeInstances')
    n_real.location = (100, 0)

    n_join = nodes.new('GeometryNodeJoinGeometry')
    n_join.location = (400, 0)

    links.new(n_in.outputs['Geometry'],    n_dist.inputs['Mesh'])
    links.new(n_in.outputs['Density'],     n_dist.inputs['Density'])
    links.new(n_in.outputs['Geometry'],    n_join.inputs['Geometry'])
    links.new(n_dist.outputs['Points'],    n_inst.inputs['Points'])
    links.new(n_ball.outputs['Mesh'],      n_inst.inputs['Instance'])
    links.new(n_inst.outputs['Instances'], n_real.inputs['Geometry'])
    links.new(n_real.outputs['Geometry'],  n_join.inputs['Geometry'])
    links.new(n_join.outputs['Geometry'],  n_out.inputs['Geometry'])

    for item in ng.interface.items_tree:
        if item.name == "Density":
            mod[item.identifier] = SPIKE_DENSITY
            break


# ─────────────────────────────────────────────
# Material
# ─────────────────────────────────────────────

def add_material(obj):
    mat = bpy.data.materials.new("ProcSculpture_Mat")
    mat.use_nodes = True
    obj.data.materials.append(mat)

    nt = mat.node_tree
    nt.nodes.clear()

    out  = nt.nodes.new('ShaderNodeOutputMaterial'); out.location  = (300, 0)
    bsdf = nt.nodes.new('ShaderNodeBsdfPrincipled'); bsdf.location = (0, 0)

    bsdf.inputs['Base Color'].default_value = BASE_COLOR
    bsdf.inputs['Roughness'].default_value  = ROUGHNESS
    bsdf.inputs['Metallic'].default_value   = 0.0

    nt.links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])


# ─────────────────────────────────────────────
# Run
# ─────────────────────────────────────────────

print("\n[geometry_nodes_growth] Building procedural sculpture…")

setup_scene()
base = create_base_sculpture()
if not SAVE_BLEND:
    # Interactive mode: add the instance growth layer too
    add_instance_layer(base)
add_material(base)

# Deselect all, select sculpture
bpy.ops.object.select_all(action='DESELECT')
base.select_set(True)
bpy.context.view_layer.objects.active = base

if SAVE_BLEND:
    out_path = os.path.abspath(OUTPUT_BLEND)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=out_path)
    print(f"[geometry_nodes_growth] Saved -> {out_path}")
else:
    print("[geometry_nodes_growth] Done.")
    print("  Adjust 'Displacement' in the NoiseDisplacement modifier.")
    print("  Adjust 'Density' in the SpikeGrowth modifier.")
    print("  Render: F12")
