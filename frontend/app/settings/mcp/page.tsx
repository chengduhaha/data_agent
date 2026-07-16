"use client";

import { useEffect, useState } from "react";
import { apiGet, apiSend } from "@/lib/api";

type Server = {
  transport: "stdio" | "streamable_http" | "sse";
  command?: string | null;
  args?: string[];
  env?: Record<string, string>;
  url?: string | null;
  headers?: Record<string, string>;
  enabled?: boolean;
};

type OrgServer = {
  name: string;
  enabled: boolean;
  managed: boolean;
  transport?: string;
  url?: string | null;
  description?: string;
};

export default function McpSettingsPage() {
  const [raw, setRaw] = useState('{\n  "mcpServers": {}\n}');
  const [orgServers, setOrgServers] = useState<OrgServer[]>([]);
  const [status, setStatus] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [tools, setTools] = useState<{ name: string; description: string }[]>([]);

  useEffect(() => {
    void (async () => {
      try {
        const data = await apiGet<{
          mcpServers: Record<string, Server>;
          org_servers?: OrgServer[];
        }>("/api/mcp");
        const { org_servers: org, ...rest } = data;
        setOrgServers(org || []);
        setRaw(JSON.stringify(rest, null, 2));
        const t = await apiGet<{ tools: { name: string; description: string }[] }>(
          "/api/mcp/tools"
        );
        setTools(t.tools || []);
      } catch (e) {
        setError((e as Error).message);
      }
    })();
  }, []);

  async function save() {
    setStatus(null);
    setError(null);
    try {
      const parsed = JSON.parse(raw);
      await apiSend("/api/mcp", "PUT", parsed);
      const t = await apiGet<{ tools: { name: string; description: string }[] }>(
        "/api/mcp/tools"
      );
      setTools(t.tools || []);
      setStatus("Saved.");
    } catch (e) {
      setError((e as Error).message);
    }
  }

  return (
    <div className="mx-auto max-w-3xl space-y-6 animate-fade-up">
      <div>
        <h1 className="font-display text-2xl text-ink-900">MCP servers</h1>
        <p className="mt-1 text-sm text-ink-500">
          Organization MCP is managed server-side. Configure personal MCP servers below.
        </p>
      </div>

      {orgServers.length > 0 && (
        <section className="panel space-y-2 p-4">
          <h2 className="text-sm font-semibold text-ink-800">Organization (shared)</h2>
          <ul className="space-y-2">
            {orgServers.map((s) => (
              <li
                key={s.name}
                className="rounded-xl border border-teal-100 bg-teal-50/50 px-3 py-2 text-sm"
              >
                <p className="font-medium text-ink-900">{s.name}</p>
                <p className="text-xs text-ink-500">{s.description}</p>
                {s.url && (
                  <p className="mt-1 break-all font-mono text-[11px] text-ink-600">{s.url}</p>
                )}
              </li>
            ))}
          </ul>
        </section>
      )}

      <section>
        <h2 className="mb-2 text-sm font-semibold text-ink-800">Personal MCP</h2>
        <textarea
          className="input min-h-[240px] font-mono text-xs"
          value={raw}
          onChange={(e) => setRaw(e.target.value)}
          spellCheck={false}
        />
      </section>

      <div className="flex items-center gap-3">
        <button type="button" className="btn-primary" onClick={() => void save()}>
          Save
        </button>
        {status && <span className="text-sm text-accent">{status}</span>}
        {error && <span className="text-sm text-red-600">{error}</span>}
      </div>
      <div>
        <h2 className="text-sm font-semibold text-ink-800">Loaded MCP tools</h2>
        <ul className="mt-2 space-y-1">
          {tools.length === 0 && (
            <li className="text-sm text-ink-400">None connected</li>
          )}
          {tools.map((t) => (
            <li key={t.name} className="font-mono text-xs text-ink-600">
              {t.name}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
