from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone


class Product(models.Model):
    # Produtos monitorados para cotação

    CATEGORY_CHOICES = [
        ("graos", "Grãos"),
        ("hortalicas", "Hortaliças"),
        ("frutas", "Frutas"),
        ("pecuaria", "Pecuária"),
        ("insumos", "Insumos Agrícolas"),
    ]

    name = models.CharField(max_length=100, unique=True, verbose_name="Nome")
    category = models.CharField(
        max_length=50, choices=CATEGORY_CHOICES, verbose_name="Categoria"
    )
    unit = models.CharField(max_length=20, default="kg", verbose_name="Unidade")
    description = models.TextField(blank=True, verbose_name="Descrição")
    is_active = models.BooleanField(default=True, verbose_name="Ativo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    class Meta:
        ordering = ["category", "name"]
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        indexes = [
            models.Index(fields=["category", "is_active"]),
            models.Index(fields=["name"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.unit})"

    def get_latest_price(self):
        return self.prices.order_by("-date").first()

    def get_price_history(self, days=30):
        start_date = timezone.now().date() - timezone.timedelta(days=days)
        return self.prices.filter(date__gte=start_date).order_by("date")


class PriceSource(models.Model):

    SOURCE_TYPE_CHOICES = [
        ("api", "API"),
        ("scraper", "Web Scraper"),
        ("manual", "Manual"),
        ("rss", "RSS Feed"),
    ]

    name = models.CharField(max_length=100, unique=True, verbose_name="Nome")
    source_type = models.CharField(
        max_length=20, choices=SOURCE_TYPE_CHOICES, verbose_name="Tipo"
    )
    url = models.URLField(blank=True, verbose_name="URL")
    description = models.TextField(blank=True, verbose_name="Descrição")
    is_active = models.BooleanField(default=True, verbose_name="Ativa")
    last_update = models.DateTimeField(
        null=True, blank=True, verbose_name="Última atualização"
    )
    update_frequency = models.CharField(
        max_length=50, default="daily", verbose_name="Frequência de atualização"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")

    class Meta:
        ordering = ["name"]
        verbose_name = "Fonte de Preços"
        verbose_name_plural = "Fontes de Preços"

    def __str__(self):
        return f"{self.name} ({self.get_source_type_display()})"


class Price(models.Model):

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="prices", verbose_name="Produto"
    )
    source = models.ForeignKey(
        PriceSource,
        on_delete=models.SET_NULL,
        null=True,
        related_name="prices",
        verbose_name="Fonte",
    )
    date = models.DateField(verbose_name="Data")
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Preço",
    )
    price_min = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        verbose_name="Preço mínimo",
    )
    price_max = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        verbose_name="Preço máximo",
    )
    volume = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        verbose_name="Volume negociado",
    )
    notes = models.TextField(blank=True, verbose_name="Observações")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")

    class Meta:
        ordering = ["-date", "product__name"]
        unique_together = ["product", "date", "source"]
        verbose_name = "Preço"
        verbose_name_plural = "Preços"
        indexes = [
            models.Index(fields=["product", "-date"]),
            models.Index(fields=["date"]),
            models.Index(fields=["product", "source", "-date"]),
        ]

    def __str__(self):
        return f"{self.product.name} - R$ {self.price} ({self.date})"

    def get_variation(self):
        previous = (
            Price.objects.filter(product=self.product, date__lt=self.date)
            .order_by("-date")
            .first()
        )

        if previous and previous.price > 0:
            variation = ((self.price - previous.price) / previous.price) * 100
            return round(variation, 2)
        return None


class Alert(models.Model):
    ALERT_TYPE_CHOICES = [
        ("above", "Acima de"),
        ("below", "Abaixo de"),
        ("variation", "Variação percentual"),
    ]

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="alerts", verbose_name="Produto"
    )
    alert_type = models.CharField(
        max_length=20, choices=ALERT_TYPE_CHOICES, verbose_name="Tipo"
    )
    threshold_value = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Valor de referência"
    )
    is_active = models.BooleanField(default=True, verbose_name="Ativo")
    email_notification = models.EmailField(
        blank=True, verbose_name="Email para notificação"
    )
    last_triggered = models.DateTimeField(
        null=True, blank=True, verbose_name="Último disparo"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Alerta de Preço"
        verbose_name_plural = "Alertas de Preço"

    def __str__(self):
        return f"{self.product.name} - {self.get_alert_type_display()} R$ {self.threshold_value}"

    def check_trigger(self, current_price):
        """Verifica se o alerta deve ser disparado"""
        if not self.is_active:
            return False

        if self.alert_type == "above" and current_price >= self.threshold_value:
            return True
        elif self.alert_type == "below" and current_price <= self.threshold_value:
            return True

        return False
