export interface Weather {
  id: number;
  temperature: number;
  feels_like: number;
  temp_min: number;
  temp_max: number;
  humidity: number;
  pressure: number;
  wind_speed: number;
  wind_deg: number;
  clouds: number;
  rain_1h: number | null;
  rain_3h: number | null;
  description: string;
  icon: string;
  sunrise: string;
  sunset: string;
  updated_at: string;
}
export type AlertSeverity = "low" | "medium" | "high" | "extreme";
export interface WeatherAlert {
  id: number;
  event: string;
  severity: AlertSeverity;
  description: string;
  start_time: string;
  end_time: string;
  is_active: boolean;
  created_at: string;
}
