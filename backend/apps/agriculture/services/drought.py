def detect_drought(last_days):

    days_without_rain = 0

    for day in last_days:
        if day["rain"] == 0:
            days_without_rain += 1

    if days_without_rain >= 7:
        return {"type": "drought", "message": "Possível seca prolongada"}

    return None
