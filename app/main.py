from fastapi import FastAPI

from app.api.health import router as health_router
from src.api.v1.weather.weather import router as weather_router

app = FastAPI()

app.include_router(health_router)
app.include_router(weather_router, prefix="/api/v1")
