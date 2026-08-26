"use client";

import { useEffect, useState } from "react";
import { apiGet } from "@/lib/api";

export default function MetricsSettingsPage() {
  const [text, setText] = useState("Loading…");
  const [error, setError] = useState<string | null>(null);

  async function refresh() {
    try {
      const res = await fetch("/api/metrics", { credentials: "include", cache: "no-store" });
      if (!res.ok) {
        const data = await apiGet<string>("/api/metrics");
        setText(String(data || ""));
        return;
      }
      setText(await res.text());
      setError(null);
    } catch (e) {
      setError((e as Error).message);
    }
  }

  useEffect(() => {
    void refresh();
    const id = window.setInterval(() => void refresh(), 30_000);
    return () => window.clearInterval(id);
  }, []);

  return (
    <div className="mx-auto max-w-3xl space-y-6 animate-fade-up">
      <div>
        <h1 className="font-display text-2xl text-ink-900">Metrics</h1>
        <p className="mt-1 text-sm text-ink-500">
          Harness counters (auto-refresh every 30s).
        </p>
      </div>
      {error ? <p className="text-sm text-red-600">{error}</p> : null}
      <pre className="overflow-auto rounded-2xl border border-ink-200 bg-white/60 p-4 text-xs">
        {text || "(no samples yet)"}
      </pre>
    </div>
  );
}
