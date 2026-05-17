@echo off
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
    echo [ERROR] Blender not found.
    pause
    exit /b 1
)

echo [geometry_nodes_growth] Creating procedural_sculpture_demo.blend ...
echo.

"%BLENDER%" --background --python geometry_nodes_growth.py

echo.
if exist "..\models\procedural_sculpture_demo.blend" (
    echo [OK] procedural_sculpture_demo.blend creato in models/
) else (
    echo [ERROR] File non creato.
)
echo.
pause
