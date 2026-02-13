import { useEffect, useState } from "react";
import { getArticles } from "../api/news";
import { NewsCard } from "../components/NewsCard";
import type { NewsArticle } from "../types/news";

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
        setError("Erro ao carregar noticias");
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchArticles();
  }, []);

  return (
    <section className="space-y-8">
      <header className="relative overflow-hidden rounded-3xl border border-emerald-100 bg-gradient-to-br from-emerald-900 via-emerald-800 to-teal-800 px-6 py-8 text-white shadow-xl sm:px-8">
        <div className="absolute -right-12 -top-16 h-44 w-44 rounded-full bg-emerald-300/20 blur-3xl" />
        <div className="absolute -bottom-16 left-16 h-40 w-40 rounded-full bg-cyan-200/20 blur-3xl" />
        <p className="relative text-sm uppercase tracking-[0.2em] text-emerald-100">
          AgroClima Feed
        </p>
        <h1 className="relative mt-3 text-3xl font-bold sm:text-4xl">
          Noticias de agricultura
        </h1>
        <p className="relative mt-3 max-w-2xl text-sm text-emerald-50 sm:text-base">
          Conteudo atualizado para acompanhar clima, mercado e tecnologia no campo.
        </p>
      </header>

      {loading && (
        <div className="rounded-2xl border border-slate-200 bg-white/90 p-8 text-center text-slate-500 shadow-sm">
          Carregando noticias...
        </div>
      )}

      {error && (
        <div className="rounded-2xl border border-rose-200 bg-rose-50 p-4 text-center text-rose-700">
          {error}
        </div>
      )}

      {!loading && !error && articles.length === 0 && (
        <div className="rounded-2xl border border-slate-200 bg-white/90 p-8 text-center text-slate-500 shadow-sm">
          Nenhuma noticia disponivel no momento.
        </div>
      )}

      {articles.length > 0 && (
        <div className="grid grid-cols-1 gap-6 md:grid-cols-2 xl:grid-cols-3">
          {articles.map((article, index) => (
            <NewsCard key={article.id} article={article} index={index} />
          ))}
        </div>
      )}
    </section>
  );
}
