import { useEffect, useState } from "react";
import {
  getCurrentWeather,
  getForecast,
  type WeatherForecastDay,
} from "../api/weather";
import { ForecastCard } from "../components/ForecastCard";
import { CloudRadar } from "../components/CloudRadar";
import { WeatherCard } from "../components/WeatherCard";
import { WeatherChart } from "../components/WeatherChart";
import type { Weather } from "../types/weather";

interface Forecast extends WeatherForecastDay {
  temperature: number;
}

export default function Weather() {
  const [currentWeather, setCurrentWeather] = useState<Weather | null>(null);
  const [forecast, setForecast] = useState<Forecast[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchWeatherData = async () => {
      try {
        setLoading(true);

        const [weatherData, forecastData] = await Promise.all([
          getCurrentWeather(),
          getForecast(),
        ]);

        const normalizedForecast = forecastData
          .map((day) => ({
            ...day,
            temperature: (day.temp_max + day.temp_min) / 2,
          }))
          .sort((first, second) => first.date.localeCompare(second.date));

        setCurrentWeather(weatherData);
        setForecast(normalizedForecast);
        setError(null);
      } catch (err) {
        setError("Erro ao carregar dados de clima");
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchWeatherData();
  }, []);

  return (
    <section className="space-y-8">
      <header className="relative overflow-hidden rounded-3xl border border-cyan-100 bg-gradient-to-br from-sky-900 via-cyan-800 to-teal-800 px-6 py-8 text-white shadow-xl sm:px-8">
        <div className="absolute -left-16 top-0 h-44 w-44 rounded-full bg-sky-300/20 blur-3xl" />
        <div className="absolute -bottom-20 right-0 h-56 w-56 rounded-full bg-cyan-100/15 blur-3xl" />
        <p className="relative text-sm uppercase tracking-[0.2em] text-cyan-100">
          Clima diario
        </p>
        <h1 className="relative mt-3 text-3xl font-bold sm:text-4xl">
          Previsao do tempo
        </h1>
        <p className="relative mt-3 max-w-2xl text-sm text-cyan-50 sm:text-base">
          Acompanhe os próximos dias com temperaturas, chuva e tendência geral.
        </p>
      </header>

      {loading && (
        <div className="rounded-2xl border border-slate-200 bg-white/90 p-8 text-center text-slate-500 shadow-sm">
          Carregando dados de clima...
        </div>
      )}

      {error && (
        <div className="rounded-2xl border border-rose-200 bg-rose-50 p-4 text-center text-rose-700">
          {error}
        </div>
      )}

      {currentWeather && (
        <>
          <WeatherCard data={currentWeather} />
          <CloudRadar
            cloudiness={currentWeather.clouds}
            updatedAt={currentWeather.updated_at}
          />

          <div className="rounded-2xl border border-emerald-100 bg-white/95 p-6 shadow-sm">
            <div className="mb-5 flex items-center justify-between">
              <h2 className="text-xl font-semibold text-slate-900">
                Previsao para os proximos dias
              </h2>
              <span className="rounded-full bg-emerald-50 px-3 py-1 text-xs font-medium text-emerald-700">
                {forecast.length} dias
              </span>
            </div>

            {forecast.length > 0 ? (
              <div className="grid grid-cols-2 gap-4 md:grid-cols-4 xl:grid-cols-7">
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

          {forecast.length > 0 && <WeatherChart data={forecast} />}
        </>
      )}
    </section>
  );
}
