"use client";

export function ScrollToBottom({
  visible,
  onClick,
}: {
  visible: boolean;
  onClick: () => void;
}) {
  if (!visible) return null;
  return (
    <button
      type="button"
      onClick={onClick}
      className="sticky bottom-3 z-10 ml-auto mr-3 flex w-fit items-center gap-1 rounded-full border border-ink-200 bg-white/90 px-3 py-1.5 text-xs font-medium text-ink-600 shadow-soft transition hover:bg-white"
    >
      <span aria-hidden>↓</span> New messages
    </button>
  );
}
