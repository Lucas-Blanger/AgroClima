from rest_framework import serializers
from apps.prices.models import Product, PriceSource, Price, Alert


class ProductSerializer(serializers.ModelSerializer):
    latest_price = serializers.SerializerMethodField()
    price_trend = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "category",
            "unit",
            "description",
            "is_active",
            "latest_price",
            "price_trend",
            "created_at",
        ]

    def get_latest_price(self, obj):
        latest = obj.get_latest_price()
        if latest:
            return {
                "price": str(latest.price),
                "date": latest.date,
                "source": latest.source.name if latest.source else None,
            }
        return None

    def get_price_trend(self, obj):
        history = obj.get_price_history(days=7)
        if history.count() >= 2:
            first_price = float(history.first().price)
            last_price = float(history.last().price)
            if first_price > 0:
                variation = ((last_price - first_price) / first_price) * 100
                return {
                    "variation": round(variation, 2),
                    "direction": (
                        "up" if variation > 0 else "down" if variation < 0 else "stable"
                    ),
                }
        return None


class PriceSourceSerializer(serializers.ModelSerializer):
    total_prices = serializers.SerializerMethodField()

    class Meta:
        model = PriceSource
        fields = [
            "id",
            "name",
            "source_type",
            "url",
            "description",
            "is_active",
            "last_update",
            "update_frequency",
            "total_prices",
        ]

    def get_total_prices(self, obj):
        return obj.prices.count()


class PriceSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    product_unit = serializers.CharField(source="product.unit", read_only=True)
    product_category = serializers.CharField(source="product.category", read_only=True)
    source_name = serializers.CharField(source="source.name", read_only=True)
    variation = serializers.SerializerMethodField()

    class Meta:
        model = Price
        fields = [
            "id",
            "product",
            "product_name",
            "product_unit",
            "product_category",
            "source",
            "source_name",
            "date",
            "price",
            "price_min",
            "price_max",
            "volume",
            "variation",
            "notes",
            "created_at",
        ]

    def get_variation(self, obj):
        return obj.get_variation()


class PriceCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Price
        fields = [
            "product",
            "source",
            "date",
            "price",
            "price_min",
            "price_max",
            "volume",
            "notes",
        ]

    def validate(self, data):
        if data.get("price_min") and data.get("price_max"):
            if data["price_min"] > data["price_max"]:
                raise serializers.ValidationError(
                    "Preço mínimo não pode ser maior que preço máximo"
                )

        if data.get("price_min") and data["price"] < data["price_min"]:
            raise serializers.ValidationError(
                "Preço não pode ser menor que o preço mínimo"
            )

        if data.get("price_max") and data["price"] > data["price_max"]:
            raise serializers.ValidationError(
                "Preço não pode ser maior que o preço máximo"
            )

        return data


class AlertSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)

    class Meta:
        model = Alert
        fields = [
            "id",
            "product",
            "product_name",
            "alert_type",
            "threshold_value",
            "is_active",
            "email_notification",
            "last_triggered",
            "created_at",
        ]


class PriceHistorySerializer(serializers.Serializer):
    date = serializers.DateField()
    avg_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    min_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    max_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    count = serializers.IntegerField()


class PriceComparisonSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    product_name = serializers.CharField()
    current_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    variation_7d = serializers.DecimalField(max_digits=10, decimal_places=2)
    variation_30d = serializers.DecimalField(max_digits=10, decimal_places=2)
