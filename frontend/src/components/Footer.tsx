export function Footer() {
  return (
    <footer className="mt-16 border-t border-emerald-100 bg-white/95">
      <div className="mx-auto max-w-7xl px-6 py-10">
        <div className="grid grid-cols-1 gap-8 md:grid-cols-3">
          <div>
            <div className="flex items-center gap-3">
              <img
                src="/logo.png"
                alt="Logo AgroClima"
                className="h-10 w-auto"
              />
              <h3 className="text-lg font-bold text-emerald-700">AgroClima</h3>
            </div>

            <p className="mt-3 text-sm text-slate-600">
              Plataforma para acompanhar clima, cotações agrícolas e notícias
              relevantes para apoiar decisões no campo.
            </p>
          </div>
          <div>
            <h4 className="text-sm font-semibold uppercase tracking-wider text-slate-800">
              Navegação
            </h4>
            <ul className="mt-3 space-y-2 text-sm">
              <li>
                <a
                  href="/"
                  className="text-slate-600 hover:text-emerald-700 transition"
                >
                  Dashboard
                </a>
              </li>
              <li>
                <a
                  href="/weather"
                  className="text-slate-600 hover:text-emerald-700 transition"
                >
                  Clima
                </a>
              </li>

              <li>
                <a
                  href="/news"
                  className="text-slate-600 hover:text-emerald-700 transition"
                >
                  Notícias
                </a>
              </li>
            </ul>
          </div>

          <div>
            <h4 className="text-sm font-semibold uppercase tracking-wider text-slate-800">
              Informações
            </h4>
            <ul className="mt-3 space-y-2 text-sm text-slate-600">
              <li>Dados climáticos: OpenWeather</li>
              <li>Cotações: CEPEA/ESALQ/DADOS-MANUAIS</li>
              <li>Atualizado diariamente</li>
            </ul>
          </div>
        </div>

        <div className="mt-10 border-t border-emerald-100 pt-6 text-center text-xs text-slate-500">
          © {new Date().getFullYear()} AgroClima. Todos os direitos reservados.
        </div>
      </div>
    </footer>
  );
}
