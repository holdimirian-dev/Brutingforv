#!/usr/bin/env python3
"""
Simple test to verify the GUI tool works correctly
"""

import tkinter as tk
import sys
import os

def test_gui_dependencies():
    print("🧪 Testing GUI Tool Dependencies")
    print("=" * 40)
    
    # Test Python version
    if sys.version_info < (3, 6):
        print("❌ Python 3.6+ required")
        return False
    print("✅ Python version OK:", sys.version.split()[0])
    
    # Test tkinter
    try:
        import tkinter
        print("✅ tkinter available")
    except ImportError:
        print("❌ tkinter not available")
        return False
    
    # Test mnemonic library
    try:
        from mnemonic import Mnemonic
        mnemo = Mnemonic("english")
        print("✅ mnemonic library working")
        print(f"✅ BIP39 wordlist loaded ({len(mnemo.wordlist)} words)")
    except ImportError:
        print("❌ mnemonic library not found - run: pip install mnemonic")
        return False
    except Exception as e:
        print(f"❌ mnemonic library error: {e}")
        return False
    
    # Test GUI creation
    try:
        root = tk.Tk()
        root.withdraw()  # Hide the window
        print("✅ GUI window creation OK")
        root.destroy()
    except Exception as e:
        print(f"❌ GUI creation failed: {e}")
        return False
    
    print("=" * 40)
    print("✅ All tests passed! GUI tool should work correctly.")
    return True

if __name__ == "__main__":
    if test_gui_dependencies():
        print("\n🚀 Ready to run the GUI tool!")
        print("Run: python mnemonic_recovery_gui.py")
    else:
        print("\n❌ Please fix the issues above before running the GUI tool.")
        input("Press Enter to exit...")
    
    input("\nPress Enter to exit...")