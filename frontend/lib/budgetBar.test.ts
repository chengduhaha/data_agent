import { describe, expect, it } from "vitest";
import { shouldShowBudgetBar } from "./budgetBar";

describe("shouldShowBudgetBar", () => {
  const budget = { steps_used: 3, steps_limit: 150, phase: "ok" as const };

  it("hides when budget is null (new chat)", () => {
    expect(shouldShowBudgetBar(null, { threadId: null, streaming: false })).toBe(false);
  });

  it("shows during streaming even before thread id is assigned", () => {
    expect(shouldShowBudgetBar(budget, { threadId: null, streaming: true })).toBe(true);
  });

  it("hides on new chat with stale budget cleared", () => {
    expect(shouldShowBudgetBar(budget, { threadId: null, streaming: false })).toBe(false);
  });

  it("shows for an active thread with budget", () => {
    expect(shouldShowBudgetBar(budget, { threadId: "abc", streaming: false })).toBe(true);
  });
});
