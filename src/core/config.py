import os

from dotenv import load_dotenv

load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
OPENWEATHER_URL = os.getenv("OPENWEATHER_URL")
WEATHER_UNITS = os.getenv("WEATHER_UNITS")
WEATHER_LANGUAGE = os.getenv("WEATHER_LANGUAGE")
WEATHER_REQUEST_TIMEOUT = float(os.getenv("WEATHER_REQUEST_TIMEOUT", "5"))
