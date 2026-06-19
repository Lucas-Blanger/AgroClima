import type { Weather } from "../types/weather";

interface Props {
  data: Weather;
}

function formatHour(datetime: string): string {
  return new Intl.DateTimeFormat("pt-BR", {
    hour: "2-digit",
    minute: "2-digit",
  }).format(new Date(datetime));
}

export function WeatherCard({ data }: Props) {
  return (
    <div className="overflow-hidden rounded-3xl bg-linear-to-br from-emerald-600 via-emerald-700 to-teal-800 p-7 text-white shadow-xl">
      <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <div>
          <p className="text-sm uppercase tracking-[0.18em] text-emerald-100">
            Agora
          </p>
          <h2 className="mt-2 text-6xl font-bold leading-none">
            {data.temperature.toFixed(0)}
            <span className="text-4xl align-top"> C</span>
          </h2>
          <p className="mt-2 text-lg capitalize text-emerald-50">
            {data.description}
          </p>
        </div>

        <img
          src={`https://openweathermap.org/img/wn/${data.icon}@4x.png`}
          alt="icone clima"
          className="w-28 md:w-32"
        />
      </div>

      <div className="mt-7 grid grid-cols-2 gap-3 text-sm md:grid-cols-4 lg:grid-cols-6">
        <div className="rounded-xl bg-white/12 p-3">
          <p className="text-emerald-100">Umidade</p>
          <p className="mt-1 font-semibold">{data.humidity}%</p>
        </div>
        <div className="rounded-xl bg-white/12 p-3">
          <p className="text-emerald-100">Vento</p>
          <p className="mt-1 font-semibold">{data.wind_speed} m/s</p>
        </div>
        <div className="rounded-xl bg-white/12 p-3">
          <p className="text-emerald-100">Pressao</p>
          <p className="mt-1 font-semibold">{data.pressure} hPa</p>
        </div>
        <div className="rounded-xl bg-white/12 p-3">
          <p className="text-emerald-100">Nuvens</p>
          <p className="mt-1 font-semibold">{data.clouds}%</p>
        </div>
        <div className="rounded-xl bg-white/12 p-3">
          <p className="text-emerald-100">Nascer do sol</p>
          <p className="mt-1 font-semibold">{formatHour(data.sunrise)}</p>
        </div>
        <div className="rounded-xl bg-white/12 p-3">
          <p className="text-emerald-100">Chuva (1h)</p>
          <p className="mt-1 font-semibold">
            {(data.rain_1h ?? 0).toFixed(1)} mm
          </p>
        </div>
      </div>
    </div>
  );
}
