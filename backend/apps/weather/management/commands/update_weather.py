"""
Comando Django para atualizar dados climáticos
Uso: python manage.py update_weather
"""

from collections import defaultdict
from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import timezone
from datetime import datetime
import requests
from apps.weather.models import WeatherCurrent, WeatherForecast


class Command(BaseCommand):
    help = "Atualiza dados climáticos do OpenWeatherMap"

    def handle(self, *args, **options):
        self.stdout.write("Iniciando atualização de dados climáticos...")

        api_key = settings.OPENWEATHER_API_KEY
        if not api_key:
            self.stdout.write(
                self.style.ERROR("API key do OpenWeatherMap não configurada")
            )
            return

        lat = settings.CITY_LAT
        lon = settings.CITY_LON

        # Atualizar clima atual
        self.update_current_weather(api_key, lat, lon)

        # Atualizar previsão
        self.update_forecast(api_key, lat, lon)

        self.stdout.write(self.style.SUCCESS("Atualização concluída!"))

    def update_current_weather(self, api_key, lat, lon):
        # Atualiza dados climáticos atuais
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "lat": lat,
            "lon": lon,
            "appid": api_key,
            "units": "metric",
            "lang": "pt_br",
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            # Criar ou atualizar registro
            WeatherCurrent.objects.all().delete()  # Remove registros antigos
            WeatherCurrent.objects.create(
                temperature=data["main"]["temp"],
                feels_like=data["main"]["feels_like"],
                temp_min=data["main"]["temp_min"],
                temp_max=data["main"]["temp_max"],
                humidity=data["main"]["humidity"],
                pressure=data["main"]["pressure"],
                wind_speed=data["wind"]["speed"],
                wind_deg=data["wind"]["deg"],
                clouds=data["clouds"]["all"],
                rain_1h=data.get("rain", {}).get("1h"),
                rain_3h=data.get("rain", {}).get("3h"),
                description=data["weather"][0]["description"],
                icon=data["weather"][0]["icon"],
                sunrise=datetime.fromtimestamp(
                    data["sys"]["sunrise"], tz=timezone.get_current_timezone()
                ),
                sunset=datetime.fromtimestamp(
                    data["sys"]["sunset"], tz=timezone.get_current_timezone()
                ),
            )

            self.stdout.write(self.style.SUCCESS("✓ Clima atual atualizado"))

        except requests.exceptions.RequestException as e:
            self.stdout.write(self.style.ERROR(f"✗ Erro ao buscar clima atual: {e}"))

    def update_forecast(self, api_key, lat, lon):
        url = "https://api.openweathermap.org/data/2.5/forecast"
        params = {
            "lat": lat,
            "lon": lon,
            "appid": api_key,
            "units": "metric",
            "lang": "pt_br",
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            dias = defaultdict(list)

            # Agrupa por dia
            for item in data["list"]:
                date = datetime.fromtimestamp(
                    item["dt"], tz=timezone.get_current_timezone()
                ).date()
                dias[date].append(item)

            # Remove previsões antigas
            WeatherForecast.objects.all().delete()

            # Processa até 5 dias
            for date, items in list(dias.items())[:5]:

                def avg(lst):
                    return sum(lst) / len(lst) if lst else None

                WeatherForecast.objects.create(
                    date=date,
                    temp_min=min(i["main"]["temp"] for i in items),
                    temp_max=max(i["main"]["temp"] for i in items),
                    humidity=int(
                        sum(i["main"]["humidity"] for i in items) / len(items)
                    ),
                    pressure=int(
                        sum(i["main"]["pressure"] for i in items) / len(items)
                    ),
                    wind_speed=sum(i["wind"]["speed"] for i in items) / len(items),
                    clouds=int(sum(i["clouds"]["all"] for i in items) / len(items)),
                    rain=sum(i.get("rain", {}).get("3h", 0) for i in items),
                    pop=max(i.get("pop", 0) for i in items),
                    description=items[0]["weather"][0]["description"],
                    icon=items[0]["weather"][0]["icon"],
                )

            self.stdout.write(self.style.SUCCESS("✓ Previsão atualizada (5 dias)"))

        except requests.exceptions.RequestException as e:
            self.stdout.write(self.style.ERROR(f"✗ Erro ao buscar previsão: {e}"))
