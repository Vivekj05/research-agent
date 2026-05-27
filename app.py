from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel
import json
import asyncio
from pathlib import Path

# ── Import your pipeline ──────────────────────────────────────────────────────
# Make sure pipeline.py, agents.py, tools.py are in the same directory as app.py
from pipeline import run_research_pipeline

app = FastAPI(title="Research Agent API", version="1.0.0")

BASE_DIR = Path(__file__).resolve().parent

# ── CORS — allow the HTML frontend to call this server ────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # tighten this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Request / Response models ─────────────────────────────────────────────────
class ResearchRequest(BaseModel):
    topic: str


class ResearchResponse(BaseModel):
    topic: str
    search_results: str
    scraped_content: str
    report: str
    feedback: str


@app.get("/")
async def index():
    return FileResponse(BASE_DIR / "research_agent_ui.html")


# ── /run  (blocking, returns full result) ─────────────────────────────────────
@app.post("/run", response_model=ResearchResponse)
async def run_research(request: ResearchRequest):
    """
    Run the full 4-step research pipeline and return all results at once.
    The frontend polls this endpoint and renders results when it completes.
    """
    if not request.topic.strip():
        raise HTTPException(status_code=400, detail="Topic cannot be empty.")

    # run_research_pipeline is synchronous (LangChain agents), so we run it
    # in a thread executor to avoid blocking the event loop
    loop = asyncio.get_event_loop()
    try:
        state = await loop.run_in_executor(
            None, run_research_pipeline, request.topic
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pipeline error: {str(e)}")

    return ResearchResponse(
        topic=request.topic,
        search_results=state.get("search_results", ""),
        scraped_content=state.get("scraped_content", ""),
        report=state.get("report", ""),
        feedback=state.get("feedback", ""),
    )


# ── /run/stream  (SSE — sends step-by-step progress events) ──────────────────
@app.post("/run/stream")
async def run_research_stream(request: ResearchRequest):
    """
    Server-Sent Events endpoint.
    The frontend connects here and receives JSON events as each step completes:

        data: {"step": 1, "label": "search",  "status": "running"}
        data: {"step": 1, "label": "search",  "status": "done",    "result": "..."}
        data: {"step": 2, "label": "scrape",  "status": "running"}
        ...
        data: {"step": 4, "label": "critic",  "status": "done",    "result": "..."}
        data: {"step": 0, "label": "done",    "status": "done"}
    """
    if not request.topic.strip():
        raise HTTPException(status_code=400, detail="Topic cannot be empty.")

    topic = request.topic

    async def event_generator():
        from agents import build_scrape_agent, build_search_agent, writer_chain, critic_chain
        from langchain_core.messages import HumanMessage

        def emit(data: dict) -> str:
            return f"data: {json.dumps(data)}\n\n"

        state = {}
        loop = asyncio.get_event_loop()

        # ── Step 1 — Search ───────────────────────────────────────────────────
        yield emit({"step": 1, "label": "search", "status": "running"})
        try:
            def _search():
                agent = build_search_agent()
                return agent.invoke({
                    "messages": [HumanMessage(
                        content=f"Find recent, reliable and detailed information about: {topic}"
                    )]
                })
            result = await loop.run_in_executor(None, _search)
            state["search_results"] = result["messages"][-1].content
            yield emit({"step": 1, "label": "search", "status": "done",
                        "result": state["search_results"]})
        except Exception as e:
            yield emit({"step": 1, "label": "search", "status": "error",
                        "error": str(e)})
            return

        # ── Step 2 — Scrape ───────────────────────────────────────────────────
        yield emit({"step": 2, "label": "scrape", "status": "running"})
        try:
            def _scrape():
                agent = build_scrape_agent()
                return agent.invoke({
                    "messages": [HumanMessage(
                        content=(
                            f"Based on the following search results about '{topic}', "
                            f"pick the most relevant URL and scrape it for deeper content.\n\n"
                            f"Search Results:\n{state['search_results'][:800]}"
                        )
                    )]
                })
            result = await loop.run_in_executor(None, _scrape)
            state["scraped_content"] = result["messages"][-1].content
            yield emit({"step": 2, "label": "scrape", "status": "done",
                        "result": state["scraped_content"]})
        except Exception as e:
            yield emit({"step": 2, "label": "scrape", "status": "error",
                        "error": str(e)})
            return

        # ── Step 3 — Writer ───────────────────────────────────────────────────
        yield emit({"step": 3, "label": "writer", "status": "running"})
        try:
            research_combined = (
                f"SEARCH RESULTS:\n{state['search_results']}\n\n"
                f"DETAILED SCRAPED CONTENT:\n{state['scraped_content']}"
            )
            def _write():
                return writer_chain.invoke({
                    "topic": topic,
                    "research": research_combined
                })
            state["report"] = await loop.run_in_executor(None, _write)
            yield emit({"step": 3, "label": "writer", "status": "done",
                        "result": state["report"]})
        except Exception as e:
            yield emit({"step": 3, "label": "writer", "status": "error",
                        "error": str(e)})
            return

        # ── Step 4 — Critic ───────────────────────────────────────────────────
        yield emit({"step": 4, "label": "critic", "status": "running"})
        try:
            def _critique():
                return critic_chain.invoke({"report": state["report"]})
            state["feedback"] = await loop.run_in_executor(None, _critique)
            yield emit({"step": 4, "label": "critic", "status": "done",
                        "result": state["feedback"]})
        except Exception as e:
            yield emit({"step": 4, "label": "critic", "status": "error",
                        "error": str(e)})
            return

        # ── All done ──────────────────────────────────────────────────────────
        yield emit({"step": 0, "label": "done", "status": "done"})

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",   # disables nginx buffering if behind proxy
        },
    )


# ── Health check ──────────────────────────────────────────────────────────────
@app.get("/health")
async def health():
    return {"status": "ok", "service": "research-agent"}


# ── Run directly: python app.py ───────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)