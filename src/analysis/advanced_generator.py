# -*- coding: utf-8 -*-
"""
Advanced Music Generator — emotion-aware facade.

Delegates to focused strategy modules in :mod:`src.generation`.
Preserves the original public API so callers need no changes.
"""

from __future__ import annotations

from typing import List

from src.app.models import Note
from src.generation.common import GenerationStyle, MusicPhrase  # re-export for dependents
from src.generation.melody import generate_melody, generate_counter_melody
from src.generation.bass import generate_bass
from src.generation.drums import generate_drums
from src.generation.pad import generate_pad


class AdvancedMusicGenerator:
    """
    Generates diverse musical content with deep prompt awareness.

    Thin facade — each method delegates to the matching strategy module.
    """

    def __init__(self, session_id: str = "default"):
        self.session_id = session_id
        self.call_counter = 0

    # -- Melody ----------------------------------------------------------

    def generate_aware_melody(
        self,
        root: int,
        mode: str,
        bars: int,
        energy: str,
        genre: str,
        style_descriptors: List[str] | None = None,
        emotions: List[str] | None = None,
        complexity: str = "moderate",
    ) -> List[Note]:
        self.call_counter += 1
        return generate_melody(
            root, mode, bars, energy, genre,
            style_descriptors=style_descriptors,
            emotions=emotions,
            complexity=complexity,
        )

    # -- Bass ------------------------------------------------------------

    def generate_smart_bass(
        self,
        root: int,
        genre: str,
        bars: int,
        energy: str,
        style_descriptors: List[str] | None = None,
    ) -> List[Note]:
        return generate_bass(root, genre, bars, energy, style_descriptors=style_descriptors)

    # -- Drums -----------------------------------------------------------

    def generate_smart_drums(
        self,
        genre: str,
        bars: int,
        energy: str,
        style_descriptors: List[str] | None = None,
        emotions: List[str] | None = None,
    ) -> List[Note]:
        return generate_drums(genre, bars, energy, style_descriptors=style_descriptors, emotions=emotions)

    # -- Pad / Atmosphere ------------------------------------------------

    def generate_smart_pad(
        self,
        root: int,
        mode: str,
        bars: int,
        style_descriptors: List[str] | None = None,
        emotions: List[str] | None = None,
    ) -> List[Note]:
        return generate_pad(root, mode, bars, style_descriptors=style_descriptors, emotions=emotions)
