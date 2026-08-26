"use client";

import { useEffect, useState } from "react";
import { apiGet, apiSend } from "@/lib/api";

type PackSummary = {
  name: string;
  version: string;
  sector: string;
  display_name?: string;
};

export default function PacksSettingsPage() {
  const [installed, setInstalled] = useState(false);
  const [message, setMessage] = useState<string | null>(null);
  const [packs, setPacks] = useState<PackSummary[]>([]);
  const [current, setCurrent] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function load() {
    try {
      const data = await apiGet<{
        installed: boolean;
        packs: PackSummary[];
        current?: string | null;
        message?: string;
      }>("/api/packs");
      setInstalled(data.installed);
      setPacks(data.packs || []);
      setCurrent(data.current || null);
      setMessage(data.message || null);
    } catch (e) {
      setError((e as Error).message);
    }
  }

  useEffect(() => {
    void load();
  }, []);

  async function activate(name: string) {
    setError(null);
    try {
      await apiSend("/api/packs/activate", "POST", { name });
      await load();
    } catch (e) {
      setError((e as Error).message);
    }
  }

  if (!installed) {
    return (
      <div className="mx-auto max-w-3xl space-y-4 animate-fade-up">
        <h1 className="font-display text-2xl text-ink-900">Packs</h1>
        <p className="text-sm text-ink-500">
          {message || "Pack Framework not installed"}
        </p>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-3xl space-y-6 animate-fade-up">
      <div>
        <h1 className="font-display text-2xl text-ink-900">Packs</h1>
        <p className="mt-1 text-sm text-ink-500">
          Installed sector packs. Current: {current || "none"}
        </p>
      </div>
      <ul className="divide-y divide-ink-100 rounded-2xl border border-ink-200/70 bg-white/60">
        {packs.map((pack) => (
          <li key={pack.name} className="flex items-center justify-between px-4 py-3">
            <div>
              <p className="text-sm font-medium text-ink-900">
                {pack.display_name || pack.name}
              </p>
              <p className="text-xs text-ink-500">
                {pack.name} · v{pack.version} · {pack.sector}
              </p>
            </div>
            <button type="button" className="btn-primary" onClick={() => void activate(pack.name)}>
              Activate
            </button>
          </li>
        ))}
      </ul>
      {error ? <p className="text-sm text-red-600">{error}</p> : null}
    </div>
  );
}
