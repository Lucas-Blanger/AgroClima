from django.urls import path, include
from .views import HealthCheckView


urlpatterns = [
    path("", HealthCheckView.as_view(), name="health-check"),
]
