/** Languages that must stay as monospace code blocks. */
const CODE_LANGUAGES = new Set([
  "sql",
  "json",
  "python",
  "py",
  "bash",
  "sh",
  "shell",
  "javascript",
  "js",
  "typescript",
  "ts",
  "yaml",
  "yml",
  "xml",
  "html",
  "css",
  "java",
  "go",
  "rust",
  "c",
  "cpp",
  "csharp",
  "cs",
  "ruby",
  "rb",
  "php",
  "kotlin",
  "swift",
  "scala",
  "r",
  "lua",
  "perl",
  "dockerfile",
  "makefile",
  "graphql",
  "protobuf",
  "proto",
]);

const PROSE_LANGUAGES = new Set(["markdown", "md", "text", "plain", "txt", "prose"]);

/** Heuristic: tool/model text that should render as markdown instead of a monospace block. */
export function looksLikeMarkdown(text: string): boolean {
  const t = text.trim();
  if (!t || t.length < 8) return false;
  if (t.startsWith("{") || t.startsWith("[")) return false;
  if (/^```[\s\S]*```$/m.test(t)) return true;
  return /^#{1,6}\s|^\s*[-*]\s|\|.+\||\*\*[^*]+\*\*/m.test(t);
}

/** Plain-English agent planning / reasoning text (not SQL/JSON). */
export function looksLikeProse(text: string): boolean {
  if (looksLikeMarkdown(text)) return true;
  const t = text.trim();
  if (!t || t.length < 20) return false;
  if (/^(SELECT|INSERT|UPDATE|DELETE|WITH|CREATE|ALTER)\b/im.test(t)) return false;
  if (t.startsWith("{") || t.startsWith("[")) return false;
  if (
    /^(let me|i need to|based on|now i|first,|next,|the user|i'll|i will|i should)/im.test(
      t
    )
  ) {
    return true;
  }
  if (/\n\d+\.\s/.test(t)) return true;
  if (t.length > 60 && /[.!?][\s\n]/.test(t)) return true;
  return false;
}

export function shouldUnwrapFence(lang: string | undefined, body: string): boolean {
  const language = (lang || "").trim().toLowerCase();
  if (language && CODE_LANGUAGES.has(language)) return false;
  if (language && PROSE_LANGUAGES.has(language)) return true;
  return looksLikeProse(body);
}

/** Replace prose-like fenced blocks with their inner markdown body. */
export function unwrapProseCodeFences(content: string): string {
  return content.replace(/```([^\n`]*)\n([\s\S]*?)```/g, (match, lang, body) => {
    if (shouldUnwrapFence(String(lang).trim(), body)) {
      return `\n${String(body).trim()}\n`;
    }
    return match;
  });
}

const SYNTHESIS_HEADING_RE = /^##\s+(?:Summary|Evidence|结论|分析)\b/im;
const BASED_ON_ANSWER_RE = /\bBased\s*on\s+the\s+(?:database|query|evidence|contract)/i;

/**
 * Drop streamed research/planning narration that precedes the user-facing synthesis.
 */
const PLANNING_BEFORE_ANSWER_RE =
  /\b(?:let me|now let me|i found the|good\.|the contract specifies|now i can see|i see \d+ rows|the columns are)\b/i;

export function stripResearchPreamble(content: string): string {
  const text = (content ?? "").trim();
  if (!text) return text;

  const heading = text.search(SYNTHESIS_HEADING_RE);
  if (heading > 0) return text.slice(heading).trimStart();

  const based = text.search(BASED_ON_ANSWER_RE);
  if (based > 0) {
    const before = text.slice(0, based);
    if (PLANNING_BEFORE_ANSWER_RE.test(before) || before.length > 80) {
      return text.slice(based).trimStart();
    }
  }

  const letMeCount = (text.match(/\blet me\b/gi) || []).length;
  if (letMeCount >= 2 && text.length > 400) {
    const answerStart = text.search(
      /(?:##\s+(?:Summary|Evidence)\b|Based on the (?:database|query|evidence|contract))/i
    );
    if (answerStart > 0) return text.slice(answerStart).trimStart();
  }

  const planningOnly =
    /^(?:let me |now let me |i found the |good\.|the contract specifies:|now i can see)/im.test(
      text
    ) && text.length > 400;
  if (planningOnly) {
    const answerStart = text.search(
      /(?:##\s+(?:Summary|Evidence)\b|Based\s*on\s+the\s+(?:database|query|evidence|contract))/i
    );
    if (answerStart > 0) return text.slice(answerStart).trimStart();

    const tableStart = text.search(/\|[^\n]+\|/);
    const keyNotes = text.search(/(?:^|\n)\s*#{0,3}\s*Key\s*Notes\s*:/im);
    const cut = keyNotes >= 0 ? keyNotes : tableStart;
    if (cut > 80) return text.slice(cut).trimStart();
  }

  return text;
}

function normalizeTableRow(row: string): string {
  return row
    .replace(/\s+/g, " ")
    .replace(/\|\s*\|/g, "| ")
    .replace(/^\|\s*/, "| ")
    .replace(/\s*\|$/, " |")
    .trim();
}

function isTableSeparatorRow(row: string): boolean {
  return /^\|\s*:?-{3,}/.test(row.replace(/\s+/g, " "));
}

function pipeCount(row: string): number {
  return (row.match(/\|/g) || []).length;
}

function splitGluedTableRows(flat: string): string[] {
  const chunks = flat
    .split(
      /(?<=%)\s*(?=\|\s*(?:\|\s*)?(?:January|February|March|April|May|June|July|August|September|October|November|December))/i
    )
    .flatMap((chunk) => chunk.split(/\s*\|\|\s*(?=\|\s*(?:January|February|March|April|May|June|July|August|September|October|November|December))/i));
  return chunks.map((c) => c.trim()).filter(Boolean);
}

/** Join vertically fragmented `| cell |` lines into GFM table rows. */
export function reassembleFragmentedTable(content: string): string {
  const lines = content.split("\n");
  const out: string[] = [];
  let i = 0;

  while (i < lines.length) {
    const trimmed = lines[i].trim();
    if (!trimmed.startsWith("|")) {
      out.push(lines[i]);
      i++;
      continue;
    }

    const block: string[] = [];
    while (i < lines.length) {
      const t = lines[i].trim();
      if (!t) {
        i++;
        continue;
      }
      if (!t.includes("|")) break;
      block.push(t);
      i++;
    }

    if (block.length < 2) {
      out.push(...block);
      continue;
    }

    if (block.some((row) => pipeCount(row) >= 5)) {
      out.push(...block.map(normalizeTableRow));
      continue;
    }

    const flat = block.join(" ").replace(/\|\|/g, " | ");
    const glued = splitGluedTableRows(flat);
    if (glued.length > 1) {
      for (const chunk of glued) {
        const row = normalizeTableRow(chunk);
        if (row.includes("|")) out.push(row);
      }
      continue;
    }

    let current = "";
    for (const part of block) {
      if (!current) {
        current = part;
        continue;
      }
      if (isTableSeparatorRow(part)) {
        if (current) out.push(normalizeTableRow(current));
        out.push(normalizeTableRow(part));
        current = "";
        continue;
      }
      if (pipeCount(current) < 6) {
        current = `${current} ${part.replace(/^\|/, "|")}`;
      } else {
        out.push(normalizeTableRow(current));
        current = part;
      }
    }
    if (current) out.push(normalizeTableRow(current));
  }

  return out.join("\n");
}

/**
 * Repair common streaming/model glitches so GFM tables and headings parse.
 * - Headings glued to prior text ("February## Summary")
 * - Table separator merged with header row ("| Var || :--- |")
 * - Section titles without leading newlines
 */
export function repairMarkdownStructure(content: string): string {
  let text = content ?? "";
  if (!text.trim()) return text;

  // "## Summary" / "### Evidence" glued to previous word
  text = text.replace(/([^\n#])(#{1,6}\s)/g, "$1\n\n$2");
  // Horizontal rule glued to text (not table separators like :---)
  text = text.replace(/([^\n|:\-])\n?---\n(?!:)/g, "$1\n\n---\n\n");
  // Table separator row stuck on same line as header/data ("| Mar || :--- |")
  text = text.replace(/\|\|(\s*:?-{3,})/g, "|\n|$1");
  // Prose glued to table ("Totals below| A | B |")
  text = text.replace(/([a-zA-Z0-9%)])(\| [^|\n]+)/g, "$1\n\n$2");
  // Key notes glued to last table cell ("| 2.16% |KeyNotes:")
  text = text.replace(/\|(\s*Key\s*Notes\b)/gi, "|\n\n## Key Notes");
  // Bold section labels glued to body text ("**Evidence**Data execution...")
  text = text.replace(
    /\*\*\s*(Summary|Evidence|Analysis\s*approach\s*&\s*confidence|摘要|证据|分析思路与信心)\s*\*\*(?=\S)/gi,
    (_match, label) => `## ${String(label).replace(/\s+/g, " ").trim()}\n\n`
  );
  text = text.replace(/\bAnalysisapproach\b/gi, "Analysis approach");
  text = text.replace(/\bDataExecution\b/g, "Data Execution");
  // Remove blank lines inside pipe-table blocks
  text = text.replace(/(^\s*\|[^\n]*)\n\n+(?=^\s*\|)/gm, "$1\n");
  // Light word glue repair before headings ("FebruarySummary")
  text = text.replace(/([a-z])(Summary|Evidence)\b/g, "$1 $2");
  text = text.replace(/Basedon/gi, "Based on");
  text = text.replace(/databasequery/gi, "database query");
  text = text.replace(/forPM\b/gi, "for PM");
  text = text.replace(/PM ID(\d+)/gi, "PM ID $1");
  text = text.replace(/hereis/gi, "here is");
  text = text.replace(/datafor/gi, "data for");
  text = text.replace(/broken downby/gi, "broken down by");
  text = text.replace(/andApril/gi, "and April");
  text = text.replace(/(January|February|March|April|May|June|July|August|September|October|November|December)(\d{4})/gi, "$1 $2");
  // Collapse 3+ newlines to 2
  text = text.replace(/\n{3,}/g, "\n\n");
  return text;
}

/**
 * Unwrap prose code fences and normalize narrative before markdown preview.
 * Handles ```, ```text, ```markdown, and streaming open fences.
 */
export function normalizeNarrativeMarkdown(content: string, streaming = false): string {
  let text = content ?? "";
  const trimmed = text.trim();
  if (!trimmed) return text;

  const singleFence = trimmed.match(/^```([^\n`]*)\s*\n([\s\S]*?)\n```\s*$/);
  if (singleFence && shouldUnwrapFence(singleFence[1].trim(), singleFence[2])) {
    text = singleFence[2];
  } else {
    const openFence = trimmed.match(/^```([^\n`]*)\s*\n([\s\S]*)$/);
    if (openFence && shouldUnwrapFence(openFence[1].trim(), openFence[2])) {
      // Strip a leading prose fence while streaming or when the fence never closed.
      if (streaming || !trimmed.includes("\n```")) {
        text = openFence[2];
      }
    }
  }

  return repairMarkdownStructure(
    reassembleFragmentedTable(stripResearchPreamble(unwrapProseCodeFences(text)))
  );
}

/** Whether a string payload should use markdown preview (tools, subagents, etc.). */
export function shouldRenderAsMarkdown(text: string): boolean {
  return looksLikeProse(normalizeNarrativeMarkdown(text));
}
