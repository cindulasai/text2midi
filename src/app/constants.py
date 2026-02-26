# -*- coding: utf-8 -*-
"""
Music Theory Constants
Scales, instruments, genres, and chord progressions.
"""

# Scales
SCALES = {
    "major": [0, 2, 4, 5, 7, 9, 11],
    "minor": [0, 2, 3, 5, 7, 8, 10],
    "dorian": [0, 2, 3, 5, 7, 9, 10],
    "mixolydian": [0, 2, 4, 5, 7, 9, 10],
    "pentatonic_major": [0, 2, 4, 7, 9],
    "pentatonic_minor": [0, 3, 5, 7, 10],
    "blues": [0, 3, 5, 6, 7, 10],
    "harmonic_minor": [0, 2, 3, 5, 7, 8, 11],
}

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

# General MIDI Instruments
GM_INSTRUMENTS = {
    "piano": 0, "bright_piano": 1, "electric_grand": 2,
    "electric_piano": 4, "rhodes": 4, "harpsichord": 6,
    "clavinet": 7, "celesta": 8, "glockenspiel": 9,
    "music_box": 10, "vibraphone": 11, "marimba": 12,
    "xylophone": 13, "tubular_bells": 14,
    "organ": 19, "church_organ": 19, "rock_organ": 18,
    "guitar": 24, "acoustic_guitar": 25, "electric_guitar": 27,
    "clean_guitar": 27, "distortion_guitar": 30,
    "bass": 32, "electric_bass": 33, "finger_bass": 33,
    "pick_bass": 34, "fretless_bass": 35, "slap_bass": 36,
    "synth_bass": 38, "synth_bass_2": 39,
    "violin": 40, "viola": 41, "cello": 42, "contrabass": 43,
    "strings": 48, "synth_strings": 50, "slow_strings": 49,
    "choir": 52, "voice_oohs": 53, "synth_voice": 54,
    "trumpet": 56, "trombone": 57, "tuba": 58, "brass": 61,
    "saxophone": 64, "alto_sax": 65, "tenor_sax": 66,
    "clarinet": 71, "oboe": 68, "bassoon": 70,
    "flute": 73, "recorder": 74, "pan_flute": 75,
    "synth_lead": 80, "square_lead": 80, "sawtooth": 81,
    "synth_pad": 88, "warm_pad": 89, "polysynth": 90,
    "space_voice": 91, "bowed_pad": 92, "metallic_pad": 93,
    "halo_pad": 94, "sweep_pad": 95,
    "fx_rain": 96, "fx_soundtrack": 97, "fx_crystal": 98,
    "fx_atmosphere": 99, "fx_brightness": 100,
    "sitar": 104, "banjo": 105, "shamisen": 106, "koto": 107,
    "kalimba": 108, "bagpipe": 109, "fiddle": 110,
}

# Genre configurations
GENRE_CONFIG = {
    "pop": {"tempo_range": (100, 130), "key": "C", "mode": "major", "energy": "medium", "typical_tracks": 4},
    "rock": {"tempo_range": (110, 140), "key": "E", "mode": "minor", "energy": "high", "typical_tracks": 5},
    "electronic": {"tempo_range": (120, 135), "key": "A", "mode": "minor", "energy": "high", "typical_tracks": 6},
    "lofi": {"tempo_range": (70, 90), "key": "D", "mode": "minor", "energy": "low", "typical_tracks": 4},
    "jazz": {"tempo_range": (80, 140), "key": "F", "mode": "dorian", "energy": "medium", "typical_tracks": 5},
    "classical": {"tempo_range": (60, 120), "key": "G", "mode": "major", "energy": "medium", "typical_tracks": 4},
    "ambient": {"tempo_range": (60, 80), "key": "C", "mode": "major", "energy": "low", "typical_tracks": 3},
    "cinematic": {"tempo_range": (70, 100), "key": "D", "mode": "minor", "energy": "high", "typical_tracks": 7},
    "funk": {"tempo_range": (95, 115), "key": "E", "mode": "mixolydian", "energy": "high", "typical_tracks": 5},
    "rnb": {"tempo_range": (70, 100), "key": "Ab", "mode": "minor", "energy": "medium", "typical_tracks": 5},
}

# Chord progressions by genre
CHORD_PROGRESSIONS = {
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
}
