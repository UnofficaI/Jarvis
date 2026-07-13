"""Tests for Weather API module"""

import unittest
from unittest.mock import patch, MagicMock
from jarvis.weather.weather_api import WeatherAPI


class TestWeatherAPI(unittest.TestCase):
    """Test cases for WeatherAPI class"""

    def setUp(self):
        """Set up test fixtures"""
        self.api = WeatherAPI("test_api_key")

    @patch("jarvis.weather.weather_api.requests.get")
    def test_get_current_weather_success(self, mock_get):
        """Test successful current weather fetch"""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "name": "London",
            "sys": {"country": "GB"},
            "main": {"temp": 15, "feels_like": 14, "humidity": 70},
            "weather": [{"description": "Cloudy"}],
        }
        mock_get.return_value = mock_response

        result = self.api.get_current_weather("London")
        self.assertIsNotNone(result)
        self.assertEqual(result["name"], "London")

    @patch("jarvis.weather.weather_api.requests.get")
    def test_get_current_weather_failure(self, mock_get):
        """Test failed current weather fetch"""
        mock_get.side_effect = Exception("API Error")
        result = self.api.get_current_weather("London")
        self.assertIsNone(result)

    @patch("jarvis.weather.weather_api.requests.get")
    def test_get_weather_by_coordinates(self, mock_get):
        """Test weather fetch by coordinates"""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "name": "London",
            "coord": {"lat": 51.51, "lon": -0.13},
        }
        mock_get.return_value = mock_response

        result = self.api.get_weather_by_coordinates(51.51, -0.13)
        self.assertIsNotNone(result)


if __name__ == "__main__":
    unittest.main()
