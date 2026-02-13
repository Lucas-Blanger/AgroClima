from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Avg, Min, Max, Count
from django.utils import timezone
from datetime import timedelta
from apps.prices.models import Product, PriceSource, Price, Alert
from .serializers import (
    ProductSerializer,
    PriceSourceSerializer,
    PriceSerializer,
    PriceCreateSerializer,
    AlertSerializer,
)


class ProductViewSet(viewsets.ModelViewSet):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all()

        # Filtro por categoria
        category = self.request.query_params.get("category")
        if category:
            queryset = queryset.filter(category=category)

        # Filtro por ativo/inativo
        is_active = self.request.query_params.get("is_active")
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == "true")

        # Busca por nome
        search = self.request.query_params.get("search")
        if search:
            queryset = queryset.filter(name__icontains=search)

        return queryset

    @action(detail=False, methods=["get"])
    def categories(self, request):
        categories = Product.objects.values_list("category", flat=True).distinct()
        return Response(list(categories))

    @action(detail=True, methods=["get"])
    def price_history(self, request, pk=None):
        product = self.get_object()
        days = int(request.query_params.get("days", 30))

        start_date = timezone.now().date() - timedelta(days=days)
        prices = (
            Price.objects.filter(product=product, date__gte=start_date)
            .select_related("source")
            .order_by("date")
        )

        serializer = PriceSerializer(prices, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def statistics(self, request, pk=None):
        product = self.get_object()
        days = int(request.query_params.get("days", 30))

        start_date = timezone.now().date() - timedelta(days=days)
        prices = Price.objects.filter(product=product, date__gte=start_date)

        stats = prices.aggregate(
            avg_price=Avg("price"),
            min_price=Min("price"),
            max_price=Max("price"),
            total_records=Count("id"),
        )

        return Response(
            {"product": product.name, "period_days": days, "statistics": stats}
        )


class PriceSourceViewSet(viewsets.ModelViewSet):

    queryset = PriceSource.objects.all()
    serializer_class = PriceSourceSerializer

    def get_queryset(self):
        queryset = PriceSource.objects.all()

        # Filtro por tipo
        source_type = self.request.query_params.get("type")
        if source_type:
            queryset = queryset.filter(source_type=source_type)

        # Filtro por ativo
        is_active = self.request.query_params.get("is_active")
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == "true")

        return queryset


class PriceViewSet(viewsets.ModelViewSet):
    """CRUD de preços - retorna apenas preços de uma data específica"""

    queryset = Price.objects.all()

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return PriceCreateSerializer
        return PriceSerializer

    def get_queryset(self):
        queryset = Price.objects.select_related("product", "source")

        # Filtro por produto
        product_id = self.request.query_params.get("product")
        if product_id:
            queryset = queryset.filter(product_id=product_id)

        # Filtro por categoria de produto
        category = self.request.query_params.get("category")
        if category:
            queryset = queryset.filter(product__category=category)

        # Filtro por fonte
        source_id = self.request.query_params.get("source")
        if source_id:
            queryset = queryset.filter(source_id=source_id)

        # Filtro por período
        days = self.request.query_params.get("days")
        if days:
            start_date = timezone.now().date() - timedelta(days=int(days))
            queryset = queryset.filter(date__gte=start_date)

        # Filtro por data específica
        date = self.request.query_params.get("date")
        if date:
            queryset = queryset.filter(date=date)

        return queryset

    @action(detail=False, methods=["get"])
    def latest(self, request):
        products = Product.objects.filter(is_active=True)
        latest_prices = []

        for product in products:
            latest = product.prices.select_related("source").order_by("-date").first()
            if latest:
                latest_prices.append(
                    {
                        "product_id": product.id,
                        "product_name": product.name,
                        "category": product.category,
                        "unit": product.unit,
                        "price": str(latest.price),
                        "date": latest.date,
                        "source": latest.source.name if latest.source else None,
                        "variation": latest.get_variation(),
                    }
                )

        return Response(latest_prices)

    @action(detail=False, methods=["get"])
    def by_date(self, request):
        date = request.query_params.get("date")
        if not date:
            return Response(
                {"error": "Parâmetro date é obrigatório"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        prices = Price.objects.filter(date=date).select_related("product", "source")
        serializer = self.get_serializer(prices, many=True)
        return Response(serializer.data)


class AlertViewSet(viewsets.ModelViewSet):

    queryset = Alert.objects.all()
    serializer_class = AlertSerializer

    def get_queryset(self):
        queryset = Alert.objects.select_related("product")

        # Filtro por produto
        product_id = self.request.query_params.get("product")
        if product_id:
            queryset = queryset.filter(product_id=product_id)

        # Filtro por ativo
        is_active = self.request.query_params.get("is_active")
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == "true")

        return queryset

    @action(detail=False, methods=["post"])
    def check_alerts(self, request):
        alerts = Alert.objects.filter(is_active=True).select_related("product")
        triggered_alerts = []

        for alert in alerts:
            latest_price = alert.product.get_latest_price()
            if latest_price and alert.check_trigger(float(latest_price.price)):
                triggered_alerts.append(
                    {
                        "alert_id": alert.id,
                        "product": alert.product.name,
                        "alert_type": alert.get_alert_type_display(),
                        "threshold": str(alert.threshold_value),
                        "current_price": str(latest_price.price),
                    }
                )

                # Atualizar último disparo
                alert.last_triggered = timezone.now()
                alert.save(update_fields=["last_triggered"])

        return Response(
            {
                "total_checked": alerts.count(),
                "triggered": len(triggered_alerts),
                "alerts": triggered_alerts,
            }
        )
