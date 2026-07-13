"""Weather API integration with OpenWeatherMap"""

import requests
from typing import Dict, Optional


class WeatherAPI:
    """Fetch weather data from OpenWeatherMap API"""

    BASE_URL = "https://api.openweathermap.org/data/2.5"

    def __init__(self, api_key: str):
        """Initialize Weather API with API key

        Args:
            api_key: OpenWeatherMap API key
        """
        self.api_key = api_key

    def get_current_weather(self, city: str, units: str = "metric") -> Optional[Dict]:
        """Get current weather for a city

        Args:
            city: City name
            units: Temperature units ('metric', 'imperial', 'standard')

        Returns:
            Dictionary with weather data or None if request fails
        """
        try:
            url = f"{self.BASE_URL}/weather"
            params = {
                "q": city,
                "appid": self.api_key,
                "units": units
            }
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather data: {e}")
            return None

    def get_forecast(self, city: str, units: str = "metric") -> Optional[Dict]:
        """Get 5-day weather forecast for a city

        Args:
            city: City name
            units: Temperature units ('metric', 'imperial', 'standard')

        Returns:
            Dictionary with forecast data or None if request fails
        """
        try:
            url = f"{self.BASE_URL}/forecast"
            params = {
                "q": city,
                "appid": self.api_key,
                "units": units
            }
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching forecast data: {e}")
            return None

    def get_weather_by_coordinates(
        self, lat: float, lon: float, units: str = "metric"
    ) -> Optional[Dict]:
        """Get weather by latitude and longitude

        Args:
            lat: Latitude
            lon: Longitude
            units: Temperature units ('metric', 'imperial', 'standard')

        Returns:
            Dictionary with weather data or None if request fails
        """
        try:
            url = f"{self.BASE_URL}/weather"
            params = {
                "lat": lat,
                "lon": lon,
                "appid": self.api_key,
                "units": units
            }
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather data: {e}")
            return None
