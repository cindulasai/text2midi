# -*- coding: utf-8 -*-
"""
Music Theory Constants
Scales, instruments, genres, and chord progressions.

NOTE: The genre_registry (src.config.genre_registry) is now the single source
of truth.  This file keeps backward-compatible aliases so that existing code
(generators, MIDI builder) continues to work without changes.
"""

from src.config.genre_registry import (
    SCALES_EXTENDED,
    GM_INSTRUMENTS_EXTENDED,
    GENRE_TREE,
    get_genre,
)

# Scales — now pulled from the registry (30 scales)
SCALES = SCALES_EXTENDED

# Note to MIDI mapping
NOTE_TO_MIDI = {
    "C": 60, "C#": 61, "Db": 61,
    "D": 62, "D#": 63, "Eb": 63,
    "E": 64, "F": 65, "F#": 66, "Gb": 66,
    "G": 67, "G#": 68, "Ab": 68,
    "A": 69, "A#": 70, "Bb": 70, "B": 71,
}

# Drum mapping
DRUM_MAP = {
    "kick": 36, "bass_drum": 35, "snare": 38,
    "closed_hihat": 42, "open_hihat": 46,
    "crash": 49, "ride": 51,
    "tom_low": 45, "tom_mid": 47, "tom_high": 50,
    "clap": 39, "rimshot": 37, "shaker": 70,
}

# General MIDI Instruments — now pulled from the registry (130+ instruments)
GM_INSTRUMENTS = GM_INSTRUMENTS_EXTENDED

# Genre configurations — dynamically built from registry for all genres.
# Each entry: {"tempo_range": (lo,hi), "key": str, "mode": str, "energy": str, "typical_tracks": int}
def _build_genre_config():
    config = {}
    for gid, node in GENRE_TREE.items():
        config[gid] = {
            "tempo_range": node.tempo_range,
            "key": node.default_key,
            "mode": node.default_scale,
            "energy": node.energy,
            "typical_tracks": node.typical_tracks,
        }
    return config

GENRE_CONFIG = _build_genre_config()

# Chord progressions by genre
# Kept as original hand-tuned interval arrays; sub-genres inherit from root.
_CHORD_PROGRESSIONS_BASE = {
    "pop": [[0, 4, 7], [5, 9, 12], [7, 11, 14], [5, 9, 12]],
    "rock": [[0, 4, 7], [7, 11, 14], [5, 9, 12], [0, 4, 7]],
    "jazz": [[0, 4, 7, 11], [5, 9, 12, 16], [2, 5, 9, 12], [7, 11, 14, 17]],
    "lofi": [[0, 4, 7, 11], [2, 5, 9], [5, 9, 12], [7, 11, 14]],
    "electronic": [[0, 4, 7], [0, 4, 7], [5, 9, 12], [7, 11, 14]],
    "classical": [[0, 4, 7], [5, 9, 12], [4, 7, 11], [0, 4, 7]],
    "ambient": [[0, 4, 7, 11], [0, 4, 7, 11], [5, 9, 12, 16], [5, 9, 12, 16]],
    "cinematic": [[0, 3, 7], [5, 8, 12], [7, 10, 14], [3, 7, 10]],
    "funk": [[0, 4, 7, 10], [5, 9, 12], [0, 4, 7, 10], [7, 11, 14]],
    "rnb": [[0, 4, 7, 11], [2, 5, 9, 12], [5, 9, 12, 16], [7, 11, 14, 17]],
    # New root genres
    "hiphop": [[0, 3, 7], [5, 8, 12], [7, 10, 14], [0, 3, 7]],
    "metal": [[0, 7], [5, 12], [3, 10], [0, 7]],  # power chords
    "blues": [[0, 4, 7, 10], [5, 9, 12, 15], [0, 4, 7, 10], [7, 11, 14]],
    "folk": [[0, 4, 7], [5, 9, 12], [0, 4, 7], [7, 11, 14]],
    "latin": [[0, 4, 7], [5, 9, 12], [7, 11, 14], [0, 4, 7]],
    "african": [[0, 4, 7], [5, 9, 12], [7, 11, 14], [0, 4, 7]],
    "asian": [[0, 4, 7], [0, 4, 7], [5, 9, 12], [0, 4, 7]],
}


def _resolve_chord_progression(genre_id: str):
    """Get chord progression for a genre — falls back to root then pop."""
    if genre_id in _CHORD_PROGRESSIONS_BASE:
        return _CHORD_PROGRESSIONS_BASE[genre_id]
    root = genre_id.split(".")[0]
    if root in _CHORD_PROGRESSIONS_BASE:
        return _CHORD_PROGRESSIONS_BASE[root]
    return _CHORD_PROGRESSIONS_BASE["pop"]


# Build full CHORD_PROGRESSIONS dict for all registered genres
CHORD_PROGRESSIONS = {
    gid: _resolve_chord_progression(gid)
    for gid in GENRE_TREE
}
# Also keep the original 10 keys guaranteed:
CHORD_PROGRESSIONS.update(_CHORD_PROGRESSIONS_BASE)
