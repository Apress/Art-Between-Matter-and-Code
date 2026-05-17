@echo off
setlocal
cd /d "%~dp0"
set "OUTDIR=%~dp0..\images"

REM -- Find Python --
if not defined PYTHON if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" set "PYTHON=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
if not defined PYTHON if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" set "PYTHON=%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
if not defined PYTHON if exist "%LOCALAPPDATA%\Programs\Python\Python310\python.exe" set "PYTHON=%LOCALAPPDATA%\Programs\Python\Python310\python.exe"
if not defined PYTHON (
    where python >/dev/null 2>&1 && set "PYTHON=python"
)
if not defined PYTHON (
    echo [ERROR] Python not found. Install Python 3.x from python.org
    cmd /k
    exit /b 1
)

"%PYTHON%" fabrication_workflow_diagram.py --output "%OUTDIR%"
if errorlevel 1 ( cmd /k & exit /b 1 )

start "" "%OUTDIR%ef_fabrication_workflow_diagram.svg"
