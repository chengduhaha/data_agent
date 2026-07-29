"use client";

import { useCallback, useEffect, useState } from "react";
import { apiGet, apiSend } from "@/lib/api";
import {
  catalogLabel,
  type ModelCatalog,
  type UserModelConfig,
} from "@/lib/modelConfig";

type Props = {
  disabled?: boolean;
};

export function ModelSwitcher({ disabled }: Props) {
  const [catalog, setCatalog] = useState<ModelCatalog | null>(null);
  const [modelCfg, setModelCfg] = useState<UserModelConfig | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const reload = useCallback(async () => {
    try {
      const [cat, res] = await Promise.all([
        apiGet<ModelCatalog>("/api/model-catalog"),
        apiGet<{ model: UserModelConfig }>("/api/model"),
      ]);
      setCatalog(cat);
      setModelCfg(res.model);
      setError(null);
    } catch (e) {
      setError((e as Error).message || "Failed to load models");
    }
  }, []);

  useEffect(() => {
    void reload();
  }, [reload]);

  const currentId = modelCfg?.model || "";
  const isSynnex = Boolean(catalog && modelCfg?.provider === catalog.provider_id);
  const inCatalog = Boolean(catalog?.models?.some((m) => m.id === currentId));

  async function onSelect(modelId: string) {
    if (!modelCfg || !catalog || !modelId || (modelId === currentId && isSynnex)) return;
    setBusy(true);
    setError(null);
    setModelCfg({ ...modelCfg, model: modelId, provider: catalog.provider_id });
    try {
      const saved = await apiSend<{ model: UserModelConfig }>("/api/model", "PUT", {
        model: modelId,
      });
      setModelCfg(saved.model);
    } catch (e) {
      setError((e as Error).message || "Failed to switch model");
      await reload();
    } finally {
      setBusy(false);
    }
  }

  if (!catalog || !modelCfg) {
    return (
      <div className="mt-2 flex items-center gap-2 text-[11px] text-ink-400">
        {error ? <span className="text-red-600">{error}</span> : <span>Loading models…</span>}
      </div>
    );
  }

  return (
    <div className="mt-2 flex min-w-0 items-center gap-2">
      <label htmlFor="chat-model-switcher" className="sr-only">
        Model
      </label>
      <div className="relative inline-flex max-w-full items-center">
        <select
          id="chat-model-switcher"
          className="max-w-[min(100%,280px)] cursor-pointer appearance-none rounded-lg border border-ink-200/70 bg-white/60 py-1 pl-2.5 pr-7 text-xs font-medium text-ink-700 outline-none transition hover:border-ink-300 hover:bg-white hover:text-ink-900 focus:border-accent focus:ring-1 focus:ring-accent/20 disabled:cursor-not-allowed disabled:opacity-60"
          value={isSynnex && inCatalog ? currentId : isSynnex ? currentId : ""}
          disabled={disabled || busy}
          onChange={(e) => void onSelect(e.target.value)}
          title={catalogLabel(catalog, currentId)}
        >
          {!isSynnex && (
            <option value="">
              {modelCfg.provider}:{currentId || "select model…"}
            </option>
          )}
          {isSynnex && !inCatalog && currentId && (
            <option value={currentId}>{currentId}</option>
          )}
          {catalog.models.map((m) => (
            <option key={m.id} value={m.id}>
              {m.display_name}
            </option>
          ))}
        </select>
        <svg
          aria-hidden
          viewBox="0 0 16 16"
          className="pointer-events-none absolute right-2 h-3 w-3 text-ink-400"
          fill="none"
          stroke="currentColor"
          strokeWidth="1.75"
        >
          <path d="M4 6l4 4 4-4" strokeLinecap="round" strokeLinejoin="round" />
        </svg>
      </div>
      {busy && <span className="text-[11px] text-ink-400">Saving…</span>}
      {error && (
        <span className="truncate text-[11px] text-red-600" title={error}>
          {error}
        </span>
      )}
    </div>
  );
}
