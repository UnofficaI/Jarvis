"""Example voice assistant with weather command"""

import os
from dotenv import load_dotenv
from jarvis.voice import VoiceAssistant
from jarvis.weather import WeatherDashboard

# Load environment variables
load_dotenv()

# Initialize voice assistant
assistant = VoiceAssistant(name="Jarvis", voice_id=0)  # voice_id: 0=male, 1=female

# Initialize weather dashboard
api_key = os.getenv("OPENWEATHER_API_KEY")
if api_key:
    weather = WeatherDashboard(api_key)
else:
    weather = None
    assistant.speaker.speak("Weather API key not configured. Weather commands won't work.")


def handle_weather_command(text: str) -> None:
    """Handle weather-related commands"""
    if not weather:
        assistant.speaker.speak("Weather API is not configured.")
        return

    # Extract city name if mentioned
    city = "London"  # default city

    if "weather" in text or "temperature" in text:
        if "forecast" in text:
            assistant.speaker.speak(f"Getting 5-day forecast for {city}")
            weather.display_forecast(city)
        else:
            assistant.speaker.speak(f"Getting weather for {city}")
            weather.display_current_weather(city)


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
    help_text = "I can help you with: weather, time, date, and more. Just ask!"
    assistant.speaker.speak(help_text)
    print(f"\n📋 Available Commands:\n")
    print("  - 'weather' or 'temperature' - Get current weather")
    print("  - 'forecast' - Get 5-day forecast")
    print("  - 'time' - Get current time")
    print("  - 'date' - Get current date")
    print("  - 'hello' or 'hi' - Greet Jarvis")
    print("  - 'help' - Get help")
    print("  - 'stop' or 'exit' - Stop Jarvis\n")


# Register commands
assistant.register_command(["weather", "temperature", "forecast"], handle_weather_command)
assistant.register_command(["hello", "hi", "hey"], handle_greeting)
assistant.register_command(["time"], handle_time_command)
assistant.register_command(["date"], handle_date_command)
assistant.register_command(["help"], handle_help_command)

# Print available commands
print("\n" + "="*60)
print("🤖 JARVIS - Voice Assistant")
print("="*60)
print("\n📋 Available Commands:")
print("  - 'weather' or 'temperature' - Get current weather")
print("  - 'forecast' - Get 5-day forecast")
print("  - 'time' - Get current time")
print("  - 'date' - Get current date")
print("  - 'hello' or 'hi' - Greet Jarvis")
print("  - 'help' - Get help")
print("  - 'stop' or 'exit' - Stop Jarvis")
print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    try:
        # Start listening for commands (continuous mode)
        print("Starting voice assistant in continuous mode...\n")
        assistant.listen_and_process(continuous=True)
    except KeyboardInterrupt:
        print("\n\nShutting down...")
        assistant.stop()
