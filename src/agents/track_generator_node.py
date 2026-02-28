# -*- coding: utf-8 -*-
"""
Track Generator Node: Generate actual musical tracks with advanced awareness.
Uses AdvancedMusicGenerator which creates diverse, emotion-aware content.
"""

import logging
from pathlib import Path
from src.agents.state import MusicState

logger = logging.getLogger(__name__)


def track_generator_node(state: MusicState) -> MusicState:
    """
    Agent Node: Generate actual musical tracks with deep intent awareness.
    
    Uses AdvancedMusicGenerator which:
    - Creates different melodic patterns for different emotions/genres
    - Selects appropriate instruments for user intent
    - Generates genre-specific bass and drum patterns
    - Responds to style descriptors and emotions
    """
    logger.info("\n[PIANO] [TRACK GENERATOR] Generating aware musical tracks...")
    
    if state.get("error"):
        return state
    
    intent = state.get("intent")
    track_plan = state.get("track_plan", [])
    session_id = state.get("session_id", "default")
    
    if not track_plan:
        state["error"] = "No track plan available for generation"
        return state
    
    try:
        # Import advanced tools
        from src.app import NOTE_TO_MIDI, Track
        from src.analysis.advanced_generator import AdvancedMusicGenerator
        from src.analysis.emotion_instruments import EmotionAwareInstrumentMapper
        from src.config.genre_registry import get_genre, find_by_alias
        
        root_note = NOTE_TO_MIDI.get(intent.key_preference or "C", 60)
        
        # Determine mode from genre registry instead of naive string matching
        genre_node = get_genre(intent.genre) or find_by_alias(intent.genre)
        if genre_node:
            mode = genre_node.default_scale
        else:
            mode = "major"  # safe default when genre not found
        bars = intent.duration_requested or 16
        
        # Initialize advanced generator with this session
        advanced_gen = AdvancedMusicGenerator(session_id=session_id)
        
        # Get extended intent information
        style_descriptors = intent.style_descriptors or []
        emotions = getattr(intent, 'emotions', []) or []
        complexity = getattr(intent, 'complexity', 'moderate')
        
        generated_tracks = []
        
        logger.info("   Generating %d tracks...", len(track_plan))
        logger.info("   Style: %s", ', '.join(style_descriptors) if style_descriptors else 'Default')
        logger.info("   Emotions: %s", ', '.join(emotions) if emotions else 'None')
        
        for i, config in enumerate(track_plan):
            logger.info("   [%d/%d] %s (%s)", i+1, len(track_plan), config.track_type, config.instrument)
            
            try:
                # Generate based on track type with awareness
                if config.track_type == "lead":
                    notes = advanced_gen.generate_aware_melody(
                        root_note, mode, bars, intent.energy, intent.genre,
                        style_descriptors=style_descriptors,
                        emotions=emotions,
                        complexity=str(complexity)
                    )
                elif config.track_type == "counter_melody":
                    notes = advanced_gen.generate_aware_melody(
                        root_note, mode, bars, "low", intent.genre,
                        style_descriptors=style_descriptors,
                        emotions=emotions,
                        complexity="moderate"
                    )
                elif config.track_type == "harmony":
                    # Use smart pad generation for harmony
                    notes = advanced_gen.generate_smart_pad(
                        root_note, mode, bars,
                        style_descriptors=style_descriptors,
                        emotions=emotions
                    )
                elif config.track_type == "bass":
                    notes = advanced_gen.generate_smart_bass(
                        root_note, intent.genre, bars, intent.energy,
                        style_descriptors=style_descriptors
                    )
                elif config.track_type == "drums":
                    notes = advanced_gen.generate_smart_drums(
                        intent.genre, bars, intent.energy,
                        style_descriptors=style_descriptors,
                        emotions=emotions
                    )
                elif config.track_type == "arpeggio":
                    notes = advanced_gen.generate_aware_melody(
                        root_note, mode, bars, intent.energy, intent.genre,
                        style_descriptors=style_descriptors + ["rhythmic"],
                        emotions=emotions,
                        complexity="moderate"
                    )
                elif config.track_type == "pad":
                    notes = advanced_gen.generate_smart_pad(
                        root_note, mode, bars,
                        style_descriptors=style_descriptors,
                        emotions=emotions
                    )
                else:
                    # Default: generate adaptive melody
                    notes = advanced_gen.generate_aware_melody(
                        root_note, mode, bars, intent.energy, intent.genre,
                        style_descriptors=style_descriptors,
                        emotions=emotions,
                        complexity=str(complexity)
                    )
                
                track = Track(
                    name=f"{config.track_type.title()} ({config.instrument})",
                    notes=notes,
                    midi_program=_get_midi_program(config.instrument),
                    channel=config.channel,
                    track_type=config.track_type
                )
                generated_tracks.append(track)
                
            except Exception as track_error:
                logger.warning("      ⚠️  Generation for %s had issue: %s", config.track_type, str(track_error))
                # Fall back to basic generation for this track
                from src.app import MusicGenerator
                fallback_gen = MusicGenerator()
                
                if config.track_type == "lead":
                    notes = fallback_gen.generate_melody(root_note, mode, bars, intent.energy, intent.genre)
                elif config.track_type == "bass":
                    notes = fallback_gen.generate_bass(root_note, intent.genre, bars, intent.energy)
                elif config.track_type == "drums":
                    notes = fallback_gen.generate_drums(intent.genre, bars, intent.energy)
                else:
                    notes = fallback_gen.generate_pad(root_note, mode, bars)
                
                track = Track(
                    name=f"{config.track_type.title()} ({config.instrument})",
                    notes=notes,
                    midi_program=_get_midi_program(config.instrument),
                    channel=config.channel,
                    track_type=config.track_type
                )
                generated_tracks.append(track)
        
        state["generated_tracks"] = generated_tracks
        state["generation_metadata"] = {
            "root": intent.key_preference or "C",
            "mode": mode,
            "bars": bars,
            "energy": intent.energy,
            "genre": intent.genre,
            "style": ", ".join(style_descriptors),
            "emotions": ", ".join(emotions),
            "generator": "AdvancedMusicGenerator",
        }
        
        logger.info("[OK] Generated %d tracks with advanced awareness", len(generated_tracks))
        
    except Exception as e:
        import traceback
        state["error"] = f"Track generation failed: {str(e)}\n{traceback.format_exc()}"
        logger.error("[ERROR] Error: %s", state['error'])
    
    return state


def _get_midi_program(instrument: str) -> int:
    """Get MIDI program number for instrument."""
    from src.app import GM_INSTRUMENTS
    return GM_INSTRUMENTS.get(instrument.lower(), 0)
