@echo off
REM BIP39 Mnemonic Recovery Tool - Windows 11 Setup Script
REM Installs all dependencies including Edge WebDriver for MetaMask automation

echo.
echo ================================================================
echo 🔐 BIP39 Mnemonic Recovery Tool - Windows 11 Setup
echo ================================================================
echo Installing Python dependencies and Edge WebDriver automation
echo.

REM Check if Python is installed - try multiple common commands
set "PYTHON_CMD="

echo 🔍 Searching for Python installation...

REM Try 'python' command first
python --version >nul 2>&1
if not errorlevel 1 (
    set "PYTHON_CMD=python"
    goto :python_found
)

REM Try 'py' command (Python Launcher for Windows)
py --version >nul 2>&1
if not errorlevel 1 (
    set "PYTHON_CMD=py"
    goto :python_found
)

REM Try 'python3' command
python3 --version >nul 2>&1
if not errorlevel 1 (
    set "PYTHON_CMD=python3"
    goto :python_found
)

REM Try common installation paths
if exist "%LOCALAPPDATA%\Programs\Python\Python*\python.exe" (
    for /d %%i in ("%LOCALAPPDATA%\Programs\Python\Python*") do (
        set "PYTHON_CMD=%%i\python.exe"
        goto :python_found
    )
)

if exist "%PROGRAMFILES%\Python*\python.exe" (
    for /d %%i in ("%PROGRAMFILES%\Python*") do (
        set "PYTHON_CMD=%%i\python.exe"
        goto :python_found
    )
)

REM Python not found
echo ❌ Python not found in PATH or common locations
echo.
echo 💡 Python installation options:
echo    1. Download from: https://python.org/downloads/
echo    2. ⚠️  IMPORTANT: Check "Add Python to PATH" during installation
echo    3. Or install from Microsoft Store: https://apps.microsoft.com/store/detail/python-39/9P7QFQMJRFP7
echo.
echo 🔧 If Python is installed, try these commands manually:
echo    python --version
echo    py --version  
echo    python3 --version
echo.
echo 🛠️ Quick fix: Try running this setup with 'py setup_windows11.bat' instead
pause
exit /b 1

:python_found
echo ✅ Python found: %PYTHON_CMD%
%PYTHON_CMD% --version

echo.
echo 📦 Installing Python dependencies...

REM Install core mnemonic library
%PYTHON_CMD% -m pip install mnemonic>=0.21
if errorlevel 1 (
    echo ❌ Failed to install mnemonic library
    echo 💡 Try running as administrator or check internet connection
    pause
    exit /b 1
)
echo ✅ BIP39 mnemonic library installed

REM Install Selenium for browser automation
%PYTHON_CMD% -m pip install selenium>=4.35.0
if errorlevel 1 (
    echo ❌ Failed to install selenium
    echo 💡 Try running as administrator or check internet connection
    pause
    exit /b 1
)
echo ✅ Selenium browser automation installed

REM Install WebDriver Manager for automatic Edge driver management
%PYTHON_CMD% -m pip install webdriver-manager>=4.0.0
if errorlevel 1 (
    echo ❌ Failed to install webdriver-manager
    echo 💡 Try running as administrator or check internet connection
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
%PYTHON_CMD% -c "
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
    echo 💡 Try running as administrator
    pause
    exit /b 1
)

echo.
echo ================================================================
echo 🎉 INSTALLATION COMPLETE!
echo ================================================================
echo.
echo 🚀 To run the mnemonic recovery tool:
echo    %PYTHON_CMD% server.py
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
echo   • WINDOWS11_RECOVERY_GUIDE.md - Complete guide
echo.
pause