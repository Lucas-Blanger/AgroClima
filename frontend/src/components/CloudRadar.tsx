import { formatDate, parseDate } from "../utils/date";

interface Props {
  cloudiness: number;
  updatedAt?: string;
}

const CLOUD_POSITIONS = [
  {
    id: "north",
    x: 28,
    y: 26,
    size: 56,
    baseOpacity: 0.55,
    drift: "cloud-float",
    delay: "0s",
  },
  {
    id: "east",
    x: 72,
    y: 22,
    size: 44,
    baseOpacity: 0.4,
    drift: "cloud-drift",
    delay: "1.1s",
  },
  {
    id: "center",
    x: 58,
    y: 55,
    size: 68,
    baseOpacity: 0.5,
    drift: "cloud-float",
    delay: "0.6s",
  },
  {
    id: "south",
    x: 34,
    y: 72,
    size: 50,
    baseOpacity: 0.38,
    drift: "cloud-drift",
    delay: "1.6s",
  },
  {
    id: "west",
    x: 20,
    y: 50,
    size: 36,
    baseOpacity: 0.32,
    drift: "cloud-float",
    delay: "0.9s",
  },
  {
    id: "southeast",
    x: 76,
    y: 64,
    size: 40,
    baseOpacity: 0.34,
    drift: "cloud-drift",
    delay: "0.3s",
  },
] as const;

function clamp(value: number, min: number, max: number): number {
  return Math.min(max, Math.max(min, value));
}

function normalizeCloudiness(value: number): number {
  if (!Number.isFinite(value)) {
    return 0;
  }

  return clamp(Math.round(value), 0, 100);
}

function formatHour(dateInput: string): string {
  return new Intl.DateTimeFormat("pt-BR", {
    hour: "2-digit",
    minute: "2-digit",
  }).format(parseDate(dateInput));
}

function cloudLabel(value: number): string {
  if (value < 15) {
    return "Céu aberto";
  }
  if (value < 35) {
    return "Poucas nuvens";
  }
  if (value < 60) {
    return "Parcialmente nublado";
  }
  if (value < 85) {
    return "Nublado";
  }
  return "Encoberto";
}

function CloudIcon({ className }: { className?: string }) {
  return (
    <svg
      viewBox="0 0 64 40"
      fill="none"
      className={className}
      aria-hidden="true"
    >
      <path
        d="M18.5 32h26.2a11.8 11.8 0 0 0 0-23.6 14.6 14.6 0 0 0-28.4-2.2A10.3 10.3 0 0 0 18.5 32z"
        fill="currentColor"
      />
    </svg>
  );
}

export function CloudRadar({ cloudiness, updatedAt }: Props) {
  const normalizedCloudiness = normalizeCloudiness(cloudiness);
  const density = normalizedCloudiness / 100;
  const cloudCount = Math.max(1, Math.round(1 + density * 5));
  const visibleClouds = CLOUD_POSITIONS.slice(0, cloudCount);
  const opacityBoost = 0.25 + density * 0.6;

  return (
    <div className="rounded-2xl border border-emerald-100 bg-white/95 p-6 shadow-sm">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h2 className="text-xl font-semibold text-slate-900">
            Radar de nuvens
          </h2>
          <p className="mt-1 text-sm text-slate-500">
            Visualização local da cobertura de nuvens.
          </p>
        </div>
        <div className="rounded-full bg-emerald-50 px-3 py-1 text-xs font-semibold text-emerald-700">
          Nebulosidade {normalizedCloudiness}%
        </div>
      </div>

      <div className="mt-6 grid gap-6 lg:grid-cols-[minmax(0,280px)_1fr]">
        <div className="flex items-center justify-center">
          <div className="relative aspect-square w-64 overflow-hidden rounded-full sm:w-72">
            <div
              className="absolute inset-0 rounded-full"
              style={{
                background:
                  "radial-gradient(circle at center, rgba(20,184,166,0.35) 0%, rgba(15,118,110,0.35) 38%, rgba(8,47,73,0.95) 100%)",
              }}
            />
            <div
              className="absolute inset-0 rounded-full opacity-70"
              style={{
                background:
                  "repeating-radial-gradient(circle at center, rgba(45,212,191,0.35) 0 1px, transparent 1px 22px)",
              }}
            />
            <div className="absolute inset-0 rounded-full border border-emerald-100/40" />
            <div className="absolute left-1/2 top-2 h-[calc(100%-16px)] w-px -translate-x-1/2 bg-emerald-200/40" />
            <div className="absolute left-2 top-1/2 h-px w-[calc(100%-16px)] -translate-y-1/2 bg-emerald-200/40" />
            <div
              className="radar-sweep absolute inset-0 rounded-full opacity-80"
              style={{
                background:
                  "conic-gradient(from 0deg, rgba(20,184,166,0) 0deg, rgba(20,184,166,0.45) 35deg, rgba(20,184,166,0) 70deg, transparent 360deg)",
              }}
            />

            {visibleClouds.map((cloud) => (
              <div
                key={cloud.id}
                className="absolute -translate-x-1/2 -translate-y-1/2"
                style={{ left: `${cloud.x}%`, top: `${cloud.y}%` }}
              >
                <div
                  className={`${cloud.drift} text-cyan-50 drop-shadow-[0_10px_16px_rgba(16,185,129,0.35)]`}
                  style={{
                    width: `${cloud.size}px`,
                    opacity: cloud.baseOpacity * opacityBoost,
                    animationDelay: cloud.delay,
                  }}
                >
                  <CloudIcon className="h-full w-full" />
                </div>
              </div>
            ))}

            <div className="absolute inset-0 rounded-full border border-emerald-200/40 shadow-[inset_0_0_30px_rgba(6,78,59,0.45)]" />
          </div>
        </div>

        <div className="space-y-4 text-sm text-slate-600">
          <div className="rounded-xl border border-emerald-100 bg-emerald-50/50 p-4">
            <p className="text-xs font-semibold uppercase tracking-[0.2em] text-emerald-600">
              Condição atual
            </p>
            <p className="mt-2 text-lg font-semibold text-slate-900">
              {cloudLabel(normalizedCloudiness)}
            </p>
            <div className="mt-3 h-2 w-full rounded-full bg-emerald-100">
              <div
                className="h-full rounded-full bg-emerald-500"
                style={{ width: `${normalizedCloudiness}%` }}
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div className="rounded-xl border border-slate-200/70 bg-white/80 p-3">
              <p className="text-xs text-slate-500">Cobertura</p>
              <p className="mt-1 font-semibold text-slate-900">
                {normalizedCloudiness}%
              </p>
            </div>
            <div className="rounded-xl border border-slate-200/70 bg-white/80 p-3">
              <p className="text-xs text-slate-500">Qualidade do céu</p>
              <p className="mt-1 font-semibold text-slate-900">
                {cloudLabel(normalizedCloudiness)}
              </p>
            </div>
          </div>

          {updatedAt && (
            <p className="text-xs text-slate-500">
              Atualizado em {formatDate(updatedAt)} as {formatHour(updatedAt)}.
            </p>
          )}
        </div>
      </div>
    </div>
  );
}
