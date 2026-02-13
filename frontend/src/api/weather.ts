import { api } from "./axios";
import type { Weather } from "../types/weather";

export interface WeatherForecastDay {
  date: string;
  temp_min: number;
  temp_max: number;
  icon: string;
  rain?: number;
}

export const getCurrentWeather = async (): Promise<Weather> => {
  const { data } = await api.get("/api/weather/current/");
  return data as Weather;
};

export const getForecast = async (): Promise<WeatherForecastDay[]> => {
  const { data } = await api.get("/api/weather/forecast/");
  return data as WeatherForecastDay[];
};
