import { formatDate, formatWeekday } from "../utils/date";

interface Forecast {
  date: string;
  temp_min: number;
  temp_max: number;
  icon: string;
  rain?: number;
}

interface Props {
  data: Forecast;
}

export function ForecastCard({ data }: Props) {
  return (
    <div className="group rounded-2xl border border-emerald-100 bg-white/90 p-4 text-center shadow-sm transition-all duration-300 hover:-translate-y-0.5 hover:shadow-lg">
      <p className="text-sm font-semibold uppercase tracking-wide text-slate-700">
        {formatWeekday(data.date)}
      </p>
      <p className="text-xs text-slate-500">{formatDate(data.date)}</p>

      <img
        src={`https://openweathermap.org/img/wn/${data.icon}@2x.png`}
        className="mx-auto mt-1 w-20 transition-transform duration-300 group-hover:scale-105"
        alt="icone clima"
      />

      <p className="text-lg font-semibold text-slate-900">
        {data.temp_max.toFixed(0)} C
      </p>
      <p className="text-sm text-slate-500">{data.temp_min.toFixed(0)} C</p>
      {data.rain !== undefined && data.rain > 0 && (
        <p className="mt-2 text-xs font-medium text-cyan-700">
          Chuva: {data.rain.toFixed(1)} mm
        </p>
      )}
    </div>
  );
}
