import { api } from "./axios";
import type {
  AgricultureCurrentWeather,
  AgricultureInsightAlert,
  AgricultureInsightDrought,
  AgricultureInsights,
  AgricultureRecommendation,
} from "../types/agriculture";

const normalizeAlerts = (value: unknown): AgricultureInsightAlert[] => {
  if (!Array.isArray(value)) {
    return [];
  }

  return value
    .filter(
      (item): item is Record<string, unknown> =>
        Boolean(item) && typeof item === "object",
    )
    .map((item) => ({
      type: typeof item.type === "string" ? item.type : "info",
      message: typeof item.message === "string" ? item.message : "",
    }));
};

const normalizeDrought = (value: unknown): AgricultureInsightDrought | null => {
  if (!value || typeof value !== "object") {
    return null;
  }

  const record = value as Record<string, unknown>;
  return {
    type: typeof record.type === "string" ? record.type : "drought",
    message: typeof record.message === "string" ? record.message : "",
  };
};

const normalizeRecommendations = (
  value: unknown,
): AgricultureRecommendation | null => {
  if (!value || typeof value !== "object") {
    return null;
  }

  const record = value as Record<string, unknown>;
  return {
    season: typeof record.season === "string" ? record.season : "",
    recommended_crops: Array.isArray(record.recommended_crops)
      ? record.recommended_crops.filter(
          (item): item is string => typeof item === "string",
        )
      : [],
  };
};

const normalizeCurrentWeather = (
  value: unknown,
): AgricultureCurrentWeather | null => {
  if (!value || typeof value !== "object") {
    return null;
  }

  const record = value as Record<string, unknown>;
  if (typeof record.temperature !== "number") {
    return null;
  }

  return {
    temperature: record.temperature,
    rain_1h: typeof record.rain_1h === "number" ? record.rain_1h : null,
    rain_3h: typeof record.rain_3h === "number" ? record.rain_3h : null,
    wind_speed: typeof record.wind_speed === "number" ? record.wind_speed : 0,
    updated_at: typeof record.updated_at === "string" ? record.updated_at : "",
  };
};

const normalizeInsights = (value: unknown): AgricultureInsights => {
  const record =
    value && typeof value === "object" ? (value as Record<string, unknown>) : {};

  return {
    alerts: normalizeAlerts(record.alerts),
    drought: normalizeDrought(record.drought),
    recommendations: normalizeRecommendations(record.recommendations),
    current_weather: normalizeCurrentWeather(record.current_weather),
    history_days: typeof record.history_days === "number" ? record.history_days : 0,
    history_records:
      typeof record.history_records === "number" ? record.history_records : 0,
  };
};

export const getInsights = async (days = 7): Promise<AgricultureInsights> => {
  const { data } = await api.get(`/agriculture/insights/?days=${days}`);
  return normalizeInsights(data);
};
