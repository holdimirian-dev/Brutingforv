#!/usr/bin/env python3
"""
BIP39 Mnemonic Recovery Tool
Recovers missing 22nd word from a 24-word mnemonic phrase
Compatible with MetaMask and Ledger wallets
"""

import sys
import time
from mnemonic import Mnemonic


class MnemonicRecovery:
    def __init__(self):
        self.mnemo = Mnemonic("english")
        self.wordlist = self.mnemo.wordlist
        print(f"Loaded BIP39 wordlist with {len(self.wordlist)} words")
    
    def validate_input_words(self, words):
        """Validate that all input words are in the BIP39 wordlist"""
        invalid_words = []
        for i, word in enumerate(words):
            if word.lower() not in self.wordlist:
                invalid_words.append(f"Position {i+1}: '{word}'")
        
        if invalid_words:
            print("❌ Invalid words found (not in BIP39 wordlist):")
            for invalid in invalid_words:
                print(f"   {invalid}")
            return False
        return True
    
    def recover_missing_word(self, known_words):
        """
        Recover the missing 22nd word by trying all possibilities
        
        Args:
            known_words: List of 23 words (missing word at position 22 should be None or empty)
        
        Returns:
            Complete valid mnemonic or None if not found
        """
        if len(known_words) != 23:
            raise ValueError("Must provide exactly 23 words (missing the 22nd)")
        
        # Validate input words
        valid_words = [w for w in known_words if w and w.strip()]
        if not self.validate_input_words(valid_words):
            return None
        
        print(f"\n🔍 Starting recovery process...")
        print(f"📝 Testing {len(self.wordlist)} possible words for position 22...")
        print("⏳ This may take a few moments...\n")
        
        attempts = 0
        start_time = time.time()
        
        # Try each word from BIP39 wordlist in position 22
        for word_candidate in self.wordlist:
            attempts += 1
            
            # Create complete mnemonic with candidate word
            test_mnemonic = known_words[:21] + [word_candidate] + known_words[21:]
            mnemonic_phrase = " ".join(test_mnemonic)
            
            # Test if this mnemonic is valid
            if self.mnemo.check(mnemonic_phrase):
                elapsed_time = time.time() - start_time
                print(f"✅ SUCCESS! Found valid mnemonic after {attempts} attempts in {elapsed_time:.2f} seconds")
                print(f"🔑 Missing word (position 22): '{word_candidate}'")
                print(f"📋 Complete mnemonic:")
                print(f"   {mnemonic_phrase}")
                return mnemonic_phrase
            
            # Progress indicator
            if attempts % 200 == 0:
                elapsed = time.time() - start_time
                rate = attempts / elapsed if elapsed > 0 else 0
                print(f"⏱️  Tested {attempts}/{len(self.wordlist)} words ({rate:.1f} words/sec)")
        
        elapsed_time = time.time() - start_time
        print(f"❌ No valid mnemonic found after testing all {attempts} words in {elapsed_time:.2f} seconds")
        print("💡 Please verify your input words are correct and in the right positions")
        return None


def get_user_input():
    """Get the 23 known words from user input"""
    print("🔐 BIP39 Mnemonic Recovery Tool")
    print("=" * 50)
    print("This tool will help recover your missing 22nd word from a 24-word mnemonic.")
    print("Compatible with MetaMask and Ledger wallets.\n")
    
    print("📝 Please enter your 23 known words:")
    print("   - Words 1-21 (before the missing word)")
    print("   - Words 23-24 (after the missing word)")
    print("   - Separate words with spaces")
    print("   - Press Enter when done\n")
    
    words_input = input("Enter words: ").strip().lower()
    
    if not words_input:
        print("❌ No input provided. Exiting...")
        return None
    
    words = words_input.split()
    
    if len(words) != 23:
        print(f"❌ Expected 23 words, but got {len(words)}. Please try again.")
        return None
    
    print(f"\n📋 You entered {len(words)} words:")
    for i, word in enumerate(words):
        pos = i + 1 if i < 21 else i + 2  # Account for missing position 22
        print(f"   {pos:2d}: {word}")
    
    print(f"   22: [MISSING - TO BE RECOVERED]")
    
    confirm = input("\n❓ Is this correct? (y/n): ").lower().strip()
    if confirm != 'y':
        print("Operation cancelled.")
        return None
    
    return words


def main():
    try:
        # Get user input
        known_words = get_user_input()
        if not known_words:
            sys.exit(1)
        
        # Initialize recovery tool
        recovery = MnemonicRecovery()
        
        # Attempt recovery
        result = recovery.recover_missing_word(known_words)
        
        if result:
            print(f"\n🎉 Recovery completed successfully!")
            print(f"💾 You can now use this mnemonic with MetaMask or your Ledger device.")
            print(f"⚠️  IMPORTANT: Keep this mnemonic secure and delete this output when done.")
        else:
            print(f"\n😞 Recovery failed. Please check your input words and try again.")
            print(f"💡 Make sure all words are spelled correctly and in the right positions.")
        
    except KeyboardInterrupt:
        print(f"\n\n⏹️  Operation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()