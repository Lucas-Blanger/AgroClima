import type { WeatherAlert, AlertSeverity } from "../types/weather";

interface Props {
  alert: WeatherAlert;
}

const severityStyles: Record<AlertSeverity, string> = {
  low: "bg-yellow-50 border-yellow-300 text-yellow-800",
  medium: "bg-orange-50 border-orange-300 text-orange-800",
  high: "bg-red-50 border-red-300 text-red-800",
  extreme: "bg-purple-50 border-purple-400 text-purple-900",
};

export function AlertCard({ alert }: Props) {
  return (
    <div
      className={`border rounded-2xl p-5 shadow-sm ${severityStyles[alert.severity]}`}
    >
      <div className="flex justify-between items-center">
        <h4 className="font-semibold text-lg">{alert.event}</h4>

        <span className="text-sm font-medium capitalize">{alert.severity}</span>
      </div>

      <p className="text-sm mt-3">{alert.description}</p>

      <div className="text-xs mt-4 opacity-70">
        <p>Início: {new Date(alert.start_time).toLocaleString("pt-BR")}</p>
        <p>Fim: {new Date(alert.end_time).toLocaleString("pt-BR")}</p>
      </div>
    </div>
  );
}
