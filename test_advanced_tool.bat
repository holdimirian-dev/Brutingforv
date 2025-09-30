@echo off
REM Test script for Advanced BIP39 Recovery Tool

echo.
echo 🧪 Testing Advanced BIP39 Recovery Tool
echo =======================================

REM Find Python
set PYTHON_CMD=

py --version >nul 2>&1
if not errorlevel 1 (
    set PYTHON_CMD=py
    goto :test_tool
)

python --version >nul 2>&1
if not errorlevel 1 (
    set PYTHON_CMD=python
    goto :test_tool
)

python3 --version >nul 2>&1
if not errorlevel 1 (
    set PYTHON_CMD=python3
    goto :test_tool
)

echo ❌ Python not found! Please install Python first.
pause
exit /b 1

:test_tool
echo ✅ Using Python command: %PYTHON_CMD%
echo.

REM Run the test
%PYTHON_CMD% test_advanced_tool.py

if errorlevel 1 (
    echo.
    echo ❌ Tests failed. Please run setup_advanced.bat
) else (
    echo.
    echo 🎉 Tests completed!
)

echo.
pause