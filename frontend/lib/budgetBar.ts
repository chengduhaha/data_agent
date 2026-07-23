import type { BudgetPayload } from "@/lib/api";

/** Whether the Agent steps / phase progress bar should render. */
export function shouldShowBudgetBar(
  budget: BudgetPayload | null,
  opts: { threadId: string | null; streaming: boolean }
): boolean {
  if (!budget || budget.steps_limit == null) return false;
  if (!opts.streaming && opts.threadId == null) return false;
  return true;
}
