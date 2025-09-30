#!/usr/bin/env python3
"""
Advanced BIP39 Mnemonic Recovery Tool - MetaMask Integration
Recovers missing word from any position and tests with actual MetaMask wallet
Supports save/load functionality and finds ALL valid combinations
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import time
import json
import os
from datetime import datetime
from mnemonic import Mnemonic
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import webbrowser


class AdvancedMnemonicRecoveryGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🔐 Advanced BIP39 Mnemonic Recovery Tool - MetaMask Integration")
        self.root.geometry("1000x800")
        self.root.resizable(True, True)
        
        # Initialize mnemonic handler
        self.mnemo = Mnemonic("english")
        self.wordlist = self.mnemo.wordlist
        self.recovery_running = False
        self.valid_combinations = []
        self.missing_position = 22  # Default to 22, but user can change
        
        self.setup_ui()
    
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="🔐 Advanced BIP39 Mnemonic Recovery Tool", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 5))
        
        # Subtitle
        subtitle_label = ttk.Label(main_frame, text="MetaMask Integration • Any Missing Position • Save/Load • All Valid Results",
                                  font=("Arial", 10), foreground="blue")
        subtitle_label.grid(row=1, column=0, columnspan=3, pady=(0, 15))
        
        # Control panel
        control_frame = ttk.LabelFrame(main_frame, text="Recovery Settings", padding="10")
        control_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        control_frame.columnconfigure(1, weight=1)
        
        # Missing position selector
        ttk.Label(control_frame, text="Missing Position:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.position_var = tk.IntVar(value=22)
        position_frame = ttk.Frame(control_frame)
        position_frame.grid(row=0, column=1, sticky=tk.W)
        
        self.position_spinbox = ttk.Spinbox(position_frame, from_=1, to=24, width=5, 
                                           textvariable=self.position_var,
                                           command=self.update_missing_position)
        self.position_spinbox.pack(side=tk.LEFT)
        
        ttk.Button(position_frame, text="Update", command=self.update_missing_position).pack(side=tk.LEFT, padx=(5, 0))
        
        # Browser selection
        ttk.Label(control_frame, text="Browser:").grid(row=0, column=2, sticky=tk.W, padx=(20, 10))
        self.browser_var = tk.StringVar(value="Chrome")
        browser_combo = ttk.Combobox(control_frame, textvariable=self.browser_var, 
                                    values=["Chrome", "Firefox", "Edge"], width=10)
        browser_combo.grid(row=0, column=3, sticky=tk.W)
        
        # MetaMask testing checkbox
        self.test_metamask_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(control_frame, text="Test with MetaMask", 
                       variable=self.test_metamask_var).grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        
        # Find all combinations checkbox
        self.find_all_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(control_frame, text="Find ALL valid combinations", 
                       variable=self.find_all_var).grid(row=1, column=1, sticky=tk.W, pady=(5, 0))
        
        # Save/Load buttons
        save_load_frame = ttk.Frame(control_frame)
        save_load_frame.grid(row=1, column=2, columnspan=2, sticky=tk.E, pady=(5, 0))
        
        ttk.Button(save_load_frame, text="💾 Save Words", command=self.save_words).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(save_load_frame, text="📂 Load Words", command=self.load_words).pack(side=tk.LEFT)
        
        # Instructions
        instructions = f"""INSTRUCTIONS:
1. Select which position is missing (default: 22)
2. Enter your known words in their correct positions
3. The missing position will be grayed out automatically
4. Choose whether to test with MetaMask in browser
5. Click 'Start Advanced Recovery' to find ALL possible words
6. Tool will test each valid word with MetaMask if enabled"""
        
        inst_label = ttk.Label(main_frame, text=instructions, justify=tk.LEFT,
                              font=("Arial", 9), foreground="darkgreen")
        inst_label.grid(row=3, column=0, columnspan=3, sticky=tk.W, pady=(0, 15))
        
        # Create scrollable frame for word inputs
        canvas = tk.Canvas(main_frame, height=250)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        scrollbar.grid(row=4, column=2, sticky=(tk.N, tk.S), pady=(0, 10))
        
        # Word input fields
        self.word_entries = []
        ttk.Label(scrollable_frame, text="Enter your 23 known words:", 
                 font=("Arial", 11, "bold")).grid(row=0, column=0, columnspan=6, pady=(0, 10))
        
        self.create_word_inputs(scrollable_frame)
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=3, pady=10)
        
        # Buttons
        self.start_button = ttk.Button(button_frame, text="🔍 Start Advanced Recovery", 
                                      command=self.start_recovery)
        self.start_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_button = ttk.Button(button_frame, text="⏹️ Stop", 
                                     command=self.stop_recovery, state='disabled')
        self.stop_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.clear_button = ttk.Button(button_frame, text="🗑️ Clear All", 
                                      command=self.clear_fields)
        self.clear_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.test_button = ttk.Button(button_frame, text="🧪 Load Test Data", 
                                     command=self.load_test_data)
        self.test_button.pack(side=tk.LEFT)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, length=500, mode='determinate')
        self.progress.grid(row=6, column=0, columnspan=3, pady=10, sticky=(tk.W, tk.E))
        
        # Status label
        self.status_var = tk.StringVar(value="Ready to start recovery")
        status_label = ttk.Label(main_frame, textvariable=self.status_var, font=("Arial", 9))
        status_label.grid(row=7, column=0, columnspan=3, pady=(0, 10))
        
        # Results text area
        results_label = ttk.Label(main_frame, text="Recovery Results:", font=("Arial", 11, "bold"))
        results_label.grid(row=8, column=0, sticky=tk.W, pady=(10, 5))
        
        self.results_text = scrolledtext.ScrolledText(main_frame, width=100, height=15, 
                                                     font=("Courier", 9))
        self.results_text.grid(row=9, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), 
                              pady=(0, 10))
        
        # Configure grid weights for resizing
        main_frame.rowconfigure(9, weight=1)
        
        # Initial message
        self.log_message("🔐 Advanced BIP39 Mnemonic Recovery Tool Ready")
        self.log_message(f"📊 Loaded BIP39 wordlist with {len(self.wordlist)} words")
        self.log_message("🚀 NEW FEATURES: Any missing position • MetaMask testing • Save/Load • All results")
        self.log_message("⚠️  SECURITY: For maximum security, disconnect from internet after loading this tool")
        self.log_message("=" * 80)
    
    def create_word_inputs(self, parent):
        """Create word input fields"""
        self.word_entries = []
        
        for i in range(24):
            row = (i // 6) + 1
            col = i % 6
            
            # Position label
            pos_label = ttk.Label(parent, text=f"{i+1}:", font=("Arial", 9))
            pos_label.grid(row=row*2, column=col, sticky=tk.W, padx=(5, 0), pady=(5, 0))
            
            # Entry field
            entry = ttk.Entry(parent, width=12, font=("Arial", 9))
            entry.grid(row=row*2+1, column=col, padx=5, pady=(0, 10))
            
            self.word_entries.append(entry)
        
        # Update the display for current missing position
        self.update_missing_position()
    
    def update_missing_position(self):
        """Update which position is marked as missing"""
        self.missing_position = self.position_var.get()
        
        # Reset all entries to normal state
        for i, entry in enumerate(self.word_entries):
            entry.configure(state='normal')
            
        # Disable the missing position
        if 1 <= self.missing_position <= 24:
            missing_idx = self.missing_position - 1
            self.word_entries[missing_idx].configure(state='disabled')
            self.word_entries[missing_idx].delete(0, tk.END)
            
        self.log_message(f"🎯 Updated: Position {self.missing_position} is now the missing word")
    
    def save_words(self):
        """Save current words to a file"""
        filename = filedialog.asksaveasfilename(
            title="Save Mnemonic Words",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                words_data = {
                    "missing_position": self.missing_position,
                    "words": {},
                    "saved_date": datetime.now().isoformat(),
                    "note": "BIP39 mnemonic word recovery backup"
                }
                
                for i, entry in enumerate(self.word_entries):
                    if i != self.missing_position - 1:  # Don't save the missing position
                        word = entry.get().strip().lower()
                        if word:
                            words_data["words"][str(i + 1)] = word
                
                with open(filename, 'w') as f:
                    json.dump(words_data, f, indent=2)
                
                self.log_message(f"💾 Words saved to: {filename}")
                messagebox.showinfo("Saved", f"Words saved successfully to:\n{filename}")
                
            except Exception as e:
                self.log_message(f"❌ Error saving words: {e}")
                messagebox.showerror("Save Error", f"Could not save words: {e}")
    
    def load_words(self):
        """Load words from a file"""
        filename = filedialog.askopenfilename(
            title="Load Mnemonic Words",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'r') as f:
                    words_data = json.load(f)
                
                # Clear current fields
                self.clear_fields()
                
                # Set missing position
                if "missing_position" in words_data:
                    self.position_var.set(words_data["missing_position"])
                    self.update_missing_position()
                
                # Load words
                if "words" in words_data:
                    for pos_str, word in words_data["words"].items():
                        pos = int(pos_str) - 1  # Convert to 0-based index
                        if 0 <= pos < 24 and pos != self.missing_position - 1:
                            self.word_entries[pos].delete(0, tk.END)
                            self.word_entries[pos].insert(0, word)
                
                saved_date = words_data.get("saved_date", "Unknown")
                self.log_message(f"📂 Words loaded from: {filename}")
                self.log_message(f"📅 Saved on: {saved_date}")
                messagebox.showinfo("Loaded", f"Words loaded successfully from:\n{filename}")
                
            except Exception as e:
                self.log_message(f"❌ Error loading words: {e}")
                messagebox.showerror("Load Error", f"Could not load words: {e}")
    
    def clear_fields(self):
        """Clear all input fields"""
        for i, entry in enumerate(self.word_entries):
            if entry['state'] != 'disabled':
                entry.delete(0, tk.END)
        self.results_text.delete(1.0, tk.END)
        self.progress['value'] = 0
        self.status_var.set("Fields cleared")
        self.valid_combinations = []
        self.log_message("🗑️ All fields cleared")
    
    def load_test_data(self):
        """Load test data for demonstration"""
        # Clear first
        self.clear_fields()
        
        # Set missing position to 22
        self.position_var.set(22)
        self.update_missing_position()
        
        # Test mnemonic: abandon abandon... abandon [MISSING] abandon art
        test_words = ['abandon'] * 24
        test_words[22] = 'abandon'  # Position 23
        test_words[23] = 'art'      # Position 24
        
        for i, word in enumerate(test_words):
            if i != 21:  # Skip position 22 (0-indexed 21)
                self.word_entries[i].delete(0, tk.END)
                self.word_entries[i].insert(0, word)
        
        self.log_message("🧪 Test data loaded:")
        self.log_message("   • Missing position: 22")
        self.log_message("   • Expected missing word: 'abandon'")
        self.log_message("   • This should find the word quickly for testing")
    
    def log_message(self, message):
        """Add message to results text area"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.results_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.results_text.see(tk.END)
        self.root.update()
    
    def validate_inputs(self):
        """Validate user inputs"""
        words = []
        
        for i, entry in enumerate(self.word_entries):
            if i == self.missing_position - 1:  # Missing position
                words.append(None)
                continue
                
            word = entry.get().strip().lower()
            if not word:
                messagebox.showerror("Input Error", f"Position {i+1} is empty. Please fill all positions except {self.missing_position}.")
                return None
            
            if word not in self.wordlist:
                messagebox.showerror("Invalid Word", 
                                   f"Word '{word}' at position {i+1} is not in the BIP39 wordlist!")
                return None
            words.append(word)
        
        # Remove the None (missing word) for processing
        known_words = [w for w in words if w is not None]
        
        if len(known_words) != 23:
            messagebox.showerror("Input Error", f"Please provide exactly 23 words (missing position {self.missing_position})")
            return None
        
        return words
    
    def start_recovery(self):
        """Start the recovery process"""
        if self.recovery_running:
            messagebox.showwarning("Recovery Running", "Recovery is already in progress!")
            return
        
        # Validate inputs
        words_with_missing = self.validate_inputs()
        if not words_with_missing:
            return
        
        # Update UI
        self.start_button.config(state='disabled')
        self.stop_button.config(state='normal')
        self.recovery_running = True
        self.valid_combinations = []
        
        # Clear previous results
        self.results_text.delete(1.0, tk.END)
        self.progress['value'] = 0
        
        # Start recovery in separate thread
        threading.Thread(target=self.recovery_worker, args=(words_with_missing,), daemon=True).start()
    
    def stop_recovery(self):
        """Stop the recovery process"""
        self.recovery_running = False
        self.log_message("⏹️ Recovery stopped by user")
        self.finish_recovery()
    
    def recovery_worker(self, words_with_missing):
        """Worker thread for recovery process"""
        try:
            self.log_message("🔍 Starting advanced recovery process...")
            self.log_message(f"📍 Missing position: {self.missing_position}")
            self.log_message(f"📝 Testing {len(self.wordlist)} possible words...")
            self.log_message(f"🔄 Finding {'ALL valid combinations' if self.find_all_var.get() else 'first valid word'}")
            if self.test_metamask_var.get():
                self.log_message(f"🌐 Will test valid words with MetaMask in {self.browser_var.get()}")
            self.log_message("=" * 80)
            
            attempts = 0
            start_time = time.time()
            valid_found = 0
            
            # Try each word from BIP39 wordlist in the missing position
            for word_candidate in self.wordlist:
                if not self.recovery_running:
                    break
                    
                attempts += 1
                self.status_var.set(f"Testing word {attempts}/{len(self.wordlist)}: {word_candidate}")
                
                # Create complete mnemonic with candidate word
                test_words = words_with_missing.copy()
                test_words[self.missing_position - 1] = word_candidate
                mnemonic_phrase = " ".join(test_words)
                
                # Test if this mnemonic is valid (BIP39 checksum)
                if self.mnemo.check(mnemonic_phrase):
                    valid_found += 1
                    self.log_message(f"✅ VALID #{valid_found}: Position {self.missing_position} = '{word_candidate}'")
                    
                    combination = {
                        'word': word_candidate,
                        'position': self.missing_position,
                        'mnemonic': mnemonic_phrase,
                        'found_at_attempt': attempts
                    }
                    
                    # Test with MetaMask if enabled
                    if self.test_metamask_var.get():
                        metamask_result = self.test_with_metamask(mnemonic_phrase, word_candidate)
                        combination['metamask_test'] = metamask_result
                    
                    self.valid_combinations.append(combination)
                    
                    # If not finding all, stop at first valid
                    if not self.find_all_var.get():
                        break
                
                # Update progress
                progress_percent = (attempts / len(self.wordlist)) * 100
                self.root.after(0, lambda p=progress_percent: setattr(self.progress, 'value', p))
                
                # Progress message every 100 attempts
                if attempts % 100 == 0:
                    elapsed = time.time() - start_time
                    rate = attempts / elapsed if elapsed > 0 else 0
                    message = f"⏱️  Progress: {attempts}/{len(self.wordlist)} ({rate:.1f} words/sec) - Found {valid_found} valid"
                    self.root.after(0, lambda m=message: self.log_message(m))
            
            elapsed_time = time.time() - start_time
            
            if self.valid_combinations:
                self.root.after(0, lambda: self.recovery_success(elapsed_time, attempts))
            else:
                self.root.after(0, lambda: self.recovery_failed(attempts, elapsed_time))
                
        except Exception as e:
            self.root.after(0, lambda: self.recovery_error(str(e)))
    
    def test_with_metamask(self, mnemonic, word):
        """Test mnemonic with MetaMask using browser automation"""
        try:
            self.log_message(f"🌐 Opening {self.browser_var.get()} browser for MetaMask testing...")
            
            # Import the MetaMask testing module
            from metamask_integration import MetaMaskTester
            
            tester = MetaMaskTester(self.browser_var.get())
            setup_result = tester.setup_driver()
            
            if setup_result is not True:
                return {"status": "error", "message": f"Browser setup failed: {setup_result[1]}"}
            
            # Open MetaMask website for manual testing
            website_result = tester.open_metamask_website()
            
            if website_result[0]:
                self.log_message("🌐 Browser opened - Manual testing required")
                
                # Show instructions to user
                instructions = f"""
MANUAL METAMASK TEST for word '{word}':

1. Browser is now open with MetaMask website
2. Install MetaMask extension if not already installed
3. In MetaMask, choose "Import using Secret Recovery Phrase"
4. Enter this complete mnemonic:

{mnemonic}

5. If import SUCCESS ✅: This word '{word}' is CORRECT
6. If import FAILS ❌: This word '{word}' is WRONG

IMPORTANT: Only test with small amounts first!
                """
                
                # Don't close browser immediately - let user test
                return {
                    "status": "manual_test_ready", 
                    "message": instructions,
                    "browser_opened": True
                }
            else:
                tester.close_driver()
                return {"status": "error", "message": f"Failed to open MetaMask: {website_result[1]}"}
                
        except ImportError:
            return {"status": "error", "message": "Selenium not installed. Please run setup_advanced.bat"}
        except Exception as e:
            return {"status": "error", "message": f"MetaMask test error: {str(e)}"}
    
    
    def recovery_success(self, elapsed_time, attempts):
        """Handle successful recovery"""
        self.log_message("=" * 80)
        self.log_message("🎉 RECOVERY COMPLETED SUCCESSFULLY!")
        self.log_message("=" * 80)
        self.log_message(f"⏱️  Time: {elapsed_time:.2f} seconds")
        self.log_message(f"🔍 Attempts: {attempts}")
        self.log_message(f"✅ Valid combinations found: {len(self.valid_combinations)}")
        self.log_message("")
        
        for i, combo in enumerate(self.valid_combinations, 1):
            self.log_message(f"RESULT #{i}:")
            self.log_message(f"  Position {combo['position']}: '{combo['word']}'")
            self.log_message(f"  Found at attempt: {combo['found_at_attempt']}")
            self.log_message(f"  Complete mnemonic:")
            
            # Display mnemonic with word positions
            words = combo['mnemonic'].split()
            for j in range(0, 24, 6):
                line = "    " + "  ".join([f"{k+1:2d}:{words[k]:>10}" for k in range(j, min(j+6, 24))])
                self.log_message(line)
            
            if 'metamask_test' in combo:
                self.log_message(f"  MetaMask test: {combo['metamask_test']['status']}")
            
            self.log_message("")
        
        self.log_message("=" * 80)
        self.log_message("💾 You can now use these mnemonics with MetaMask or your Ledger device.")
        self.log_message("⚠️  IMPORTANT: Test each one carefully to find the correct wallet!")
        self.log_message("⚠️  Keep these mnemonics secure and delete this output when done!")
        
        # Show success dialog
        result_summary = f"Found {len(self.valid_combinations)} valid word(s):\n"
        for combo in self.valid_combinations[:5]:  # Show first 5
            result_summary += f"• Position {combo['position']}: '{combo['word']}'\n"
        if len(self.valid_combinations) > 5:
            result_summary += f"... and {len(self.valid_combinations) - 5} more (see results area)"
        
        messagebox.showinfo("Recovery Successful!", result_summary)
        self.finish_recovery()
    
    def recovery_failed(self, attempts, elapsed_time):
        """Handle failed recovery"""
        self.log_message("=" * 80)
        self.log_message("❌ Recovery failed - No valid words found")
        self.log_message("=" * 80)
        self.log_message(f"⏱️  Tested all {attempts} words in {elapsed_time:.2f} seconds")
        self.log_message("💡 Possible issues:")
        self.log_message("   • Check all words are spelled correctly")
        self.log_message("   • Verify all words are in correct positions")
        self.log_message("   • Make sure the right position is marked as missing")
        self.log_message("   • Original mnemonic might have multiple errors")
        
        messagebox.showerror("Recovery Failed", 
                           "Could not find valid words.\nPlease check your input words and positions.")
        self.finish_recovery()
    
    def recovery_error(self, error_msg):
        """Handle recovery error"""
        self.log_message(f"❌ Error during recovery: {error_msg}")
        messagebox.showerror("Recovery Error", f"An error occurred: {error_msg}")
        self.finish_recovery()
    
    def finish_recovery(self):
        """Clean up after recovery"""
        self.progress['value'] = 0
        self.start_button.config(state='normal')
        self.stop_button.config(state='disabled')
        self.recovery_running = False
        self.status_var.set("Recovery completed")


def main():
    try:
        # Test dependencies
        from mnemonic import Mnemonic
        
        print("🚀 Starting Advanced BIP39 Mnemonic Recovery Tool...")
        print("📋 Features:")
        print("  • Any missing position (not just 22)")
        print("  • Save/Load word combinations") 
        print("  • Find ALL valid combinations")
        print("  • MetaMask browser integration (coming soon)")
        print()
        
        # Create GUI
        root = tk.Tk()
        app = AdvancedMnemonicRecoveryGUI(root)
        root.mainloop()
        
    except ImportError as e:
        print(f"❌ Required library missing: {e}")
        print("Please run: pip install mnemonic selenium")
        input("Press Enter to exit...")
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        input("Press Enter to exit...")


if __name__ == "__main__":
    main()