"use client";

import type { ChatMessage, SubagentEvent } from "@/lib/api";
import { toolStepLabel } from "@/lib/toolLabels";
import { MarkdownRenderer } from "./MarkdownRenderer";
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
  const hasContent = Boolean(message.content?.trim());
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
              <div className="whitespace-pre-wrap leading-relaxed">{message.content}</div>
            ) : (
              <MarkdownRenderer content={message.content} />
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
          <SubagentCard key={s.id} event={s} />
        ))}
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
  return (
    <div className="mt-2 rounded-xl border border-dashed border-accent/40 bg-accent-soft/50 px-3 py-2">
      <p className="text-[10px] font-semibold uppercase tracking-wider text-accent-strong">
        Subagent · {event.phase}
      </p>
      <p className="font-mono text-xs text-ink-700">{event.tool || "task"}</p>
    </div>
  );
}
