#!/usr/bin/env python3
"""
MetaMask Browser Automation Module
Handles actual MetaMask wallet testing with browser automation
"""

import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, WebDriverException


class MetaMaskTester:
    def __init__(self, browser="Chrome"):
        self.browser = browser
        self.driver = None
        self.wait = None
    
    def setup_driver(self):
        """Setup WebDriver for the specified browser"""
        try:
            if self.browser.lower() == "chrome":
                options = Options()
                # Add MetaMask extension if available
                options.add_argument("--disable-web-security")
                options.add_argument("--disable-features=VizDisplayCompositor")
                # Uncomment to run headless: options.add_argument("--headless")
                self.driver = webdriver.Chrome(options=options)
            
            elif self.browser.lower() == "firefox":
                options = FirefoxOptions()
                # options.add_argument("--headless")  # Uncomment for headless
                self.driver = webdriver.Firefox(options=options)
            
            elif self.browser.lower() == "edge":
                options = EdgeOptions()
                # options.add_argument("--headless")  # Uncomment for headless
                self.driver = webdriver.Edge(options=options)
            
            else:
                raise ValueError(f"Unsupported browser: {self.browser}")
            
            self.wait = WebDriverWait(self.driver, 10)
            return True
            
        except WebDriverException as e:
            return False, f"WebDriver error: {str(e)}"
        except Exception as e:
            return False, f"Setup error: {str(e)}"
    
    def open_metamask_website(self):
        """Open MetaMask website for manual testing"""
        try:
            # Open MetaMask website
            self.driver.get("https://metamask.io/")
            time.sleep(3)
            
            # Look for "Add to Chrome" or similar button
            try:
                add_button = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Add to') or contains(text(), 'Install')]"))
                )
                return True, "MetaMask website loaded - ready for manual installation"
            except TimeoutException:
                return True, "MetaMask website loaded - please install extension manually"
                
        except Exception as e:
            return False, f"Error opening MetaMask: {str(e)}"
    
    def test_mnemonic_manual_guidance(self, mnemonic, missing_word):
        """Provide guidance for manual MetaMask testing"""
        instructions = f"""
        MANUAL METAMASK TESTING INSTRUCTIONS:
        
        1. MetaMask should be opening in your browser
        2. If not installed, install MetaMask extension
        3. In MetaMask, choose "Import using Secret Recovery Phrase"
        4. Enter this mnemonic phrase:
           {mnemonic}
        
        5. If the import is SUCCESSFUL:
           - The missing word '{missing_word}' is CORRECT
           - You should see your wallet with the right balance/addresses
        
        6. If the import FAILS:
           - The missing word '{missing_word}' is WRONG
           - Try the next word the tool finds
        
        7. IMPORTANT: Only test with small amounts first!
        """
        return instructions
    
    def automated_metamask_test(self, mnemonic, missing_word):
        """Attempt automated MetaMask testing (advanced)"""
        try:
            # This would require MetaMask to be already installed and configured
            # For now, we'll simulate the process
            
            # Navigate to a test page or MetaMask directly
            self.driver.get("chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html")
            time.sleep(2)
            
            # This is complex and would need MetaMask's specific UI elements
            # For now, return guidance for manual testing
            return {
                "status": "manual_guidance",
                "message": self.test_mnemonic_manual_guidance(mnemonic, missing_word),
                "automated": False
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Automated testing failed: {str(e)}",
                "automated": False
            }
    
    def close_driver(self):
        """Clean up WebDriver"""
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
    
    def test_multiple_mnemonics(self, mnemonic_combinations):
        """Test multiple mnemonic combinations"""
        results = []
        
        for i, combo in enumerate(mnemonic_combinations):
            print(f"Testing combination {i+1}/{len(mnemonic_combinations)}: {combo['word']}")
            
            result = self.automated_metamask_test(combo['mnemonic'], combo['word'])
            result['combination_index'] = i
            result['word'] = combo['word']
            result['position'] = combo['position']
            
            results.append(result)
            
            # Wait between tests
            time.sleep(2)
        
        return results


def test_metamask_integration():
    """Test the MetaMask integration functionality"""
    print("🧪 Testing MetaMask Integration")
    print("=" * 40)
    
    tester = MetaMaskTester("Chrome")
    
    # Test driver setup
    setup_result = tester.setup_driver()
    if setup_result is True:
        print("✅ WebDriver setup successful")
    else:
        print(f"❌ WebDriver setup failed: {setup_result[1]}")
        return
    
    # Test opening MetaMask website
    website_result = tester.open_metamask_website()
    if website_result[0]:
        print(f"✅ MetaMask website: {website_result[1]}")
    else:
        print(f"❌ MetaMask website failed: {website_result[1]}")
    
    # Keep browser open for manual inspection
    input("Press Enter to close browser...")
    tester.close_driver()


if __name__ == "__main__":
    test_metamask_integration()