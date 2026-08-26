"use client";

import { useEffect, useState } from "react";
import { apiGet, apiSend } from "@/lib/api";

type GovernanceConfig = {
  budget_warn_threshold: number;
  segment_max_per_thread: number;
  evidence_max_items: number;
  enable_dw_governance: boolean;
  enable_completeness_enhanced: boolean;
  enable_pack_framework: boolean;
  forward_instruction_language: string;
  budget_merge_strategy: string;
};

export default function GovernanceSettingsPage() {
  const [cfg, setCfg] = useState<GovernanceConfig | null>(null);
  const [status, setStatus] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    void (async () => {
      try {
        const data = await apiGet<{ config: GovernanceConfig }>("/api/governance");
        setCfg(data.config);
      } catch (e) {
        setError((e as Error).message);
      }
    })();
  }, []);

  async function save() {
    if (!cfg) return;
    setStatus(null);
    setError(null);
    try {
      const data = await apiSend<{ config: GovernanceConfig }>("/api/governance", "PUT", cfg);
      setCfg(data.config);
      setStatus("Saved. Changes apply to new agent runs immediately.");
    } catch (e) {
      setError((e as Error).message);
    }
  }

  if (!cfg) {
    return <p className="text-sm text-ink-500">{error || "Loading…"}</p>;
  }

  return (
    <div className="mx-auto max-w-3xl space-y-6 animate-fade-up">
      <div>
        <h1 className="font-display text-2xl text-ink-900">Governance</h1>
        <p className="mt-1 text-sm text-ink-500">
          Harness budgets, segment retention, and optional sub-library switches.
        </p>
      </div>
      <label className="block text-sm">
        Budget warn threshold
        <input
          className="mt-1 w-full rounded-xl border border-ink-200 px-3 py-2"
          type="number"
          step="0.05"
          min={0}
          max={1}
          value={cfg.budget_warn_threshold}
          onChange={(e) =>
            setCfg({ ...cfg, budget_warn_threshold: Number(e.target.value) })
          }
        />
      </label>
      <label className="block text-sm">
        Segments kept per thread
        <input
          className="mt-1 w-full rounded-xl border border-ink-200 px-3 py-2"
          type="number"
          min={1}
          value={cfg.segment_max_per_thread}
          onChange={(e) =>
            setCfg({ ...cfg, segment_max_per_thread: Number(e.target.value) })
          }
        />
      </label>
      <label className="flex items-center gap-2 text-sm">
        <input
          type="checkbox"
          checked={cfg.enable_dw_governance}
          onChange={(e) => setCfg({ ...cfg, enable_dw_governance: e.target.checked })}
        />
        Enable DW governance
      </label>
      <label className="flex items-center gap-2 text-sm">
        <input
          type="checkbox"
          checked={cfg.enable_completeness_enhanced}
          onChange={(e) =>
            setCfg({ ...cfg, enable_completeness_enhanced: e.target.checked })
          }
        />
        Enable enhanced completeness
      </label>
      <label className="flex items-center gap-2 text-sm">
        <input
          type="checkbox"
          checked={cfg.enable_pack_framework}
          onChange={(e) => setCfg({ ...cfg, enable_pack_framework: e.target.checked })}
        />
        Enable pack framework
      </label>
      <button type="button" className="btn-primary" onClick={() => void save()}>
        Save
      </button>
      {status ? <p className="text-sm text-ink-500">{status}</p> : null}
      {error ? <p className="text-sm text-red-600">{error}</p> : null}
    </div>
  );
}
