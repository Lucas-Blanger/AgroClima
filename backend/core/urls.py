from django.contrib import admin
from django.urls import path, include
from dotenv import load_dotenv


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/weather/", include("apps.weather.api.urls")),
    path("api/news/", include("apps.news.api.urls")),
]
