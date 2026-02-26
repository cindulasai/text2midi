# -*- coding: utf-8 -*-
"""
MIDI Creator Node: Create final MIDI file from validated tracks.
"""

import sys
from pathlib import Path
from datetime import datetime
from src.agents.state import MusicState

# Add parent to path for importing app
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


def midi_creation_agent_node(state: MusicState) -> MusicState:
    """
    Agent Node: Create final MIDI file from validated tracks.
    Saves to outputs directory with metadata.
    """
    print("\n[SAVE] [MIDI CREATOR] Creating final MIDI file...")
    
    if state.get("error"):
        print(f"   Skipping: {state['error']}")
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
        Path("outputs").mkdir(exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        session_id = state.get("session_id", "unknown")[:8]
        filename = f"midigen_{intent.genre}_{session_id}_{timestamp}.mid"
        filepath = Path("outputs") / filename
        
        midi.save(str(filepath))
        
        state["final_midi_path"] = str(filepath)
        print(f"[OK] MIDI saved: {filename}")
        print(f"   Tracks: {len(generated_tracks)}")
        print(f"   Tempo: {intent.tempo_preference or 120} BPM")
        print(f"   Duration: {state.get('generation_metadata', {}).get('bars', 16)} bars")
        
    except Exception as e:
        import traceback
        state["error"] = f"MIDI creation failed: {str(e)}\n{traceback.format_exc()}"
        print(f"[ERROR] Error: {state['error']}")
    
    return state
