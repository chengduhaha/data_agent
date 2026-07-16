"use client";

import { useEffect, useState } from "react";
import { apiGet, apiSend } from "@/lib/api";

type Tool = {
  name: string;
  description: string;
  source: string;
  enabled: boolean;
};

export default function ToolsSettingsPage() {
  const [tools, setTools] = useState<Tool[]>([]);
  const [enabled, setEnabled] = useState<Record<string, boolean>>({});
  const [status, setStatus] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    void (async () => {
      try {
        const data = await apiGet<{
          tools: Tool[];
          enabled_tools: Record<string, boolean>;
        }>("/api/tools");
        setTools(data.tools || []);
        setEnabled(data.enabled_tools || {});
      } catch (e) {
        setError((e as Error).message);
      }
    })();
  }, []);

  async function save() {
    setStatus(null);
    setError(null);
    try {
      await apiSend("/api/tools", "PUT", { enabled_tools: enabled });
      setStatus("Saved.");
    } catch (e) {
      setError((e as Error).message);
    }
  }

  return (
    <div className="mx-auto max-w-3xl space-y-6 animate-fade-up">
      <div>
        <h1 className="font-display text-2xl text-ink-900">Tools</h1>
        <p className="mt-1 text-sm text-ink-500">
          Toggle optional built-in tools. Deepagents filesystem/shell tools are always available
          (gated by HITL settings).
        </p>
      </div>
      <ul className="divide-y divide-ink-100 rounded-2xl border border-ink-200/70 bg-white/60">
        {tools.map((t) => (
          <li key={`${t.source}-${t.name}`} className="flex items-start justify-between gap-3 px-4 py-3">
            <div>
              <p className="font-mono text-sm text-ink-900">{t.name}</p>
              <p className="text-xs text-ink-500">{t.description}</p>
              <p className="mt-1 text-[10px] uppercase tracking-wide text-ink-400">
                {t.source}
              </p>
            </div>
            {t.source === "builtin" ? (
              <input
                type="checkbox"
                checked={enabled[t.name] !== false}
                onChange={(e) =>
                  setEnabled((prev) => ({ ...prev, [t.name]: e.target.checked }))
                }
              />
            ) : (
              <span className="text-xs text-ink-400">always on</span>
            )}
          </li>
        ))}
      </ul>
      <div className="flex items-center gap-3">
        <button type="button" className="btn-primary" onClick={() => void save()}>
          Save
        </button>
        {status && <span className="text-sm text-accent">{status}</span>}
        {error && <span className="text-sm text-red-600">{error}</span>}
      </div>
    </div>
  );
}
