"use client";

import { useEffect, useState } from "react";
import { apiGet, apiSend } from "@/lib/api";

export default function RulesSettingsPage() {
  const [content, setContent] = useState("");
  const [status, setStatus] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    void (async () => {
      try {
        const data = await apiGet<{ content: string }>("/api/rules");
        setContent(data.content || "");
      } catch (e) {
        setError((e as Error).message);
      }
    })();
  }, []);

  async function save() {
    setStatus(null);
    setError(null);
    try {
      await apiSend("/api/rules", "PUT", { content });
      setStatus("Saved.");
    } catch (e) {
      setError((e as Error).message);
    }
  }

  return (
    <div className="mx-auto max-w-3xl space-y-6 animate-fade-up">
      <div>
        <h1 className="font-display text-2xl text-ink-900">Rules</h1>
        <p className="mt-1 text-sm text-ink-500">
          Persistent memory loaded from <code className="font-mono text-xs">AGENTS.md</code>.
        </p>
      </div>
      <textarea
        className="input min-h-[420px] font-mono text-xs"
        value={content}
        onChange={(e) => setContent(e.target.value)}
        spellCheck={false}
      />
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
