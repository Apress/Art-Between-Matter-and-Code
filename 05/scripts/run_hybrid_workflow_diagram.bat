@echo off
:: hybrid_workflow_diagram.py ??? launcher for Windows
:: Generates the Hybrid Workflow diagram (Chapter 5) as a standalone SVG.
:: The SVG is saved in the current folder and opens automatically in your browser.

cd /d "%~dp0"

python hybrid_workflow_diagram.py --output ..\images

if exist "..\images\ref_hybrid_workflow_diagram.svg" (
    echo.
    echo [OK] SVG saved to images\ref_hybrid_workflow_diagram.svg
    start "" "..\images\ref_hybrid_workflow_diagram.svg"
) else (
    echo [ERROR] SVG was not created. Make sure Python 3.x is installed.
    pause
)
