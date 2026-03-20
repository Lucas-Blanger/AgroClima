from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


urlpatterns = [
    # path("admin/", admin.site.urls),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/v1/weather/", include("apps.weather.api.urls")),
    path("api/v1/news/", include("apps.news.api.urls")),
    path("api/v1/prices/", include("apps.prices.api.urls")),
    path("api/v1/agriculture/", include("apps.agriculture.api.urls")),
    path("api/v1/health/", include("apps.health.urls")),
]
