"""
Comando Django para atualizar noticias agricolas.
Uso: python manage.py update_news
"""

import re
from html import unescape

import feedparser
import requests
from dateutil import parser
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.news.models import NewsArticle, NewsCategory, NewsSource


class Command(BaseCommand):
    help = "Atualiza noticias agricolas de diversas fontes"

    def handle(self, *args, **options):
        self.stdout.write("Iniciando atualizacao de noticias...")

        self.ensure_categories_exist()

        if settings.NEWS_API_KEY:
            self.update_from_newsapi()

        self.update_from_rss()

        self.stdout.write(self.style.SUCCESS("Atualizacao de noticias concluida!"))

    def ensure_categories_exist(self):
        categories = [
            {"name": "Agricultura Geral", "slug": "agricultura-geral"},
            {"name": "Graos", "slug": "graos"},
            {"name": "Pecuaria", "slug": "pecuaria"},
            {"name": "Clima e Tempo", "slug": "clima-tempo"},
            {"name": "Mercado", "slug": "mercado"},
            {"name": "Tecnologia Agricola", "slug": "tecnologia"},
            {"name": "Sustentabilidade", "slug": "sustentabilidade"},
        ]

        for category in categories:
            NewsCategory.objects.get_or_create(
                slug=category["slug"],
                defaults={"name": category["name"], "is_active": True},
            )

        self.stdout.write(self.style.SUCCESS("OK Categorias verificadas"))

    def update_from_newsapi(self):
        source, _ = NewsSource.objects.get_or_create(
            name="NewsAPI",
            defaults={
                "source_type": "api",
                "url": "https://newsapi.org/v2/everything",
                "is_active": True,
                "fetch_interval": 360,
            },
        )

        keywords = ["agricultura", "agronegocio", "safra", "graos"]

        for keyword in keywords:
            params = {
                "q": keyword,
                "language": "pt",
                "sortBy": "publishedAt",
                "apiKey": settings.NEWS_API_KEY,
                "pageSize": 10,
            }

            try:
                response = requests.get(
                    "https://newsapi.org/v2/everything", params=params, timeout=10
                )
                response.raise_for_status()
                payload = response.json()

                if payload.get("status") == "ok":
                    for article in payload.get("articles", []):
                        self.save_article(article, "NewsAPI", keyword)

            except requests.exceptions.RequestException as error:
                self.stdout.write(
                    self.style.ERROR(f"Erro ao buscar noticias do NewsAPI: {error}")
                )

        source.last_fetch = timezone.now()
        source.save(update_fields=["last_fetch"])
        self.stdout.write(self.style.SUCCESS("OK NewsAPI atualizado"))

    def update_from_rss(self):
        rss_feeds = [
            {
                "name": "Canal Rural",
                "url": "https://www.canalrural.com.br/feed/",
                "category_slug": "agricultura-geral",
            },
        ]

        for feed_data in rss_feeds:
            source, _ = NewsSource.objects.get_or_create(
                name=feed_data["name"],
                defaults={
                    "source_type": "rss",
                    "url": feed_data["url"],
                    "is_active": True,
                    "fetch_interval": 360,
                },
            )

            try:
                feed = feedparser.parse(feed_data["url"])

                for entry in feed.entries[:10]:
                    article_data = {
                        "title": entry.get("title", ""),
                        "summary": entry.get("summary", entry.get("description", "")),
                        "url": entry.get("link", ""),
                        "source": feed_data["name"],
                        "author": entry.get("author", ""),
                        "image_url": self.extract_image(entry),
                        "published_at": self.parse_date(entry.get("published")),
                    }

                    self.save_article(
                        article_data,
                        feed_data["name"],
                        feed_data["category_slug"],
                    )

                source.last_fetch = timezone.now()
                source.save(update_fields=["last_fetch"])
                self.stdout.write(
                    self.style.SUCCESS(f'OK RSS {feed_data["name"]} atualizado')
                )

            except Exception as error:
                self.stdout.write(
                    self.style.ERROR(
                        f'Erro ao processar RSS {feed_data["name"]}: {error}'
                    )
                )

    def save_article(self, article_data, source_name, category_slug=None):
        try:
            url = article_data.get("url", "")
            if not url:
                return

            if NewsArticle.objects.filter(url=url).exists():
                return

            title = self.clean_text(article_data.get("title", ""))
            if not title or len(title) > 300:
                return

            summary = self.clean_text(
                article_data.get("summary", article_data.get("description", ""))
            )
            if len(summary) > 1000:
                summary = summary[:997] + "..."

            published_value = article_data.get(
                "published_at", article_data.get("publishedAt")
            )

            article = NewsArticle.objects.create(
                title=title,
                summary=summary,
                url=url,
                source=source_name,
                author=self.clean_text(article_data.get("author", "")),
                image_url=article_data.get(
                    "image_url", article_data.get("urlToImage", "")
                ),
                published_at=self.parse_date(published_value),
            )

            if category_slug:
                try:
                    category = NewsCategory.objects.get(slug=category_slug)
                    article.categories.add(category)
                except NewsCategory.DoesNotExist:
                    pass

            self.stdout.write(f"  + {title[:50]}...")

        except Exception as error:
            self.stdout.write(self.style.WARNING(f"  ! Erro ao salvar artigo: {error}"))

    def clean_text(self, value):
        if not value:
            return ""

        text = unescape(str(value))
        text = re.sub(r"<[^>]+>", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def extract_image(self, entry):
        if hasattr(entry, "media_content") and entry.media_content:
            return entry.media_content[0].get("url", "")

        if hasattr(entry, "media_thumbnail") and entry.media_thumbnail:
            return entry.media_thumbnail[0].get("url", "")

        if hasattr(entry, "enclosures") and entry.enclosures:
            return entry.enclosures[0].get("href", "")

        return ""

    def parse_date(self, value):
        if not value:
            return timezone.now()

        if hasattr(value, "tzinfo"):
            return value

        try:
            return parser.parse(str(value))
        except Exception:
            return timezone.now()
