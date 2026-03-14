def detect_weather_alerts(weather):

    alerts = []
    temperature = weather.get("temperature")
    rain = weather.get("precipitation")
    wind_speed = weather.get("wind_speed")

    if temperature is not None and temperature <= 2:
        alerts.append({"type": "frost", "message": "Risco de geada"})

    if rain is not None and rain >= 50:
        alerts.append({"type": "heavy_rain", "message": "Chuva intensa prevista"})

    if wind_speed is not None and wind_speed >= 60:
        alerts.append({"type": "strong_wind", "message": "Ventos fortes"})

    return alerts
