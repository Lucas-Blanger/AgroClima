from datetime import timedelta

from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.weather.models import WeatherCurrent, WeatherForecast
from apps.agriculture.services.alerts import detect_weather_alerts
from apps.agriculture.services.drought import detect_drought
from apps.agriculture.services.recommendations import recommend_crops


class AgricultureInsightsViewSet(APIView):

    def get(self, request):
        days = int(request.query_params.get("days", 7))
        today = timezone.now().date()

        current = None
        try:
            current = WeatherCurrent.objects.latest("updated_at")
        except WeatherCurrent.DoesNotExist:
            current = None

        if current:
            precipitation = current.rain_1h
            if precipitation is None:
                precipitation = current.rain_3h

            weather_context = {
                "temperature": current.temperature,
                "precipitation": precipitation or 0,
                "wind_speed": current.wind_speed,
                "rain": precipitation or 0,
            }
            current_payload = {
                "temperature": current.temperature,
                "rain_1h": current.rain_1h,
                "rain_3h": current.rain_3h,
                "wind_speed": current.wind_speed,
                "updated_at": current.updated_at,
            }
        else:
            weather_context = {
                "temperature": None,
                "precipitation": None,
                "wind_speed": None,
                "rain": None,
            }
            current_payload = None

        alerts = detect_weather_alerts(weather_context)

        start_date = today - timedelta(days=days)
        history = WeatherForecast.objects.filter(
            date__gte=start_date, date__lte=today
        ).order_by("-date")[:days]

        last_days = [
            {"date": item.date, "rain": float(item.rain or 0)} for item in history
        ]
        drought = detect_drought(last_days) if last_days else None

        recommendations = None
        if weather_context.get("temperature") is not None:
            recommendations = recommend_crops(weather_context)

        return Response(
            {
                "alerts": alerts,
                "drought": drought,
                "recommendations": recommendations,
                "current_weather": current_payload,
                "history_days": days,
                "history_records": len(last_days),
            }
        )


class AgricultureRecommendationsViewSet(APIView):
    def get(self, request):
        current = None
        try:
            current = WeatherCurrent.objects.latest("updated_at")
        except WeatherCurrent.DoesNotExist:
            current = None

        if current:
            weather_context = {
                "temperature": current.temperature,
                "precipitation": current.rain_1h or current.rain_3h or 0,
                "wind_speed": current.wind_speed,
                "rain": current.rain_1h or current.rain_3h or 0,
            }
        else:
            weather_context = {
                "temperature": None,
                "precipitation": None,
                "wind_speed": None,
                "rain": None,
            }

        recommendations = recommend_crops(weather_context)
        if not recommendations["recommended_crops"]:
            recommendations["message"] = (
                "Nenhuma cultura recomendada com base nas condições atuais."
            )

        return Response({"recommendations": recommendations})
