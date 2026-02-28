# -*- coding: utf-8 -*-
"""
Music Generation Engine — basic facade.

Delegates to focused strategy modules in :mod:`src.generation`.
Preserves the original public API so callers need no changes.
"""

from typing import List

from src.app.models import Note
from src.generation.melody import generate_melody_basic, generate_counter_melody
from src.generation.bass import generate_bass_basic
from src.generation.drums import generate_drums_basic
from src.generation.pad import (
    generate_pad_basic,
    generate_chords,
    generate_arpeggio,
    generate_fx,
)


class MusicGenerator:
    """Generates musical content for different track types."""

    def generate_melody(self, root: int, mode: str, bars: int, energy: str, genre: str) -> List[Note]:
        return generate_melody_basic(root, mode, bars, energy, genre)

    def generate_counter_melody(self, root: int, mode: str, bars: int, energy: str) -> List[Note]:
        return generate_counter_melody(root, mode, bars, energy)

    def generate_chords(self, root: int, genre: str, bars: int) -> List[Note]:
        return generate_chords(root, genre, bars)

    def generate_arpeggio(self, root: int, genre: str, bars: int, energy: str) -> List[Note]:
        return generate_arpeggio(root, genre, bars, energy)

    def generate_bass(self, root: int, genre: str, bars: int, energy: str = "medium") -> List[Note]:
        return generate_bass_basic(root, genre, bars, energy)

    def generate_pad(self, root: int, mode: str, bars: int) -> List[Note]:
        return generate_pad_basic(root, mode, bars)

    def generate_drums(self, genre: str, bars: int, energy: str) -> List[Note]:
        return generate_drums_basic(genre, bars, energy)

    def generate_fx(self, root: int, bars: int) -> List[Note]:
        return generate_fx(root, bars)
