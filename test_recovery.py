#!/usr/bin/env python3
"""
Quick test script for the mnemonic recovery tool
Tests with a known valid mnemonic to ensure everything works
"""

from mnemonic_recovery import MnemonicRecovery

def run_test():
    print("🧪 Testing BIP39 Mnemonic Recovery Tool")
    print("=" * 45)
    
    # Known valid mnemonic: abandon abandon... abandon abandon art
    # We'll provide all words except position 22 (which should be "abandon")
    test_known_words = [
        'abandon', 'abandon', 'abandon', 'abandon', 'abandon', 'abandon',
        'abandon', 'abandon', 'abandon', 'abandon', 'abandon', 'abandon',
        'abandon', 'abandon', 'abandon', 'abandon', 'abandon', 'abandon',
        'abandon', 'abandon', 'abandon',  # positions 1-21
        'abandon', 'art'  # positions 23-24
    ]
    
    print("📝 Test scenario: Known mnemonic missing word at position 22")
    print(f"🎯 Expected missing word: 'abandon'")
    print(f"📊 Testing with {len(test_known_words)} known words")
    
    # Initialize recovery tool
    recovery = MnemonicRecovery()
    
    # Run recovery
    result = recovery.recover_missing_word(test_known_words)
    
    if result:
        print(f"\n✅ Test PASSED!")
        print(f"🔍 Tool successfully found the missing word")
    else:
        print(f"\n❌ Test FAILED!")
        print(f"🔍 Tool could not find the missing word")

if __name__ == "__main__":
    run_test()