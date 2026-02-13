interface Props {
  title: string;
  children: React.ReactNode;
}

export function Card({ title, children }: Props) {
  return (
    <div className="rounded-2xl border border-emerald-100 bg-white/95 p-6 shadow-sm transition-all duration-300 hover:-translate-y-0.5 hover:shadow-lg">
      <h2 className="mb-4 text-xl font-semibold text-slate-900">{title}</h2>
      {children}
    </div>
  );
}
