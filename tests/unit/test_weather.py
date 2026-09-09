from fastapi.testclient import TestClient

from app.main import app


class TestWeather:
    client = TestClient(app)

    def test_get_weather_for_Valencia_city_returns_weather_data(self):
        response = self.client.get("/api/v1/weather?city=Valencia")
        assert response.status_code == 200
        assert "city" in response.json()
        assert "temperature" in response.json()
        assert "description" in response.json()
        assert response.json()["city"] == "Valencia"
