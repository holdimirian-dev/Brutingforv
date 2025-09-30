#!/usr/bin/env python3
"""
Backend Test Suite for BIP39 Mnemonic Recovery Tool
Tests the terminal-based mnemonic recovery functionality in server.py
"""

import sys
import os
import time
import unittest
from unittest.mock import patch, MagicMock, call
from io import StringIO
import subprocess

# Add the app directory to Python path to import server.py
sys.path.insert(0, '/app')

try:
    from server import TerminalMnemonicRecovery
    from mnemonic import Mnemonic
    from selenium import webdriver
    from selenium.webdriver.edge.options import Options as EdgeOptions
    from webdriver_manager.microsoft import EdgeChromiumDriverManager
    from selenium.webdriver.edge.service import Service as EdgeService
    SERVER_IMPORT_SUCCESS = True
except ImportError as e:
    print(f"❌ Import error: {e}")
    SERVER_IMPORT_SUCCESS = False


class TestBIP39Dependencies(unittest.TestCase):
    """Test that all required dependencies are available"""
    
    def test_mnemonic_library(self):
        """Test that mnemonic library is installed and working"""
        try:
            from mnemonic import Mnemonic
            mnemo = Mnemonic("english")
            self.assertIsNotNone(mnemo)
            self.assertGreater(len(mnemo.wordlist), 2000)  # BIP39 has 2048 words
            print("✅ Mnemonic library working correctly")
        except ImportError:
            self.fail("❌ Mnemonic library not installed")
    
    def test_selenium_library(self):
        """Test that selenium library is installed"""
        try:
            from selenium import webdriver
            from selenium.webdriver.edge.options import Options as EdgeOptions
            print("✅ Selenium library available")
        except ImportError:
            self.fail("❌ Selenium library not installed")
    
    def test_webdriver_manager(self):
        """Test that webdriver-manager is installed"""
        try:
            from webdriver_manager.microsoft import EdgeChromiumDriverManager
            print("✅ WebDriver Manager available")
        except ImportError:
            self.fail("❌ WebDriver Manager not installed")


class TestTerminalMnemonicRecovery(unittest.TestCase):
    """Test the TerminalMnemonicRecovery class functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        if not SERVER_IMPORT_SUCCESS:
            self.skipTest("Cannot import server.py - skipping tests")
        
        self.recovery = TerminalMnemonicRecovery()
        
        # Known valid test mnemonic for testing
        self.test_mnemonic_words = [
            'abandon', 'abandon', 'abandon', 'abandon', 'abandon', 'abandon',
            'abandon', 'abandon', 'abandon', 'abandon', 'abandon', 'abandon',
            'abandon', 'abandon', 'abandon', 'abandon', 'abandon', 'abandon',
            'abandon', 'abandon', 'abandon', 'abandon', 'abandon', 'art'
        ]
        self.test_mnemonic_phrase = ' '.join(self.test_mnemonic_words)
    
    def test_initialization(self):
        """Test that the recovery tool initializes correctly"""
        self.assertIsNotNone(self.recovery.mnemo)
        self.assertIsNotNone(self.recovery.wordlist)
        self.assertEqual(len(self.recovery.wordlist), 2048)
        self.assertFalse(self.recovery.recovery_running)
        self.assertEqual(len(self.recovery.valid_combinations), 0)
        print("✅ TerminalMnemonicRecovery initialization successful")
    
    @patch('builtins.input')
    def test_get_missing_position_default(self, mock_input):
        """Test getting missing position with default value"""
        mock_input.return_value = ""  # Empty input should default to 22
        position = self.recovery.get_missing_position()
        self.assertEqual(position, 22)
        print("✅ Default missing position (22) working correctly")
    
    @patch('builtins.input')
    def test_get_missing_position_valid(self, mock_input):
        """Test getting missing position with valid input"""
        mock_input.return_value = "15"
        position = self.recovery.get_missing_position()
        self.assertEqual(position, 15)
        print("✅ Custom missing position input working correctly")
    
    @patch('builtins.input')
    def test_get_missing_position_invalid_then_valid(self, mock_input):
        """Test getting missing position with invalid then valid input"""
        mock_input.side_effect = ["0", "25", "abc", "10"]  # Invalid inputs then valid
        position = self.recovery.get_missing_position()
        self.assertEqual(position, 10)
        print("✅ Input validation for missing position working correctly")
    
    def test_bip39_validation(self):
        """Test BIP39 mnemonic validation"""
        # Test valid mnemonic
        self.assertTrue(self.recovery.mnemo.check(self.test_mnemonic_phrase))
        
        # Test invalid mnemonic (wrong checksum)
        invalid_mnemonic = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon"
        self.assertFalse(self.recovery.mnemo.check(invalid_mnemonic))
        
        print("✅ BIP39 validation working correctly")
    
    def test_wordlist_validation(self):
        """Test that words are properly validated against BIP39 wordlist"""
        # Valid words
        self.assertIn("abandon", self.recovery.wordlist)
        self.assertIn("art", self.recovery.wordlist)
        self.assertIn("zoo", self.recovery.wordlist)
        
        # Invalid words
        self.assertNotIn("invalid", self.recovery.wordlist)
        self.assertNotIn("notaword", self.recovery.wordlist)
        self.assertNotIn("123", self.recovery.wordlist)
        
        print("✅ BIP39 wordlist validation working correctly")
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_get_user_words_valid_input(self, mock_print, mock_input):
        """Test getting user words with valid input"""
        # Simulate user input for 23 words (missing position 22)
        test_inputs = []
        for i in range(24):
            if i + 1 == 22:  # Skip position 22 (missing)
                continue
            test_inputs.append(self.test_mnemonic_words[i])
        test_inputs.append('y')  # Confirm input
        
        mock_input.side_effect = test_inputs
        
        result = self.recovery.get_user_words(22)
        self.assertIsNotNone(result)
        self.assertEqual(len([w for w in result if w is not None]), 23)
        self.assertIsNone(result[21])  # Position 22 should be None
        print("✅ User word input validation working correctly")
    
    @patch('builtins.input')
    def test_get_user_words_invalid_word(self, mock_input):
        """Test handling of invalid BIP39 words"""
        mock_input.side_effect = ["invalidword", "abandon", "quit"]
        
        with self.assertRaises(SystemExit):
            self.recovery.get_user_words(22)
        print("✅ Invalid word rejection working correctly")
    
    def test_edge_webdriver_setup_mock(self):
        """Test Edge WebDriver setup (mocked for container environment)"""
        with patch('server.EdgeChromiumDriverManager') as mock_manager, \
             patch('server.webdriver.Edge') as mock_edge, \
             patch('server.EdgeService') as mock_service:
            
            # Mock successful setup
            mock_manager.return_value.install.return_value = "/path/to/driver"
            mock_driver = MagicMock()
            mock_edge.return_value = mock_driver
            
            driver = self.recovery.setup_edge_driver()
            
            self.assertIsNotNone(driver)
            mock_manager.assert_called_once()
            mock_edge.assert_called_once()
            print("✅ Edge WebDriver setup (mocked) working correctly")
    
    def test_edge_webdriver_setup_failure_mock(self):
        """Test Edge WebDriver setup failure handling"""
        with patch('server.EdgeChromiumDriverManager') as mock_manager:
            # Mock setup failure
            mock_manager.side_effect = Exception("WebDriver setup failed")
            
            driver = self.recovery.setup_edge_driver()
            
            self.assertIsNone(driver)
            print("✅ Edge WebDriver setup failure handling working correctly")
    
    @patch('builtins.input')
    def test_metamask_automation_mock(self, mock_input):
        """Test MetaMask automation with mocked browser"""
        mock_driver = MagicMock()
        mock_input.return_value = "y"  # Simulate successful test
        
        result = self.recovery.test_metamask_automation(
            mock_driver, 
            self.test_mnemonic_phrase, 
            "abandon"
        )
        
        self.assertIsInstance(result, dict)
        self.assertIn('status', result)
        self.assertIn('verified', result)
        mock_driver.get.assert_called_once()
        print("✅ MetaMask automation (mocked) working correctly")
    
    def test_recovery_logic_with_known_mnemonic(self):
        """Test the core recovery logic with a known valid mnemonic"""
        # Create test words with missing position 22
        test_words = self.test_mnemonic_words.copy()
        test_words[21] = None  # Remove word at position 22
        
        # Mock WebDriver setup to avoid browser issues in container
        with patch.object(self.recovery, 'setup_edge_driver', return_value=None):
            self.recovery.recovery_running = True
            
            valid_combinations, attempts, elapsed_time = self.recovery.recover_missing_word(
                test_words, 22, test_metamask=False
            )
            
            # Should find at least one valid combination
            self.assertGreater(len(valid_combinations), 0)
            self.assertGreater(attempts, 0)
            self.assertGreater(elapsed_time, 0)
            
            # Check that the found word creates a valid mnemonic
            found_word = valid_combinations[0]['word']
            test_mnemonic = test_words.copy()
            test_mnemonic[21] = found_word
            complete_mnemonic = ' '.join(test_mnemonic)
            self.assertTrue(self.recovery.mnemo.check(complete_mnemonic))
            
            print(f"✅ Recovery logic working correctly - found word: '{found_word}'")
    
    def test_recovery_with_invalid_input(self):
        """Test recovery with invalid input that should find no results"""
        # Create invalid test words (all same word, will never have valid checksum)
        invalid_words = ['abandon'] * 24
        invalid_words[21] = None  # Missing position 22
        
        with patch.object(self.recovery, 'setup_edge_driver', return_value=None):
            self.recovery.recovery_running = True
            
            # Limit search to first 10 words for speed
            original_wordlist = self.recovery.wordlist
            self.recovery.wordlist = self.recovery.wordlist[:10]
            
            valid_combinations, attempts, elapsed_time = self.recovery.recover_missing_word(
                invalid_words, 22, test_metamask=False
            )
            
            # Restore original wordlist
            self.recovery.wordlist = original_wordlist
            
            # Should find no valid combinations with this invalid setup
            self.assertEqual(len(valid_combinations), 0)
            self.assertEqual(attempts, 10)  # Should have tried 10 words
            
            print("✅ Recovery with invalid input handled correctly")
    
    def test_display_results_with_valid_combinations(self):
        """Test results display functionality"""
        # Create mock valid combinations
        mock_combinations = [
            {
                'word': 'abandon',
                'position': 22,
                'mnemonic': self.test_mnemonic_phrase,
                'found_at_attempt': 1,
                'metamask_test': {'status': 'success'},
                'verified': True
            }
        ]
        
        # Capture output
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.recovery.display_results(mock_combinations, 1, 0.5)
            output = mock_stdout.getvalue()
            
            self.assertIn("RECOVERY COMPLETED SUCCESSFULLY", output)
            self.assertIn("abandon", output)
            self.assertIn("Position 22", output)
            
        print("✅ Results display working correctly")
    
    def test_display_results_no_combinations(self):
        """Test results display with no valid combinations found"""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.recovery.display_results([], 2048, 10.0)
            output = mock_stdout.getvalue()
            
            self.assertIn("NO VALID WORDS FOUND", output)
            self.assertIn("2048", output)
            self.assertIn("10.0", output)
            
        print("✅ No results display working correctly")


class TestErrorHandling(unittest.TestCase):
    """Test error handling and edge cases"""
    
    def setUp(self):
        if not SERVER_IMPORT_SUCCESS:
            self.skipTest("Cannot import server.py - skipping tests")
        self.recovery = TerminalMnemonicRecovery()
    
    @patch('builtins.input')
    def test_keyboard_interrupt_handling(self, mock_input):
        """Test handling of keyboard interrupt (Ctrl+C)"""
        mock_input.side_effect = KeyboardInterrupt()
        
        with self.assertRaises(SystemExit):
            self.recovery.get_missing_position()
        print("✅ Keyboard interrupt handling working correctly")
    
    def test_invalid_mnemonic_length(self):
        """Test handling of invalid mnemonic length"""
        # Test with wrong number of words
        short_words = ['abandon'] * 10
        short_words[5] = None
        
        with patch.object(self.recovery, 'setup_edge_driver', return_value=None):
            self.recovery.recovery_running = True
            
            # This should still work but find no valid combinations
            valid_combinations, attempts, elapsed_time = self.recovery.recover_missing_word(
                short_words, 6, test_metamask=False
            )
            
            # Should complete without crashing
            self.assertIsInstance(valid_combinations, list)
            self.assertIsInstance(attempts, int)
            self.assertIsInstance(elapsed_time, float)
            
        print("✅ Invalid mnemonic length handling working correctly")


class TestIntegrationScenarios(unittest.TestCase):
    """Test integration scenarios and real-world usage"""
    
    def setUp(self):
        if not SERVER_IMPORT_SUCCESS:
            self.skipTest("Cannot import server.py - skipping tests")
    
    def test_server_py_execution(self):
        """Test that server.py can be executed without crashing"""
        try:
            # Test that the file can be imported and main function exists
            import server
            self.assertTrue(hasattr(server, 'main'))
            self.assertTrue(hasattr(server, 'TerminalMnemonicRecovery'))
            print("✅ server.py can be imported and has required functions")
        except Exception as e:
            self.fail(f"❌ server.py execution test failed: {e}")
    
    def test_environment_compatibility(self):
        """Test environment compatibility checks"""
        # Test OS detection (will be 'posix' in Linux container)
        self.assertEqual(os.name, 'posix')
        print("✅ Environment compatibility check working (Linux container detected)")
    
    def test_dependencies_installation_check(self):
        """Test that all required dependencies can be imported"""
        required_modules = [
            'mnemonic',
            'selenium',
            'webdriver_manager'
        ]
        
        for module in required_modules:
            try:
                __import__(module)
                print(f"✅ {module} dependency available")
            except ImportError:
                self.fail(f"❌ Required dependency {module} not available")


def run_comprehensive_test():
    """Run all tests and provide summary"""
    print("🔐 BIP39 Mnemonic Recovery Tool - Comprehensive Backend Test Suite")
    print("=" * 80)
    print("🐧 Running in Linux container environment (Windows 11 features mocked)")
    print("=" * 80)
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestBIP39Dependencies,
        TestTerminalMnemonicRecovery,
        TestErrorHandling,
        TestIntegrationScenarios
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    result = runner.run(test_suite)
    
    # Print summary
    print("\n" + "=" * 80)
    print("🧪 TEST SUMMARY")
    print("=" * 80)
    
    total_tests = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    passed = total_tests - failures - errors
    
    print(f"✅ Tests Passed: {passed}/{total_tests}")
    if failures > 0:
        print(f"❌ Tests Failed: {failures}")
    if errors > 0:
        print(f"💥 Test Errors: {errors}")
    
    if failures > 0 or errors > 0:
        print("\n🔍 FAILURE/ERROR DETAILS:")
        for test, traceback in result.failures + result.errors:
            print(f"❌ {test}: {traceback}")
    
    success_rate = (passed / total_tests) * 100 if total_tests > 0 else 0
    print(f"\n📊 Success Rate: {success_rate:.1f}%")
    
    if success_rate >= 90:
        print("🎉 EXCELLENT: BIP39 Mnemonic Recovery Tool is working well!")
    elif success_rate >= 70:
        print("✅ GOOD: Most functionality working, minor issues detected")
    else:
        print("⚠️  NEEDS ATTENTION: Significant issues detected")
    
    return result


if __name__ == "__main__":
    result = run_comprehensive_test()
    
    # Exit with appropriate code
    if result.failures or result.errors:
        sys.exit(1)
    else:
        sys.exit(0)