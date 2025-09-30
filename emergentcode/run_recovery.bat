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

REM Check if dependencies are installed
python -c "import mnemonic, selenium; print('Dependencies OK')" >nul 2>&1
if errorlevel 1 (
    echo ❌ Dependencies not found
    echo.
    echo 💡 Please run setup first:
    echo    setup_windows11.bat
    echo.
    pause
    exit /b 1
)

REM Run the recovery tool
python server.py

echo.
echo 👋 Thank you for using BIP39 Mnemonic Recovery Tool!
pause