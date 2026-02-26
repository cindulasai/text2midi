# -*- coding: utf-8 -*-
"""
Session management utilities for MidiGen application.
"""

from pathlib import Path
from src.app.models import CompositionSession


def get_session_summary(session: CompositionSession) -> str:
    """Get current session state as formatted string.
    
    Args:
        session: CompositionSession object
        
    Returns:
        Formatted session summary string
    """
    if not session or session.total_bars == 0:
        return "No active composition"
    
    track_list = "\n".join([f"  - {t.name} ({t.track_type})" for t in session.tracks])
    return f"""**Current Composition:**
- Genre: {session.genre}
- Key: {session.key} {session.mode}
- Tempo: {session.tempo} BPM
- Duration: {session.total_bars} bars
- Tracks ({len(session.tracks)}):
{track_list}"""


def ensure_output_directory() -> Path:
    """Ensure output directory exists.
    
    Returns:
        Path to output directory
    """
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)
    return output_dir
