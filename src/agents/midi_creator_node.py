# -*- coding: utf-8 -*-
"""
MIDI Creator Node: Create final MIDI file from validated tracks.
"""

import logging
from pathlib import Path
from datetime import datetime
from src.agents.state import MusicState
from src.config.constants import OUTPUT_DIR

logger = logging.getLogger(__name__)


def midi_creation_agent_node(state: MusicState) -> MusicState:
    """
    Agent Node: Create final MIDI file from validated tracks.
    Saves to outputs directory with metadata.
    """
    logger.info("\n[SAVE] [MIDI CREATOR] Creating final MIDI file...")
    
    if state.get("error"):
        logger.info("   Skipping: %s", state['error'])
        return state
    
    generated_tracks = state.get("generated_tracks", [])
    
    if not generated_tracks:
        state["error"] = "No tracks to save"
        return state
    
    try:
        from src.app import MIDIGenerator
        
        intent = state.get("intent")
        
        # Create MIDI
        midi_gen = MIDIGenerator()
        midi = midi_gen.create_midi(generated_tracks, intent.tempo_preference or 120)
        
        # Save file
        OUTPUT_DIR.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        session_id = state.get("session_id", "unknown")[:8]
        filename = f"midigen_{intent.genre}_{session_id}_{timestamp}.mid"
        filepath = OUTPUT_DIR / filename
        
        midi.save(str(filepath))
        
        state["final_midi_path"] = str(filepath)
        logger.info("[OK] MIDI saved: %s", filename)
        logger.info("   Tracks: %d", len(generated_tracks))
        logger.info("   Tempo: %s BPM", intent.tempo_preference or 120)
        logger.info("   Duration: %s bars", state.get('generation_metadata', {}).get('bars', 16))
        
    except Exception as e:
        import traceback
        state["error"] = f"MIDI creation failed: {str(e)}\n{traceback.format_exc()}"
        logger.error("[ERROR] Error: %s", state['error'])
    
    return state
