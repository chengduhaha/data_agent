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

/** True when text looks like planning / tool narration rather than a delivered answer. */
export function looksLikePlanningPreamble(text: string): boolean {
  const t = (text ?? "").trim();
  if (!t) return true;
  if (t.length < 40) return PLANNING_BEFORE_ANSWER_RE.test(t) || /^(?:let me |now let me |i'll |i will )/im.test(t);
  const letMeCount = (t.match(/\blet me\b/gi) || []).length;
  if (letMeCount >= 2 && t.length < 600) return true;
  if (/^(?:let me |now let me |i found the |good\.|the contract specifies:|now i can see)/im.test(t)) {
    // Pure planning stub — no tables / sectioned analysis yet.
    if (!/\|.+\|/.test(t) && !/(?:^|\n)\s*[A-D][\.、]\s+\S/.test(t) && !SYNTHESIS_HEADING_RE.test(t)) {
      return true;
    }
  }
  return false;
}

/**
 * Substantial user-facing answer already present (Chinese sectioned reports, tables, etc.).
 * Used so a late wrap-up `## Summary` does not erase an earlier streamed answer.
 */
export function looksLikeSubstantialAnswer(text: string): boolean {
  const t = (text ?? "").trim();
  if (!t || t.length < 200) return false;
  if (SYNTHESIS_HEADING_RE.test(t)) return true;
  if (BASED_ON_ANSWER_RE.test(t) && t.length > 280) return true;
  const tablePipes = (t.match(/\|/g) || []).length;
  if (tablePipes >= 8 && t.length > 280) return true;
  // Sectioned analysis: "A. …" / "C. 供应商" / "### …"
  if (/(?:^|\n)\s*[A-D][\.、]\s+\S{2,}/m.test(t) && t.length > 280) return true;
  if (/(?:^|\n)#{2,3}\s+\S+/m.test(t) && t.length > 280) return true;
  // Long CJK analysis body
  const cjk = (t.match(/[\u4e00-\u9fff]/g) || []).join("").length;
  if (cjk >= 120 && t.length > 400) return true;
  return false;
}

export function stripResearchPreamble(content: string): string {
  const text = (content ?? "").trim();
  if (!text) return text;

  const heading = text.search(SYNTHESIS_HEADING_RE);
  if (heading > 0) {
    const before = text.slice(0, heading).trimEnd();
    const after = text.slice(heading).trimStart();
    // Wrap-up often appends `## Summary` AFTER a full streamed answer. Prefer the
    // already-delivered answer so the UI does not "lose" it when steps finish.
    if (looksLikeSubstantialAnswer(before)) {
      if (!looksLikeSubstantialAnswer(after) || before.length >= after.length) {
        return before;
      }
    }
    if (looksLikePlanningPreamble(before) || before.length < 120) {
      return after;
    }
    // Mixed: keep both, with the synthesis heading as the start of the final block.
    return `${before}\n\n${after}`.trim();
  }

  const based = text.search(BASED_ON_ANSWER_RE);
  if (based > 0) {
    const before = text.slice(0, based);
    if (looksLikePlanningPreamble(before) || (before.length > 80 && !looksLikeSubstantialAnswer(before))) {
      return text.slice(based).trimStart();
    }
  }

  const letMeCount = (text.match(/\blet me\b/gi) || []).length;
  if (letMeCount >= 2 && text.length > 400) {
    const answerStart = text.search(
      /(?:##\s+(?:Summary|Evidence)\b|Based on the (?:database|query|evidence|contract))/i
    );
    if (answerStart > 0) {
      const before = text.slice(0, answerStart);
      if (!looksLikeSubstantialAnswer(before)) {
        return text.slice(answerStart).trimStart();
      }
    }
  }

  const planningOnly =
    /^(?:let me |now let me |i found the |good\.|the contract specifies:|now i can see)/im.test(
      text
    ) && text.length > 400;
  if (planningOnly && !looksLikeSubstantialAnswer(text)) {
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

function mergeLowPipeFragments(rows: string[]): string {
  let current = "";
  for (const row of rows) {
    if (!current) {
      current = row;
      continue;
    }
    if (isTableSeparatorRow(row)) {
      break;
    }
    current = `${current} ${row.replace(/^\|/, "|")}`;
  }
  return normalizeTableRow(current);
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
        // Allow a single blank line inside a fragmented header (low pipe count).
        if (
          block.length > 0 &&
          i + 1 < lines.length &&
          lines[i + 1].trim().includes("|") &&
          pipeCount(block[block.length - 1]) < 5
        ) {
          i++;
          continue;
        }
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
      const headerFrag: string[] = [];
      let idx = 0;
      while (
        idx < block.length &&
        pipeCount(block[idx]) < 5 &&
        !isTableSeparatorRow(block[idx]) &&
        !/^\|\s*-?\d+\s*\|/.test(block[idx])
      ) {
        headerFrag.push(block[idx]);
        idx++;
      }
      if (headerFrag.length > 1) {
        out.push(mergeLowPipeFragments(headerFrag));
      } else if (headerFrag.length === 1) {
        out.push(normalizeTableRow(headerFrag[0]));
      }
      for (const row of block.slice(idx)) {
        out.push(normalizeTableRow(row));
      }
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

    // Reaching here: no row has >=5 pipes (all low-pipe) and no glued split.
    // If a GFM separator row is present, this is a clean/well-formed table where
    // each line is an independent row — do NOT merge, or a multi-row table
    // (e.g. 10 rows of 2 columns) collapses to half its rows.
    if (block.some(isTableSeparatorRow)) {
      for (const row of block) {
        out.push(normalizeTableRow(row));
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
 * Split multiple GFM rows glued on one physical line ("| ... | | 1 | ... | | 2 |").
 */
function splitWideTableRow(line: string): string[] {
  const trimmed = line.trim();
  if (!trimmed.startsWith("|") || isTableSeparatorRow(trimmed)) {
    return [line];
  }
  // Two logical rows on one line without double pipe: "| 1 | a | x | 2 | b | y |"
  if (pipeCount(trimmed) < 7) {
    return [line];
  }
  const rows: string[] = [];
  let rest = trimmed;
  while (rest) {
    const match = rest.match(/\s\|\s+(?=-?\d{1,2}\s*\|)/);
    if (!match || match.index === undefined) {
      const row = rest.trim();
      if (row) rows.push(normalizeTableRow(row));
      break;
    }
    const head = rest.slice(0, match.index).trim();
    if (head) rows.push(normalizeTableRow(head));
    rest = rest.slice(match.index).trim();
    if (rest && !rest.startsWith("|")) rest = `| ${rest}`;
  }
  return rows.length > 1 ? rows : [line];
}

function splitOneGluedTableLine(line: string): string[] {
  const trimmed = line.trim();
  if (!trimmed.startsWith("|")) {
    return [line];
  }

  const wide = splitWideTableRow(line);
  if (wide.length > 1) {
    return wide;
  }

  if (pipeCount(trimmed) < 8) {
    return [line];
  }

  const rows: string[] = [];
  let rest = trimmed;
  while (rest) {
    const match = rest.match(/\s*\|\s*\|\s+(?=-?\d{1,2}\s*\|)/);
    if (!match || match.index === undefined) {
      const row = rest.trim();
      if (row) rows.push(normalizeTableRow(row));
      break;
    }
    const head = rest.slice(0, match.index).trim();
    if (head) {
      let row = head;
      if ((isTableSeparatorRow(row) || /:---/.test(row)) && !row.trimEnd().endsWith("|")) {
        row = `${row.trimEnd()} |`;
      }
      rows.push(normalizeTableRow(row));
    }
    rest = rest.slice(match.index + match[0].length).trimStart();
    if (rest && !rest.startsWith("|")) rest = `| ${rest}`;
  }

  return rows.length > 1 ? rows : [line];
}

export function splitGluedTableRowLines(content: string): string {
  return content.split("\n").flatMap((line) => splitOneGluedTableLine(line)).join("\n");
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
  text = splitGluedTableRowLines(text);
  // Title or prose line immediately before a table row
  text = text.replace(/([^\n|])\n(\| [^\n]+\|)/g, "$1\n\n$2");
  // Prose glued to table ("Totals below| A | B |") — never inside pipe rows
  text = text
    .split("\n")
    .map((line) => {
      if (line.trim().startsWith("|")) return line;
      return line.replace(/([a-zA-Z0-9%)])(\| [^|\n]+)/g, "$1\n\n$2");
    })
    .join("\n");
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
    reassembleFragmentedTable(
      stripResearchPreamble(unwrapProseCodeFences(splitGluedTableRowLines(text)))
    )
  );
}

/** Whether a string payload should use markdown preview (tools, subagents, etc.). */
export function shouldRenderAsMarkdown(text: string): boolean {
  return looksLikeProse(normalizeNarrativeMarkdown(text));
}
