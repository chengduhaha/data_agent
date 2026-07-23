"use client";

import { useEffect, useState } from "react";
import { apiGet, apiSend } from "@/lib/api";

type Skill = {
  name: string;
  description: string;
  source: "builtin" | "org" | "user";
  path: string;
  content?: string | null;
  editable?: boolean;
  disabled?: boolean;
};

const SOURCE_LABEL: Record<Skill["source"], string> = {
  builtin: "Platform",
  org: "Shared",
  user: "Personal",
};

function sourceBadgeClass(source: Skill["source"]) {
  if (source === "user") return "bg-accent-soft text-accent-strong";
  if (source === "org") return "bg-teal-50 text-teal-800";
  return "bg-ink-100 text-ink-600";
}

export default function SkillsSettingsPage() {
  const [skills, setSkills] = useState<Skill[]>([]);
  const [selected, setSelected] = useState<Skill | null>(null);
  const [content, setContent] = useState("");
  const [newName, setNewName] = useState("");
  const [status, setStatus] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const [disabledSkills, setDisabledSkills] = useState<string[]>([]);
  const shared = skills.filter((s) => s.source === "builtin" || s.source === "org");
  const personal = skills.filter((s) => s.source === "user");

  async function refresh() {
    const data = await apiGet<{ skills: Skill[] }>("/api/skills?include_disabled=true");
    setSkills(data.skills || []);
    const cfg = await apiGet<{ disabled_skills?: string[] }>("/api/config");
    setDisabledSkills(cfg.disabled_skills || []);
  }

  useEffect(() => {
    void refresh().catch((e) => setError((e as Error).message));
  }, []);

  async function toggleSkill(name: string, disable: boolean) {
    setError(null);
    try {
      const cfg = await apiGet<Record<string, unknown>>("/api/config");
      const next = disable
        ? Array.from(new Set([...(cfg.disabled_skills as string[] || []), name]))
        : ((cfg.disabled_skills as string[]) || []).filter((n) => n !== name);
      await apiSend("/api/config", "PUT", { ...cfg, disabled_skills: next });
      setDisabledSkills(next);
      await refresh();
    } catch (e) {
      setError((e as Error).message);
    }
  }

  async function openSkill(s: Skill) {
    setError(null);
    const full = await apiGet<Skill>(
      `/api/skills/${encodeURIComponent(s.name)}?source=${s.source}`
    );
    setSelected(full);
    setContent(full.content || "");
  }

  async function save() {
    if (!selected || !selected.editable) return;
    setStatus(null);
    try {
      await apiSend(`/api/skills/${encodeURIComponent(selected.name)}`, "PUT", {
        name: selected.name,
        content,
      });
      setStatus("Saved.");
      await refresh();
    } catch (e) {
      setError((e as Error).message);
    }
  }

  async function createSkill() {
    const name = newName.trim();
    if (!name) return;
    const body = `---\nname: ${name}\ndescription: \n---\n\n# ${name}\n\nInstructions go here.\n`;
    try {
      await apiSend(`/api/skills/${encodeURIComponent(name)}`, "PUT", {
        name,
        content: body,
      });
      setNewName("");
      await refresh();
      setSelected({ name, description: "", source: "user", path: "", content: body, editable: true });
      setContent(body);
    } catch (e) {
      setError((e as Error).message);
    }
  }

  async function remove() {
    if (!selected || !selected.editable) return;
    try {
      await apiSend(`/api/skills/${encodeURIComponent(selected.name)}`, "DELETE");
      setSelected(null);
      setContent("");
      await refresh();
    } catch (e) {
      setError((e as Error).message);
    }
  }

  function SkillList({ items, title }: { items: Skill[]; title: string }) {
    if (items.length === 0) return null;
    return (
      <div className="space-y-1">
        <p className="px-1 text-[10px] font-semibold uppercase tracking-wider text-ink-400">
          {title}
        </p>
        <ul className="space-y-1">
          {items.map((s) => (
            <li key={`${s.source}-${s.name}`} className="flex items-center gap-1">
              <button
                type="button"
                onClick={() => void openSkill(s)}
                className={`flex-1 rounded-xl px-3 py-2 text-left text-sm transition ${
                  selected?.name === s.name && selected?.source === s.source
                    ? "bg-accent-soft text-accent-strong"
                    : "hover:bg-ink-50"
                } ${disabledSkills.includes(s.name) ? "opacity-50" : ""}`}
              >
                <span className="font-medium">{s.name}</span>
                <span
                  className={`ml-2 inline-block rounded-md px-1.5 py-0.5 text-[10px] font-semibold uppercase ${sourceBadgeClass(s.source)}`}
                >
                  {SOURCE_LABEL[s.source]}
                </span>
              </button>
              {s.source !== "user" && (
                <input
                  type="checkbox"
                  title="Enabled"
                  checked={!disabledSkills.includes(s.name)}
                  onChange={(e) => void toggleSkill(s.name, !e.target.checked)}
                />
              )}
            </li>
          ))}
        </ul>
      </div>
    );
  }

  return (
    <div className="space-y-6 animate-fade-up">
      <div>
        <h1 className="font-display text-2xl text-ink-900">Skills</h1>
        <p className="mt-1 text-sm text-ink-500">
          Shared organization skills are read-only. Personal skills override by name.
        </p>
      </div>
      <div className="grid gap-4 lg:grid-cols-[260px_1fr]">
        <div className="space-y-4">
          <SkillList items={shared} title="Shared" />
          <SkillList items={personal} title="Personal" />
          <div className="flex gap-1 border-t border-ink-100 pt-3">
            <input
              className="input text-xs"
              placeholder="new-skill"
              value={newName}
              onChange={(e) => setNewName(e.target.value)}
            />
            <button type="button" className="btn-ghost !px-2" onClick={() => void createSkill()}>
              Add
            </button>
          </div>
        </div>
        <div>
          {selected ? (
            <>
              <textarea
                className="input min-h-[360px] font-mono text-xs"
                value={content}
                disabled={!selected.editable}
                onChange={(e) => setContent(e.target.value)}
                spellCheck={false}
              />
              <div className="mt-3 flex gap-2">
                {selected.editable ? (
                  <>
                    <button type="button" className="btn-primary" onClick={() => void save()}>
                      Save
                    </button>
                    <button type="button" className="btn-ghost" onClick={() => void remove()}>
                      Delete
                    </button>
                  </>
                ) : (
                  <p className="text-sm text-ink-400">
                    {SOURCE_LABEL[selected.source]} skills are read-only.
                  </p>
                )}
                {status && <span className="text-sm text-accent">{status}</span>}
              </div>
            </>
          ) : (
            <p className="text-sm text-ink-400">Select a skill to view or edit.</p>
          )}
          {error && <p className="mt-2 text-sm text-red-600">{error}</p>}
        </div>
      </div>
    </div>
  );
}
