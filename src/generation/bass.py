# -*- coding: utf-8 -*-
"""
Bass generation strategies.

Each public function returns ``List[Note]``.  The router
:func:`generate_bass` picks the right strategy.
"""

from __future__ import annotations

import random
from typing import List

from src.app.models import Note
from src.app.constants import CHORD_PROGRESSIONS


# ---------------------------------------------------------------------------
# Router (replaces AdvancedMusicGenerator.generate_smart_bass)
# ---------------------------------------------------------------------------

def generate_bass(
    root: int,
    genre: str,
    bars: int,
    energy: str,
    style_descriptors: List[str] | None = None,
) -> List[Note]:
    """Generate a bass line using the strategy best matching the intent."""
    style_descriptors = style_descriptors or []
    progression = CHORD_PROGRESSIONS.get(genre, CHORD_PROGRESSIONS["pop"])
    beats_per_chord = 4

    if "funky" in style_descriptors + [genre] or genre == "funk":
        return _funky(root, progression, bars, beats_per_chord)
    if genre == "ambient" or "peaceful" in style_descriptors:
        return _ambient(root, progression, bars, beats_per_chord)
    if genre == "jazz":
        return _walking(root, progression, bars)
    if genre in ("rock", "metal"):
        return _power(root, progression, bars, beats_per_chord, energy)
    if genre == "electronic":
        return _synth(root, progression, bars, beats_per_chord, energy)
    return _standard(root, progression, bars, beats_per_chord, energy)


def generate_bass_basic(
    root: int,
    genre: str,
    bars: int,
    energy: str = "medium",
) -> List[Note]:
    """Simple bass (replaces MusicGenerator.generate_bass)."""
    notes: List[Note] = []
    progression = CHORD_PROGRESSIONS.get(genre, CHORD_PROGRESSIONS["pop"])
    beats_per_chord = 4
    beat = 0.0
    chord_idx = 0

    while beat < bars * 4:
        chord = progression[chord_idx % len(progression)]
        bass_note = root + chord[0] - 24

        if genre in ("electronic", "rock", "funk"):
            for i in range(8):
                vel = 95 if i % 2 == 0 else 75
                notes.append(Note(pitch=bass_note, start_time=beat + i * 0.5,
                                  duration=0.4, velocity=vel, channel=2))
        elif genre == "jazz":
            for i in range(4):
                walk = bass_note + random.choice([0, 2, 4, 7])
                notes.append(Note(pitch=walk, start_time=beat + i,
                                  duration=0.9, velocity=75, channel=2))
        else:
            for i in range(4):
                notes.append(Note(pitch=bass_note, start_time=beat + i,
                                  duration=0.9, velocity=80, channel=2))

        beat += beats_per_chord
        chord_idx += 1
    return notes


# ---------------------------------------------------------------------------
# Strategy implementations
# ---------------------------------------------------------------------------

def _funky(root: int, progression, bars: int, bpc: int) -> List[Note]:
    notes: List[Note] = []
    beat = 0.0
    cidx = 0
    for _ in range(bars):
        chord = progression[cidx % len(progression)]
        bn = root + chord[0] - 24
        for t in [0, 0.5, 1.5, 2.0, 2.5, 3.0, 3.5]:
            vel = 100 if t % 1 == 0 else 70
            notes.append(Note(pitch=bn, start_time=beat + t, duration=0.4, velocity=vel, channel=2))
        beat += bpc
        cidx += 1
    return notes


def _ambient(root: int, progression, bars: int, bpc: int) -> List[Note]:
    notes: List[Note] = []
    beat = 0.0
    cidx = 0
    for _ in range(bars):
        chord = progression[cidx % len(progression)]
        bn = root + chord[0] - 24
        notes.append(Note(pitch=bn, start_time=beat, duration=bpc - 0.5, velocity=55, channel=2))
        beat += bpc
        cidx += 1
    return notes


def _walking(root: int, progression, bars: int) -> List[Note]:
    notes: List[Note] = []
    beat = 0.0
    cidx = 0
    for _ in range(bars):
        chord = progression[cidx % len(progression)]
        for i in range(4):
            wn = root + chord[i % len(chord)] - 24
            notes.append(Note(pitch=wn, start_time=beat + i, duration=0.9, velocity=75, channel=2))
        beat += 4
        cidx += 1
    return notes


def _power(root: int, progression, bars: int, bpc: int, energy: str) -> List[Note]:
    notes: List[Note] = []
    beat = 0.0
    cidx = 0
    for _ in range(bars):
        chord = progression[cidx % len(progression)]
        bn = root + chord[0] - 24
        cnt = 8 if energy == "high" else 4
        for i in range(cnt):
            vel = 105 if i % 2 == 0 else 75
            notes.append(Note(pitch=bn, start_time=beat + i * 0.5, duration=0.4, velocity=vel, channel=2))
        beat += bpc
        cidx += 1
    return notes


def _synth(root: int, progression, bars: int, bpc: int, energy: str) -> List[Note]:
    notes: List[Note] = []
    beat = 0.0
    cidx = 0
    for _ in range(bars):
        chord = progression[cidx % len(progression)]
        bn = [root + chord[0] - 24, root + chord[0] - 12]
        if energy == "high":
            for t in [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5]:
                pitch = bn[int(t) % len(bn)]
                notes.append(Note(pitch=pitch, start_time=beat + t, duration=0.4,
                                  velocity=random.randint(80, 100), channel=2))
        else:
            notes.append(Note(pitch=bn[0], start_time=beat, duration=bpc - 0.5, velocity=75, channel=2))
        beat += bpc
        cidx += 1
    return notes


def _standard(root: int, progression, bars: int, bpc: int, energy: str) -> List[Note]:
    notes: List[Note] = []
    beat = 0.0
    cidx = 0
    for _ in range(bars):
        chord = progression[cidx % len(progression)]
        bn = root + chord[0] - 24
        for i in range(4):
            notes.append(Note(pitch=bn, start_time=beat + i, duration=0.9, velocity=80, channel=2))
        beat += bpc
        cidx += 1
    return notes
