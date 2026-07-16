"use client";

export type ContinuePromptPayload = {
  thread_id?: string;
  run_segment?: number;
  steps_used?: number;
  steps_limit?: number;
  message?: string;
};

export function ContinuePanel({
  payload,
  onContinue,
  busy,
}: {
  payload: ContinuePromptPayload;
  onContinue: () => void;
  busy?: boolean;
}) {
  const segment = payload.run_segment ?? 1;
  const steps = payload.steps_used ?? 100;
  const limit = payload.steps_limit ?? steps;

  return (
    <div className="panel border-accent/30 bg-accent-soft/40 p-4 animate-fade-up">
      <p className="text-xs font-semibold uppercase tracking-wider text-accent-strong">
        Continue run
      </p>
      <p className="mt-1 text-sm text-ink-700">
        {payload.message ||
          "The agent reached the tool-step limit for this segment. Continue from the checkpoint or send a new message with tighter constraints."}
      </p>
      <p className="mt-2 text-xs text-ink-500">
        Segment {segment} · {steps} / {limit} tool steps
      </p>
      <div className="mt-3 flex gap-2">
        <button
          type="button"
          className="btn-primary"
          disabled={busy}
          onClick={onContinue}
        >
          Continue
        </button>
      </div>
    </div>
  );
}
