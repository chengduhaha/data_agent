/** Build SSE bodies for mocked chat streams in Playwright route handlers. */

export type MockSseEvent = {
  event: string;
  data: Record<string, unknown>;
};

export function encodeSse(events: MockSseEvent[]): string {
  return events
    .map((e) => `event: ${e.event}\ndata: ${JSON.stringify(e.data)}\n\n`)
    .join("");
}

/** Deterministic acceptance stream: narrative + appendix + budget phases. */
export function acceptanceChatStream(threadId = "e2e-thread-1"): MockSseEvent[] {
  return [
    { event: "meta", data: { thread_id: threadId, user_id: "local", run_segment: 1 } },
    { event: "status", data: { text: "Agent ready", phase: "init" } },
    {
      event: "budget",
      data: {
        steps_used: 2,
        steps_limit: 150,
        phase: "ok",
        run_phase: "research",
        thread_id: threadId,
      },
    },
    { event: "token", data: { text: "## Summary\n\nRevenue is up 5% QoQ." } },
    {
      event: "budget",
      data: {
        steps_used: 5,
        steps_limit: 150,
        phase: "ok",
        run_phase: "execute",
        thread_id: threadId,
      },
    },
    { event: "token", data: { text: "\n\n## Evidence\n\nValidated against Vertica." } },
    {
      event: "query_appendix",
      data: {
        queries: [{ sql: "SELECT revenue FROM fact_sales LIMIT 1", tool: "run_query_safely" }],
      },
    },
    {
      event: "budget",
      data: {
        steps_used: 8,
        steps_limit: 150,
        phase: "ok",
        run_phase: "synthesize",
        thread_id: threadId,
      },
    },
    { event: "done", data: { incomplete: false } },
  ];
}

/** Many small token events to exercise scroll stability (F2). */
export function streamingScrollStream(threadId = "e2e-scroll-thread"): MockSseEvent[] {
  const events: MockSseEvent[] = [
    { event: "meta", data: { thread_id: threadId, user_id: "local", run_segment: 1 } },
    { event: "status", data: { text: "Streaming…", phase: "init" } },
    {
      event: "budget",
      data: {
        steps_used: 1,
        steps_limit: 150,
        phase: "ok",
        run_phase: "research",
        thread_id: threadId,
      },
    },
  ];
  for (let i = 0; i < 40; i++) {
    events.push({
      event: "token",
      data: { text: `Line ${i + 1}: streaming filler content for scroll stability.\n` },
    });
  }
  events.push({ event: "done", data: { incomplete: false } });
  return events;
}
