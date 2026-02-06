from django.db import models


class NewsCategory(models.Model):
    # Categorias de notícias

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Categoria de Notícia"
        verbose_name_plural = "Categorias de Notícias"

    def __str__(self):
        return self.name


class NewsArticle(models.Model):
    # Notícias sobre agricultura

    title = models.CharField(max_length=300)
    summary = models.TextField(help_text="Resumo ou descrição da notícia")
    url = models.URLField(unique=True, help_text="Link para a notícia original")
    source = models.CharField(max_length=100, help_text="Fonte da notícia")
    author = models.CharField(max_length=200, blank=True, help_text="Autor da notícia")
    image_url = models.URLField(blank=True, help_text="URL da imagem de capa")
    published_at = models.DateTimeField(help_text="Data de publicação original")
    categories = models.ManyToManyField(
        NewsCategory, related_name="articles", blank=True
    )
    is_featured = models.BooleanField(
        default=False, help_text="Destacar na página inicial"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-published_at"]
        verbose_name = "Notícia"
        verbose_name_plural = "Notícias"
        indexes = [
            models.Index(fields=["-published_at"]),
            models.Index(fields=["source", "-published_at"]),
        ]

    def __str__(self):
        return self.title


class NewsSource(models.Model):
    # Fontes de notícias (RSS feeds, APIs, etc)

    SOURCE_TYPES = [
        ("rss", "RSS Feed"),
        ("api", "API"),
        ("scraper", "Web Scraper"),
    ]

    name = models.CharField(max_length=100, unique=True)
    source_type = models.CharField(max_length=20, choices=SOURCE_TYPES)
    url = models.URLField(help_text="URL do feed ou API")
    is_active = models.BooleanField(default=True)
    last_fetch = models.DateTimeField(null=True, blank=True)
    fetch_interval = models.IntegerField(
        default=360, help_text="Intervalo de atualização em minutos"
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Fonte de Notícias"
        verbose_name_plural = "Fontes de Notícias"

    def __str__(self):
        return f"{self.name} ({self.get_source_type_display()})"
