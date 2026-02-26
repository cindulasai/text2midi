# -*- coding: utf-8 -*-
"""
MIDI Generation Test Cases
==========================
110 distinct, realistic test cases that cover a broad range of genres,
moods, energies and edge conditions.

Each ``TestCase`` includes:
  - ``test_id``         – unique identifier (e.g. "tc_001")
  - ``prompt``          – the user prompt sent to the agentic graph
  - ``expected_*``      – constraints used by ``MidiEvaluator``
  - ``comment``         – human-readable explanation of what is being tested

Expected Attribute Conventions
-------------------------------
Tempo ranges are genre-informed:
  - Slow ballad / ambient    : 50–80 BPM
  - Mid-tempo pop / R&B      : 80–110 BPM
  - Lo-fi / Chill hip-hop    : 70–95 BPM
  - Standard rock / pop      : 100–130 BPM
  - Upbeat / dance           : 120–140 BPM
  - Fast / drum-n-bass       : 140–180 BPM
  - Very fast / metal        : 160–220 BPM

Pitch ranges (average MIDI note):
  - Bass-heavy (bass guitar)    : 28–52
  - Mid-range (piano, guitar)   : 48–72
  - High-energy / bright leads  : 60–84

Note density thresholds are calibrated for a typical 60-second output.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Tuple


@dataclass
class TestCase:
    """Single MIDI generation test case."""

    test_id: str
    prompt: str
    comment: str

    # Expected attribute constraints (None = not evaluated)
    expected_tempo_range: Optional[Tuple[float, float]] = None
    expected_track_count_range: Optional[Tuple[int, int]] = None
    expected_note_count_range: Optional[Tuple[int, int]] = None
    expected_duration_range: Optional[Tuple[float, float]] = None
    expected_pitch_range: Optional[Tuple[float, float]] = None
    expected_has_drums: Optional[bool] = None

    # Per-case pass threshold override (default used when None)
    pass_threshold: float = 0.55


# ============================================================================
# TEST CASES – 110 entries
# ============================================================================

TEST_CASES: list[TestCase] = [

    # ── Lo-Fi / Chill ────────────────────────────────────────────────────────

    TestCase(
        test_id="tc_001",
        prompt="Calm lo-fi hip-hop study beats with soft piano and vinyl crackle",
        comment="Classic lo-fi: slow swing tempo, light piano, subtle percussion",
        expected_tempo_range=(65, 95),
        expected_track_count_range=(2, 5),
        expected_note_count_range=(60, 500),
        expected_duration_range=(30, 180),
        expected_pitch_range=(45, 78),
        expected_has_drums=True,
    ),
    TestCase(
        test_id="tc_002",
        prompt="Rainy evening lo-fi chill with mellow guitar and slow drum groove",
        comment="Lo-fi with acoustic guitar texture; moderate note density",
        expected_tempo_range=(70, 90),
        expected_track_count_range=(2, 4),
        expected_note_count_range=(50, 400),
        expected_duration_range=(30, 180),
        expected_has_drums=True,
    ),
    TestCase(
        test_id="tc_003",
        prompt="Lo-fi bedroom pop with dreamy synth pads and slow bass",
        comment="Lo-fi synth-pop: lower register bass against pad harmonics",
        expected_tempo_range=(68, 92),
        expected_track_count_range=(2, 4),
        expected_note_count_range=(40, 350),
        expected_duration_range=(30, 180),
        expected_has_drums=True,
    ),

    # ── Ambient / Atmospheric ────────────────────────────────────────────────

    TestCase(
        test_id="tc_004",
        prompt="Slow evolving ambient soundscape with long reverb tails and no percussion",
        comment="Pure ambient: very low note count, wide sustain, no drums",
        expected_tempo_range=(50, 80),
        expected_track_count_range=(1, 4),
        expected_note_count_range=(5, 150),
        expected_duration_range=(30, 240),
        expected_has_drums=False,
    ),
    TestCase(
        test_id="tc_005",
        prompt="Space ambient with shimmering pads, ethereal vocals and deep sub-drone",
        comment="Ambient: very sparse notes, high register pads over sub-bass",
        expected_tempo_range=(40, 75),
        expected_track_count_range=(2, 5),
        expected_note_count_range=(5, 200),
        expected_duration_range=(30, 240),
        expected_has_drums=False,
    ),
    TestCase(
        test_id="tc_006",
        prompt="Dark ambient horror atmosphere with dissonant strings and low drones",
        comment="Horror ambient: dissonant low pitches, no drums, tense mood",
        expected_tempo_range=(40, 80),
        expected_track_count_range=(1, 4),
        expected_note_count_range=(5, 180),
        expected_duration_range=(30, 180),
        expected_pitch_range=(28, 62),
        expected_has_drums=False,
    ),
    TestCase(
        test_id="tc_007",
        prompt="Nature-inspired ambient with flowing water sounds, gentle flute melody",
        comment="Gentle ambient: mid-to-high register flute melody, serene",
        expected_tempo_range=(55, 85),
        expected_track_count_range=(1, 3),
        expected_note_count_range=(20, 200),
        expected_duration_range=(30, 180),
        expected_has_drums=False,
    ),
    TestCase(
        test_id="tc_008",
        prompt="Meditative ambient drone for yoga and mindfulness practice",
        comment="Meditative drone: very slow, sparse, low-energy",
        expected_tempo_range=(45, 70),
        expected_track_count_range=(1, 3),
        expected_note_count_range=(5, 100),
        expected_duration_range=(30, 300),
        expected_has_drums=False,
    ),

    # ── Classical ────────────────────────────────────────────────────────────

    TestCase(
        test_id="tc_009",
        prompt="Romantic era piano sonata with flowing arpeggios and expressive dynamics",
        comment="Classical piano: rich note density, wide pitch range, no drums",
        expected_tempo_range=(60, 120),
        expected_track_count_range=(1, 2),
        expected_note_count_range=(150, 1200),
        expected_duration_range=(30, 300),
        expected_pitch_range=(36, 84),
        expected_has_drums=False,
    ),
    TestCase(
        test_id="tc_010",
        prompt="Baroque counterpoint harpsichord piece with intricate voice leading",
        comment="Baroque: multiple independent voices, moderate tempo, no drums",
        expected_tempo_range=(80, 130),
        expected_track_count_range=(2, 4),
        expected_note_count_range=(200, 1500),
        expected_duration_range=(30, 240),
        expected_has_drums=False,
    ),
    TestCase(
        test_id="tc_011",
        prompt="Classical string quartet with violin, viola and cello performing adagio",
        comment="String quartet: 4 tracks, slow sustained notes, no drums",
        expected_tempo_range=(50, 90),
        expected_track_count_range=(3, 5),
        expected_note_count_range=(80, 600),
        expected_duration_range=(30, 240),
        expected_has_drums=False,
    ),
    TestCase(
        test_id="tc_012",
        prompt="Fast vivace classical piano etude with rapid scale runs",
        comment="Fast etude: very high note density, wide pitch span, fast tempo",
        expected_tempo_range=(120, 200),
        expected_track_count_range=(1, 2),
        expected_note_count_range=(300, 2000),
        expected_duration_range=(20, 180),
        expected_has_drums=False,
    ),
    TestCase(
        test_id="tc_013",
        prompt="Orchestral classical symphony opening movement with full strings and brass",
        comment="Full orchestra: many tracks, high note count, dynamic range",
        expected_tempo_range=(80, 160),
        expected_track_count_range=(4, 10),
        expected_note_count_range=(200, 2000),
        expected_duration_range=(30, 300),
        expected_has_drums=False,
    ),

    # ── Jazz ─────────────────────────────────────────────────────────────────

    TestCase(
        test_id="tc_014",
        prompt="Slow jazz ballad with warm tenor saxophone and walking bass",
        comment="Jazz ballad: slow tempo, rich chord extensions, walking bass",
        expected_tempo_range=(55, 90),
        expected_track_count_range=(2, 4),
        expected_note_count_range=(80, 600),
        expected_duration_range=(30, 180),
        expected_has_drums=True,
    ),
    TestCase(
        test_id="tc_015",
        prompt="Upbeat bebop jazz with fast melodic runs and complex chord progressions",
        comment="Bebop: fast tempo, complex harmonics, high note density",
        expected_tempo_range=(160, 280),
        expected_track_count_range=(2, 5),
        expected_note_count_range=(200, 1500),
        expected_duration_range=(20, 120),
        expected_has_drums=True,
    ),
    TestCase(
        test_id="tc_016",
        prompt="Cool jazz piano trio with brushed drums and double bass",
        comment="Cool jazz: medium tempo, light percussion (brushed feel), piano",
        expected_tempo_range=(100, 160),
        expected_track_count_range=(2, 4),
        expected_note_count_range=(100, 800),
        expected_duration_range=(30, 180),
        expected_has_drums=True,
    ),
    TestCase(
        test_id="tc_017",
        prompt="Latin jazz bossa nova with nylon guitar and subtle congas",
        comment="Bossa nova: characteristic syncopated rhythm, guitar focus",
        expected_tempo_range=(100, 140),
        expected_track_count_range=(2, 4),
        expected_note_count_range=(80, 700),
        expected_duration_range=(30, 180),
        expected_has_drums=True,
    ),

    # ── Electronic / EDM ─────────────────────────────────────────────────────

    TestCase(
        test_id="tc_018",
        prompt="Four-on-the-floor house music with punchy kick and arpeggiated synth",
        comment="House music: 4/4 kick pattern (120–128 BPM), arpeggios",
        expected_tempo_range=(118, 135),
        expected_track_count_range=(3, 7),
        expected_note_count_range=(200, 1500),
        expected_duration_range=(30, 240),
        expected_has_drums=True,
    ),
    TestCase(
        test_id="tc_019",
        prompt="Techno warehouse banger with hypnotic bassline and industrial percussion",
        comment="Techno: 130–145 BPM, heavy kick, minimal melodic content",
        expected_tempo_range=(128, 148),
        expected_track_count_range=(3, 7),
        expected_note_count_range=(150, 1200),
        expected_duration_range=(30, 300),
        expected_has_drums=True,
    ),
    TestCase(
        test_id="tc_020",
        prompt="Drum and bass breakbeat with fast amen break and sub bass reese",
        comment="DnB: very fast tempo, complex drum pattern, low bass",
        expected_tempo_range=(160, 185),
        expected_track_count_range=(2, 5),
        expected_note_count_range=(150, 1200),
        expected_duration_range=(30, 180),
        expected_pitch_range=(28, 72),
        expected_has_drums=True,
    ),
    TestCase(
        test_id="tc_021",
        prompt="Chillout downtempo electronica with warm pads and slow beat",
        comment="Downtempo: 80–100 BPM, soft pads, light drums",
        expected_tempo_range=(78, 100),
        expected_track_count_range=(2, 5),
        expected_note_count_range=(50, 400),
        expected_duration_range=(30, 180),
        expected_has_drums=True,
    ),
    TestCase(
        test_id="tc_022",
        prompt="Uplifting trance progression with soaring synth lead and 138 BPM build",
        comment="Trance: ~138 BPM, high-register lead, long build sections",
        expected_tempo_range=(130, 148),
        expected_track_count_range=(3, 7),
        expected_note_count_range=(200, 1800),
        expected_duration_range=(30, 300),
        expected_pitch_range=(55, 90),
        expected_has_drums=True,
    ),
    TestCase(
        test_id="tc_023",
        prompt="Dubstep track with heavy 140 BPM half-time groove and massive wobble bass",
        comment="Dubstep: 140 BPM with half-time feel, prominent low bass",
        expected_tempo_range=(135, 150),
        expected_track_count_range=(3, 6),
        expected_note_count_range=(100, 1000),
        expected_duration_range=(30, 180),
        expected_pitch_range=(28, 72),
        expected_has_drums=True,
    ),
    TestCase(
        test_id="tc_024",
        prompt="Ambient techno minimal with slowly evolving pads and subtle beat",
        comment="Minimal techno: moderate note density, sustained pads, simple drums",
        expected_tempo_range=(110, 135),
        expected_track_count_range=(2, 5),
        expected_note_count_range=(60, 600),
        expected_duration_range=(30, 300),
        expected_has_drums=True,
    ),
    TestCase(
        test_id="tc_025",
        prompt="Future bass drop with sidechain pumping lead chords and trap-style hi-hats",
        comment="Future bass: ~150 BPM, dense hi-hats, major key bright chords",
        expected_tempo_range=(140, 165),
        expected_track_count_range=(3, 7),
        expected_note_count_range=(150, 1500),
        expected_duration_range=(20, 180),
        expected_has_drums=True,
    ),

    # ── Pop ───────────────────────────────────────────────────────────────────

    TestCase(
        test_id="tc_026",
        prompt="Catchy upbeat pop song with electric piano chord stabs and claps",
        comment="Upbeat pop: 110–130 BPM, bright instrumentation, full arrangement",
        expected_tempo_range=(108, 132),
        expected_track_count_range=(3, 6),
        expected_note_count_range=(100, 900),
        expected_duration_range=(30, 180),
        expected_has_drums=True,
    ),
    TestCase(
        test_id="tc_027",
        prompt="Emotional pop ballad with heartfelt piano and soft strings",
        comment="Pop ballad: slow tempo, expressive dynamics, no drums",
        expected_tempo_range=(60, 90),
        expected_track_count_range=(2, 4),
        expected_note_count_range=(80, 600),
        expected_duration_range=(30, 240),
        expected_has_drums=False,
    ),
    TestCase(
        test_id="tc_028",
        prompt="Synthpop 80s retro track with analogue synths and drum machine",
        comment="80s synthpop: ~120 BPM, retro synth timbres, electronic drums",
        expected_tempo_range=(110, 135),
        expected_track_count_range=(3, 6),
        expected_note_count_range=(100, 900),
        expected_duration_range=(30, 240),
        expected_has_drums=True,
    ),
    TestCase(
        test_id="tc_029",
        prompt="K-Pop energetic dance track with building chorus and bright lead melody",
        comment="K-pop: 120–145 BPM, bright pitch range, punchy production",
        expected_tempo_range=(118, 148),
        expected_track_count_range=(3, 7),
        expected_note_count_range=(150, 1200),
        expected_duration_range=(30, 240),
        expected_pitch_range=(52, 88),
        expected_has_drums=True,
    ),

    # ── Rock ──────────────────────────────────────────────────────────────────

    TestCase(
        test_id="tc_030",
        prompt="Classic rock guitar riff with distorted electric guitar and driving drums",
        comment="Classic rock: ~120 BPM, power chords, mid-pitch guitar, strong kick/snare",
        expected_tempo_range=(100, 140),
        expected_track_count_range=(3, 6),
        expected_note_count_range=(100, 900),
        expected_duration_range=(30, 180),
        expected_has_drums=True,
    ),
    TestCase(
        test_id="tc_031",
        prompt="Heavy metal riff with drop-D tuned guitar, blast beats and aggressive energy",
        comment="Metal: very fast drums, low-register guitar, high energy",
        expected_tempo_range=(150, 220),
        expected_track_count_range=(3, 6),
        expected_note_count_range=(200, 1500),
        expected_duration_range=(20, 180),
        expected_pitch_range=(26, 70),
        expected_has_drums=True,
    ),
    TestCase(
        test_id="tc_032",
        prompt="Indie rock track with jangly clean guitar, bass and brushed drums",
        comment="Indie rock: medium tempo, clean guitar, relaxed feel",
        expected_tempo_range=(90, 135),
        expected_track_count_range=(3, 5),
        expected_note_count_range=(80, 800),
        expected_duration_range=(30, 180),
        expected_has_drums=True,
    ),
    TestCase(
        test_id="tc_033",
        prompt="Post-rock slow build from quiet arpeggios to crushing wall of sound",
        comment="Post-rock: slow start, big crescendo, wide dynamic range",
        expected_tempo_range=(70, 110),
        expected_track_count_range=(3, 7),
        expected_note_count_range=(100, 1200),
        expected_duration_range=(60, 360),
        expected_has_drums=True,
    ),
    TestCase(
        test_id="tc_034",
        prompt="Punk rock fast three-chord banger with aggressive energy and shouted vocals",
        comment="Punk: very fast, simple chord progression, aggressive percussion",
        expected_tempo_range=(160, 220),
        expected_track_count_range=(2, 5),
        expected_note_count_range=(100, 1000),
        expected_duration_range=(15, 120),
        expected_has_drums=True,
    ),

    # ── Hip-Hop / Trap ────────────────────────────────────────────────────────

    TestCase(
        test_id="tc_035",
        prompt="Trap beat with 808 bass, rapid hi-hats and punchy snare rolls",
        comment="Trap: 130–145 BPM, heavy 808 sub-bass, rolling hi-hats",
        expected_tempo_range=(128, 148),
        expected_track_count_range=(2, 5),
        expected_note_count_range=(80, 900),
        expected_duration_range=(20, 180),
        expected_pitch_range=(28, 65),
        expected_has_drums=True,
    ),
    TestCase(
        test_id="tc_036",
        prompt="Old-school East Coast hip-hop beat with boom-bap drums and soulful sample chops",
        comment="Boom-bap: 85–100 BPM, classic kick/snare pattern, soulful melody",
        expected_tempo_range=(82, 105),
        expected_track_count_range=(2, 5),
        expected_note_count_range=(60, 600),
        expected_duration_range=(20, 180),
        expected_has_drums=True,
    ),
    TestCase(
        test_id="tc_037",
        prompt="Chill hip-hop with jazzy piano chops and mellow bass groove",
        comment="Chill hip-hop: 80–95 BPM, jazz harmonics, light drums",
        expected_tempo_range=(78, 98),
        expected_track_count_range=(2, 4),
        expected_note_count_range=(60, 500),
        expected_duration_range=(20, 180),
        expected_has_drums=True,
    ),
    TestCase(
        test_id="tc_038",
        prompt="Drill music beat with sliding 808s, dark melody and offbeat hi-hats",
        comment="Drill: 140–150 BPM, dark low melody, sliding 808 bass",
        expected_tempo_range=(135, 155),
        expected_track_count_range=(2, 5),
        expected_note_count_range=(60, 700),
        expected_duration_range=(20, 180),
        expected_pitch_range=(28, 65),
        expected_has_drums=True,
    ),

    # ── Funk / R&B / Soul ─────────────────────────────────────────────────────

    TestCase(
        test_id="tc_039",
        prompt="Funky groove with slap bass, tight drums and wah-wah guitar",
        comment="Funk: syncopated groove, 100–115 BPM, bass-driven, strong drums",
        expected_tempo_range=(95, 120),
        expected_track_count_range=(3, 6),
        expected_note_count_range=(100, 900),
        expected_duration_range=(30, 180),
        expected_has_drums=True,
    ),
    TestCase(
        test_id="tc_040",
        prompt="Neo-soul R&B with lush chord extensions and smooth vocal melody",
        comment="Neo-soul: mid-tempo, rich harmonics, smooth feel",
        expected_tempo_range=(80, 110),
        expected_track_count_range=(2, 5),
        expected_note_count_range=(80, 700),
        expected_duration_range=(30, 240),
        expected_has_drums=True,
    ),
    TestCase(
        test_id="tc_041",
        prompt="Classic soul ballad in the style of Motown with strings and horn section",
        comment="Motown soul: moderate tempo, strings + brass, emotional melody",
        expected_tempo_range=(70, 110),
        expected_track_count_range=(3, 7),
        expected_note_count_range=(100, 900),
        expected_duration_range=(30, 240),
        expected_has_drums=True,
    ),

    # ── Cinematic / Film Score ────────────────────────────────────────────────

    TestCase(
        test_id="tc_042",
        prompt="Epic cinematic orchestral trailer music with powerful brass fanfare",
        comment="Trailer music: fast brass, high energy, many tracks, high note count",
        expected_tempo_range=(100, 180),
        expected_track_count_range=(4, 10),
        expected_note_count_range=(200, 2000),
        expected_duration_range=(20, 180),
        expected_has_drums=True,
    ),
    TestCase(
        test_id="tc_043",
        prompt="Sad cinematic piano ballad with solo piano and subtle strings",
        comment="Sad score: slow, expressive piano, minimal instrumentation",
        expected_tempo_range=(50, 85),
        expected_track_count_range=(1, 3),
        expected_note_count_range=(60, 600),
        expected_duration_range=(30, 300),
        expected_has_drums=False,
    ),
    TestCase(
        test_id="tc_044",
        prompt="Tense thriller action sequence with staccato strings and pounding timpani",
        comment="Thriller score: fast staccato, high tension, drums/timpani present",
        expected_tempo_range=(120, 200),
        expected_track_count_range=(3, 8),
        expected_note_count_range=(150, 1500),
        expected_duration_range=(20, 180),
        expected_has_drums=True,
    ),
    TestCase(
        test_id="tc_045",
        prompt="Heroic fantasy adventure theme with bold brass, strings and choir",
        comment="Fantasy theme: epic, full orchestra, bright brass leads",
        expected_tempo_range=(90, 160),
        expected_track_count_range=(4, 10),
        expected_note_count_range=(200, 2000),
        expected_duration_range=(30, 240),
        expected_has_drums=True,
    ),
    TestCase(
        test_id="tc_046",
        prompt="Romantic film score with sweeping strings and delicate piano",
        comment="Romance score: slow sweeping strings, emotional piano, no drums",
        expected_tempo_range=(55, 90),
        expected_track_count_range=(2, 5),
        expected_note_count_range=(80, 700),
        expected_duration_range=(30, 300),
        expected_has_drums=False,
    ),

    # ── World Music ───────────────────────────────────────────────────────────

    TestCase(
        test_id="tc_047",
        prompt="Traditional Indian raga with sitar, tabla and tanpura drone",
        comment="Indian classical: drone bass, ornamental sitar melody, percussion",
        expected_tempo_range=(60, 150),
        expected_track_count_range=(2, 4),
        expected_note_count_range=(100, 1200),
        expected_duration_range=(30, 300),
        expected_has_drums=True,
    ),
    TestCase(
        test_id="tc_048",
        prompt="Flamenco guitar with passionate runs, rhythmic strumming and palmas",
        comment="Flamenco: fast runs, rhythmic accents, wide pitch span",
        expected_tempo_range=(90, 180),
        expected_track_count_range=(1, 3),
        expected_note_count_range=(150, 1500),
        expected_duration_range=(20, 180),
        expected_has_drums=True,
    ),
    TestCase(
        test_id="tc_049",
        prompt="African djembe drum circle with polyrhythmic percussion and chanting",
        comment="African percussion: multiple rhythmically offset drum patterns",
        expected_tempo_range=(100, 160),
        expected_track_count_range=(2, 6),
        expected_note_count_range=(100, 1500),
        expected_duration_range=(20, 180),
        expected_has_drums=True,
    ),
    TestCase(
        test_id="tc_050",
        prompt="Celtic folk with fiddle, tin whistle and bodhrán",
        comment="Celtic: fast jig/reel, high register melody, light percussion",
        expected_tempo_range=(120, 200),
        expected_track_count_range=(2, 4),
        expected_note_count_range=(150, 1200),
        expected_duration_range=(20, 180),
        expected_pitch_range=(55, 90),
        expected_has_drums=True,
    ),
    TestCase(
        test_id="tc_051",
        prompt="Japanese koto and shakuhachi meditation piece",
        comment="Japanese traditional: pentatonic scale, sparse notes, no drums",
        expected_tempo_range=(50, 90),
        expected_track_count_range=(1, 3),
        expected_note_count_range=(20, 300),
        expected_duration_range=(30, 240),
        expected_has_drums=False,
    ),

    # ── Country / Bluegrass ───────────────────────────────────────────────────

    TestCase(
        test_id="tc_052",
        prompt="Country waltz with acoustic guitar, fiddle and gentle steel guitar",
        comment="Country waltz: 3/4 feel, 80–100 BPM, acoustic instrumentation",
        expected_tempo_range=(75, 110),
        expected_track_count_range=(2, 5),
        expected_note_count_range=(80, 700),
        expected_duration_range=(30, 240),
        expected_has_drums=True,
    ),
    TestCase(
        test_id="tc_053",
        prompt="Bluegrass breakdown with fast banjo, mandolin and upright bass",
        comment="Bluegrass: very fast, intricate picking patterns, high note density",
        expected_tempo_range=(160, 240),
        expected_track_count_range=(3, 5),
        expected_note_count_range=(200, 1500),
        expected_duration_range=(20, 180),
        expected_has_drums=False,
    ),

    # ── Reggae / Ska / Dub ────────────────────────────────────────────────────

    TestCase(
        test_id="tc_054",
        prompt="Roots reggae with offbeat guitar skank, bassline and one-drop drumming",
        comment="Reggae: offbeat rhythm, 70–90 BPM, bass-prominent, one-drop pattern",
        expected_tempo_range=(68, 92),
        expected_track_count_range=(3, 5),
        expected_note_count_range=(80, 700),
        expected_duration_range=(30, 240),
        expected_has_drums=True,
    ),
    TestCase(
        test_id="tc_055",
        prompt="Dub music with heavy reverb, echo effects and sparse bass hits",
        comment="Dub: very sparse melodic content, pronounced bass, drums",
        expected_tempo_range=(65, 92),
        expected_track_count_range=(2, 5),
        expected_note_count_range=(20, 300),
        expected_duration_range=(30, 300),
        expected_has_drums=True,
    ),

    # ── Blues ─────────────────────────────────────────────────────────────────

    TestCase(
        test_id="tc_056",
        prompt="12-bar blues shuffle with electric guitar bends and harmonica",
        comment="Blues: 12-bar structure, swing feel, expressive bends",
        expected_tempo_range=(80, 130),
        expected_track_count_range=(2, 4),
        expected_note_count_range=(60, 600),
        expected_duration_range=(20, 180),
        expected_has_drums=True,
    ),
    TestCase(
        test_id="tc_057",
        prompt="Delta blues fingerpicking with raw slide guitar and sparse bass",
        comment="Delta blues: acoustic, solo or duo, slow tempo, pentatonic",
        expected_tempo_range=(60, 100),
        expected_track_count_range=(1, 3),
        expected_note_count_range=(30, 400),
        expected_duration_range=(20, 180),
        expected_has_drums=False,
    ),

    # ── Gospel / Church ───────────────────────────────────────────────────────

    TestCase(
        test_id="tc_058",
        prompt="Gospel choir with powerful organ, hand claps and uplifting vocal harmonies",
        comment="Gospel: moderate tempo, rich chord harmonics, call-and-response feel",
        expected_tempo_range=(75, 120),
        expected_track_count_range=(2, 6),
        expected_note_count_range=(100, 900),
        expected_duration_range=(30, 240),
        expected_has_drums=True,
    ),

    # ── Video Game Music ──────────────────────────────────────────────────────

    TestCase(
        test_id="tc_059",
        prompt="8-bit retro video game boss battle theme with fast arpeggios",
        comment="Chiptune: fast arp patterns, high-pitched square waves, drums",
        expected_tempo_range=(160, 240),
        expected_track_count_range=(2, 4),
        expected_note_count_range=(200, 2000),
        expected_duration_range=(15, 120),
        expected_pitch_range=(52, 95),
        expected_has_drums=True,
    ),
    TestCase(
        test_id="tc_060",
        prompt="Relaxing RPG village music with gentle harp and woodwind melodies",
        comment="Village theme: slow, pastoral, high register melody, no drums",
        expected_tempo_range=(70, 110),
        expected_track_count_range=(2, 4),
        expected_note_count_range=(60, 500),
        expected_duration_range=(20, 180),
        expected_has_drums=False,
    ),
    TestCase(
        test_id="tc_061",
        prompt="Intense action game level music with driving synths and heavy percussion",
        comment="Action game: fast, intense, full arrangement, drums",
        expected_tempo_range=(130, 190),
        expected_track_count_range=(3, 7),
        expected_note_count_range=(150, 1500),
        expected_duration_range=(20, 180),
        expected_has_drums=True,
    ),
    TestCase(
        test_id="tc_062",
        prompt="Mystery puzzle game music with ambient pad and sparse melodic hints",
        comment="Puzzle theme: slow, sparse, atmospheric, no drums",
        expected_tempo_range=(50, 90),
        expected_track_count_range=(1, 4),
        expected_note_count_range=(10, 200),
        expected_duration_range=(20, 240),
        expected_has_drums=False,
    ),

    # ── Children's / Nursery ──────────────────────────────────────────────────

    TestCase(
        test_id="tc_063",
        prompt="Happy children's nursery rhyme with glockenspiel and xylophone",
        comment="Children's: bright high tones, simple melody, happy tempo, no drums",
        expected_tempo_range=(90, 130),
        expected_track_count_range=(1, 3),
        expected_note_count_range=(40, 400),
        expected_duration_range=(15, 120),
        expected_pitch_range=(60, 96),
        expected_has_drums=False,
    ),

    # ── Wedding / Celebration ─────────────────────────────────────────────────

    TestCase(
        test_id="tc_064",
        prompt="Wedding march processional with pipe organ and brass",
        comment="Wedding march: stately 4/4, full organ, triumphant",
        expected_tempo_range=(70, 100),
        expected_track_count_range=(2, 5),
        expected_note_count_range=(80, 700),
        expected_duration_range=(20, 180),
        expected_has_drums=False,
    ),

    # ── Meditation / Healing ──────────────────────────────────────────────────

    TestCase(
        test_id="tc_065",
        prompt="432 Hz healing music for deep sleep with binaural undertones and soft piano",
        comment="Healing: very slow, minimal notes, low dynamics",
        expected_tempo_range=(40, 70),
        expected_track_count_range=(1, 3),
        expected_note_count_range=(5, 120),
        expected_duration_range=(30, 600),
        expected_has_drums=False,
    ),
    TestCase(
        test_id="tc_066",
        prompt="Tibetan singing bowl meditation with long sustains and gentle chimes",
        comment="Singing bowl: very sparse, no percussion, long note durations",
        expected_tempo_range=(40, 70),
        expected_track_count_range=(1, 3),
        expected_note_count_range=(2, 60),
        expected_duration_range=(30, 600),
        expected_has_drums=False,
    ),

    # ── Latin / Salsa ─────────────────────────────────────────────────────────

    TestCase(
        test_id="tc_067",
        prompt="Salsa tropical with brass section, clave rhythm and piano montuno",
        comment="Salsa: ~170 BPM, brass section, rhythmic piano montuno",
        expected_tempo_range=(150, 200),
        expected_track_count_range=(4, 8),
        expected_note_count_range=(200, 1800),
        expected_duration_range=(20, 180),
        expected_has_drums=True,
    ),
    TestCase(
        test_id="tc_068",
        prompt="Cumbia beat with accordion melody and rhythmic bass pattern",
        comment="Cumbia: 100–120 BPM, accordion lead, syncopated bass",
        expected_tempo_range=(95, 125),
        expected_track_count_range=(2, 5),
        expected_note_count_range=(100, 900),
        expected_duration_range=(20, 180),
        expected_has_drums=True,
    ),

    # ── Afrobeats ─────────────────────────────────────────────────────────────

    TestCase(
        test_id="tc_069",
        prompt="Afrobeats groove with talking drum, rhythmic guitar and bass",
        comment="Afrobeats: 100–120 BPM, rhythmic guitar, polyrhythmic percussion",
        expected_tempo_range=(95, 125),
        expected_track_count_range=(3, 6),
        expected_note_count_range=(100, 1000),
        expected_duration_range=(30, 180),
        expected_has_drums=True,
    ),

    # ── Marching Band ─────────────────────────────────────────────────────────

    TestCase(
        test_id="tc_070",
        prompt="Military marching band with snare drums, brass fanfare and cadence",
        comment="March: 100–130 BPM, strong snare beat, brass above mid-range",
        expected_tempo_range=(96, 135),
        expected_track_count_range=(3, 7),
        expected_note_count_range=(100, 1200),
        expected_duration_range=(20, 180),
        expected_has_drums=True,
    ),

    # ── Edge Cases ────────────────────────────────────────────────────────────

    TestCase(
        test_id="tc_071",
        prompt="Single note drone on C2 held for 60 seconds with soft filter sweep",
        comment="Extreme minimalism: almost no notes, long sustain, no drums",
        expected_tempo_range=(40, 120),
        expected_track_count_range=(1, 2),
        expected_note_count_range=(1, 30),
        expected_duration_range=(20, 120),
        expected_has_drums=False,
    ),
    TestCase(
        test_id="tc_072",
        prompt="Extremely fast technical death metal with 30-second blast beat",
        comment="Extreme tempo: >200 BPM, dense percussion, short duration",
        expected_tempo_range=(180, 300),
        expected_track_count_range=(2, 5),
        expected_note_count_range=(100, 2000),
        expected_duration_range=(10, 60),
        expected_has_drums=True,
    ),
    TestCase(
        test_id="tc_073",
        prompt="Abstract experimental noise music with random pitches and irregular rhythm",
        comment="Experimental: no specific tempo constraint, irregular, wide pitch",
        expected_track_count_range=(1, 6),
        expected_note_count_range=(10, 1500),
        expected_duration_range=(10, 300),
    ),
    TestCase(
        test_id="tc_074",
        prompt="A very long 5 minute ambient composition with slowly evolving tones",
        comment="Long duration test: should generate >180 second output",
        expected_tempo_range=(40, 90),
        expected_track_count_range=(1, 5),
        expected_note_count_range=(5, 400),
        expected_duration_range=(120, 600),
        expected_has_drums=False,
    ),

    # ── Mood / Emotion Tests ──────────────────────────────────────────────────

    TestCase(
        test_id="tc_075",
        prompt="Joyful and energetic celebration music with brass and percussion",
        comment="Joyful: bright timbre, fast tempo, high energy, upbeat rhythm",
        expected_tempo_range=(120, 180),
        expected_track_count_range=(3, 7),
        expected_note_count_range=(100, 1200),
        expected_duration_range=(20, 180),
        expected_has_drums=True,
    ),
    TestCase(
        test_id="tc_076",
        prompt="Deep melancholic sadness with slow minor piano and weeping strings",
        comment="Sad: minor key, slow, emotional piano + strings, no drums",
        expected_tempo_range=(45, 80),
        expected_track_count_range=(2, 4),
        expected_note_count_range=(50, 500),
        expected_duration_range=(30, 300),
        expected_has_drums=False,
    ),
    TestCase(
        test_id="tc_077",
        prompt="Angry aggressive industrial punk with distorted everything",
        comment="Angry: very fast, aggressive, maximum energy, drums",
        expected_tempo_range=(140, 220),
        expected_track_count_range=(2, 6),
        expected_note_count_range=(150, 2000),
        expected_duration_range=(15, 120),
        expected_has_drums=True,
    ),
    TestCase(
        test_id="tc_078",
        prompt="Nostalgic childhood memory piano solo with simple melody",
        comment="Nostalgic: simple diatonic melody, moderate slow tempo, piano only",
        expected_tempo_range=(60, 100),
        expected_track_count_range=(1, 2),
        expected_note_count_range=(30, 400),
        expected_duration_range=(20, 180),
        expected_has_drums=False,
    ),
    TestCase(
        test_id="tc_079",
        prompt="Romantic love theme with tender strings and gentle piano",
        comment="Romance: slow, lush harmonics, dynamics, no drums",
        expected_tempo_range=(55, 90),
        expected_track_count_range=(2, 4),
        expected_note_count_range=(50, 500),
        expected_duration_range=(30, 240),
        expected_has_drums=False,
    ),
    TestCase(
        test_id="tc_080",
        prompt="Eerie horror suspense with dissonant clusters and creeping tempo",
        comment="Horror: dissonant, slow, low pitches, building tension",
        expected_tempo_range=(40, 90),
        expected_track_count_range=(1, 5),
        expected_note_count_range=(10, 400),
        expected_duration_range=(20, 300),
        expected_pitch_range=(24, 62),
        expected_has_drums=False,
    ),
    TestCase(
        test_id="tc_081",
        prompt="Triumphant victory fanfare with full brass and percussion",
        comment="Victory fanfare: short, loud, high-register brass, drums",
        expected_tempo_range=(110, 160),
        expected_track_count_range=(3, 7),
        expected_note_count_range=(30, 400),
        expected_duration_range=(5, 60),
        expected_has_drums=True,
    ),
    TestCase(
        test_id="tc_082",
        prompt="Tense suspense underscoring for a thriller scene, strings only",
        comment="Suspense: string tremolo, slow/medium tempo, quiet, no drums",
        expected_tempo_range=(50, 100),
        expected_track_count_range=(2, 5),
        expected_note_count_range=(30, 600),
        expected_duration_range=(20, 300),
        expected_has_drums=False,
    ),

    # ── Instrument-Focused Tests ──────────────────────────────────────────────

    TestCase(
        test_id="tc_083",
        prompt="Solo acoustic guitar fingerstyle piece with gentle arpeggios",
        comment="Solo guitar: moderate tempo, single-instrument, rich note density",
        expected_tempo_range=(60, 110),
        expected_track_count_range=(1, 2),
        expected_note_count_range=(80, 800),
        expected_duration_range=(20, 240),
        expected_has_drums=False,
    ),
    TestCase(
        test_id="tc_084",
        prompt="Bass guitar solo with slaps, pops and melodic runs",
        comment="Bass solo: low pitch register, rhythmic, expressive dynamics",
        expected_tempo_range=(80, 140),
        expected_track_count_range=(1, 2),
        expected_note_count_range=(60, 600),
        expected_duration_range=(15, 120),
        expected_pitch_range=(28, 55),
        expected_has_drums=False,
    ),
    TestCase(
        test_id="tc_085",
        prompt="Drum solo with complex polyrhythmic patterns and fills",
        comment="Pure drums: all rhythm, channel 9 heavy, high note count",
        expected_tempo_range=(80, 180),
        expected_track_count_range=(1, 3),
        expected_note_count_range=(100, 1500),
        expected_duration_range=(15, 180),
        expected_has_drums=True,
    ),
    TestCase(
        test_id="tc_086",
        prompt="Trumpet jazz solo with bebop runs and blues inflections",
        comment="Trumpet solo: high-register, fast runs, blues scale",
        expected_tempo_range=(120, 250),
        expected_track_count_range=(1, 3),
        expected_note_count_range=(80, 800),
        expected_duration_range=(15, 120),
        expected_pitch_range=(55, 90),
        expected_has_drums=False,
    ),

    # ── Different Time Signatures ─────────────────────────────────────────────

    TestCase(
        test_id="tc_087",
        prompt="Waltz in 3/4 time with piano and strings",
        comment="3/4 waltz: characteristic 1-2-3 feel, moderate tempo",
        expected_tempo_range=(120, 200),
        expected_track_count_range=(2, 4),
        expected_note_count_range=(60, 700),
        expected_duration_range=(20, 180),
        expected_has_drums=False,
    ),
    TestCase(
        test_id="tc_088",
        prompt="7/8 progressive rock riff with asymmetric rhythm and electric guitar",
        comment="Odd time: complex syncopation, guitar-based, prog rock feel",
        expected_tempo_range=(100, 160),
        expected_track_count_range=(2, 5),
        expected_note_count_range=(80, 800),
        expected_duration_range=(20, 180),
        expected_has_drums=True,
    ),
    TestCase(
        test_id="tc_089",
        prompt="5/4 jazz with swinging feel like Take Five",
        comment="5/4 jazz: syncopated, moderate tempo, piano + bass + drums",
        expected_tempo_range=(140, 200),
        expected_track_count_range=(2, 4),
        expected_note_count_range=(100, 800),
        expected_duration_range=(20, 180),
        expected_has_drums=True,
    ),

    # ── Specific Instrumentation Tests ───────────────────────────────────────

    TestCase(
        test_id="tc_090",
        prompt="Full big band jazz with 4 horns, rhythm section and piano comp",
        comment="Big band: 5+ tracks, full arrangement, bright brass",
        expected_tempo_range=(120, 220),
        expected_track_count_range=(4, 10),
        expected_note_count_range=(200, 2000),
        expected_duration_range=(30, 300),
        expected_has_drums=True,
    ),
    TestCase(
        test_id="tc_091",
        prompt="Piano duet four hands with interlocking busy lines",
        comment="Piano duet: 2 piano tracks, high density, wide pitch range",
        expected_tempo_range=(80, 160),
        expected_track_count_range=(2, 3),
        expected_note_count_range=(200, 1500),
        expected_duration_range=(20, 240),
        expected_has_drums=False,
    ),
    TestCase(
        test_id="tc_092",
        prompt="Harp solo with flowing glissandos and delicate arpeggios",
        comment="Harp: high register, flowing arpeggios, no drums, gentle dynamics",
        expected_tempo_range=(60, 110),
        expected_track_count_range=(1, 2),
        expected_note_count_range=(80, 700),
        expected_duration_range=(20, 180),
        expected_pitch_range=(45, 90),
        expected_has_drums=False,
    ),

    # ── Production Style Tests ────────────────────────────────────────────────

    TestCase(
        test_id="tc_093",
        prompt="Minimalist piano with only 4 notes looping for 60 seconds",
        comment="Extreme minimalism: very low note count, looping pattern",
        expected_tempo_range=(60, 120),
        expected_track_count_range=(1, 2),
        expected_note_count_range=(4, 80),
        expected_duration_range=(20, 120),
        expected_has_drums=False,
    ),
    TestCase(
        test_id="tc_094",
        prompt="Dense maximalist orchestral texture with every section playing simultaneously",
        comment="Maximalist: maximum track count, very high note density",
        expected_track_count_range=(5, 15),
        expected_note_count_range=(500, 5000),
        expected_duration_range=(20, 300),
    ),
    TestCase(
        test_id="tc_095",
        prompt="Slow jazz quartet with swing at 80 BPM and space between notes",
        comment="Specific tempo: verifies tempo rendering close to 80 BPM",
        expected_tempo_range=(72, 90),
        expected_track_count_range=(2, 5),
        expected_note_count_range=(40, 500),
        expected_duration_range=(20, 240),
        expected_has_drums=True,
    ),

    # ── Cross-Genre / Fusion ──────────────────────────────────────────────────

    TestCase(
        test_id="tc_096",
        prompt="Jazz-hop fusion with hip-hop drums and bebop piano improvisation",
        comment="Jazz-hop: hybrid genre, 80–100 BPM, jazz piano + hip-hop drums",
        expected_tempo_range=(78, 105),
        expected_track_count_range=(3, 5),
        expected_note_count_range=(80, 800),
        expected_duration_range=(20, 180),
        expected_has_drums=True,
    ),
    TestCase(
        test_id="tc_097",
        prompt="Classical piano meets electronic with arpeggiated synths and glitchy percussion",
        comment="Classical-electronic fusion: structured melody + electronic beats",
        expected_tempo_range=(100, 145),
        expected_track_count_range=(3, 6),
        expected_note_count_range=(100, 1200),
        expected_duration_range=(20, 180),
        expected_has_drums=True,
    ),
    TestCase(
        test_id="tc_098",
        prompt="Flamenco-electronic crossover with sample guitar and 4-on-the-floor kick",
        comment="Flamenco + electronic: mixed time feel, guitar + electronic kick",
        expected_tempo_range=(110, 140),
        expected_track_count_range=(2, 5),
        expected_note_count_range=(100, 1000),
        expected_duration_range=(20, 180),
        expected_has_drums=True,
    ),

    # ── Seasonal / Contextual ─────────────────────────────────────────────────

    TestCase(
        test_id="tc_099",
        prompt="Christmas carol arrangement with jingle bells, sleigh bells and choir",
        comment="Christmas: recognisable festive timbre, moderate tempo, bright",
        expected_tempo_range=(100, 150),
        expected_track_count_range=(2, 6),
        expected_note_count_range=(60, 700),
        expected_duration_range=(20, 180),
        expected_has_drums=True,
    ),
    TestCase(
        test_id="tc_100",
        prompt="Spooky Halloween music with pipe organ, creaking sounds and distant bells",
        comment="Halloween: dark, slow, dissonant harmony, no drums",
        expected_tempo_range=(50, 100),
        expected_track_count_range=(1, 4),
        expected_note_count_range=(20, 400),
        expected_duration_range=(20, 240),
        expected_pitch_range=(28, 70),
        expected_has_drums=False,
    ),

    # ── More Genre Variations (101–110) ───────────────────────────────────────

    TestCase(
        test_id="tc_101",
        prompt="Bossa nova guitar and bass with soft brushed percussion",
        comment="Bossa nova: gentle swing, 100–130 BPM, guitar-bass duo",
        expected_tempo_range=(98, 132),
        expected_track_count_range=(2, 4),
        expected_note_count_range=(60, 600),
        expected_duration_range=(20, 240),
        expected_has_drums=True,
    ),
    TestCase(
        test_id="tc_102",
        prompt="90s RnB slow jam with lush chord stabs and soulful melody",
        comment="90s RnB: 75–95 BPM, rich chords, smooth melody",
        expected_tempo_range=(72, 98),
        expected_track_count_range=(2, 5),
        expected_note_count_range=(60, 600),
        expected_duration_range=(20, 240),
        expected_has_drums=True,
    ),
    TestCase(
        test_id="tc_103",
        prompt="Hardstyle electronic with reverse bassline and distorted kick at 150 BPM",
        comment="Hardstyle: 145–155 BPM, prominent kick, distorted bass",
        expected_tempo_range=(143, 158),
        expected_track_count_range=(2, 5),
        expected_note_count_range=(100, 1200),
        expected_duration_range=(20, 300),
        expected_has_drums=True,
    ),
    TestCase(
        test_id="tc_104",
        prompt="Smooth jazz with muted trumpet, electric piano and bossa groove",
        comment="Smooth jazz: 90–120 BPM, laid back, electric piano, light percussion",
        expected_tempo_range=(88, 122),
        expected_track_count_range=(2, 5),
        expected_note_count_range=(80, 700),
        expected_duration_range=(20, 240),
        expected_has_drums=True,
    ),
    TestCase(
        test_id="tc_105",
        prompt="Orchestral minimalism with slow string ostinato and held brass chord",
        comment="Minimalist orchestra: sparse, string repetition, low note ratio",
        expected_tempo_range=(60, 110),
        expected_track_count_range=(2, 5),
        expected_note_count_range=(30, 400),
        expected_duration_range=(30, 300),
        expected_has_drums=False,
    ),
    TestCase(
        test_id="tc_106",
        prompt="Neoclassical piano with introspective melody and arpeggiated left hand",
        comment="Neoclassical: Satie-inspired, delicate, 65–90 BPM, no drums",
        expected_tempo_range=(60, 95),
        expected_track_count_range=(1, 2),
        expected_note_count_range=(80, 700),
        expected_duration_range=(20, 300),
        expected_has_drums=False,
    ),
    TestCase(
        test_id="tc_107",
        prompt="Phonk trap with dark Memphis sample, distorted 808 and trap hi-hats",
        comment="Phonk: dark trap, 130–145 BPM, very low 808, aggressive hats",
        expected_tempo_range=(128, 148),
        expected_track_count_range=(2, 5),
        expected_note_count_range=(60, 800),
        expected_duration_range=(20, 180),
        expected_pitch_range=(24, 62),
        expected_has_drums=True,
    ),
    TestCase(
        test_id="tc_108",
        prompt="Hyperpop with glitchy stutters, pitch-shifted vocals and 168 BPM",
        comment="Hyperpop: very fast, chaotic, high-pitched elements",
        expected_tempo_range=(158, 178),
        expected_track_count_range=(2, 6),
        expected_note_count_range=(100, 1500),
        expected_duration_range=(15, 180),
        expected_has_drums=True,
    ),
    TestCase(
        test_id="tc_109",
        prompt="New age music with crystal bowls, gentle harp and nature sounds",
        comment="New age: very slow, high-register delicate tones, no drums",
        expected_tempo_range=(40, 75),
        expected_track_count_range=(1, 3),
        expected_note_count_range=(5, 150),
        expected_duration_range=(30, 600),
        expected_has_drums=False,
    ),
    TestCase(
        test_id="tc_110",
        prompt="Energetic workout music with driving 130 BPM beat and motivating synth",
        comment="Workout: 125–138 BPM, energetic, driving rhythm, full arrangement",
        expected_tempo_range=(123, 140),
        expected_track_count_range=(3, 7),
        expected_note_count_range=(150, 1500),
        expected_duration_range=(30, 300),
        expected_has_drums=True,
    ),
]
