@echo off
REM Run the Advanced BIP39 Mnemonic Recovery Tool

echo.
echo 🚀 Starting Advanced BIP39 Recovery Tool...
echo ===========================================

REM Try to find Python using the same logic as setup.bat
set PYTHON_CMD=

REM Method 1: Try 'py' command (Windows Python Launcher)
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

echo ❌ Python not found! Please run setup_advanced.bat first.
pause
exit /b 1

:python_found
echo ✅ Found Python: %PYTHON_CMD%

REM Check required libraries
%PYTHON_CMD% -c "import mnemonic, selenium" >nul 2>&1
if errorlevel 1 (
    echo ❌ Required libraries missing! Please run setup_advanced.bat first.
    pause
    exit /b 1
)

echo ✅ All dependencies found
echo.
echo 🆕 ADVANCED FEATURES:
echo   • Any missing position (1-24)
echo   • Save/Load word combinations
echo   • Find ALL valid words
echo   • Browser MetaMask integration
echo.
echo ⚠️  SECURITY REMINDER:
echo   • Use offline for maximum security
echo   • Test with small amounts first
echo   • Keep recovered mnemonics private
echo.

REM Run the advanced tool
%PYTHON_CMD% mnemonic_recovery_advanced.py

if errorlevel 1 (
    echo.
    echo ❌ Error running the tool. Please check:
    echo 1. mnemonic_recovery_advanced.py exists
    echo 2. All dependencies are installed
    echo.
)

pause