import { api } from "./axios";
import type { NewsArticle } from "../types/news";

interface PaginatedResponse<T> {
  results: T[];
}

export const getArticles = async (): Promise<NewsArticle[]> => {
  const { data } = await api.get("/news/articles/");

  if (Array.isArray(data)) {
    return data as NewsArticle[];
  }

  if (data && Array.isArray((data as PaginatedResponse<NewsArticle>).results)) {
    return (data as PaginatedResponse<NewsArticle>).results;
  }

  return [] as NewsArticle[];
};

export const getFeatured = async (): Promise<NewsArticle[]> => {
  const { data } = await api.get("/news/articles/featured/");
  return data as NewsArticle[];
};
