from unittest.mock import patch

from src.core.config import OPENWEATHER_URL, WEATHER_LANGUAGE, WEATHER_UNITS
from src.services.weather_service import get_weather_for_city


class TestGetWeatherService:
    def test_get_weather_for_valid_city_returns_weather_data(self):
        with patch("src.services.weather_service.httpx2.get") as mock_get:
            mock_get.return_value.json.return_value = {
                "name": "Valencia",
                "main": {
                    "temp": 25.0,
                },
                "weather": [
                    {
                        "description": "cielo claro",
                    }
                ],
            }

            weather = get_weather_for_city("Valencia")

        assert weather == {
            "city": "Valencia",
            "temperature": 25.0,
            "description": "cielo claro",
        }

        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        assert args[0] == OPENWEATHER_URL
        assert kwargs["params"]["q"] == "Valencia"
        assert kwargs["params"]["units"] == WEATHER_UNITS
        assert kwargs["params"]["lang"] == WEATHER_LANGUAGE
        assert "appid" in kwargs["params"]
