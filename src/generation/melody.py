# -*- coding: utf-8 -*-
"""
Melody generation strategies.

Each public function accepts ``(root, mode, bars, energy, ...)`` and returns
a ``List[Note]``.  The router :func:`generate_melody` picks the right
strategy based on intent attributes.
"""

from __future__ import annotations

import random
from typing import List

from src.app.models import Note
from src.app.constants import SCALES
from src.generation.common import (
    GenerationStyle,
    MusicPhrase,
    create_directional_phrase,
    determine_style,
)


# ---------------------------------------------------------------------------
# Router (replaces AdvancedMusicGenerator.generate_aware_melody)
# ---------------------------------------------------------------------------

def generate_melody(
    root: int,
    mode: str,
    bars: int,
    energy: str,
    genre: str,
    style_descriptors: List[str] | None = None,
    emotions: List[str] | None = None,
    complexity: str = "moderate",
) -> List[Note]:
    """Generate a melody using the strategy best matching the intent."""
    style_descriptors = style_descriptors or []
    emotions = emotions or []
    strategy = determine_style(genre, style_descriptors, emotions, energy)

    dispatch = {
        GenerationStyle.MINIMAL: _minimal,
        GenerationStyle.FLOWING: _flowing,
        GenerationStyle.RHYTHMIC: _rhythmic,
        GenerationStyle.CHAOTIC: _chaotic,
        GenerationStyle.STRUCTURED: _structured,
        GenerationStyle.ORGANIC: _organic,
    }
    return dispatch[strategy](root, mode, bars, energy, genre)


def generate_melody_basic(
    root: int,
    mode: str,
    bars: int,
    energy: str,
    genre: str,
) -> List[Note]:
    """Simple melody (replaces MusicGenerator.generate_melody)."""
    notes: List[Note] = []
    scale = SCALES.get(mode, SCALES["major"])
    beats = bars * 4
    density = {"low": 0.3, "medium": 0.5, "high": 0.7}.get(energy, 0.5)

    beat = 0.0
    while beat < beats:
        if random.random() < density:
            octave = random.choice([0, 0, 12, 12, -12])
            pitch = root + random.choice(scale) + octave
            durations = [0.5, 1.0, 1.5, 2.0] if energy == "low" else [0.25, 0.5, 0.75, 1.0]
            duration = random.choice(durations)
            velocity = random.randint(60, 90) if energy == "low" else random.randint(70, 110)
            notes.append(Note(pitch=pitch, start_time=beat, duration=duration, velocity=velocity))
            beat += duration
        else:
            beat += 0.5
    return notes


def generate_counter_melody(
    root: int,
    mode: str,
    bars: int,
    energy: str,
) -> List[Note]:
    """Counter-melody complementing the main line."""
    notes: List[Note] = []
    scale = SCALES.get(mode, SCALES["major"])
    beats = bars * 4

    beat = 0.0
    while beat < beats:
        if random.random() < 0.4:
            pitch = root + random.choice(scale[2:5]) + random.choice([-12, 0])
            duration = random.choice([1.0, 1.5, 2.0])
            notes.append(Note(pitch=pitch, start_time=beat, duration=duration,
                              velocity=random.randint(55, 75), channel=1))
            beat += duration
        else:
            beat += 1.0
    return notes


# ---------------------------------------------------------------------------
# Strategy implementations
# ---------------------------------------------------------------------------

def _minimal(root: int, mode: str, bars: int, energy: str, _genre: str = "") -> List[Note]:
    notes: List[Note] = []
    scale = SCALES.get(mode, SCALES["major"])
    beat = 0.0
    beats = bars * 4
    while beat < beats:
        if random.random() < 0.2:
            pitch = root + random.choice(scale)
            dur = random.choice([2.0, 4.0, 8.0])
            notes.append(Note(pitch=pitch, start_time=beat, duration=dur, velocity=random.randint(40, 60)))
            beat += dur
        else:
            beat += 2.0
    return notes


def _flowing(root: int, mode: str, bars: int, energy: str, _genre: str = "") -> List[Note]:
    notes: List[Note] = []
    scale = SCALES.get(mode, SCALES["major"])
    beat = 0.0
    beats = bars * 4
    while beat < beats:
        phrase_len = random.choice([4, 8])
        phrase_type = random.choice([MusicPhrase.ASCENDING, MusicPhrase.DESCENDING, MusicPhrase.ARCH])
        for note in create_directional_phrase(root, scale, phrase_type, phrase_len):
            if beat + note.start_time < beats:
                note.start_time += beat
                notes.append(note)
        beat += phrase_len
    return notes


def _rhythmic(root: int, mode: str, bars: int, energy: str, _genre: str = "") -> List[Note]:
    notes: List[Note] = []
    scale = SCALES.get(mode, SCALES["major"])
    beats = bars * 4
    patterns = [[0.5, 0.5, 1.0], [1.0, 1.0, 2.0], [0.25, 0.25, 0.25, 0.25]]
    beat = 0.0
    pidx = 0
    while beat < beats:
        for dur in patterns[pidx % len(patterns)]:
            if beat < beats:
                pitch = root + random.choice(scale) + random.choice([-12, 0, 12])
                notes.append(Note(pitch=pitch, start_time=beat, duration=dur, velocity=random.randint(65, 100)))
                beat += dur
        pidx += 1
    return notes


def _chaotic(root: int, mode: str, bars: int, energy: str, _genre: str = "") -> List[Note]:
    notes: List[Note] = []
    scale = SCALES.get(mode, SCALES["major"])
    beat = 0.0
    beats = bars * 4
    while beat < beats:
        pitch = root + random.choice(scale) + random.choice([-24, -12, 0, 12, 24])
        dur = random.choice([0.125, 0.25, 0.5, 2.0, 3.0])
        notes.append(Note(pitch=pitch, start_time=beat, duration=dur, velocity=random.randint(30, 110)))
        beat += dur
    return notes


def _structured(root: int, mode: str, bars: int, energy: str, _genre: str = "") -> List[Note]:
    notes: List[Note] = []
    scale = SCALES.get(mode, SCALES["major"])
    beats = bars * 4
    phrase_length = 8
    beat = 0.0
    while beat < beats:
        ascending = int(beat / phrase_length) % 2 == 0
        rng = range(8) if ascending else range(7, -1, -1)
        for i in rng:
            if beat < beats:
                pitch = root + scale[i % len(scale)]
                notes.append(Note(pitch=pitch, start_time=beat, duration=1.0, velocity=75))
                beat += 1.0
    return notes


def _organic(root: int, mode: str, bars: int, energy: str, _genre: str = "") -> List[Note]:
    notes: List[Note] = []
    scale = SCALES.get(mode, SCALES["major"])
    beats = bars * 4
    beat = 0.0
    last_pitch = root
    while beat < beats:
        cur_idx = (last_pitch - root) % len(scale)
        nearby = [scale[(cur_idx + d) % len(scale)] for d in range(-2, 3)]
        pitch = root + random.choice(nearby) + random.choice([-12, 0, 12]) * random.choice([0, 1])
        if energy == "low":
            dur = random.choice([1.0, 1.5, 2.0])
        elif energy == "high":
            dur = random.choice([0.25, 0.5, 0.75])
        else:
            dur = random.choice([0.5, 1.0, 1.5])
        notes.append(Note(pitch=pitch, start_time=beat, duration=dur, velocity=random.randint(60, 90)))
        last_pitch = pitch
        beat += dur
    return notes
