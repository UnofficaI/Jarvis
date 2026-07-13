"""Example voice assistant with app launching capabilities"""

import os
from dotenv import load_dotenv
from jarvis.voice import VoiceAssistant
from jarvis.weather import WeatherDashboard
from jarvis.apps import AppLauncher

# Load environment variables
load_dotenv()

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
    """Handle weather-related commands"""
    if not weather:
        assistant.speaker.speak("Weather API is not configured.")
        return

    city = "London"  # default city

    if "weather" in text or "temperature" in text:
        if "forecast" in text:
            assistant.speaker.speak(f"Getting 5-day forecast for {city}")
            weather.display_forecast(city)
        else:
            assistant.speaker.speak(f"Getting weather for {city}")
            weather.display_current_weather(city)


def handle_app_launch_command(text: str) -> None:
    """Handle app launching commands"""
    # Extract app name from command
    # Examples: "open chrome", "launch firefox", "start notepad"
    words = text.split()
    
    # Remove command words like "open", "launch", "start"
    command_words = ["open", "launch", "start", "run", "close"]
    app_name = None
    
    for i, word in enumerate(words):
        if word in command_words:
            # Get the word(s) after the command
            if i + 1 < len(words):
                app_name = " ".join(words[i+1:])
                break
    
    if not app_name:
        assistant.speaker.speak("Please specify which application to open.")
        return
    
    # Check if it's a close command
    if "close" in words:
        if app_launcher.close_app(app_name):
            assistant.speaker.speak(f"Closing {app_name}")
        else:
            assistant.speaker.speak(f"Could not close {app_name}")
    else:
        if app_launcher.launch_app(app_name):
            assistant.speaker.speak(f"Opening {app_name}")
        else:
            assistant.speaker.speak(f"Could not open {app_name}. Please check the name and try again.")


def handle_greeting(text: str) -> None:
    """Handle greeting commands"""
    assistant.speaker.speak(f"Hello! How can I assist you?")


def handle_time_command(text: str) -> None:
    """Handle time commands"""
    from datetime import datetime
    current_time = datetime.now().strftime("%I:%M %p")
    assistant.speaker.speak(f"The current time is {current_time}")


def handle_date_command(text: str) -> None:
    """Handle date commands"""
    from datetime import datetime
    current_date = datetime.now().strftime("%A, %B %d, %Y")
    assistant.speaker.speak(f"Today is {current_date}")


def handle_help_command(text: str) -> None:
    """Handle help commands"""
    help_text = "I can help you with: opening apps, weather, time, date, and more. Just ask!"
    assistant.speaker.speak(help_text)
    print(f"\n📋 Available Commands:\n")
    print("  APPS:")
    print("    - 'open [app name]' - Open an application")
    print("    - 'launch [app name]' - Launch an application")
    print("    - 'close [app name]' - Close an application")
    print("    - 'list apps' - Show available applications")
    print("\n  WEATHER:")
    print("    - 'weather' or 'temperature' - Get current weather")
    print("    - 'forecast' - Get 5-day forecast")
    print("\n  OTHER:")
    print("    - 'time' - Get current time")
    print("    - 'date' - Get current date")
    print("    - 'hello' or 'hi' - Greet Jarvis")
    print("    - 'help' - Get help")
    print("    - 'stop' or 'exit' - Stop Jarvis\n")


def handle_list_apps_command(text: str) -> None:
    """Handle list apps command"""
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

# Print available commands and apps
print("\n" + "="*60)
print("🤖 JARVIS - Voice Assistant with App Launcher")
print("="*60)
print("\n📋 Available Commands:")
print("\n  APPS:")
print("    - 'open [app name]' - Open an application")
print("    - 'launch [app name]' - Launch an application")
print("    - 'close [app name]' - Close an application")
print("    - 'list apps' - Show available applications")
print("\n  WEATHER:")
print("    - 'weather' or 'temperature' - Get current weather")
print("    - 'forecast' - Get 5-day forecast")
print("\n  OTHER:")
print("    - 'time' - Get current time")
print("    - 'date' - Get current date")
print("    - 'hello' or 'hi' - Greet Jarvis")
print("    - 'help' - Get help")
print("    - 'stop' or 'exit' - Stop Jarvis")
print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    try:
        # Start listening for commands (continuous mode)
        print("Starting voice assistant in continuous mode...\n")
        assistant.listen_and_process(continuous=True)
    except KeyboardInterrupt:
        print("\n\nShutting down...")
        assistant.stop()
