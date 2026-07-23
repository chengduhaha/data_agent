/**
 * Split an assistant message into narrative (prose/markdown) vs a legacy
 * inline query appendix, and detect "planning" lines that should render as
 * a status strip rather than body text.
 *
 * New messages carry queries in `ChatMessage.queryAppendix` (structured, via
 * the `query_appendix` SSE event) and never need this split. This helper only
 * exists to gracefully render older threads (or `## Query validation` /
 * `## Vertica validation` text) that was persisted with SQL inlined into the
 * message body before this change.
 */

export type SplitAssistantContent = {
  narrative: string;
  queryAppendix: { sql: string; tool?: string }[];
  /** True when the entire message is a bare ```sql block with no narrative — signals an incomplete analysis. */
  appendixOnly: boolean;
};

const APPENDIX_HEADING_RE = /\n{0,2}---\n{0,2}##\s+(?:Query|Vertica)\s+validation\s*\n/i;
const SQL_BLOCK_RE = /```sql\n([\s\S]*?)```/g;

export function splitAssistantContent(content: string): SplitAssistantContent {
  const text = content ?? "";
  const match = text.search(APPENDIX_HEADING_RE);

  if (match === -1) {
    const trimmed = text.trim();
    const onlySql = trimmed.match(/^```sql\n([\s\S]*?)```\s*$/);
    if (onlySql) {
      return {
        narrative: "",
        queryAppendix: [{ sql: onlySql[1].trim() }],
        appendixOnly: true,
      };
    }
    return { narrative: text, queryAppendix: [], appendixOnly: false };
  }

  const narrative = text.slice(0, match).trimEnd();
  const appendixSection = text.slice(match);
  const queries: { sql: string; tool?: string }[] = [];
  let sqlMatch: RegExpExecArray | null;
  SQL_BLOCK_RE.lastIndex = 0;
  while ((sqlMatch = SQL_BLOCK_RE.exec(appendixSection)) !== null) {
    const sql = sqlMatch[1].trim();
    if (sql) queries.push({ sql });
  }

  return {
    narrative,
    queryAppendix: queries,
    appendixOnly: narrative.length === 0 && queries.length > 0,
  };
}

/** Heuristic: a short "Now let me query…" style planning sentence, not a real answer. */
const PLANNING_PREFIXES = [
  "let me ",
  "now let me ",
  "now i ",
  "i'll ",
  "i will ",
  "next, i",
  "first, i",
];

export function isPlanningOnly(text: string, maxLen = 200): boolean {
  const trimmed = (text || "").trim();
  if (!trimmed || trimmed.length > maxLen) return false;
  if (trimmed.includes("##")) return false;
  const lower = trimmed.toLowerCase();
  return PLANNING_PREFIXES.some((p) => lower.startsWith(p));
}
