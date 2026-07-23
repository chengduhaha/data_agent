"use client";

type Thread = {
  thread_id: string;
  title?: string;
  updated_at?: string | null;
};

export function ThreadSidebar({
  threads,
  activeId,
  onSelect,
  onNew,
  onDelete,
}: {
  threads: Thread[];
  activeId: string | null;
  onSelect: (id: string) => void;
  onNew: () => void;
  onDelete?: (id: string) => void;
}) {
  return (
    <aside className="panel flex min-h-0 w-full shrink-0 flex-col overflow-hidden md:w-60">
      <div className="flex items-center justify-between border-b border-ink-200/60 px-3 py-3">
        <p className="text-xs font-semibold uppercase tracking-wider text-ink-400">
          Chats
        </p>
        <button type="button" className="btn-ghost !px-2 !py-1 text-xs" onClick={onNew}>
          New
        </button>
      </div>
      <ul className="min-h-0 max-h-48 flex-1 space-y-0.5 overflow-y-auto p-2 md:max-h-none">
        {threads.length === 0 && (
          <li className="px-2 py-3 text-xs text-ink-400">No chats yet</li>
        )}
        {threads.map((t) => {
          const label = t.title?.trim() || `${t.thread_id.slice(0, 8)}…`;
          return (
            <li key={t.thread_id} className="group relative">
              <button
                type="button"
                onClick={() => onSelect(t.thread_id)}
                className={`w-full rounded-xl px-2.5 py-2 pr-8 text-left text-xs transition ${
                  activeId === t.thread_id
                    ? "bg-ink-900 text-white"
                    : "text-ink-600 hover:bg-ink-50"
                }`}
                title={label}
              >
                <span className="line-clamp-2 leading-snug">{label}</span>
              </button>
              {onDelete && (
                <button
                  type="button"
                  title="Delete chat"
                  aria-label={`Delete chat ${label}`}
                  onClick={(e) => {
                    e.stopPropagation();
                    if (window.confirm(`Delete "${label}"? This cannot be undone.`)) {
                      onDelete(t.thread_id);
                    }
                  }}
                  className={`absolute right-1.5 top-1/2 -translate-y-1/2 rounded-lg px-1.5 py-0.5 text-[11px] opacity-0 transition group-hover:opacity-100 ${
                    activeId === t.thread_id
                      ? "text-white/80 hover:bg-white/15 hover:text-white"
                      : "text-ink-400 hover:bg-red-50 hover:text-red-600"
                  }`}
                >
                  ⌫
                </button>
              )}
            </li>
          );
        })}
      </ul>
    </aside>
  );
}
