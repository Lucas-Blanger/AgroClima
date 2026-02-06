from django.urls import path
from apps.weather.api.views import WeatherViewSet

app_name = "weather"

urlpatterns = [
    path("current/", WeatherViewSet.as_view({"get": "current"}), name="current"),
    path("forecast/", WeatherViewSet.as_view({"get": "forecast"}), name="forecast"),
    path("alerts/", WeatherViewSet.as_view({"get": "alerts"}), name="alerts"),
    path("history/", WeatherViewSet.as_view({"get": "history"}), name="history"),
]
