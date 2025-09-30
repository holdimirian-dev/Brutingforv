#!/usr/bin/env python3
"""
Test script for the Advanced BIP39 Mnemonic Recovery Tool
Run this to verify everything is working correctly
"""

def test_dependencies():
    """Test all required dependencies"""
    print("🧪 Testing Advanced BIP39 Recovery Tool Dependencies")
    print("=" * 55)
    
    success = True
    
    # Test Python version
    import sys
    if sys.version_info >= (3, 6):
        print(f"✅ Python version: {sys.version.split()[0]}")
    else:
        print(f"❌ Python version too old: {sys.version.split()[0]} (need 3.6+)")
        success = False
    
    # Test core libraries
    try:
        from mnemonic import Mnemonic
        mnemo = Mnemonic("english")
        print(f"✅ mnemonic library: {len(mnemo.wordlist)} words loaded")
    except ImportError:
        print("❌ mnemonic library missing - run setup_advanced.bat")
        success = False
    except Exception as e:
        print(f"❌ mnemonic library error: {e}")
        success = False
    
    # Test GUI library
    try:
        import tkinter as tk
        print("✅ tkinter GUI library available")
    except ImportError:
        print("❌ tkinter GUI library missing")
        success = False
    
    # Test optional browser automation
    try:
        import selenium
        print("✅ selenium browser automation available")
    except ImportError:
        print("⚠️  selenium not installed - browser automation disabled")
        print("   Tool will still work for basic recovery")
    
    # Test core BIP39 functionality
    try:
        test_mnemonic = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon art"
        if mnemo.check(test_mnemonic):
            print("✅ BIP39 validation working correctly")
        else:
            print("❌ BIP39 validation failed")
            success = False
    except:
        print("❌ BIP39 testing failed")
        success = False
    
    print("=" * 55)
    if success:
        print("🎉 ALL TESTS PASSED - Advanced tool ready to use!")
        print("🚀 Run: python mnemonic_recovery_advanced.py")
    else:
        print("❌ Some tests failed - please run setup_advanced.bat")
        print("📖 Check ADVANCED_USER_GUIDE.md for troubleshooting")
    
    return success

def test_file_syntax():
    """Test if the main file has correct syntax"""
    print("\n🔍 Testing file syntax...")
    
    try:
        import py_compile
        py_compile.compile('mnemonic_recovery_advanced.py', doraise=True)
        print("✅ Python syntax is correct")
        return True
    except py_compile.PyCompileError as e:
        print(f"❌ Syntax error in file: {e}")
        return False
    except FileNotFoundError:
        print("❌ mnemonic_recovery_advanced.py file not found")
        return False

if __name__ == "__main__":
    try:
        # Test file syntax first
        syntax_ok = test_file_syntax()
        
        if syntax_ok:
            # Test dependencies
            deps_ok = test_dependencies()
            
            if deps_ok:
                print("\n🎯 Ready to recover your mnemonic!")
                print("📖 Read ADVANCED_USER_GUIDE.md for instructions")
        
        input("\nPress Enter to exit...")
        
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        input("Press Enter to exit...")