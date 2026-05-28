import streamlit as st
import re

st.set_page_config(
    page_title="Research Agent",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=IBM+Plex+Mono:wght@400;500&family=Inter:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #0a0a0f;
    color: #e8e6e1;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 2.5rem 4rem; max-width: 1300px; }

.hero { text-align: center; padding: 2.5rem 0 2rem; }
.hero-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem; letter-spacing: 0.22em;
    color: #63dcb4; text-transform: uppercase; margin-bottom: 0.75rem;
}
.hero-title {
    font-family: 'Syne', sans-serif; font-size: 2.8rem; font-weight: 800;
    background: linear-gradient(135deg, #ffffff 0%, #63dcb4 60%, #3ba8d4 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; margin: 0 0 0.5rem;
}
.hero-sub { font-size: 0.92rem; font-weight: 300; color: #6a6868; max-width: 480px; margin: 0 auto; line-height: 1.6; }

.stTextInput > div > div > input {
    background: #111118 !important; border: 1px solid #2a2a3a !important;
    border-radius: 10px !important; color: #e8e6e1 !important;
    font-size: 1rem !important; padding: 0.85rem 1.1rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: #63dcb4 !important; box-shadow: 0 0 0 3px rgba(99,220,180,0.07) !important;
}
.stTextInput > label {
    font-family: 'IBM Plex Mono', monospace !important; font-size: 0.68rem !important;
    letter-spacing: 0.15em !important; text-transform: uppercase !important; color: #63dcb4 !important;
}
.stButton > button {
    background: linear-gradient(135deg, #63dcb4, #3ba8d4) !important;
    color: #0a0a0f !important; font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important; border: none !important; border-radius: 10px !important;
    padding: 0.75rem 1.5rem !important; width: 100%;
}
.stButton > button:hover { opacity: 0.88 !important; }

.stDownloadButton > button {
    background: transparent !important; color: #63dcb4 !important;
    font-family: 'IBM Plex Mono', monospace !important; font-size: 0.75rem !important;
    border: 1px solid #2a3a34 !important; border-radius: 8px !important;
    padding: 0.5rem 1rem !important; letter-spacing: 0.08em;
}
.stDownloadButton > button:hover { border-color: #63dcb4 !important; background: rgba(99,220,180,0.05) !important; }

/* Report panel */
.report-wrap {
    background: #0e0e16; border: 1px solid #1e1e2a;
    border-radius: 14px; padding: 1.6rem 1.8rem; min-height: 420px;
}
.report-label {
    font-family: 'IBM Plex Mono', monospace; font-size: 0.65rem;
    letter-spacing: 0.18em; text-transform: uppercase; color: #63dcb4;
    margin-bottom: 1rem; padding-bottom: 0.75rem; border-bottom: 1px solid #1e1e2a;
}
.report-body { font-size: 0.88rem; line-height: 1.85; color: #c4c1bc; white-space: pre-wrap; font-weight: 300; }
.report-empty {
    display: flex; flex-direction: column; align-items: center;
    justify-content: center; min-height: 300px; gap: 0.6rem;
    color: #2a2a3a; font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem; letter-spacing: 0.12em; text-transform: uppercase;
}

/* Pipeline steps - native streamlit friendly */
.pipe-wrap {
    background: #0e0e16; border: 1px solid #1e1e2a;
    border-radius: 14px; padding: 1.4rem 1.2rem;
}
.pipe-title {
    font-family: 'IBM Plex Mono', monospace; font-size: 0.65rem;
    letter-spacing: 0.18em; text-transform: uppercase; color: #3ba8d4;
    margin-bottom: 1rem; padding-bottom: 0.75rem; border-bottom: 1px solid #1e1e2a;
}
.srow {
    display: flex; align-items: center; justify-content: space-between;
    padding: 0.7rem 0; border-bottom: 1px solid #0f0f18; gap: 0.6rem;
}
.srow:last-child { border-bottom: none; }
.sicon {
    width: 24px; height: 24px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.6rem; flex-shrink: 0;
    border: 1px solid #2a2a3a; background: #111118; color: #3a3a4a;
}
.sicon-run { border-color: #63dcb4 !important; background: rgba(99,220,180,0.12) !important; color: #63dcb4 !important; }
.sicon-done { border-color: #3ba8d4 !important; background: rgba(59,168,212,0.12) !important; color: #3ba8d4 !important; }
.sname { font-family: 'Syne', sans-serif; font-size: 0.82rem; font-weight: 600; color: #e8e6e1; flex: 1; }
.sname-dim { color: #4a4a5a !important; }
.sbadge {
    font-family: 'IBM Plex Mono', monospace; font-size: 0.58rem;
    letter-spacing: 0.06em; text-transform: uppercase;
    padding: 0.15rem 0.45rem; border-radius: 20px;
}
.sb-pending { background: #111118; color: #3a3a4a; border: 1px solid #1a1a28; }
.sb-running { background: rgba(99,220,180,0.12); color: #63dcb4; border: 1px solid rgba(99,220,180,0.3); }
.sb-done    { background: rgba(59,168,212,0.12); color: #3ba8d4; border: 1px solid rgba(59,168,212,0.3); }
.sb-skipped { background: #111118; color: #444; border: 1px solid #1a1a28; }

.score-row {
    margin-top: 1rem; padding-top: 0.9rem; border-top: 1px solid #1e1e2a;
    display: flex; align-items: center; gap: 0.6rem;
}
.sc-badge {
    font-family: 'IBM Plex Mono', monospace; font-size: 0.7rem;
    padding: 0.25rem 0.7rem; border-radius: 6px;
    background: rgba(99,220,180,0.1); border: 1px solid rgba(99,220,180,0.25); color: #63dcb4;
}
.sc-badge-low { background: rgba(220,130,80,0.1) !important; border-color: rgba(220,130,80,0.25) !important; color: #dc8250 !important; }
.sc-note { font-size: 0.72rem; color: #3a3a4a; }

.stTabs [data-baseweb="tab-list"] { background: transparent !important; border-bottom: 1px solid #1e1e2a !important; }
.stTabs [data-baseweb="tab"] {
    font-family: 'IBM Plex Mono', monospace !important; font-size: 0.65rem !important;
    letter-spacing: 0.1em !important; text-transform: uppercase !important;
    color: #4a4a5a !important; background: transparent !important; border: none !important;
}
.stTabs [aria-selected="true"] { color: #63dcb4 !important; border-bottom: 2px solid #63dcb4 !important; }
.tab-content { font-size: 0.83rem; line-height: 1.75; color: #9a9790; white-space: pre-wrap; font-weight: 300; padding-top: 1rem; }
</style>
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-label">Autonomous AI · Multi-Agent Pipeline</div>
  <h1 class="hero-title">Research Agent</h1>
  <p class="hero-sub">Enter a topic — the pipeline searches, scrapes, writes, critiques, and refines a full report automatically.</p>
</div>
""", unsafe_allow_html=True)

# ── Search bar ────────────────────────────────────────────────────────────────
c1, c2 = st.columns([5, 1], gap="small")
with c1:
    topic = st.text_input("Research Topic", placeholder="e.g. Latest advances in quantum error correction", label_visibility="visible")
with c2:
    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
    run_btn = st.button("Run", use_container_width=True)

st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

# ── Build step HTML (no st.empty tricks — fully self-contained string) ────────
STEPS = [
    ("Search Agent",   "Web search"),
    ("Scraper Agent",  "Extract sources"),
    ("Writer Chain",   "Draft report"),
    ("Critic Chain",   "Score & review"),
    ("Revision Chain", "Refine report"),
]

def build_steps_html(statuses, score=None):
    imap = {"pending": ("", "·"), "running": ("sicon-run", "▶"), "done": ("sicon-done", "✓"), "skipped": ("", "—")}
    bmap = {"pending": "sb-pending", "running": "sb-running", "done": "sb-done", "skipped": "sb-skipped"}

    rows = ""
    for i, (name, desc) in enumerate(STEPS):
        s = statuses[i]
        icls, ichar = imap[s]
        ncls = "" if s != "pending" else "sname-dim"
        rows += f"""
        <div class="srow">
          <div class="sicon {icls}">{ichar}</div>
          <div class="sname {ncls}">{name}<br><span style="font-family:Inter,sans-serif;font-size:0.7rem;font-weight:300;color:#3a3a4a">{desc}</span></div>
          <span class="sbadge {bmap[s]}">{s}</span>
        </div>"""

    score_html = ""
    if score is not None:
        sc = "sc-badge-low" if score < 8 else ""
        note = "revised" if score < 8 else "passed"
        score_html = f'<div class="score-row"><span class="sc-badge {sc}">Score {score}/10</span><span class="sc-note">{note}</span></div>'

    return f'<div class="pipe-wrap"><div class="pipe-title">Pipeline</div>{rows}{score_html}</div>'


def build_report_html(text=None, label="Final Report"):
    if text is None:
        body = '<div class="report-empty"><span style="font-size:2rem;opacity:0.12">◈</span>Awaiting pipeline run</div>'
    else:
        safe = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        body = f'<div class="report-body">{safe}</div>'
    return f'<div class="report-wrap"><div class="report-label">{label}</div>{body}</div>'


# ── Layout ────────────────────────────────────────────────────────────────────
col_report, col_steps = st.columns([3, 1], gap="medium")

with col_report:
    report_slot = st.empty()

with col_steps:
    steps_slot = st.empty()

# initial render
report_slot.markdown(build_report_html(), unsafe_allow_html=True)
steps_slot.markdown(build_steps_html(["pending"] * 5), unsafe_allow_html=True)

detail_slot = st.empty()

# ── Run ───────────────────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.warning("Please enter a research topic first.")
        st.stop()

    from agents import build_search_agent, build_scrape_agent, writer_chain, critic_chain, revision_chain
    from langchain_core.messages import HumanMessage

    statuses = ["pending"] * 5

    def tick(i, s):
        statuses[i] = s
        steps_slot.markdown(build_steps_html(statuses), unsafe_allow_html=True)

    # Step 1 — Search
    tick(0, "running")
    sa = build_search_agent()
    sr = sa.invoke({"messages": [HumanMessage(content=f"Find recent, reliable and detailed information about: {topic}")]})
    search_results = sr["messages"][-1].content
    tick(0, "done")

    # Step 2 — Scrape
    tick(1, "running")
    ra = build_scrape_agent()
    rr = ra.invoke({"messages": [HumanMessage(content=f"""
        Based on the following search results about '{topic}', identify the 3 most relevant and reliable URLs.
        Scrape all 3 and combine key findings into one detailed research context.
        Prioritize: recent, reliable, technical depth, factual consistency.
        Search Results: {search_results[:1200]}
    """)]})
    scraped_content = rr["messages"][-1].content
    tick(1, "done")

    # Step 3 — Write
    tick(2, "running")
    combined = f"SEARCH RESULTS:\n{search_results}\n\nSCRAPED CONTENT:\n{scraped_content}"
    report = writer_chain.invoke({"topic": topic, "research": combined})
    report_slot.markdown(build_report_html(report, "Draft Report"), unsafe_allow_html=True)
    tick(2, "done")

    # Step 4 — Critic
    tick(3, "running")
    feedback = critic_chain.invoke({"report": report})
    def extract_score(t):
        m = re.search(r"Score:\s*(\d+)/10", t)
        return int(m.group(1)) if m else 0
    score = extract_score(feedback)
    tick(3, "done")

    # Step 5 — Revise
    if score < 8:
        tick(4, "running")
        revised = revision_chain.invoke({"report": report, "feedback": feedback})
        tick(4, "done")
    else:
        revised = report
        statuses[4] = "skipped"

    steps_slot.markdown(build_steps_html(statuses, score=score), unsafe_allow_html=True)
    report_slot.markdown(build_report_html(revised, "Final Report"), unsafe_allow_html=True)

    # Detail tabs
    with detail_slot.container():
        st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)
        st.markdown("<div style='font-family:IBM Plex Mono,monospace;font-size:0.65rem;letter-spacing:0.18em;text-transform:uppercase;color:#3ba8d4;margin-bottom:0.5rem'>Intermediate Outputs</div>", unsafe_allow_html=True)
        t1, t2, t3, t4 = st.tabs(["Search Results", "Scraped Content", "Critic Feedback", "Original Draft"])
        with t1:
            st.markdown(f"<div class='tab-content'>{search_results}</div>", unsafe_allow_html=True)
        with t2:
            st.markdown(f"<div class='tab-content'>{scraped_content}</div>", unsafe_allow_html=True)
        with t3:
            st.markdown(f"<div class='tab-content'>{feedback}</div>", unsafe_allow_html=True)
        with t4:
            st.markdown(f"<div class='tab-content'>{report}</div>", unsafe_allow_html=True)
        st.markdown("<div style='height:0.75rem'></div>", unsafe_allow_html=True)
        st.download_button(
            label="⬇  Download Final Report (.txt)",
            data=revised,
            file_name=f"research_{topic[:40].replace(' ', '_')}.txt",
            mime="text/plain",
        )