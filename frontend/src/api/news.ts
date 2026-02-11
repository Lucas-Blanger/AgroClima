import { api } from "./axios";

export const getArticles = async () => {
  const { data } = await api.get("/api/news/articles/");
  return data;
};

export const getFeatured = async () => {
  const { data } = await api.get("/api/news/articles/featured/");
  return data;
};
