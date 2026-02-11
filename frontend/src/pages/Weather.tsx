import { useEffect, useState } from "react";
import { getCurrentWeather, getForecast } from "../api/weather";
import { WeatherCard } from "../components/WeatherCard";
import { ForecastCard } from "../components/ForecastCard";
import { WeatherChart } from "../components/WeatherChart";
import type { Weather } from "../types/weather";

interface Forecast {
  date: string;
  temp_min: number;
  temp_max: number;
  icon: string;
  temperature: number;
  rain?: number;
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
        setCurrentWeather(weatherData);
        setForecast(forecastData);
        setError(null);
      } catch (err) {
        setError("Erro ao carregar dados de tempo");
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchWeatherData();
  }, []);

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold text-gray-800 mb-8">
        Previsão do Tempo
      </h1>

      {loading && (
        <p className="text-center text-gray-500">
          Carregando dados de tempo...
        </p>
      )}
      {error && <p className="text-center text-red-500">{error}</p>}

      {currentWeather && (
        <>
          <WeatherCard data={currentWeather} />

          <div className="mt-8">
            <h2 className="text-2xl font-bold text-gray-800 mb-6">
              Previsão de 7 Dias
            </h2>
            {forecast.length > 0 ? (
              <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-4">
                {forecast.map((day, index) => (
                  <ForecastCard key={index} data={day} />
                ))}
              </div>
            ) : (
              <p className="text-center text-gray-500">
                Nenhuma previsão disponível
              </p>
            )}
          </div>

          {forecast.length > 0 && <WeatherChart data={forecast} />}
        </>
      )}
    </div>
  );
}
