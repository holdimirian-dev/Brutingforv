@echo off
REM Setup script for BIP39 Mnemonic Recovery Tool (Windows)
REM This script installs required dependencies and sets up the tool

echo.
echo ========================================
echo 🔐 BIP39 Mnemonic Recovery Tool Setup
echo ========================================
echo.

REM Try different ways to find Python on Windows
set PYTHON_CMD=
set PIP_CMD=

echo 🔍 Looking for Python installation...
echo.

REM Method 1: Try 'py' command (Windows Python Launcher)
py --version >nul 2>&1
if not errorlevel 1 (
    echo ✅ Found Python using 'py' command:
    py --version
    set PYTHON_CMD=py
    set PIP_CMD=py -m pip
    goto :python_found
)

REM Method 2: Try 'python' command
python --version >nul 2>&1
if not errorlevel 1 (
    echo ✅ Found Python using 'python' command:
    python --version
    set PYTHON_CMD=python
    set PIP_CMD=pip
    goto :python_found
)

REM Method 3: Try 'python3' command
python3 --version >nul 2>&1
if not errorlevel 1 (
    echo ✅ Found Python using 'python3' command:
    python3 --version
    set PYTHON_CMD=python3
    set PIP_CMD=pip3
    goto :python_found
)

REM If we get here, Python was not found
echo ❌ Python is not found or not added to PATH!
echo.
echo 🔧 SOLUTION STEPS:
echo.
echo 1. First, let's check if Python is actually installed:
echo    - Press Windows Key + R
echo    - Type: appwiz.cpl
echo    - Press Enter
echo    - Look for "Python 3.13" or similar in the list
echo.
echo 2. If Python IS installed but this script can't find it:
echo    - You need to add Python to your PATH
echo    - Here's how:
echo.
echo    OPTION A - Reinstall Python (EASIEST):
echo    • Go to https://www.python.org/downloads/
echo    • Download Python 3.13
echo    • During installation, CHECK the box: "Add Python to PATH"
echo    • This will fix the PATH issue
echo.
echo    OPTION B - Manual PATH fix (ADVANCED):
echo    • Press Windows Key + R, type: sysdm.cpl
echo    • Click "Environment Variables"
echo    • Find Python in your Programs folder and add to PATH
echo.
echo 3. After fixing, restart your computer and run this script again
echo.
pause
exit /b 1

:python_found
echo.
echo 📋 Python command to use: %PYTHON_CMD%
echo 📋 Pip command to use: %PIP_CMD%
echo.

REM Test pip
echo 🔍 Checking if pip works...
%PIP_CMD% --version >nul 2>&1
if errorlevel 1 (
    echo ❌ pip is not working properly
    echo.
    echo 🔧 SOLUTION: Try this command manually:
    echo   %PYTHON_CMD% -m ensurepip --default-pip
    echo.
    pause
    exit /b 1
)

echo ✅ pip is working:
%PIP_CMD% --version
echo.

REM Install required Python packages
echo 📦 Installing required packages...
echo This may take a minute...
echo.

%PIP_CMD% install mnemonic selenium
if errorlevel 1 (
    echo ❌ Failed to install required libraries
    echo.
    echo 🔧 MANUAL SOLUTION:
    echo Open Command Prompt as Administrator and run:
    echo   %PIP_CMD% install mnemonic selenium
    echo.
    echo Or try:
    echo   %PYTHON_CMD% -m pip install mnemonic selenium
    echo.
    pause
    exit /b 1
)

echo.
echo ✅ Successfully installed mnemonic library!
echo.
echo 🎉 Setup completed successfully!
echo.
echo ========================================
echo          HOW TO RUN THE TOOL
echo ========================================
echo.
echo 🖱️ EASIEST WAY:
echo   Double-click: run_tool.bat
echo.
echo 📱 Or directly run the GUI:
echo   Double-click: mnemonic_recovery_gui.py
echo.
echo 💻 Command Line Version:
echo   Double-click: mnemonic_recovery.py
echo.
echo ⚠️  SECURITY REMINDERS:
echo   - Disconnect from internet before running (recommended)
echo   - Keep your recovered mnemonic private
echo   - Delete all outputs when done
echo   - Use on a secure, clean computer
echo.
echo 📖 Read USER_GUIDE.md for detailed instructions
echo.
echo Your Python command is: %PYTHON_CMD%
echo.
pause