@echo off
:: Scan Cleanup — import your scan first, then run this
:: Select the scan mesh in Blender before running.
cd /d "%~dp0"
set BLENDER_EXE=
for %%B in (
    "C:\Program Files\Blender Foundation\Blender 5.1\blender.exe"
    "C:\Program Files\Blender Foundation\Blender 5.0\blender.exe"
    "C:\Program Files\Blender Foundation\Blender 4.4\blender.exe"
    "C:\Program Files\Blender Foundation\Blender 4.3\blender.exe"
) do ( if exist %%B ( set BLENDER_EXE=%%B & goto :found ) )
where blender >nul 2>&1 && set BLENDER_EXE=blender && goto :found
echo Blender not found. Install from https://www.blender.org & pause & exit /b 1
:found
echo.
echo NOTE: Import your scan mesh FIRST, select it, then re-run from Blender Scripting tab.
echo       Or load scan_cleanup.py manually via Scripting - Open - Run Script (Alt+P).
echo.
start "" %BLENDER_EXE%
pause
