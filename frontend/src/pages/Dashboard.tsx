import { useEffect, useState } from "react";
import { getArticles, getFeatured } from "../api/news";
import { getLatestPrices } from "../api/prices";
import {
  getCurrentWeather,
  getForecast,
  type WeatherForecastDay,
} from "../api/weather";
import { Card } from "../components/Card";
import { ForecastCard } from "../components/ForecastCard";
import { NewsCard } from "../components/NewsCard";
import type { NewsArticle } from "../types/news";
import type { DailyPriceQuote } from "../types/prices";
import type { Weather } from "../types/weather";
import { formatDate } from "../utils/date";

const CATEGORY_LABELS: Record<string, string> = {
  graos: "Graos",
  hortalicas: "Hortalicas",
  frutas: "Frutas",
  pecuaria: "Pecuaria",
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

export default function Dashboard() {
  const [weather, setWeather] = useState<Weather | null>(null);
  const [forecast, setForecast] = useState<WeatherForecastDay[]>([]);
  const [forecastLoading, setForecastLoading] = useState(true);
  const [prices, setPrices] = useState<DailyPriceQuote[]>([]);
  const [pricesLoading, setPricesLoading] = useState(true);
  const [news, setNews] = useState<NewsArticle[]>([]);
  const [newsLoading, setNewsLoading] = useState(true);

  useEffect(() => {
    getCurrentWeather().then(setWeather).catch(() => setWeather(null));

    getForecast()
      .then((data) => setForecast(data.slice(0, 5)))
      .catch(() => setForecast([]))
      .finally(() => setForecastLoading(false));

    getLatestPrices()
      .then((data) => setPrices(data))
      .catch(() => setPrices([]))
      .finally(() => setPricesLoading(false));

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
      <header className="relative overflow-hidden rounded-3xl border border-emerald-100 bg-gradient-to-br from-emerald-700 via-emerald-600 to-teal-700 px-6 py-8 text-white shadow-xl sm:px-8">
        <div className="absolute -left-14 top-0 h-40 w-40 rounded-full bg-emerald-300/20 blur-3xl" />
        <div className="absolute -bottom-20 right-10 h-52 w-52 rounded-full bg-cyan-100/20 blur-3xl" />
        <p className="relative text-sm uppercase tracking-[0.2em] text-emerald-100">Painel diario</p>
        <h1 className="relative mt-3 text-3xl font-bold sm:text-4xl">
          Visao geral do AgroClima
        </h1>
        <p className="relative mt-3 max-w-2xl text-sm text-emerald-50 sm:text-base">
          Temperatura atual, previsao de 5 dias e noticias para apoiar decisoes no campo.
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
                  <p className="mt-2 capitalize text-slate-600">{weather.description}</p>
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
                  <p className="font-semibold text-slate-800">{weather.humidity}%</p>
                </div>
                <div>
                  <span className="text-slate-500">Vento:</span>
                  <p className="font-semibold text-slate-800">{weather.wind_speed} m/s</p>
                </div>
                <div>
                  <span className="text-slate-500">Pressao:</span>
                  <p className="font-semibold text-slate-800">{weather.pressure} hPa</p>
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

        <Card title="Noticias em destaque">
          {newsLoading ? (
            <p className="text-slate-500">Carregando noticias...</p>
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
                  <p className="mt-1 text-xs text-slate-500">{article.source}</p>
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-slate-500">Nenhuma noticia disponivel.</p>
          )}
        </Card>
      </div>

      <div className="rounded-2xl border border-emerald-100 bg-white/95 p-6 shadow-sm">
        <div className="mb-5 flex items-center justify-between">
          <h2 className="text-xl font-semibold text-slate-900">Previsao de 5 dias</h2>
          <span className="rounded-full bg-emerald-50 px-3 py-1 text-xs font-medium text-emerald-700">
            Atualizado diariamente
          </span>
        </div>

        {forecastLoading ? (
          <p className="text-center text-slate-500">Carregando previsao...</p>
        ) : forecast.length > 0 ? (
          <div className="grid grid-cols-2 gap-4 md:grid-cols-3 xl:grid-cols-5">
            {forecast.map((day) => (
              <ForecastCard key={day.date} data={day} />
            ))}
          </div>
        ) : (
          <p className="text-center text-slate-500">Nenhuma previsao disponivel.</p>
        )}
      </div>

      <div className="rounded-2xl border border-emerald-100 bg-white/95 p-6 shadow-sm">
        <div className="mb-5 flex items-center justify-between">
          <h2 className="text-xl font-semibold text-slate-900">Cotacoes diarias</h2>
          <span className="rounded-full bg-amber-50 px-3 py-1 text-xs font-medium text-amber-700">
            Mercado agricola
          </span>
        </div>

        {pricesLoading ? (
          <p className="text-center text-slate-500">Carregando cotacoes...</p>
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
                    <div>
                      <h3 className="text-base font-semibold text-slate-900">{quote.product_name}</h3>
                      <p className="text-xs text-slate-500">
                        {CATEGORY_LABELS[quote.category] ?? quote.category}
                      </p>
                    </div>
                    <span className={`text-xs font-semibold ${variationClass}`}>
                      {variation === null
                        ? "Sem variacao"
                        : `Variacao ${variation > 0 ? "+" : ""}${variation.toFixed(2)}%`}
                    </span>
                  </div>

                  <p className="mt-4 text-2xl font-bold text-slate-900">
                    {price === null ? String(quote.price) : CURRENCY_FORMATTER.format(price)}
                  </p>
                  <p className="text-sm text-slate-500">Unidade: {quote.unit}</p>

                  <div className="mt-4 flex items-center justify-between border-t border-amber-100 pt-3 text-xs text-slate-500">
                    <span>{quote.source ?? "Sem fonte"}</span>
                    <span>{formatDate(quote.date)}</span>
                  </div>
                </article>
              );
            })}
          </div>
        ) : (
          <p className="text-center text-slate-500">Nenhuma cotacao disponivel.</p>
        )}
      </div>

      {news.length > 0 && (
        <div>
          <h2 className="mb-6 text-2xl font-bold text-slate-900">Ultimas noticias</h2>
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
