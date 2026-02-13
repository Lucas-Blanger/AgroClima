"""
Comando Django para atualizar cotacoes agricolas.
Uso:
    python manage.py update_prices
    python manage.py update_prices --source cepea
    python manage.py update_prices --date 2026-02-13 --replace
"""

from decimal import Decimal, InvalidOperation

from django.core.management.base import BaseCommand, CommandError
from django.db import OperationalError, ProgrammingError
from django.utils import timezone
from django.utils.dateparse import parse_date

from apps.prices.models import Price, PriceSource, Product


class Command(BaseCommand):
    help = "Atualiza cotacoes de produtos agricolas"

    SOURCE_CONFIG = {
        "cepea": {
            "name": "CEPEA/ESALQ",
            "source_type": "scraper",
            "url": "https://www.cepea.esalq.usp.br/br",
            "description": "Centro de Estudos Avancados em Economia Aplicada",
            "update_frequency": "daily",
        },
        "manual": {
            "name": "Dados Manuais",
            "source_type": "manual",
            "url": "",
            "description": "Dados de cotacao mantidos internamente",
            "update_frequency": "weekly",
        },
    }

    SAMPLE_QUOTES = {
        "cepea": [
            {
                "name": "Soja",
                "category": "graos",
                "unit": "saca 60kg",
                "price": "150.00",
            },
            {
                "name": "Milho",
                "category": "graos",
                "unit": "saca 60kg",
                "price": "82.50",
            },
            {
                "name": "Trigo",
                "category": "graos",
                "unit": "saca 60kg",
                "price": "95.00",
            },
            {
                "name": "Boi Gordo",
                "category": "pecuaria",
                "unit": "@",
                "price": "320.00",
            },
            {"name": "Leite", "category": "pecuaria", "unit": "litro", "price": "2.50"},
        ],
        "manual": [
            {
                "name": "Arroz",
                "category": "graos",
                "unit": "saca 60kg",
                "price": "124.30",
            },
            {
                "name": "Fertilizante NPK",
                "category": "insumos",
                "unit": "saca 50kg",
                "price": "210.00",
            },
            {
                "name": "Tomate",
                "category": "hortalicas",
                "unit": "caixa 20kg",
                "price": "88.40",
            },
        ],
    }

    def add_arguments(self, parser):
        parser.add_argument(
            "--source",
            type=str,
            choices=["all", *self.SOURCE_CONFIG.keys()],
            default="all",
            help="Fonte de cotacao para atualizar (default: all)",
        )
        parser.add_argument(
            "--date",
            type=str,
            help="Data da cotacao no formato YYYY-MM-DD (default: hoje)",
        )
        parser.add_argument(
            "--replace",
            action="store_true",
            help="Substitui cotacoes existentes para a mesma data",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Mostra o que seria alterado sem salvar no banco",
        )

    def handle(self, *args, **options):
        source_name = options["source"]
        target_date = self._resolve_date(options.get("date"))
        replace_existing = options["replace"]
        dry_run = options["dry_run"]

        selected_sources = (
            list(self.SOURCE_CONFIG.keys()) if source_name == "all" else [source_name]
        )

        mode = "simulacao" if dry_run else "execucao"
        self.stdout.write(
            f"Iniciando atualizacao de cotacoes ({mode}) para {target_date.isoformat()}..."
        )

        totals = {
            "products_created": 0,
            "products_updated": 0,
            "prices_created": 0,
            "prices_updated": 0,
            "prices_skipped": 0,
        }

        for source_key in selected_sources:
            try:
                source_stats = self._update_source(
                    source_key=source_key,
                    target_date=target_date,
                    replace_existing=replace_existing,
                    dry_run=dry_run,
                )
            except (OperationalError, ProgrammingError) as exc:
                raise CommandError(
                    "Falha ao acessar as tabelas de precos. "
                    "Verifique se o banco esta sincronizado com as migrations."
                ) from exc

            for key in totals:
                totals[key] += source_stats[key]

            self.stdout.write(
                self.style.SUCCESS(
                    "  -> {source}: produtos +{products_created}, metadados {products_updated}, "
                    "cotacoes +{prices_created}, atualizadas {prices_updated}, ignoradas {prices_skipped}".format(
                        source=self.SOURCE_CONFIG[source_key]["name"],
                        **source_stats,
                    )
                )
            )

        summary = (
            "Resumo final: produtos +{products_created}, metadados {products_updated}, "
            "cotacoes +{prices_created}, atualizadas {prices_updated}, ignoradas {prices_skipped}"
        ).format(**totals)

        if dry_run:
            self.stdout.write(self.style.WARNING(f"[DRY-RUN] {summary}"))
            return

        self.stdout.write(self.style.SUCCESS(summary))

    def _update_source(self, source_key, target_date, replace_existing, dry_run):
        source = self._get_or_create_source(source_key=source_key, dry_run=dry_run)
        quotes = self._load_quotes(source_key)

        stats = {
            "products_created": 0,
            "products_updated": 0,
            "prices_created": 0,
            "prices_updated": 0,
            "prices_skipped": 0,
        }

        for quote in quotes:
            product, product_created, product_updated = self._get_or_sync_product(
                quote=quote, dry_run=dry_run
            )

            stats["products_created"] += int(product_created)
            stats["products_updated"] += int(product_updated)

            existing_price = None
            if product.pk and source.pk:
                existing_price = Price.objects.filter(
                    product=product,
                    source=source,
                    date=target_date,
                ).first()

            price_data = self._build_price_data(quote, target_date)

            if existing_price:
                if not replace_existing:
                    stats["prices_skipped"] += 1
                    continue

                if not dry_run:
                    for field, value in price_data.items():
                        setattr(existing_price, field, value)
                    existing_price.save(
                        update_fields=[
                            "price",
                            "price_min",
                            "price_max",
                            "volume",
                            "notes",
                        ]
                    )
                stats["prices_updated"] += 1
                continue

            if not dry_run:
                Price.objects.create(product=product, source=source, **price_data)
            stats["prices_created"] += 1

        if not dry_run and source.pk:
            source.last_update = timezone.now()
            source.save(update_fields=["last_update"])

        return stats

    def _resolve_date(self, raw_value):
        if not raw_value:
            return timezone.localdate()

        parsed = parse_date(raw_value)
        if parsed:
            return parsed

        raise CommandError("Data invalida. Use o formato YYYY-MM-DD.")

    def _load_quotes(self, source_key):
        quotes = self.SAMPLE_QUOTES.get(source_key, [])
        if not quotes:
            self.stdout.write(
                self.style.WARNING(
                    f"Nenhuma cotacao configurada para a fonte '{source_key}'."
                )
            )
        return quotes

    def _get_or_create_source(self, source_key, dry_run):
        config = self.SOURCE_CONFIG[source_key]
        source = PriceSource.objects.filter(name=config["name"]).first()
        if source:
            defaults = self._source_defaults(config)
            fields_to_update = []

            for field, value in defaults.items():
                if getattr(source, field) != value:
                    setattr(source, field, value)
                    fields_to_update.append(field)

            if fields_to_update and not dry_run:
                source.save(update_fields=fields_to_update)
            return source

        if dry_run:
            return PriceSource(name=config["name"], **self._source_defaults(config))

        source, _ = PriceSource.objects.get_or_create(
            name=config["name"],
            defaults=self._source_defaults(config),
        )
        return source

    def _source_defaults(self, config):
        return {
            "source_type": config["source_type"],
            "url": config["url"],
            "description": config["description"],
            "is_active": True,
            "update_frequency": config["update_frequency"],
        }

    def _get_or_sync_product(self, quote, dry_run):
        defaults = {
            "category": quote["category"],
            "unit": quote["unit"],
            "is_active": True,
        }

        product = Product.objects.filter(name=quote["name"]).first()
        if not product:
            if dry_run:
                return Product(name=quote["name"], **defaults), True, False

            product = Product.objects.create(name=quote["name"], **defaults)
            return product, True, False

        fields_to_update = []
        if product.category != quote["category"]:
            product.category = quote["category"]
            fields_to_update.append("category")
        if product.unit != quote["unit"]:
            product.unit = quote["unit"]
            fields_to_update.append("unit")
        if not product.is_active:
            product.is_active = True
            fields_to_update.append("is_active")

        if fields_to_update and not dry_run:
            product.save(update_fields=fields_to_update)

        return product, False, bool(fields_to_update)

    def _build_price_data(self, quote, target_date):
        product_name = quote["name"]
        price = self._to_decimal(
            quote["price"], field_name="price", product_name=product_name
        )
        price_min = self._to_decimal(
            quote.get("price_min"),
            field_name="price_min",
            product_name=product_name,
            required=False,
        )
        price_max = self._to_decimal(
            quote.get("price_max"),
            field_name="price_max",
            product_name=product_name,
            required=False,
        )
        volume = self._to_decimal(
            quote.get("volume"),
            field_name="volume",
            product_name=product_name,
            required=False,
        )

        if price_min is not None and price_max is not None and price_min > price_max:
            raise CommandError(
                f"Cotacao invalida para '{product_name}': price_min maior que price_max."
            )
        if price_min is not None and price < price_min:
            raise CommandError(
                f"Cotacao invalida para '{product_name}': price menor que price_min."
            )
        if price_max is not None and price > price_max:
            raise CommandError(
                f"Cotacao invalida para '{product_name}': price maior que price_max."
            )

        return {
            "date": target_date,
            "price": price,
            "price_min": price_min,
            "price_max": price_max,
            "volume": volume,
            "notes": quote.get("notes", ""),
        }

    def _to_decimal(self, raw_value, field_name, product_name, required=True):
        if raw_value in (None, ""):
            if required:
                raise CommandError(
                    f"Cotacao invalida para '{product_name}': campo '{field_name}' nao informado."
                )
            return None

        try:
            value = Decimal(str(raw_value))
        except (InvalidOperation, TypeError, ValueError) as exc:
            raise CommandError(
                f"Cotacao invalida para '{product_name}': '{field_name}' nao eh numerico."
            ) from exc

        if value < 0:
            raise CommandError(
                f"Cotacao invalida para '{product_name}': '{field_name}' deve ser >= 0."
            )

        return value
