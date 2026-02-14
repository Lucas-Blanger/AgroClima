from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from apps.weather.models import WeatherCurrent, WeatherForecast, WeatherAlert
from apps.weather.api.serializers import (
    WeatherCurrentSerializer,
    WeatherForecastSerializer,
    WeatherAlertSerializer,
)


class WeatherViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = WeatherForecast.objects.all()
    serializer_class = WeatherForecastSerializer

    # API endpoints para dados climáticos
    @action(detail=False, methods=["get"])
    def current(self, request):
        # Retorna dados climáticos atuais
        try:
            weather = WeatherCurrent.objects.latest("updated_at")
            serializer = WeatherCurrentSerializer(weather)
            return Response(serializer.data)
        except WeatherCurrent.DoesNotExist:
            return Response(
                {"detail": "Dados climáticos ainda não disponíveis"},
                status=status.HTTP_404_NOT_FOUND,
            )

    @action(detail=False, methods=["get"])
    def forecast(self, request):
        # Retorna previsão para os próximos 7 dias
        today = timezone.now().date()
        forecasts = WeatherForecast.objects.filter(date__gte=today).order_by("date")[:7]
        serializer = WeatherForecastSerializer(forecasts, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def alerts(self, request):
        # Retorna alertas climáticos ativos
        alerts = WeatherAlert.objects.filter(
            is_active=True, end_time__gte=timezone.now()
        )
        serializer = WeatherAlertSerializer(alerts, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def history(self, request):
        # Retorna histórico dos últimos 7 dias
        days = int(request.query_params.get("days", 7))
        start_date = timezone.now().date() - timedelta(days=days)

        forecasts = WeatherForecast.objects.filter(
            date__gte=start_date, date__lte=timezone.now().date()
        ).order_by("date")

        serializer = WeatherForecastSerializer(forecasts, many=True)
        return Response(serializer.data)
