from .season import get_current_season


def recommend_crops(weather):

    temp = weather.get("temperature")
    rain = weather.get("rain")

    season = get_current_season()

    crops = []

    if 20 <= temp <= 30 and rain >= 5:
        crops.append("Soja")

    if 18 <= temp <= 28:
        crops.append("Milho")

    if season == "winter" and temp <= 20:
        crops.append("Trigo")

    if temp >= 25 and rain >= 10:
        crops.append("Arroz")

    return {"season": season, "recommended_crops": crops}
