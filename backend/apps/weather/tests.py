from datetime import timedelta

from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from apps.weather.models import WeatherAlert, WeatherCurrent, WeatherForecast


class WeatherApiTests(APITestCase):
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

    def test_current_returns_404_when_empty(self):
        response = self.client.get("/api/v1/weather/current/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("detail", response.data)

    def test_current_returns_latest_record(self):
        older = self._create_current(description="older")
        WeatherCurrent.objects.filter(pk=older.pk).update(
            updated_at=timezone.now() - timedelta(hours=2)
        )

        latest = self._create_current(description="latest", icon="02d")

        response = self.client.get("/api/v1/weather/current/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], latest.id)
        self.assertEqual(response.data["description"], "latest")

    def test_forecast_returns_next_7_days_only(self):
        today = timezone.now().date()

        for offset in range(-2, 9):
            self._create_forecast(today + timedelta(days=offset))

        response = self.client.get("/api/v1/weather/forecast/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 7)

        expected_dates = [str(today + timedelta(days=offset)) for offset in range(0, 7)]
        returned_dates = [item["date"] for item in response.data]
        self.assertEqual(returned_dates, expected_dates)

    def test_alerts_returns_only_active_non_expired(self):
        now = timezone.now()

        active_alert = WeatherAlert.objects.create(
            event="Strong rain",
            severity="high",
            description="Heavy rain expected",
            start_time=now - timedelta(hours=1),
            end_time=now + timedelta(hours=4),
            is_active=True,
        )

        WeatherAlert.objects.create(
            event="Old warning",
            severity="medium",
            description="Already inactive",
            start_time=now - timedelta(hours=3),
            end_time=now + timedelta(hours=1),
            is_active=False,
        )

        WeatherAlert.objects.create(
            event="Expired warning",
            severity="low",
            description="Expired",
            start_time=now - timedelta(hours=6),
            end_time=now - timedelta(hours=1),
            is_active=True,
        )

        response = self.client.get("/api/v1/weather/alerts/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], active_alert.id)

    def test_history_respects_days_parameter(self):
        today = timezone.now().date()

        for offset in range(-10, 1):
            self._create_forecast(today + timedelta(days=offset))

        response = self.client.get("/api/v1/weather/history/?days=3")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
        self.assertEqual(response.data[0]["date"], str(today - timedelta(days=3)))
        self.assertEqual(response.data[-1]["date"], str(today))
