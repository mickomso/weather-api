from unittest.mock import patch

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
