"""Example usage of Weather Dashboard"""

import os
from dotenv import load_dotenv
from jarvis.weather import WeatherDashboard

# Load environment variables
load_dotenv()

api_key = os.getenv("OPENWEATHER_API_KEY")

if not api_key:
    print("Error: OPENWEATHER_API_KEY not found in environment variables.")
    print("Please set up your .env file with your OpenWeatherMap API key.")
    print("Get a free API key at: https://openweathermap.org/api")
    exit(1)

# Create dashboard instance
dashboard = WeatherDashboard(api_key)

# Display current weather
print("\n🌤️  Fetching current weather...")
dashboard.display_current_weather("London")

# Display forecast
print("📅 Fetching 5-day forecast...")
dashboard.display_forecast("London", days=5)

# You can also use Fahrenheit
print("\n🌡️  Weather in Fahrenheit:")
dashboard.display_current_weather("New York", units="imperial")
