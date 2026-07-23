"use client";

import { useState } from "react";
import type { ToolCall } from "@/lib/api";
import { normalizeNarrativeMarkdown, shouldRenderAsMarkdown } from "@/lib/markdownOutput";
import { MarkdownRenderer } from "./MarkdownRenderer";
import { toolStepDetail, toolStepLabel } from "@/lib/toolLabels";

/** Generic SQL-shaped tool detection (not vendor-specific — any `run_query*`/`execute_query*` tool). */
function isQueryTool(tool: string): boolean {
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
  const queryTool = isQueryTool(tool.tool);
  const fullSql = queryTool ? extractQuery(tool.input) : null;
  const inputMaxHeight = queryTool ? "max-h-96" : "max-h-28";
  const outputMaxHeight = queryTool ? "max-h-96" : "max-h-40";

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
            <ToolPayloadBody value={fullSql ?? tool.input} preferMarkdown={!queryTool} />
          )}
          {tool.output !== undefined && (
            <ToolPayloadBody value={tool.output} preferMarkdown maxHeight={outputMaxHeight} />
          )}
        </div>
      )}
    </div>
  );
}

function ToolPayloadBody({
  value,
  preferMarkdown = true,
  maxHeight = "max-h-40",
}: {
  value: unknown;
  preferMarkdown?: boolean;
  maxHeight?: string;
}) {
  const text = format(value);
  const markdownText =
    typeof value === "string" ? normalizeNarrativeMarkdown(value) : text;
  if (preferMarkdown && typeof value === "string" && shouldRenderAsMarkdown(value)) {
    return (
      <div
        className={`${maxHeight} overflow-auto border-b border-ink-200/40 px-3 py-2 last:border-b-0`}
      >
        <MarkdownRenderer content={markdownText} />
      </div>
    );
  }
  return (
    <pre
      className={`${maxHeight} overflow-auto border-b border-ink-200/40 px-3 py-2 font-mono text-[11px] text-ink-700 last:border-b-0`}
    >
      {text}
    </pre>
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
