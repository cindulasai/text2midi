# -*- coding: utf-8 -*-
"""
Drum pattern generation strategies.

Each public function returns ``List[Note]``.  The router
:func:`generate_drums` picks the right strategy.
"""

from __future__ import annotations

import random
from typing import List

from src.app.models import Note
from src.app.constants import DRUM_MAP


# ---------------------------------------------------------------------------
# Router (replaces AdvancedMusicGenerator.generate_smart_drums)
# ---------------------------------------------------------------------------

def generate_drums(
    genre: str,
    bars: int,
    energy: str,
    style_descriptors: List[str] | None = None,
    emotions: List[str] | None = None,
) -> List[Note]:
    """Generate a drum pattern using the strategy best matching the intent."""
    style_descriptors = style_descriptors or []
    emotions = emotions or []

    if "minimal" in style_descriptors or genre == "ambient":
        return _minimal(genre, bars, energy)
    if "jazzy" in style_descriptors or genre == "jazz":
        return _jazz(bars)
    if "hip hop" in style_descriptors + [genre] or genre == "lofi":
        return _hiphop(bars, energy)
    if "progressive" in style_descriptors or genre in ("progressive", "metal"):
        return _progressive(genre, bars, energy)
    if "uplifting" in emotions or "epic" in style_descriptors:
        return _epic(bars, energy)
    return _standard(genre, bars, energy)


def generate_drums_basic(
    genre: str,
    bars: int,
    energy: str,
) -> List[Note]:
    """Simple drums (replaces MusicGenerator.generate_drums)."""
    notes: List[Note] = []

    if genre == "electronic":
        kick_p = [0, 1, 2, 3]
        snare_p = [1, 3]
        hh_p = [i * 0.25 for i in range(16)]
    elif genre == "jazz":
        kick_p = [0, 2.5]
        snare_p: list = []
        hh_p = [i * (1 / 3) for i in range(12)]
    elif genre == "rock":
        kick_p = [0, 2]
        snare_p = [1, 3]
        hh_p = [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5]
    else:
        kick_p = [0, 2]
        snare_p = [1, 3]
        hh_p = [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5] if energy != "low" else [0, 1, 2, 3]

    for bar in range(bars):
        bs = bar * 4
        for b in kick_p:
            notes.append(Note(pitch=DRUM_MAP["kick"], start_time=bs + b, duration=0.5, velocity=100, channel=9))
        for b in snare_p:
            notes.append(Note(pitch=DRUM_MAP["snare"], start_time=bs + b, duration=0.5, velocity=90, channel=9))
        for b in hh_p:
            if bs + b < (bar + 1) * 4:
                vel = 60 if b % 1 != 0 else 75
                notes.append(Note(pitch=DRUM_MAP["closed_hihat"], start_time=bs + b, duration=0.25, velocity=vel, channel=9))
        if bar % 4 == 0:
            notes.append(Note(pitch=DRUM_MAP["crash"], start_time=bs, duration=2.0, velocity=85, channel=9))
    return notes


# ---------------------------------------------------------------------------
# Strategy implementations
# ---------------------------------------------------------------------------

def _minimal(_genre: str, bars: int, _energy: str) -> List[Note]:
    notes: List[Note] = []
    for bar in range(bars):
        bs = bar * 4
        notes.append(Note(pitch=DRUM_MAP["kick"], start_time=bs, duration=0.5, velocity=100, channel=9))
        notes.append(Note(pitch=DRUM_MAP["kick"], start_time=bs + 2, duration=0.5, velocity=100, channel=9))
    return notes


def _jazz(bars: int) -> List[Note]:
    notes: List[Note] = []
    for bar in range(bars):
        bs = bar * 4
        notes.append(Note(pitch=DRUM_MAP["kick"], start_time=bs, duration=0.5, velocity=90, channel=9))
        notes.append(Note(pitch=DRUM_MAP["kick"], start_time=bs + 2.5, duration=0.5, velocity=80, channel=9))
        notes.append(Note(pitch=DRUM_MAP["snare"], start_time=bs + 1.5, duration=0.5, velocity=85, channel=9))
        for t in [0, 2 / 3, 1.33, 2, 2.67, 3.33]:
            notes.append(Note(pitch=DRUM_MAP["closed_hihat"], start_time=bs + t, duration=0.2, velocity=70, channel=9))
    return notes


def _hiphop(bars: int, _energy: str) -> List[Note]:
    notes: List[Note] = []
    for bar in range(bars):
        bs = bar * 4
        notes.append(Note(pitch=DRUM_MAP["kick"], start_time=bs, duration=0.5, velocity=105, channel=9))
        notes.append(Note(pitch=DRUM_MAP["kick"], start_time=bs + 2.5, duration=0.5, velocity=95, channel=9))
        notes.append(Note(pitch=DRUM_MAP["snare"], start_time=bs + 1.5, duration=0.5, velocity=95, channel=9))
        notes.append(Note(pitch=DRUM_MAP["snare"], start_time=bs + 3.5, duration=0.5, velocity=85, channel=9))
        for t in [0, 1, 2, 3]:
            notes.append(Note(pitch=DRUM_MAP["closed_hihat"], start_time=bs + t, duration=0.25, velocity=50, channel=9))
    return notes


def _progressive(_genre: str, bars: int, energy: str) -> List[Note]:
    notes: List[Note] = []
    for bar in range(bars):
        bs = bar * 4
        kick_times = [0, 0.75, 1.5, 2.25, 3, 3.75] if energy == "high" else [0, 1.5, 2.5, 3.5]
        for t in kick_times:
            notes.append(Note(pitch=DRUM_MAP["kick"], start_time=bs + t, duration=0.35, velocity=100, channel=9))
        for t in [1, 3, 1.75, 3.25]:
            notes.append(Note(pitch=DRUM_MAP["snare"], start_time=bs + t, duration=0.4, velocity=90, channel=9))
        for t in [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5]:
            hat = DRUM_MAP["open_hihat"] if t % 1 == 0.5 else DRUM_MAP["closed_hihat"]
            notes.append(Note(pitch=hat, start_time=bs + t, duration=0.2, velocity=random.randint(60, 80), channel=9))
    return notes


def _epic(bars: int, _energy: str) -> List[Note]:
    notes: List[Note] = []
    for bar in range(bars):
        bs = bar * 4
        notes.append(Note(pitch=DRUM_MAP["kick"], start_time=bs, duration=0.6, velocity=110, channel=9))
        notes.append(Note(pitch=DRUM_MAP["kick"], start_time=bs + 2, duration=0.6, velocity=105, channel=9))
        notes.append(Note(pitch=DRUM_MAP["kick"], start_time=bs + 3.5, duration=0.5, velocity=95, channel=9))
        notes.append(Note(pitch=DRUM_MAP["snare"], start_time=bs + 1, duration=0.5, velocity=100, channel=9))
        notes.append(Note(pitch=DRUM_MAP["snare"], start_time=bs + 3, duration=0.5, velocity=95, channel=9))
        if bar % 4 == 3:
            for t in [0, 0.25, 0.5, 0.75]:
                notes.append(Note(pitch=DRUM_MAP.get("tom_mid", 48), start_time=bs + 3 + t,
                                  duration=0.2, velocity=85, channel=9))
    return notes


def _standard(_genre: str, bars: int, _energy: str) -> List[Note]:
    notes: List[Note] = []
    for bar in range(bars):
        bs = bar * 4
        notes.append(Note(pitch=DRUM_MAP["kick"], start_time=bs, duration=0.5, velocity=100, channel=9))
        notes.append(Note(pitch=DRUM_MAP["kick"], start_time=bs + 2, duration=0.5, velocity=100, channel=9))
        notes.append(Note(pitch=DRUM_MAP["snare"], start_time=bs + 1, duration=0.5, velocity=90, channel=9))
        notes.append(Note(pitch=DRUM_MAP["snare"], start_time=bs + 3, duration=0.5, velocity=90, channel=9))
        for t in [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5]:
            vel = 75 if t % 1 == 0 else 60
            notes.append(Note(pitch=DRUM_MAP["closed_hihat"], start_time=bs + t, duration=0.25, velocity=vel, channel=9))
    return notes
