from datetime import timedelta

from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from apps.weather.models import WeatherCurrent, WeatherForecast


class AgricultureApiTests(APITestCase):
    def _create_current(self, **overrides):
        now = timezone.now()
        data = {
            "temperature": 25.0,
            "feels_like": 26.0,
            "temp_min": 20.0,
            "temp_max": 30.0,
            "humidity": 70,
            "pressure": 1012,
            "wind_speed": 3.0,
            "wind_deg": 120,
            "clouds": 35,
            "rain_1h": 0.0,
            "rain_3h": 0.0,
            "description": "clear sky",
            "icon": "01d",
            "sunrise": now - timedelta(hours=6),
            "sunset": now + timedelta(hours=6),
        }
        data.update(overrides)
        return WeatherCurrent.objects.create(**data)

    def _create_forecast(self, date, **overrides):
        data = {
            "date": date,
            "temp_min": 19.0,
            "temp_max": 29.0,
            "humidity": 65,
            "pressure": 1010,
            "wind_speed": 4.0,
            "clouds": 40,
            "rain": 0.0,
            "pop": 0.2,
            "description": "partly cloudy",
            "icon": "02d",
        }
        data.update(overrides)
        return WeatherForecast.objects.create(**data)

    def test_insights_without_current_returns_nulls(self):
        response = self.client.get("/api/v1/agriculture/insights/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["alerts"], [])
        self.assertIsNone(response.data["drought"])
        self.assertIsNone(response.data["recommendations"])
        self.assertIsNone(response.data["current_weather"])
        self.assertEqual(response.data["history_days"], 7)
        self.assertEqual(response.data["history_records"], 0)

    def test_insights_returns_alerts_drought_and_recommendations(self):
        self._create_current(
            temperature=25.0,
            rain_1h=55.0,
            wind_speed=70.0,
        )

        today = timezone.now().date()
        for offset in range(0, 7):
            self._create_forecast(today - timedelta(days=offset), rain=0.0)

        response = self.client.get("/api/v1/agriculture/insights/?days=7")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["history_days"], 7)
        self.assertEqual(response.data["history_records"], 7)
        self.assertIsNotNone(response.data["current_weather"])

        alert_types = {item["type"] for item in response.data["alerts"]}
        self.assertEqual(alert_types, {"heavy_rain", "strong_wind"})

        self.assertIsNotNone(response.data["drought"])
        self.assertEqual(response.data["drought"]["type"], "drought")

        self.assertIsNotNone(response.data["recommendations"])
        self.assertEqual(
            response.data["recommendations"]["recommended_crops"],
            ["Soja", "Milho", "Arroz"],
        )

    def test_recommendations_returns_crops_when_current_exists(self):
        self._create_current(
            temperature=26.0,
            rain_1h=12.0,
            wind_speed=5.0,
        )

        response = self.client.get("/api/v1/agriculture/recommendations/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("recommendations", response.data)
        self.assertEqual(
            response.data["recommendations"]["recommended_crops"],
            ["Soja", "Milho", "Arroz"],
        )
        self.assertNotIn("message", response.data["recommendations"])
