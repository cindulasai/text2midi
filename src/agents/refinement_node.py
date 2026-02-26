# -*- coding: utf-8 -*-
"""
Refinement Node: Refine tracks based on quality feedback.
"""

import sys
from pathlib import Path
from src.agents.state import MusicState

# Add parent to path for importing app
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


def refinement_agent_node(state: MusicState) -> MusicState:
    """
    Agent Node: Refine tracks based on quality feedback.
    Regenerates problematic tracks or adjusts parameters.
    """
    print("\n[FIX] [REFINEMENT AGENT] Refining tracks...")
    
    if state.get("error"):
        return state
    
    report = state.get("quality_report")
    if not report or not report.issues:
        print("   No refinement needed")
        return state
    
    try:
        state["current_iteration"] = state.get("current_iteration", 0) + 1
        generated_tracks = state.get("generated_tracks", [])
        
        from src.app import MusicGenerator
        generator = MusicGenerator()
        
        # Get parameters
        metadata = state.get("generation_metadata", {})
        root = metadata.get("root", 60)
        mode = metadata.get("mode", "major")
        bars = metadata.get("bars", 16)
        energy = metadata.get("energy", "medium")
        genre = metadata.get("genre", "pop")
        
        # Handle high-severity issues
        for issue in report.issues:
            if issue.severity == "high" and issue.track_index < len(generated_tracks):
                track = generated_tracks[issue.track_index]
                print(f"   Regenerating track {issue.track_index}: {track.track_type}")
                
                # Regenerate with different parameters
                if issue.issue_type == "density":
                    # Generate with higher density
                    notes = generator.generate_melody(root, mode, bars, "high", genre)
                elif issue.issue_type == "harmony":
                    # Regenerate chords
                    notes = generator.generate_chords(root, genre, bars)
                else:
                    # Generic regeneration
                    notes = generator.generate_melody(root, mode, bars, energy, genre)
                
                track.notes = notes
        
        state["refinement_attempts"] = state.get("refinement_attempts", 0) + 1
        state["refinement_feedback"] = f"Applied refinements (iteration {state['current_iteration']})"
        
        print(f"[OK] Refinement applied (iteration {state['current_iteration']})")
        
    except Exception as e:
        state["error"] = f"Refinement failed: {str(e)}"
    
    return state


def refinement_router(state: MusicState) -> str:
    """Router to determine if refinement should recheck or finalize."""
    current_iteration = state.get("current_iteration", 0)
    max_iterations = state.get("max_refinement_iterations", 2)
    
    if current_iteration < max_iterations:
        return "recheck"
    else:
        return "finalize"
