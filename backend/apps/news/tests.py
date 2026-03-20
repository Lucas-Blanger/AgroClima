from datetime import timedelta

from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from apps.news.models import NewsArticle, NewsCategory


class NewsApiTests(APITestCase):
    def _create_article(self, title, published_at=None, is_featured=False):
        article_index = NewsArticle.objects.count() + 1
        return NewsArticle.objects.create(
            title=title,
            summary=f"Summary for {title}",
            url=f"https://example.com/news-{article_index}",
            source="Agro News",
            published_at=published_at or timezone.now(),
            is_featured=is_featured,
        )

    def test_list_returns_paginated_data(self):
        self._create_article("Market update")

        response = self.client.get("/api/v1/news/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("count", response.data)
        self.assertIn("results", response.data)
        self.assertEqual(response.data["count"], 1)

    def test_list_filters_by_category_slug(self):
        climate = NewsCategory.objects.create(name="Climate", slug="climate")
        prices = NewsCategory.objects.create(name="Prices", slug="prices")

        first = self._create_article("Climate report")
        second = self._create_article("Prices report")
        first.categories.add(climate)
        second.categories.add(prices)

        response = self.client.get("/api/v1/news/?category=climate")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["id"], first.id)

    def test_latest_respects_limit(self):
        now = timezone.now()

        self._create_article("Older", published_at=now - timedelta(days=2))
        middle = self._create_article("Middle", published_at=now - timedelta(days=1))
        latest = self._create_article("Latest", published_at=now)

        response = self.client.get("/api/v1/news/articles/latest/?limit=2")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["id"], latest.id)
        self.assertEqual(response.data[1]["id"], middle.id)

    def test_featured_returns_only_featured_and_max_5(self):
        now = timezone.now()

        for index in range(6):
            self._create_article(
                f"Featured {index}",
                published_at=now - timedelta(hours=index),
                is_featured=True,
            )

        self._create_article("Regular article", is_featured=False)

        response = self.client.get("/api/v1/news/articles/featured/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)
        self.assertTrue(all(item["is_featured"] for item in response.data))

    def test_by_category_groups_active_categories_with_articles_only(self):
        active_with_article = NewsCategory.objects.create(
            name="Weather", slug="weather"
        )
        NewsCategory.objects.create(name="Empty", slug="empty")
        inactive_with_article = NewsCategory.objects.create(
            name="Inactive",
            slug="inactive",
            is_active=False,
        )

        active_article = self._create_article("Weather alert")
        inactive_article = self._create_article("Inactive category article")
        active_article.categories.add(active_with_article)
        inactive_article.categories.add(inactive_with_article)

        response = self.client.get("/api/v1/news/articles/by_category/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["slug"], "weather")
        self.assertEqual(len(response.data[0]["articles"]), 1)
        self.assertEqual(response.data[0]["articles"][0]["id"], active_article.id)
