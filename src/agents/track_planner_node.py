"""
Track Planner Node: Create optimal track configuration based on intent.
Uses emotion-aware instrument selection for versatile music generation.

Delegates core planning logic to :mod:`src.services.track_planning`.
"""

import logging

from src.agents.state import MusicState, TrackConfig
from src.config.llm import LLMConfig
from src.services.track_planning import (
    enhance_with_emotion_instruments,
    ensure_track_count,
    plan_tracks_with_ai,
    plan_tracks_with_rules,
    _EMOTION_MAPPER_AVAILABLE,
)

logger = logging.getLogger(__name__)


def track_planner_node(state: MusicState) -> MusicState:
    """
    Agent Node: Create optimal track configuration with emotion awareness.

    Uses emotion-aware instrument selection to ensure:
    - Different moods get different instrument colors
    - Styles are reflected in track arrangement
    - Genre conventions are respected
    - Track generation is versatile and responsive
    """
    logger.info("\n[MUSIC] [TRACK PLANNER AGENT] Planning emotion-aware track configuration...")

    if state.get("error"):
        return state

    intent = state.get("intent")
    if not intent:
        state["error"] = "No intent available for track planning"
        return state

    try:
        # Extract extended intent information
        parsed_intent = state.get("parsed_intent")
        emotions = getattr(intent, "emotions", []) or []
        style_descriptors = intent.style_descriptors or []
        specific_instruments = intent.specific_instruments or []

        # Compute instrument confidence from ParsedIntent (if available)
        instrument_confidence = _compute_instrument_confidence(parsed_intent)

        logger.info("   Emotions: %s", emotions if emotions else 'Not specified')
        logger.info("   Styles: %s", style_descriptors if style_descriptors else 'Not specified')
        if instrument_confidence >= 0.7:
            logger.info("   Instruments: high-confidence user request → preserving")
        else:
            logger.info("   Instruments: low-confidence → planner may override")

        # --- Core planning (delegated) ---
        if LLMConfig.DEFAULT_PROVIDER:
            track_plan = plan_tracks_with_ai(intent)
        else:
            track_plan = plan_tracks_with_rules(intent)

        # --- Emotion enhancement ---
        if _EMOTION_MAPPER_AVAILABLE and (emotions or style_descriptors) and instrument_confidence < 0.7:
            track_plan = enhance_with_emotion_instruments(
                track_plan, intent.genre, emotions, style_descriptors, specific_instruments,
            )
        elif specific_instruments and instrument_confidence >= 0.7:
            logger.info("   ✓ Keeping user-specified instruments (high confidence)")

        # --- Ensure count ---
        if intent.track_count and len(track_plan) != intent.track_count:
            logger.warning("[WARN] Adjusting track count from %d to %s", len(track_plan), intent.track_count)
            track_plan = ensure_track_count(track_plan, intent.track_count, intent.genre)

        state["track_plan"] = track_plan
        logger.info("[OK] Track plan created: %d emotion-aware tracks", len(track_plan))
        for i, track in enumerate(track_plan, 1):
            logger.info("   %d. %-15s | %-20s | Priority: %s", i, track.track_type, track.instrument, track.priority)

    except Exception as e:
        import traceback
        state["error"] = f"Track planning failed: {str(e)}\n{traceback.format_exc()}"
        logger.error("[ERROR] Error: %s", state['error'])

    return state


# ---------------------------------------------------------------------------
# Helpers (node-specific, not shared)
# ---------------------------------------------------------------------------

def _compute_instrument_confidence(parsed_intent) -> float:
    """Derive instrument confidence from a ``ParsedIntent``, if present."""
    if parsed_intent is None:
        return 0.5
    try:
        from src.intent.schema import ParsedIntent

        if isinstance(parsed_intent, ParsedIntent) and parsed_intent.instruments:
            return min(
                (inst.priority / 10.0 for inst in parsed_intent.instruments),
                default=0.5,
            )
    except ImportError:
        pass
    return 0.5
