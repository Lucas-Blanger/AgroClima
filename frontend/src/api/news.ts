import { api } from "./axios";
import type { NewsArticle } from "../types/news";

interface PaginatedResponse<T> {
  results: T[];
}

const normalizeCategoryNames = (value: unknown): string[] => {
  if (Array.isArray(value)) {
    return value.filter((item): item is string => typeof item === "string");
  }

  if (typeof value === "string" && value.trim()) {
    return [value];
  }

  return [];
};

const normalizeArticle = (value: unknown): NewsArticle | null => {
  if (!value || typeof value !== "object") {
    return null;
  }

  const article = value as Partial<NewsArticle>;

  if (typeof article.id !== "number" || typeof article.title !== "string") {
    return null;
  }

  return {
    id: article.id,
    title: article.title,
    summary: typeof article.summary === "string" ? article.summary : "",
    url: typeof article.url === "string" ? article.url : "#",
    source: typeof article.source === "string" ? article.source : "Sem fonte",
    author: typeof article.author === "string" ? article.author : "",
    image_url: typeof article.image_url === "string" ? article.image_url : "",
    published_at:
      typeof article.published_at === "string" ? article.published_at : "",
    category_names: normalizeCategoryNames(article.category_names),
    is_featured: Boolean(article.is_featured),
  };
};

const normalizeArticles = (value: unknown): NewsArticle[] => {
  if (!Array.isArray(value)) {
    return [];
  }

  return value
    .map((article) => normalizeArticle(article))
    .filter((article): article is NewsArticle => article !== null);
};

export const getArticles = async (): Promise<NewsArticle[]> => {
  const { data } = await api.get("/news/articles/");

  if (Array.isArray(data)) {
    return normalizeArticles(data);
  }

  if (data && Array.isArray((data as PaginatedResponse<NewsArticle>).results)) {
    return normalizeArticles((data as PaginatedResponse<NewsArticle>).results);
  }

  return [];
};

export const getFeatured = async (): Promise<NewsArticle[]> => {
  const { data } = await api.get("/news/articles/featured/");

  if (Array.isArray(data)) {
    return normalizeArticles(data);
  }

  if (data && Array.isArray((data as PaginatedResponse<NewsArticle>).results)) {
    return normalizeArticles((data as PaginatedResponse<NewsArticle>).results);
  }

  return [];
};
