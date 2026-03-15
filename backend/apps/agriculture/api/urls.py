from django.urls import path
from apps.agriculture.api.views import (
    AgricultureInsightsViewSet,
    AgricultureRecommendationsViewSet,
)

app_name = "agriculture"

urlpatterns = [
    path("insights/", AgricultureInsightsViewSet.as_view(), name="insights"),
    path("recommendations/", AgricultureRecommendationsViewSet.as_view()),
]
