import { api } from "./axios";

export const getCurrentWeather = async () => {
  const { data } = await api.get("/api/weather/current/");
  return data;
};

export const getForecast = async () => {
  const { data } = await api.get("/api/weather/forecast/");
  return data;
};
