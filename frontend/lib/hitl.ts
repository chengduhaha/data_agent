/** Build HITL resume decisions for LangGraph HumanInTheLoopMiddleware. */

import type { InterruptPayload } from "@/lib/api";

export function hitlDecisionCount(payload: InterruptPayload | null | undefined): number {
  if (!payload?.interrupts?.length) return 1;
  for (const intr of payload.interrupts) {
    const value =
      intr && typeof intr === "object" && "value" in intr
        ? (intr as { value?: unknown }).value
        : intr;
    if (value && typeof value === "object" && "action_requests" in value) {
      const requests = (value as { action_requests?: unknown[] }).action_requests;
      if (Array.isArray(requests) && requests.length > 0) {
        return requests.length;
      }
    }
  }
  return 1;
}

export function buildHitlDecisions(
  approve: boolean,
  payload: InterruptPayload | null | undefined
): Array<Record<string, unknown>> {
  const count = hitlDecisionCount(payload);
  const decision = approve
    ? { type: "approve" }
    : { type: "reject", message: "User rejected the action." };
  return Array.from({ length: count }, () => ({ ...decision }));
}
