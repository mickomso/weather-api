from fastapi import APIRouter

from src.services.weather_service import get_weather_for_city

router = APIRouter()


@router.get("/weather")
def get_weather(city: str):
    weather = get_weather_for_city(city)
    return weather
