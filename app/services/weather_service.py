import httpx2

from app.core.config import (
    OPENWEATHER_API_KEY,
    OPENWEATHER_URL,
    WEATHER_LANGUAGE,
    WEATHER_REQUEST_TIMEOUT,
    WEATHER_UNITS,
)
from app.services.exceptions import (
    WeatherConfigurationError,
    WeatherServiceUnavailableError,
)


def get_weather_for_city(city: str):
    if not OPENWEATHER_API_KEY or not OPENWEATHER_URL:
        raise WeatherConfigurationError("Weather provider configuration is incomplete")

    params = {
        "q": city,
        "appid": OPENWEATHER_API_KEY,
        "units": WEATHER_UNITS,
        "lang": WEATHER_LANGUAGE,
    }
    try:
        response = httpx2.get(
            OPENWEATHER_URL,
            params=params,
            timeout=WEATHER_REQUEST_TIMEOUT,
        )
        weather_data = response.json()

        if str(weather_data.get("cod")) == "404":
            return None

        response.raise_for_status()
    except httpx2.HTTPError as error:
        raise WeatherServiceUnavailableError from error

    return {
        "city": weather_data["name"],
        "temperature": weather_data["main"]["temp"],
        "description": weather_data["weather"][0]["description"],
    }
