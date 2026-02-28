# -*- coding: utf-8 -*-
"""
Session Summary Node: Generate summary of the composition session.
"""

import logging

from src.agents.state import MusicState

logger = logging.getLogger(__name__)


def session_summary_agent_node(state: MusicState) -> MusicState:
    """
    Agent Node: Generate summary of the composition session.
    """
    logger.info("\n[INFO] [SESSION SUMMARY] Generating summary...")
    
    try:
        intent = state.get("intent")
        generated_tracks = state.get("generated_tracks", [])
        quality_report = state.get("quality_report")
        
        summary_parts = [
            "## Composition Summary",
        ]
        
        if intent:
            summary_parts.append(f"**Action:** {intent.action.title()}")
            summary_parts.append(f"**Genre:** {intent.genre}")
        
        summary_parts.extend([
            f"**Total Tracks:** {len(generated_tracks)}",
            f"**Duration:** {state.get('generation_metadata', {}).get('bars', 16)} bars",
            f"**Tempo:** {(intent.tempo_preference if intent else None) or 120} BPM",
        ])
        
        if intent:
            summary_parts.append(f"**Key:** {intent.key_preference or 'C'} {state.get('generation_metadata', {}).get('mode', 'major')}")
        
        if quality_report:
            summary_parts.append(f"**Quality Score:** {quality_report.overall_score:.2f}/1.0")
        
        if state.get("final_midi_path"):
            summary_parts.append(f"\n[OK] **MIDI file ready for download!**")
        
        state["session_summary"] = "\n".join(summary_parts)
        logger.info("[OK] Summary generated")
        
    except Exception as e:
        state["session_summary"] = "Could not generate summary"
    
    return state
