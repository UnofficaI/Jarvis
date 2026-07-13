"""Weather Dashboard for displaying weather information"""

from typing import Optional, List
from datetime import datetime
from .weather_api import WeatherAPI


class WeatherDashboard:
    """Display weather information in a formatted dashboard"""

    def __init__(self, api_key: str):
        """Initialize Weather Dashboard

        Args:
            api_key: OpenWeatherMap API key
        """
        self.api = WeatherAPI(api_key)

    def display_current_weather(self, city: str, units: str = "metric") -> None:
        """Display current weather for a city

        Args:
            city: City name
            units: Temperature units ('metric', 'imperial', 'standard')
        """
        weather_data = self.api.get_current_weather(city, units)

        if not weather_data:
            print(f"Could not fetch weather data for {city}")
            return

        self._print_current_weather(weather_data, units)

    def display_forecast(self, city: str, units: str = "metric", days: int = 5) -> None:
        """Display weather forecast for a city

        Args:
            city: City name
            units: Temperature units ('metric', 'imperial', 'standard')
            days: Number of days to display (max 5)
        """
        forecast_data = self.api.get_forecast(city, units)

        if not forecast_data:
            print(f"Could not fetch forecast data for {city}")
            return

        self._print_forecast(forecast_data, units, days)

    def _print_current_weather(self, weather_data: dict, units: str) -> None:
        """Print formatted current weather

        Args:
            weather_data: Weather data from API
            units: Temperature units
        """
        city = weather_data.get("name", "Unknown")
        country = weather_data.get("sys", {}).get("country", "")
        temp = weather_data.get("main", {}).get("temp", "N/A")
        feels_like = weather_data.get("main", {}).get("feels_like", "N/A")
        humidity = weather_data.get("main", {}).get("humidity", "N/A")
        pressure = weather_data.get("main", {}).get("pressure", "N/A")
        description = weather_data.get("weather", [{}])[0].get("description", "N/A")
        wind_speed = weather_data.get("wind", {}).get("speed", "N/A")

        unit_symbol = "°C" if units == "metric" else "°F"

        print("\n" + "="*50)
        print(f"🌍 WEATHER DASHBOARD - {city}, {country}")
        print("="*50)
        print(f"📊 Current Weather: {description.capitalize()}")
        print(f"🌡️  Temperature: {temp}{unit_symbol}")
        print(f"🤔 Feels Like: {feels_like}{unit_symbol}")
        print(f"💧 Humidity: {humidity}%")
        print(f"🔽 Pressure: {pressure} hPa")
        print(f"💨 Wind Speed: {wind_speed} m/s")
        print("="*50 + "\n")

    def _print_forecast(self, forecast_data: dict, units: str, days: int) -> None:
        """Print formatted forecast

        Args:
            forecast_data: Forecast data from API
            units: Temperature units
            days: Number of days to display
        """
        city = forecast_data.get("city", {}).get("name", "Unknown")
        country = forecast_data.get("city", {}).get("country", "")
        list_data = forecast_data.get("list", [])

        unit_symbol = "°C" if units == "metric" else "°F"
        displayed_days = 0
        last_date = None

        print("\n" + "="*50)
        print(f"📅 FORECAST - {city}, {country}")
        print("="*50)

        for item in list_data:
            if displayed_days >= days:
                break

            timestamp = datetime.fromtimestamp(item.get("dt", 0))
            current_date = timestamp.date()

            if last_date and current_date != last_date:
                displayed_days += 1

            last_date = current_date

            if displayed_days < days:
                temp = item.get("main", {}).get("temp", "N/A")
                description = item.get("weather", [{}])[0].get("description", "N/A")
                humidity = item.get("main", {}).get("humidity", "N/A")
                wind_speed = item.get("wind", {}).get("speed", "N/A")

                print(f"\n📍 {timestamp.strftime('%a, %b %d %H:%M')}")
                print(f"   Description: {description.capitalize()}")
                print(f"   Temp: {temp}{unit_symbol} | Humidity: {humidity}% | Wind: {wind_speed} m/s")

        print("\n" + "="*50 + "\n")
