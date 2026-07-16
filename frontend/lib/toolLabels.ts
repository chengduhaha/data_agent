/** Map tool names (+ input sniff) to Cursor-style friendly step labels. */

function asRecord(input: unknown): Record<string, unknown> | null {
  if (input && typeof input === "object" && !Array.isArray(input)) {
    return input as Record<string, unknown>;
  }
  return null;
}

function shortPath(path: string): string {
  const cleaned = path.replace(/^\/workspace\//, "").replace(/^\/skills\//, "skills/");
  if (cleaned.length <= 48) return cleaned;
  const parts = cleaned.split("/");
  if (parts.length <= 2) return `…${cleaned.slice(-45)}`;
  return `…/${parts.slice(-2).join("/")}`;
}

function sniffCommand(input: unknown): string {
  const rec = asRecord(input);
  if (!rec) return typeof input === "string" ? input : "";
  const cmd = rec.command ?? rec.cmd ?? rec.script;
  return typeof cmd === "string" ? cmd : "";
}

export function toolStepLabel(tool: string, input?: unknown): string {
  const name = (tool || "tool").toLowerCase();
  const rec = asRecord(input);

  if (name === "read_file" || name === "read") {
    const path = String(rec?.file_path ?? rec?.path ?? "");
    return path ? `Reading ${shortPath(path)}` : "Reading file";
  }
  if (name === "write_file" || name === "write") {
    const path = String(rec?.file_path ?? rec?.path ?? "");
    return path ? `Writing ${shortPath(path)}` : "Writing file";
  }
  if (name === "edit_file" || name === "edit") {
    const path = String(rec?.file_path ?? rec?.path ?? "");
    return path ? `Editing ${shortPath(path)}` : "Editing file";
  }
  if (name === "ls") {
    const path = String(rec?.path ?? "");
    return path ? `Listing ${shortPath(path)}` : "Listing directory";
  }
  if (name === "glob") {
    return `Finding files${rec?.pattern ? `: ${rec.pattern}` : ""}`;
  }
  if (name === "grep") {
    const pattern = String(rec?.pattern ?? rec?.query ?? "");
    return pattern ? `Searching “${pattern.slice(0, 40)}”` : "Searching files";
  }
  if (name === "execute" || name === "shell" || name === "bash") {
    const cmd = sniffCommand(input);
    if (/run_query|wkb\.indexing|tools\.wkb/i.test(cmd)) return "WKB retrieval";
    if (/index_builder/i.test(cmd)) return "Building WKB index";
    if (cmd) {
      const short = cmd.length > 56 ? `${cmd.slice(0, 56)}…` : cmd;
      return `Running: ${short}`;
    }
    return "Running shell command";
  }
  if (name === "run_query_safely" || name === "execute_query_paginated") {
    return "Querying Vertica";
  }
  if (name.includes("vertica") || name.includes("run_query")) {
    return "Querying Vertica";
  }
  if (name === "write_todos" || name === "todowrite") {
    return "Planning steps";
  }
  if (name === "task") {
    return "Delegating to subagent";
  }
  if (name === "web_fetch") {
    const url = String(rec?.url ?? "");
    return url ? `Fetching ${url.slice(0, 48)}` : "Fetching URL";
  }
  if (name === "web_search") {
    const q = String(rec?.query ?? "");
    return q ? `Searching web: ${q.slice(0, 40)}` : "Searching the web";
  }

  return tool || "Tool";
}

export function toolStepDetail(input?: unknown): string | null {
  const rec = asRecord(input);
  if (!rec) {
    if (typeof input === "string" && input.trim()) return input.slice(0, 200);
    return null;
  }
  const cmd = sniffCommand(input);
  if (cmd) return cmd.length > 160 ? `${cmd.slice(0, 160)}…` : cmd;
  const query = rec.query;
  if (typeof query === "string" && query.trim()) {
    const oneLine = query.replace(/\s+/g, " ").trim();
    return oneLine.length > 160 ? `${oneLine.slice(0, 160)}…` : oneLine;
  }
  return null;
}
