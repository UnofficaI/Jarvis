"""Tests for Startup Manager module"""

import unittest
from unittest.mock import patch
from jarvis.startup import StartupManager


class TestStartupManager(unittest.TestCase):
    """Test cases for StartupManager class"""

    def setUp(self):
        """Set up test fixtures"""
        self.manager = StartupManager()

    def test_initialization(self):
        """Test StartupManager initialization"""
        self.assertIsNotNone(self.manager.system)
        self.assertIsNotNone(self.manager.startup_script)

    def test_is_startup_enabled(self):
        """Test checking startup status"""
        # Just check that it returns a boolean
        result = self.manager.is_startup_enabled()
        self.assertIsInstance(result, bool)

    def test_print_status(self):
        """Test printing startup status"""
        # Should not raise an exception
        try:
            self.manager.print_status()
        except Exception as e:
            self.fail(f"print_status raised {type(e).__name__} unexpectedly!")


if __name__ == "__main__":
    unittest.main()
