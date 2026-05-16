@echo off
:: blender_metadata.py — launcher for Windows
:: Opens Blender with the script loaded in the Scripting workspace.
:: Edit the CONFIG block (AUTHOR, TITLE, LICENSE...) then press Alt+P to run.
::
:: _launch_metadata.py is an internal helper used by this launcher. Do not run it directly.

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

echo [blender_metadata] Opening Blender...
echo   1. Edit the CONFIG block at the top of the script (AUTHOR, TITLE, LICENSE...)
echo   2. Press Alt+P to apply metadata to the current scene.
echo   3. Go to Scene Properties ^> Custom Properties to verify.
echo   4. Save your .blend file.
echo.

"%BLENDER%" --python _launch_metadata.py
