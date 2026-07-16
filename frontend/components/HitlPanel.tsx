"use client";

export function HitlPanel({
  payload,
  onApprove,
  onReject,
  busy,
}: {
  payload: unknown;
  onApprove: () => void;
  onReject: () => void;
  busy?: boolean;
}) {
  return (
    <div className="panel border-warn/30 bg-warn-soft/60 p-4 animate-fade-up">
      <p className="text-xs font-semibold uppercase tracking-wider text-warn">
        Approval required
      </p>
      <p className="mt-1 text-sm text-ink-700">
        The agent wants to run a gated tool (write/execute). Review and approve or reject.
      </p>
      <pre className="mt-3 max-h-40 overflow-auto rounded-xl bg-white/70 p-3 font-mono text-[11px] text-ink-700">
        {typeof payload === "string"
          ? payload
          : JSON.stringify(payload, null, 2)}
      </pre>
      <div className="mt-3 flex gap-2">
        <button
          type="button"
          className="btn-primary"
          disabled={busy}
          onClick={onApprove}
        >
          Approve
        </button>
        <button
          type="button"
          className="btn-ghost"
          disabled={busy}
          onClick={onReject}
        >
          Reject
        </button>
      </div>
    </div>
  );
}
