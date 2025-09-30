# Windows 11 Terminal BIP39 Mnemonic Recovery Guide

## Overview
This tool helps recover missing words from BIP39 mnemonic phrases (12, 24 words) with MetaMask validation using Microsoft Edge browser automation. Designed specifically for local Windows 11 execution with terminal interface.

## 🚀 Quick Start

### 1. Installation
```batch
# Run the setup script
setup_windows11.bat
```

### 2. Launch Tool
```batch
# Start the recovery tool
python server.py

# OR use the runner script
run_recovery.bat
```

## 📋 Step-by-Step Usage

### Phase 1: Setup
1. **Run Setup Script**: Double-click `setup_windows11.bat`
2. **Install Dependencies**: Script will install Python libraries
3. **Verify Edge**: Script checks Microsoft Edge installation
4. **Test Installation**: Automated verification of all components

### Phase 2: Recovery Process
1. **Launch Tool**: Run `python server.py`
2. **Enter Missing Position**: Specify which word position is missing (1-24)
3. **Input Known Words**: Enter your 23 known words one by one
4. **Enable MetaMask Testing**: Choose whether to test with MetaMask
5. **Start Recovery**: Tool searches all 2048 BIP39 words
6. **MetaMask Validation**: For each valid word found, test in MetaMask
7. **Results**: Get confirmed working mnemonic phrases

### Phase 3: Validation
1. **Edge Browser Opens**: MetaMask website loads automatically
2. **Manual Testing**: Import each valid mnemonic to MetaMask
3. **Confirmation**: Verify wallet addresses and balances
4. **Result Logging**: Tool tracks which mnemonics work

## 🛠️ Technical Features

### Core Functionality
- **Any Missing Position**: Not limited to position 22, supports 1-24
- **BIP39 Compliance**: Full validation against official wordlist
- **Progress Tracking**: Real-time progress with attempts/second
- **Error Handling**: Comprehensive input validation

### Browser Automation
- **Microsoft Edge**: Uses Edge WebDriver for Windows 11 compatibility
- **Automatic Setup**: WebDriver Manager handles driver installation
- **MetaMask Integration**: Opens MetaMask website for wallet testing
- **Manual Validation**: User confirms wallet import success/failure

### Security Features
- **Local Execution**: No network communication except MetaMask testing
- **Input Validation**: Verifies all words against BIP39 wordlist
- **Progress Indicators**: Clear feedback during long operations
- **Error Recovery**: Handles browser and network errors gracefully

## 📊 Example Session

```
🔐 BIP39 Mnemonic Recovery Tool - Terminal Edition
============================================================
📊 Loaded BIP39 wordlist with 2048 words
🪟 Windows 11 | 🌐 Edge WebDriver | 📱 MetaMask Integration
============================================================

📍 Enter the missing word position (1-24, default 22): 22

📝 Enter your 23 known words (missing position 22):
Position  1: abandon
Position  2: abandon
...
Position 21: abandon
Position 22: [MISSING - WILL BE RECOVERED]
Position 23: abandon
Position 24: art
done

❓ Is this correct? (y/n): y

🧪 Test valid words with MetaMask? (y/n, default y): y

🔍 Starting recovery process...
📍 Missing position: 22
📝 Testing 2048 possible words...
🧪 MetaMask testing: Enabled

🌐 Setting up Microsoft Edge WebDriver...
✅ Edge WebDriver setup successful

✅ VALID WORD FOUND #1!
   Word: 'abandon' (position 22)
   Attempts: 1/2048
   Time: 0.05 seconds
   Mnemonic: abandon abandon ... abandon abandon art

🧪 Testing with MetaMask...
🌐 MetaMask website opened
📋 AUTOMATED TESTING INSTRUCTIONS:
   1. Install MetaMask extension if not present
   2. Open MetaMask and select 'Import wallet'
   3. Enter this mnemonic phrase:
      abandon abandon ... abandon abandon art
   4. If import succeeds ✅: Word 'abandon' is CORRECT
   5. If import fails ❌: Word 'abandon' is WRONG

⏸️  Press Enter after testing this mnemonic in MetaMask...
🔍 Did the mnemonic import successfully? (y/n/skip): y
🎉 CONFIRMED: This mnemonic works with MetaMask!

🎯 Found confirmed working mnemonic!
Continue searching for more possibilities? (y/n): n

============================================================
🎉 RECOVERY COMPLETED SUCCESSFULLY!
⏱️  Time: 15.32 seconds
🔍 Total attempts: 1
✅ Valid combinations found: 1

RESULT #1:
  🎯 Position 22: 'abandon'
  📊 Found at attempt: 1
  ✅ MetaMask: CONFIRMED WORKING
  📋 Complete mnemonic:
     abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon art

============================================================
💾 You can now use these mnemonics with MetaMask or hardware wallets
⚠️  IMPORTANT: Test with small amounts first!
⚠️  Keep these mnemonics secure and delete when done!
```

## ⚠️ Security Recommendations

### Before Recovery
- **Secure Environment**: Use offline computer when possible
- **Clean System**: Ensure computer is free of malware
- **Backup Data**: Backup any existing important data
- **Private Space**: Use tool in private, secure location

### During Recovery
- **No Screenshots**: Don't capture screen during mnemonic display
- **Verify Input**: Double-check all known words are correct
- **One at a Time**: Test one mnemonic at a time in MetaMask
- **Small Amounts**: Only test with minimal funds initially

### After Recovery
- **Secure Storage**: Store recovered mnemonic in secure location
- **Delete Traces**: Clear terminal history and browser data
- **Test Thoroughly**: Verify all wallet functions before using
- **Document Safely**: If needed, store backup securely offline

## 🔧 Troubleshooting

### Installation Issues
```
❌ Python not found
📋 Solution: Install Python 3.6+ from python.org
```

```
❌ Edge not found  
📋 Solution: Install Microsoft Edge from microsoft.com/edge
```

```
❌ Dependencies failed
📋 Solution: Run 'pip install mnemonic selenium webdriver-manager'
```

### Runtime Issues
```
❌ WebDriver setup failed
📋 Solution: Check Edge installation, update webdriver-manager
```

```
❌ Invalid word detected
📋 Solution: Check spelling against BIP39 wordlist
```

```
❌ No valid words found
📋 Solution: Verify all known words and positions are correct
```

### MetaMask Testing Issues
```
❌ Browser won't open
📋 Solution: Check Edge installation, disable antivirus temporarily
```

```
❌ MetaMask not responding
📋 Solution: Install MetaMask extension, refresh page
```

## 📁 File Structure

```
/BIP39-Recovery/
├── server.py                 # Main terminal application
├── setup_windows11.bat       # Windows 11 installer
├── run_recovery.bat          # Quick launcher
├── mnemonic_recovery.py      # Legacy basic version
├── mnemonic_recovery_advanced.py  # Legacy GUI version
├── metamask_integration.py   # Browser automation module
├── test_advanced_tool.py     # Dependency tester
└── docs/
    ├── README.md
    ├── MNEMONIC_RECOVERY_README.md
    └── USER_GUIDE.md
```

## 🆘 Support

### Common Issues
1. **Python Path Issues**: Add Python to system PATH
2. **Edge Driver Problems**: Update Edge browser to latest version
3. **Permission Errors**: Run as administrator if needed
4. **Network Issues**: Disable VPN/proxy for MetaMask testing

### Getting Help
- Check error messages carefully
- Run dependency test: `python test_advanced_tool.py`
- Verify Edge installation and version
- Ensure Python 3.6+ is installed

### Known Limitations
- Requires Windows 11 and Microsoft Edge
- MetaMask testing requires internet connection
- Only supports English BIP39 wordlist
- GUI interactions require manual confirmation

## 📈 Advanced Usage

### Batch Testing
The tool can find multiple valid words for the same position. This happens when:
- Multiple valid checksums exist
- Different words create valid mnemonics
- Testing helps identify the correct wallet

### Custom Configurations
- Modify missing position for any word 1-24
- Skip MetaMask testing for faster results
- Continue searching after finding first valid word
- Handle multiple error scenarios gracefully

### Performance Tips
- Close other browser windows during testing
- Disable unnecessary browser extensions
- Use wired internet for MetaMask testing
- Run on computer with sufficient RAM (4GB+)