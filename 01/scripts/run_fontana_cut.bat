@echo off
:: ============================================================
::  run_fontana_cut.bat
::  Opens Blender and automatically runs fontana_cut.py
::
::  Blender is launched in GUI mode so you can see the result.
::  The script adds a parametric Fontana-cut canvas to the scene.
::
::  Adjust BLENDER_PATH below if Blender is installed elsewhere.
:: ============================================================

cd /d "%~dp0"

:: ── Set Blender path ──────────────────────────────────────────
:: Try common installation paths automatically
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
echo  Launching Blender with fontana_cut.py ...
echo  Blender: %BLENDER_EXE%
echo.
echo  Once Blender opens:
echo    - The Fontana-cut canvas is already added to the scene.
echo    - Edit parameters at the top of fontana_cut.py and re-run
echo      from Blender's Scripting workspace (Alt+P).
echo.

start "" %BLENDER_EXE% --python "%~dp0fontana_cut.py"
