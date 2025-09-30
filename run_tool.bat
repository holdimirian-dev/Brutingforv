@echo off
REM Quick Start Script for BIP39 Mnemonic Recovery Tool (Windows)
REM This script runs the GUI version of the tool

echo.
echo 🔐 Starting BIP39 Mnemonic Recovery Tool...
echo ==========================================

REM Try to find Python using different methods
set PYTHON_CMD=

REM Method 1: Try 'py' command (Windows Python Launcher) - Most reliable
py --version >nul 2>&1
if not errorlevel 1 (
    set PYTHON_CMD=py
    goto :python_found
)

REM Method 2: Try 'python' command
python --version >nul 2>&1
if not errorlevel 1 (
    set PYTHON_CMD=python
    goto :python_found
)

REM Method 3: Try 'python3' command
python3 --version >nul 2>&1
if not errorlevel 1 (
    set PYTHON_CMD=python3
    goto :python_found
)

REM Python not found
echo ❌ Python not found! Please run setup.bat first.
echo.
echo 🔧 QUICK FIX:
echo 1. Double-click setup.bat to install Python properly
echo 2. Make sure to check "Add Python to PATH" during Python installation
echo 3. Restart your computer after installing Python
echo.
pause
exit /b 1

:python_found
echo ✅ Found Python: %PYTHON_CMD%

REM Check if mnemonic library is installed
%PYTHON_CMD% -c "import mnemonic" >nul 2>&1
if errorlevel 1 (
    echo ❌ mnemonic library not found! Please run setup.bat first.
    echo.
    echo 🔧 QUICK FIX:
    echo Double-click setup.bat to install required libraries
    echo.
    pause
    exit /b 1
)

echo ✅ All dependencies found
echo 🚀 Starting GUI tool...
echo.
echo ⚠️  SECURITY REMINDER:
echo   - Disconnect from internet for maximum security
echo   - Keep your recovered mnemonic private
echo   - Only enter your REAL words when ready
echo.

REM Run the GUI tool
%PYTHON_CMD% mnemonic_recovery_gui.py

if errorlevel 1 (
    echo.
    echo ❌ Error running the tool. Please check:
    echo 1. All files are in the same folder
    echo 2. mnemonic_recovery_gui.py exists
    echo 3. Python is working correctly
    echo.
)

pause