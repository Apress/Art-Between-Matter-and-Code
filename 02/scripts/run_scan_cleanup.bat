@echo off
:: Scan Cleanup — opens Blender in Scripting workspace with scan_cleanup.py loaded.
:: Import your scan mesh first (File > Import), select it, then Alt+P to run.
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
if not exist "%~dp0_scripting_startup.blend" (
    echo [first run] Building Scripting workspace startup file - please wait...
    %BLENDER_EXE% --python "%~dp0_make_startup.py"
    echo [first run] Done.
)

echo.
echo Blender will open in Scripting workspace with scan_cleanup.py loaded.
echo   1. File ^> Import ^> OBJ / FBX / PLY  — import your scan mesh
echo   2. Click the mesh in the 3D viewport to select it
echo   3. Press Alt+P in the text editor to run the cleanup
echo.
start "" %BLENDER_EXE% "%~dp0_scripting_startup.blend" --python "%~dp0scan_cleanup.py"
