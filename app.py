"""
AI Research Agent
------------------
A single-agent research assistant.

Flow:
1. User enters a research topic in the Streamlit UI.
2. The agent searches the web (DuckDuckGo, free, no API key) for that topic.
3. The search results are handed to a Groq-hosted LLM (openai/gpt-oss-120b).
4. The LLM writes a structured research report, citing the sources it used.

Author: Waseem Hassan
"""

import streamlit as st

from research_agent import run_research_agent

# --------------------------------------------------------------------------
# Page setup
# --------------------------------------------------------------------------
st.set_page_config(
    page_title="AI Research Agent",
    page_icon="🔎",
    layout="centered",
)

st.title("🔎 AI Research Agent")
st.caption(
    "Enter any topic. The agent searches the web with DuckDuckGo and writes "
    "a structured research report using Groq's `openai/gpt-oss-120b` model."
)

# --------------------------------------------------------------------------
# Sidebar — settings
# --------------------------------------------------------------------------
with st.sidebar:
    st.header("⚙️ Settings")

    # The Groq API key is read ONLY from Streamlit secrets — it is never
    # shown in the UI or typed by visitors. Set it in .streamlit/secrets.toml
    # locally, or in the app's "Secrets" box on Streamlit Cloud.
    groq_api_key = st.secrets.get("GROQ_API_KEY", "")

    num_results = st.slider(
        "Number of web sources to use",
        min_value=3,
        max_value=10,
        value=5,
        help="More sources = more thorough, but slower and uses more tokens.",
    )

    st.divider()
    st.markdown(
        "**Model:** `openai/gpt-oss-120b` (via Groq)\n\n"
        "**Search:** DuckDuckGo (free, no API key)"
    )

# --------------------------------------------------------------------------
# Main input
# --------------------------------------------------------------------------
topic = st.text_input(
    "Research topic",
    placeholder="e.g. Impact of AI agents on customer support in 2026",
)

run_button = st.button("Run Research", type="primary", use_container_width=True)

# --------------------------------------------------------------------------
# Run the agent
# --------------------------------------------------------------------------
if run_button:
    if not groq_api_key:
        st.error(
            "No Groq API key found. Add GROQ_API_KEY to "
            ".streamlit/secrets.toml (locally) or to your app's Secrets "
            "on Streamlit Cloud."
        )
    elif not topic.strip():
        st.error("Please enter a research topic.")
    else:
        status_box = st.empty()
        try:
            with st.spinner("Searching the web and writing your report..."):
                status_box.info("Step 1/2 — Searching DuckDuckGo...")
                report, sources = run_research_agent(
                    topic=topic,
                    groq_api_key=groq_api_key,
                    num_results=num_results,
                    on_search_done=lambda: status_box.info(
                        "Step 2/2 — Asking the LLM to write the report..."
                    ),
                )
            status_box.empty()

            st.success("Done! Here is your research report:")
            st.markdown(report)

            with st.expander("📚 Sources used"):
                for i, src in enumerate(sources, start=1):
                    st.markdown(f"{i}. [{src['title']}]({src['href']})")

            st.download_button(
                "Download report as Markdown",
                data=report,
                file_name="research_report.md",
                mime="text/markdown",
                use_container_width=True,
            )

        except Exception as exc:  # noqa: BLE001 — show any error to a beginner user
            status_box.empty()
            st.error(f"Something went wrong: {exc}")

st.divider()
st.caption(
    "Built with Streamlit + Groq (openai/gpt-oss-120b) + DuckDuckGo search."
)
