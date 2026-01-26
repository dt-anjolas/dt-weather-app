"""Weather API endpoints.

Provides weather data for cities using mock data (for demo purposes).
In production, this would integrate with a real weather API.
"""

from fastapi import APIRouter, HTTPException

from src.models import CityWeather, WeatherCondition, WeatherForecast
from src.services.weather_service import WeatherService

router = APIRouter()
weather_service = WeatherService()


@router.get("/weather/{city}", response_model=CityWeather)
async def get_weather(city: str) -> CityWeather:
    """Get current weather for a city.

    Args:
        city: City name (e.g., 'Auckland', 'Sydney', 'London')

    Returns:
        Current weather data for the city

    Raises:
        HTTPException: If city is not found
    """
    weather = await weather_service.get_current_weather(city)
    if weather is None:
        raise HTTPException(
            status_code=404,
            detail=f"Weather data not found for city: {city}",
        )
    return weather


@router.get("/weather/{city}/forecast", response_model=WeatherForecast)
async def get_forecast(city: str, days: int = 3) -> WeatherForecast:
    """Get weather forecast for a city.

    Args:
        city: City name
        days: Number of days to forecast (1-7, default 3)

    Returns:
        Weather forecast data

    Raises:
        HTTPException: If city is not found or days out of range
    """
    if days < 1 or days > 7:
        raise HTTPException(
            status_code=400,
            detail="Days must be between 1 and 7",
        )

    forecast = await weather_service.get_forecast(city, days)
    if forecast is None:
        raise HTTPException(
            status_code=404,
            detail=f"Forecast data not found for city: {city}",
        )
    return forecast


@router.get("/conditions", response_model=list[WeatherCondition])
async def list_conditions() -> list[WeatherCondition]:
    """List all possible weather conditions."""
    return weather_service.get_all_conditions()
