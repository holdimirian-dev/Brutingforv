@echo off
REM Quick Start Script for BIP39 Mnemonic Recovery Tool (Windows)
REM This script runs the GUI version of the tool

echo.
echo 🔐 Starting BIP39 Mnemonic Recovery Tool...
echo ==========================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found! Please run setup.bat first.
    echo.
    pause
    exit /b 1
)

REM Check if mnemonic library is installed
python -c "import mnemonic" >nul 2>&1
if errorlevel 1 (
    echo ❌ mnemonic library not found! Please run setup.bat first.
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
echo.

REM Run the GUI tool
python mnemonic_recovery_gui.py

pause