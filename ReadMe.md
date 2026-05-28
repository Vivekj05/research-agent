# 🔍 Research Agent

An agentic AI pipeline that researches any topic by searching the web, scraping content, writing a structured report, critically reviewing it, and refining it — all in 5 automated steps.

---

## Architecture

```
                        ┌─────────────────────┐
                        │        INPUT        │
                        │  Research Topic /   │
                        │      Question       │
                        └──────────┬──────────┘
                                   │
                                   ▼
              ┌────────────────────────────────────────┐
              │           STEP 1 · SEARCH AGENT        │
              │  Uses Tavily to find recent, reliable  │
              │        and relevant information        │
              │                                        │
              │  Output: Search Results                │
              │          (Top Links & Snippets)        │
              └────────────────────┬───────────────────┘
                                   │
                                   ▼
              ┌────────────────────────────────────────┐
              │          STEP 2 · READER AGENT         │
              │  Selects top 3 URLs and scrapes full   │
              │     content from multiple sources      │
              │                                        │
              │  Output: Scraped Content               │
              │          (Aggregated Context)          │
              └────────────────────┬───────────────────┘
                                   │
                                   ▼
              ┌────────────────────────────────────────┐
              │          STEP 3 · WRITER CHAIN         │
              │   Synthesizes search + scraped data    │
              │    into a well-structured report       │
              │                                        │
              │  Output: Draft Research Report         │
              └────────────────────┬───────────────────┘
                                   │
                                   ▼
              ┌────────────────────────────────────────┐
              │          STEP 4 · CRITIC CHAIN         │
              │  Evaluates report for quality,         │
              │  accuracy, completeness, and clarity   │
              │                                        │
              │  Output: Critique & Feedback           │
              │          + Score (0–10)                │
              └────────────────────┬───────────────────┘
                                   │
                          ┌────────▼────────┐
                          │   Score ≥ 8?    │
                          └────────┬────────┘
                     Yes ◄─────────┴──────────► No
                      │                          │
                      │                          ▼
                      │       ┌────────────────────────────────────────┐
                      │       │        STEP 5 · REVISION CHAIN         │
                      │       │  Refines the draft based on critic     │
                      │       │  feedback to address gaps and improve  │
                      │       │  quality                               │
                      │       │                                        │
                      │       │  Output: Revised Report                │
                      │       └──────────────────┬─────────────────────┘
                      │                          │
                      └──────────────┬───────────┘
                                     │
                                     ▼
              ┌────────────────────────────────────────┐
              │           FINAL RESEARCH REPORT        │
              │   High-quality, refined report ready   │
              │               for use                  │
              └────────────────────────────────────────┘
```

---

## Project Structure

```
RESEARCH-AGENT/
├── agents.py               # Search agent, scrape agent, writer, critic & revision chains
├── pipeline.py             # Orchestrates all 5 steps
├── tools.py                # Tool definitions (Tavily search, scraper)
├── app.py                  # Streamlit UI
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

**Launch the Streamlit app:**
```bash
streamlit run app.py
```

App runs at → `http://localhost:8501`

The UI shows a live pipeline panel on the right as each step runs — search, scrape, write, critique, and (if needed) revise — with the final report rendered on the left.

---

## Run from Terminal (no UI)

```bash
python pipeline.py
```

You'll be prompted to enter a topic directly. The pipeline prints each step's output and saves the final report.

---

## How the Revision Loop Works

After the Writer Chain produces a draft, the Critic Chain scores it from 0–10 based on quality, accuracy, completeness, and clarity.

- **Score ≥ 8** → Draft is accepted as the final report directly.
- **Score < 8** → The Revision Chain receives both the draft and the critic's feedback, and produces an improved version which becomes the final report.

---

## Requirements

- Python 3.9+
- Mistral AI API key
- Tavily API key (for web search)