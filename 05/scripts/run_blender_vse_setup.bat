@echo off
:: blender_vse_setup.py — launcher for Windows
:: Opens Blender with the VSE setup script loaded in the Scripting workspace.
:: Press Alt+P to configure render settings and switch to the Video Editing workspace.

cd /d "%~dp0"

set BLENDER=
for %%v in (5.1 5.0 4.4 4.3) do (
    if not defined BLENDER (
        if exist "C:\Program Files\Blender Foundation\Blender %%v\blender.exe" (
            set BLENDER=C:\Program Files\Blender Foundation\Blender %%v\blender.exe
        )
    )
)

if not defined BLENDER (
    echo [ERROR] Blender not found. Install Blender 4.3-5.1 in the default location.
    pause
    exit /b 1
)

echo [blender_vse_setup] Opening Blender...
echo   1. The script blender_vse_setup.py is loaded in the Scripting workspace.
echo   2. Press Alt+P to configure render settings (H.264, 1920x1080, 24fps).
echo   3. Switch to the Video Editing workspace.
echo   4. Add your AI-generated clips: Add > Movie
echo   5. Export: Render > Render Animation (Ctrl+F12)
echo.

"%BLENDER%" --python _launch_vse.py
