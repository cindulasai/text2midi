# -*- coding: utf-8 -*-
"""
Music Theory Validator Node: Validate harmonic and melodic choices.
"""

import logging

from src.agents.state import MusicState
from src.config.genre_registry import get_genre_instruments

logger = logging.getLogger(__name__)


def music_theory_validator_node(state: MusicState) -> MusicState:
    """
    Agent Node: Validate harmonic, melodic, and rhythmic choices.
    Ensures the planned tracks follow music theory principles.
    """
    logger.info("\n[THEORY] [MUSIC THEORY VALIDATOR] Validating musical choices...")
    
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
        
        # Check 1: Genre-appropriate instruments (uses genre registry as SSOT)
        known_instruments = {name for name, _, _ in get_genre_instruments(intent.genre)}
        for track in track_plan:
            if track.instrument not in known_instruments and track.track_type != "drums":
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
            logger.info("[OK] All music theory checks passed")
        else:
            logger.warning("[WARN] Theory issues found (%d)", len(issues))
            for issue in issues[:3]:
                logger.warning("   - %s", issue)
            if len(issues) > 3:
                logger.warning("   ... and %d more", len(issues) - 3)
        
    except Exception as e:
        state["error"] = f"Theory validation failed: {str(e)}"
        state["theory_valid"] = False
    
    return state
