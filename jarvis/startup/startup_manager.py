"""Startup Manager for Jarvis - Add to system startup"""

import os
import platform
import subprocess
from pathlib import Path
from typing import Optional


class StartupManager:
    """Manage Jarvis startup on system boot"""

    def __init__(self):
        """Initialize Startup Manager"""
        self.system = platform.system()
        self.script_path = os.path.abspath(__file__)
        self.jarvis_root = Path(self.script_path).parent.parent.parent
        self.startup_script = self.jarvis_root / "example_app_launcher.py"

    def enable_startup_windows(self) -> bool:
        """Enable startup for Windows

        Returns:
            True if successful, False otherwise
        """
        try:
            import winreg
            from pathlib import Path

            # Get Python executable path
            python_path = os.sys.executable
            script_path = str(self.startup_script)

            # Create registry entry
            registry_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
            key_name = "Jarvis"

            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, registry_path, 0, winreg.KEY_WRITE) as key:
                command = f'"{python_path}" "{script_path}"'
                winreg.SetValueEx(key, key_name, 0, winreg.REG_SZ, command)

            print("✅ Jarvis added to Windows startup")
            print(f"   Path: {registry_path}\\{key_name}")
            return True

        except ImportError:
            print("❌ This feature requires Windows")
            return False
        except Exception as e:
            print(f"❌ Error enabling startup: {e}")
            return False

    def disable_startup_windows(self) -> bool:
        """Disable startup for Windows

        Returns:
            True if successful, False otherwise
        """
        try:
            import winreg

            registry_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
            key_name = "Jarvis"

            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, registry_path, 0, winreg.KEY_WRITE) as key:
                try:
                    winreg.DeleteValue(key, key_name)
                    print("✅ Jarvis removed from Windows startup")
                    return True
                except FileNotFoundError:
                    print("⚠️  Jarvis was not in startup")
                    return False

        except ImportError:
            print("❌ This feature requires Windows")
            return False
        except Exception as e:
            print(f"❌ Error disabling startup: {e}")
            return False

    def enable_startup_macos(self) -> bool:
        """Enable startup for macOS using LaunchAgent

        Returns:
            True if successful, False otherwise
        """
        try:
            import plistlib

            # Create launch agent directory if it doesn't exist
            launch_agents_dir = Path.home() / ".config" / "launchd"
            launch_agents_dir.mkdir(parents=True, exist_ok=True)

            # Create plist file
            plist_path = launch_agents_dir / "com.jarvis.plist"
            python_path = os.sys.executable
            script_path = str(self.startup_script)

            plist_content = {
                "Label": "com.jarvis",
                "ProgramArguments": [python_path, script_path],
                "RunAtLoad": True,
                "KeepAlive": True,
                "StandardOutPath": str(self.jarvis_root / "jarvis.log"),
                "StandardErrorPath": str(self.jarvis_root / "jarvis_error.log"),
            }

            with open(plist_path, "wb") as f:
                plistlib.dump(plist_content, f)

            # Register with launchd
            subprocess.run(["launchctl", "load", str(plist_path)], check=False)

            print("✅ Jarvis added to macOS startup")
            print(f"   LaunchAgent: {plist_path}")
            return True

        except Exception as e:
            print(f"❌ Error enabling startup: {e}")
            return False

    def disable_startup_macos(self) -> bool:
        """Disable startup for macOS

        Returns:
            True if successful, False otherwise
        """
        try:
            launch_agents_dir = Path.home() / ".config" / "launchd"
            plist_path = launch_agents_dir / "com.jarvis.plist"

            if plist_path.exists():
                subprocess.run(["launchctl", "unload", str(plist_path)], check=False)
                plist_path.unlink()
                print("✅ Jarvis removed from macOS startup")
                return True
            else:
                print("⚠️  Jarvis was not in startup")
                return False

        except Exception as e:
            print(f"❌ Error disabling startup: {e}")
            return False

    def enable_startup_linux(self) -> bool:
        """Enable startup for Linux using autostart

        Returns:
            True if successful, False otherwise
        """
        try:
            # Create autostart directory if it doesn't exist
            autostart_dir = Path.home() / ".config" / "autostart"
            autostart_dir.mkdir(parents=True, exist_ok=True)

            # Create desktop entry file
            desktop_file = autostart_dir / "jarvis.desktop"
            python_path = os.sys.executable
            script_path = str(self.startup_script)

            content = f"""[Desktop Entry]
Version=1.0
Type=Application
Name=Jarvis
Comment=Voice Assistant
Exec={python_path} {script_path}
StartupNotify=false
Terminal=true
Categories=Utility;
"""

            with open(desktop_file, "w") as f:
                f.write(content)

            # Make it executable
            os.chmod(desktop_file, 0o755)

            print("✅ Jarvis added to Linux autostart")
            print(f"   Desktop Entry: {desktop_file}")
            return True

        except Exception as e:
            print(f"❌ Error enabling startup: {e}")
            return False

    def disable_startup_linux(self) -> bool:
        """Disable startup for Linux

        Returns:
            True if successful, False otherwise
        """
        try:
            autostart_dir = Path.home() / ".config" / "autostart"
            desktop_file = autostart_dir / "jarvis.desktop"

            if desktop_file.exists():
                desktop_file.unlink()
                print("✅ Jarvis removed from Linux autostart")
                return True
            else:
                print("⚠️  Jarvis was not in autostart")
                return False

        except Exception as e:
            print(f"❌ Error disabling startup: {e}")
            return False

    def enable_startup(self) -> bool:
        """Enable Jarvis to start on system boot

        Returns:
            True if successful, False otherwise
        """
        print(f"\n🚀 Enabling startup for {self.system}...\n")

        if self.system == "Windows":
            return self.enable_startup_windows()
        elif self.system == "Darwin":
            return self.enable_startup_macos()
        elif self.system == "Linux":
            return self.enable_startup_linux()
        else:
            print(f"❌ Unsupported operating system: {self.system}")
            return False

    def disable_startup(self) -> bool:
        """Disable Jarvis from starting on system boot

        Returns:
            True if successful, False otherwise
        """
        print(f"\n🚀 Disabling startup for {self.system}...\n")

        if self.system == "Windows":
            return self.disable_startup_windows()
        elif self.system == "Darwin":
            return self.disable_startup_macos()
        elif self.system == "Linux":
            return self.disable_startup_linux()
        else:
            print(f"❌ Unsupported operating system: {self.system}")
            return False

    def is_startup_enabled(self) -> bool:
        """Check if Jarvis is enabled for startup

        Returns:
            True if enabled, False otherwise
        """
        try:
            if self.system == "Windows":
                import winreg
                registry_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, registry_path, 0, winreg.KEY_READ) as key:
                    try:
                        winreg.QueryValueEx(key, "Jarvis")
                        return True
                    except FileNotFoundError:
                        return False

            elif self.system == "Darwin":
                plist_path = Path.home() / ".config" / "launchd" / "com.jarvis.plist"
                return plist_path.exists()

            elif self.system == "Linux":
                desktop_file = Path.home() / ".config" / "autostart" / "jarvis.desktop"
                return desktop_file.exists()

        except Exception as e:
            print(f"Error checking startup status: {e}")

        return False

    def print_status(self) -> None:
        """Print startup status"""
        status = "Enabled" if self.is_startup_enabled() else "Disabled"
        print(f"\n" + "="*60)
        print(f"🚀 Jarvis Startup Status: {status}")
        print(f"   Operating System: {self.system}")
        print(f"   Script: {self.startup_script}")
        print("="*60 + "\n")
