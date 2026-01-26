"""Weather service with mock data for demo purposes."""

import random
from dataclasses import dataclass
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from src.models import CityWeather, DayForecast, WeatherCondition, WeatherForecast

NZ_TZ = ZoneInfo("Pacific/Auckland")


def _get_seeded_random(city: str, date_str: str | None = None) -> random.Random:
    """Get a seeded Random instance for consistent weather within each hour."""
    now = datetime.now(tz=NZ_TZ)
    hour_key = now.strftime("%Y-%m-%d-%H")
    if date_str:
        hour_key = date_str
    seed = hash(f"{city.lower()}-{hour_key}")
    return random.Random(seed)  # noqa: S311

CONDITIONS: dict[str, WeatherCondition] = {
    "sunny": WeatherCondition(code="sunny", name="Sunny", icon="☀️"),
    "partly_cloudy": WeatherCondition(code="partly_cloudy", name="Partly Cloudy", icon="⛅"),
    "cloudy": WeatherCondition(code="cloudy", name="Cloudy", icon="☁️"),
    "rainy": WeatherCondition(code="rainy", name="Rainy", icon="🌧️"),
    "stormy": WeatherCondition(code="stormy", name="Stormy", icon="⛈️"),
    "windy": WeatherCondition(code="windy", name="Windy", icon="💨"),
    "foggy": WeatherCondition(code="foggy", name="Foggy", icon="🌫️"),
    "snowy": WeatherCondition(code="snowy", name="Snowy", icon="❄️"),
}


@dataclass
class CityData:
    """City weather configuration."""

    country: str
    temp_min: float
    temp_max: float
    typical_conditions: list[str]


CITIES: dict[str, CityData] = {
    "auckland": CityData("NZ", 12.0, 24.0, ["sunny", "partly_cloudy", "cloudy", "rainy"]),
    "wellington": CityData("NZ", 10.0, 20.0, ["windy", "cloudy", "partly_cloudy", "rainy"]),
    "christchurch": CityData("NZ", 8.0, 22.0, ["sunny", "partly_cloudy", "cloudy", "foggy"]),
    "sydney": CityData("AU", 15.0, 28.0, ["sunny", "partly_cloudy", "cloudy"]),
    "melbourne": CityData("AU", 12.0, 25.0, ["sunny", "partly_cloudy", "cloudy", "rainy", "windy"]),
    "brisbane": CityData("AU", 18.0, 32.0, ["sunny", "partly_cloudy", "stormy"]),
    "london": CityData("GB", 5.0, 18.0, ["cloudy", "rainy", "foggy", "partly_cloudy"]),
    "new york": CityData("US", 2.0, 28.0, ["sunny", "partly_cloudy", "cloudy", "rainy", "snowy"]),
}


class WeatherService:
    """Service for retrieving weather data."""

    def _celsius_to_fahrenheit(self, celsius: float) -> float:
        return round(celsius * 9 / 5 + 32, 1)

    def _generate_temperature(self, city_data: CityData, rng: random.Random) -> float:
        return round(rng.uniform(city_data.temp_min, city_data.temp_max), 1)

    def _get_random_condition(self, city_data: CityData, rng: random.Random) -> WeatherCondition:
        condition_code = rng.choice(city_data.typical_conditions)
        return CONDITIONS[condition_code]

    async def get_current_weather(self, city: str) -> CityWeather | None:
        """Get current weather for a city."""
        city_data = CITIES.get(city.lower())
        if city_data is None:
            return None

        rng = _get_seeded_random(city)
        temp_c = self._generate_temperature(city_data, rng)
        condition = self._get_random_condition(city_data, rng)
        humidity = rng.randint(40, 85)
        wind_speed = round(rng.uniform(5, 35), 1)
        feels_like = temp_c - (wind_speed / 10) + (humidity / 50)

        return CityWeather(
            city=city.title(),
            country=city_data.country,
            temperature_celsius=temp_c,
            temperature_fahrenheit=self._celsius_to_fahrenheit(temp_c),
            humidity_percent=humidity,
            wind_speed_kmh=wind_speed,
            condition=condition,
            feels_like_celsius=round(feels_like, 1),
        )

    async def get_forecast(self, city: str, days: int = 3) -> WeatherForecast | None:
        """Get weather forecast for a city."""
        city_data = CITIES.get(city.lower())
        if city_data is None:
            return None

        today = datetime.now(tz=NZ_TZ)
        forecasts: list[DayForecast] = []

        for i in range(days):
            forecast_date = today + timedelta(days=i + 1)
            date_str = forecast_date.strftime("%Y-%m-%d")
            rng = _get_seeded_random(city, date_str)
            daily_high = round(rng.uniform(city_data.temp_max - 3, city_data.temp_max + 3), 1)
            daily_low = round(rng.uniform(city_data.temp_min - 2, city_data.temp_min + 2), 1)
            condition = self._get_random_condition(city_data, rng)
            rain_chance = 10 if condition.code == "sunny" else rng.randint(20, 80)

            forecasts.append(
                DayForecast(
                    day=forecast_date.strftime("%A"),
                    date=forecast_date.strftime("%Y-%m-%d"),
                    high_celsius=daily_high,
                    low_celsius=daily_low,
                    condition=condition,
                    chance_of_rain_percent=rain_chance,
                )
            )

        return WeatherForecast(city=city.title(), country=city_data.country, days=forecasts)

    def get_all_conditions(self) -> list[WeatherCondition]:
        """Get all possible weather conditions."""
        return list(CONDITIONS.values())
