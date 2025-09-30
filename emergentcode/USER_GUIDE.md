# 🔐 BIP39 Mnemonic Recovery Tool - Complete User Guide

## What This Tool Does
This tool helps you recover a missing 22nd word from your 24-word cryptocurrency wallet mnemonic phrase (seed phrase). It works with MetaMask, Ledger, and all BIP39-compatible wallets.

---

## BEFORE YOU START - IMPORTANT SECURITY NOTES ⚠️

### 🔒 SECURITY WARNINGS:
- **NEVER run this on a computer connected to the internet if possible**
- **NEVER share your mnemonic phrase with anyone**
- **DELETE all traces of your mnemonic after recovery**
- **Use a clean, virus-free computer**
- **Close all unnecessary programs before running**

### 🦠 RECOMMENDED: Use an offline computer
1. Download this tool on a USB drive
2. Disconnect your computer from internet
3. Run the recovery tool offline
4. Write down the recovered mnemonic on paper
5. Delete everything before reconnecting to internet

---

## STEP-BY-STEP INSTALLATION GUIDE

### For Windows Users:

#### Step 1: Check if Python is Installed
1. Press `Windows Key + R`
2. Type `cmd` and press Enter
3. In the black window, type: `python --version`
4. Press Enter

**If you see something like "Python 3.x.x"** ✅ Python is installed, go to Step 3
**If you see an error** ❌ Go to Step 2

#### Step 2: Install Python (if needed)
1. Go to https://www.python.org/downloads/
2. Click the big yellow "Download Python" button
3. Run the downloaded file
4. ⚠️ **IMPORTANT**: Check the box "Add Python to PATH" during installation
5. Click "Install Now"
6. When done, restart your computer
7. Repeat Step 1 to verify installation

#### Step 3: Install Required Library
1. Press `Windows Key + R`
2. Type `cmd` and press Enter
3. In the black window, type: `pip install mnemonic`
4. Press Enter and wait for it to finish

#### Step 4: Download and Run the Tool
1. Download all these files to a folder (like Desktop\MnemonicRecovery\):
   - `mnemonic_recovery_gui.py` (the main tool)
   - `setup.bat` (helper script)
2. Double-click `setup.bat` to automatically install requirements
3. To run the tool: Double-click `mnemonic_recovery_gui.py`

---

## HOW TO USE THE TOOL

### Opening the Tool
- Double-click `mnemonic_recovery_gui.py`
- A window will open with 24 numbered boxes

### Entering Your Words

#### 🎯 THE GOLDEN RULE:
- Enter your 23 known words in their EXACT positions
- Leave position 22 EMPTY (this is what we're finding)
- Position 22 will be grayed out and show "[MISSING]"

#### Example:
If your mnemonic is: `word1 word2 word3... word21 [MISSING] word23 word24`

1. Type `word1` in box 1
2. Type `word2` in box 2
3. Continue until box 21
4. **SKIP BOX 22** (leave empty - it's disabled)
5. Type `word23` in box 23
6. Type `word24` in box 24

### Starting Recovery
1. After entering all 23 words, click "🔍 Start Recovery"
2. The tool will automatically test all 2048 possible BIP39 words
3. Watch the progress bar and messages in the results area
4. **BE PATIENT** - this can take a few minutes

### When Recovery Completes
- ✅ **SUCCESS**: You'll see the missing word and complete mnemonic
- ❌ **FAILED**: Double-check your words are correct and in right positions

---

## USING WITH YOUR LEDGER DEVICE

### Option 1: Test the Recovered Mnemonic
1. **NEVER enter your real mnemonic directly into MetaMask on a connected computer**
2. After recovery, write the complete mnemonic on paper
3. Use Ledger Live to restore your wallet with the complete mnemonic
4. Verify the addresses match your expected wallet

### Option 2: Safer Method (Recommended)
1. Use the recovered mnemonic to restore your Ledger device
2. Set up the Ledger as new with the complete mnemonic
3. Connect Ledger to MetaMask as hardware wallet
4. This keeps your mnemonic secure in the hardware device

---

## TESTING THE TOOL (Recommended First Step)

### Before Using Your Real Words:
1. Click "🧪 Load Test Data" button
2. This loads a test mnemonic with known missing word
3. Click "🔍 Start Recovery"
4. It should find the missing word "abandon" quickly
5. This confirms the tool works correctly

---

## TROUBLESHOOTING

### ❌ "Invalid Word" Error
- **Problem**: One of your words isn't in the BIP39 wordlist
- **Solution**: Check spelling carefully. Words must be exact BIP39 words

### ❌ "Too Many Empty Positions" Error
- **Problem**: You left more than just position 22 empty
- **Solution**: Fill in all boxes except 22

### ❌ "Wrong Empty Position" Error
- **Problem**: You left a position other than 22 empty
- **Solution**: Only position 22 should be empty

### ❌ Tool Won't Start
- **Problem**: Python or mnemonic library not installed
- **Solution**: Run `setup.bat` or manually install: `pip install mnemonic`

### ❌ "No Valid Mnemonic Found"
Possible causes:
1. **Wrong word positions**: Verify each word is in its correct position
2. **Spelling errors**: Double-check every word
3. **Wrong missing position**: Maybe it's not position 22 that's missing
4. **Damaged mnemonic**: The original might have more errors

---

## FREQUENTLY ASKED QUESTIONS

### Q: Is this tool safe?
A: The tool runs locally on your computer and doesn't send data anywhere. However, always use offline for maximum security.

### Q: How long does recovery take?
A: Usually under 2 minutes. In worst case, it tests all 2048 words.

### Q: Can I recover other missing positions?
A: This tool is specifically for position 22. For other positions, the code would need modification.

### Q: What if I have multiple missing words?
A: This tool only works for ONE missing word. Multiple missing words require different approaches.

### Q: Will this work with my hardware wallet?
A: Yes! The recovered mnemonic works with any BIP39-compatible wallet (Ledger, Trezor, MetaMask, etc.)

---

## FILES INCLUDED

- `mnemonic_recovery_gui.py` - Main GUI tool (user-friendly)
- `mnemonic_recovery.py` - Command-line version  
- `setup.bat` - Windows setup script
- `setup.sh` - Linux/Mac setup script
- `test_recovery.py` - Test script
- `MNEMONIC_RECOVERY_README.md` - Technical documentation

---

## FINAL SECURITY REMINDERS 🔒

1. **Use offline** if dealing with significant funds
2. **Delete everything** after successful recovery
3. **Never share** your mnemonic with anyone
4. **Write on paper**, not digital files
5. **Verify addresses** match before moving large amounts
6. **Keep backup** of recovered mnemonic in secure location

---

## Emergency Contacts

If you're having issues:
1. Double-check all steps in this guide
2. Try the test data first to verify tool works
3. Ensure all words are spelled exactly as in BIP39 wordlist
4. Consider trying on a different computer if problems persist

**Remember: This tool is for educational and recovery purposes. Always prioritize security when dealing with cryptocurrency wallets.**