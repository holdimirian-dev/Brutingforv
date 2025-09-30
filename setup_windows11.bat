@echo off
REM BIP39 Mnemonic Recovery Tool - Windows 11 Setup Script
REM Installs all dependencies including Edge WebDriver for MetaMask automation

echo.
echo ================================================================
echo 🔐 BIP39 Mnemonic Recovery Tool - Windows 11 Setup
echo ================================================================
echo Installing Python dependencies and Edge WebDriver automation
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found in PATH
    echo.
    echo 💡 Please install Python 3.6+ from:
    echo    https://python.org/downloads/
    echo.
    echo ⚠️  Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo ✅ Python found
python --version

echo.
echo 📦 Installing Python dependencies...

REM Install core mnemonic library
python -m pip install mnemonic>=0.21
if errorlevel 1 (
    echo ❌ Failed to install mnemonic library
    pause
    exit /b 1
)
echo ✅ BIP39 mnemonic library installed

REM Install Selenium for browser automation
python -m pip install selenium>=4.35.0
if errorlevel 1 (
    echo ❌ Failed to install selenium
    pause
    exit /b 1
)
echo ✅ Selenium browser automation installed

REM Install WebDriver Manager for automatic Edge driver management
python -m pip install webdriver-manager>=4.0.0
if errorlevel 1 (
    echo ❌ Failed to install webdriver-manager
    pause
    exit /b 1
)
echo ✅ WebDriver Manager installed

echo.
echo 🌐 Checking Microsoft Edge installation...

REM Check if Edge is installed
if exist "%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe" (
    echo ✅ Microsoft Edge found
) else if exist "%ProgramFiles%\Microsoft\Edge\Application\msedge.exe" (
    echo ✅ Microsoft Edge found
) else (
    echo ❌ Microsoft Edge not found
    echo.
    echo 💡 Please install Microsoft Edge from:
    echo    https://www.microsoft.com/edge/
    echo.
    echo ⚠️  Edge is required for MetaMask automation
    pause
    exit /b 1
)

echo.
echo 🧪 Testing installation...

REM Test the installation
python -c "
try:
    from mnemonic import Mnemonic
    mnemo = Mnemonic('english')
    print('✅ BIP39 library:', len(mnemo.wordlist), 'words loaded')
    
    import selenium
    print('✅ Selenium browser automation ready')
    
    from webdriver_manager.microsoft import EdgeChromiumDriverManager
    print('✅ Edge WebDriver manager ready')
    
    print('🎉 All dependencies installed successfully!')
    
except Exception as e:
    print('❌ Installation test failed:', e)
    exit(1)
"

if errorlevel 1 (
    echo.
    echo ❌ Installation test failed
    echo 💡 Please check the error messages above
    pause
    exit /b 1
)

echo.
echo ================================================================
echo 🎉 INSTALLATION COMPLETE!
echo ================================================================
echo.
echo 🚀 To run the mnemonic recovery tool:
echo    python server.py
echo.
echo 📋 Features available:
echo   • Recover missing words from any position (1-24)
echo   • BIP39 compliant validation
echo   • MetaMask integration with Edge browser
echo   • Step-by-step terminal guidance
echo   • Progress tracking and validation
echo.
echo ⚠️  SECURITY RECOMMENDATIONS:
echo   • Run this tool on a secure, offline computer when possible
echo   • Never share your mnemonic phrases with anyone
echo   • Test with small amounts first when importing to MetaMask
echo   • Delete any saved outputs after successful recovery
echo.
echo 📖 Need help? Check the documentation files:
echo   • README.md - Basic usage
echo   • MNEMONIC_RECOVERY_README.md - Detailed guide
echo   • USER_GUIDE.md - Step-by-step instructions
echo.
pause