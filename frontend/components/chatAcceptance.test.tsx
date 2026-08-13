import "@testing-library/jest-dom/vitest";
import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";
import { ContextBudgetBar } from "@/components/ContextBudgetBar";
import { MessageBubble } from "@/components/MessageBubble";
import { QueryAppendix } from "@/components/QueryAppendix";
import { RunPhaseBar } from "@/components/RunPhaseBar";

afterEach(() => cleanup());

describe("F1 MessageBubble + QueryAppendix", () => {
  it("renders narrative markdown separately from collapsible SQL appendix", () => {
    render(
      <MessageBubble
        message={{
          id: "a1",
          role: "assistant",
          content: "## Summary\n\nRevenue is up 5%.",
          queryAppendix: [{ sql: "SELECT 1", tool: "run_query_safely" }],
        }}
      />
    );

    expect(screen.getByText(/Revenue is up 5%/)).toBeInTheDocument();
    expect(screen.queryByText("SELECT 1")).not.toBeInTheDocument();

    fireEvent.click(screen.getByRole("button", { name: /Query validation/i }));
    expect(screen.getByText("SELECT 1")).toBeInTheDocument();
  });

  it("does not put SQL in the narrative body for legacy inline appendix", () => {
    const content =
      "## Summary\n\nDone.\n\n---\n\n## Query validation\n\n```sql\nSELECT legacy\n```\n";
    render(
      <MessageBubble
        message={{
          id: "a2",
          role: "assistant",
          content,
        }}
      />
    );

    expect(screen.getByText(/Done\./)).toBeInTheDocument();
    expect(screen.queryByText("SELECT legacy")).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: /Query validation/i }));
    expect(screen.getByText("SELECT legacy")).toBeInTheDocument();
  });

  it("renders tool output markdown as preview when expanded", () => {
    render(
      <MessageBubble
        message={{
          id: "a3",
          role: "assistant",
          content: "",
          tools: [
            {
              id: "t1",
              tool: "Read",
              status: "done",
              output: "### Analysis Approach\n\n- Confirm month mapping",
            },
          ],
        }}
      />
    );

    fireEvent.click(screen.getByRole("button", { name: /Read/i }));
    expect(
      screen.getByRole("heading", { level: 3, name: "Analysis Approach" })
    ).toBeInTheDocument();
    expect(screen.getByText("Confirm month mapping")).toBeInTheDocument();
  });

  it("renders prose tool output outside black code blocks", () => {
    render(
      <MessageBubble
        message={{
          id: "a3b",
          role: "assistant",
          content: "",
          tools: [
            {
              id: "t2",
              tool: "Read",
              status: "done",
              output:
                "Let me take a different approach and check the DWD table schema for PMID-706187.",
            },
          ],
        }}
      />
    );

    fireEvent.click(screen.getByRole("button", { name: /Read/i }));
    expect(
      screen.getByText(/Let me take a different approach/)
    ).toBeInTheDocument();
    expect(document.querySelector(".markdown-body pre.bg-ink-950")).toBeNull();
  });

  it("renders assistant narrative wrapped in plain code fences as markdown preview", () => {
    render(
      <MessageBubble
        message={{
          id: "a3c",
          role: "assistant",
          content:
            "```\nLet me take a different approach.\n\n### Recommended Table\n\n- pm_id\n```",
        }}
      />
    );

    expect(screen.getByRole("heading", { level: 3, name: "Recommended Table" })).toBeInTheDocument();
    expect(document.querySelector(".markdown-body pre.bg-ink-950")).toBeNull();
  });

  it("renders all 10 rows of a top-10 answer when the model glues two ranks per line", () => {
    // Regression test for a bug where the model streamed two logical table rows
    // on one physical markdown line (e.g. "| 1 | ... | | 2 | ... |"). GFM only
    // parsed 5 rows from that input, so only odd ranks (1,3,5,7,9) rendered and
    // even ranks (2,4,6,8,10) silently disappeared from the final answer.
    const content = `## Summary

Top 10 negative-NGM orders — 2026-04-30

| Rank | Order | NGM |
| --- | --- | --- |
| 1 | -77294 | x | 2 | 621286 | x |
| 3 | 657888 | x | 4 | 141692 | x |
| 5 | 413709 | x | 6 | 173937798 | x |
| 7 | 124858 | x | 8 | 529859 | x |
| 9 | 303148 | x | 10 | 695266 | x |`;

    render(
      <MessageBubble
        message={{
          id: "a5",
          role: "assistant",
          content,
        }}
      />
    );

    const rows = document.querySelectorAll(".markdown-body table tbody tr");
    expect(rows.length).toBe(10);

    const orderIds = [
      "-77294",
      "621286",
      "657888",
      "141692",
      "413709",
      "173937798",
      "124858",
      "529859",
      "303148",
      "695266",
    ];
    for (const orderId of orderIds) {
      expect(screen.getByText(orderId)).toBeInTheDocument();
    }
  });

  it("hides empty subagent start cards and renders end output", () => {
    const sharedId = "019f6a55-e960-79b0-807e-3c1dcef9cbdd";
    render(
      <MessageBubble
        message={{
          id: "a4",
          role: "assistant",
          content: "Done.",
          subagents: [
            { id: sharedId, phase: "start", tool: "task" },
            { id: sharedId, phase: "end", tool: "task", output: "Subagent finished." },
          ],
        }}
      />
    );

    expect(screen.getByText(/Subagent finished/)).toBeInTheDocument();
    expect(screen.queryByText(/Subagent · start/i)).not.toBeInTheDocument();
  });
});

describe("F3 ContextBudgetBar", () => {
  const budget = {
    steps_used: 4,
    steps_limit: 150,
    phase: "ok" as const,
    run_phase: "execute" as const,
  };

  it("hides on new chat when budget is cleared", () => {
    const { container, rerender } = render(
      <ContextBudgetBar budget={budget} threadId="thread-1" streaming={false} />
    );
    expect(container.querySelector('[data-testid="context-budget-bar"]')).toBeTruthy();

    rerender(<ContextBudgetBar budget={null} threadId={null} streaming={false} />);
    expect(container.querySelector('[data-testid="context-budget-bar"]')).toBeNull();
  });

  it("shows during streaming before thread id is assigned", () => {
    render(<ContextBudgetBar budget={budget} threadId={null} streaming />);
    expect(screen.getByText("Agent steps")).toBeInTheDocument();
  });
});

describe("UX RunPhaseBar + QueryAppendix", () => {
  it("shows research → execute → synthesize phases", () => {
    render(
      <RunPhaseBar
        budget={{
          steps_used: 2,
          steps_limit: 150,
          run_phase: "research",
        }}
      />
    );
    expect(screen.getByText("Research")).toBeInTheDocument();
    expect(screen.getByText("Execute")).toBeInTheDocument();
    expect(screen.getByText("Synthesize")).toBeInTheDocument();
  });

  it("keeps SQL appendix collapsed by default", () => {
    render(
      <QueryAppendix queries={[{ sql: "SELECT hidden", tool: "run_query_safely" }]} />
    );
    expect(screen.queryByText("SELECT hidden")).not.toBeInTheDocument();
    expect(screen.getByText("▸")).toBeInTheDocument();
  });
});
