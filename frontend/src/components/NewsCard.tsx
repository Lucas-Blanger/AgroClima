export function NewsCard({ article }: { article: any }) {
  return (
    <a
      href={article.url}
      target="_blank"
      rel="noopener noreferrer"
      className="bg-white rounded-2xl shadow-md overflow-hidden hover:shadow-xl transition"
    >
      {article.image_url && (
        <img
          src={article.image_url}
          alt={article.title}
          className="w-full h-48 object-cover"
        />
      )}
      <div className="p-6">
        <div className="flex items-center justify-between mb-2">
          <span className="text-xs font-medium text-green-600 bg-green-50 px-2 py-1 rounded">
            {article.source}
          </span>
          <span className="text-xs text-gray-500">
            {new Date(article.published_at).toLocaleDateString("pt-BR")}
          </span>
        </div>
        <h3 className="font-semibold text-lg line-clamp-2">{article.title}</h3>
        <p className="text-sm text-gray-600 mt-2 line-clamp-2">
          {article.summary}
        </p>
        {article.category_names && article.category_names.length > 0 && (
          <div className="flex gap-2 mt-3 flex-wrap">
            {article.category_names.map((cat: string, idx: number) => (
              <span
                key={idx}
                className="text-xs bg-gray-100 text-gray-700 px-2 py-1 rounded"
              >
                {cat}
              </span>
            ))}
          </div>
        )}
      </div>
    </a>
  );
}
