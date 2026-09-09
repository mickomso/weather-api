from unittest.mock import patch

import httpx2
import pytest

from src.core.config import (
    OPENWEATHER_URL,
    WEATHER_LANGUAGE,
    WEATHER_REQUEST_TIMEOUT,
    WEATHER_UNITS,
)
from src.services import weather_service
from src.services.exceptions import (
    WeatherConfigurationError,
    WeatherServiceUnavailableError,
)
from src.services.weather_service import get_weather_for_city


class TestGetWeatherService:
    @pytest.fixture
    def mock_http_get(self):
        with patch("src.services.weather_service.httpx2.get") as mock_get:
            yield mock_get

    @pytest.fixture
    def valid_weather_response(self):
        return {
            "name": "Valencia",
            "main": {"temp": 25.0},
            "weather": [{"description": "cielo claro"}],
        }

    @pytest.fixture
    def city_not_found_response(self):
        return {
            "cod": "404",
            "message": "city not found",
        }

    @pytest.fixture
    def valid_weather_data(self):
        return {
            "city": "Valencia",
            "temperature": 25.0,
            "description": "cielo claro",
        }

    def test_get_weather_for_valid_city_returns_weather_data(
        self, mock_http_get, valid_weather_response, valid_weather_data
    ):
        mock_http_get.return_value.json.return_value = valid_weather_response

        weather = get_weather_for_city("Valencia")

        assert weather == valid_weather_data

    def test_get_weather_for_city_sends_expected_request(
        self, mock_http_get, valid_weather_response
    ):
        mock_http_get.return_value.json.return_value = valid_weather_response

        get_weather_for_city("Valencia")

        mock_http_get.assert_called_once()
        args, kwargs = mock_http_get.call_args
        assert args[0] == OPENWEATHER_URL
        assert kwargs["params"]["q"] == "Valencia"
        assert kwargs["params"]["units"] == WEATHER_UNITS
        assert kwargs["params"]["lang"] == WEATHER_LANGUAGE
        assert kwargs["params"]["appid"]
        assert kwargs["timeout"] == WEATHER_REQUEST_TIMEOUT

    def test_get_weather_for_invalid_city_returns_none(
        self, mock_http_get, city_not_found_response
    ):
        mock_http_get.return_value.json.return_value = city_not_found_response

        weather = get_weather_for_city("InvalidCity")

        assert weather is None

    def test_get_weather_for_city_accepts_numeric_not_found_code(self, mock_http_get):
        mock_http_get.return_value.json.return_value = {
            "cod": 404,
            "message": "city not found",
        }

        weather = get_weather_for_city("InvalidCity")

        assert weather is None

    def test_get_weather_for_city_raises_when_provider_is_unavailable(
        self, mock_http_get
    ):
        mock_http_get.side_effect = httpx2.HTTPError("Service unavailable")

        with pytest.raises(WeatherServiceUnavailableError):
            get_weather_for_city("Valencia")

    def test_get_weather_for_city_raises_when_provider_times_out(self, mock_http_get):
        mock_http_get.side_effect = httpx2.TimeoutException("Request timed out")

        with pytest.raises(WeatherServiceUnavailableError):
            get_weather_for_city("Valencia")

    def test_get_weather_for_city_raises_when_configuration_is_incomplete(self):
        with (
            patch.object(weather_service, "OPENWEATHER_API_KEY", None),
            pytest.raises(WeatherConfigurationError),
        ):
            get_weather_for_city("Valencia")

    def test_get_weather_for_city_raises_when_provider_returns_server_error(
        self, mock_http_get
    ):
        mock_http_get.return_value.json.return_value = {
            "cod": 500,
            "message": "internal error",
        }
        mock_http_get.return_value.raise_for_status.side_effect = httpx2.HTTPError(
            "Server error"
        )

        with pytest.raises(WeatherServiceUnavailableError):
            get_weather_for_city("Valencia")
