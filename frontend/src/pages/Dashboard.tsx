import { useEffect, useState } from "react";
import { getCurrentWeather } from "../api/weather";
import { getFeatured } from "../api/news";
import { Card } from "../components/Card";
import { NewsCard } from "../components/NewsCard";
import type { Weather } from "../types/weather";
import type { NewsArticle } from "../types/news";

export default function Dashboard() {
  const [weather, setWeather] = useState<Weather | null>(null);
  const [news, setNews] = useState<NewsArticle[]>([]);
  const [newsLoading, setNewsLoading] = useState(true);

  useEffect(() => {
    getCurrentWeather().then(setWeather);
    getFeatured()
      .then(setNews)
      .catch(() => setNews([]))
      .finally(() => setNewsLoading(false));
  }, []);

  return (
    <div className="p-8">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        <Card title="Clima Atual">
          {weather ? (
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-4xl font-bold text-green-600">
                    {weather.temperature.toFixed(0)}°C
                  </p>
                  <p className="text-slate-500 capitalize mt-2">
                    {weather.description}
                  </p>
                </div>
                <img
                  src={`https://openweathermap.org/img/wn/${weather.icon}@4x.png`}
                  alt="weather"
                  className="w-20"
                />
              </div>

              <div className="grid grid-cols-2 gap-3 text-sm">
                <div>
                  <span className="text-gray-500">Umidade:</span>
                  <p className="font-semibold">{weather.humidity}%</p>
                </div>
                <div>
                  <span className="text-gray-500">Vento:</span>
                  <p className="font-semibold">{weather.wind_speed} m/s</p>
                </div>
                <div>
                  <span className="text-gray-500">Pressão:</span>
                  <p className="font-semibold">{weather.pressure} hPa</p>
                </div>
                <div>
                  <span className="text-gray-500">Chuva:</span>
                  <p className="font-semibold">
                    {(weather.rain_1h ?? 0).toFixed(1)} mm
                  </p>
                </div>
              </div>
            </div>
          ) : (
            "Carregando..."
          )}
        </Card>

        <Card title="Notícias em Destaque">
          {newsLoading ? (
            <p className="text-gray-500">Carregando notícias...</p>
          ) : news.length > 0 ? (
            <ul className="space-y-3">
              {news.slice(0, 3).map((article) => (
                <li key={article.id}>
                  <a
                    href={article.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-sm font-medium text-green-600 hover:underline line-clamp-2"
                  >
                    {article.title}
                  </a>
                  <p className="text-xs text-gray-500 mt-1">{article.source}</p>
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-gray-500">Nenhuma notícia disponível</p>
          )}
        </Card>
      </div>

      {news.length > 0 && (
        <div>
          <h2 className="text-2xl font-bold text-gray-800 mb-6">
            Últimas Notícias
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {news.map((article) => (
              <NewsCard key={article.id} article={article} />
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
