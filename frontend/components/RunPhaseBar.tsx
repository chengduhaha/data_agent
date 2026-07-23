"use client";

import type { BudgetPayload } from "@/lib/api";

const PHASE_LABEL: Record<string, string> = {
  research: "Research",
  execute: "Execute",
  synthesize: "Synthesize",
};

const PHASE_ORDER = ["research", "execute", "synthesize"];

export function RunPhaseBar({ budget }: { budget: BudgetPayload | null }) {
  const phase = budget?.run_phase;
  if (!phase) return null;
  const activeIdx = PHASE_ORDER.indexOf(phase);

  return (
    <div className="mb-2 flex items-center gap-1.5 text-[11px] text-ink-500">
      {PHASE_ORDER.map((p, i) => (
        <span key={p} className="flex items-center gap-1.5">
          <span
            className={`rounded-full px-2 py-0.5 font-medium transition ${
              i === activeIdx
                ? "bg-accent-soft text-accent-strong"
                : i < activeIdx
                  ? "bg-ink-100 text-ink-400"
                  : "text-ink-300"
            }`}
          >
            {PHASE_LABEL[p]}
          </span>
          {i < PHASE_ORDER.length - 1 && <span className="text-ink-200">→</span>}
        </span>
      ))}
    </div>
  );
}
