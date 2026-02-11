"""
Comando Django para atualizar notícias agrícolas
Uso: python manage.py update_news
"""

from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import timezone
from datetime import datetime, timedelta
import requests
import feedparser
from dateutil import parser
from apps.news.models import NewsArticle, NewsCategory, NewsSource


class Command(BaseCommand):
    help = "Atualiza notícias agrícolas de diversas fontes"

    def handle(self, *args, **options):
        self.stdout.write("Iniciando atualização de notícias...")

        # Garantir que categorias existam
        self.ensure_categories_exist()

        # Atualizar do NewsAPI
        if settings.NEWS_API_KEY:
            self.update_from_newsapi()

        # Atualizar de RSS feeds
        self.update_from_rss()

        self.stdout.write(self.style.SUCCESS("Atualização de notícias concluída!"))

    def ensure_categories_exist(self):
        categories = [
            {"name": "Agricultura Geral", "slug": "agricultura-geral"},
            {"name": "Grãos", "slug": "graos"},
            {"name": "Pecuária", "slug": "pecuaria"},
            {"name": "Clima e Tempo", "slug": "clima-tempo"},
            {"name": "Mercado", "slug": "mercado"},
            {"name": "Tecnologia Agrícola", "slug": "tecnologia"},
            {"name": "Sustentabilidade", "slug": "sustentabilidade"},
        ]

        for cat_data in categories:
            NewsCategory.objects.get_or_create(
                slug=cat_data["slug"],
                defaults={"name": cat_data["name"], "is_active": True},
            )

        self.stdout.write(self.style.SUCCESS("✓ Categorias verificadas"))

    def update_from_newsapi(self):
        api_key = settings.NEWS_API_KEY

        # Registrar fonte
        source, _ = NewsSource.objects.get_or_create(
            name="NewsAPI",
            defaults={
                "source_type": "api",
                "url": "https://newsapi.org/v2/everything",
                "is_active": True,
                "fetch_interval": 360,  # 6 horas
            },
        )

        # Buscar notícias sobre agricultura
        keywords = ["agricultura", "agronegócio", "safra", "grãos"]

        for keyword in keywords:
            url = "https://newsapi.org/v2/everything"
            params = {
                "q": keyword,
                "language": "pt",
                "sortBy": "publishedAt",
                "apiKey": api_key,
                "pageSize": 10,
            }

            try:
                response = requests.get(url, params=params, timeout=10)
                response.raise_for_status()
                data = response.json()

                if data["status"] == "ok":
                    for article in data["articles"]:
                        self.save_article(article, "NewsAPI", keyword)

            except requests.exceptions.RequestException as e:
                self.stdout.write(self.style.ERROR(f"Erro ao buscar de NewsAPI: {e}"))

        source.last_fetch = timezone.now()
        source.save()
        self.stdout.write(self.style.SUCCESS("✓ NewsAPI atualizado"))

    def update_from_rss(self):
        rss_feeds = [
            {
                "name": "Canal Rural",
                "url": "https://www.canalrural.com.br/feed/",
                "category_slug": "agricultura-geral",
            },
            # Adicione mais feeds RSS aqui
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

                for entry in feed.entries[:10]:  # Limitar a 10 mais recentes
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
                        article_data, feed_data["name"], feed_data["category_slug"]
                    )

                source.last_fetch = timezone.now()
                source.save()
                self.stdout.write(
                    self.style.SUCCESS(f'✓ RSS {feed_data["name"]} atualizado')
                )

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Erro ao processar RSS {feed_data["name"]}: {e}')
                )

    def save_article(self, article_data, source_name, category_slug=None):
        try:
            # Verificar se já existe
            if NewsArticle.objects.filter(url=article_data["url"]).exists():
                return

            # Extrair campos
            title = article_data.get("title", "")
            if not title or len(title) > 300:
                return

            summary = article_data.get("summary", article_data.get("description", ""))
            if len(summary) > 1000:
                summary = summary[:997] + "..."

            # Criar artigo
            article = NewsArticle.objects.create(
                title=title,
                summary=summary,
                url=article_data["url"],
                source=source_name,
                author=article_data.get("author", ""),
                image_url=article_data.get(
                    "image_url", article_data.get("urlToImage", "")
                ),
                published_at=article_data.get(
                    "published_at", article_data.get("publishedAt", timezone.now())
                ),
            )

            # Adicionar categoria se fornecida
            if category_slug:
                try:
                    category = NewsCategory.objects.get(slug=category_slug)
                    article.categories.add(category)
                except NewsCategory.DoesNotExist:
                    pass

            self.stdout.write(f"  + {title[:50]}...")

        except Exception as e:
            self.stdout.write(self.style.WARNING(f"  ⚠ Erro ao salvar artigo: {e}"))

    def extract_image(self, entry):
        """Extrai URL da imagem do entry RSS"""
        # Tentar diferentes campos comuns
        if hasattr(entry, "media_content"):
            return entry.media_content[0]["url"]
        elif hasattr(entry, "media_thumbnail"):
            return entry.media_thumbnail[0]["url"]
        elif hasattr(entry, "enclosures") and entry.enclosures:
            return entry.enclosures[0].get("href", "")
        return ""

    def parse_date(self, date_str):
        if not date_str:
            return timezone.now()

        try:

            return parser.parse(date_str)
        except:
            return timezone.now()
