/** REST + SSE client for the data_agent backend. */

import type { AuthBootstrap, AuthConfig, AuthUser } from "@/lib/authTypes";

const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE !== undefined
    ? process.env.NEXT_PUBLIC_API_BASE.replace(/\/$/, "")
    : "";

export class AuthRequiredError extends Error {
  constructor(message = "Authentication required") {
    super(message);
    this.name = "AuthRequiredError";
  }
}

export function getApiBase() {
  return API_BASE;
}

function apiUrl(path: string): string {
  const full = path.startsWith("http") ? path : `${API_BASE}${path}`;
  if (full.startsWith("http")) return full;
  const base =
    typeof window !== "undefined"
      ? window.location.origin
      : "http://127.0.0.1:6641";
  return new URL(full, base).toString();
}

async function handleResponse<T>(res: Response): Promise<T> {
  if (res.status === 401) {
    throw new AuthRequiredError(await res.text());
  }
  if (!res.ok) throw new Error(await res.text());
  if (res.status === 204) return undefined as T;
  const text = await res.text();
  if (!text) return undefined as T;
  return JSON.parse(text) as T;
}

const fetchOpts: RequestInit = {
  credentials: "include",
  cache: "no-store",
};

export async function getAuthConfig(): Promise<AuthConfig> {
  const res = await fetch(apiUrl("/api/auth/config"), fetchOpts);
  return handleResponse<AuthConfig>(res);
}

export async function getAuthBootstrap(): Promise<AuthBootstrap> {
  const res = await fetch(apiUrl("/api/auth/bootstrap"), fetchOpts);
  return handleResponse<AuthBootstrap>(res);
}

export async function getAuthMe(): Promise<AuthUser> {
  const res = await fetch(apiUrl("/api/auth/me"), fetchOpts);
  return handleResponse<AuthUser>(res);
}

export async function logout(): Promise<void> {
  const res = await fetch(apiUrl("/api/auth/logout"), {
    ...fetchOpts,
    method: "POST",
  });
  await handleResponse<{ message: string }>(res);
}

export async function apiGet<T = unknown>(path: string): Promise<T> {
  const res = await fetch(apiUrl(path), fetchOpts);
  return handleResponse<T>(res);
}

export async function apiSend<T = unknown>(
  path: string,
  method: string,
  body?: unknown
): Promise<T> {
  const res = await fetch(apiUrl(path), {
    ...fetchOpts,
    method,
    headers: { "Content-Type": "application/json" },
    body: body === undefined ? undefined : JSON.stringify(body),
  });
  return handleResponse<T>(res);
}

export async function apiUpload(
  path: string,
  formData: FormData,
  query?: Record<string, string>
): Promise<void> {
  const url = new URL(apiUrl(path));
  if (query) {
    for (const [k, v] of Object.entries(query)) {
      url.searchParams.set(k, v);
    }
  }
  const res = await fetch(url.toString(), {
    credentials: "include",
    method: "POST",
    body: formData,
  });
  await handleResponse(res);
}

export async function deleteThread(threadId: string): Promise<void> {
  await apiSend(`/api/chat/threads/${encodeURIComponent(threadId)}`, "DELETE");
}

export type SseHandler = (event: string, data: Record<string, unknown>) => void;

export type StreamChatOptions = {
  title?: string;
  continue_run?: boolean;
  extended_run?: boolean;
};

export async function streamChat(
  message: string,
  threadId: string | null,
  onEvent: SseHandler,
  signal?: AbortSignal,
  options?: StreamChatOptions
): Promise<void> {
  const res = await fetch(apiUrl("/api/chat/stream"), {
    ...fetchOpts,
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Accept: "text/event-stream",
    },
    body: JSON.stringify({
      message,
      thread_id: threadId,
      title: options?.title,
      continue_run: options?.continue_run ?? false,
      extended_run: options?.extended_run ?? false,
    }),
    signal,
  });
  if (res.status === 401) {
    throw new AuthRequiredError(await res.text());
  }
  if (!res.ok || !res.body) {
    throw new Error(await res.text());
  }
  await readSse(res.body, onEvent);
}

export async function resumeChat(
  threadId: string,
  decisions: Array<Record<string, unknown>>,
  onEvent: SseHandler,
  signal?: AbortSignal
): Promise<void> {
  const res = await fetch(apiUrl("/api/chat/resume"), {
    ...fetchOpts,
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Accept: "text/event-stream",
    },
    body: JSON.stringify({
      thread_id: threadId,
      decisions,
    }),
    signal,
  });
  if (res.status === 401) {
    throw new AuthRequiredError(await res.text());
  }
  if (!res.ok || !res.body) {
    throw new Error(await res.text());
  }
  await readSse(res.body, onEvent);
}

async function readSse(
  body: ReadableStream<Uint8Array>,
  onEvent: SseHandler
): Promise<void> {
  const reader = body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";
  let eventName = "message";

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });
    const parts = buffer.split("\n");
    buffer = parts.pop() || "";

    for (const line of parts) {
      if (line.startsWith("event:")) {
        eventName = line.slice(6).trim();
      } else if (line.startsWith("data:")) {
        const raw = line.slice(5).trim();
        if (!raw) continue;
        try {
          const data = JSON.parse(raw) as Record<string, unknown>;
          onEvent(eventName, data);
        } catch {
          onEvent(eventName, { raw });
        }
        eventName = "message";
      } else if (line.trim() === "") {
        eventName = "message";
      }
    }
  }
}

export type ChatMessage = {
  id: string;
  role: "user" | "assistant" | "system";
  content: string;
  statusText?: string;
  tools?: ToolCall[];
  subagents?: SubagentEvent[];
  /** Executed queries kept as structured data, never concatenated into `content`. */
  queryAppendix?: QueryAppendixItem[];
};

export type QueryAppendixItem = {
  sql: string;
  tool: string;
};

export type ToolCall = {
  id: string;
  tool: string;
  input?: unknown;
  output?: unknown;
  status: "running" | "done" | "error";
};

export type SubagentEvent = {
  id: string;
  phase: string;
  tool?: string;
  input?: unknown;
  output?: unknown;
};

export type InterruptPayload = {
  interrupts: unknown[];
  thread_id?: string;
};

export type ContinuePromptPayload = {
  thread_id?: string;
  run_segment?: number;
  steps_used?: number;
  steps_limit?: number;
  message?: string;
};

export type BudgetPayload = {
  steps_used?: number;
  steps_limit?: number;
  steps_warn_at?: number;
  phase?: "ok" | "warn" | "exhausted";
  run_phase?: "research" | "execute" | "synthesize";
  sql_queries_used?: number;
  tool_calls_used?: Record<string, number>;
  run_segment?: number;
  thread_id?: string;
};

export type TopicHintPayload = {
  relation?: string;
  suggest_new_thread?: boolean;
  message?: string;
};
