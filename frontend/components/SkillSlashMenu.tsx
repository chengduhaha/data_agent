"use client";

import type { SlashSkill } from "@/lib/skillSlash";
import { sourceLabel } from "@/lib/skillSlash";

export function SkillSlashMenu({
  skills,
  highlightIndex,
  onHighlight,
  onSelect,
}: {
  skills: SlashSkill[];
  highlightIndex: number;
  onHighlight: (index: number) => void;
  onSelect: (skill: SlashSkill) => void;
}) {
  if (skills.length === 0) {
    return (
      <div className="slash-menu">
        <p className="px-3 py-2 text-xs text-ink-400">No matching skills</p>
      </div>
    );
  }

  const highlighted =
    highlightIndex >= 0 && highlightIndex < skills.length
      ? skills[highlightIndex]
      : skills[0];

  return (
    <div className="slash-menu-grid">
      <div className="slash-menu max-h-[min(320px,40vh)] overflow-y-auto">
        <p className="px-3 pb-1 pt-2 text-[10px] font-semibold uppercase tracking-wider text-ink-400">
          Skills
        </p>
        <ul>
          {skills.map((skill, idx) => {
            const active = idx === highlightIndex;
            return (
              <li key={`${skill.source}:${skill.name}`}>
                <button
                  type="button"
                  className={`slash-menu-item ${active ? "slash-menu-item-active" : ""}`}
                  onMouseEnter={() => onHighlight(idx)}
                  onMouseDown={(e) => {
                    e.preventDefault();
                    onSelect(skill);
                  }}
                >
                  <span className="font-mono text-sm font-medium text-ink-900">
                    /{skill.name}
                  </span>
                  <span className="mt-0.5 line-clamp-2 text-xs text-ink-500">
                    {skill.description || sourceLabel(skill.source)}
                  </span>
                </button>
              </li>
            );
          })}
        </ul>
      </div>
      {highlighted && (
        <aside className="slash-menu-preview hidden sm:block">
          <p className="font-mono text-sm font-semibold text-ink-900">
            /{highlighted.name}
          </p>
          <p className="mt-1 text-[10px] font-medium uppercase tracking-wide text-teal-700">
            {sourceLabel(highlighted.source)}
          </p>
          <p className="mt-2 text-xs leading-relaxed text-ink-600">
            {highlighted.description ||
              "Invoke this skill. The agent will read SKILL.md and follow its workflow."}
          </p>
        </aside>
      )}
    </div>
  );
}
