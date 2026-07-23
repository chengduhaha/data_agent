/** Structured executed-query data for the collapsible appendix (generic, not vendor-specific). */

export type QueryAppendixItem = {
  sql: string;
  tool: string;
};

export function parseQueryAppendixEvent(
  data: Record<string, unknown>
): QueryAppendixItem[] {
  const raw = data.queries;
  if (!Array.isArray(raw)) return [];
  const out: QueryAppendixItem[] = [];
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
