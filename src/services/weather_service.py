import httpx2

from src.core.config import (
    OPENWEATHER_API_KEY,
    OPENWEATHER_URL,
    WEATHER_LANGUAGE,
    WEATHER_UNITS,
)


def get_weather_for_city(city: str):
    params = {
        "q": city,
        "appid": OPENWEATHER_API_KEY,
        "units": WEATHER_UNITS,
        "lang": WEATHER_LANGUAGE,
    }
    response = httpx2.get(OPENWEATHER_URL, params=params)
    weather_data = response.json()

    return {
        "city": weather_data["name"],
        "temperature": weather_data["main"]["temp"],
        "description": weather_data["weather"][0]["description"],
    }
