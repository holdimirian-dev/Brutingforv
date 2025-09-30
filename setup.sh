#!/bin/bash

# Setup script for BIP39 Mnemonic Recovery Tool
# This script installs required dependencies and sets up the tool

echo "🔐 BIP39 Mnemonic Recovery Tool Setup"
echo "===================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.6 or higher."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip."
    exit 1
fi

echo "✅ pip3 found"

# Install required Python packages
echo "📦 Installing required packages..."
pip3 install mnemonic

if [ $? -eq 0 ]; then
    echo "✅ Successfully installed mnemonic library"
else
    echo "❌ Failed to install mnemonic library"
    exit 1
fi

# Make the recovery script executable
chmod +x mnemonic_recovery.py

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "To run the recovery tool:"
echo "  python3 mnemonic_recovery.py"
echo ""
echo "⚠️  SECURITY REMINDER:"
echo "  - Run this tool on a secure, offline computer"
echo "  - Keep your recovered mnemonic private"
echo "  - Delete outputs after use"