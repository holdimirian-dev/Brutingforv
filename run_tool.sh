#!/bin/bash

# Quick Start Script for BIP39 Mnemonic Recovery Tool
# This script runs the GUI version of the tool

echo "🔐 Starting BIP39 Mnemonic Recovery Tool..."
echo "=========================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.6 or higher."
    exit 1
fi

# Check if GUI libraries are available (for Linux users)
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    python3 -c "import tkinter" 2>/dev/null
    if [ $? -ne 0 ]; then
        echo "❌ tkinter not found. Please install it:"
        echo "   Ubuntu/Debian: sudo apt-get install python3-tk"
        echo "   CentOS/RHEL: sudo yum install tkinter"
        exit 1
    fi
fi

# Check if mnemonic library is installed
python3 -c "import mnemonic" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ mnemonic library not found. Installing..."
    pip3 install mnemonic
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install mnemonic library"
        exit 1
    fi
fi

echo "✅ All dependencies found"
echo "🚀 Starting GUI..."
echo ""

# Run the GUI tool
python3 mnemonic_recovery_gui.py