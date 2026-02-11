from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.news.api.views import (
    NewsCategoryViewSet,
    NewsArticleViewSet,
    NewsSourceViewSet,
)

app_name = "news"

router = DefaultRouter()
router.register(r"categories", NewsCategoryViewSet, basename="category")
router.register(r"articles", NewsArticleViewSet, basename="article")
router.register(r"sources", NewsSourceViewSet, basename="source")

urlpatterns = [
    path("", NewsArticleViewSet.as_view({"get": "list"}), name="list"),
    path("", include(router.urls)),
]
