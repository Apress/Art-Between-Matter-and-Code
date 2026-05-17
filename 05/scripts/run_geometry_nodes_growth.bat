@echo off
:: geometry_nodes_growth.py — launcher for Windows
:: Creates procedural_sculpture_demo.blend in the models/ folder.
:: Requires Blender 4.3 or later installed in the default location.

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

echo [geometry_nodes_growth] Creating procedural_sculpture_demo.blend ...
"%BLENDER%" --background --python geometry_nodes_growth.py

if exist "..\models\procedural_sculpture_demo.blend" (
    echo.
    echo [OK] procedural_sculpture_demo.blend created in models/
    echo      Open it in Blender to explore the Geometry Nodes setup.
) else (
    echo [ERROR] .blend file was not created. Check Blender output above.
)
pause
