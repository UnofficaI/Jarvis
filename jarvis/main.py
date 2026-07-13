"""Updated main module for Jarvis with autostart setup"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from jarvis.voice import VoiceAssistant
from jarvis.weather import WeatherDashboard
from jarvis.apps import AppLauncher
from jarvis.startup import StartupManager

# Load environment variables
load_dotenv()


def show_menu():
    """Display main menu"""
    print("\n" + "="*60)
    print("🤖 JARVIS - Voice Assistant")
    print("="*60)
    print("\nChoose an option:")
    print("  1. Start Voice Assistant")
    print("  2. Configure Startup Settings")
    print("  3. Exit")
    print("\n" + "="*60)


def configure_startup():
    """Configure startup settings"""
    startup_manager = StartupManager()

    print("\n" + "="*60)
    print("🚀 STARTUP CONFIGURATION")
    print("="*60)
    print("\nChoose an option:")
    print("  1. Enable autostart (Jarvis starts on PC boot)")
    print("  2. Disable autostart")
    print("  3. Check startup status")
    print("  4. Back to main menu")

    choice = input("\nEnter your choice (1-4): ").strip()

    if choice == "1":
        if startup_manager.enable_startup():
            print("\n✅ Jarvis autostart enabled!")
            input("Press Enter to continue...")
    elif choice == "2":
        if startup_manager.disable_startup():
            print("\n✅ Jarvis autostart disabled!")
            input("Press Enter to continue...")
    elif choice == "3":
        startup_manager.print_status()
        input("Press Enter to continue...")
    elif choice == "4":
        return
    else:
        print("\n❌ Invalid choice.")
        input("Press Enter to continue...")


def start_voice_assistant():
    """Start the voice assistant"""
    # Initialize components
    assistant = VoiceAssistant(name="Jarvis", voice_id=0)
    app_launcher = AppLauncher()

    # Initialize weather dashboard
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if api_key:
        weather = WeatherDashboard(api_key)
    else:
        weather = None

    def handle_weather_command(text: str) -> None:
        """Handle weather commands"""
        if not weather:
            assistant.speaker.speak("Weather API is not configured.")
            return
        city = "London"
        if "weather" in text or "temperature" in text:
            if "forecast" in text:
                assistant.speaker.speak(f"Getting 5-day forecast for {city}")
                weather.display_forecast(city)
            else:
                assistant.speaker.speak(f"Getting weather for {city}")
                weather.display_current_weather(city)

    def handle_app_launch_command(text: str) -> None:
        """Handle app launch commands"""
        words = text.split()
        command_words = ["open", "launch", "start", "run", "close"]
        app_name = None

        for i, word in enumerate(words):
            if word in command_words:
                if i + 1 < len(words):
                    app_name = " ".join(words[i+1:])
                    break

        if not app_name:
            assistant.speaker.speak("Please specify which application to open.")
            return

        if "close" in words:
            if app_launcher.close_app(app_name):
                assistant.speaker.speak(f"Closing {app_name}")
            else:
                assistant.speaker.speak(f"Could not close {app_name}")
        else:
            if app_launcher.launch_app(app_name):
                assistant.speaker.speak(f"Opening {app_name}")
            else:
                assistant.speaker.speak(f"Could not open {app_name}")

    def handle_greeting(text: str) -> None:
        assistant.speaker.speak("Hello! How can I assist you?")

    def handle_time_command(text: str) -> None:
        from datetime import datetime
        current_time = datetime.now().strftime("%I:%M %p")
        assistant.speaker.speak(f"The current time is {current_time}")

    def handle_date_command(text: str) -> None:
        from datetime import datetime
        current_date = datetime.now().strftime("%A, %B %d, %Y")
        assistant.speaker.speak(f"Today is {current_date}")

    def handle_help_command(text: str) -> None:
        assistant.speaker.speak("I can help with opening apps, weather, time, date, and more")

    def handle_list_apps_command(text: str) -> None:
        assistant.speaker.speak("Showing available applications")
        app_launcher.list_available_apps()

    # Register commands
    assistant.register_command(["open", "launch", "start", "run", "close"], handle_app_launch_command)
    assistant.register_command(["weather", "temperature", "forecast"], handle_weather_command)
    assistant.register_command(["hello", "hi", "hey"], handle_greeting)
    assistant.register_command(["time"], handle_time_command)
    assistant.register_command(["date"], handle_date_command)
    assistant.register_command(["help"], handle_help_command)
    assistant.register_command(["list apps"], handle_list_apps_command)

    # Print info
    print("\n" + "="*60)
    print("🤖 JARVIS - Voice Assistant")
    print("="*60)
    print("\n📋 Available Commands:")
    print("\n  APPS:")
    print("    - 'open [app]' - Open application")
    print("    - 'launch [app]' - Launch application")
    print("    - 'close [app]' - Close application")
    print("    - 'list apps' - Show available apps")
    print("\n  WEATHER:")
    print("    - 'weather' - Get current weather")
    print("    - 'forecast' - Get 5-day forecast")
    print("\n  OTHER:")
    print("    - 'time' - Get current time")
    print("    - 'date' - Get current date")
    print("    - 'help' - Get help")
    print("    - 'stop' or 'exit' - Stop Jarvis")
    print("\n" + "="*60 + "\n")

    try:
        assistant.listen_and_process(continuous=True)
    except KeyboardInterrupt:
        print("\n\nShutting down...")
        assistant.stop()


def main():
    """Main entry point"""
    while True:
        show_menu()
        choice = input("Enter your choice (1-3): ").strip()

        if choice == "1":
            start_voice_assistant()
        elif choice == "2":
            configure_startup()
        elif choice == "3":
            print("\nGoodbye!")
            sys.exit(0)
        else:
            print("\n❌ Invalid choice. Please try again.")
            input("Press Enter to continue...")


if __name__ == "__main__":
    main()
