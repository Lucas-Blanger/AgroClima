from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, PriceSourceViewSet, PriceViewSet, AlertViewSet

app_name = "prices"

router = DefaultRouter()
router.register(r"products", ProductViewSet, basename="product")
router.register(r"sources", PriceSourceViewSet, basename="source")
router.register(r"prices", PriceViewSet, basename="price")
router.register(r"alerts", AlertViewSet, basename="alert")

urlpatterns = [
    path("", include(router.urls)),
]
