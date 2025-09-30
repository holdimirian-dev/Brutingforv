@echo off
REM Python Detection and Troubleshooting Tool
REM Helps diagnose Python installation issues on Windows 11

echo.
echo ================================================================
echo 🔧 Python Detection and Troubleshooting Tool
echo ================================================================
echo.

echo 🔍 Checking for Python installations...
echo.

REM Test different Python commands
echo Testing 'python' command:
python --version 2>&1
if not errorlevel 1 (
    echo ✅ 'python' command works
) else (
    echo ❌ 'python' command not found
)

echo.
echo Testing 'py' command:
py --version 2>&1
if not errorlevel 1 (
    echo ✅ 'py' command works (Python Launcher)
) else (
    echo ❌ 'py' command not found
)

echo.
echo Testing 'python3' command:
python3 --version 2>&1
if not errorlevel 1 (
    echo ✅ 'python3' command works
) else (
    echo ❌ 'python3' command not found
)

echo.
echo 📁 Checking common installation paths...

if exist "%LOCALAPPDATA%\Programs\Python\" (
    echo ✅ Found Python in user directory:
    dir "%LOCALAPPDATA%\Programs\Python\" /b
) else (
    echo ❌ No Python found in %LOCALAPPDATA%\Programs\Python\
)

if exist "%PROGRAMFILES%\Python*\" (
    echo ✅ Found Python in Program Files:
    dir "%PROGRAMFILES%\Python*" /b 2>nul
) else (
    echo ❌ No Python found in Program Files
)

if exist "%PROGRAMFILES(X86)%\Python*\" (
    echo ✅ Found Python in Program Files (x86):
    dir "%PROGRAMFILES(X86)%\Python*" /b 2>nul
) else (
    echo ❌ No Python found in Program Files (x86)
)

echo.
echo 🌐 Checking PATH environment variable...
echo PATH contains:
echo %PATH% | findstr /i python
if errorlevel 1 (
    echo ❌ No Python paths found in PATH environment variable
) else (
    echo ✅ Python paths found in PATH
)

echo.
echo ================================================================
echo 💡 TROUBLESHOOTING SUGGESTIONS
echo ================================================================
echo.

echo If no Python commands work:
echo   1. Install Python from: https://python.org/downloads/
echo   2. ⚠️  IMPORTANT: Check "Add Python to PATH" during installation
echo   3. Or install from Microsoft Store: search "Python"
echo   4. Restart Command Prompt after installation
echo.

echo If Python is installed but not in PATH:
echo   1. Search for "Environment Variables" in Start menu
echo   2. Click "Environment Variables" button
echo   3. Under "System variables", find and edit "Path"
echo   4. Add your Python installation directory
echo   5. Restart Command Prompt
echo.

echo Quick installation (Microsoft Store):
echo   1. Open Microsoft Store
echo   2. Search for "Python 3.11" or "Python 3.12"
echo   3. Install the official Python version
echo   4. This automatically adds Python to PATH
echo.

echo Alternative approach:
echo   If 'py' command works but 'python' doesn't:
echo   - Use 'py server.py' instead of 'python server.py'
echo   - Modify the batch files to use 'py' instead of 'python'
echo.

pause