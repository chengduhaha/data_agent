"use client";

import { useEffect, useState } from "react";
import { apiGet, apiSend } from "@/lib/api";

type SubAgent = {
  name: string;
  description: string;
  system_prompt: string;
  tools?: string[];
  model?: string | null;
  skills?: string[];
};

export default function SubagentsSettingsPage() {
  const [items, setItems] = useState<SubAgent[]>([]);
  const [status, setStatus] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    void (async () => {
      try {
        const data = await apiGet<{ subagents: SubAgent[] }>("/api/subagents");
        setItems(data.subagents || []);
      } catch (e) {
        setError((e as Error).message);
      }
    })();
  }, []);

  function update(i: number, patch: Partial<SubAgent>) {
    setItems((prev) => prev.map((s, idx) => (idx === i ? { ...s, ...patch } : s)));
  }

  async function save() {
    setStatus(null);
    setError(null);
    try {
      await apiSend("/api/subagents", "PUT", { subagents: items });
      setStatus("Saved.");
    } catch (e) {
      setError((e as Error).message);
    }
  }

  return (
    <div className="mx-auto max-w-3xl space-y-6 animate-fade-up">
      <div className="flex items-end justify-between gap-3">
        <div>
          <h1 className="font-display text-2xl text-ink-900">Subagents</h1>
          <p className="mt-1 text-sm text-ink-500">
            Declarative specialists the main agent can call via the <code className="font-mono text-xs">task</code> tool.
          </p>
        </div>
        <button
          type="button"
          className="btn-ghost"
          onClick={() =>
            setItems((prev) => [
              ...prev,
              {
                name: `agent-${prev.length + 1}`,
                description: "",
                system_prompt: "You are a helpful specialist.",
              },
            ])
          }
        >
          Add
        </button>
      </div>
      <div className="space-y-4">
        {items.map((s, i) => (
          <div key={i} className="rounded-2xl border border-ink-200/70 bg-white/60 p-4">
            <div className="grid gap-3 md:grid-cols-2">
              <div>
                <label className="label">Name</label>
                <input
                  className="input"
                  value={s.name}
                  onChange={(e) => update(i, { name: e.target.value })}
                />
              </div>
              <div>
                <label className="label">Description</label>
                <input
                  className="input"
                  value={s.description}
                  onChange={(e) => update(i, { description: e.target.value })}
                />
              </div>
            </div>
            <div className="mt-3">
              <label className="label">System prompt</label>
              <textarea
                className="input min-h-[90px]"
                value={s.system_prompt}
                onChange={(e) => update(i, { system_prompt: e.target.value })}
              />
            </div>
            <button
              type="button"
              className="btn-ghost mt-3 !py-1 text-xs"
              onClick={() => setItems((prev) => prev.filter((_, idx) => idx !== i))}
            >
              Remove
            </button>
          </div>
        ))}
      </div>
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
