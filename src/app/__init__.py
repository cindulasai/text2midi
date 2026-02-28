# -*- coding: utf-8 -*-
"""
MidiGen Application Package
AI-powered music generation library.
"""

from src.app.models import (
    Note, Track, TrackConfig, GenerationSnapshot, CompositionSession
)
from src.app.generator import MusicGenerator
from src.app.midi_creator import MIDIGenerator
from src.app.track_planner import TrackPlanner
from src.app.constants import (
    NOTE_TO_MIDI, DRUM_MAP, GM_INSTRUMENTS, SCALES, GENRE_CONFIG, CHORD_PROGRESSIONS
)
from src.app.errors import (  # noqa: F401
    PipelineError, IntentParsingError, TrackPlanningError,
    TheoryValidationError, GenerationError, MIDICreationError,
    QualityAssessmentError, LLMProviderError,
)

__version__ = "2.0.0"
__all__ = [
    "Note",
    "Track",
    "TrackConfig",
    "GenerationSnapshot",
    "CompositionSession",
    "MusicGenerator",
    "MIDIGenerator",
    "TrackPlanner",
    "NOTE_TO_MIDI",
    "DRUM_MAP",
    "GM_INSTRUMENTS",
    "SCALES",
    "GENRE_CONFIG",
    "CHORD_PROGRESSIONS",
    # Errors
    "PipelineError",
    "IntentParsingError",
    "TrackPlanningError",
    "TheoryValidationError",
    "GenerationError",
    "MIDICreationError",
    "QualityAssessmentError",
    "LLMProviderError",
]
