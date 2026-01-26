import pytest

from src.models import CityWeather, WeatherForecast
from src.services.weather_service import WeatherService


@pytest.fixture
def weather_service() -> WeatherService:
    return WeatherService()


@pytest.mark.asyncio
async def test_get_current_weather_valid_city(weather_service: WeatherService) -> None:
    result = await weather_service.get_current_weather("Auckland")

    assert result is not None
    assert isinstance(result, CityWeather)
    assert result.city == "Auckland"
    assert result.country == "NZ"
    assert -10 <= result.temperature_celsius <= 40
    assert 0 <= result.humidity_percent <= 100


@pytest.mark.asyncio
async def test_get_current_weather_case_insensitive(weather_service: WeatherService) -> None:
    result = await weather_service.get_current_weather("SYDNEY")

    assert result is not None
    assert result.city == "Sydney"
    assert result.country == "AU"


@pytest.mark.asyncio
async def test_get_current_weather_invalid_city(weather_service: WeatherService) -> None:
    result = await weather_service.get_current_weather("NonExistentCity")

    assert result is None


@pytest.mark.asyncio
async def test_get_forecast_valid_city(weather_service: WeatherService) -> None:
    result = await weather_service.get_forecast("Wellington", days=3)

    assert result is not None
    assert isinstance(result, WeatherForecast)
    assert result.city == "Wellington"
    assert len(result.days) == 3


@pytest.mark.asyncio
async def test_get_forecast_invalid_city(weather_service: WeatherService) -> None:
    result = await weather_service.get_forecast("FakeCity", days=3)

    assert result is None


def test_get_all_conditions(weather_service: WeatherService) -> None:
    conditions = weather_service.get_all_conditions()

    assert len(conditions) >= 5
    assert all(c.code for c in conditions)
    assert all(c.name for c in conditions)
    assert all(c.icon for c in conditions)


def test_celsius_to_fahrenheit(weather_service: WeatherService) -> None:
    assert weather_service._celsius_to_fahrenheit(0) == 32.0
    assert weather_service._celsius_to_fahrenheit(100) == 212.0
    assert weather_service._celsius_to_fahrenheit(20) == 68.0
