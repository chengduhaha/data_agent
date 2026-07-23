export type SlashSkillExtensions = {
  rules?: string[];
  tools?: string[];
  mcp?: string[];
};

export type SlashSkill = {
  name: string;
  description: string;
  source: "builtin" | "org" | "user";
  extensions?: SlashSkillExtensions;
};

export function skillVirtualPath(skill: SlashSkill): string {
  const dir =
    skill.source === "builtin"
      ? "builtin"
      : skill.source === "org"
        ? "org"
        : "user";
  return `/skills/${dir}/${skill.name}/SKILL.md`;
}

/** Text before cursor matches an in-progress `/skill` token. */
export function parseSlashSkillQuery(
  text: string,
  cursor: number
): { query: string; start: number } | null {
  const before = text.slice(0, cursor);
  const match = before.match(/(?:^|\s)\/([\w-]*)$/);
  if (!match) return null;
  const token = match[0];
  const start = before.length - token.length + (token.startsWith(" ") ? 1 : 0);
  return { query: match[1], start };
}

export function filterSlashSkills(skills: SlashSkill[], query: string): SlashSkill[] {
  const q = query.toLowerCase();
  return skills.filter(
    (s) =>
      s.name.toLowerCase().includes(q) ||
      s.description.toLowerCase().includes(q)
  );
}

/** Expand `/skill-name …` into an agent instruction (Cursor-style slash invoke).
 *
 * Any extra rule fragments a skill needs are declared in its own SKILL.md
 * frontmatter (`extensions.rules`) and resolved on the backend — this stays
 * generic so a new skill never requires a frontend code change.
 */
export function expandSkillMessage(text: string, skills: SlashSkill[]): string {
  const trimmed = text.trim();
  const match = trimmed.match(/^\/([\w-]+)(?:\s+([\s\S]*))?$/);
  if (!match) return text;

  const [, name, body] = match;
  const skill = skills.find((s) => s.name === name);
  if (!skill) return text;

  const path = skillVirtualPath(skill);
  const task = (body || "").trim() || "Follow the skill workflow for my request.";
  const rules = skill.extensions?.rules || [];
  const extra = rules.length
    ? `\n\nAfter reading the skill, also read: ${rules.map((r) => `\`${r}\``).join(", ")}.`
    : "";
  return (
    `Use skill "${name}". Read and follow \`${path}\` before answering.\n\n` +
    `User request:\n${task}` +
    extra
  );
}

export function sourceLabel(source: SlashSkill["source"]): string {
  if (source === "user") return "Personal";
  if (source === "org") return "Shared";
  return "Built-in";
}
