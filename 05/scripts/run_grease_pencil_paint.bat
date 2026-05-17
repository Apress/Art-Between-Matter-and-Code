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

echo Istruzioni:
echo   1. Blender si apre nel workspace Scripting
echo   2. Il file grease_pencil_video_paint.py e gia caricato
echo   3. Premi Alt+P per avviare
echo   4. Usa le frecce per navigare tra i frame e dipingi
echo.

"%BLENDER%" --python _launch_gp_paint.py
