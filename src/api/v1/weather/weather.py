from fastapi import APIRouter, HTTPException

from src.services.exceptions import WeatherServiceUnavailableError
from src.services.weather_service import get_weather_for_city

router = APIRouter()


@router.get("/weather")
def get_weather(city: str):
    try:
        weather = get_weather_for_city(city)
    except WeatherServiceUnavailableError:
        raise HTTPException(status_code=502, detail="Weather service unavailable")

    if weather is None:
        raise HTTPException(status_code=404, detail="City not found")

    return weather
