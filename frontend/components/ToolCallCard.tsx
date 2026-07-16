"use client";

import { useState } from "react";
import type { ToolCall } from "@/lib/api";
import { toolStepDetail, toolStepLabel } from "@/lib/toolLabels";

function isVerticaQueryTool(tool: string): boolean {
  const name = (tool || "").toLowerCase();
  return (
    name === "run_query_safely" ||
    name === "execute_query_paginated" ||
    name === "execute_query_stream" ||
    name.includes("run_query") ||
    name.startsWith("execute_query")
  );
}

function extractQuery(input: unknown): string | null {
  if (!input || typeof input !== "object" || Array.isArray(input)) return null;
  const rec = input as Record<string, unknown>;
  const query = rec.query ?? rec.sql;
  return typeof query === "string" && query.trim() ? query : null;
}

export function ToolCallCard({ tool }: { tool: ToolCall }) {
  const [open, setOpen] = useState(false);
  const label = toolStepLabel(tool.tool, tool.input);
  const detail = toolStepDetail(tool.input);
  const hasBody = tool.input !== undefined || tool.output !== undefined;
  const verticaQuery = isVerticaQueryTool(tool.tool);
  const fullSql = verticaQuery ? extractQuery(tool.input) : null;
  const inputMaxHeight = verticaQuery ? "max-h-96" : "max-h-28";
  const outputMaxHeight = verticaQuery ? "max-h-96" : "max-h-40";

  return (
    <div className="mt-1.5 overflow-hidden rounded-xl border border-ink-200/70 bg-ink-50/60 animate-fade-up">
      <button
        type="button"
        className="flex w-full items-center justify-between gap-2 px-3 py-1.5 text-left transition hover:bg-white/50"
        onClick={() => hasBody && setOpen((v) => !v)}
        disabled={!hasBody}
      >
        <div className="flex min-w-0 items-center gap-2">
          <StatusDot status={tool.status} />
          <span className="truncate text-xs font-medium text-ink-800">{label}</span>
        </div>
        <div className="flex shrink-0 items-center gap-2">
          <span className="text-[10px] uppercase tracking-wide text-ink-400">
            {tool.status === "running" ? "running" : tool.status}
          </span>
          {hasBody && (
            <span className="text-[10px] text-ink-400">{open ? "▾" : "▸"}</span>
          )}
        </div>
      </button>
      {!open && detail && tool.status === "running" && (
        <p className="truncate border-t border-ink-200/40 px-3 py-1 font-mono text-[10px] text-ink-500">
          {detail}
        </p>
      )}
      {open && (
        <div className="border-t border-ink-200/50">
          {tool.input !== undefined && (
            <pre
              className={`${inputMaxHeight} overflow-auto border-b border-ink-200/40 px-3 py-2 font-mono text-[11px] text-ink-600`}
            >
              {fullSql ?? format(tool.input)}
            </pre>
          )}
          {tool.output !== undefined && (
            <pre
              className={`${outputMaxHeight} overflow-auto px-3 py-2 font-mono text-[11px] text-ink-700`}
            >
              {format(tool.output)}
            </pre>
          )}
        </div>
      )}
    </div>
  );
}

function StatusDot({ status }: { status: ToolCall["status"] }) {
  if (status === "running") {
    return (
      <span className="relative flex h-2.5 w-2.5">
        <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-accent opacity-50" />
        <span className="relative inline-flex h-2.5 w-2.5 rounded-full bg-accent" />
      </span>
    );
  }
  if (status === "error") {
    return <span className="h-2.5 w-2.5 rounded-full bg-red-500" />;
  }
  return (
    <span className="flex h-2.5 w-2.5 items-center justify-center rounded-full bg-accent/20 text-[9px] font-bold text-accent">
      ✓
    </span>
  );
}

function format(v: unknown) {
  if (typeof v === "string") return v;
  try {
    return JSON.stringify(v, null, 2);
  } catch {
    return String(v);
  }
}
