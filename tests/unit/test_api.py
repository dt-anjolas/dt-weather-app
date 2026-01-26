import pytest
from fastapi.testclient import TestClient

from src.main import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def test_root_endpoint_returns_html(client: TestClient) -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "DataTorque Weather" in response.text


def test_api_info_endpoint(client: TestClient) -> None:
    response = client.get("/api")

    assert response.status_code == 200
    data = response.json()
    assert data["service"] == "DataTorque Weather API"
    assert "version" in data


def test_health_endpoint(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_ready_endpoint(client: TestClient) -> None:
    response = client.get("/ready")

    assert response.status_code == 200
    assert response.json() == {"status": "ready"}


def test_weather_valid_city(client: TestClient) -> None:
    response = client.get("/api/v1/weather/auckland")

    assert response.status_code == 200
    data = response.json()
    assert data["city"] == "Auckland"
    assert data["country"] == "NZ"
    assert "temperature_celsius" in data
    assert "condition" in data


def test_weather_invalid_city(client: TestClient) -> None:
    response = client.get("/api/v1/weather/nonexistent")

    assert response.status_code == 404


def test_forecast_valid_city(client: TestClient) -> None:
    response = client.get("/api/v1/weather/sydney/forecast?days=3")

    assert response.status_code == 200
    data = response.json()
    assert data["city"] == "Sydney"
    assert len(data["days"]) == 3


def test_forecast_invalid_days(client: TestClient) -> None:
    response = client.get("/api/v1/weather/sydney/forecast?days=10")

    assert response.status_code == 400


def test_conditions_endpoint(client: TestClient) -> None:
    response = client.get("/api/v1/conditions")

    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 5
