@echo off
REM IonQ Demo - Virtual Environment Setup Script (Windows)
REM This script creates and activates a Python virtual environment for the IonQ demo

setlocal enabledelayedexpansion

echo.
echo ========================================
echo IonQ Demo - Virtual Environment Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH.
    echo Please install Python 3.9 or higher from https://www.python.org/
    pause
    exit /b 1
)

REM Get Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Python version: %PYTHON_VERSION%
echo.

REM Define venv directory
set VENV_DIR=venv

REM Check if venv already exists
if exist "%VENV_DIR%" (
    echo Virtual environment already exists at %VENV_DIR%
    set /p RECREATE="Do you want to recreate it? (y/n): "
    if /i "!RECREATE!"=="y" (
        echo Removing existing virtual environment...
        rmdir /s /q "%VENV_DIR%"
    ) else (
        echo Using existing virtual environment.
        goto ACTIVATE_VENV
    )
)

REM Create virtual environment
echo Creating virtual environment...
python -m venv "%VENV_DIR%"
if errorlevel 1 (
    echo Error creating virtual environment.
    pause
    exit /b 1
)
echo ✓ Virtual environment created
echo.

:ACTIVATE_VENV
REM Activate virtual environment
echo Activating virtual environment...
call "%VENV_DIR%\Scripts\activate.bat"
if errorlevel 1 (
    echo Error activating virtual environment.
    pause
    exit /b 1
)
echo ✓ Virtual environment activated
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip setuptools wheel -q
echo ✓ Pip upgraded
echo.

REM Install requirements
if exist "requirements.txt" (
    echo Installing dependencies from requirements.txt...
    pip install -r requirements.txt -q
    echo ✓ Dependencies installed
    echo.
) else (
    echo Error: requirements.txt not found in current directory.
    pause
    exit /b 1
)

REM Verify installation
echo Verifying installation...
python -c "from qiskit import transpile; print('✓ Qiskit OK')" 2>nul
if errorlevel 1 (
    echo Warning: Some imports may have failed
) else (
    echo ✓ All imports successful
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.

echo Next steps:
echo 1. Verify the environment is active (you should see '(venv)' in your prompt)
echo 2. Run the Jupyter notebook:
echo    jupyter notebook IonQ_Demo_Notebook.ipynb
echo.
echo 3. Or run individual Python scripts:
echo    python 03-Hardware-Connectivity\connectivity_challenge.py
echo    python 01-Finance-AmericanOptions\finance_comparator_demo.py
echo    python 02-Chemistry-CarbonCapture\chemistry_vqe_demo.py
echo.
echo To deactivate the environment, run: deactivate
echo.
pause
