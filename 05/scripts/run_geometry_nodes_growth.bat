@echo off
title Chapter 5 - Procedural Sculpture Generator
echo.
echo  === Chapter 5 - Procedural Sculpture Generator ===
echo.

cd /d "%~dp0"

:: Find Blender
set "BLENDER="
for %%v in (5.1 5.0 4.4 4.3) do (
    if not defined BLENDER (
        if exist "C:\Program Files\Blender Foundation\Blender %%v\blender.exe" (
            set "BLENDER=C:\Program Files\Blender Foundation\Blender %%v\blender.exe"
            echo Blender trovato: %%v
        )
    )
)

if not defined BLENDER (
    echo [ERRORE] Blender non trovato.
    echo Installa Blender 4.3-5.1 nella posizione predefinita.
    echo.
    pause
    goto :eof
)

echo.
echo Esecuzione script...
echo.

"%BLENDER%" --background --python geometry_nodes_growth.py

echo.
echo -----------------------------------------
if exist "..\models\procedural_sculpture_demo.blend" (
    echo [OK] procedural_sculpture_demo.blend creato in models/
) else (
    echo [ERRORE] File non creato.
)
echo -----------------------------------------
echo.
pause
