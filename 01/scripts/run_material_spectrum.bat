@echo off
:: ============================================================
::  run_material_spectrum.bat
::  Opens Blender and automatically runs material_spectrum.py
::
::  The script builds a row of five objects — same form, five
::  material states: marble, terracotta, bronze, glass, wireframe.
::
::  Adjust BLENDER_PATH below if Blender is installed elsewhere.
:: ============================================================

cd /d "%~dp0"

:: ── Set Blender path ──────────────────────────────────────────
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

:: Also try PATH
where blender >nul 2>&1
if %errorlevel%==0 (
    set BLENDER_EXE=blender
    goto :found
)

echo.
echo  ERROR: Blender not found.
echo  Edit this .bat file and set BLENDER_PATH to your blender.exe location.
echo  Example: "C:\Program Files\Blender Foundation\Blender 4.4\blender.exe"
echo.
pause
exit /b 1

:found
echo  Launching Blender with material_spectrum.py ...
echo  Blender: %BLENDER_EXE%
echo.
echo  Once Blender opens:
echo    - Five objects appear in a row: marble, terracotta, bronze, glass, wireframe.
echo    - Edit BASE_FORM, SPACING or SEED at the top of material_spectrum.py
echo      and re-run from Blender's Scripting workspace (Alt+P).
echo.

start "" %BLENDER_EXE% --python "%~dp0material_spectrum.py"
