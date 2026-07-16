"use client";

export type BudgetPayload = {
  steps_used?: number;
  steps_limit?: number;
  steps_warn_at?: number;
  phase?: "ok" | "warn" | "exhausted";
  run_segment?: number;
  thread_id?: string;
};

export function ContextBudgetBar({ budget }: { budget: BudgetPayload | null }) {
  if (!budget || budget.steps_limit == null) return null;

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
    <div className="mb-2 rounded-xl border border-ink-200/80 bg-white/80 px-3 py-2 text-xs text-ink-600">
      <div className="mb-1 flex items-center justify-between gap-2">
        <span className="font-medium text-ink-700">Agent steps</span>
        <span className="tabular-nums text-ink-500">
          {used} / {limit}
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
