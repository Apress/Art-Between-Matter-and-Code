@echo off
:: ============================================================
::  run_aura_transition.bat
::  Generates ref_aura_transition_diagram.svg and opens it
::  in your default browser.
::
::  No extra packages needed — pure Python only.
::  Works with system Python or Blender's built-in Python.
:: ============================================================

cd /d "%~dp0"

:: Try system Python
where python >nul 2>&1
if %errorlevel%==0 (
    python aura_transition.py --output .
    goto :done
)

:: Try Python Launcher
where py >nul 2>&1
if %errorlevel%==0 (
    py aura_transition.py --output .
    goto :done
)

:: Try Blender's built-in Python
for %%B in (
    "C:\Program Files\Blender Foundation\Blender 5.1\5.1\python\bin\python.exe"
    "C:\Program Files\Blender Foundation\Blender 5.0\5.0\python\bin\python.exe"
    "C:\Program Files\Blender Foundation\Blender 4.4\4.4\python\bin\python.exe"
    "C:\Program Files\Blender Foundation\Blender 4.3\4.3\python\bin\python.exe"
    "C:\Program Files\Blender Foundation\Blender 4.2\4.2\python\bin\python.exe"
) do (
    if exist %%B (
        %%B aura_transition.py --output .
        goto :done
    )
)

echo.
echo  ERROR: Python not found.
echo  Download Python from https://www.python.org/downloads/
echo  Then double-click this file again.
echo.
pause
exit /b 1

:done
echo.
echo  Done. The SVG file should have opened in your browser.
echo  If not, open: %~dp0ref_aura_transition_diagram.svg
echo.
pause
