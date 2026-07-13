"""Tests for App Launcher module"""

import unittest
from unittest.mock import patch, MagicMock
from jarvis.apps import AppLauncher


class TestAppLauncher(unittest.TestCase):
    """Test cases for AppLauncher class"""

    def setUp(self):
        """Set up test fixtures"""
        self.launcher = AppLauncher()

    def test_register_app(self):
        """Test registering a custom app"""
        self.launcher.register_app(
            "test_app",
            "Test Application",
            "/path/to/app",
            ["test", "testing"]
        )
        self.assertIn("test_app", self.launcher.app_registry)

    def test_get_app_by_keyword(self):
        """Test finding app by keyword"""
        self.launcher.register_app(
            "test_app",
            "Test Application",
            "/path/to/app",
            ["test", "testing"]
        )
        app = self.launcher.get_app_by_keyword("test")
        self.assertIsNotNone(app)
        self.assertEqual(app["name"], "Test Application")

    def test_get_app_not_found(self):
        """Test app not found"""
        app = self.launcher.get_app_by_keyword("nonexistent")
        self.assertIsNone(app)

    @patch("subprocess.Popen")
    def test_launch_app_success(self, mock_popen):
        """Test successful app launch"""
        self.launcher.register_app(
            "test_app",
            "Test Application",
            "/path/to/app",
            ["test"]
        )
        result = self.launcher.launch_app("test")
        self.assertTrue(result)

    def test_launch_app_not_found(self):
        """Test app launch when app doesn't exist"""
        result = self.launcher.launch_app("nonexistent")
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
