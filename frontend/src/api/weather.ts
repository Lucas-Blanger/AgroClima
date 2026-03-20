import { api } from "./axios";
import type { Weather } from "../types/weather";

export interface WeatherForecastDay {
  date: string;
  temp_min: number;
  temp_max: number;
  icon: string;
  rain?: number;
}

const isWeather = (value: unknown): value is Weather => {
  if (!value || typeof value !== "object") {
    return false;
  }

  const data = value as Weather;
  return typeof data.temperature === "number";
};

export const getCurrentWeather = async (): Promise<Weather> => {
  const { data } = await api.get("/weather/current/");
  if (!isWeather(data)) {
    throw new Error("Invalid weather response");
  }
  return data;
};

export const getForecast = async (): Promise<WeatherForecastDay[]> => {
  const { data } = await api.get("/weather/forecast/");
  if (!Array.isArray(data)) {
    throw new Error("Invalid forecast response");
  }
  return data as WeatherForecastDay[];
};
