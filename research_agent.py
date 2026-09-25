"""
research_agent.py
-------------------
The core "agent" logic. This is intentionally a simple, linear pipeline
(not a multi-step autonomous loop) so it's easy for a beginner to read,
debug, and extend:

    topic --> web search --> build context --> LLM writes report

This is what's usually called a single-agent RAG-style research assistant.
"""

from typing import Callable, Optional

from search_tool import search_web
from llm_client import ask_llm

SYSTEM_PROMPT = """You are a professional research analyst.

You will be given a research topic and a set of web search results
(title, link, and short snippet for each). Your job is to write a
clear, well-organized research report based ONLY on the information
in those search results.

Rules:
- Do not invent facts that are not supported by the provided sources.
- If the sources disagree or are unclear, say so explicitly.
- Write in plain, professional English.
- Structure the report with markdown headings, for example:
  ## Overview
  ## Key Findings
  ## Different Perspectives (if relevant)
  ## Summary
- At the end of each key point, add a bracketed source number, e.g. [1],
  matching the numbered source list you were given.
"""


def _build_user_prompt(topic: str, sources: list[dict]) -> str:
    lines = [f"Research topic: {topic}", "", "Search results:"]
    for i, src in enumerate(sources, start=1):
        lines.append(f"[{i}] {src['title']}")
        lines.append(f"    URL: {src['href']}")
        lines.append(f"    Snippet: {src['body']}")
        lines.append("")
    lines.append(
        "Using only the information above, write the research report now."
    )
    return "\n".join(lines)


def run_research_agent(
    topic: str,
    groq_api_key: str,
    num_results: int = 5,
    on_search_done: Optional[Callable[[], None]] = None,
) -> tuple[str, list[dict]]:
    """
    Run the full pipeline and return (report_markdown, sources_used).
    """
    # Step 1: search the web (free, no API key)
    sources = search_web(topic, num_results=num_results)

    if not sources:
        raise RuntimeError(
            "No search results were found for this topic. Try rephrasing it."
        )

    if on_search_done:
        on_search_done()

    # Step 2: ask the LLM to turn the raw sources into a report
    user_prompt = _build_user_prompt(topic, sources)
    report = ask_llm(
        api_key=groq_api_key,
        system_prompt=SYSTEM_PROMPT,
        user_prompt=user_prompt,
    )

    return report, sources
