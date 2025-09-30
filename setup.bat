@echo off
REM Setup script for BIP39 Mnemonic Recovery Tool (Windows)
REM This script installs required dependencies and sets up the tool

echo 🔐 BIP39 Mnemonic Recovery Tool Setup
echo ====================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.6 or higher.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python found
python --version

REM Check if pip is installed
pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ pip is not installed. Please install pip.
    pause
    exit /b 1
)

echo ✅ pip found

REM Install required Python packages
echo 📦 Installing required packages...
pip install mnemonic

if errorlevel 1 (
    echo ❌ Failed to install mnemonic library
    pause
    exit /b 1
)

echo ✅ Successfully installed mnemonic library
echo.
echo 🎉 Setup completed successfully!
echo.
echo To run the recovery tool:
echo   python mnemonic_recovery.py
echo.
echo ⚠️  SECURITY REMINDER:
echo   - Run this tool on a secure, offline computer
echo   - Keep your recovered mnemonic private
echo   - Delete outputs after use
echo.
pause