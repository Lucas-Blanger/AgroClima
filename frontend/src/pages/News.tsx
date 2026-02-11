import { useEffect, useState } from "react";
import { getArticles } from "../api/news";
import { NewsCard } from "../components/NewsCard";

interface NewsArticle {
  id: number;
  title: string;
  summary: string;
  content: string;
  image_url: string;
  published_at: string;
}

export default function News() {
  const [articles, setArticles] = useState<NewsArticle[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchArticles = async () => {
      try {
        setLoading(true);
        const data = await getArticles();
        setArticles(data);
        setError(null);
      } catch (err) {
        setError("Erro ao carregar as notícias");
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchArticles();
  }, []);

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold text-gray-800 mb-8">
        Notícias de Agricultura
      </h1>

      {loading && (
        <p className="text-center text-gray-500">Carregando notícias...</p>
      )}
      {error && <p className="text-center text-red-500">{error}</p>}

      {articles.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {articles.map((article) => (
            <NewsCard key={article.id} article={article} />
          ))}
        </div>
      ) : (
        !loading && (
          <p className="text-center text-gray-500">
            Nenhuma notícia disponível
          </p>
        )
      )}
    </div>
  );
}
