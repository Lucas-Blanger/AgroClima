import { useEffect, useState } from "react";
import { getArticles, getFeatured } from "../api/news";
import { getLatestPrices } from "../api/prices";
import { getInsights } from "../api/agriculture";
import {
  getCurrentWeather,
  getForecast,
  type WeatherForecastDay,
} from "../api/weather";
import { Card } from "../components/Card";
import { CloudRadar } from "../components/CloudRadar";
import { ForecastCard } from "../components/ForecastCard";
import { NewsCard } from "../components/NewsCard";
import type { NewsArticle } from "../types/news";
import type { DailyPriceQuote } from "../types/prices";
import type { Weather } from "../types/weather";
import type { AgricultureInsights } from "../types/agriculture";
import { formatDate } from "../utils/date";

const CATEGORY_LABELS: Record<string, string> = {
  graos: "Grãos",
  hortalicas: "Hortaliças",
  frutas: "Frutas",
  pecuaria: "Pecuária",
  insumos: "Insumos",
};

const CURRENCY_FORMATTER = new Intl.NumberFormat("pt-BR", {
  style: "currency",
  currency: "BRL",
});

function toNumber(value: string | number | null | undefined): number | null {
  if (value === null || value === undefined) {
    return null;
  }

  const parsed = typeof value === "number" ? value : Number(value);
  return Number.isFinite(parsed) ? parsed : null;
}

type CultureIconKind =
  | "grain"
  | "vegetable"
  | "fruit"
  | "livestock"
  | "input"
  | "generic";

const PRODUCT_ICON_KINDS: Record<string, CultureIconKind> = {
  soja: "grain",
  milho: "grain",
  trigo: "grain",
  arroz: "grain",
  tomate: "vegetable",
  leite: "livestock",
  "boi gordo": "livestock",
  "fertilizante npk": "input",
};

const CATEGORY_ICON_KINDS: Record<string, CultureIconKind> = {
  graos: "grain",
  hortalicas: "vegetable",
  frutas: "fruit",
  pecuaria: "livestock",
  insumos: "input",
};

function getCultureIconKind(quote: DailyPriceQuote): CultureIconKind {
  const byProduct = PRODUCT_ICON_KINDS[quote.product_name.trim().toLowerCase()];
  if (byProduct) {
    return byProduct;
  }

  return CATEGORY_ICON_KINDS[quote.category] ?? "generic";
}

function CultureIcon({ kind }: { kind: CultureIconKind }) {
  const className = "h-5 w-5 text-amber-700";

  if (kind === "grain") {
    return (
      <svg viewBox="0 0 24 24" fill="none" className={className}>
        <path
          d="M12 3v18M8 7c2 0 3 1 3 3-2 0-3-1-3-3zM16 7c-2 0-3 1-3 3 2 0 3-1 3-3zM8 12c2 0 3 1 3 3-2 0-3-1-3-3zM16 12c-2 0-3 1-3 3 2 0 3-1 3-3z"
          stroke="currentColor"
          strokeWidth="1.8"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </svg>
    );
  }

  if (kind === "vegetable") {
    return (
      <svg viewBox="0 0 24 24" fill="none" className={className}>
        <path
          d="M5 15c0-5 4-9 9-9h5v5c0 5-4 9-9 9H5v-5zM8 16c3-3 5-5 8-8"
          stroke="currentColor"
          strokeWidth="1.8"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </svg>
    );
  }

  if (kind === "fruit") {
    return (
      <svg viewBox="0 0 24 24" fill="none" className={className}>
        <path
          d="M12 7c-2.5 0-4 1.8-4 4.2 0 3.4 2.2 6.8 4 6.8s4-3.4 4-6.8C16 8.8 14.5 7 12 7zM12 7c0-1.4.9-2.7 2.2-3.2M10 5c.8.8 2 .8 2.8 0"
          stroke="currentColor"
          strokeWidth="1.8"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </svg>
    );
  }

  if (kind === "livestock") {
    return (
      <svg viewBox="0 0 24 24" fill="none" className={className}>
        <path
          d="M7 9h10a2 2 0 0 1 2 2v4a4 4 0 0 1-4 4H9a4 4 0 0 1-4-4v-4a2 2 0 0 1 2-2zM7 10 4.5 8M17 10 19.5 8M10 17h4"
          stroke="currentColor"
          strokeWidth="1.8"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
        <circle cx="10" cy="13.5" r="0.8" fill="currentColor" />
        <circle cx="14" cy="13.5" r="0.8" fill="currentColor" />
      </svg>
    );
  }

  if (kind === "input") {
    return (
      <svg viewBox="0 0 24 24" fill="none" className={className}>
        <path
          d="M10 3h4M11 3v5l-4.5 7.5A2 2 0 0 0 8.2 19h7.6a2 2 0 0 0 1.7-3l-4.5-7.5V3M9 14h6"
          stroke="currentColor"
          strokeWidth="1.8"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </svg>
    );
  }

  return (
    <svg viewBox="0 0 24 24" fill="none" className={className}>
      <path
        d="M12 20c4-2.5 6-6.2 6-10 0-1.7-1.3-3-3-3-1.3 0-2.4.8-3 1.9C11.4 7.8 10.3 7 9 7c-1.7 0-3 1.3-3 3 0 3.8 2 7.5 6 10z"
        stroke="currentColor"
        strokeWidth="1.8"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

export default function Dashboard() {
  const [weather, setWeather] = useState<Weather | null>(null);
  const [forecast, setForecast] = useState<WeatherForecastDay[]>([]);
  const [forecastLoading, setForecastLoading] = useState(true);
  const [prices, setPrices] = useState<DailyPriceQuote[]>([]);
  const [pricesLoading, setPricesLoading] = useState(true);
  const [news, setNews] = useState<NewsArticle[]>([]);
  const [newsLoading, setNewsLoading] = useState(true);
  const [insights, setInsights] = useState<AgricultureInsights | null>(null);
  const [insightsLoading, setInsightsLoading] = useState(true);

  useEffect(() => {
    getCurrentWeather()
      .then(setWeather)
      .catch(() => setWeather(null));

    getForecast()
      .then((data) => setForecast(data.slice(0, 5)))
      .catch(() => setForecast([]))
      .finally(() => setForecastLoading(false));

    getLatestPrices()
      .then((data) => setPrices(data))
      .catch(() => setPrices([]))
      .finally(() => setPricesLoading(false));

    getInsights()
      .then(setInsights)
      .catch(() => setInsights(null))
      .finally(() => setInsightsLoading(false));

    const fetchNews = async () => {
      try {
        const featured = await getFeatured();

        if (featured.length > 0) {
          setNews(featured);
          return;
        }

        const latest = await getArticles();
        setNews(latest.slice(0, 6));
      } catch {
        setNews([]);
      } finally {
        setNewsLoading(false);
      }
    };

    fetchNews();
  }, []);

  return (
    <section className="space-y-8">
      <header className="relative overflow-hidden rounded-3xl border border-emerald-100 bg-linear-to-br from-emerald-700 via-emerald-600 to-teal-700 px-6 py-8 text-white shadow-xl sm:px-8">
        <div className="absolute -left-14 top-0 h-40 w-40 rounded-full bg-emerald-300/20 blur-3xl" />
        <div className="absolute -bottom-20 right-10 h-52 w-52 rounded-full bg-cyan-100/20 blur-3xl" />
        <p className="relative text-sm uppercase tracking-[0.2em] text-emerald-100">
          Painel diário
        </p>
        <h1 className="relative mt-3 text-3xl font-bold sm:text-4xl">
          Visão geral do AgroClima
        </h1>
        <p className="relative mt-3 max-w-2xl text-sm text-emerald-50 sm:text-base">
          Temperatura atual, previsão de 5 dias e notícias para apoiar decisões
          no campo.
        </p>
      </header>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <Card title="Clima atual">
          {weather ? (
            <div className="space-y-4">
              <div className="flex items-center justify-between gap-4">
                <div>
                  <p className="text-5xl font-bold text-emerald-700">
                    {weather.temperature.toFixed(0)} C
                  </p>
                  <p className="mt-2 capitalize text-slate-600">
                    {weather.description}
                  </p>
                </div>
                <img
                  src={`https://openweathermap.org/img/wn/${weather.icon}@4x.png`}
                  alt="icone clima"
                  className="w-24"
                />
              </div>

              <div className="grid grid-cols-2 gap-3 text-sm">
                <div>
                  <span className="text-slate-500">Umidade:</span>
                  <p className="font-semibold text-slate-800">
                    {weather.humidity}%
                  </p>
                </div>
                <div>
                  <span className="text-slate-500">Vento:</span>
                  <p className="font-semibold text-slate-800">
                    {weather.wind_speed} m/s
                  </p>
                </div>
                <div>
                  <span className="text-slate-500">Pressão:</span>
                  <p className="font-semibold text-slate-800">
                    {weather.pressure} hPa
                  </p>
                </div>
                <div>
                  <span className="text-slate-500">Chuva 1h:</span>
                  <p className="font-semibold text-slate-800">
                    {(weather.rain_1h ?? 0).toFixed(1)} mm
                  </p>
                </div>
              </div>
            </div>
          ) : (
            <p className="text-slate-500">Carregando clima...</p>
          )}
        </Card>

        <Card title="Notícias em destaque">
          {newsLoading ? (
            <p className="text-slate-500">Carregando notícias...</p>
          ) : news.length > 0 ? (
            <ul className="space-y-3">
              {news.slice(0, 4).map((article) => (
                <li key={article.id}>
                  <a
                    href={article.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="line-clamp-2 text-sm font-semibold text-emerald-700 transition-colors hover:text-emerald-900"
                  >
                    {article.title}
                  </a>
                  <p className="mt-1 text-xs text-slate-500">
                    {article.source}
                  </p>
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-slate-500">Nenhuma notícia disponível.</p>
          )}
        </Card>
      </div>

      <Card title="Insights agrícolas">
        {insightsLoading ? (
          <p className="text-slate-500">Carregando insights...</p>
        ) : insights ? (
          <div className="space-y-4">
            <div>
              <p className="text-sm font-semibold text-slate-700">
                Recomendações
              </p>
              {insights.recommendations?.recommended_crops?.length ? (
                <div className="mt-2 flex flex-wrap gap-2">
                  {insights.recommendations.recommended_crops.map((crop) => (
                    <span
                      key={crop}
                      className="rounded-full bg-emerald-50 px-3 py-1 text-xs font-semibold text-emerald-700"
                    >
                      {crop}
                    </span>
                  ))}
                </div>
              ) : (
                <p className="mt-2 text-sm text-slate-500">
                  Sem recomendações no momento.
                </p>
              )}
              <p className="mt-2 text-xs text-slate-500">
                Estacao: {insights.recommendations?.season ?? "indisponivel"}
              </p>
            </div>

            <div>
              <p className="text-sm font-semibold text-slate-700">Alertas</p>
              {insights.alerts.length > 0 ? (
                <ul className="mt-2 space-y-2 text-sm text-slate-600">
                  {insights.alerts.map((alert, index) => (
                    <li
                      key={`${alert.type}-${index}`}
                      className="rounded-lg border border-amber-100 bg-amber-50/50 px-3 py-2"
                    >
                      <span className="font-semibold text-amber-800">
                        {alert.type}
                      </span>{" "}
                      - {alert.message}
                    </li>
                  ))}
                </ul>
              ) : (
                <p className="mt-2 text-sm text-slate-500">
                  Sem alertas no momento.
                </p>
              )}
            </div>

            <div>
              <p className="text-sm font-semibold text-slate-700">Seca</p>
              {insights.drought ? (
                <p className="mt-2 text-sm text-rose-700">
                  {insights.drought.message}
                </p>
              ) : (
                <p className="mt-2 text-sm text-slate-500">
                  Sem indícios de seca.
                </p>
              )}
            </div>
          </div>
        ) : (
          <p className="text-slate-500">Sem dados de insights.</p>
        )}
      </Card>

      <div className="rounded-2xl border border-emerald-100 bg-white/95 p-6 shadow-sm">
        <div className="mb-5 flex items-center justify-between">
          <h2 className="text-xl font-semibold text-slate-900">
            Previsão de 5 dias
          </h2>
        </div>

        {forecastLoading ? (
          <p className="text-center text-slate-500">Carregando previsão...</p>
        ) : forecast.length > 0 ? (
          <div className="grid grid-cols-2 gap-4 md:grid-cols-3 xl:grid-cols-5">
            {forecast.map((day) => (
              <ForecastCard key={day.date} data={day} />
            ))}
          </div>
        ) : (
          <p className="text-center text-slate-500">
            Nenhuma previsão disponível.
          </p>
        )}
      </div>

      <div className="rounded-2xl border border-emerald-100 bg-white/95 p-6 shadow-sm">
        <div className="mb-5 flex items-center justify-between">
          <h2 className="text-xl font-semibold text-slate-900">
            Cotações Diárias
          </h2>
        </div>

        {pricesLoading ? (
          <p className="text-center text-slate-500">Carregando cotações...</p>
        ) : prices.length > 0 ? (
          <div className="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-3">
            {prices.map((quote) => {
              const price = toNumber(quote.price);
              const variation = toNumber(quote.variation);
              const variationClass =
                variation === null
                  ? "text-slate-500"
                  : variation > 0
                    ? "text-emerald-700"
                    : variation < 0
                      ? "text-rose-700"
                      : "text-slate-500";

              return (
                <article
                  key={quote.product_id}
                  className="rounded-xl border border-amber-100 bg-gradient-to-br from-white to-amber-50/40 p-4 shadow-sm"
                >
                  <div className="flex items-start justify-between gap-3">
                    <div className="flex items-center gap-3">
                      <span className="inline-flex h-10 w-10 items-center justify-center rounded-xl bg-amber-100 shadow-sm">
                        <CultureIcon kind={getCultureIconKind(quote)} />
                      </span>
                      <div>
                        <h3 className="text-base font-semibold text-slate-900">
                          {quote.product_name}
                        </h3>
                        <p className="text-xs text-slate-500">
                          {CATEGORY_LABELS[quote.category] ?? quote.category}
                        </p>
                      </div>
                    </div>
                    <span className={`text-xs font-semibold ${variationClass}`}>
                      {variation === null
                        ? "Sem variação"
                        : `Variação ${variation > 0 ? "+" : ""}${variation.toFixed(2)}%`}
                    </span>
                  </div>

                  <p className="mt-4 text-2xl font-bold text-slate-900">
                    {price === null
                      ? String(quote.price)
                      : CURRENCY_FORMATTER.format(price)}
                  </p>
                  <p className="text-sm text-slate-500">
                    Unidade: {quote.unit}
                  </p>

                  <div className="mt-4 flex items-center justify-between border-t border-amber-100 pt-3 text-xs text-slate-500">
                    <span>{quote.source ?? "Sem fonte"}</span>
                    <span>{formatDate(quote.date)}</span>
                  </div>
                </article>
              );
            })}
          </div>
        ) : (
          <p className="text-center text-slate-500">
            Nenhuma cotação disponível.
          </p>
        )}
      </div>

      {weather && (
        <CloudRadar
          cloudiness={weather.clouds}
          updatedAt={weather.updated_at}
        />
      )}

      {news.length > 0 && (
        <div>
          <h2 className="mb-6 text-2xl font-bold text-slate-900">
            Ultimas notícias
          </h2>
          <div className="grid grid-cols-1 gap-6 md:grid-cols-2 xl:grid-cols-3">
            {news.map((article, index) => (
              <NewsCard key={article.id} article={article} index={index} />
            ))}
          </div>
        </div>
      )}
    </section>
  );
}
