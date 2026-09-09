from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app


class TestWeather:
    client = TestClient(app)

    def test_get_weather_for_valid_city_returns_weather_data(self):
        response = self.client.get("/api/v1/weather?city=Valencia")
        assert response.status_code == 200
        assert "city" in response.json()
        assert "temperature" in response.json()
        assert "description" in response.json()
        assert response.json()["city"] == "Valencia"

    def test_get_weather_passes_city_to_weather_service(self):
        with patch(
            "src.api.v1.weather.weather.get_weather_for_city"
        ) as mock_get_weather:
            mock_get_weather.return_value = {
                "city": "Valencia",
                "temperature": 25.0,
                "description": "Sunny",
            }
            response = self.client.get("/api/v1/weather?city=Valencia")
            assert response.status_code == 200
            mock_get_weather.assert_called_once_with("Valencia")

    def test_get_weather_without_city_returns_422(self):
        response = self.client.get("/api/v1/weather")
        assert response.status_code == 422

    def test_get_weather_for_invalid_city_returns_404(self):
        with patch(
            "src.api.v1.weather.weather.get_weather_for_city"
        ) as mock_get_weather:
            mock_get_weather.return_value = None
            response = self.client.get("/api/v1/weather?city=InvalidCity")
            assert response.status_code == 404
            assert response.json() == {"detail": "City not found"}
