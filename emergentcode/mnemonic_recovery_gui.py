#!/usr/bin/env python3
"""
BIP39 Mnemonic Recovery Tool - GUI Version
User-friendly interface for recovering missing 22nd word from 24-word mnemonic
Compatible with MetaMask and Ledger wallets
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import time
from mnemonic import Mnemonic


class MnemonicRecoveryGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🔐 BIP39 Mnemonic Recovery Tool")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        
        # Initialize mnemonic handler
        self.mnemo = Mnemonic("english")
        self.wordlist = self.mnemo.wordlist
        self.recovery_running = False
        
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
        title_label = ttk.Label(main_frame, text="🔐 BIP39 Mnemonic Recovery Tool", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        # Subtitle
        subtitle_label = ttk.Label(main_frame, text="Recover your missing 22nd word from a 24-word mnemonic phrase",
                                  font=("Arial", 10))
        subtitle_label.grid(row=1, column=0, columnspan=2, pady=(0, 20))
        
        # Instructions
        instructions = """INSTRUCTIONS:
1. Enter your 23 known words in the boxes below
2. Leave position 22 EMPTY (this is the word we'll recover)
3. Make sure all other words are in their correct positions
4. Click 'Start Recovery' to find the missing word
5. The tool will test all 2048 possible BIP39 words for position 22"""
        
        inst_label = ttk.Label(main_frame, text=instructions, justify=tk.LEFT,
                              font=("Arial", 9), foreground="blue")
        inst_label.grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=(0, 20))
        
        # Create scrollable frame for word inputs
        canvas = tk.Canvas(main_frame, height=300)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        scrollbar.grid(row=3, column=2, sticky=(tk.N, tk.S), pady=(0, 10))
        
        # Word input fields
        self.word_entries = []
        ttk.Label(scrollable_frame, text="Enter your 23 known words (leave position 22 empty):", 
                 font=("Arial", 11, "bold")).grid(row=0, column=0, columnspan=6, pady=(0, 10))
        
        for i in range(24):
            row = (i // 6) + 1
            col = i % 6
            
            # Position label
            pos_label = ttk.Label(scrollable_frame, text=f"{i+1}:", font=("Arial", 9))
            pos_label.grid(row=row*2, column=col, sticky=tk.W, padx=(5, 0), pady=(5, 0))
            
            if i == 21:  # Position 22 (0-indexed 21)
                # Special styling for the missing word position
                entry = ttk.Entry(scrollable_frame, width=12, font=("Arial", 9),
                                state='disabled')
                entry.grid(row=row*2+1, column=col, padx=5, pady=(0, 10))
                
                # Add label indicating this is the missing word
                missing_label = ttk.Label(scrollable_frame, text="[MISSING]", 
                                        font=("Arial", 8), foreground="red")
                missing_label.grid(row=row*2+2, column=col, pady=(0, 5))
            else:
                entry = ttk.Entry(scrollable_frame, width=12, font=("Arial", 9))
                entry.grid(row=row*2+1, column=col, padx=5, pady=(0, 10))
            
            self.word_entries.append(entry)
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        # Buttons
        self.start_button = ttk.Button(button_frame, text="🔍 Start Recovery", 
                                      command=self.start_recovery)
        self.start_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.clear_button = ttk.Button(button_frame, text="🗑️ Clear All", 
                                      command=self.clear_fields)
        self.clear_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.test_button = ttk.Button(button_frame, text="🧪 Load Test Data", 
                                     command=self.load_test_data)
        self.test_button.pack(side=tk.LEFT)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, length=400, mode='determinate')
        self.progress.grid(row=5, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))
        
        # Results text area
        results_label = ttk.Label(main_frame, text="Recovery Results:", font=("Arial", 11, "bold"))
        results_label.grid(row=6, column=0, sticky=tk.W, pady=(20, 5))
        
        self.results_text = scrolledtext.ScrolledText(main_frame, width=80, height=10, 
                                                     font=("Courier", 9))
        self.results_text.grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), 
                              pady=(0, 10))
        
        # Configure grid weights for resizing
        main_frame.rowconfigure(7, weight=1)
        
        # Initial message
        self.log_message("🔐 BIP39 Mnemonic Recovery Tool Ready")
        self.log_message(f"📊 Loaded BIP39 wordlist with {len(self.wordlist)} words")
        self.log_message("⚠️  SECURITY: This tool handles sensitive data - use on a secure computer!")
        self.log_message("=" * 60)
    
    def clear_fields(self):
        """Clear all input fields"""
        for i, entry in enumerate(self.word_entries):
            if i != 21:  # Don't try to clear the disabled field
                entry.delete(0, tk.END)
        self.results_text.delete(1.0, tk.END)
        self.progress['value'] = 0
        self.log_message("🗑️ All fields cleared")
    
    def load_test_data(self):
        """Load test data for demonstration"""
        test_words = [
            'abandon', 'abandon', 'abandon', 'abandon', 'abandon', 'abandon',
            'abandon', 'abandon', 'abandon', 'abandon', 'abandon', 'abandon',
            'abandon', 'abandon', 'abandon', 'abandon', 'abandon', 'abandon',
            'abandon', 'abandon', 'abandon', None, 'abandon', 'art'
        ]
        
        for i, word in enumerate(test_words):
            if word and i != 21:
                self.word_entries[i].delete(0, tk.END)
                self.word_entries[i].insert(0, word)
        
        self.log_message("🧪 Test data loaded (missing word should be 'abandon' at position 22)")
    
    def log_message(self, message):
        """Add message to results text area"""
        self.results_text.insert(tk.END, f"{message}\n")
        self.results_text.see(tk.END)
        self.root.update()
    
    def validate_inputs(self):
        """Validate user inputs"""
        words = []
        empty_positions = []
        
        for i, entry in enumerate(self.word_entries):
            if i == 21:  # Skip position 22 (it should be empty)
                words.append(None)
                continue
            
            word = entry.get().strip().lower()
            if not word:
                empty_positions.append(i + 1)
                words.append(None)
            else:
                if word not in self.wordlist:
                    messagebox.showerror("Invalid Word", 
                                       f"Word '{word}' at position {i+1} is not in the BIP39 wordlist!")
                    return None
                words.append(word)
        
        # Check that we have exactly one empty position (position 22)
        if len(empty_positions) > 1:
            messagebox.showerror("Input Error", 
                               f"Too many empty positions: {empty_positions}. Only position 22 should be empty!")
            return None
        
        if len(empty_positions) == 1 and empty_positions[0] != 22:
            messagebox.showerror("Input Error", 
                               f"Wrong empty position: {empty_positions[0]}. Only position 22 should be empty!")
            return None
        
        # Remove the None at position 22 for processing
        known_words = words[:21] + words[22:]
        
        if len([w for w in known_words if w]) != 23:
            messagebox.showerror("Input Error", 
                               "Please provide exactly 23 words (all positions except 22)")
            return None
        
        return known_words
    
    def start_recovery(self):
        """Start the recovery process"""
        if self.recovery_running:
            messagebox.showwarning("Recovery Running", "Recovery is already in progress!")
            return
        
        # Validate inputs
        known_words = self.validate_inputs()
        if not known_words:
            return
        
        # Disable start button
        self.start_button.config(state='disabled', text='🔄 Recovering...')
        self.recovery_running = True
        
        # Clear previous results
        self.results_text.delete(1.0, tk.END)
        self.progress['value'] = 0
        
        # Start recovery in separate thread
        threading.Thread(target=self.recovery_worker, args=(known_words,), daemon=True).start()
    
    def recovery_worker(self, known_words):
        """Worker thread for recovery process"""
        try:
            self.log_message("🔍 Starting recovery process...")
            self.log_message(f"📝 Testing {len(self.wordlist)} possible words for position 22...")
            self.log_message("⏳ This may take a few moments...")
            self.log_message("=" * 60)
            
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
                    
                    # Success!
                    self.root.after(0, lambda: self.recovery_success(word_candidate, mnemonic_phrase, 
                                                                   attempts, elapsed_time))
                    return
                
                # Update progress
                progress_percent = (attempts / len(self.wordlist)) * 100
                self.root.after(0, lambda p=progress_percent, a=attempts: self.update_progress(p, a))
                
                # Progress message every 200 attempts
                if attempts % 200 == 0:
                    elapsed = time.time() - start_time
                    rate = attempts / elapsed if elapsed > 0 else 0
                    message = f"⏱️  Tested {attempts}/{len(self.wordlist)} words ({rate:.1f} words/sec)"
                    self.root.after(0, lambda m=message: self.log_message(m))
            
            # No valid mnemonic found
            elapsed_time = time.time() - start_time
            self.root.after(0, lambda: self.recovery_failed(attempts, elapsed_time))
            
        except Exception as e:
            self.root.after(0, lambda: self.recovery_error(str(e)))
    
    def update_progress(self, percent, attempts):
        """Update progress bar and status"""
        self.progress['value'] = percent
    
    def recovery_success(self, missing_word, complete_mnemonic, attempts, elapsed_time):
        """Handle successful recovery"""
        self.log_message("=" * 60)
        self.log_message("✅ SUCCESS! Recovery completed!")
        self.log_message("=" * 60)
        self.log_message(f"🔑 Missing word (position 22): '{missing_word}'")
        self.log_message(f"⏱️  Found after {attempts} attempts in {elapsed_time:.2f} seconds")
        self.log_message("")
        self.log_message("📋 COMPLETE MNEMONIC:")
        self.log_message("=" * 60)
        
        # Display mnemonic with word numbers
        words = complete_mnemonic.split()
        for i in range(0, 24, 6):
            line = "  ".join([f"{j+1:2d}:{words[j]:>10}" for j in range(i, min(i+6, 24))])
            self.log_message(line)
        
        self.log_message("=" * 60)
        self.log_message("💾 You can now use this mnemonic with MetaMask or your Ledger device.")
        self.log_message("⚠️  IMPORTANT: Keep this mnemonic secure and delete this output when done!")
        
        # Show success dialog
        messagebox.showinfo("Recovery Successful!", 
                          f"Found missing word: '{missing_word}'\n\n"
                          f"Complete mnemonic is displayed in the results area.\n"
                          f"IMPORTANT: Keep this secure!")
        
        self.finish_recovery()
    
    def recovery_failed(self, attempts, elapsed_time):
        """Handle failed recovery"""
        self.log_message("=" * 60)
        self.log_message("❌ Recovery failed")
        self.log_message("=" * 60)
        self.log_message(f"⏱️  Tested all {attempts} words in {elapsed_time:.2f} seconds")
        self.log_message("💡 No valid mnemonic found. Please check:")
        self.log_message("   • All words are spelled correctly")
        self.log_message("   • All words are in the correct positions")
        self.log_message("   • The missing word is actually position 22")
        self.log_message("   • Your original mnemonic was 24 words")
        
        messagebox.showerror("Recovery Failed", 
                           "Could not find the missing word.\n\n"
                           "Please verify your input words are correct and in the right positions.")
        
        self.finish_recovery()
    
    def recovery_error(self, error_msg):
        """Handle recovery error"""
        self.log_message(f"❌ Error during recovery: {error_msg}")
        messagebox.showerror("Recovery Error", f"An error occurred: {error_msg}")
        self.finish_recovery()
    
    def finish_recovery(self):
        """Clean up after recovery"""
        self.progress['value'] = 0
        self.start_button.config(state='normal', text='🔍 Start Recovery')
        self.recovery_running = False


def main():
    try:
        # Test if mnemonic library is available
        from mnemonic import Mnemonic
        
        # Create GUI
        root = tk.Tk()
        app = MnemonicRecoveryGUI(root)
        root.mainloop()
        
    except ImportError:
        print("❌ Required library 'mnemonic' is not installed.")
        print("Please run: pip install mnemonic")
        input("Press Enter to exit...")
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        input("Press Enter to exit...")


if __name__ == "__main__":
    main()