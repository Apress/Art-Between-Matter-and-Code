@echo off
title Chapter 5 - Grease Pencil Video Paint
echo.
echo  === Chapter 5 - Grease Pencil Video Paint ===
echo.
cd /d "%~dp0"

set "BLENDER="
if exist "C:\Program Files\Blender Foundation\Blender 5.1\blender.exe" set "BLENDER=C:\Program Files\Blender Foundation\Blender 5.1\blender.exe"
if not defined BLENDER if exist "C:\Program Files\Blender Foundation\Blender 5.0\blender.exe" set "BLENDER=C:\Program Files\Blender Foundation\Blender 5.0\blender.exe"
if not defined BLENDER if exist "C:\Program Files\Blender Foundation\Blender 4.4\blender.exe" set "BLENDER=C:\Program Files\Blender Foundation\Blender 4.4\blender.exe"
if not defined BLENDER if exist "C:\Program Files\Blender Foundation\Blender 4.3\blender.exe" set "BLENDER=C:\Program Files\Blender Foundation\Blender 4.3\blender.exe"

if not defined BLENDER (
    echo [ERRORE] Blender non trovato.
    pause
    exit /b 1
)

:: %1 = file .blend trascinato sopra il bat (opzionale)
if "%~1"=="" (
    echo Nessun file .blend specificato - apro scena vuota.
    echo Suggerimento: trascina un file .blend sopra questo bat.
    echo.
    "%BLENDER%" --python _launch_gp_paint.py
) else (
    echo File: %~1
    echo.
    "%BLENDER%" "%~1" --python _launch_gp_paint.py
)
