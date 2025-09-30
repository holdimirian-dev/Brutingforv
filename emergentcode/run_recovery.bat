@echo off
REM BIP39 Mnemonic Recovery Tool - Windows 11 Runner
REM Quick launcher for the terminal-based recovery tool

echo.
echo ================================================================
echo 🔐 BIP39 Mnemonic Recovery Tool
echo ================================================================
echo Terminal Interface • Windows 11 • Edge WebDriver • MetaMask
echo ================================================================
echo.

REM Find Python command
set "PYTHON_CMD="

REM Try different Python commands
python --version >nul 2>&1
if not errorlevel 1 (
    set "PYTHON_CMD=python"
    goto :python_found
)

py --version >nul 2>&1
if not errorlevel 1 (
    set "PYTHON_CMD=py"
    goto :python_found
)

python3 --version >nul 2>&1
if not errorlevel 1 (
    set "PYTHON_CMD=python3"
    goto :python_found
)

echo ❌ Python not found
echo 💡 Please run setup_windows11.bat first
pause
exit /b 1

:python_found
REM Check if dependencies are installed
%PYTHON_CMD% -c "import mnemonic, selenium; print('Dependencies OK')" >nul 2>&1
if errorlevel 1 (
    echo ❌ Dependencies not found
    echo.
    echo 💡 Please run setup first:
    echo    setup_windows11.bat
    echo.
    pause
    exit /b 1
)

echo ✅ Python found: %PYTHON_CMD%
echo ✅ Dependencies installed

REM Run the recovery tool
%PYTHON_CMD% server.py

echo.
echo 👋 Thank you for using BIP39 Mnemonic Recovery Tool!
pause