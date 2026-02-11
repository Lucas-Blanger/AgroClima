from rest_framework import serializers
from apps.news.models import NewsCategory, NewsArticle, NewsSource


class NewsCategorySerializer(serializers.ModelSerializer):
    article_count = serializers.SerializerMethodField()

    class Meta:
        model = NewsCategory
        fields = ["id", "name", "slug", "description", "article_count"]

    def get_article_count(self, obj):
        return obj.articles.count()


class NewsArticleSerializer(serializers.ModelSerializer):
    categories = NewsCategorySerializer(many=True, read_only=True)
    category_names = serializers.SerializerMethodField()

    class Meta:
        model = NewsArticle
        fields = [
            "id",
            "title",
            "summary",
            "url",
            "source",
            "author",
            "image_url",
            "published_at",
            "categories",
            "category_names",
            "is_featured",
            "created_at",
        ]

    def get_category_names(self, obj):
        return [cat.name for cat in obj.categories.all()]


class NewsArticleListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listagem"""

    category_names = serializers.SerializerMethodField()

    class Meta:
        model = NewsArticle
        fields = [
            "id",
            "title",
            "summary",
            "url",
            "source",
            "image_url",
            "published_at",
            "category_names",
            "is_featured",
        ]

    def get_category_names(self, obj):
        return [cat.name for cat in obj.categories.all()]


class NewsSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsSource
        fields = "__all__"
