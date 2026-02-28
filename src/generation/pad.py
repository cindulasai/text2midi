# -*- coding: utf-8 -*-
"""
Pad, chord, arpeggio, and FX generation strategies.
"""

from __future__ import annotations

import math
import random
from typing import List

from src.app.models import Note
from src.app.constants import SCALES, CHORD_PROGRESSIONS


# ---------------------------------------------------------------------------
# Pad (smart — replaces AdvancedMusicGenerator.generate_smart_pad)
# ---------------------------------------------------------------------------

def generate_pad(
    root: int,
    mode: str,
    bars: int,
    style_descriptors: List[str] | None = None,
    emotions: List[str] | None = None,
) -> List[Note]:
    """Emotion-aware pad generation."""
    style_descriptors = style_descriptors or []
    emotions = emotions or []
    notes: List[Note] = []
    scale = SCALES.get(mode, SCALES["major"])
    total_beats = bars * 4

    if "minimal" in style_descriptors:
        notes.append(Note(pitch=root, start_time=0, duration=total_beats - 0.5, velocity=35, channel=3))

    elif "dark" in emotions or "melancholic" in emotions:
        for deg in [0, 3, 7]:
            pitch = root + scale[deg % len(scale)] - 12
            notes.append(Note(pitch=pitch, start_time=0, duration=total_beats - 0.5,
                              velocity=random.randint(30, 50), channel=3))

    elif "bright" in emotions or "happy" in emotions:
        for deg in [0, 2, 4, 7]:
            pitch = root + scale[deg % len(scale)]
            notes.append(Note(pitch=pitch, start_time=0, duration=total_beats - 0.5,
                              velocity=random.randint(40, 60), channel=3))

    else:
        # Evolving chord blocks
        bars_per_block = max(4, bars // max(2, bars // 8))
        block_beats = bars_per_block * 4
        num_blocks = max(2, math.ceil(total_beats / block_beats))
        chord_rot = [[0, 2, 4], [2, 4, 6], [4, 6, 8], [0, 2, 4]]
        for bi in range(num_blocks):
            start = bi * block_beats
            if start >= total_beats:
                break
            dur = min(block_beats - 0.5, total_beats - start - 0.5)
            for deg in chord_rot[bi % len(chord_rot)]:
                pitch = root + scale[deg % len(scale)] - 12
                notes.append(Note(pitch=max(0, min(127, pitch)), start_time=start,
                                  duration=dur, velocity=random.randint(38, 58), channel=3))
    return notes


# ---------------------------------------------------------------------------
# Pad basic (replaces MusicGenerator.generate_pad)
# ---------------------------------------------------------------------------

def generate_pad_basic(root: int, mode: str, bars: int) -> List[Note]:
    notes: List[Note] = []
    scale = SCALES.get(mode, SCALES["major"])
    total_beats = bars * 4
    beat = 0.0
    while beat < total_beats:
        dur = random.choice([4.0, 8.0])
        for deg in [0, 2, 4]:
            if deg < len(scale):
                pitch = root + scale[deg] - 12
                notes.append(Note(pitch=pitch, start_time=beat, duration=dur - 0.5,
                                  velocity=random.randint(40, 60), channel=3))
        beat += dur
    return notes


# ---------------------------------------------------------------------------
# Chords (replaces MusicGenerator.generate_chords)
# ---------------------------------------------------------------------------

def generate_chords(root: int, genre: str, bars: int) -> List[Note]:
    notes: List[Note] = []
    progression = CHORD_PROGRESSIONS.get(genre, CHORD_PROGRESSIONS["pop"])
    bpc = 4
    beat = 0.0
    cidx = 0
    while beat < bars * 4:
        chord = progression[cidx % len(progression)]
        for interval in chord:
            pitch = root + interval - 12
            notes.append(Note(pitch=pitch, start_time=beat, duration=bpc - 0.5,
                              velocity=70, channel=1))
        beat += bpc
        cidx += 1
    return notes


# ---------------------------------------------------------------------------
# Arpeggio (replaces MusicGenerator.generate_arpeggio)
# ---------------------------------------------------------------------------

def generate_arpeggio(root: int, genre: str, bars: int, energy: str) -> List[Note]:
    notes: List[Note] = []
    progression = CHORD_PROGRESSIONS.get(genre, CHORD_PROGRESSIONS["pop"])
    bpc = 4
    arp_speed = {"low": 1.0, "medium": 0.5, "high": 0.25}.get(energy, 0.5)

    beat = 0.0
    cidx = 0
    while beat < bars * 4:
        chord = progression[cidx % len(progression)]
        cb = beat
        while cb < beat + bpc:
            for i, interval in enumerate(chord):
                if cb + i * arp_speed < beat + bpc:
                    notes.append(Note(pitch=root + interval, start_time=cb + i * arp_speed,
                                      duration=arp_speed * 0.8, velocity=random.randint(60, 80), channel=2))
            cb += len(chord) * arp_speed
        beat += bpc
        cidx += 1
    return notes


# ---------------------------------------------------------------------------
# FX / texture (replaces MusicGenerator.generate_fx)
# ---------------------------------------------------------------------------

def generate_fx(root: int, bars: int) -> List[Note]:
    notes: List[Note] = []
    total_beats = bars * 4
    beat = 0.0
    while beat < total_beats:
        if random.random() < 0.15:
            pitch = root + random.choice([0, 7, 12, 19, 24])
            dur = random.choice([2.0, 4.0, 8.0])
            notes.append(Note(pitch=pitch, start_time=beat, duration=dur,
                              velocity=random.randint(30, 50), channel=4))
        beat += random.choice([2.0, 4.0])
    return notes
