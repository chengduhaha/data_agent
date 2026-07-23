"use client";

import type { BudgetPayload } from "@/lib/api";
import { RunPhaseBar } from "./RunPhaseBar";
import { shouldShowBudgetBar } from "@/lib/budgetBar";

export type { BudgetPayload };

export function ContextBudgetBar({
  budget,
  threadId = null,
  streaming = false,
}: {
  budget: BudgetPayload | null;
  threadId?: string | null;
  streaming?: boolean;
}) {
  if (!budget || !shouldShowBudgetBar(budget, { threadId, streaming })) return null;

  const used = budget.steps_used ?? 0;
  const limit = budget.steps_limit ?? 1;
  const pct = Math.min(100, Math.round((used / limit) * 100));
  const phase = budget.phase ?? "ok";

  const barColor =
    phase === "exhausted"
      ? "bg-red-500"
      : phase === "warn"
        ? "bg-amber-500"
        : "bg-accent";

  return (
    <div className="mb-2 rounded-xl border border-ink-200/80 bg-white/80 px-3 py-2 text-xs text-ink-600" data-testid="context-budget-bar">
      <RunPhaseBar budget={budget} />
      <div className="mb-1 flex items-center justify-between gap-2">
        <span className="font-medium text-ink-700">Agent steps</span>
        <span className="tabular-nums text-ink-500">
          {used} / {limit}
          {budget.sql_queries_used ? ` · ${budget.sql_queries_used} queries` : ""}
          {budget.run_segment != null ? ` · seg ${budget.run_segment}` : ""}
        </span>
      </div>
      <div className="h-1.5 overflow-hidden rounded-full bg-ink-100">
        <div
          className={`h-full transition-all duration-300 ${barColor}`}
          style={{ width: `${pct}%` }}
        />
      </div>
      {phase === "warn" && (
        <p className="mt-1 text-amber-700">
          Step budget running low — the agent will prioritize finishing your answer.
        </p>
      )}
      {phase === "exhausted" && (
        <p className="mt-1 text-red-700">
          Step budget reached — wrap-up or Continue may be required.
        </p>
      )}
    </div>
  );
}
