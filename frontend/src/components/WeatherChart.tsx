import {
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { formatDate, formatWeekday } from "../utils/date";

interface ForecastChartPoint {
  date: string;
  temp_min: number;
  temp_max: number;
  temperature: number;
}

interface Props {
  data: ForecastChartPoint[];
}

function formatAxisDate(date: string): string {
  return `${formatWeekday(date)} ${formatDate(date).slice(0, 5)}`;
}

export function WeatherChart({ data }: Props) {
  return (
    <div className="mt-8 rounded-2xl border border-emerald-100 bg-white/95 p-6 shadow-sm">
      <h3 className="mb-4 text-lg font-semibold text-slate-900">
        Tendência de temperatura
      </h3>

      <ResponsiveContainer width="100%" height={320}>
        <LineChart
          data={data}
          margin={{ top: 20, right: 16, left: 0, bottom: 0 }}
        >
          <XAxis
            dataKey="date"
            tickFormatter={formatAxisDate}
            tick={{ fill: "#475569", fontSize: 12 }}
            axisLine={{ stroke: "#e2e8f0" }}
            tickLine={{ stroke: "#e2e8f0" }}
          />
          <YAxis
            tick={{ fill: "#475569", fontSize: 12 }}
            axisLine={{ stroke: "#e2e8f0" }}
            tickLine={{ stroke: "#e2e8f0" }}
            unit="C"
          />
          <Tooltip
            labelFormatter={(value) => formatDate(String(value))}
            contentStyle={{
              borderRadius: "12px",
              borderColor: "#d1fae5",
              backgroundColor: "#ffffff",
            }}
          />
          <Line
            type="monotone"
            dataKey="temp_max"
            name="Max"
            stroke="#f97316"
            strokeWidth={2.5}
            dot={{ r: 2.5 }}
            activeDot={{ r: 4 }}
          />
          <Line
            type="monotone"
            dataKey="temperature"
            name="Media"
            stroke="#0f766e"
            strokeWidth={2.5}
            dot={{ r: 2.5 }}
            activeDot={{ r: 4 }}
          />
          <Line
            type="monotone"
            dataKey="temp_min"
            name="Min"
            stroke="#2563eb"
            strokeWidth={2.5}
            dot={{ r: 2.5 }}
            activeDot={{ r: 4 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
