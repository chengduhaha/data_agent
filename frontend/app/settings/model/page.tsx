"use client";

import { useEffect, useState } from "react";
import { apiGet, apiSend } from "@/lib/api";
import {
  applyCatalogModel,
  type ModelCatalog,
  type UserConfig,
} from "@/lib/modelConfig";

type Provider = {
  id: string;
  name: string;
  kind: string;
  default_base_url?: string | null;
  models: string[];
  requires_api_key: boolean;
};

type Config = UserConfig;

export default function ModelSettingsPage() {
  const [providers, setProviders] = useState<Provider[]>([]);
  const [catalog, setCatalog] = useState<ModelCatalog | null>(null);
  const [cfg, setCfg] = useState<Config | null>(null);
  const [apiKey, setApiKey] = useState("");
  const [status, setStatus] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    void (async () => {
      try {
        const [p, c, cat] = await Promise.all([
          apiGet<{ providers: Provider[] }>("/api/providers"),
          apiGet<Config>("/api/config"),
          apiGet<ModelCatalog>("/api/model-catalog"),
        ]);
        setProviders(p.providers);
        setCatalog(cat);
        setCfg(c);
      } catch (e) {
        setError((e as Error).message);
      }
    })();
  }, []);

  const selected = providers.find((p) => p.id === cfg?.model.provider);
  const isSynnex = Boolean(catalog && cfg?.model.provider === catalog.provider_id);
  const selectedCatalog = catalog?.models.find((m) => m.id === cfg?.model.model);

  async function save() {
    if (!cfg) return;
    setStatus(null);
    setError(null);
    const body = {
      ...cfg,
      model: {
        ...cfg.model,
        api_key: apiKey || cfg.model.api_key,
      },
    };
    try {
      const saved = await apiSend<Config>("/api/config", "PUT", body);
      setCfg(saved);
      setApiKey("");
      setStatus("Saved.");
    } catch (e) {
      setError((e as Error).message);
    }
  }

  if (!cfg) {
    return <p className="text-sm text-ink-500">{error || "Loading…"}</p>;
  }

  return (
    <div className="mx-auto max-w-2xl space-y-6 animate-fade-up">
      <div>
        <h1 className="font-display text-2xl text-ink-900">Model & providers</h1>
        <p className="mt-1 text-sm text-ink-500">
          Synnex AI Gateway presets are ready out of the box — or pick another provider.
        </p>
      </div>

      {catalog && (
        <div className="rounded-lg border border-ink-200 bg-ink-50/60 p-4 space-y-3">
          <div>
            <p className="text-sm font-medium text-ink-800">{catalog.provider_name}</p>
            <p className="mt-0.5 text-xs text-ink-500">{catalog.description}</p>
          </div>
          <div>
            <label className="label">Gateway model</label>
            <select
              className="input"
              value={isSynnex ? cfg.model.model : ""}
              onChange={(e) => {
                const id = e.target.value;
                if (!id) return;
                setCfg(applyCatalogModel(cfg, catalog, id));
                setApiKey("");
              }}
            >
              {!isSynnex && <option value="">Select a Synnex preset…</option>}
              {catalog.models.map((m) => (
                <option key={m.id} value={m.id}>
                  {m.display_name}
                </option>
              ))}
            </select>
          </div>
          {isSynnex && selectedCatalog && (
            <p className="font-mono text-[11px] text-ink-400 break-all">
              {selectedCatalog.provider_type}
              {selectedCatalog.api_version ? ` · api-version=${selectedCatalog.api_version}` : ""}
              {" · "}
              {selectedCatalog.api_base}
            </p>
          )}
        </div>
      )}

      <div>
        <label className="label">Provider</label>
        <select
          className="input"
          value={cfg.model.provider}
          onChange={(e) => {
            const id = e.target.value;
            if (catalog && id === catalog.provider_id) {
              setCfg(applyCatalogModel(cfg, catalog, catalog.default_model));
              setApiKey("");
              return;
            }
            const p = providers.find((x) => x.id === id);
            setCfg({
              ...cfg,
              model: {
                ...cfg.model,
                provider: id,
                base_url: p?.default_base_url || "",
                model: p?.models[0] || "",
                api_version: "",
                api_model: "",
              },
            });
          }}
        >
          <option value="">Select…</option>
          {providers.map((p) => (
            <option key={p.id} value={p.id}>
              {p.name}
            </option>
          ))}
        </select>
      </div>

      {!isSynnex && (
        <div>
          <label className="label">Model</label>
          {selected && selected.models.length > 0 ? (
            <select
              className="input"
              value={cfg.model.model}
              onChange={(e) =>
                setCfg({ ...cfg, model: { ...cfg.model, model: e.target.value } })
              }
            >
              {selected.models.map((m) => (
                <option key={m} value={m}>
                  {m}
                </option>
              ))}
            </select>
          ) : (
            <input
              className="input"
              value={cfg.model.model}
              onChange={(e) =>
                setCfg({ ...cfg, model: { ...cfg.model, model: e.target.value } })
              }
              placeholder="model id"
            />
          )}
        </div>
      )}

      {(selected?.kind === "openai_compatible" || cfg.model.provider === "deepseek") &&
        !isSynnex && (
          <div>
            <label className="label">Base URL</label>
            <input
              className="input font-mono text-xs"
              value={cfg.model.base_url}
              onChange={(e) =>
                setCfg({ ...cfg, model: { ...cfg.model, base_url: e.target.value } })
              }
              placeholder="https://…"
            />
          </div>
        )}

      <div>
        <label className="label">
          API key {cfg.model.api_key_set ? "(set)" : ""}
        </label>
        <input
          className="input font-mono text-xs"
          type="password"
          value={apiKey}
          onChange={(e) => setApiKey(e.target.value)}
          placeholder={cfg.model.api_key_set ? "•••• leave blank to keep" : "sk-…"}
        />
      </div>

      <div>
        <label className="label">Temperature</label>
        <input
          className="input"
          type="number"
          step="0.1"
          min={0}
          max={2}
          value={cfg.model.temperature}
          onChange={(e) =>
            setCfg({
              ...cfg,
              model: { ...cfg.model, temperature: Number(e.target.value) },
            })
          }
        />
      </div>

      <div>
        <label className="label">System prompt</label>
        <textarea
          className="input min-h-[100px]"
          value={cfg.system_prompt}
          onChange={(e) => setCfg({ ...cfg, system_prompt: e.target.value })}
        />
      </div>

      <div className="flex flex-wrap gap-4">
        <label className="flex items-center gap-2 text-sm">
          <input
            type="checkbox"
            checked={cfg.approve_writes}
            onChange={(e) => setCfg({ ...cfg, approve_writes: e.target.checked })}
          />
          Approve file writes
        </label>
        <label className="flex items-center gap-2 text-sm">
          <input
            type="checkbox"
            checked={cfg.approve_execute}
            onChange={(e) => setCfg({ ...cfg, approve_execute: e.target.checked })}
          />
          Approve shell execute
        </label>
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
