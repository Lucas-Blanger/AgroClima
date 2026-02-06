from rest_framework import serializers
from apps.weather.models import WeatherCurrent, WeatherForecast, WeatherAlert


class WeatherCurrentSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherCurrent
        fields = "__all__"


class WeatherForecastSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherForecast
        fields = "__all__"


class WeatherAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherAlert
        fields = "__all__"
