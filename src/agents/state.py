# -*- coding: utf-8 -*-
"""
LangGraph state definitions for agentic music generation.
Defines the shared state that flows through all agents.

Also hosts legacy dataclasses (``EnhancedMusicIntent``, ``CompositionStructure``,
``CompositionComplexity``, ``MusicalStyle``) previously in the deprecated
``src.analysis.advanced_intent_parser`` module.
"""

from typing_extensions import TypedDict
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


@dataclass
class MusicIntent:
    """Parsed user intent."""
    action: str  # "new", "extend", "modify", "analyze"
    genre: str
    mood: str
    energy: str
    track_count: Optional[int]
    duration_requested: Optional[int]
    specific_instruments: List[str]
    style_descriptors: List[str]
    tempo_preference: Optional[int]
    key_preference: Optional[str]
    raw_prompt: str


# ---------------------------------------------------------------------------
# Legacy types migrated from src.analysis.advanced_intent_parser (deprecated).
# Still used by the agentic graph compatibility bridge in src.intent.engine.
# ---------------------------------------------------------------------------

class MusicalStyle(Enum):
    """Detected musical style from prompt."""
    AMBIENT = "ambient"
    CINEMATIC = "cinematic"
    RHYTHMIC = "rhythmic"
    MELODIC = "melodic"
    HARMONIC = "harmonic"
    PERCUSSIVE = "percussive"
    MINIMALIST = "minimalist"
    COMPLEX = "complex"


class CompositionComplexity(Enum):
    """How complex the composition should be."""
    SIMPLE = "simple"
    MODERATE = "moderate"
    RICH = "rich"
    VERY_COMPLEX = "very_complex"


@dataclass
class CompositionStructure:
    """Detailed composition structure inferred from duration and intent."""
    total_bars: int
    tempo: int
    time_signature: str = "4/4"

    # Structure sections (bars each)
    intro_bars: int = 0
    verse_bars: int = 0
    chorus_bars: int = 0
    bridge_bars: int = 0
    outro_bars: int = 0

    # Musical characteristics
    main_scale: str = "major"
    complexity: CompositionComplexity = CompositionComplexity.MODERATE
    primary_styles: List[MusicalStyle] = field(default_factory=list)

    # Pacing
    energy_arc: str = "build"  # "build", "smooth", "dynamic", "decay"
    intro_density: float = 0.3  # 0-1, how full the intro is

    def total_seconds(self) -> float:
        """Calculate total duration in seconds."""
        beats = self.total_bars * 4  # Assuming 4/4
        return (beats / self.tempo) * 60


@dataclass
class EnhancedMusicIntent:
    """Enhanced music intent with deep semantic understanding."""
    action: str
    genre: str
    mood: str
    energy: str

    # Duration details
    duration_seconds: Optional[int] = None
    duration_bars: Optional[int] = None

    # Instruments
    specific_instruments: List[str] = field(default_factory=list)
    instrument_priorities: Dict[str, int] = field(default_factory=dict)

    # Style
    style_descriptors: List[str] = field(default_factory=list)
    emotions: List[str] = field(default_factory=list)
    dynamics: str = "moderate"  # "minimal", "moderate", "dramatic"

    # Preferences
    tempo_preference: Optional[int] = None
    key_preference: Optional[str] = None
    complexity: CompositionComplexity = CompositionComplexity.MODERATE

    # Composition structure
    composition_structure: Optional[CompositionStructure] = None

    # Reasoning
    reasoning: List[str] = field(default_factory=list)

    # Original prompt
    raw_prompt: str = ""


@dataclass
class TrackConfig:
    """Configuration for a single track."""
    track_type: str
    instrument: str
    role: str
    priority: int = 1
    channel: int = 0


@dataclass
class TrackQualityIssue:
    """Quality issue found in generated tracks."""
    track_index: int
    issue_type: str  # "harmony", "rhythm", "density", "instrumentation", "voice_leading"
    severity: str  # "low", "medium", "high"
    description: str
    suggestion: str


@dataclass
class GenerationQualityReport:
    """Quality assessment of generated music."""
    overall_score: float  # 0-1
    issues: List[TrackQualityIssue] = field(default_factory=list)
    needs_refinement: bool = False
    refinement_suggestions: List[str] = field(default_factory=list)
    positive_aspects: List[str] = field(default_factory=list)


class MusicState(TypedDict, total=False):
    """Complete state for agentic music generation workflow."""
    
    # User input
    user_prompt: str
    
    # Parsed intent (from intent agent)
    intent: Optional[MusicIntent]
    parsed_intent: Optional[Any]  # ParsedIntent from src.intent.schema (rich Pydantic model)
    enhanced_intent: Optional[EnhancedMusicIntent]  # deep semantic understanding
    
    # Composition structure (from intent parser)
    composition_structure: Optional[CompositionStructure]
    
    # Track planning (from planner agent)
    track_plan: List[TrackConfig]
    
    # Theory validation (from validator agent)
    theory_validation: Dict[str, Any]
    theory_valid: bool
    theory_issues: List[str]
    
    # Generated tracks (from generator agent)
    generated_tracks: List[Any]  # List[Track]
    generation_metadata: Dict[str, Any]
    
    # Quality assessment (from QA agent)
    quality_report: Optional[GenerationQualityReport]
    intelligent_quality_report: Optional[Any]  # IntelligentQualityReviewer report
    previous_quality_reviews: List[Any]  # history for consistency checking
    
    # Refinement (from refinement agent)
    refinement_attempts: int
    refinement_feedback: str
    needs_refinement: bool
    
    # Final output
    final_midi_path: Optional[str]
    session_summary: str
    
    # Context and history
    messages: List[Dict[str, str]]
    error: Optional[str]
    error_context: Optional[str]
    
    # Session info
    session_id: str
    composition_state: Dict[str, Any]
    
    # Control flags
    max_refinement_iterations: int
    current_iteration: int
