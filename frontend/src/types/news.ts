export interface NewsArticle {
  id: number;
  title: string;
  summary: string;
  url: string;
  source: string;
  author: string;
  image_url: string;
  published_at: string;
  category_names: string[];
  is_featured: boolean;
}
