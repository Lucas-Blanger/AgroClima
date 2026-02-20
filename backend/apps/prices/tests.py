from datetime import timedelta

from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from apps.prices.models import Alert, Price, PriceSource, Product


class PricesApiTests(APITestCase):
    def setUp(self):
        self.source = PriceSource.objects.create(
            name="Main Source",
            source_type="manual",
            url="https://example.com/source",
        )

    def _create_product(self, name, category="graos", is_active=True):
        return Product.objects.create(
            name=name,
            category=category,
            unit="kg",
            is_active=is_active,
        )

    def _create_price(self, product, price, days_ago=0, source=None, date=None):
        return Price.objects.create(
            product=product,
            source=source or self.source,
            date=date or (timezone.now().date() - timedelta(days=days_ago)),
            price=price,
        )

    def test_products_filter_by_category_and_active(self):
        matching = self._create_product("Corn", category="graos", is_active=True)
        self._create_product("Tomato", category="hortalicas", is_active=True)
        self._create_product("Soy", category="graos", is_active=False)

        response = self.client.get("/api/prices/products/?category=graos&is_active=true")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["id"], matching.id)

    def test_product_categories_returns_distinct_values(self):
        self._create_product("Corn", category="graos")
        self._create_product("Beans", category="graos")
        self._create_product("Apple", category="frutas")

        response = self.client.get("/api/prices/products/categories/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(set(response.data), {"graos", "frutas"})

    def test_price_by_date_requires_date_parameter(self):
        response = self.client.get("/api/prices/prices/by_date/")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_price_by_date_returns_only_requested_day(self):
        product = self._create_product("Corn")
        selected_date = timezone.now().date() - timedelta(days=1)

        self._create_price(product, price="100.00", date=selected_date)
        self._create_price(product, price="110.00", date=timezone.now().date())

        response = self.client.get(f"/api/prices/prices/by_date/?date={selected_date}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["date"], str(selected_date))

    def test_latest_returns_only_active_products_with_latest_price(self):
        active_product = self._create_product("Corn", is_active=True)
        inactive_product = self._create_product("Soy", is_active=False)

        self._create_price(active_product, price="80.00", days_ago=2)
        self._create_price(active_product, price="90.00", days_ago=0)
        self._create_price(inactive_product, price="70.00", days_ago=0)

        response = self.client.get("/api/prices/prices/latest/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["product_id"], active_product.id)
        self.assertEqual(response.data[0]["price"], "90.00")

    def test_product_statistics_returns_aggregates(self):
        product = self._create_product("Corn")

        self._create_price(product, price="10.00", days_ago=2)
        self._create_price(product, price="20.00", days_ago=1)

        response = self.client.get(f"/api/prices/products/{product.id}/statistics/?days=30")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["product"], "Corn")
        self.assertEqual(response.data["period_days"], 30)
        self.assertEqual(response.data["statistics"]["total_records"], 2)
        self.assertAlmostEqual(float(response.data["statistics"]["avg_price"]), 15.0)
        self.assertAlmostEqual(float(response.data["statistics"]["min_price"]), 10.0)
        self.assertAlmostEqual(float(response.data["statistics"]["max_price"]), 20.0)

    def test_check_alerts_returns_triggered_and_updates_last_triggered(self):
        product = self._create_product("Corn")
        self._create_price(product, price="150.00")

        alert = Alert.objects.create(
            product=product,
            alert_type="above",
            threshold_value="100.00",
            is_active=True,
        )

        response = self.client.post("/api/prices/alerts/check_alerts/", data={})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total_checked"], 1)
        self.assertEqual(response.data["triggered"], 1)
        self.assertEqual(len(response.data["alerts"]), 1)

        alert.refresh_from_db()
        self.assertIsNotNone(alert.last_triggered)
