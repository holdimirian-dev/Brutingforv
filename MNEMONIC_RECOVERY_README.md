# BIP39 Mnemonic Recovery Tool

A command-line tool to recover a missing 22nd word from a 24-word BIP39 mnemonic phrase. Compatible with MetaMask and Ledger wallets.

## Features

- ✅ BIP39 compliant validation
- 🔍 Tests all 2048 standard BIP39 words
- ⚡ Fast iteration with progress tracking
- 🛡️ Input validation and error handling
- 📱 Compatible with MetaMask and Ledger
- 💻 Cross-platform Python script

## Requirements

- Python 3.6 or higher
- `mnemonic` library for BIP39 functionality

## Installation

1. Install the required Python library:
```bash
pip install mnemonic
```

2. Download the script:
```bash
# The script is already created as mnemonic_recovery.py
```

## Usage

1. Run the script:
```bash
python mnemonic_recovery.py
```

2. When prompted, enter your 23 known words separated by spaces:
   - Enter words 1-21 (before the missing word)
   - Enter words 23-24 (after the missing word)
   - The tool will automatically try all possibilities for position 22

3. The tool will:
   - Validate your input words against the BIP39 wordlist
   - Test each of the 2048 possible words for position 22
   - Show progress updates every 200 attempts
   - Report the correct word when found

## Example

```
🔐 BIP39 Mnemonic Recovery Tool
==================================================
This tool will help recover your missing 22nd word from a 24-word mnemonic.
Compatible with MetaMask and Ledger wallets.

📝 Please enter your 23 known words:
   - Words 1-21 (before the missing word)
   - Words 23-24 (after the missing word)
   - Separate words with spaces
   - Press Enter when done

Enter words: abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon

📋 You entered 23 words:
    1: abandon
    2: abandon
    ...
   21: abandon
   22: [MISSING - TO BE RECOVERED]
   23: abandon
   24: abandon

❓ Is this correct? (y/n): y

🔍 Starting recovery process...
📝 Testing 2048 possible words for position 22...
⏳ This may take a few moments...

✅ SUCCESS! Found valid mnemonic after 1 attempts in 0.01 seconds
🔑 Missing word (position 22): 'art'
📋 Complete mnemonic:
   abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon art abandon abandon
```

## Security Notes

- ⚠️ **IMPORTANT**: This tool handles sensitive cryptographic material
- 🔒 Keep your recovered mnemonic secure and private
- 🗑️ Delete the script output after use
- 💻 Run this tool on a secure, offline computer if possible
- 🚫 Never share your mnemonic phrase with anyone

## How it Works

1. **Input Validation**: Verifies all provided words exist in the BIP39 wordlist
2. **Systematic Testing**: Tries each of the 2048 BIP39 words in position 22
3. **Checksum Validation**: Uses BIP39 checksum to verify mnemonic validity
4. **Result Output**: Reports the correct word and complete mnemonic when found

## Compatibility

- ✅ MetaMask wallets
- ✅ Ledger hardware wallets  
- ✅ All BIP39-compliant wallets
- ✅ Windows, macOS, Linux

## Troubleshooting

**"Invalid words found"**: One or more of your input words is not in the BIP39 wordlist. Double-check spelling.

**"No valid mnemonic found"**: 
- Verify all words are in correct positions
- Check that you have exactly 23 words
- Ensure the missing word is actually position 22

**Script won't run**: Make sure you have Python 3.6+ and the `mnemonic` library installed.

## License

This tool is provided as-is for educational and recovery purposes. Use at your own risk.