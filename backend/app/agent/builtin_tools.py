"""Built-in tools beyond deepagents filesystem/shell suite."""

from __future__ import annotations

import re
from typing import Any
from urllib.parse import quote_plus

import httpx
from langchain_core.tools import tool


@tool
async def web_fetch(url: str, max_chars: int = 12000) -> str:
    """Fetch a URL and return cleaned text content (HTML tags stripped when possible).

    Args:
        url: Absolute http(s) URL to fetch.
        max_chars: Truncate returned text to this many characters.
    """
    if not url.startswith(("http://", "https://")):
        return "Error: url must start with http:// or https://"
    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=30.0) as client:
            resp = await client.get(url, headers={"User-Agent": "data-agent/1.0"})
            resp.raise_for_status()
            content_type = resp.headers.get("content-type", "")
            text = resp.text
            if "html" in content_type.lower() or text.lstrip().startswith("<"):
                text = _html_to_text(text)
            text = text.strip()
            if len(text) > max_chars:
                text = text[:max_chars] + "\n\n…[truncated]"
            return text or "(empty response)"
    except Exception as exc:
        return f"Error fetching {url}: {exc}"


@tool
async def web_search(query: str, max_results: int = 5) -> str:
    """Search the web via DuckDuckGo HTML results (no API key required).

    Args:
        query: Search query string.
        max_results: Maximum number of results to return.
    """
    max_results = max(1, min(max_results, 10))
    url = f"https://html.duckduckgo.com/html/?q={quote_plus(query)}"
    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=30.0) as client:
            resp = await client.get(
                url,
                headers={"User-Agent": "data-agent/1.0"},
            )
            resp.raise_for_status()
            results = _parse_ddg_html(resp.text, max_results)
            if not results:
                return (
                    f"No results parsed for query={query!r}. "
                    "Try web_fetch on a specific URL, or refine the query."
                )
            lines = []
            for i, item in enumerate(results, 1):
                lines.append(f"{i}. {item['title']}\n   {item['url']}\n   {item['snippet']}")
            return "\n\n".join(lines)
    except Exception as exc:
        return f"Error searching for {query!r}: {exc}"


def _html_to_text(html: str) -> str:
    html = re.sub(r"(?is)<(script|style|noscript).*?>.*?</\1>", " ", html)
    html = re.sub(r"(?is)<br\s*/?>", "\n", html)
    html = re.sub(r"(?is)</p>", "\n\n", html)
    html = re.sub(r"(?is)<[^>]+>", " ", html)
    html = re.sub(r"&nbsp;", " ", html)
    html = re.sub(r"&amp;", "&", html)
    html = re.sub(r"&lt;", "<", html)
    html = re.sub(r"&gt;", ">", html)
    html = re.sub(r"&#39;", "'", html)
    html = re.sub(r"&quot;", '"', html)
    html = re.sub(r"[ \t]+\n", "\n", html)
    html = re.sub(r"\n{3,}", "\n\n", html)
    html = re.sub(r"[ \t]{2,}", " ", html)
    return html


def _parse_ddg_html(html: str, max_results: int) -> list[dict[str, str]]:
    results: list[dict[str, str]] = []
    # DuckDuckGo HTML result blocks
    pattern = re.compile(
        r'class="result__a"[^>]*href="(?P<href>[^"]+)"[^>]*>(?P<title>.*?)</a>'
        r'.*?class="result__snippet"[^>]*>(?P<snippet>.*?)</(?:a|td|div)',
        re.IGNORECASE | re.DOTALL,
    )
    for match in pattern.finditer(html):
        title = _html_to_text(match.group("title")).strip()
        snippet = _html_to_text(match.group("snippet")).strip()
        href = match.group("href")
        # DDG wraps redirects sometimes
        if "uddg=" in href:
            m = re.search(r"uddg=([^&]+)", href)
            if m:
                from urllib.parse import unquote

                href = unquote(m.group(1))
        results.append({"title": title, "url": href, "snippet": snippet})
        if len(results) >= max_results:
            break
    return results


def get_builtin_tools(
    enabled: dict[str, bool] | None = None,
    *,
    backend: Any | None = None,
    include_harness_tools: bool = False,
) -> list[Any]:
    enabled = enabled or {}
    tools: list[Any] = []
    if enabled.get("web_fetch", True):
        tools.append(web_fetch)
    if enabled.get("web_search", True):
        tools.append(web_search)
    if include_harness_tools and backend is not None:
        from app.agent.harness.clarification import make_ask_user_tool
        from app.agent.harness.tools import make_search_knowledge_tool

        tools.append(make_search_knowledge_tool(backend))
        if enabled.get("ask_user", True):
            tools.append(make_ask_user_tool())
    return tools


BUILTIN_TOOL_CATALOG = [
    {"name": "web_fetch", "description": "Fetch a URL and return cleaned text.", "source": "builtin"},
    {"name": "web_search", "description": "Search the web (DuckDuckGo HTML).", "source": "builtin"},
    {"name": "search_knowledge", "description": "Search org/workspace knowledge by pattern.", "source": "builtin"},
    {"name": "wkb_query", "description": "WKB index retrieval for contract data analysis.", "source": "builtin"},
    {
        "name": "ask_user",
        "description": "Ask the user a focused clarification (single/multi select or free text).",
        "source": "builtin",
    },
    {"name": "ls", "description": "List directory contents.", "source": "deepagents"},
    {"name": "read_file", "description": "Read a file from the agent filesystem.", "source": "deepagents"},
    {"name": "write_file", "description": "Write a file to the agent filesystem.", "source": "deepagents"},
    {"name": "edit_file", "description": "Edit a file in the agent filesystem.", "source": "deepagents"},
    {"name": "glob", "description": "Find files by glob pattern.", "source": "deepagents"},
    {"name": "grep", "description": "Search file contents.", "source": "deepagents"},
    {"name": "execute", "description": "Run a shell command in the workspace.", "source": "deepagents"},
    {"name": "write_todos", "description": "Manage an agent todo list.", "source": "deepagents"},
    {"name": "task", "description": "Delegate work to a subagent.", "source": "deepagents"},
]
