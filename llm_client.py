"""
llm_client.py
--------------
A thin wrapper around the Groq API.

Model: openai/gpt-oss-120b — an open-weight reasoning model hosted on
Groq's fast inference hardware. Great free/cheap option for agent-style
tasks like this one.
"""

from groq import Groq

MODEL_NAME = "openai/gpt-oss-120b"


def ask_llm(api_key: str, system_prompt: str, user_prompt: str) -> str:
    """
    Send a single-turn chat request to Groq and return the text response.
    """
    client = Groq(api_key=api_key)

    completion = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.4,
        max_tokens=2000,
    )

    return completion.choices[0].message.content
