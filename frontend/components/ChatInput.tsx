"use client";

import {
  useCallback,
  useEffect,
  useMemo,
  useRef,
  useState,
  type KeyboardEvent,
} from "react";
import {
  filterSlashSkills,
  parseSlashSkillQuery,
  type SlashSkill,
} from "@/lib/skillSlash";
import { SkillSlashMenu } from "./SkillSlashMenu";

const MIN_ROWS = 3;
const DEFAULT_HEIGHT_PX = 88;

export function ChatInput({
  value,
  onChange,
  onSend,
  skills,
  disabled,
  placeholder = "Message Data Agent… (type / for skills)",
}: {
  value: string;
  onChange: (value: string) => void;
  onSend: () => void;
  skills: SlashSkill[];
  disabled?: boolean;
  placeholder?: string;
}) {
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const [menuOpen, setMenuOpen] = useState(false);
  const [slashStart, setSlashStart] = useState(0);
  const [slashQuery, setSlashQuery] = useState("");
  const [highlightIndex, setHighlightIndex] = useState(0);
  const [activeSkill, setActiveSkill] = useState<SlashSkill | null>(null);

  const filtered = useMemo(
    () => filterSlashSkills(skills, slashQuery),
    [skills, slashQuery]
  );

  const syncSlashMenu = useCallback(
    (text: string, cursor: number, resetHighlight = false) => {
      const parsed = parseSlashSkillQuery(text, cursor);
      if (!parsed) {
        setMenuOpen(false);
        setSlashQuery("");
        return;
      }
      setMenuOpen(true);
      setSlashStart(parsed.start);
      setSlashQuery((prev) => {
        if (resetHighlight || prev !== parsed.query) {
          setHighlightIndex(0);
        }
        return parsed.query;
      });
    },
    []
  );

  useEffect(() => {
    if (!menuOpen) return;
    setHighlightIndex((i) => Math.min(i, Math.max(0, filtered.length - 1)));
  }, [filtered.length, menuOpen]);

  function insertSkill(skill: SlashSkill) {
    const el = textareaRef.current;
    const cursor = el?.selectionStart ?? value.length;
    const parsed = parseSlashSkillQuery(value, cursor);
    if (!parsed) return;

    const before = value.slice(0, parsed.start);
    const after = value.slice(cursor);
    const insertion = `/${skill.name} `;
    const next = `${before}${insertion}${after}`;
    onChange(next);
    setActiveSkill(skill);
    setMenuOpen(false);
    setSlashQuery("");

    requestAnimationFrame(() => {
      const pos = before.length + insertion.length;
      el?.focus();
      el?.setSelectionRange(pos, pos);
    });
  }

  function handleChange(text: string) {
    onChange(text);
    const cursor = textareaRef.current?.selectionStart ?? text.length;
    syncSlashMenu(text, cursor, true);

    const trimmed = text.trim();
    if (activeSkill && !trimmed.startsWith(`/${activeSkill.name}`)) {
      setActiveSkill(null);
    }
  }

  function handleKeyDown(e: KeyboardEvent<HTMLTextAreaElement>) {
    if (menuOpen && filtered.length > 0) {
      if (e.key === "ArrowDown") {
        e.preventDefault();
        e.stopPropagation();
        setHighlightIndex((i) => (i + 1) % filtered.length);
        return;
      }
      if (e.key === "ArrowUp") {
        e.preventDefault();
        e.stopPropagation();
        setHighlightIndex((i) => (i - 1 + filtered.length) % filtered.length);
        return;
      }
      if (e.key === "Enter" || e.key === "Tab") {
        e.preventDefault();
        insertSkill(filtered[highlightIndex]);
        return;
      }
      if (e.key === "Escape") {
        e.preventDefault();
        setMenuOpen(false);
        return;
      }
    }

    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      submit();
    }
  }

  function handleKeyUp(e: KeyboardEvent<HTMLTextAreaElement>) {
    // Arrow/Enter/Tab/Esc are handled in keydown — do not re-sync or the
    // highlight index gets forced back to 0 on every keyup.
    if (
      e.key === "ArrowDown" ||
      e.key === "ArrowUp" ||
      e.key === "Enter" ||
      e.key === "Tab" ||
      e.key === "Escape"
    ) {
      return;
    }
    syncSlashMenu(
      value,
      (e.target as HTMLTextAreaElement).selectionStart
    );
  }

  function submit() {
    const text = value.trim();
    if (!text || disabled) return;
    onSend();
    setActiveSkill(null);
    setMenuOpen(false);
  }

  return (
    <div className="relative w-full">
      {menuOpen && (
        <div className="absolute bottom-full left-0 right-0 z-20 mb-2">
          <SkillSlashMenu
            skills={filtered}
            highlightIndex={highlightIndex}
            onHighlight={setHighlightIndex}
            onSelect={insertSkill}
          />
        </div>
      )}
      {activeSkill && (
        <div className="mb-2 flex items-center gap-2 text-xs text-ink-500">
          <span className="rounded-lg bg-teal-50 px-2 py-0.5 font-medium text-teal-800">
            Skill: /{activeSkill.name}
          </span>
          <span className="text-ink-400">Agent will read SKILL.md on send</span>
        </div>
      )}
      <textarea
        ref={textareaRef}
        className="chat-textarea input"
        rows={MIN_ROWS}
        style={{ height: DEFAULT_HEIGHT_PX }}
        placeholder={placeholder}
        value={value}
        disabled={disabled}
        onChange={(e) => handleChange(e.target.value)}
        onKeyDown={handleKeyDown}
        onClick={(e) =>
          syncSlashMenu(value, (e.target as HTMLTextAreaElement).selectionStart)
        }
        onKeyUp={handleKeyUp}
      />
    </div>
  );
}
