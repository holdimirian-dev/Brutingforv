@echo off
REM Setup script for BIP39 Mnemonic Recovery Tool (Windows)
REM This script installs required dependencies and sets up the tool

echo.
echo ========================================
echo 🔐 BIP39 Mnemonic Recovery Tool Setup
echo ========================================
echo.

REM Check if Python is installed
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed!
    echo.
    echo Please install Python first:
    echo 1. Go to https://www.python.org/downloads/
    echo 2. Download and install Python 3.6 or higher
    echo 3. ⚠️ IMPORTANT: Check "Add Python to PATH" during installation
    echo 4. Restart your computer after installation
    echo 5. Run this setup script again
    echo.
    pause
    exit /b 1
)

echo ✅ Python found:
python --version
echo.

REM Check if pip is installed
echo Checking pip installation...
pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ pip is not installed. This usually comes with Python.
    echo Please reinstall Python from https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ pip found
echo.

REM Install required Python packages
echo 📦 Installing required packages...
echo This may take a minute...
pip install mnemonic

if errorlevel 1 (
    echo ❌ Failed to install mnemonic library
    echo.
    echo Try running this command manually:
    echo   pip install mnemonic
    echo.
    pause
    exit /b 1
)

echo.
echo ✅ Successfully installed mnemonic library
echo.
echo 🎉 Setup completed successfully!
echo.
echo ========================================
echo          HOW TO RUN THE TOOL
echo ========================================
echo.
echo GUI Version (Recommended for beginners):
echo   Double-click: mnemonic_recovery_gui.py
echo.
echo Command Line Version:
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
pause