@echo off
REM Emergency Python Fix Script - Manual Installation
REM Use this if setup.bat keeps failing

echo.
echo ========================================
echo 🆘 Emergency Python Fix for BIP39 Tool
echo ========================================
echo.

echo 🔍 Let's find your Python installation...
echo.

REM Test all possible Python commands
echo Testing different Python commands:
echo.

echo [TEST 1] py --version
py --version 2>nul
if not errorlevel 1 (
    echo ✅ 'py' command works!
    echo.
    echo 📦 Installing mnemonic library using 'py'...
    py -m pip install mnemonic
    if not errorlevel 1 (
        echo ✅ SUCCESS! Library installed.
        echo.
        echo 🚀 To run the tool, use:
        echo   py mnemonic_recovery_gui.py
        echo.
        goto :success
    )
)

echo.
echo [TEST 2] python --version
python --version 2>nul
if not errorlevel 1 (
    echo ✅ 'python' command works!
    echo.
    echo 📦 Installing mnemonic library using 'python'...
    python -m pip install mnemonic
    if not errorlevel 1 (
        echo ✅ SUCCESS! Library installed.
        echo.
        echo 🚀 To run the tool, use:
        echo   python mnemonic_recovery_gui.py
        echo.
        goto :success
    )
)

echo.
echo [TEST 3] python3 --version
python3 --version 2>nul
if not errorlevel 1 (
    echo ✅ 'python3' command works!
    echo.
    echo 📦 Installing mnemonic library using 'python3'...
    python3 -m pip install mnemonic
    if not errorlevel 1 (
        echo ✅ SUCCESS! Library installed.
        echo.
        echo 🚀 To run the tool, use:
        echo   python3 mnemonic_recovery_gui.py
        echo.
        goto :success
    )
)

echo.
echo ❌ None of the Python commands work!
echo.
echo 🔧 SOLUTIONS:
echo.
echo 1. EASIEST: Reinstall Python
echo    • Go to https://www.python.org/downloads/
echo    • Download Python 3.13
echo    • ✅ CHECK "Add Python to PATH" during installation
echo    • Restart computer
echo.
echo 2. MANUAL: Add Python to PATH
echo    • Find where Python is installed (usually C:\Python313\)
echo    • Add that folder to your Windows PATH variable
echo.
echo 3. ALTERNATIVE: Use full path to Python
echo    • Find python.exe file on your computer
echo    • Run it with full path, like:
echo    • "C:\Python313\python.exe" mnemonic_recovery_gui.py
echo.
goto :end

:success
echo ========================================
echo 🎉 INSTALLATION SUCCESSFUL!
echo ========================================
echo.
echo The mnemonic library is now installed.
echo You can run the recovery tool.
echo.
echo 📖 Read USER_GUIDE.md for instructions on using the tool.
echo.

:end
echo Press any key to exit...
pause >nul