"""Application Launcher for Jarvis"""

import subprocess
import platform
import os
from typing import Dict, List, Optional


class AppLauncher:
    """Launch applications from voice commands"""

    def __init__(self):
        """Initialize App Launcher"""
        self.system = platform.system()
        self.app_registry: Dict[str, Dict[str, str]] = {}
        self._load_default_apps()

    def _load_default_apps(self) -> None:
        """Load default applications for the system"""
        if self.system == "Windows":
            self.app_registry = {
                "chrome": {"name": "Google Chrome", "path": "chrome", "keywords": ["chrome", "browser"]},
                "firefox": {"name": "Firefox", "path": "firefox", "keywords": ["firefox"]},
                "edge": {"name": "Microsoft Edge", "path": "msedge", "keywords": ["edge"]},
                "notepad": {"name": "Notepad", "path": "notepad", "keywords": ["notepad", "text editor"]},
                "calculator": {"name": "Calculator", "path": "calc", "keywords": ["calculator", "calc"]},
                "word": {"name": "Microsoft Word", "path": "winword", "keywords": ["word"]},
                "excel": {"name": "Microsoft Excel", "path": "excel", "keywords": ["excel"]},
                "powerpoint": {"name": "PowerPoint", "path": "powerpnt", "keywords": ["powerpoint", "ppt"]},
                "outlook": {"name": "Outlook", "path": "outlook", "keywords": ["outlook", "email"]},
                "vlc": {"name": "VLC Media Player", "path": "vlc", "keywords": ["vlc", "video player"]},
                "spotify": {"name": "Spotify", "path": "spotify", "keywords": ["spotify", "music"]},
                "discord": {"name": "Discord", "path": "discord", "keywords": ["discord"]},
                "slack": {"name": "Slack", "path": "slack", "keywords": ["slack"]},
                "teams": {"name": "Microsoft Teams", "path": "teams", "keywords": ["teams"]},
                "vscode": {"name": "Visual Studio Code", "path": "code", "keywords": ["code", "vs code", "vscode"]},
            }
        elif self.system == "Darwin":  # macOS
            self.app_registry = {
                "chrome": {"name": "Google Chrome", "path": "/Applications/Google Chrome.app", "keywords": ["chrome", "browser"]},
                "firefox": {"name": "Firefox", "path": "/Applications/Firefox.app", "keywords": ["firefox"]},
                "safari": {"name": "Safari", "path": "/Applications/Safari.app", "keywords": ["safari"]},
                "notes": {"name": "Notes", "path": "/Applications/Notes.app", "keywords": ["notes", "notes app"]},
                "calculator": {"name": "Calculator", "path": "/Applications/Calculator.app", "keywords": ["calculator", "calc"]},
                "vlc": {"name": "VLC Media Player", "path": "/Applications/VLC.app", "keywords": ["vlc", "video player"]},
                "spotify": {"name": "Spotify", "path": "/Applications/Spotify.app", "keywords": ["spotify", "music"]},
                "discord": {"name": "Discord", "path": "/Applications/Discord.app", "keywords": ["discord"]},
                "slack": {"name": "Slack", "path": "/Applications/Slack.app", "keywords": ["slack"]},
                "vscode": {"name": "Visual Studio Code", "path": "/Applications/Visual Studio Code.app", "keywords": ["code", "vs code", "vscode"]},
            }
        elif self.system == "Linux":
            self.app_registry = {
                "chrome": {"name": "Google Chrome", "path": "google-chrome", "keywords": ["chrome", "browser"]},
                "firefox": {"name": "Firefox", "path": "firefox", "keywords": ["firefox"]},
                "gedit": {"name": "Gedit", "path": "gedit", "keywords": ["gedit", "text editor"]},
                "calculator": {"name": "Calculator", "path": "gnome-calculator", "keywords": ["calculator", "calc"]},
                "vlc": {"name": "VLC Media Player", "path": "vlc", "keywords": ["vlc", "video player"]},
                "spotify": {"name": "Spotify", "path": "spotify", "keywords": ["spotify", "music"]},
                "discord": {"name": "Discord", "path": "discord", "keywords": ["discord"]},
                "slack": {"name": "Slack", "path": "slack", "keywords": ["slack"]},
                "vscode": {"name": "Visual Studio Code", "path": "code", "keywords": ["code", "vs code", "vscode"]},
            }

    def register_app(self, app_id: str, name: str, path: str, keywords: List[str]) -> None:
        """Register a custom application

        Args:
            app_id: Unique identifier for the app
            name: Display name of the app
            path: Path to the app executable
            keywords: Keywords that trigger this app
        """
        self.app_registry[app_id] = {
            "name": name,
            "path": path,
            "keywords": [keyword.lower() for keyword in keywords]
        }
        print(f"✅ Registered app: {name}")

    def get_app_by_keyword(self, keyword: str) -> Optional[Dict[str, str]]:
        """Find an app by keyword

        Args:
            keyword: Keyword to search for

        Returns:
            App dictionary or None if not found
        """
        keyword = keyword.lower()
        for app_id, app_info in self.app_registry.items():
            if keyword in app_info["keywords"]:
                return app_info
        return None

    def launch_app(self, app_name: str) -> bool:
        """Launch an application

        Args:
            app_name: Name or keyword of the application to launch

        Returns:
            True if app launched successfully, False otherwise
        """
        try:
            # Try to find app by keyword
            app_info = self.get_app_by_keyword(app_name)

            if not app_info:
                print(f"❌ Application '{app_name}' not found in registry")
                return False

            app_path = app_info["path"]
            app_display_name = app_info["name"]

            print(f"🚀 Launching {app_display_name}...")

            if self.system == "Windows":
                subprocess.Popen(app_path)
            elif self.system == "Darwin":  # macOS
                subprocess.Popen(["open", "-a", app_path])
            elif self.system == "Linux":
                subprocess.Popen(app_path)

            print(f"✅ {app_display_name} launched successfully!")
            return True

        except FileNotFoundError:
            print(f"❌ Could not find application: {app_name}")
            return False
        except Exception as e:
            print(f"❌ Error launching app: {e}")
            return False

    def launch_app_with_args(self, app_name: str, args: List[str] = None) -> bool:
        """Launch an application with arguments

        Args:
            app_name: Name or keyword of the application
            args: List of arguments to pass to the app

        Returns:
            True if app launched successfully, False otherwise
        """
        try:
            app_info = self.get_app_by_keyword(app_name)

            if not app_info:
                print(f"❌ Application '{app_name}' not found")
                return False

            app_path = app_info["path"]
            app_display_name = app_info["name"]

            print(f"🚀 Launching {app_display_name}...")

            if args is None:
                args = []

            if self.system == "Windows":
                subprocess.Popen([app_path] + args)
            elif self.system == "Darwin":
                subprocess.Popen(["open", "-a", app_path] + args)
            elif self.system == "Linux":
                subprocess.Popen([app_path] + args)

            print(f"✅ {app_display_name} launched successfully!")
            return True

        except Exception as e:
            print(f"❌ Error launching app: {e}")
            return False

    def list_available_apps(self) -> None:
        """List all available applications"""
        print("\n" + "="*60)
        print("📱 Available Applications")
        print("="*60)
        for app_id, app_info in self.app_registry.items():
            keywords_str = ", ".join(app_info["keywords"])
            print(f"  • {app_info['name']}")
            print(f"    Keywords: {keywords_str}")
        print("="*60 + "\n")

    def close_app(self, app_name: str) -> bool:
        """Close a running application

        Args:
            app_name: Name or keyword of the application

        Returns:
            True if app closed successfully, False otherwise
        """
        try:
            app_info = self.get_app_by_keyword(app_name)
            if not app_info:
                print(f"❌ Application '{app_name}' not found")
                return False

            app_display_name = app_info["name"]

            if self.system == "Windows":
                subprocess.run(["taskkill", "/IM", f"{app_info['path']}.exe", "/F"])
            elif self.system == "Darwin":
                subprocess.run(["pkill", "-f", app_display_name])
            elif self.system == "Linux":
                subprocess.run(["pkill", "-f", app_info["path"]])

            print(f"✅ {app_display_name} closed successfully!")
            return True

        except Exception as e:
            print(f"❌ Error closing app: {e}")
            return False
