@echo off
:: Anish Kapoor: Tall Tree and the Eye (§3.6.3.2 · Fig 22)
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
if exist "%~dp0_scripting_startup.blend" (
    start "" %BLENDER_EXE% "%~dp0_scripting_startup.blend" --python "%~dp0kapoor_tall_tree.py"
) else (
    start "" %BLENDER_EXE% --python "%~dp0kapoor_tall_tree.py"
)
