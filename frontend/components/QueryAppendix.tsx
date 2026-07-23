"use client";

import { useState } from "react";
import type { QueryAppendixItem } from "@/lib/api";

/** Collapsed-by-default appendix for executed queries — never inline in the narrative. */
export function QueryAppendix({ queries }: { queries: QueryAppendixItem[] }) {
  const [open, setOpen] = useState(false);
  if (!queries.length) return null;

  return (
    <div className="mt-3 overflow-hidden rounded-xl border border-ink-200/60 bg-ink-50/50" data-testid="query-appendix">
      <button
        type="button"
        className="flex w-full items-center justify-between gap-2 px-3 py-1.5 text-left text-xs font-medium text-ink-600 transition hover:bg-white/50"
        onClick={() => setOpen((v) => !v)}
      >
        <span>
          Query validation ({queries.length} {queries.length === 1 ? "query" : "queries"})
        </span>
        <span className="text-[10px] text-ink-400">{open ? "▾" : "▸"}</span>
      </button>
      {open && (
        <div className="space-y-2 border-t border-ink-200/50 px-3 py-2">
          {queries.map((q, i) => (
            <div key={i}>
              {queries.length > 1 && (
                <p className="mb-1 text-[10px] uppercase tracking-wide text-ink-400">
                  Query {i + 1} · {q.tool}
                </p>
              )}
              <pre className="max-h-72 overflow-auto rounded-lg bg-ink-900/90 px-3 py-2 font-mono text-[11px] text-ink-50">
                {q.sql}
              </pre>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
