import os
import sys
from django.apps import AppConfig
from django.conf import settings


class WeatherConfig(AppConfig):
    name = "apps.weather"

    def ready(self):
        if not getattr(settings, "AUTO_DAILY_UPDATE_ENABLED", True):
            return

        command = sys.argv[1] if len(sys.argv) > 1 else ""
        entrypoint = os.path.basename(sys.argv[0]).lower()

        web_entrypoints = ("gunicorn", "uvicorn", "daphne", "uwsgi")
        is_web_process = command == "runserver" or any(
            name in entrypoint for name in web_entrypoints
        )

        if not is_web_process:
            return

        if command == "runserver" and os.environ.get("RUN_MAIN") != "true":
            return

        from apps.weather.daily_scheduler import start_daily_scheduler

        start_daily_scheduler()
