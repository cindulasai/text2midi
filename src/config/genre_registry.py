# -*- coding: utf-8 -*-
"""
Genre Registry — Single Source of Truth for all genre, scale, and instrument data.

Every other module (schema.py, constants.py, engine.py, genre_validator.py,
prompt_templates.py, sidebar.py) imports from HERE instead of maintaining
their own hardcoded copies.

Design:
  - GenreNode dataclass holds every parameter a genre needs.
  - GENRE_TREE is a flat dict keyed by dot-notation ID (e.g. "electronic.house").
  - Root genres are also registered at their short key (e.g. "electronic").
  - Helper functions provide traversal, alias lookup, and validation lists.
  - SCALES_EXTENDED expands the original 8 scales to 30.
  - GM_INSTRUMENTS_EXTENDED merges original + world-music instruments.
  - Full backward compatibility: the original 10 genre IDs still work.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


# =====================================================================
# GenreNode dataclass
# =====================================================================

@dataclass(frozen=True)
class GenreNode:
    """Immutable definition of a single genre or sub-genre."""

    id: str  # dot-notation, e.g. "electronic.house.deep_house"
    name: str  # human-readable, e.g. "Deep House"
    parent: Optional[str] = None  # parent ID, e.g. "electronic.house"
    aliases: Tuple[str, ...] = ()  # alternative names for intent matching

    # Musical parameters
    tempo_range: Tuple[int, int] = (100, 130)
    default_key: str = "C"
    default_scale: str = "major"
    energy: str = "medium"  # very_low | low | medium | high | very_high
    typical_tracks: int = 4
    chord_feel: str = "triads"  # triads | 7ths | extended | power | modal | open

    # Instruments: list of (instrument_name, role, priority)
    instruments: Tuple[Tuple[str, str, int], ...] = ()

    # Validation constraints (for genre_validator)
    note_density: Tuple[int, int] = (15, 40)  # notes per bar
    rhythm_regularity: Tuple[float, float] = (0.5, 0.9)
    dissonance_tolerance: Tuple[float, float] = (0.1, 0.5)

    @property
    def root(self) -> str:
        """Return the root genre ID (first segment)."""
        return self.id.split(".")[0]

    @property
    def depth(self) -> int:
        """Return hierarchy depth (0 = root, 1 = sub, 2 = variant)."""
        return self.id.count(".")


# =====================================================================
# SCALES_EXTENDED — 30 scales (8 original + 22 new)
# =====================================================================

SCALES_EXTENDED: Dict[str, List[int]] = {
    # ---- Original 8 ----
    "major": [0, 2, 4, 5, 7, 9, 11],
    "minor": [0, 2, 3, 5, 7, 8, 10],
    "dorian": [0, 2, 3, 5, 7, 9, 10],
    "mixolydian": [0, 2, 4, 5, 7, 9, 10],
    "pentatonic_major": [0, 2, 4, 7, 9],
    "pentatonic_minor": [0, 3, 5, 7, 10],
    "blues": [0, 3, 5, 6, 7, 10],
    "harmonic_minor": [0, 2, 3, 5, 7, 8, 11],

    # ---- New: Western modes ----
    "phrygian": [0, 1, 3, 5, 7, 8, 10],
    "lydian": [0, 2, 4, 6, 7, 9, 11],
    "locrian": [0, 1, 3, 5, 6, 8, 10],
    "melodic_minor": [0, 2, 3, 5, 7, 9, 11],

    # ---- New: Dominant / altered ----
    "phrygian_dominant": [0, 1, 4, 5, 7, 8, 10],
    "lydian_dominant": [0, 2, 4, 6, 7, 9, 10],
    "whole_tone": [0, 2, 4, 6, 8, 10],
    "diminished_whole_half": [0, 2, 3, 5, 6, 8, 9, 11],
    "diminished_half_whole": [0, 1, 3, 4, 6, 7, 9, 10],
    "chromatic": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],

    # ---- New: World / cultural ----
    "hungarian_minor": [0, 2, 3, 6, 7, 8, 11],
    "double_harmonic": [0, 1, 4, 5, 7, 8, 11],  # aka Byzantine / Arabic
    "hijaz": [0, 1, 4, 5, 7, 8, 10],
    "maqam_bayati": [0, 2, 3, 5, 7, 8, 10],  # quarter-tone approximated to nearest semitone
    "raga_bhairav": [0, 1, 4, 5, 7, 8, 11],
    "raga_yaman": [0, 2, 4, 6, 7, 9, 11],  # same as Lydian
    "japanese_in": [0, 1, 5, 7, 8],
    "japanese_yo": [0, 2, 5, 7, 9],
    "chinese_pentatonic": [0, 2, 4, 7, 9],
    "balinese_pelog": [0, 1, 3, 7, 8],
    "ethiopian_tizita": [0, 2, 4, 7, 9],  # major pentatonic variant
    "klezmer_freygish": [0, 1, 4, 5, 7, 8, 10],  # Phrygian dominant
}

# Scale aliases for intent matching (maps alias → canonical scale name)
SCALE_ALIASES: Dict[str, str] = {
    "natural_minor": "minor",
    "aeolian": "minor",
    "ionian": "major",
    "arabic": "double_harmonic",
    "byzantine": "double_harmonic",
    "spanish": "phrygian_dominant",
    "flamenco": "phrygian_dominant",
    "gypsy": "hungarian_minor",
    "romani": "hungarian_minor",
    "japanese": "japanese_in",
    "egyptian": "phrygian",
    "chinese": "chinese_pentatonic",
    "indian": "raga_bhairav",
    "persian": "double_harmonic",
    "freygish": "klezmer_freygish",
}


# =====================================================================
# GM_INSTRUMENTS_EXTENDED — merges original + world instruments
# =====================================================================

GM_INSTRUMENTS_EXTENDED: Dict[str, int] = {
    # ---- Original from constants.py ----
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

    # ---- World / Cultural string instruments ----
    "oud": 25, "pipa": 25, "erhu": 40, "guzheng": 107,
    "gayageum": 107, "tar": 25, "santur": 15, "bouzouki": 25,
    "balalaika": 25, "ukulele": 25, "mandolin": 25,
    "charango": 25, "tres": 25, "vihuela": 25,
    "nyckelharpa": 110, "hardingfele": 110, "morin_khuur": 110,
    "kora": 46, "harp": 46,

    # ---- World / Cultural wind instruments ----
    "ney": 75, "shakuhachi": 77, "dizi": 73, "daegeum": 73,
    "bansuri": 73, "duduk": 68, "tin_whistle": 74,
    "zurna": 68, "suona": 68, "didgeridoo": 58,
    "harmonica": 22, "accordion": 21, "harmonium": 20,
    "bandoneon": 21, "melodica": 22, "sheng": 20,

    # ---- Pitched percussion ----
    "steel_drum": 114, "hang_drum": 12, "tongue_drum": 12,
    "mbira": 108, "balafon": 12, "angklung": 14,

    # ---- Synth aliases ----
    "supersaw": 81, "pluck": 80, "wobble_bass": 87,
    "808_bass": 38, "sub_bass": 38, "acid_bass": 87,
    "reese_bass": 39, "fm_bass": 38,
    "pad_strings": 48, "pad_choir": 52, "pad_atmosphere": 99,

    # ---- Additional useful mappings ----
    "french_horn": 60, "timpani": 47, "bells": 14,
    "steel_guitar": 25, "percussion": 47,
}


# =====================================================================
# GENRE_TREE — Complete genre registry
# =====================================================================

def _g(
    id: str,
    name: str,
    *,
    parent: Optional[str] = None,
    aliases: Tuple[str, ...] = (),
    tempo: Tuple[int, int] = (100, 130),
    key: str = "C",
    scale: str = "major",
    energy: str = "medium",
    tracks: int = 4,
    chord_feel: str = "triads",
    instruments: Tuple[Tuple[str, str, int], ...] = (),
    density: Tuple[int, int] = (15, 40),
    regularity: Tuple[float, float] = (0.5, 0.9),
    dissonance: Tuple[float, float] = (0.1, 0.5),
) -> GenreNode:
    """Shorthand factory for GenreNode."""
    return GenreNode(
        id=id, name=name, parent=parent, aliases=aliases,
        tempo_range=tempo, default_key=key, default_scale=scale,
        energy=energy, typical_tracks=tracks, chord_feel=chord_feel,
        instruments=instruments,
        note_density=density, rhythm_regularity=regularity,
        dissonance_tolerance=dissonance,
    )


def _build_genre_tree() -> Dict[str, GenreNode]:
    """Build the complete genre tree. Called once at module load."""
    nodes: list[GenreNode] = []

    # =================================================================
    # POP
    # =================================================================
    nodes.append(_g("pop", "Pop",
        aliases=("pop music", "popular"),
        tempo=(100, 130), key="C", scale="major", energy="medium", tracks=4,
        chord_feel="triads",
        instruments=(("piano", "harmony", 7), ("electric_guitar", "melody", 8), ("electric_bass", "bass", 8), ("drums", "rhythm", 9)),
        density=(20, 40), regularity=(0.75, 0.95), dissonance=(0.1, 0.4),
    ))
    nodes.append(_g("pop.synth_pop", "Synth Pop", parent="pop",
        aliases=("synthpop", "synth-pop", "80s pop"),
        tempo=(110, 130), key="C", scale="major", energy="medium", tracks=5,
        chord_feel="triads",
        instruments=(("synth_lead", "lead", 9), ("synth_pad", "pad", 7), ("synth_bass", "bass", 8), ("drums", "rhythm", 9), ("electric_guitar", "melody", 5)),
    ))
    nodes.append(_g("pop.kpop", "K-Pop", parent="pop",
        aliases=("k-pop", "korean pop"),
        tempo=(110, 135), key="C", scale="minor", energy="high", tracks=6,
        chord_feel="triads",
        instruments=(("synth_lead", "lead", 9), ("piano", "harmony", 7), ("synth_bass", "bass", 8), ("drums", "rhythm", 9), ("strings", "pad", 6), ("synth_pad", "pad", 5)),
    ))
    nodes.append(_g("pop.jpop", "J-Pop", parent="pop",
        aliases=("j-pop", "japanese pop"),
        tempo=(120, 145), key="C", scale="major", energy="high", tracks=5,
        chord_feel="triads",
        instruments=(("piano", "melody", 8), ("synth_lead", "lead", 7), ("electric_bass", "bass", 8), ("drums", "rhythm", 9), ("strings", "harmony", 6)),
    ))
    nodes.append(_g("pop.city_pop", "City Pop", parent="pop",
        aliases=("japanese city pop", "80s japanese"),
        tempo=(100, 120), key="F", scale="major", energy="medium", tracks=5,
        chord_feel="7ths",
        instruments=(("electric_piano", "harmony", 8), ("electric_guitar", "melody", 7), ("synth_bass", "bass", 7), ("drums", "rhythm", 8), ("saxophone", "lead", 6)),
    ))
    nodes.append(_g("pop.dream_pop", "Dream Pop", parent="pop",
        aliases=("dreampop",),
        tempo=(90, 115), key="D", scale="major", energy="low", tracks=5,
        chord_feel="triads",
        instruments=(("voice_oohs", "melody", 8), ("synth_pad", "pad", 8), ("electric_bass", "bass", 7), ("drums", "rhythm", 6), ("electric_guitar", "harmony", 7)),
    ))
    nodes.append(_g("pop.tropical", "Tropical Pop", parent="pop",
        aliases=("tropical house pop",),
        tempo=(100, 115), key="C", scale="major", energy="medium", tracks=5,
        instruments=(("marimba", "melody", 8), ("acoustic_guitar", "harmony", 7), ("synth_bass", "bass", 7), ("drums", "rhythm", 8), ("synth_pad", "pad", 5)),
    ))

    # =================================================================
    # ROCK
    # =================================================================
    nodes.append(_g("rock", "Rock",
        aliases=("rock music",),
        tempo=(110, 140), key="E", scale="minor", energy="high", tracks=5,
        chord_feel="power",
        instruments=(("electric_guitar", "lead", 9), ("electric_guitar", "harmony", 7), ("electric_bass", "bass", 8), ("drums", "rhythm", 9), ("organ", "harmony", 5)),
        density=(20, 45), regularity=(0.7, 0.9), dissonance=(0.3, 0.7),
    ))
    nodes.append(_g("rock.classic", "Classic Rock", parent="rock",
        aliases=("classic rock", "70s rock"),
        tempo=(110, 140), key="E", scale="minor", energy="high", tracks=5,
        instruments=(("electric_guitar", "lead", 9), ("piano", "harmony", 7), ("electric_bass", "bass", 8), ("drums", "rhythm", 9), ("organ", "harmony", 5)),
    ))
    nodes.append(_g("rock.progressive", "Progressive Rock", parent="rock",
        aliases=("prog rock", "prog"),
        tempo=(80, 140), key="D", scale="minor", energy="medium", tracks=6,
        chord_feel="extended",
        instruments=(("synth_lead", "lead", 8), ("piano", "harmony", 7), ("electric_bass", "bass", 8), ("drums", "rhythm", 9), ("strings", "pad", 6), ("electric_guitar", "melody", 7)),
    ))
    nodes.append(_g("rock.psychedelic", "Psychedelic Rock", parent="rock",
        aliases=("psych rock", "psychedelia"),
        tempo=(90, 130), key="E", scale="mixolydian", energy="medium", tracks=5,
        instruments=(("electric_guitar", "lead", 9), ("sitar", "melody", 6), ("electric_bass", "bass", 7), ("drums", "rhythm", 8), ("synth_pad", "pad", 6)),
    ))
    nodes.append(_g("rock.grunge", "Grunge", parent="rock",
        aliases=("90s grunge", "seattle grunge"),
        tempo=(100, 135), key="E", scale="minor", energy="high", tracks=4,
        instruments=(("distortion_guitar", "lead", 9), ("electric_bass", "bass", 8), ("drums", "rhythm", 9), ("voice_oohs", "melody", 5)),
    ))
    nodes.append(_g("rock.punk", "Punk Rock", parent="rock",
        aliases=("punk",),
        tempo=(150, 200), key="A", scale="minor", energy="very_high", tracks=4,
        instruments=(("distortion_guitar", "lead", 9), ("electric_bass", "bass", 8), ("drums", "rhythm", 9), ("distortion_guitar", "harmony", 6)),
    ))
    nodes.append(_g("rock.shoegaze", "Shoegaze", parent="rock",
        aliases=(),
        tempo=(80, 120), key="D", scale="major", energy="medium", tracks=5,
        instruments=(("electric_guitar", "lead", 9), ("synth_pad", "pad", 8), ("electric_bass", "bass", 7), ("drums", "rhythm", 7), ("voice_oohs", "melody", 5)),
    ))
    nodes.append(_g("rock.post_rock", "Post-Rock", parent="rock",
        aliases=("post rock",),
        tempo=(80, 130), key="G", scale="minor", energy="medium", tracks=5,
        instruments=(("electric_guitar", "lead", 9), ("piano", "harmony", 6), ("electric_bass", "bass", 7), ("drums", "rhythm", 7), ("strings", "pad", 8)),
    ))
    nodes.append(_g("rock.surf", "Surf Rock", parent="rock",
        aliases=("surf",),
        tempo=(130, 160), key="E", scale="major", energy="high", tracks=4,
        instruments=(("electric_guitar", "lead", 9), ("organ", "harmony", 5), ("electric_bass", "bass", 8), ("drums", "rhythm", 8)),
    ))

    # =================================================================
    # METAL
    # =================================================================
    nodes.append(_g("metal", "Metal",
        aliases=("heavy metal", "metal music"),
        tempo=(100, 180), key="E", scale="minor", energy="very_high", tracks=5,
        chord_feel="power",
        instruments=(("distortion_guitar", "lead", 9), ("distortion_guitar", "harmony", 7), ("electric_bass", "bass", 8), ("drums", "rhythm", 9), ("synth_lead", "lead", 4)),
        density=(25, 50), regularity=(0.6, 0.9), dissonance=(0.4, 0.8),
    ))
    nodes.append(_g("metal.heavy", "Heavy Metal", parent="metal",
        tempo=(110, 160), key="E", scale="minor", energy="very_high", tracks=5,
        instruments=(("distortion_guitar", "lead", 9), ("distortion_guitar", "harmony", 7), ("electric_bass", "bass", 8), ("drums", "rhythm", 9), ("synth_lead", "lead", 4)),
    ))
    nodes.append(_g("metal.symphonic", "Symphonic Metal", parent="metal",
        aliases=("orchestral metal",),
        tempo=(100, 150), key="D", scale="minor", energy="very_high", tracks=7,
        instruments=(("distortion_guitar", "lead", 9), ("strings", "harmony", 8), ("electric_bass", "bass", 8), ("drums", "rhythm", 9), ("choir", "pad", 7), ("piano", "harmony", 5), ("synth_pad", "pad", 4)),
    ))
    nodes.append(_g("metal.doom", "Doom Metal", parent="metal",
        tempo=(50, 80), key="D", scale="minor", energy="high", tracks=4,
        instruments=(("distortion_guitar", "lead", 9), ("organ", "harmony", 6), ("electric_bass", "bass", 8), ("drums", "rhythm", 7)),
    ))
    nodes.append(_g("metal.power", "Power Metal", parent="metal",
        tempo=(130, 180), key="E", scale="minor", energy="very_high", tracks=6,
        instruments=(("distortion_guitar", "lead", 9), ("choir", "pad", 7), ("electric_bass", "bass", 8), ("drums", "rhythm", 9), ("strings", "harmony", 6), ("synth_lead", "melody", 5)),
    ))
    nodes.append(_g("metal.djent", "Djent", parent="metal",
        aliases=("progressive metal",),
        tempo=(100, 140), key="D", scale="minor", energy="high", tracks=5,
        instruments=(("distortion_guitar", "lead", 9), ("piano", "harmony", 5), ("electric_bass", "bass", 8), ("drums", "rhythm", 9), ("synth_pad", "pad", 5)),
    ))

    # =================================================================
    # ELECTRONIC
    # =================================================================
    nodes.append(_g("electronic", "Electronic",
        aliases=("edm", "electronic music", "electronic dance music"),
        tempo=(120, 135), key="A", scale="minor", energy="high", tracks=6,
        chord_feel="triads",
        instruments=(("synth_lead", "lead", 8), ("synth_pad", "pad", 7), ("synth_bass", "bass", 8), ("drums", "rhythm", 9), ("synth_lead", "melody", 5), ("fx_atmosphere", "fx", 4)),
        density=(20, 50), regularity=(0.6, 0.95), dissonance=(0.3, 0.7),
    ))
    nodes.append(_g("electronic.house", "House", parent="electronic",
        aliases=("house music",),
        tempo=(120, 130), key="C", scale="minor", energy="high", tracks=5,
        instruments=(("synth_lead", "lead", 8), ("piano", "harmony", 6), ("synth_bass", "bass", 8), ("drums", "rhythm", 9), ("synth_pad", "pad", 6)),
    ))
    nodes.append(_g("electronic.deep_house", "Deep House", parent="electronic",
        aliases=("deep house",),
        tempo=(118, 125), key="D", scale="minor", energy="medium", tracks=5,
        chord_feel="7ths",
        instruments=(("synth_lead", "lead", 7), ("electric_piano", "harmony", 7), ("synth_bass", "bass", 8), ("drums", "rhythm", 9), ("synth_pad", "pad", 7)),
    ))
    nodes.append(_g("electronic.techno", "Techno", parent="electronic",
        aliases=("berlin techno",),
        tempo=(125, 140), key="A", scale="minor", energy="high", tracks=5,
        instruments=(("synth_lead", "lead", 7), ("synth_bass", "bass", 8), ("drums", "rhythm", 9), ("synth_pad", "pad", 6), ("fx_atmosphere", "fx", 5)),
    ))
    nodes.append(_g("electronic.trance", "Trance", parent="electronic",
        aliases=("uplifting trance",),
        tempo=(130, 145), key="A", scale="minor", energy="high", tracks=6,
        instruments=(("synth_lead", "lead", 9), ("piano", "harmony", 6), ("synth_bass", "bass", 8), ("drums", "rhythm", 9), ("synth_pad", "pad", 7), ("strings", "harmony", 5)),
    ))
    nodes.append(_g("electronic.dubstep", "Dubstep", parent="electronic",
        aliases=("brostep",),
        tempo=(135, 145), key="F", scale="minor", energy="very_high", tracks=4,
        instruments=(("synth_lead", "lead", 8), ("wobble_bass", "bass", 9), ("drums", "rhythm", 9), ("synth_pad", "pad", 5)),
    ))
    nodes.append(_g("electronic.drum_and_bass", "Drum & Bass", parent="electronic",
        aliases=("drum and bass", "dnb", "d&b", "jungle"),
        tempo=(170, 180), key="D", scale="minor", energy="very_high", tracks=4,
        instruments=(("synth_lead", "lead", 7), ("synth_bass", "bass", 9), ("drums", "rhythm", 9), ("synth_pad", "pad", 5)),
    ))
    nodes.append(_g("electronic.synthwave", "Synthwave", parent="electronic",
        aliases=("synth wave", "retrowave", "outrun"),
        tempo=(100, 120), key="A", scale="minor", energy="medium", tracks=5,
        instruments=(("synth_lead", "lead", 9), ("electric_guitar", "melody", 5), ("synth_bass", "bass", 8), ("drums", "rhythm", 8), ("synth_pad", "pad", 7)),
    ))
    nodes.append(_g("electronic.vaporwave", "Vaporwave", parent="electronic",
        aliases=("vapor wave",),
        tempo=(80, 100), key="Eb", scale="major", energy="low", tracks=4,
        instruments=(("electric_piano", "melody", 8), ("synth_pad", "pad", 7), ("synth_bass", "bass", 6), ("drums", "rhythm", 5)),
    ))
    nodes.append(_g("electronic.future_bass", "Future Bass", parent="electronic",
        tempo=(130, 145), key="D", scale="major", energy="high", tracks=5,
        instruments=(("synth_lead", "lead", 9), ("piano", "harmony", 6), ("synth_bass", "bass", 8), ("drums", "rhythm", 9), ("voice_oohs", "pad", 5)),
    ))
    nodes.append(_g("electronic.downtempo", "Downtempo", parent="electronic",
        aliases=("chillout", "trip-hop"),
        tempo=(80, 110), key="D", scale="minor", energy="low", tracks=5,
        instruments=(("synth_pad", "pad", 8), ("acoustic_guitar", "melody", 6), ("synth_bass", "bass", 7), ("drums", "rhythm", 7), ("flute", "melody", 5)),
    ))
    nodes.append(_g("electronic.uk_garage", "UK Garage", parent="electronic",
        aliases=("2-step", "garage"),
        tempo=(128, 135), key="C", scale="minor", energy="medium", tracks=5,
        instruments=(("synth_lead", "lead", 7), ("synth_bass", "bass", 8), ("drums", "rhythm", 9), ("synth_pad", "pad", 6), ("voice_oohs", "melody", 5)),
    ))
    nodes.append(_g("electronic.idm", "IDM", parent="electronic",
        aliases=("intelligent dance music", "glitch"),
        tempo=(100, 150), key="C", scale="minor", energy="medium", tracks=5,
        instruments=(("synth_lead", "lead", 7), ("synth_pad", "pad", 7), ("synth_bass", "bass", 6), ("drums", "rhythm", 8), ("fx_atmosphere", "fx", 6)),
    ))

    # =================================================================
    # HIP-HOP
    # =================================================================
    nodes.append(_g("hiphop", "Hip-Hop",
        aliases=("hip-hop", "hip hop", "rap"),
        tempo=(80, 115), key="D", scale="minor", energy="medium", tracks=4,
        chord_feel="triads",
        instruments=(("piano", "harmony", 7), ("synth_bass", "bass", 8), ("drums", "rhythm", 9), ("synth_pad", "pad", 5)),
        density=(15, 35), regularity=(0.5, 0.8), dissonance=(0.2, 0.5),
    ))
    nodes.append(_g("hiphop.boom_bap", "Boom Bap", parent="hiphop",
        aliases=("boom-bap", "90s hip-hop"),
        tempo=(85, 100), key="D", scale="minor", energy="medium", tracks=4,
        instruments=(("piano", "harmony", 7), ("saxophone", "melody", 5), ("synth_bass", "bass", 8), ("drums", "rhythm", 9)),
    ))
    nodes.append(_g("hiphop.trap", "Trap", parent="hiphop",
        aliases=("trap music", "trap beat"),
        tempo=(130, 160), key="D", scale="minor", energy="high", tracks=4,
        instruments=(("synth_lead", "lead", 7), ("piano", "harmony", 5), ("808_bass", "bass", 9), ("drums", "rhythm", 9)),
    ))
    nodes.append(_g("hiphop.lofi_hiphop", "Lo-fi Hip-Hop", parent="hiphop",
        aliases=("lo-fi hip hop", "lofi beats", "chillhop"),
        tempo=(70, 90), key="D", scale="minor", energy="low", tracks=4,
        chord_feel="7ths",
        instruments=(("electric_piano", "melody", 8), ("acoustic_guitar", "harmony", 6), ("synth_bass", "bass", 7), ("drums", "rhythm", 8)),
    ))
    nodes.append(_g("hiphop.drill", "Drill", parent="hiphop",
        aliases=("uk drill", "chicago drill"),
        tempo=(135, 145), key="C", scale="minor", energy="high", tracks=4,
        instruments=(("piano", "melody", 7), ("808_bass", "bass", 9), ("drums", "rhythm", 9), ("strings", "pad", 5)),
    ))
    nodes.append(_g("hiphop.g_funk", "G-Funk", parent="hiphop",
        aliases=("g funk", "west coast"),
        tempo=(90, 105), key="C", scale="minor", energy="medium", tracks=5,
        instruments=(("synth_lead", "lead", 8), ("piano", "harmony", 6), ("synth_bass", "bass", 8), ("drums", "rhythm", 9), ("voice_oohs", "pad", 5)),
    ))
    nodes.append(_g("hiphop.phonk", "Phonk", parent="hiphop",
        aliases=("drift phonk",),
        tempo=(130, 145), key="D", scale="minor", energy="high", tracks=4,
        instruments=(("piano", "melody", 7), ("808_bass", "bass", 9), ("drums", "rhythm", 9), ("voice_oohs", "pad", 5)),
    ))

    # =================================================================
    # JAZZ
    # =================================================================
    nodes.append(_g("jazz", "Jazz",
        aliases=("jazz music",),
        tempo=(80, 140), key="F", scale="dorian", energy="medium", tracks=5,
        chord_feel="7ths",
        instruments=(("piano", "harmony", 8), ("fretless_bass", "bass", 8), ("drums", "rhythm", 8), ("saxophone", "melody", 9), ("trumpet", "lead", 6)),
        density=(25, 50), regularity=(0.3, 0.7), dissonance=(0.4, 0.8),
    ))
    nodes.append(_g("jazz.swing", "Swing", parent="jazz",
        aliases=("big band", "swing jazz"),
        tempo=(120, 160), key="Bb", scale="mixolydian", energy="high", tracks=5,
        instruments=(("trumpet", "lead", 9), ("piano", "harmony", 8), ("fretless_bass", "bass", 8), ("drums", "rhythm", 8), ("saxophone", "melody", 7)),
    ))
    nodes.append(_g("jazz.bebop", "Bebop", parent="jazz",
        aliases=("bop",),
        tempo=(140, 200), key="Bb", scale="dorian", energy="high", tracks=4,
        instruments=(("saxophone", "lead", 9), ("piano", "harmony", 8), ("fretless_bass", "bass", 8), ("drums", "rhythm", 8)),
    ))
    nodes.append(_g("jazz.cool", "Cool Jazz", parent="jazz",
        aliases=("west coast jazz",),
        tempo=(90, 130), key="C", scale="dorian", energy="low", tracks=5,
        instruments=(("trumpet", "lead", 8), ("piano", "harmony", 7), ("fretless_bass", "bass", 8), ("drums", "rhythm", 7), ("flute", "melody", 6)),
    ))
    nodes.append(_g("jazz.modal", "Modal Jazz", parent="jazz",
        aliases=("modal",),
        tempo=(90, 140), key="D", scale="dorian", energy="medium", tracks=4,
        instruments=(("saxophone", "lead", 9), ("piano", "harmony", 7), ("fretless_bass", "bass", 8), ("drums", "rhythm", 7)),
    ))
    nodes.append(_g("jazz.fusion", "Jazz Fusion", parent="jazz",
        aliases=("fusion",),
        tempo=(100, 150), key="A", scale="dorian", energy="high", tracks=5,
        instruments=(("electric_guitar", "lead", 8), ("electric_piano", "harmony", 7), ("electric_bass", "bass", 8), ("drums", "rhythm", 9), ("saxophone", "melody", 6)),
    ))
    nodes.append(_g("jazz.smooth", "Smooth Jazz", parent="jazz",
        aliases=("smooth",),
        tempo=(80, 110), key="Eb", scale="dorian", energy="low", tracks=5,
        instruments=(("saxophone", "lead", 9), ("electric_piano", "harmony", 8), ("electric_bass", "bass", 7), ("drums", "rhythm", 7), ("synth_pad", "pad", 5)),
    ))
    nodes.append(_g("jazz.gypsy", "Gypsy Jazz", parent="jazz",
        aliases=("gypsy jazz", "manouche", "django"),
        tempo=(130, 180), key="D", scale="minor", energy="high", tracks=4,
        instruments=(("acoustic_guitar", "lead", 9), ("violin", "melody", 7), ("fretless_bass", "bass", 8), ("acoustic_guitar", "harmony", 7)),
    ))
    nodes.append(_g("jazz.bossa_nova", "Bossa Nova", parent="jazz",
        aliases=("bossa nova", "bossa"),
        tempo=(105, 120), key="C", scale="major", energy="low", tracks=4,
        instruments=(("acoustic_guitar", "lead", 9), ("piano", "harmony", 7), ("fretless_bass", "bass", 7), ("drums", "rhythm", 7)),
    ))
    nodes.append(_g("jazz.ethio", "Ethio-Jazz", parent="jazz",
        aliases=("ethiopian jazz",),
        tempo=(90, 130), key="D", scale="minor", energy="medium", tracks=5,
        instruments=(("saxophone", "lead", 8), ("organ", "harmony", 7), ("electric_bass", "bass", 8), ("drums", "rhythm", 8), ("electric_guitar", "melody", 5)),
    ))
    nodes.append(_g("jazz.latin", "Latin Jazz", parent="jazz",
        aliases=("latin jazz", "afro-cuban jazz"),
        tempo=(100, 140), key="D", scale="dorian", energy="high", tracks=5,
        instruments=(("trumpet", "lead", 8), ("piano", "harmony", 8), ("fretless_bass", "bass", 8), ("drums", "rhythm", 9), ("saxophone", "melody", 6)),
    ))

    # =================================================================
    # BLUES
    # =================================================================
    nodes.append(_g("blues", "Blues",
        aliases=("blues music",),
        tempo=(60, 120), key="E", scale="blues", energy="medium", tracks=4,
        chord_feel="7ths",
        instruments=(("electric_guitar", "lead", 9), ("piano", "harmony", 7), ("electric_bass", "bass", 8), ("drums", "rhythm", 8)),
        density=(15, 35), regularity=(0.5, 0.8), dissonance=(0.3, 0.6),
    ))
    nodes.append(_g("blues.delta", "Delta Blues", parent="blues",
        aliases=("delta",),
        tempo=(60, 90), key="E", scale="blues", energy="low", tracks=2,
        instruments=(("acoustic_guitar", "lead", 9), ("harmonica", "melody", 7)),
    ))
    nodes.append(_g("blues.chicago", "Chicago Blues", parent="blues",
        aliases=("electric blues",),
        tempo=(80, 120), key="E", scale="blues", energy="medium", tracks=5,
        instruments=(("electric_guitar", "lead", 9), ("piano", "harmony", 7), ("electric_bass", "bass", 8), ("drums", "rhythm", 8), ("harmonica", "melody", 6)),
    ))
    nodes.append(_g("blues.soul", "Soul", parent="blues",
        aliases=("soul music",),
        tempo=(70, 110), key="Ab", scale="minor", energy="medium", tracks=5,
        instruments=(("voice_oohs", "melody", 9), ("organ", "harmony", 7), ("electric_bass", "bass", 8), ("drums", "rhythm", 8), ("strings", "pad", 6)),
    ))
    nodes.append(_g("blues.motown", "Motown", parent="blues",
        aliases=("motown sound",),
        tempo=(100, 130), key="Ab", scale="major", energy="medium", tracks=5,
        instruments=(("voice_oohs", "melody", 9), ("piano", "harmony", 7), ("electric_bass", "bass", 8), ("drums", "rhythm", 8), ("strings", "pad", 6)),
    ))
    nodes.append(_g("blues.neo_soul", "Neo-Soul", parent="blues",
        aliases=("neo soul",),
        tempo=(70, 100), key="D", scale="minor", energy="low", tracks=5,
        chord_feel="7ths",
        instruments=(("voice_oohs", "melody", 8), ("electric_piano", "harmony", 8), ("synth_bass", "bass", 7), ("drums", "rhythm", 7), ("synth_pad", "pad", 5)),
    ))
    nodes.append(_g("blues.gospel", "Gospel", parent="blues",
        aliases=("gospel music",),
        tempo=(80, 130), key="C", scale="major", energy="high", tracks=4,
        instruments=(("choir", "melody", 9), ("organ", "harmony", 8), ("electric_bass", "bass", 7), ("drums", "rhythm", 8)),
    ))

    # =================================================================
    # R&B / FUNK
    # =================================================================
    nodes.append(_g("rnb", "R&B",
        aliases=("r&b", "rhythm and blues", "r and b"),
        tempo=(70, 100), key="Ab", scale="minor", energy="medium", tracks=5,
        chord_feel="7ths",
        instruments=(("piano", "harmony", 8), ("electric_bass", "bass", 8), ("drums", "rhythm", 8), ("synth_pad", "pad", 6), ("voice_oohs", "melody", 9)),
        density=(20, 40), regularity=(0.5, 0.8), dissonance=(0.2, 0.5),
    ))
    nodes.append(_g("rnb.funk", "Funk", parent="rnb",
        aliases=("funk music", "funky"),
        tempo=(95, 115), key="E", scale="mixolydian", energy="high", tracks=5,
        instruments=(("electric_guitar", "melody", 9), ("slap_bass", "bass", 9), ("drums", "rhythm", 9), ("organ", "harmony", 7), ("brass", "lead", 6)),
    ))
    nodes.append(_g("rnb.disco", "Disco", parent="rnb",
        aliases=("disco music",),
        tempo=(110, 130), key="C", scale="major", energy="high", tracks=5,
        instruments=(("strings", "harmony", 8), ("piano", "harmony", 6), ("synth_bass", "bass", 8), ("drums", "rhythm", 9), ("electric_guitar", "melody", 6)),
    ))
    nodes.append(_g("rnb.contemporary", "Contemporary R&B", parent="rnb",
        aliases=("modern r&b", "modern rnb"),
        tempo=(70, 95), key="Ab", scale="minor", energy="medium", tracks=5,
        instruments=(("voice_oohs", "melody", 9), ("electric_piano", "harmony", 7), ("synth_bass", "bass", 7), ("drums", "rhythm", 7), ("synth_pad", "pad", 6)),
    ))
    nodes.append(_g("rnb.neo_funk", "Neo-Funk", parent="rnb",
        aliases=("modern funk",),
        tempo=(100, 120), key="D", scale="minor", energy="medium", tracks=5,
        instruments=(("synth_lead", "lead", 8), ("electric_guitar", "melody", 7), ("synth_bass", "bass", 8), ("drums", "rhythm", 8), ("brass", "lead", 5)),
    ))

    # =================================================================
    # FOLK & COUNTRY
    # =================================================================
    nodes.append(_g("folk", "Folk",
        aliases=("folk music",),
        tempo=(80, 130), key="G", scale="major", energy="medium", tracks=3,
        chord_feel="triads",
        instruments=(("acoustic_guitar", "lead", 9), ("fiddle", "melody", 7), ("fretless_bass", "bass", 6)),
        density=(15, 35), regularity=(0.6, 0.9), dissonance=(0.1, 0.3),
    ))
    nodes.append(_g("folk.celtic", "Celtic", parent="folk",
        aliases=("irish", "celtic music", "irish music"),
        tempo=(100, 150), key="D", scale="dorian", energy="high", tracks=4,
        instruments=(("tin_whistle", "melody", 9), ("fiddle", "melody", 8), ("acoustic_guitar", "harmony", 7), ("drums", "rhythm", 5)),
    ))
    nodes.append(_g("folk.country", "Country", parent="folk",
        aliases=("country music",),
        tempo=(100, 140), key="G", scale="major", energy="medium", tracks=5,
        instruments=(("acoustic_guitar", "lead", 8), ("steel_guitar", "melody", 7), ("electric_bass", "bass", 7), ("drums", "rhythm", 8), ("fiddle", "melody", 5)),
    ))
    nodes.append(_g("folk.bluegrass", "Bluegrass", parent="folk",
        aliases=(),
        tempo=(120, 160), key="G", scale="major", energy="high", tracks=4,
        instruments=(("banjo", "lead", 9), ("mandolin", "melody", 8), ("acoustic_guitar", "harmony", 7), ("fretless_bass", "bass", 7)),
    ))
    nodes.append(_g("folk.americana", "Americana", parent="folk",
        aliases=("roots rock",),
        tempo=(90, 130), key="G", scale="major", energy="medium", tracks=5,
        instruments=(("acoustic_guitar", "lead", 8), ("electric_guitar", "melody", 7), ("electric_bass", "bass", 7), ("drums", "rhythm", 7), ("organ", "harmony", 5)),
    ))
    nodes.append(_g("folk.balkan", "Balkan", parent="folk",
        aliases=("balkan music", "balkan brass"),
        tempo=(100, 160), key="D", scale="phrygian_dominant", energy="high", tracks=4,
        instruments=(("trumpet", "lead", 9), ("tuba", "bass", 7), ("clarinet", "melody", 8), ("drums", "rhythm", 8)),
    ))
    nodes.append(_g("folk.nordic", "Nordic Folk", parent="folk",
        aliases=("scandinavian folk",),
        tempo=(70, 120), key="D", scale="dorian", energy="low", tracks=3,
        instruments=(("nyckelharpa", "lead", 9), ("hardingfele", "melody", 7), ("synth_pad", "pad", 5)),
    ))
    nodes.append(_g("folk.klezmer", "Klezmer", parent="folk",
        aliases=("klezmer music",),
        tempo=(100, 160), key="D", scale="klezmer_freygish", energy="high", tracks=4,
        instruments=(("clarinet", "lead", 9), ("violin", "melody", 8), ("accordion", "harmony", 7), ("drums", "rhythm", 6)),
    ))
    nodes.append(_g("folk.fado", "Fado", parent="folk",
        aliases=("portuguese fado",),
        tempo=(60, 90), key="A", scale="minor", energy="low", tracks=3,
        instruments=(("acoustic_guitar", "lead", 9), ("voice_oohs", "melody", 8), ("acoustic_guitar", "harmony", 6)),
    ))
    nodes.append(_g("folk.flamenco", "Flamenco", parent="folk",
        aliases=("flamenco music",),
        tempo=(80, 150), key="E", scale="phrygian_dominant", energy="high", tracks=3,
        instruments=(("acoustic_guitar", "lead", 9), ("acoustic_guitar", "harmony", 7), ("drums", "rhythm", 6)),
    ))

    # =================================================================
    # LATIN & CARIBBEAN
    # =================================================================
    nodes.append(_g("latin", "Latin",
        aliases=("latin music",),
        tempo=(90, 140), key="C", scale="major", energy="high", tracks=5,
        chord_feel="triads",
        instruments=(("trumpet", "lead", 8), ("piano", "harmony", 8), ("electric_bass", "bass", 7), ("drums", "rhythm", 9), ("acoustic_guitar", "harmony", 5)),
        density=(20, 45), regularity=(0.5, 0.8), dissonance=(0.1, 0.4),
    ))
    nodes.append(_g("latin.salsa", "Salsa", parent="latin",
        aliases=("salsa music",),
        tempo=(140, 180), key="C", scale="major", energy="very_high", tracks=6,
        instruments=(("trumpet", "lead", 9), ("piano", "harmony", 8), ("electric_bass", "bass", 8), ("drums", "rhythm", 9), ("trombone", "harmony", 6), ("saxophone", "melody", 5)),
    ))
    nodes.append(_g("latin.reggaeton", "Reggaeton", parent="latin",
        aliases=("reggaeton", "perreo"),
        tempo=(85, 100), key="D", scale="minor", energy="high", tracks=4,
        instruments=(("synth_lead", "lead", 8), ("synth_bass", "bass", 9), ("drums", "rhythm", 9), ("voice_oohs", "pad", 5)),
    ))
    nodes.append(_g("latin.samba", "Samba", parent="latin",
        aliases=("samba music", "brazilian samba"),
        tempo=(100, 130), key="C", scale="major", energy="high", tracks=4,
        instruments=(("acoustic_guitar", "lead", 8), ("piano", "harmony", 6), ("electric_bass", "bass", 7), ("drums", "rhythm", 9)),
    ))
    nodes.append(_g("latin.cumbia", "Cumbia", parent="latin",
        aliases=("cumbia music",),
        tempo=(90, 110), key="C", scale="major", energy="medium", tracks=4,
        instruments=(("accordion", "lead", 8), ("electric_guitar", "harmony", 6), ("electric_bass", "bass", 7), ("drums", "rhythm", 8)),
    ))
    nodes.append(_g("latin.reggae", "Reggae", parent="latin",
        aliases=("reggae music", "roots reggae"),
        tempo=(70, 90), key="G", scale="major", energy="medium", tracks=4,
        instruments=(("electric_guitar", "melody", 8), ("organ", "harmony", 7), ("electric_bass", "bass", 9), ("drums", "rhythm", 8)),
    ))
    nodes.append(_g("latin.tango", "Tango", parent="latin",
        aliases=("argentine tango",),
        tempo=(60, 80), key="D", scale="minor", energy="medium", tracks=4,
        instruments=(("bandoneon", "lead", 9), ("violin", "melody", 7), ("electric_bass", "bass", 7), ("piano", "harmony", 6)),
    ))
    nodes.append(_g("latin.ska", "Ska", parent="latin",
        aliases=("ska music",),
        tempo=(110, 130), key="G", scale="major", energy="high", tracks=5,
        instruments=(("electric_guitar", "melody", 8), ("organ", "harmony", 7), ("electric_bass", "bass", 8), ("drums", "rhythm", 9), ("brass", "lead", 7)),
    ))
    nodes.append(_g("latin.dancehall", "Dancehall", parent="latin",
        aliases=("dancehall",),
        tempo=(95, 110), key="D", scale="minor", energy="high", tracks=4,
        instruments=(("synth_lead", "lead", 8), ("synth_bass", "bass", 9), ("drums", "rhythm", 9), ("voice_oohs", "pad", 5)),
    ))
    nodes.append(_g("latin.bachata", "Bachata", parent="latin",
        aliases=("bachata music",),
        tempo=(110, 130), key="D", scale="minor", energy="medium", tracks=4,
        instruments=(("acoustic_guitar", "lead", 9), ("acoustic_guitar", "harmony", 7), ("electric_bass", "bass", 7), ("drums", "rhythm", 7)),
    ))
    nodes.append(_g("latin.merengue", "Merengue", parent="latin",
        tempo=(130, 160), key="C", scale="major", energy="very_high", tracks=4,
        instruments=(("accordion", "lead", 8), ("electric_bass", "bass", 7), ("drums", "rhythm", 9), ("saxophone", "melody", 6)),
    ))
    nodes.append(_g("latin.calypso", "Calypso", parent="latin",
        aliases=("soca", "calypso music"),
        tempo=(100, 130), key="C", scale="major", energy="high", tracks=4,
        instruments=(("steel_drum", "lead", 9), ("electric_bass", "bass", 7), ("drums", "rhythm", 8), ("acoustic_guitar", "harmony", 6)),
    ))

    # =================================================================
    # AFRICAN
    # =================================================================
    nodes.append(_g("african", "African",
        aliases=("african music",),
        tempo=(100, 140), key="C", scale="major", energy="high", tracks=5,
        chord_feel="triads",
        instruments=(("electric_guitar", "lead", 8), ("trumpet", "melody", 6), ("electric_bass", "bass", 8), ("drums", "rhythm", 9), ("piano", "harmony", 5)),
        density=(20, 45), regularity=(0.4, 0.8), dissonance=(0.1, 0.4),
    ))
    nodes.append(_g("african.afrobeat", "Afrobeat", parent="african",
        aliases=("afrobeats", "afro beat", "afro-beat"),
        tempo=(100, 130), key="D", scale="dorian", energy="high", tracks=6,
        instruments=(("trumpet", "lead", 8), ("organ", "harmony", 7), ("electric_bass", "bass", 8), ("drums", "rhythm", 9), ("saxophone", "melody", 6), ("electric_guitar", "harmony", 5)),
    ))
    nodes.append(_g("african.amapiano", "Amapiano", parent="african",
        aliases=("amapiano music",),
        tempo=(110, 120), key="C", scale="major", energy="medium", tracks=5,
        instruments=(("piano", "lead", 9), ("kalimba", "melody", 7), ("synth_bass", "bass", 8), ("drums", "rhythm", 8), ("synth_pad", "pad", 5)),
    ))
    nodes.append(_g("african.highlife", "Highlife", parent="african",
        aliases=("ghanaian highlife",),
        tempo=(100, 130), key="C", scale="major", energy="medium", tracks=5,
        instruments=(("electric_guitar", "lead", 9), ("trumpet", "melody", 7), ("electric_bass", "bass", 8), ("drums", "rhythm", 8), ("piano", "harmony", 5)),
    ))
    nodes.append(_g("african.soukous", "Soukous", parent="african",
        aliases=("congolese rumba",),
        tempo=(110, 140), key="C", scale="major", energy="high", tracks=5,
        instruments=(("electric_guitar", "lead", 9), ("piano", "harmony", 6), ("electric_bass", "bass", 8), ("drums", "rhythm", 9), ("brass", "lead", 5)),
    ))
    nodes.append(_g("african.desert_blues", "Desert Blues", parent="african",
        aliases=("saharan blues", "tuareg", "tinariwen"),
        tempo=(80, 110), key="A", scale="pentatonic_minor", energy="medium", tracks=4,
        instruments=(("electric_guitar", "lead", 9), ("electric_bass", "bass", 7), ("drums", "rhythm", 7), ("drums", "rhythm", 5)),
    ))
    nodes.append(_g("african.gnawa", "Gnawa", parent="african",
        aliases=("gnawa music",),
        tempo=(80, 120), key="D", scale="minor", energy="medium", tracks=3,
        instruments=(("electric_bass", "lead", 9), ("kalimba", "melody", 7), ("drums", "rhythm", 8)),
    ))
    nodes.append(_g("african.mbalax", "Mbalax", parent="african",
        aliases=("senegalese mbalax",),
        tempo=(110, 140), key="C", scale="major", energy="very_high", tracks=4,
        instruments=(("drums", "rhythm", 9), ("electric_guitar", "lead", 7), ("electric_bass", "bass", 7), ("voice_oohs", "melody", 5)),
    ))
    nodes.append(_g("african.juju", "Jùjú", parent="african",
        aliases=("juju music",),
        tempo=(100, 130), key="G", scale="major", energy="medium", tracks=5,
        instruments=(("drums", "rhythm", 9), ("electric_guitar", "lead", 8), ("electric_bass", "bass", 7), ("steel_guitar", "melody", 6), ("drums", "rhythm", 5)),
    ))

    # =================================================================
    # ASIAN & MIDDLE EASTERN
    # =================================================================
    nodes.append(_g("asian", "Asian & Middle Eastern",
        aliases=("asian music", "middle eastern"),
        tempo=(70, 130), key="D", scale="minor", energy="medium", tracks=4,
        chord_feel="modal",
        instruments=(("acoustic_guitar", "lead", 8), ("flute", "melody", 7), ("electric_bass", "bass", 6), ("drums", "rhythm", 7)),
        density=(15, 40), regularity=(0.4, 0.8), dissonance=(0.2, 0.6),
    ))
    nodes.append(_g("asian.hindustani", "Hindustani Classical", parent="asian",
        aliases=("raga", "hindustani", "indian classical"),
        tempo=(60, 130), key="C", scale="raga_bhairav", energy="medium", tracks=3,
        instruments=(("sitar", "lead", 9), ("flute", "melody", 7), ("drums", "rhythm", 8)),
    ))
    nodes.append(_g("asian.carnatic", "Carnatic", parent="asian",
        aliases=("carnatic music",),
        tempo=(60, 130), key="C", scale="major", energy="medium", tracks=3,
        instruments=(("violin", "lead", 9), ("flute", "melody", 7), ("drums", "rhythm", 8)),
    ))
    nodes.append(_g("asian.bollywood", "Bollywood", parent="asian",
        aliases=("bollywood music", "hindi film"),
        tempo=(90, 140), key="D", scale="harmonic_minor", energy="high", tracks=6,
        instruments=(("sitar", "lead", 7), ("violin", "melody", 7), ("electric_bass", "bass", 7), ("drums", "rhythm", 8), ("synth_strings", "pad", 6), ("piano", "harmony", 5)),
    ))
    nodes.append(_g("asian.gamelan", "Gamelan", parent="asian",
        aliases=("javanese gamelan", "balinese gamelan"),
        tempo=(60, 100), key="C", scale="balinese_pelog", energy="low", tracks=4,
        instruments=(("glockenspiel", "lead", 8), ("xylophone", "melody", 7), ("marimba", "harmony", 7), ("drums", "rhythm", 5)),
    ))
    nodes.append(_g("asian.maqam", "Maqam", parent="asian",
        aliases=("arabic maqam", "arabic", "arabic music"),
        tempo=(80, 120), key="D", scale="hijaz", energy="medium", tracks=4,
        instruments=(("oud", "lead", 9), ("ney", "melody", 7), ("electric_bass", "bass", 6), ("drums", "rhythm", 7)),
    ))
    nodes.append(_g("asian.turkish", "Turkish", parent="asian",
        aliases=("turkish music", "ottoman"),
        tempo=(80, 130), key="D", scale="hijaz", energy="medium", tracks=4,
        instruments=(("oud", "lead", 8), ("violin", "melody", 7), ("electric_bass", "bass", 6), ("drums", "rhythm", 7)),
    ))
    nodes.append(_g("asian.persian", "Persian", parent="asian",
        aliases=("persian music", "iranian"),
        tempo=(70, 120), key="D", scale="double_harmonic", energy="medium", tracks=3,
        instruments=(("tar", "lead", 9), ("ney", "melody", 7), ("drums", "rhythm", 6)),
    ))
    nodes.append(_g("asian.qawwali", "Qawwali", parent="asian",
        aliases=("qawwali music",),
        tempo=(80, 140), key="D", scale="minor", energy="high", tracks=4,
        instruments=(("harmonium", "harmony", 8), ("drums", "rhythm", 8), ("voice_oohs", "melody", 9), ("drums", "rhythm", 6)),
    ))
    nodes.append(_g("asian.japanese_traditional", "Japanese Traditional", parent="asian",
        aliases=("traditional japanese",),
        tempo=(50, 100), key="D", scale="japanese_in", energy="low", tracks=3,
        instruments=(("koto", "lead", 9), ("shakuhachi", "melody", 8), ("drums", "rhythm", 5)),
    ))
    nodes.append(_g("asian.chinese_traditional", "Chinese Traditional", parent="asian",
        aliases=("traditional chinese",),
        tempo=(60, 110), key="C", scale="chinese_pentatonic", energy="low", tracks=3,
        instruments=(("guzheng", "lead", 9), ("dizi", "melody", 7), ("glockenspiel", "harmony", 5)),
    ))
    nodes.append(_g("asian.korean_traditional", "Korean Traditional", parent="asian",
        aliases=("traditional korean",),
        tempo=(60, 100), key="C", scale="pentatonic_minor", energy="low", tracks=3,
        instruments=(("gayageum", "lead", 9), ("flute", "melody", 7), ("drums", "rhythm", 6)),
    ))
    nodes.append(_g("asian.khaleeji", "Khaleeji", parent="asian",
        aliases=("khaliji", "gulf arabic"),
        tempo=(90, 120), key="D", scale="hijaz", energy="medium", tracks=4,
        instruments=(("oud", "lead", 8), ("synth_pad", "pad", 6), ("electric_bass", "bass", 6), ("drums", "rhythm", 8)),
    ))

    # =================================================================
    # CLASSICAL
    # =================================================================
    nodes.append(_g("classical", "Classical",
        aliases=("classical music", "orchestral"),
        tempo=(60, 120), key="G", scale="major", energy="medium", tracks=4,
        chord_feel="triads",
        instruments=(("strings", "harmony", 9), ("piano", "melody", 8), ("cello", "bass", 7), ("flute", "melody", 6)),
        density=(20, 60), regularity=(0.6, 1.0), dissonance=(0.1, 0.6),
    ))
    nodes.append(_g("classical.baroque", "Baroque", parent="classical",
        aliases=("bach", "baroque music"),
        tempo=(60, 120), key="D", scale="major", energy="medium", tracks=4,
        instruments=(("harpsichord", "lead", 9), ("violin", "melody", 8), ("cello", "bass", 7), ("strings", "harmony", 6)),
    ))
    nodes.append(_g("classical.classical_era", "Classical Era", parent="classical",
        aliases=("mozart", "haydn"),
        tempo=(80, 140), key="C", scale="major", energy="medium", tracks=4,
        instruments=(("piano", "lead", 9), ("violin", "melody", 8), ("cello", "bass", 7), ("strings", "harmony", 6)),
    ))
    nodes.append(_g("classical.romantic", "Romantic", parent="classical",
        aliases=("romantic era",),
        tempo=(50, 120), key="D", scale="minor", energy="high", tracks=6,
        instruments=(("piano", "lead", 9), ("strings", "harmony", 8), ("cello", "bass", 7), ("french_horn", "melody", 6), ("flute", "melody", 5), ("harp", "harmony", 5)),
    ))
    nodes.append(_g("classical.impressionist", "Impressionist", parent="classical",
        aliases=("debussy", "ravel"),
        tempo=(60, 100), key="D", scale="whole_tone", energy="low", tracks=4,
        instruments=(("piano", "lead", 9), ("flute", "melody", 7), ("cello", "bass", 6), ("harp", "harmony", 7)),
    ))
    nodes.append(_g("classical.minimalist", "Minimalist", parent="classical",
        aliases=("minimal classical",),
        tempo=(60, 120), key="C", scale="major", energy="low", tracks=4,
        instruments=(("piano", "lead", 9), ("marimba", "melody", 7), ("strings", "harmony", 6), ("vibraphone", "melody", 5)),
    ))
    nodes.append(_g("classical.symphonic", "Symphonic", parent="classical",
        aliases=("symphony", "orchestral symphonic"),
        tempo=(60, 140), key="D", scale="minor", energy="high", tracks=7,
        instruments=(("violin", "lead", 9), ("brass", "melody", 8), ("contrabass", "bass", 7), ("strings", "harmony", 8), ("flute", "melody", 6), ("drums", "rhythm", 5), ("harp", "harmony", 4)),
    ))
    nodes.append(_g("classical.choral", "Choral", parent="classical",
        aliases=("choir music",),
        tempo=(60, 100), key="C", scale="major", energy="medium", tracks=3,
        instruments=(("choir", "lead", 9), ("organ", "harmony", 8), ("strings", "pad", 5)),
    ))

    # =================================================================
    # LO-FI (keep as root for backward compat)
    # =================================================================
    nodes.append(_g("lofi", "Lo-fi",
        aliases=("lo-fi", "lo fi", "lo-fi hip-hop", "lofi beats"),
        tempo=(70, 90), key="D", scale="minor", energy="low", tracks=4,
        chord_feel="7ths",
        instruments=(("piano", "melody", 8), ("electric_bass", "bass", 7), ("drums", "rhythm", 8), ("synth_pad", "pad", 6)),
        density=(15, 40), regularity=(0.5, 0.8), dissonance=(0.2, 0.5),
    ))

    # =================================================================
    # AMBIENT
    # =================================================================
    nodes.append(_g("ambient", "Ambient",
        aliases=("ambient music",),
        tempo=(60, 80), key="C", scale="major", energy="low", tracks=3,
        chord_feel="open",
        instruments=(("synth_pad", "pad", 9), ("strings", "harmony", 7), ("piano", "melody", 5)),
        density=(5, 20), regularity=(0.7, 1.0), dissonance=(0.0, 0.3),
    ))

    # =================================================================
    # CINEMATIC
    # =================================================================
    nodes.append(_g("cinematic", "Cinematic",
        aliases=("film score", "soundtrack", "movie music"),
        tempo=(70, 100), key="D", scale="minor", energy="high", tracks=7,
        chord_feel="triads",
        instruments=(("strings", "harmony", 9), ("brass", "lead", 8), ("drums", "rhythm", 7), ("piano", "melody", 6), ("choir", "pad", 5), ("timpani", "rhythm", 5), ("harp", "melody", 4)),
        density=(10, 35), regularity=(0.5, 0.8), dissonance=(0.2, 0.6),
    ))
    nodes.append(_g("cinematic.epic", "Epic", parent="cinematic",
        aliases=("epic music", "trailer music"),
        tempo=(80, 110), key="D", scale="minor", energy="very_high", tracks=8,
        instruments=(("brass", "lead", 9), ("strings", "harmony", 9), ("electric_bass", "bass", 7), ("drums", "rhythm", 9), ("choir", "pad", 8), ("piano", "melody", 6), ("synth_pad", "pad", 5), ("timpani", "rhythm", 7)),
    ))
    nodes.append(_g("cinematic.dark_ambient", "Dark Ambient", parent="cinematic",
        aliases=("dark ambient",),
        tempo=(50, 70), key="D", scale="minor", energy="low", tracks=3,
        instruments=(("synth_pad", "pad", 9), ("electric_bass", "bass", 6), ("fx_atmosphere", "fx", 7)),
    ))
    nodes.append(_g("cinematic.meditation", "Meditation", parent="cinematic",
        aliases=("meditation music", "zen", "healing"),
        tempo=(50, 70), key="C", scale="major", energy="very_low", tracks=3,
        instruments=(("synth_pad", "pad", 8), ("harp", "melody", 7), ("bells", "melody", 6)),
    ))
    nodes.append(_g("cinematic.horror", "Horror", parent="cinematic",
        aliases=("horror music", "scary"),
        tempo=(60, 90), key="D", scale="minor", energy="medium", tracks=5,
        instruments=(("strings", "lead", 9), ("synth_pad", "pad", 7), ("electric_bass", "bass", 6), ("drums", "rhythm", 5), ("piano", "melody", 5)),
    ))
    nodes.append(_g("cinematic.video_game", "Video Game", parent="cinematic",
        aliases=("game music", "gaming", "8-bit", "chiptune"),
        tempo=(100, 150), key="C", scale="major", energy="high", tracks=5,
        instruments=(("synth_lead", "lead", 9), ("piano", "harmony", 6), ("electric_bass", "bass", 7), ("drums", "rhythm", 8), ("strings", "pad", 5)),
    ))
    nodes.append(_g("cinematic.fantasy", "Fantasy", parent="cinematic",
        aliases=("fantasy music", "medieval"),
        tempo=(80, 120), key="D", scale="minor", energy="medium", tracks=5,
        instruments=(("flute", "lead", 8), ("strings", "harmony", 8), ("electric_bass", "bass", 6), ("drums", "rhythm", 6), ("harp", "melody", 7)),
    ))

    # Also register backward-compat alias "funk" → "rnb.funk"
    # (handled in get_genre via alias lookup)

    # Build registry dict
    registry: Dict[str, GenreNode] = {}
    for node in nodes:
        registry[node.id] = node
    return registry


# Build once at import time
GENRE_TREE: Dict[str, GenreNode] = _build_genre_tree()


# =====================================================================
# Helper functions
# =====================================================================

def get_genre(genre_id: str) -> Optional[GenreNode]:
    """Look up a genre by ID. Returns None if not found.

    Also resolves backward-compat aliases:
      - "funk" → "rnb.funk"
    """
    node = GENRE_TREE.get(genre_id)
    if node is not None:
        return node

    # Backward compat: "funk" → "rnb.funk"
    _COMPAT_ALIASES = {
        "funk": "rnb.funk",
    }
    alias_target = _COMPAT_ALIASES.get(genre_id)
    if alias_target:
        return GENRE_TREE.get(alias_target)

    return None


def get_root_genres() -> List[GenreNode]:
    """Return all root-level genres (depth 0)."""
    return [n for n in GENRE_TREE.values() if n.depth == 0]


def get_children(parent_id: str) -> List[GenreNode]:
    """Return direct children of a given genre ID."""
    return [
        n for n in GENRE_TREE.values()
        if n.parent == parent_id
    ]


def all_genre_ids() -> List[str]:
    """Return all registered genre IDs (sorted)."""
    return sorted(GENRE_TREE.keys())


def get_genre_ids_for_validation() -> Tuple[str, ...]:
    """Return a tuple of all genre IDs suitable for schema validation.

    This replaces the hardcoded SUPPORTED_GENRES tuple in schema.py.
    """
    return tuple(sorted(GENRE_TREE.keys()))


def get_tempo_ranges() -> Dict[str, Tuple[int, int]]:
    """Return a dict of genre_id → (min_bpm, max_bpm) for all genres."""
    return {gid: node.tempo_range for gid, node in GENRE_TREE.items()}


def find_by_alias(alias: str) -> Optional[GenreNode]:
    """Find a genre by one of its aliases. Case-insensitive."""
    alias_lower = alias.lower().strip()
    for node in GENRE_TREE.values():
        if alias_lower in (a.lower() for a in node.aliases):
            return node
        if alias_lower == node.name.lower():
            return node
    return None


def get_genre_instruments(genre_id: str) -> List[Tuple[str, str, int]]:
    """Return the instrument palette for a genre as list of (name, role, priority).

    Falls back to parent genre if current has no instruments, then to pop.
    """
    node = get_genre(genre_id)
    if node is None:
        node = GENRE_TREE.get("pop")
    if node and node.instruments:
        return list(node.instruments)
    # Try parent
    if node and node.parent:
        parent = GENRE_TREE.get(node.parent)
        if parent and parent.instruments:
            return list(parent.instruments)
    return list(GENRE_TREE["pop"].instruments)


def resolve_scale(scale_name: str) -> Optional[List[int]]:
    """Resolve a scale name (including aliases) to interval list."""
    canonical = SCALE_ALIASES.get(scale_name.lower(), scale_name.lower())
    scale = SCALES_EXTENDED.get(canonical)
    if scale is not None:
        # Convert any float intervals to int (for quarter-tone approximations)
        return [int(i) for i in scale]
    return None


def get_all_scale_names() -> Tuple[str, ...]:
    """Return all supported scale names (canonical + aliases)."""
    names = set(SCALES_EXTENDED.keys())
    names.update(SCALE_ALIASES.keys())
    return tuple(sorted(names))
