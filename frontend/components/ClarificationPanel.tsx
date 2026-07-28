"use client";

import { useMemo, useState } from "react";
import type { ClarificationPayload, ClarificationQuestion } from "@/lib/api";
import { formatClarificationAnswer } from "@/lib/clarification";

type QuestionState = {
  selected: string[];
  freeText: string;
};

function emptyState(): QuestionState {
  return { selected: [], freeText: "" };
}

export function ClarificationPanel({
  payload,
  busy,
  onSubmit,
}: {
  payload: ClarificationPayload;
  busy?: boolean;
  onSubmit: (answers: Record<string, string>) => void;
}) {
  const questions = payload.questions || [];
  const [states, setStates] = useState<QuestionState[]>(() =>
    questions.map(() => emptyState())
  );

  const canSubmit = useMemo(() => {
    if (!questions.length) return false;
    return questions.every((q, i) => {
      const st = states[i] || emptyState();
      if (st.freeText.trim()) return true;
      const opts = q.options || [];
      if (opts.length === 0) return false;
      return st.selected.length > 0;
    });
  }, [questions, states]);

  if (!questions.length) return null;

  function toggleOption(qi: number, label: string, multi: boolean) {
    setStates((prev) => {
      const next = prev.map((s) => ({ ...s, selected: [...s.selected] }));
      while (next.length <= qi) next.push(emptyState());
      const cur = next[qi];
      if (multi) {
        cur.selected = cur.selected.includes(label)
          ? cur.selected.filter((v) => v !== label)
          : [...cur.selected, label];
      } else {
        cur.selected = [label];
      }
      return next;
    });
  }

  function setFreeText(qi: number, text: string) {
    setStates((prev) => {
      const next = prev.map((s) => ({ ...s, selected: [...s.selected] }));
      while (next.length <= qi) next.push(emptyState());
      next[qi].freeText = text;
      return next;
    });
  }

  function handleSubmit() {
    const answers: Record<string, string> = {};
    questions.forEach((q, i) => {
      const st = states[i] || emptyState();
      const answer = formatClarificationAnswer(q, st.selected, st.freeText);
      if (answer) answers[q.question] = answer;
    });
    if (Object.keys(answers).length === 0) return;
    onSubmit(answers);
  }

  return (
    <div className="panel border-accent/30 bg-accent-soft/40 p-4 animate-fade-up">
      <p className="text-xs font-semibold uppercase tracking-wider text-accent-strong">
        Clarification needed
      </p>
      {payload.reason ? (
        <p className="mt-1 text-sm text-ink-600">{payload.reason}</p>
      ) : null}

      <div className="mt-3 space-y-4">
        {questions.map((q, qi) => (
          <QuestionBlock
            key={`${qi}-${q.question}`}
            question={q}
            state={states[qi] || emptyState()}
            busy={busy}
            onToggle={(label) => toggleOption(qi, label, Boolean(q.multi_select))}
            onFreeText={(text) => setFreeText(qi, text)}
          />
        ))}
      </div>

      <div className="mt-3">
        <button
          type="button"
          className="btn-primary"
          disabled={busy || !canSubmit}
          onClick={handleSubmit}
        >
          Continue
        </button>
      </div>
    </div>
  );
}

function QuestionBlock({
  question,
  state,
  busy,
  onToggle,
  onFreeText,
}: {
  question: ClarificationQuestion;
  state: QuestionState;
  busy?: boolean;
  onToggle: (label: string) => void;
  onFreeText: (text: string) => void;
}) {
  const options = question.options || [];
  const multi = Boolean(question.multi_select);
  const allowFreeText =
    question.allow_free_text !== false && options.length === 0
      ? true
      : question.allow_free_text !== false;

  return (
    <div>
      {question.header ? (
        <p className="mb-1 text-[10px] font-semibold uppercase tracking-wider text-ink-400">
          {question.header}
        </p>
      ) : null}
      <p className="text-sm font-medium text-ink-900">{question.question}</p>

      {options.length > 0 && (
        <div className="mt-2 space-y-2">
          {options.map((opt) => {
            const checked = state.selected.includes(opt.label);
            const inputType = multi ? "checkbox" : "radio";
            return (
              <label
                key={opt.label}
                className={`flex cursor-pointer items-start gap-2 rounded-xl border px-3 py-2 text-sm ${
                  checked
                    ? "border-accent bg-white/90"
                    : "border-ink-200/70 bg-white/60"
                }`}
              >
                <input
                  type={inputType}
                  className="mt-0.5"
                  checked={checked}
                  disabled={busy}
                  onChange={() => onToggle(opt.label)}
                />
                <span>
                  <span className="font-medium text-ink-900">{opt.label}</span>
                  {opt.description ? (
                    <span className="mt-0.5 block text-xs text-ink-500">
                      {opt.description}
                    </span>
                  ) : null}
                </span>
              </label>
            );
          })}
        </div>
      )}

      {allowFreeText && (
        <textarea
          className="mt-2 w-full rounded-xl border border-ink-200/80 bg-white/80 px-3 py-2 text-sm text-ink-900"
          rows={options.length ? 2 : 3}
          placeholder={options.length ? "Or type a custom answer…" : "Your answer…"}
          value={state.freeText}
          disabled={busy}
          onChange={(e) => onFreeText(e.target.value)}
        />
      )}
    </div>
  );
}
