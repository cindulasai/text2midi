# -*- coding: utf-8 -*-
"""
Music Theory Validator Node: Validate harmonic and melodic choices.
"""

from typing import List
from src.agents.state import MusicState, TrackConfig


def music_theory_validator_node(state: MusicState) -> MusicState:
    """
    Agent Node: Validate harmonic, melodic, and rhythmic choices.
    Ensures the planned tracks follow music theory principles.
    """
    print("\n[THEORY] [MUSIC THEORY VALIDATOR] Validating musical choices...")
    
    if state.get("error"):
        return state
    
    intent = state.get("intent")
    track_plan = state.get("track_plan", [])
    
    if not track_plan:
        state["theory_valid"] = False
        state["theory_issues"] = ["No track plan to validate"]
        return state
    
    try:
        issues = []
        
        # Check 1: Genre-appropriate instruments
        genre_instruments = _get_genre_instruments(intent.genre)
        for track in track_plan:
            if track.instrument not in genre_instruments and track.track_type != "drums":
                issues.append(
                    f"Instrument '{track.instrument}' unusual for {intent.genre} genre"
                )
        
        # Check 2: Harmonic balance
        harmony_tracks = [t for t in track_plan if t.track_type in ["harmony", "pad"]]
        if len(harmony_tracks) == 0 and intent.energy == "high":
            issues.append("Lack of harmonic support for high-energy genre")
        
        # Check 3: Rhythm section
        rhythm_tracks = [t for t in track_plan if t.track_type in ["drums", "bass"]]
        if len(rhythm_tracks) == 0:
            issues.append("Missing rhythm section (drums/bass)")
        
        # Check 4: Melodic balance
        melodic_tracks = [t for t in track_plan if t.track_type in ["lead", "counter_melody"]]
        if len(melodic_tracks) == 0:
            issues.append("No melodic instruments in plan")
        
        # Check 5: Track priority consistency
        priorities = [t.priority for t in track_plan]
        if sorted(priorities) != list(range(1, len(priorities) + 1)):
            issues.append("Track priorities not sequential (auto-fixing)")
            for i, track in enumerate(sorted(track_plan, key=lambda t: t.priority)):
                track.priority = i + 1
        
        state["theory_issues"] = issues
        state["theory_valid"] = len(issues) == 0
        state["theory_validation"] = {
            "genre": intent.genre,
            "track_count": len(track_plan),
            "has_melody": len(melodic_tracks) > 0,
            "has_harmony": len(harmony_tracks) > 0,
            "has_rhythm": len(rhythm_tracks) > 0,
        }
        
        if state["theory_valid"]:
            print("[OK] All music theory checks passed")
        else:
            print(f"[WARN] Theory issues found ({len(issues)})")
            for issue in issues[:3]:
                print(f"   - {issue}")
            if len(issues) > 3:
                print(f"   ... and {len(issues) - 3} more")
        
    except Exception as e:
        state["error"] = f"Theory validation failed: {str(e)}"
        state["theory_valid"] = False
    
    return state


def _get_genre_instruments(genre: str) -> set:
    """Get typical instruments for a genre."""
    genre_instruments = {
        "pop": {"piano", "electric_guitar", "electric_bass", "drums", "synth_lead", "synth_pad"},
        "rock": {"electric_guitar", "electric_bass", "drums", "piano", "violin"},
        "jazz": {"piano", "saxophone", "trumpet", "electric_bass", "drums", "vibraphone"},
        "classical": {"piano", "violin", "cello", "flute", "orchestra_strings"},
        "electronic": {"synth_lead", "synth_bass", "synth_pad", "drums", "electric_guitar"},
        "lofi": {"piano", "electric_guitar", "acoustic_bass", "drums", "synth_pad"},
        "ambient": {"synth_pad", "piano", "strings", "fx_atmosphere"},
        "cinematic": {"orchestra_strings", "brass", "piano", "drums", "choir"},
        "funk": {"electric_bass", "drums", "electric_guitar", "synth_lead", "saxophone"},
        "rnb": {"electric_piano", "electric_bass", "drums", "synth_pad", "vocal_choir"},
    }
    return genre_instruments.get(genre, {"piano", "guitar", "bass", "drums"})
