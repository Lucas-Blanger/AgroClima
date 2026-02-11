import type { Weather } from "../types/weather";

interface Props {
  data: Weather;
}

export function WeatherCard({ data }: Props) {
  return (
    <div className="bg-linear-to-br from-green-500 to-green-700 text-white rounded-3xl p-8 shadow-xl">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-6xl font-bold">{data.temperature.toFixed(0)}°</h2>
          <p className="text-xl capitalize mt-2">{data.description}</p>
        </div>

        <img
          src={`https://openweathermap.org/img/wn/${data.icon}@4x.png`}
          alt="weather icon"
          className="w-32"
        />
      </div>

      <div className="grid grid-cols-5 gap-4 mt-8 text-sm">
        <div>
          <p className="opacity-70">Umidade</p>
          <p className="font-semibold">{data.humidity}%</p>
        </div>
        <div>
          <p className="opacity-70">Vento</p>
          <p className="font-semibold">{data.wind_speed} m/s</p>
        </div>
        <div>
          <p className="opacity-70">Pressão</p>
          <p className="font-semibold">{data.pressure} hPa</p>
        </div>
        <div>
          <p className="opacity-70">Nuvens</p>
          <p className="font-semibold">{data.clouds}%</p>
        </div>
        <div>
          <p className="opacity-70">Chuva</p>
          <p className="font-semibold">{(data.rain_1h ?? 0).toFixed(1)} mm</p>
        </div>
      </div>
    </div>
  );
}
