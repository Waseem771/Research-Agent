"""
search_tool.py
---------------
A thin wrapper around the free DuckDuckGo search library.

Note: the PyPI package used to be called `duckduckgo_search`. It was
renamed to `ddgs` in 2025/2026 — always install `ddgs`, not the old name.
"""

from ddgs import DDGS


def search_web(query: str, num_results: int = 5) -> list[dict]:
    """
    Run a DuckDuckGo text search and return a clean list of results.

    Each result dict has: "title", "href", "body".
    No API key is required for this search.
    """
    results: list[dict] = []

    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=num_results):
            results.append(
                {
                    "title": r.get("title", "Untitled"),
                    "href": r.get("href", ""),
                    "body": r.get("body", ""),
                }
            )

    return results
