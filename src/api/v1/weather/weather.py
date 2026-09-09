from fastapi import APIRouter

router = APIRouter()


@router.get("/weather")
def get_weather_for_city(city: str):
    return {"city": city, "temperature": 25.0, "description": "Sunny"}
