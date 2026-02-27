# -*- coding: utf-8 -*-
"""
text2midi VST3 Plugin — Python Backend Server
FastAPI server wrapping the existing LangGraph music generation pipeline.
Communicates with the JUCE VST3 plugin over HTTP localhost:18323.
"""

import asyncio
import logging
import os
import sys
import time
import uuid
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any, Dict, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

# ── Ensure project root is importable ─────────────────────────────────────────
_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_REPO_ROOT))

from src.agents.graph import get_agentic_graph
from src.agents.state import MusicState
from src.config.llm import LLMConfig
from src.config.settings import AppSettings

logger = logging.getLogger("text2midi.server")
logging.basicConfig(level=logging.INFO)

# ── In-memory generation results cache ────────────────────────────────────────
_results_cache: Dict[str, Dict[str, Any]] = {}
_CACHE_TTL_SECONDS = 300  # 5 minutes


# ── Request / Response Models ─────────────────────────────────────────────────

class ConfigureRequest(BaseModel):
    provider: str
    api_key: str
    endpoint: str = ""
    model: str = ""


class GenerateRequest(BaseModel):
    prompt: str
    session_id: str = ""


class TrackInfo(BaseModel):
    name: str
    instrument: str
    channel: int
    note_count: int
    track_type: str


class GenerateResponse(BaseModel):
    status: str
    midi_path: str = ""
    tracks: list[TrackInfo] = []
    quality_score: float = 0.0
    genre: str = ""
    tempo: int = 120
    bars: int = 0
    summary: str = ""


# ── Lifespan: cleanup stale cache entries ─────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup initialisation + background cache cleanup."""
    # ── startup ───────────────────────────────────────────────────────────────
    from dotenv import load_dotenv
    load_dotenv(_REPO_ROOT / ".env")

    AppSettings.load()
    if AppSettings.is_configured():
        AppSettings.apply_to_environment()
    LLMConfig.initialize()
    logger.info(
        "Server ready — provider=%s, available=%s",
        LLMConfig.DEFAULT_PROVIDER,
        LLMConfig.AVAILABLE_PROVIDERS,
    )

    # ── background cache cleanup ──────────────────────────────────────────────
    async def _cleanup():
        while True:
            await asyncio.sleep(60)
            now = time.time()
            stale = [
                k for k, v in _results_cache.items()
                if now - v.get("_ts", 0) > _CACHE_TTL_SECONDS
            ]
            for k in stale:
                _results_cache.pop(k, None)

    task = asyncio.create_task(_cleanup())
    yield
    task.cancel()


# ── FastAPI Application ───────────────────────────────────────────────────────

app = FastAPI(
    title="text2midi Backend",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Endpoints ─────────────────────────────────────────────────────────────────

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "version": "0.1.0",
        "provider": LLMConfig.DEFAULT_PROVIDER or "",
        "available_providers": list(LLMConfig.AVAILABLE_PROVIDERS),
    }


@app.post("/configure")
async def configure(req: ConfigureRequest):
    AppSettings.update(
        provider=req.provider,
        api_key=req.api_key,
        custom_endpoint=req.endpoint,
        custom_model=req.model,
    )
    AppSettings.save()
    AppSettings.apply_to_environment()
    LLMConfig.initialize()

    return {
        "status": "configured",
        "provider": LLMConfig.DEFAULT_PROVIDER or req.provider,
    }


@app.post("/generate", response_model=GenerateResponse)
async def generate(req: GenerateRequest):
    if not LLMConfig.DEFAULT_PROVIDER:
        raise HTTPException(
            status_code=503,
            detail="No LLM provider configured. Call POST /configure first.",
        )

    session_id = req.session_id or str(uuid.uuid4())[:8]

    try:
        result = await asyncio.get_event_loop().run_in_executor(
            None, _run_pipeline, req.prompt, session_id
        )
    except Exception as exc:
        logger.exception("Generation failed")
        raise HTTPException(status_code=500, detail=str(exc))

    # Cache the result
    result["_ts"] = time.time()
    _results_cache[session_id] = result

    return _format_response(result)


@app.get("/generate/stream")
async def generate_stream(session_id: str, prompt: str = ""):
    """SSE endpoint streaming per-node progress."""
    if not LLMConfig.DEFAULT_PROVIDER:
        raise HTTPException(status_code=503, detail="No LLM provider configured.")

    if not prompt and session_id not in _results_cache:
        raise HTTPException(status_code=400, detail="prompt is required for new generations.")

    async def _event_stream():
        import json as _json

        node_order = [
            "intent_parser", "track_planner", "theory_validator",
            "track_generator", "quality_control", "refinement",
            "midi_creator", "session_summary",
        ]

        try:
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None, _run_pipeline_streaming, prompt, session_id, node_order
            )

            # After pipeline completes, yield final result
            quality = 0.0
            qr = result.get("quality_report")
            if qr:
                quality = qr.overall_score
            yield f"data: {_json.dumps({'status': 'done', 'midi_path': result.get('final_midi_path', ''), 'quality_score': quality})}\n\n"

        except Exception as exc:
            yield f"data: {_json.dumps({'status': 'error', 'error': str(exc)})}\n\n"

    return StreamingResponse(
        _event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )


# ── Pipeline Execution ────────────────────────────────────────────────────────

def _run_pipeline(prompt: str, session_id: str) -> Dict[str, Any]:
    """Run the full LangGraph pipeline (blocking, called from executor)."""
    Path("outputs").mkdir(exist_ok=True)

    initial_state: MusicState = {
        "user_prompt": prompt,
        "intent": None,
        "track_plan": [],
        "theory_validation": {},
        "theory_valid": False,
        "theory_issues": [],
        "generated_tracks": [],
        "generation_metadata": {},
        "quality_report": None,
        "refinement_attempts": 0,
        "refinement_feedback": "",
        "needs_refinement": False,
        "final_midi_path": None,
        "session_summary": "",
        "messages": [],
        "error": None,
        "error_context": None,
        "session_id": session_id,
        "composition_state": {
            "existing_tracks": [],
            "tempo": 120,
            "key": "C",
            "genre": "pop",
            "mode": "major",
        },
        "max_refinement_iterations": 2,
        "current_iteration": 0,
    }

    config = {"configurable": {"thread_id": session_id}}
    graph = get_agentic_graph()
    result = graph.invoke(initial_state, config=config)
    return result


def _run_pipeline_streaming(
    prompt: str, session_id: str, node_order: list
) -> Dict[str, Any]:
    """Run pipeline with streaming (same as _run_pipeline but could be extended)."""
    return _run_pipeline(prompt, session_id)


def _format_response(state: Dict[str, Any]) -> GenerateResponse:
    """Convert raw pipeline state into a clean API response."""
    tracks_info = []
    for i, track in enumerate(state.get("generated_tracks", [])):
        tracks_info.append(TrackInfo(
            name=getattr(track, "name", f"Track {i}"),
            instrument=getattr(track, "name", "unknown"),
            channel=getattr(track, "channel", i),
            note_count=len(getattr(track, "notes", [])),
            track_type=getattr(track, "track_type", ""),
        ))

    quality_score = 0.0
    qr = state.get("quality_report")
    if qr:
        quality_score = qr.overall_score

    genre = ""
    intent = state.get("intent")
    if intent:
        genre = getattr(intent, "genre", "")

    tempo = 120
    comp = state.get("composition_state", {})
    if isinstance(comp, dict):
        tempo = comp.get("tempo", 120)

    return GenerateResponse(
        status="completed" if not state.get("error") else "error",
        midi_path=state.get("final_midi_path", "") or "",
        tracks=tracks_info,
        quality_score=quality_score,
        genre=genre,
        tempo=tempo,
        summary=state.get("session_summary", ""),
    )


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=18323,
        log_level="info",
    )
