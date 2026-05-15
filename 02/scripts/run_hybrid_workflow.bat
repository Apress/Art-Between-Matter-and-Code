@echo off
:: Hybrid Workflow — Four-Phase Demo (Fig 11)
:: Opens Blender in the Scripting workspace and runs all 4 phases.
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
:: First-time setup: create the Scripting workspace startup file.
:: Blender opens briefly, saves _scripting_startup.blend, then quits.
if not exist "%~dp0_scripting_startup.blend" (
    echo [first run] Building Scripting workspace startup file - please wait...
    %BLENDER_EXE% --python "%~dp0_make_startup.py"
    echo [first run] Done.
)

echo Running hybrid workflow (Manual -^> Digital -^> Generative -^> Fabrication^)...
start "" %BLENDER_EXE% "%~dp0_scripting_startup.blend" --python "%~dp0hybrid_workflow.py"
