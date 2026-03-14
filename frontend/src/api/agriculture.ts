import { api } from "./axios";
import type { AgricultureInsights } from "../types/agriculture";

export const getInsights = async (days = 7): Promise<AgricultureInsights> => {
  const { data } = await api.get(`/api/agriculture/insights/?days=${days}`);
  return data;
};
