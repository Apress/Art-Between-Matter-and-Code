@echo off
:: certify_asset.py — launcher for Windows
:: Drag any file onto this .bat to certify it, or run from terminal.
::
:: Usage:
::   Double-click   → certifies the example file below
::   From terminal  → python certify_asset.py <your_file> [options]

cd /d "%~dp0"

:: Try system Python first, then Blender's bundled Python
set PY=
for %%v in (3.13 3.12 3.11 3.10 3.9) do (
    if not defined PY (
        where python%%v >nul 2>&1 && set PY=python%%v
    )
)
if not defined PY (
    where python >nul 2>&1 && set PY=python
)

:: Fallback: Blender bundled Python
if not defined PY (
    for %%B in (5.1 5.0 4.3) do (
        if not defined PY (
            for /f "delims=" %%P in ('dir /b /s "C:\Program Files\Blender Foundation\Blender %%B\%%B\python\bin\python.exe" 2^>nul') do set PY=%%P
        )
    )
)

if not defined PY (
    echo [ERROR] Python not found. Install Python 3.x or Blender.
    pause
    exit /b 1
)

echo [certify_asset] Using Python: %PY%
echo.

:: If a file was dragged onto the bat, certify it; otherwise show usage.
if "%~1"=="" (
    echo Usage: drag any file onto this .bat, or run from terminal:
    echo   python certify_asset.py ^<file^> [--author "Name"] [--notes "..."]
    echo   python certify_asset.py ^<file^> --verify
    echo.
    pause
) else (
    %PY% certify_asset.py "%~1"
    echo.
    pause
)
