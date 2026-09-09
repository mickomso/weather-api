from fastapi import APIRouter, HTTPException

from src.services.weather_service import get_weather_for_city

router = APIRouter()


@router.get("/weather")
def get_weather(city: str):
    weather = get_weather_for_city(city)
    if weather is None:
        raise HTTPException(status_code=404, detail="City not found")
    return weather
