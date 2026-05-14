@echo off
:: ============================================================
::  run_parametric_space.bat
::  Opens Blender and automatically runs parametric_space.py
::
::  The script generates a parametric spatial field mesh
::  and adds it to the scene. Compatible with an open
::  fig_01_spazialismo_fontana.blend — it will not overwrite
::  existing objects.
::
::  To use with the Spazio scene:
::    1. Open fig_01_spazialismo_fontana.blend in Blender
::    2. Go to Scripting workspace
::    3. Open parametric_space.py and press Alt+P
::
::  Or double-click this .bat to open a new Blender session.
:: ============================================================

cd /d "%~dp0"

set BLENDER_EXE=

for %%B in (
    "C:\Program Files\Blender Foundation\Blender 5.1\blender.exe"
    "C:\Program Files\Blender Foundation\Blender 5.0\blender.exe"
    "C:\Program Files\Blender Foundation\Blender 4.4\blender.exe"
    "C:\Program Files\Blender Foundation\Blender 4.3\blender.exe"
    "C:\Program Files\Blender Foundation\Blender 4.2\blender.exe"
    "C:\Program Files\Blender Foundation\Blender 4.1\blender.exe"
    "C:\Program Files\Blender Foundation\Blender 4.0\blender.exe"
) do (
    if exist %%B (
        set BLENDER_EXE=%%B
        goto :found
    )
)

where blender >nul 2>&1
if %errorlevel%==0 (
    set BLENDER_EXE=blender
    goto :found
)

echo.
echo  ERROR: Blender not found.
echo  Edit this .bat and set BLENDER_EXE to your blender.exe path.
echo.
pause
exit /b 1

:found
echo  Launching Blender with parametric_space.py ...
echo  Blender: %BLENDER_EXE%
echo.
echo  Parameters to explore (edit parametric_space.py):
echo    FIELD_PROFILE  = "radial" / "linear" / "turbulent"
echo    WAVE_AMPLITUDE = field intensity
echo    GRID_DENSITY   = mesh resolution
echo.

start "" %BLENDER_EXE% --python "%~dp0parametric_space.py"
