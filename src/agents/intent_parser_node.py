# -*- coding: utf-8 -*-
"""
Intent Parser Node: Extract musical intent from user prompts.
Uses advanced semantic understanding with chain-of-thought reasoning.
"""

import os
from src.agents.state import MusicState, MusicIntent

try:
    from src.midigent.advanced_intent_parser import AdvancedIntentParser, EnhancedMusicIntent
    ADVANCED_PARSER_AVAILABLE = True
except ImportError:
    ADVANCED_PARSER_AVAILABLE = False

try:
    from src.midigent.intent_parser import IntentParser
    INTENT_PARSER_AVAILABLE = True
except ImportError:
    INTENT_PARSER_AVAILABLE = False


def intent_parser_node(state: MusicState) -> MusicState:
    """
    Agent Node: Parse user prompt and extract musical intent.
    Uses advanced semantic understanding with composition structure planning.
    """
    print("\n[INTENT AGENT] Analyzing user request with deep semantic understanding...")
    
    user_prompt = state.get("user_prompt", "")
    
    if not user_prompt:
        state["error"] = "No user prompt provided"
        return state
    
    try:
        # Try advanced parser first for deep semantic understanding
        if ADVANCED_PARSER_AVAILABLE:
            enhanced_intent = AdvancedIntentParser.parse_intent_deeply(user_prompt)
            
            # Display reasoning chain
            print("\nPARSING REASONING CHAIN:")
            for line in enhanced_intent.reasoning[:15]:  # Show first 15 lines
                print(f"   {line}")
            
            # Convert to MusicIntent
            intent = MusicIntent(
                action=enhanced_intent.action,
                genre=enhanced_intent.genre,
                mood=enhanced_intent.mood,
                energy=enhanced_intent.energy,
                track_count=len(enhanced_intent.specific_instruments) or 4,
                duration_requested=enhanced_intent.duration_bars,
                specific_instruments=enhanced_intent.specific_instruments,
                style_descriptors=enhanced_intent.style_descriptors,
                tempo_preference=enhanced_intent.tempo_preference,
                key_preference=enhanced_intent.key_preference,
                raw_prompt=user_prompt
            )
            
            state["intent"] = intent
            
            # Store enhanced intent for later use
            state["enhanced_intent"] = enhanced_intent
            state["composition_structure"] = enhanced_intent.composition_structure
            
            print(f"\n[OK] INTENT PARSED: Genre={intent.genre} | Energy={intent.energy}")
            print(f"   Duration: {enhanced_intent.duration_bars} bars ({enhanced_intent.duration_seconds}s)")
            print(f"   Complexity: {enhanced_intent.complexity.value}")
            print(f"   Structure: I:{enhanced_intent.composition_structure.intro_bars} V:{enhanced_intent.composition_structure.verse_bars} C:{enhanced_intent.composition_structure.chorus_bars} B:{enhanced_intent.composition_structure.bridge_bars} O:{enhanced_intent.composition_structure.outro_bars}")
            
        else:
            # Fallback to basic parser if advanced not available
            if INTENT_PARSER_AVAILABLE:
                parser = IntentParser()
                intent_dict = parser.parse_intent(user_prompt)
            else:
                intent_dict = _parse_intent_basic(user_prompt)
            
            # Convert to MusicIntent object
            intent = MusicIntent(
                action=intent_dict.get("action", "new"),
                genre=intent_dict.get("genre", "pop"),
                mood=intent_dict.get("mood", ""),
                energy=intent_dict.get("energy", "medium"),
                track_count=intent_dict.get("track_count"),
                duration_requested=intent_dict.get("bars"),
                specific_instruments=intent_dict.get("instruments", []),
                style_descriptors=intent_dict.get("descriptors", []),
                tempo_preference=intent_dict.get("tempo"),
                key_preference=intent_dict.get("key"),
                raw_prompt=user_prompt
            )
            
            state["intent"] = intent
            
            # Create a default composition structure for fallback path
            from dataclasses import dataclass, field
            from typing import List
            
            @dataclass
            class DefaultCompositionStructure:
                total_bars: int = 64
                tempo: int = 120
                time_signature: str = "4/4"
                intro_bars: int = 8
                verse_bars: int = 16
                chorus_bars: int = 16
                bridge_bars: int = 8
                outro_bars: int = 8
                main_scale: str = "major"
                complexity: str = "moderate"
                primary_styles: List[str] = field(default_factory=list)
                energy_arc: str = "smooth"
                intro_density: float = 0.4
                
                def __post_init__(self):
                    # Dynamically set total_bars and outro_bars based on intent
                    bars = int(intent_dict.get("bars", 64))
                    self.total_bars = bars
                    self.outro_bars = max(bars - 48, 8)
                    self.tempo = intent_dict.get("tempo", 120)
            
            comp_struct = DefaultCompositionStructure()
            state["composition_structure"] = comp_struct
            state["enhanced_intent"] = intent  # For backward compatibility
            
            print(f"\n[OK] INTENT PARSED - BASIC: Genre={intent.genre} | Energy={intent.energy}")
            print(f"   Duration: {intent.duration_requested} bars")
        
    except Exception as e:
        state["error"] = f"Intent parsing failed: {str(e)}"
        print(f"[ERROR] Error: {state['error']}")
    
    return state


def _parse_intent_basic(prompt: str) -> dict:
    """Basic fallback intent parser."""
    prompt_lower = prompt.lower()
    
    genre = "pop"
    for g in ["rock", "jazz", "classical", "electronic", "lofi", "ambient", "cinematic", "funk", "rnb"]:
        if g in prompt_lower:
            genre = g
            break
    
    energy = "medium"
    if "intense" in prompt_lower or "energetic" in prompt_lower or "high" in prompt_lower:
        energy = "high"
    elif "chill" in prompt_lower or "ambient" in prompt_lower or "relaxing" in prompt_lower:
        energy = "low"
    
    return {
        "action": "new",
        "genre": genre,
        "mood": prompt,
        "energy": energy,
        "track_count": None,
        "bars": 16,
        "instruments": [],
        "descriptors": [],
        "tempo": None,
        "key": None,
    }
