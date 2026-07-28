/** Helpers for ask_user clarification interrupts (Claude Code AskUserQuestion pattern). */

import type {
  ClarificationPayload,
  ClarificationQuestion,
  InterruptPayload,
} from "@/lib/api";

export function extractClarificationFromInterrupt(
  payload: InterruptPayload | null | undefined
): ClarificationPayload | null {
  if (!payload) return null;
  if (payload.clarification && Array.isArray(payload.clarification.questions)) {
    return payload.clarification;
  }
  if (payload.kind === "clarification" || payload.clarification) {
    const nested = findClarification(payload.interrupts);
    if (nested) return nested;
  }
  return findClarification(payload.interrupts);
}

function findClarification(value: unknown): ClarificationPayload | null {
  if (!value) return null;
  if (Array.isArray(value)) {
    for (const item of value) {
      const found = findClarification(item);
      if (found) return found;
    }
    return null;
  }
  if (typeof value !== "object") return null;
  const obj = value as Record<string, unknown>;
  if (obj.type === "clarification" && Array.isArray(obj.questions)) {
    return obj as unknown as ClarificationPayload;
  }
  if ("value" in obj) {
    return findClarification(obj.value);
  }
  if ("clarification" in obj) {
    return findClarification(obj.clarification);
  }
  return null;
}

export function isClarificationInterrupt(
  payload: InterruptPayload | null | undefined
): boolean {
  return extractClarificationFromInterrupt(payload) != null;
}

export function formatClarificationAnswer(
  question: ClarificationQuestion,
  selected: string[],
  freeText: string
): string {
  const typed = freeText.trim();
  if (typed) return typed;
  if (question.multi_select) return selected.join(", ");
  return selected[0] || "";
}
