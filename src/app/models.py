# -*- coding: utf-8 -*-
"""
Data Models for MidiGen Application
Core data structures for music generation.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any
from datetime import datetime
import uuid


@dataclass
class Note:
    """Represents a MIDI note."""
    pitch: int
    start_time: float
    duration: float
    velocity: int = 80
    channel: int = 0


@dataclass
class TrackConfig:
    """Configuration for a single track."""
    track_type: str  # lead, counter_melody, harmony, bass, drums, arpeggio, pad, fx
    instrument: str
    role: str
    priority: int = 1
    channel: int = 0


@dataclass
class Track:
    """Represents a MIDI track with notes."""
    name: str
    notes: List[Note]
    midi_program: int
    channel: int = 0
    track_type: str = "melody"


@dataclass
class GenerationSnapshot:
    """Snapshot of a generation for history."""
    timestamp: datetime
    prompt: str
    tracks: List[Track]
    tempo: int
    key: str
    mode: str
    bars: int


@dataclass
class CompositionSession:
    """Session state for multi-turn composition."""
    session_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    created_at: datetime = field(default_factory=datetime.now)
    
    # Current composition state
    tracks: List[Track] = field(default_factory=list)
    tempo: int = 120
    key: str = "C"
    mode: str = "major"
    llm_provider: str = ""
    genre: str = "pop"
    total_bars: int = 0
    
    # Conversation context
    messages: List[Dict[str, str]] = field(default_factory=list)
    generations: List[GenerationSnapshot] = field(default_factory=list)
    preferences: Dict[str, Any] = field(default_factory=dict)
