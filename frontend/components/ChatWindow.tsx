"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import {
  apiGet,
  type BudgetPayload,
  type ChatMessage,
  type ContinuePromptPayload,
  type InterruptPayload,
  type ToolCall,
  deleteThread,
  resumeChat,
  streamChat,
} from "@/lib/api";
import { toolStepLabel } from "@/lib/toolLabels";
import { parseQueryAppendixEvent } from "@/lib/queryAppendix";
import { HitlPanel } from "./HitlPanel";
import { ClarificationPanel } from "./ClarificationPanel";
import { ContinuePanel } from "./ContinuePanel";
import { ContextBudgetBar } from "./ContextBudgetBar";
import { MessageBubble } from "./MessageBubble";
import { ModelSwitcher } from "./ModelSwitcher";
import { ThreadSidebar } from "./ThreadSidebar";
import { ChatInput } from "./ChatInput";
import { expandSkillMessage, type SlashSkill } from "@/lib/skillSlash";
import { buildHitlDecisions } from "@/lib/hitl";
import {
  extractClarificationFromInterrupt,
  isClarificationInterrupt,
} from "@/lib/clarification";
import { useAuth } from "@/context/AuthContext";
import { useMessageScroll } from "@/hooks/useMessageScroll";
import { ScrollToBottom } from "./ScrollToBottom";

function uid() {
  return Math.random().toString(36).slice(2, 10);
}

function shouldKeepAssistant(m: ChatMessage, activeId?: string | null) {
  if (m.role !== "assistant") return true;
  const hasBody =
    Boolean(m.content?.trim()) ||
    Boolean(m.tools && m.tools.length > 0) ||
    Boolean(m.subagents && m.subagents.length > 0) ||
    Boolean(m.queryAppendix && m.queryAppendix.length > 0);
  if (activeId && m.id === activeId) return hasBody;
  return hasBody;
}

function threadTitlePreview(text: string, maxLen = 56): string {
  const normalized = text.trim().replace(/\s+/g, " ");
  if (!normalized) return "New chat";
  if (normalized.length <= maxLen) return normalized;
  return `${normalized.slice(0, maxLen - 1).trimEnd()}…`;
}

export function ChatWindow() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [threadId, setThreadId] = useState<string | null>(null);
  const [threads, setThreads] = useState<{ thread_id: string; title?: string }[]>([]);
  const [streaming, setStreaming] = useState(false);
  const [streamStartedAt, setStreamStartedAt] = useState<number | null>(null);
  const [elapsedSec, setElapsedSec] = useState(0);
  const [interrupt, setInterrupt] = useState<InterruptPayload | null>(null);
  const [continuePrompt, setContinuePrompt] = useState<ContinuePromptPayload | null>(null);
  const [budget, setBudget] = useState<BudgetPayload | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [skills, setSkills] = useState<SlashSkill[]>([]);
  const lastMsg = messages[messages.length - 1];
  const scrollDeps = useMemo(
    () => [
      messages.length,
      lastMsg?.content?.length,
      lastMsg?.tools?.length,
      interrupt,
      continuePrompt,
    ],
    [
      messages.length,
      lastMsg?.content?.length,
      lastMsg?.tools?.length,
      interrupt,
      continuePrompt,
    ]
  );
  const { scrollableRef, contentRef, bottomSentinelRef, isNearBottom, scrollToBottom, resetFollow } =
    useMessageScroll<HTMLDivElement>(scrollDeps, { streaming });
  const abortRef = useRef<AbortController | null>(null);
  const pendingTitleRef = useRef("");
  const { user, oauthEnabled } = useAuth();
  const workspaceSlug = user?.workspace_slug ?? "local";

  const refreshThreads = useCallback(async () => {
    try {
      const data = await apiGet<{ threads: { thread_id: string; title?: string }[] }>(
        "/api/chat/threads"
      );
      setThreads(data.threads || []);
    } catch {
      /* ignore until backend is up */
    }
  }, []);

  useEffect(() => {
    if (oauthEnabled && !user) return;
    setThreadId(null);
    setMessages([]);
    setInterrupt(null);
    setError(null);
    void refreshThreads();
  }, [workspaceSlug, oauthEnabled, refreshThreads]);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const data = await apiGet<{ skills: SlashSkill[] }>("/api/skills");
        if (!cancelled) setSkills(data.skills || []);
      } catch {
        /* backend may still be starting */
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  useEffect(() => {
    if (!streaming || streamStartedAt == null) {
      setElapsedSec(0);
      return;
    }
    const tick = () =>
      setElapsedSec(Math.floor((Date.now() - streamStartedAt) / 1000));
    tick();
    const id = window.setInterval(tick, 1000);
    return () => window.clearInterval(id);
  }, [streaming, streamStartedAt]);

  const liveStatus = useMemo(() => {
    if (!streaming) return null;
    const lastAssistant = [...messages]
      .reverse()
      .find((m) => m.role === "assistant");
    const running = lastAssistant?.tools?.find((t) => t.status === "running");
    if (running) return toolStepLabel(running.tool, running.input);
    if (lastAssistant?.statusText) return lastAssistant.statusText;
    if (lastAssistant?.content?.trim()) return "Writing answer…";
    if ((lastAssistant?.tools?.length || 0) > 0) return "Continuing…";
    return "Thinking…";
  }, [streaming, messages]);

  const applyStreamEvent = useCallback(
    (event: string, data: Record<string, unknown>, assistantId: string) => {
      if (event === "meta" && typeof data.thread_id === "string") {
        const tid = data.thread_id;
        setThreadId(tid);
        setThreads((prev) => {
          if (prev.some((t) => t.thread_id === tid)) return prev;
          return [
            { thread_id: tid, title: threadTitlePreview(pendingTitleRef.current) },
            ...prev,
          ];
        });
        void refreshThreads();
      }
      if (event === "budget") {
        setBudget(data as unknown as BudgetPayload);
      }
      if (event === "status" && typeof data.text === "string") {
        setMessages((prev) =>
          prev.map((m) =>
            m.id === assistantId ? { ...m, statusText: data.text as string } : m
          )
        );
      }
      if (event === "token" && typeof data.text === "string") {
        setMessages((prev) =>
          prev.map((m) =>
            m.id === assistantId
              ? { ...m, content: m.content + data.text, statusText: undefined }
              : m
          )
        );
      }
      if (event === "tool_start") {
        const tool: ToolCall = {
          id: String(data.run_id || uid()),
          tool: String(data.tool || "tool"),
          input: data.input,
          status: "running",
        };
        setMessages((prev) =>
          prev.map((m) =>
            m.id === assistantId
              ? { ...m, tools: [...(m.tools || []), tool] }
              : m
          )
        );
      }
      if (event === "tool_end") {
        setMessages((prev) =>
          prev.map((m) => {
            if (m.id !== assistantId) return m;
            const tools = (m.tools || []).map((t) =>
              t.id === String(data.run_id) ||
              (t.tool === data.tool && t.status === "running")
                ? { ...t, output: data.output, status: "done" as const }
                : t
            );
            return { ...m, tools };
          })
        );
      }
      if (event === "subagent") {
        const entry = {
          id: String(data.run_id || uid()),
          phase: String(data.phase || ""),
          tool: data.tool ? String(data.tool) : undefined,
          input: data.input,
          output: data.output,
        };
        setMessages((prev) =>
          prev.map((m) => {
            if (m.id !== assistantId) return m;
            const subs = [...(m.subagents || [])];
            const idx = subs.findIndex((s) => s.id === entry.id);
            if (idx >= 0) {
              subs[idx] = { ...subs[idx], ...entry };
            } else {
              subs.push(entry);
            }
            return { ...m, subagents: subs };
          })
        );
      }
      if (event === "query_appendix") {
        const queries = parseQueryAppendixEvent(data);
        if (queries.length) {
          setMessages((prev) =>
            prev.map((m) =>
              m.id === assistantId
                ? { ...m, queryAppendix: queries, statusText: undefined }
                : m
            )
          );
        }
      }
      if (event === "interrupt") {
        setInterrupt(data as unknown as InterruptPayload);
      }
      if (event === "continue_prompt") {
        setContinuePrompt(data as unknown as ContinuePromptPayload);
        setStreaming(false);
        setStreamStartedAt(null);
        if (data.steps_limit != null) {
          setBudget((prev) => ({
            ...prev,
            steps_used: Number(data.steps_used ?? prev?.steps_used ?? 0),
            steps_limit: Number(data.steps_limit),
            phase: "exhausted",
          }));
        }
      }
      if (event === "error") {
        setError(String(data.message || "Stream error"));
        void refreshThreads();
      }
      if (event === "done") {
        setInterrupt(null);
        setStreaming(false);
        setStreamStartedAt(null);
        if (!data.incomplete) {
          setContinuePrompt(null);
        }
        void refreshThreads();
      }
    },
    [refreshThreads]
  );

  async function send() {
    const displayText = input.trim();
    if (!displayText || streaming) return;
    const text = expandSkillMessage(displayText, skills);
    pendingTitleRef.current = displayText;
    setError(null);
    setInterrupt(null);
    setContinuePrompt(null);
    setBudget(null);
    setInput("");
    const userMsg: ChatMessage = { id: uid(), role: "user", content: displayText };
    const assistantId = uid();
    setMessages((prev) => [
      ...prev,
      userMsg,
      { id: assistantId, role: "assistant", content: "", tools: [], subagents: [] },
    ]);
    resetFollow();
    setStreaming(true);
    setStreamStartedAt(Date.now());
    const ac = new AbortController();
    abortRef.current = ac;
    try {
      await streamChat(
        text,
        threadId,
        (event, data) => applyStreamEvent(event, data, assistantId),
        ac.signal,
        { title: displayText }
      );
    } catch (e) {
      if ((e as Error).name !== "AbortError") {
        setError((e as Error).message || String(e));
      }
    } finally {
      setStreaming(false);
      setStreamStartedAt(null);
      abortRef.current = null;
      // Drop leftover empty assistant placeholders (e.g. failed init / aborted turn).
      setMessages((prev) =>
        prev.filter((m) => shouldKeepAssistant(m, assistantId))
      );
      void refreshThreads();
    }
  }

  function stopStreaming() {
    abortRef.current?.abort();
    setStreaming(false);
    setStreamStartedAt(null);
  }

  async function handleContinue() {
    if (!threadId || streaming) return;
    setStreaming(true);
    setStreamStartedAt(Date.now());
    setError(null);
    setContinuePrompt(null);
    const assistantId = uid();
    setMessages((prev) => [
      ...prev,
      {
        id: assistantId,
        role: "assistant",
        content: "",
        tools: [],
        subagents: [],
      },
    ]);
    resetFollow();
    const ac = new AbortController();
    abortRef.current = ac;
    try {
      await streamChat(
        "",
        threadId,
        (event, data) => applyStreamEvent(event, data, assistantId),
        ac.signal,
        { continue_run: true }
      );
    } catch (e) {
      if ((e as Error).name !== "AbortError") {
        setError((e as Error).message || String(e));
      }
    } finally {
      setStreaming(false);
      setStreamStartedAt(null);
      abortRef.current = null;
      setMessages((prev) =>
        prev.filter((m) => shouldKeepAssistant(m, assistantId))
      );
      void refreshThreads();
    }
  }

  async function handleResume(approve: boolean) {
    if (!threadId || streaming) return;
    if (isClarificationInterrupt(interrupt)) return;
    setStreaming(true);
    setStreamStartedAt(Date.now());
    setError(null);
    const assistantId = uid();
    setMessages((prev) => [
      ...prev,
      {
        id: assistantId,
        role: "assistant",
        content: approve ? "" : "Rejected tool call.",
        tools: [],
        subagents: [],
      },
    ]);
    const decisions = buildHitlDecisions(approve, interrupt);
    try {
      await resumeChat(threadId, decisions, (event, data) =>
        applyStreamEvent(event, data, assistantId)
      );
      setInterrupt(null);
    } catch (e) {
      setError((e as Error).message || String(e));
    } finally {
      setStreaming(false);
      setStreamStartedAt(null);
    }
  }

  async function handleClarificationSubmit(answers: Record<string, string>) {
    if (!threadId || streaming) return;
    setStreaming(true);
    setStreamStartedAt(Date.now());
    setError(null);
    setInterrupt(null);
    const assistantId = uid();
    setMessages((prev) => [
      ...prev,
      {
        id: assistantId,
        role: "assistant",
        content: "",
        tools: [],
        subagents: [],
      },
    ]);
    resetFollow();
    const ac = new AbortController();
    abortRef.current = ac;
    try {
      await resumeChat(
        threadId,
        [],
        (event, data) => applyStreamEvent(event, data, assistantId),
        ac.signal,
        { answers }
      );
    } catch (e) {
      if ((e as Error).name !== "AbortError") {
        setError((e as Error).message || String(e));
      }
    } finally {
      setStreaming(false);
      setStreamStartedAt(null);
      abortRef.current = null;
      setMessages((prev) =>
        prev.filter((m) => shouldKeepAssistant(m, assistantId))
      );
      void refreshThreads();
    }
  }

  async function loadThread(id: string) {
    setThreadId(id);
    setInterrupt(null);
    setContinuePrompt(null);
    setBudget(null);
    setError(null);
    try {
      const data = await apiGet<{
        messages: Array<{
          role: string;
          content: string;
          id?: string;
          tools?: ToolCall[];
        }>;
        interrupts?: unknown[];
      }>(`/api/chat/threads/${id}`);
      setMessages(
        (data.messages || [])
          .filter((m) => {
            const role = m.role === "human" || m.role === "user" ? "user" : "assistant";
            const content =
              typeof m.content === "string" ? m.content : JSON.stringify(m.content ?? "");
            const tools = m.tools || [];
            // Drop empty assistant placeholders (tool-only turns already folded server-side).
            if (role === "assistant" && !content.trim() && tools.length === 0) return false;
            return (
              m.role === "human" ||
              m.role === "ai" ||
              m.role === "user" ||
              m.role === "assistant"
            );
          })
          .map((m) => ({
            id: m.id || uid(),
            role:
              m.role === "human" || m.role === "user"
                ? ("user" as const)
                : ("assistant" as const),
            content:
              typeof m.content === "string" ? m.content : JSON.stringify(m.content ?? ""),
            tools: (m.tools || []).map((t) => ({
              id: t.id || uid(),
              tool: t.tool || "tool",
              input: t.input,
              output: t.output,
              status: (t.status || "done") as ToolCall["status"],
            })),
          }))
      );
      if (data.interrupts && data.interrupts.length) {
        setInterrupt({
          interrupts: data.interrupts,
          thread_id: id,
          kind: undefined,
        });
      }
    } catch (e) {
      setError((e as Error).message || String(e));
    }
  }

  function newThread() {
    abortRef.current?.abort();
    setStreaming(false);
    setStreamStartedAt(null);
    setThreadId(null);
    setMessages([]);
    setInterrupt(null);
    setContinuePrompt(null);
    setBudget(null);
    setError(null);
  }

  async function handleDelete(id: string) {
    try {
      await deleteThread(id);
      if (threadId === id) newThread();
      await refreshThreads();
    } catch (e) {
      setError((e as Error).message || String(e));
    }
  }

  const lastAssistantId = [...messages].reverse().find((m) => m.role === "assistant")?.id;
  const clarification = extractClarificationFromInterrupt(interrupt);

  return (
    <div className="flex min-h-0 flex-1 flex-col gap-3 md:flex-row">
      <ThreadSidebar
        threads={threads}
        activeId={threadId}
        onSelect={loadThread}
        onNew={newThread}
        onDelete={handleDelete}
      />
      <section className="panel relative flex min-h-0 flex-1 flex-col overflow-hidden">
        <div
          ref={scrollableRef}
          data-testid="chat-scroll"
          className="relative flex-1 overflow-y-auto px-4 py-4 md:px-6"
          style={{ scrollbarGutter: "stable" }}
        >
          <div ref={contentRef} className="space-y-3 pb-2">
          {messages.length === 0 && (
            <div className="flex h-full min-h-[40vh] flex-col items-center justify-center text-center animate-fade-up">
              <p className="font-display text-2xl text-ink-800">Ready when you are</p>
              <p className="mt-2 max-w-md text-sm text-ink-500">
                Configure a model under Settings, then ask anything. Tool calls, subagents,
                and approval prompts appear inline.
              </p>
            </div>
          )}
          {messages.map((m) => {
            const emptyAssistant =
              m.role === "assistant" &&
              !m.content?.trim() &&
              !(m.tools && m.tools.length) &&
              !(m.subagents && m.subagents.length) &&
              !(streaming && m.id === lastAssistantId);
            if (emptyAssistant) return null;
            return (
              <MessageBubble
                key={m.id}
                message={m}
                streaming={streaming && m.id === lastAssistantId}
              />
            );
          })}
          {continuePrompt && (
            <ContinuePanel
              payload={continuePrompt}
              busy={streaming}
              onContinue={() => void handleContinue()}
            />
          )}
          {clarification && (
            <ClarificationPanel
              payload={clarification}
              busy={streaming}
              onSubmit={(answers) => void handleClarificationSubmit(answers)}
            />
          )}
          {interrupt && !clarification && (
            <HitlPanel
              payload={interrupt}
              busy={streaming}
              onApprove={() => handleResume(true)}
              onReject={() => handleResume(false)}
            />
          )}
          {error && (
            <div className="rounded-xl border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-800">
              {error}
            </div>
          )}
          <div ref={bottomSentinelRef} />
          </div>
          <ScrollToBottom
            visible={!isNearBottom && messages.length > 0}
            onClick={() => resetFollow()}
          />
        </div>
        <div className="shrink-0 border-t border-ink-200/70 bg-white/50 p-3 md:p-4">
          <ContextBudgetBar budget={budget} threadId={threadId} streaming={streaming} />
          {streaming && liveStatus && (
            <div className="mb-2 flex items-center gap-2 rounded-xl border border-accent/20 bg-accent-soft/40 px-3 py-1.5 text-xs text-accent-strong">
              <span className="inline-block h-3 w-3 animate-spin rounded-full border-2 border-accent/30 border-t-accent" />
              <span className="min-w-0 flex-1 truncate">{liveStatus}</span>
              <span className="shrink-0 tabular-nums text-ink-400">{elapsedSec}s</span>
            </div>
          )}
          <form
            className="flex w-full flex-col gap-2 sm:flex-row sm:items-end"
            onSubmit={(e) => {
              e.preventDefault();
              void send();
            }}
          >
            <ChatInput
              value={input}
              onChange={setInput}
              onSend={() => void send()}
              skills={skills}
              disabled={streaming}
            />
            {streaming ? (
              <button
                type="button"
                className="btn-ghost shrink-0 self-end"
                onClick={stopStreaming}
              >
                Stop
              </button>
            ) : (
              <button
                type="submit"
                className="btn-primary shrink-0 self-end"
                disabled={!input.trim()}
              >
                Send
              </button>
            )}
          </form>
          <ModelSwitcher disabled={streaming} />
        </div>
      </section>
    </div>
  );
}
