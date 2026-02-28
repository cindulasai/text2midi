# -*- coding: utf-8 -*-
"""
Common enums and helpers shared across generation strategies.
"""

from __future__ import annotations

import random
from enum import Enum
from typing import List

from src.app.models import Note


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class MusicPhrase(Enum):
    """Musical phrase contour patterns."""
    ASCENDING = "ascending"
    DESCENDING = "descending"
    ARCH = "arch"          # Up then down
    VALLEY = "valley"      # Down then up
    REPETITIVE = "repetitive"
    WANDERING = "wandering"
    CALL_RESPONSE = "call_response"


class GenerationStyle(Enum):
    """High-level generation style inferred from user intent."""
    MINIMAL = "minimal"
    FLOWING = "flowing"
    RHYTHMIC = "rhythmic"
    CHAOTIC = "chaotic"
    STRUCTURED = "structured"
    ORGANIC = "organic"


# ---------------------------------------------------------------------------
# Strategy selector
# ---------------------------------------------------------------------------

def determine_style(
    genre: str,
    style_descriptors: List[str],
    emotions: List[str],
    energy: str,
) -> GenerationStyle:
    """Pick a :class:`GenerationStyle` from intent attributes."""
    if "ambient" in style_descriptors + [genre] or "peaceful" in emotions:
        return GenerationStyle.MINIMAL
    if "chaotic" in style_descriptors or genre in ("metal", "industrial"):
        return GenerationStyle.CHAOTIC
    if "rhythmic" in style_descriptors or genre in ("funk", "electronic"):
        return GenerationStyle.RHYTHMIC
    if genre in ("jazz", "classical"):
        return GenerationStyle.ORGANIC
    if energy == "high" and genre not in ("ambient", "lofi"):
        return GenerationStyle.FLOWING
    if "structured" in style_descriptors or genre == "classical":
        return GenerationStyle.STRUCTURED
    return GenerationStyle.ORGANIC


# ---------------------------------------------------------------------------
# Phrase helpers
# ---------------------------------------------------------------------------

def create_directional_phrase(
    root: int,
    scale: List[int],
    phrase_type: MusicPhrase,
    length: float,
) -> List[Note]:
    """Build a short melodic phrase with the given contour."""
    notes: List[Note] = []
    beat = 0.0
    note_count = max(1, int(length / 0.5))
    scale_max = len(scale) - 1

    if phrase_type == MusicPhrase.ASCENDING:
        for i in range(note_count):
            idx = (i * scale_max) // note_count
            dur = length / note_count
            notes.append(Note(pitch=root + scale[idx], start_time=beat, duration=dur, velocity=75))
            beat += dur

    elif phrase_type == MusicPhrase.DESCENDING:
        for i in range(note_count):
            idx = scale_max - (i * scale_max) // note_count
            dur = length / note_count
            notes.append(Note(pitch=root + scale[idx], start_time=beat, duration=dur, velocity=75))
            beat += dur

    elif phrase_type == MusicPhrase.ARCH:
        for i in range(note_count):
            if i < note_count / 2:
                idx = (i * scale_max) // (note_count / 2)
            else:
                idx = scale_max - ((i - note_count / 2) * scale_max) // (note_count / 2)
            dur = length / note_count
            notes.append(Note(pitch=root + scale[int(idx) % len(scale)], start_time=beat, duration=dur, velocity=75))
            beat += dur

    return notes
