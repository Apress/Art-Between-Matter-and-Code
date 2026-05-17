"""
grease_pencil_video_paint.py
────────────────────────────
Art Between Matter and Code · Gianpiero Moioli · Apress 2025
Chapter 5 — §5.2 / §5.3  Hybrid Painting over AI Video

Sets up a Grease Pencil painting layer over the video already
loaded in the Video Sequence Editor.

After running (Alt+P):
  1. You are in Draw mode on the Grease Pencil object
  2. Use ← → arrows to move between frames
  3. Draw on each frame independently (or activate Auto-Key)
  4. Ctrl+F12 → renders video + GP paint composited together

Requires: Blender 4.3+, at least one Movie strip in the VSE.
"""

import bpy

# ─── Config ────────────────────────────────────────────────
GP_NAME        = "VideoPaint"
ONION_BEFORE   = 2      # ghost frames shown before current
ONION_AFTER    = 1      # ghost frames shown after current
ONION_OPACITY  = 0.4
# ───────────────────────────────────────────────────────────


def get_movie_strip():
    """Return the first Movie strip in the active scene VSE."""
    se = bpy.context.scene.sequence_editor
    if not se:
        return None
    for strip in se.sequences_all:
        if strip.type == 'MOVIE':
            return strip
    return None


def ensure_camera():
    """Return the scene camera, creating one if needed."""
    scene = bpy.context.scene
    if scene.camera:
        return scene.camera
    bpy.ops.object.camera_add(location=(0, 0, 10))
    cam = bpy.context.active_object
    scene.camera = cam
    return cam


def setup_camera_background(strip):
    """Load the strip's video as a camera background image."""
    filepath = bpy.path.abspath(strip.filepath)

    # Reuse clip if already loaded
    clip = next(
        (c for c in bpy.data.movieclips
         if bpy.path.abspath(c.filepath) == filepath),
        None
    )
    if clip is None:
        clip = bpy.data.movieclips.load(filepath)

    cam = ensure_camera()
    cam.data.show_background_images = True
    cam.data.background_images.clear()

    bg = cam.data.background_images.new()
    bg.source       = 'MOVIE_CLIP'
    bg.clip         = clip
    bg.alpha        = 1.0
    bg.display_depth = 'BACK'
    bg.frame_method  = 'FIT'

    return clip


def add_grease_pencil():
    """Add a Grease Pencil object with onion skinning enabled."""
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.gpencil_add(align='WORLD', location=(0, 0, 0), type='EMPTY')
    gp_obj = bpy.context.active_object
    gp_obj.name = GP_NAME

    gp = gp_obj.data
    gp.name = GP_NAME

    # Paint layer
    layer = gp.layers.new("Paint", set_active=True)
    layer.use_onion_skinning = True

    # Onion skinning
    gp.use_onion_skinning   = True
    gp.onion_mode           = 'RELATIVE'
    gp.ghost_before_range   = ONION_BEFORE
    gp.ghost_after_range    = ONION_AFTER
    gp.onion_factor         = ONION_OPACITY

    return gp_obj


def setup_compositor(clip):
    """
    Compositor graph:
        Movie Clip ──┐
                     ├─► Alpha Over ──► Composite
        Render Layers (GP) ──┘
    """
    scene = bpy.context.scene
    scene.use_nodes = True
    nt = scene.node_tree
    nt.nodes.clear()

    n_rl   = nt.nodes.new('CompositorNodeRLayers')
    n_clip = nt.nodes.new('CompositorNodeMovieClip')
    n_ao   = nt.nodes.new('CompositorNodeAlphaOver')
    n_out  = nt.nodes.new('CompositorNodeComposite')
    n_view = nt.nodes.new('CompositorNodeViewer')

    n_rl.location   = (-300,  120)
    n_clip.location = (-300, -120)
    n_ao.location   = (  80,    0)
    n_out.location  = ( 320,   80)
    n_view.location = ( 320,  -80)

    n_clip.clip             = clip
    n_ao.use_premultiply    = True

    nt.links.new(n_clip.outputs['Image'], n_ao.inputs[1])   # background = video
    nt.links.new(n_rl.outputs['Image'],   n_ao.inputs[2])   # foreground = GP paint
    nt.links.new(n_ao.outputs['Image'],   n_out.inputs['Image'])
    nt.links.new(n_ao.outputs['Image'],   n_view.inputs['Image'])


def enter_draw_mode(gp_obj):
    """Activate the GP object and enter Draw mode."""
    bpy.context.view_layer.objects.active = gp_obj
    gp_obj.select_set(True)
    # Blender 4.x: PAINT_GPENCIL; Blender 5.x: PAINT_GREASE_PENCIL
    for mode in ('PAINT_GPENCIL', 'PAINT_GREASE_PENCIL'):
        try:
            bpy.ops.object.mode_set(mode=mode)
            return
        except Exception:
            pass


def switch_to_layout():
    """Switch to Layout workspace (best for painting)."""
    for ws in bpy.data.workspaces:
        if ws.name == 'Layout':
            bpy.context.window.workspace = ws
            return


# ─── Main ──────────────────────────────────────────────────

print("\n[grease_pencil_video_paint] Starting…")

strip = get_movie_strip()
if strip is None:
    print("[ERROR] No Movie strip found in the VSE.")
    print("  Add → Movie in the Video Editing workspace, then re-run.")
else:
    scene = bpy.context.scene
    scene.frame_start = strip.frame_start
    scene.frame_end   = strip.frame_start + strip.frame_final_duration - 1
    scene.frame_set(scene.frame_start)

    clip   = setup_camera_background(strip)
    gp_obj = add_grease_pencil()
    setup_compositor(clip)

    switch_to_layout()
    enter_draw_mode(gp_obj)

    print(f"  Video : {strip.filepath}")
    print(f"  Frames: {scene.frame_start} – {scene.frame_end}")
    print(f"  GP obj: {gp_obj.name}")
    print("\n[grease_pencil_video_paint] Ready — start painting!")
    print("  ← →      navigate frames")
    print("  I        insert keyframe (if Auto-Key is off)")
    print("  Ctrl+F12 render composite animation")
