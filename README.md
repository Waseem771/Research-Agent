# 🔎 AI Research Agent

A beginner-friendly, single-agent AI research assistant.

You give it a topic → it searches the web with **DuckDuckGo** (free, no API
key) → it hands the results to **Groq's `openai/gpt-oss-120b`** model →
it writes you a structured, cited research report.

## How it works (architecture)

```
topic → search_tool.py (DuckDuckGo search)
      → research_agent.py (builds the prompt)
      → llm_client.py (Groq LLM writes the report)
      → app.py (Streamlit UI shows the report)
```

This is a simple, linear "single agent" pipeline — easy to read, debug,
and extend later into a multi-step or multi-tool agent.

## File structure

```
ai-research-agent/
├── app.py                          # Streamlit UI — start here
├── research_agent.py                # Ties search + LLM together
├── search_tool.py                   # Free DuckDuckGo web search
├── llm_client.py                    # Groq API wrapper
├── requirements.txt                 # Dependencies
├── .gitignore
├── .streamlit/
│   └── secrets.toml.example         # Template — copy to secrets.toml
└── README.md
```

---

## Part 1 — Run it on your own computer

### 1. Install Python
You need Python 3.10 or newer. Check with:
```bash
python --version
```

### 2. Create a virtual environment (recommended)
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### 3. Install the dependencies
```bash
pip install -r requirements.txt
```

### 4. Get a free Groq API key
1. Go to https://console.groq.com/keys
2. Sign up (free) and click **Create API Key**.
3. Copy the key — you'll need it in the next step.

### 5. Add your key
Copy the example secrets file and paste in your real key:
```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```
Then open `.streamlit/secrets.toml` and replace the placeholder with your
real key. This file is already in `.gitignore`, so it will never be
uploaded to GitHub by accident.

> The key is read only from secrets — there is no input box for it in the
> app, so visitors can never see or need to type it.

### 6. Run the app
```bash
streamlit run app.py
```
Your browser should open automatically at `http://localhost:8501`.

---

## Part 2 — Upload the code to GitHub

1. Create a new **public** repository on GitHub (e.g. `ai-research-agent`).
2. In your project folder, run:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: AI research agent"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/ai-research-agent.git
   git push -u origin main
   ```
3. Double-check on GitHub.com that `.streamlit/secrets.toml` (the real one
   with your key) was **NOT** uploaded — only `secrets.toml.example`
   should be there. `.gitignore` takes care of this automatically.

---

## Part 3 — Deploy to Streamlit Community Cloud (free)

1. Go to https://share.streamlit.io and sign in with GitHub.
2. Click **"Create app"** → **"From an existing repo"**.
3. Select your `ai-research-agent` repository, branch `main`, and set the
   main file path to `app.py`.
4. Before clicking Deploy, open **"Advanced settings" → "Secrets"** and
   paste in:
   ```toml
   GROQ_API_KEY = "your-real-groq-api-key"
   ```
5. Click **Deploy**. After a minute or two, your app will be live at a
   public URL like `https://your-app-name.streamlit.app`.

Now anyone who opens the link can use your research agent — the app will
read the key from Streamlit's secrets automatically, so visitors don't
need to enter their own key (unless you choose to leave the sidebar box
empty for them to fill in their own).

---

## Ideas for extending this project

Once you're comfortable with the basic version, try:

- **Add memory**: let the agent remember the last few topics researched.
- **Add PDF export**: use a library like `fpdf2` to export the report as a PDF.
- **Add multiple search rounds**: have the LLM generate 2–3 sub-questions
  from the topic first, search each one, then combine everything —
  a common pattern in more advanced research agents.
- **Swap in LangChain**: wrap `search_tool.py` as a LangChain `Tool` and
  use an agent executor instead of the manual pipeline in
  `research_agent.py`.
- **Add a vector store**: cache search results in FAISS so repeated
  topics don't need a fresh web search every time.

## Troubleshooting

| Problem | Fix |
|---|---|
| `ImportError: No module named 'ddgs'` | Run `pip install -r requirements.txt` again — the package is `ddgs`, not the older `duckduckgo_search`. |
| `groq.AuthenticationError` | Your API key is missing or wrong — check `.streamlit/secrets.toml` or the sidebar input. |
| "No search results found" | DuckDuckGo occasionally rate-limits rapid repeated searches — wait a few seconds and try again, or rephrase the topic. |
| App works locally but not on Streamlit Cloud | Make sure you pasted your `GROQ_API_KEY` into the app's **Secrets** settings on share.streamlit.io. |
