import { api } from "./axios";
import type { DailyPriceQuote } from "../types/prices";

interface PaginatedResponse<T> {
  results: T[];
}

export const getLatestPrices = async (): Promise<DailyPriceQuote[]> => {
  const { data } = await api.get("/prices/prices/latest/");

  if (Array.isArray(data)) {
    return data as DailyPriceQuote[];
  }

  if (
    data &&
    Array.isArray((data as PaginatedResponse<DailyPriceQuote>).results)
  ) {
    return (data as PaginatedResponse<DailyPriceQuote>).results;
  }

  return [] as DailyPriceQuote[];
};
