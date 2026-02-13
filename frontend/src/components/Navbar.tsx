import { NavLink } from "react-router-dom";

function linkClassName(isActive: boolean): string {
  return [
    "rounded-full px-3 py-2 text-sm font-semibold transition-colors",
    isActive
      ? "bg-emerald-600 text-white shadow-sm"
      : "text-slate-700 hover:bg-emerald-50 hover:text-emerald-700",
  ].join(" ");
}

export function Navbar() {
  return (
    <nav className="sticky top-0 z-30 border-b border-emerald-100/90 bg-white/85 backdrop-blur-xl">
      <div className="mx-auto flex w-full max-w-7xl flex-col gap-4 px-4 py-4 sm:flex-row sm:items-center sm:justify-between sm:px-6 lg:px-8">
        <div className="flex items-center gap-3">
          <span className="inline-flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-br from-emerald-500 to-teal-600 text-sm font-bold text-white shadow-md">
            AC
          </span>
          <div>
            <p className="text-lg font-bold text-slate-900">AgroClima</p>
            <p className="text-xs text-slate-500">Campinas do Sul</p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <NavLink to="/" className={({ isActive }) => linkClassName(isActive)}>
            Dashboard
          </NavLink>
          <NavLink to="/news" className={({ isActive }) => linkClassName(isActive)}>
            Noticias
          </NavLink>
          <NavLink
            to="/weather"
            className={({ isActive }) => linkClassName(isActive)}
          >
            Clima
          </NavLink>
        </div>
      </div>
    </nav>
  );
}
