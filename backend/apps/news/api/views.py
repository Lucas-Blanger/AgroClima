from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from apps.news.models import NewsCategory, NewsArticle, NewsSource
from apps.news.api.serializers import (
    NewsCategorySerializer,
    NewsArticleSerializer,
    NewsArticleListSerializer,
    NewsSourceSerializer,
)


class NewsCategoryViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = NewsCategory.objects.filter(is_active=True)
    serializer_class = NewsCategorySerializer


class NewsArticleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = NewsArticle.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return NewsArticleListSerializer
        return NewsArticleSerializer

    def get_queryset(self):
        queryset = NewsArticle.objects.all()

        # Filtro por categoria
        category = self.request.query_params.get("category")
        if category:
            queryset = queryset.filter(categories__slug=category)

        # Filtro por fonte
        source = self.request.query_params.get("source")
        if source:
            queryset = queryset.filter(source__icontains=source)

        # Filtro por período
        days = self.request.query_params.get("days")
        if days:
            start_date = timezone.now() - timedelta(days=int(days))
            queryset = queryset.filter(published_at__gte=start_date)

        # Apenas notícias destacadas
        featured = self.request.query_params.get("featured")
        if featured and featured.lower() == "true":
            queryset = queryset.filter(is_featured=True)

        return queryset.prefetch_related("categories")

    @action(detail=False, methods=["get"])
    def latest(self, request):
        # Retorna as 10 notícias mais recentes
        limit = int(request.query_params.get("limit", 10))
        articles = self.get_queryset()[:limit]
        serializer = NewsArticleListSerializer(articles, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def featured(self, request):
        # Retorna notícias em destaque
        articles = NewsArticle.objects.filter(is_featured=True)[:5]
        serializer = NewsArticleListSerializer(articles, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def by_category(self, request):
        # Agrupa notícias por categoria
        categories = NewsCategory.objects.filter(is_active=True)
        result = []

        for category in categories:
            articles = NewsArticle.objects.filter(categories=category).order_by(
                "-published_at"
            )[:5]

            if articles.exists():
                result.append(
                    {
                        "category": category.name,
                        "slug": category.slug,
                        "articles": NewsArticleListSerializer(articles, many=True).data,
                    }
                )

        return Response(result)


class NewsSourceViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = NewsSource.objects.filter(is_active=True)
    serializer_class = NewsSourceSerializer
