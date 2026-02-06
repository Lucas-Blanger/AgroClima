from django.db import models


class Product(models.Model):
    # Produtos Agrícolas monitorados

    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(
        max_length=50, help_text="Categoria: grão, hortaliça, fruta, etc"
    )
    unit = models.CharField(max_length=20, default="kg", help_text="Unidade de medida")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["category", "name"]
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"

    def __str__(self):
        return f"{self.name} ({self.unit})"


class PriceHistory(models.Model):
    # Histórico de preços dos produtos

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="prices"
    )
    date = models.DateField(help_text="Data da cotação")
    price = models.DecimalField(
        max_digits=10, decimal_places=2, help_text="Preço em R$"
    )
    price_min = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Preço mínimo do dia",
    )
    price_max = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Preço máximo do dia",
    )
    source = models.CharField(max_length=100, help_text="Fonte da cotação")
    source_url = models.URLField(blank=True, help_text="Link para a fonte")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date", "product__name"]
        unique_together = ["product", "date", "source"]
        verbose_name = "Histórico de Preço"
        verbose_name_plural = "Histórico de Preços"
        indexes = [
            models.Index(fields=["product", "-date"]),
            models.Index(fields=["date"]),
        ]

    def __str__(self):
        return (
            f"{self.product.name} - R$ {self.price} ({self.date.strftime('%d/%m/%Y')})"
        )


class PriceSource(models.Model):
    # Fontes de dados de preços

    name = models.CharField(max_length=100, unique=True)
    url = models.URLField()
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    last_update = models.DateTimeField(null=True, blank=True)
    update_frequency = models.CharField(
        max_length=50,
        default="daily",
        help_text="Frequência de atualização: daily, weekly, etc",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Fonte de Preços"
        verbose_name_plural = "Fontes de Preços"

    def __str__(self):
        return self.name
