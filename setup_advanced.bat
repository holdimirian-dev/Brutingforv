@echo off
REM Advanced setup script that also installs Chrome WebDriver
REM This installs everything needed for MetaMask browser testing

echo.
echo =============================================
echo 🔐 Advanced BIP39 Recovery Tool Setup
echo =============================================
echo Installing: Python libraries + Browser drivers
echo.

REM Use the existing setup.bat logic for Python detection
call setup.bat

if errorlevel 1 (
    echo ❌ Basic setup failed. Please fix Python installation first.
    pause
    exit /b 1
)

echo.
echo 🌐 Setting up browser automation...

REM Check if Chrome is installed
echo Checking for Chrome browser...
if exist "%ProgramFiles%\Google\Chrome\Application\chrome.exe" (
    echo ✅ Chrome found
) else if exist "%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe" (
    echo ✅ Chrome found
) else (
    echo ❌ Chrome not found
    echo 💡 Please install Google Chrome for MetaMask testing
    echo Download from: https://www.google.com/chrome/
)

echo.
echo 📦 Installing WebDriver manager...
REM Install webdriver-manager to automatically handle browser drivers
%PIP_CMD% install webdriver-manager

if errorlevel 1 (
    echo ❌ Failed to install webdriver-manager
    echo 💡 Manual installation: %PIP_CMD% install webdriver-manager
    echo 💡 You can still use the tool without browser automation
) else (
    echo ✅ WebDriver manager installed successfully
)

echo.
echo 🎉 Advanced setup completed!
echo.
echo ========================================
echo          READY TO USE
echo ========================================
echo.
echo 🚀 To run the advanced tool:
echo   Double-click: run_advanced_tool.bat
echo.
echo 📱 Or run directly:
echo   %PYTHON_CMD% mnemonic_recovery_advanced.py
echo.
echo 🆕 NEW FEATURES:
echo   • Any missing position (not just 22)
echo   • Save/Load your word combinations
echo   • Find ALL valid results (not just first)
echo   • Browser integration for MetaMask testing
echo.
pause