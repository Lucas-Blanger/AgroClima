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
    <div className="bg-white rounded-2xl p-4 shadow-md text-center hover:shadow-lg transition">
      <p className="font-medium">
        {new Date(data.date).toLocaleDateString("pt-BR", {
          weekday: "short",
        })}
      </p>

      <img
        src={`https://openweathermap.org/img/wn/${data.icon}@2x.png`}
        className="mx-auto"
      />

      <p className="font-semibold">{data.temp_max.toFixed(0)}°</p>
      <p className="text-sm text-gray-500">{data.temp_min.toFixed(0)}°</p>
      {data.rain !== undefined && data.rain > 0 && (
        <p className="text-xs text-blue-600 mt-2">
          🌧️ {data.rain.toFixed(1)} mm
        </p>
      )}
    </div>
  );
}
