"""Pydantic models for the Weather API."""

from pydantic import BaseModel, Field


class WeatherCondition(BaseModel):
    """Weather condition type."""

    code: str = Field(..., description="Condition code (e.g., 'sunny', 'cloudy')")
    name: str = Field(..., description="Human-readable condition name")
    icon: str = Field(..., description="Emoji icon for the condition")


class CityWeather(BaseModel):
    """Current weather data for a city."""

    city: str = Field(..., description="City name")
    country: str = Field(..., description="Country code")
    temperature_celsius: float = Field(..., description="Temperature in Celsius")
    temperature_fahrenheit: float = Field(..., description="Temperature in Fahrenheit")
    humidity_percent: int = Field(..., ge=0, le=100, description="Humidity percentage")
    wind_speed_kmh: float = Field(..., ge=0, description="Wind speed in km/h")
    condition: WeatherCondition = Field(..., description="Current weather condition")
    feels_like_celsius: float = Field(..., description="Feels like temperature in Celsius")


class DayForecast(BaseModel):
    """Weather forecast for a single day."""

    day: str = Field(..., description="Day name (e.g., 'Monday')")
    date: str = Field(..., description="Date in YYYY-MM-DD format")
    high_celsius: float = Field(..., description="High temperature in Celsius")
    low_celsius: float = Field(..., description="Low temperature in Celsius")
    condition: WeatherCondition = Field(..., description="Expected weather condition")
    chance_of_rain_percent: int = Field(..., ge=0, le=100, description="Chance of rain")


class WeatherForecast(BaseModel):
    """Weather forecast for multiple days."""

    city: str = Field(..., description="City name")
    country: str = Field(..., description="Country code")
    days: list[DayForecast] = Field(..., description="Daily forecasts")
