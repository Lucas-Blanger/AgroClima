from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


urlpatterns = [
    # path("admin/", admin.site.urls),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/weather/", include("apps.weather.api.urls")),
    path("api/news/", include("apps.news.api.urls")),
    path("api/prices/", include("apps.prices.api.urls")),
    path("api/health/", include("apps.health.urls")),
]
