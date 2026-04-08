import type { NewsArticle } from "../types/news";
import { formatDate } from "../utils/date";
import { plainTextFromHtml } from "../utils/text";

interface Props {
  article: NewsArticle;
  index?: number;
}

export function NewsCard({ article, index = 0 }: Props) {
  const cleanSummary = plainTextFromHtml(article.summary);
  const categoryNames = Array.isArray(article.category_names)
    ? article.category_names
    : [];

  return (
    <a
      href={article.url}
      target="_blank"
      rel="noopener noreferrer"
      style={{ animationDelay: `${Math.min(index * 40, 280)}ms` }}
      className="animate-fade-up overflow-hidden rounded-2xl border border-emerald-100/70 bg-white/95 shadow-sm transition-all duration-300 hover:-translate-y-1 hover:shadow-xl"
    >
      {article.image_url ? (
        <img
          src={article.image_url}
          alt={article.title}
          className="h-48 w-full object-cover"
        />
      ) : (
        <div className="flex h-48 items-center justify-center bg-linear-to-br from-emerald-100 via-lime-50 to-cyan-100 text-sm font-semibold text-emerald-800">
          AgroClima News
        </div>
      )}

      <div className="p-5">
        <div className="mb-3 flex items-center justify-between gap-2">
          <span className="rounded-full bg-emerald-50 px-2.5 py-1 text-xs font-semibold text-emerald-700">
            {article.source}
          </span>
          <span className="text-xs text-slate-500">
            {formatDate(article.published_at)}
          </span>
        </div>

        <h3 className="line-clamp-2 text-lg font-semibold text-slate-900">
          {article.title}
        </h3>

        <p className="mt-2 line-clamp-2 text-sm text-slate-600">
          {cleanSummary || "Sem descricao disponivel."}
        </p>

        {categoryNames.length > 0 && (
          <div className="mt-3 flex flex-wrap gap-2">
            {categoryNames.slice(0, 3).map((category) => (
              <span
                key={category}
                className="rounded-md border border-slate-200 bg-slate-50 px-2 py-1 text-xs text-slate-600"
              >
                {category}
              </span>
            ))}
          </div>
        )}
      </div>
    </a>
  );
}
