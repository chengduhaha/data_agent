/** Format executed Vertica SQL for assistant answer body (wiki-style). */

export type ExecutedQuery = {
  sql: string;
  tool: string;
};

export function formatExecutedSqlSection(queries: ExecutedQuery[]): string {
  if (!queries.length) return "";

  const parts: string[] = ["\n\n---\n\n## Vertica validation\n"];
  for (let i = 0; i < queries.length; i++) {
    const q = queries[i];
    if (queries.length > 1) {
      parts.push(`\n### Query ${i + 1} (${q.tool})\n`);
    }
    parts.push(`\n\`\`\`sql\n${q.sql}\n\`\`\`\n`);
  }
  return parts.join("");
}

export function parseExecutedSqlEvent(
  data: Record<string, unknown>
): ExecutedQuery[] {
  const raw = data.queries;
  if (!Array.isArray(raw)) return [];
  const out: ExecutedQuery[] = [];
  for (const item of raw) {
    if (!item || typeof item !== "object") continue;
    const rec = item as Record<string, unknown>;
    const sql = typeof rec.sql === "string" ? rec.sql.trim() : "";
    if (!sql) continue;
    out.push({
      sql,
      tool: typeof rec.tool === "string" ? rec.tool : "run_query_safely",
    });
  }
  return out;
}
