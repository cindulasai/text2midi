# -*- coding: utf-8 -*-
"""
LangGraph state definitions for agentic music generation.
Defines the shared state that flows through all agents.
"""

from typing_extensions import TypedDict
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime


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
