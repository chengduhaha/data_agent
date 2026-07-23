"use client";

import type { ChatMessage, SubagentEvent } from "@/lib/api";
import { toolStepLabel } from "@/lib/toolLabels";
import { splitAssistantContent } from "@/lib/messageContent";
import { normalizeNarrativeMarkdown, shouldRenderAsMarkdown } from "@/lib/markdownOutput";
import { MarkdownRenderer } from "./MarkdownRenderer";
import { QueryAppendix } from "./QueryAppendix";
import { ToolCallCard } from "./ToolCallCard";

export function MessageBubble({
  message,
  streaming = false,
}: {
  message: ChatMessage;
  streaming?: boolean;
}) {
  const isUser = message.role === "user";
  const tools = message.tools || [];
  const hasTools = tools.length > 0;
  // Legacy threads may have SQL inlined into `content`; split it out so the
  // narrative area is never a bare code block (see lib/messageContent.ts).
  const { narrative, queryAppendix: inlineAppendix } = isUser
    ? { narrative: message.content, queryAppendix: [] }
    : splitAssistantContent(
        normalizeNarrativeMarkdown(message.content || "", streaming)
      );
  const structuredAppendix = message.queryAppendix || [];
  const appendixQueries =
    structuredAppendix.length > 0
      ? structuredAppendix
      : inlineAppendix.map((q) => ({ sql: q.sql, tool: q.tool || "run_query_safely" }));
  const hasContent = Boolean(narrative?.trim());
  const thinking = !isUser && streaming && !hasContent;
  const latestRunning = [...tools].reverse().find((t) => t.status === "running");
  const liveLabel =
    (latestRunning && toolStepLabel(latestRunning.tool, latestRunning.input)) ||
    message.statusText ||
    "Thinking…";

  return (
    <div
      className={`flex animate-fade-up ${isUser ? "justify-end" : "justify-start"}`}
    >
      <div
        className={`rounded-2xl px-4 py-3 ${
          isUser
            ? "max-w-[min(720px,92%)] bg-ink-900 text-white"
            : "max-w-[min(920px,96%)] border border-ink-200/70 bg-white/80 text-ink-900 shadow-soft"
        }`}
      >
        {!isUser && (
          <p className="mb-1 text-[10px] font-semibold uppercase tracking-wider text-accent">
            Agent
          </p>
        )}

        {!isUser && hasTools && (
          <div className="mb-2 space-y-1.5">
            <div className="rounded-xl border border-ink-200/60 bg-ink-50/40 p-2">
              <p className="mb-1.5 text-[10px] font-semibold uppercase tracking-wider text-ink-400">
                {streaming ? "Steps · live" : "Steps"}
              </p>
              <div className="space-y-1">
                {tools.map((t) => (
                  <ToolCallCard key={t.id} tool={t} />
                ))}
              </div>
            </div>
          </div>
        )}

        {!isUser && thinking && !hasTools && (
          <div className="mb-2">
            <div className="inline-flex max-w-full items-center gap-2 rounded-full border border-accent/25 bg-accent-soft/60 px-2.5 py-1 text-xs text-accent-strong">
              <Spinner />
              <span className="truncate">{liveLabel}</span>
            </div>
          </div>
        )}

        {hasContent && (
          <div className="text-sm">
            {isUser ? (
              <div className="whitespace-pre-wrap leading-relaxed">{narrative}</div>
            ) : (
              <MarkdownRenderer content={narrative} streaming={streaming} />
            )}
            {!isUser && streaming && (
              <span
                className="ml-0.5 inline-block h-4 w-0.5 animate-pulse bg-accent align-middle"
                aria-hidden
              />
            )}
          </div>
        )}

        {message.subagents?.map((s) => (
          <SubagentCard key={`${s.id}-${s.phase}`} event={s} />
        ))}

        {!isUser && !streaming && <QueryAppendix queries={appendixQueries} />}
      </div>
    </div>
  );
}

function Spinner() {
  return (
    <span
      className="inline-block h-3 w-3 shrink-0 animate-spin rounded-full border-2 border-accent/30 border-t-accent"
      aria-hidden
    />
  );
}

function SubagentCard({ event }: { event: SubagentEvent }) {
  const outputText =
    typeof event.output === "string"
      ? event.output
      : event.output !== undefined
        ? JSON.stringify(event.output, null, 2)
        : "";
  const showOutput = Boolean(outputText.trim());

  if (event.phase === "start" && !showOutput) return null;

  return (
    <div className="mt-2 rounded-xl border border-dashed border-accent/40 bg-accent-soft/50 px-3 py-2">
      <p className="text-[10px] font-semibold uppercase tracking-wider text-accent-strong">
        Subagent · {event.phase}
        {event.tool ? ` · ${event.tool}` : ""}
      </p>
      {showOutput && shouldRenderAsMarkdown(outputText) ? (
        <div className="mt-2 text-sm">
          <MarkdownRenderer content={outputText} />
        </div>
      ) : showOutput ? (
        <pre className="mt-2 max-h-72 overflow-auto whitespace-pre-wrap font-mono text-[11px] text-ink-700">
          {outputText}
        </pre>
      ) : null}
    </div>
  );
}
