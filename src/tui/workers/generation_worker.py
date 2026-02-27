# -*- coding: utf-8 -*-
"""
Generation Worker
Runs the LangGraph music generation pipeline in a background thread
and posts progress messages back to the TUI app.
"""

from __future__ import annotations

import time
import uuid
import logging
from pathlib import Path
from typing import Any, Dict

from textual.message import Message
from textual.worker import Worker, WorkerState

logger = logging.getLogger(__name__)


# ------------------------------------------------------------------ #
# Messages posted from the worker to the app
# ------------------------------------------------------------------ #

class NodeStarted(Message):
    def __init__(self, node_name: str) -> None:
        super().__init__()
        self.node_name = node_name


class NodeCompleted(Message):
    def __init__(self, node_name: str, elapsed: float) -> None:
        super().__init__()
        self.node_name = node_name
        self.elapsed = elapsed


class GenerationComplete(Message):
    def __init__(self, result_state: Dict[str, Any]) -> None:
        super().__init__()
        self.result_state = result_state


class GenerationError(Message):
    def __init__(self, error: str) -> None:
        super().__init__()
        self.error = error


# ------------------------------------------------------------------ #
# Worker function (called via app.run_worker)
# ------------------------------------------------------------------ #

async def run_generation(prompt: str, app: Any) -> Dict[str, Any]:
    """Execute the full LangGraph pipeline in a worker thread.

    NOTE: This function is CPU-bound / IO-bound (LLM calls) and runs
    in a *thread* via Textual's ``run_worker(..., thread=True)``.
    We import heavy modules inside the function to keep the TUI startup fast.
    """
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))

    from src.agents.graph import get_agentic_graph
    from src.agents.state import MusicState

    # Ensure outputs/ exists
    Path("outputs").mkdir(exist_ok=True)

    session_id = str(uuid.uuid4())[:8]
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

    # Stream through the graph to get per-node progress
    previous_keys: set = set()
    node_order = [
        "intent_parser", "track_planner", "theory_validator",
        "track_generator", "quality_control", "refinement",
        "midi_creator", "session_summary",
    ]

    last_state: Dict[str, Any] = dict(initial_state)

    try:
        for chunk in graph.stream(initial_state, config=config, stream_mode="values"):
            # Determine which node just completed by checking new keys
            current_keys = set(k for k, v in chunk.items() if v is not None and k not in (
                "user_prompt", "messages", "session_id", "composition_state",
                "max_refinement_iterations", "current_iteration",
            ))
            new_keys = current_keys - previous_keys
            previous_keys = current_keys
            last_state = chunk

            # Heuristic: map new keys to nodes
            key_to_node = {
                "intent": "intent_parser",
                "track_plan": "track_planner",
                "theory_validation": "theory_validator",
                "theory_valid": "theory_validator",
                "generated_tracks": "track_generator",
                "quality_report": "quality_control",
                "refinement_feedback": "refinement",
                "final_midi_path": "midi_creator",
                "session_summary": "session_summary",
            }
            for key in new_keys:
                node = key_to_node.get(key)
                if node:
                    app.post_message(NodeCompleted(node, 0.0))

    except Exception as exc:
        logger.exception("Generation pipeline failed")
        app.post_message(GenerationError(str(exc)))
        return last_state

    # Check for errors in the final state
    if last_state.get("error"):
        app.post_message(GenerationError(last_state["error"]))
    else:
        app.post_message(GenerationComplete(last_state))

    return last_state
