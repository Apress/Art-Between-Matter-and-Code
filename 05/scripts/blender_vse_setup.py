"""
blender_vse_setup.py
────────────────────
Art Between Matter and Code · Gianpiero Moioli · Apress 2025
Chapter 5 — §5.3.1.4.1  Mini tutorial: Creating Short Video Sequences

Configures Blender's Video Sequence Editor (VSE) with the recommended
render settings for the AI-video workflow described in the chapter:

  MidJourney V7 (or Kling 2.5 / Runway Gen-3) → export clips as MP4
  → import into Blender VSE → assemble, cross-fade, export H.264

Run: Blender → Scripting workspace → Alt+P
Or double-click run_blender_vse_setup.bat (Windows)
"""

import bpy
import os

# ─────────────────────────────────────────────
# CONFIG — edit before running
# ─────────────────────────────────────────────

RESOLUTION_X   = 1920       # px — matches standard AI video output
RESOLUTION_Y   = 1080       # px
FRAME_RATE     = 24         # fps — cinematic standard
FRAME_START    = 1
FRAME_END      = 240        # 10 seconds @ 24 fps (adjust per project)
OUTPUT_PATH    = "//render/final_sequence"  # // = relative to .blend file

# H.264 codec settings
CONTAINER      = "MPEG4"    # .mp4 container
VIDEO_CODEC    = "H264"
AUDIO_CODEC    = "AAC"
ENCODING_SPEED = "GOOD"     # GOOD = quality/speed balance
CONSTANT_RATE_FACTOR = 18   # 0–51: lower = better quality. 18 = high quality.

# ─────────────────────────────────────────────
# Setup
# ─────────────────────────────────────────────

def configure_render():
    scene = bpy.context.scene
    rd    = scene.render

    # Resolution
    rd.resolution_x          = RESOLUTION_X
    rd.resolution_y          = RESOLUTION_Y
    rd.resolution_percentage = 100

    # Frame range and rate
    rd.fps       = FRAME_RATE
    scene.frame_start = FRAME_START
    scene.frame_end   = FRAME_END

    # Output format
    rd.image_settings.file_format = "FFMPEG"
    rd.ffmpeg.format              = CONTAINER
    rd.ffmpeg.codec               = VIDEO_CODEC
    rd.ffmpeg.audio_codec         = AUDIO_CODEC
    rd.ffmpeg.constant_rate_factor = CONSTANT_RATE_FACTOR
    rd.ffmpeg.ffmpeg_preset       = ENCODING_SPEED

    # Output path
    rd.filepath = OUTPUT_PATH

    print("[VSE Setup] Render configured: "
          f"{RESOLUTION_X}x{RESOLUTION_Y} @ {FRAME_RATE}fps, "
          f"frames {FRAME_START}–{FRAME_END}, H.264/{CONTAINER}")


def switch_to_vse():
    """Switch active workspace to Video Editing (if available)."""
    for ws in bpy.data.workspaces:
        if "Video Editing" in ws.name or "VSE" in ws.name:
            bpy.context.window.workspace = ws
            print(f"[VSE Setup] Switched to workspace: {ws.name}")
            return
    print("[VSE Setup] Video Editing workspace not found — open it manually: "
          "top-left menu → Video Editing")


def add_usage_note():
    """Add a text block with workflow instructions."""
    name = "VSE_Workflow_Instructions"
    if name in bpy.data.texts:
        txt = bpy.data.texts[name]
        txt.clear()
    else:
        txt = bpy.data.texts.new(name)

    instructions = """
# ─────────────────────────────────────────────────────────────────────
# BLENDER VSE — AI Video Workflow  (Chapter 5 §5.3.1.4.1)
# Art Between Matter and Code · Gianpiero Moioli · Apress 2025
# ─────────────────────────────────────────────────────────────────────
#
# STEP 1 — Generate clips in MidJourney V7 (or Kling 2.5 / Runway Gen-3)
#   • Upload two images (start frame, end frame)
#   • Add a descriptive prompt
#   • Set Duration and Quality Mode → Create
#   • Export each clip as MP4
#
# STEP 2 — Import clips into the VSE
#   Add → Movie → select your MP4 files
#   Drag clips along the timeline to arrange them.
#   Recommended strip order:
#     Channel 1: first clip
#     Channel 1: second clip (after first)
#     Channel 2: cross-fade strip (Add → Effect Strip → Cross)
#
# STEP 3 — Add cross-fade between clips
#   Select two adjacent strips → Add → Effect Strip → Cross
#   The overlap zone determines fade duration (2–3 sec recommended).
#
# STEP 4 — Add audio (optional)
#   Add → Sound → import ambient audio / AI-generated music
#   Position on Channel 2 or higher.
#
# STEP 5 — Export
#   Render → Render Animation  (Ctrl+F12)
#   Output: //render/final_sequence.mp4 (as configured by the script)
#
# TIPS
#   • Use proxy rendering for long timelines (Playback → Proxy)
#   • Ctrl+Right Arrow: jump to next strip
#   • K: cut strip at playhead
#   • G: grab/move selected strip
#   • Shift+D: duplicate strip
# ─────────────────────────────────────────────────────────────────────
"""
    txt.write(instructions.strip())
    print(f"[VSE Setup] Instructions written to text block: '{name}'")
    print("  Open it: Scripting workspace → Text editor → select 'VSE_Workflow_Instructions'")


# ─────────────────────────────────────────────
# Run
# ─────────────────────────────────────────────

configure_render()
switch_to_vse()
add_usage_note()

print("[VSE Setup] Complete.")
print("  Next step: Add → Movie → import your AI-generated clips.")
print("  Export: Render → Render Animation (Ctrl+F12)")
