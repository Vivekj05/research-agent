# 🔍 Research Agent

An agentic AI pipeline that researches any topic by searching the web, scraping content, writing a structured report, and critically reviewing it — all in 4 automated steps.

---

## How It Works

```
Topic Input
    │
    ▼
[Step 1] Search Agent      → finds recent, relevant sources from the web
    │
    ▼
[Step 2] Scrape Agent      → deep-scrapes the most relevant URL
    │
    ▼
[Step 3] Writer Chain      → drafts a structured research report
    │
    ▼
[Step 4] Critic Chain      → reviews and scores the report
```

---

## Project Structure

```
RESEARCH-AGENT/
├── agents.py               # Search agent, scrape agent, writer & critic chains
├── pipeline.py             # Orchestrates all 4 steps
├── tools.py                # Tool definitions (search, scraper)
├── app.py                  # FastAPI backend (SSE streaming)
├── research_agent_ui.html  # Frontend (open in browser)
├── .env                    # API keys
└── requirements.txt        # Dependencies
```

---

## Setup

**1. Clone and enter the project**
```bash
git clone <your-repo-url>
cd RESEARCH-AGENT
```

**2. Create and activate a virtual environment**
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Mac / Linux
source .venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Add your API keys to `.env`**
```env
MISTRAL_API_KEY=your_key_here
TAVILY_API_KEY=your_key_here
```

---

## Running the Project

**Start the FastAPI server:**
```bash
uvicorn app:app --reload
```

Server runs at → `http://localhost:8000`

**Open the frontend:**

Just open `research_agent_ui.html` in your browser. No extra setup needed.

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/run/stream` | Run pipeline with live SSE updates |
| `POST` | `/run` | Run pipeline, return all results at once |
| `GET` | `/health` | Check if server is running |

---

## Run from Terminal (no UI)

```bash
python pipeline.py
```

You'll be prompted to enter a topic directly.

---

## Requirements

- Python 3.9+
- MISTRALAI API key
- Tavily API key (for web search)