from fastapi import APIRouter, HTTPException, Query

from app.schemas.weather import WeatherResponse
from app.services.exceptions import (
    WeatherConfigurationError,
    WeatherServiceUnavailableError,
)
from app.services.weather_service import get_weather_for_city

router = APIRouter()


@router.get("/weather", response_model=WeatherResponse)
def get_weather(city: str = Query(min_length=1)):
    try:
        weather = get_weather_for_city(city)
    except WeatherConfigurationError:
        raise HTTPException(status_code=500, detail="Weather service misconfigured")
    except WeatherServiceUnavailableError:
        raise HTTPException(status_code=502, detail="Weather service unavailable")

    if weather is None:
        raise HTTPException(status_code=404, detail="City not found")

    return weather
