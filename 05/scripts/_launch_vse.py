"""
_launch_vse.py — file interno, usato da run_blender_vse_setup.bat.
Non modificare. Non eseguire direttamente.
"""
import bpy, os

TARGET = os.path.join(os.path.dirname(os.path.abspath(__file__)), "blender_vse_setup.py")

def _switch():
    for ws in bpy.data.workspaces:
        if "Script" in ws.name:
            bpy.context.window.workspace = ws
            break
    return None

def _load():
    name = os.path.basename(TARGET)
    if name not in bpy.data.texts:
        bpy.data.texts.load(TARGET)
    txt = bpy.data.texts[name]
    for ws in bpy.data.workspaces:
        if "Script" in ws.name:
            for screen in ws.screens:
                for area in screen.areas:
                    if area.type == "TEXT_EDITOR":
                        area.spaces[0].text                  = txt
                        area.spaces[0].show_line_numbers     = True
                        area.spaces[0].show_syntax_highlight = True
                        return None
    return None

bpy.app.timers.register(_switch, first_interval=0.3)
bpy.app.timers.register(_load,   first_interval=0.8)
