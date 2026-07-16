---
name: web-research
description: Structured approach for researching topics on the web using web_search and web_fetch, then summarizing findings.
license: MIT
---

# Web Research Skill

## When to Use
- User asks to research a topic, compare options, or gather current information
- You need primary sources or documentation from the public web

## Workflow
1. Clarify the question and success criteria.
2. Run `web_search` with a focused query (2–4 searches max unless needed).
3. `web_fetch` the most promising 2–5 URLs.
4. Synthesize findings with clear structure:
   - Summary
   - Key points
   - Sources (URLs)
   - Open questions / caveats
5. Prefer primary sources over secondary summaries.

## Tips
- Prefer official docs, specs, and release notes for technical questions.
- Note when information may be outdated.
- Do not invent citations.
