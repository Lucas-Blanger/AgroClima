export interface AgricultureInsightAlert {
  type: string;
  message: string;
}

export interface AgricultureInsightDrought {
  type: string;
  message: string;
}

export interface AgricultureRecommendation {
  season: string;
  recommended_crops: string[];
}

export interface AgricultureCurrentWeather {
  temperature: number;
  rain_1h: number | null;
  rain_3h: number | null;
  wind_speed: number;
  updated_at: string;
}

export interface AgricultureInsights {
  alerts: AgricultureInsightAlert[];
  drought: AgricultureInsightDrought | null;
  recommendations: AgricultureRecommendation | null;
  current_weather: AgricultureCurrentWeather | null;
  history_days: number;
  history_records: number;
}
