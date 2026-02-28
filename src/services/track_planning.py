# -*- coding: utf-8 -*-
"""
Track Planning Service
======================

Shared, genre-aware track planning logic used by both the LangGraph
agent node (``src.agents.track_planner_node``) and the standalone
``TrackPlanner`` class (``src.app.track_planner``).

Merges the best features of both prior implementations:
- AI-based planning via LLM (with JSON parsing + code-fence stripping)
- Rule-based fallback with keyword-driven track-count inference
- Track-count extraction from natural language ("four tracks")
- Genre-aware fill pools (ambient, cinematic, default)
- Emotion-aware instrument enhancement (when mapper is available)
"""

from __future__ import annotations

import json
import re
import logging
from typing import List, Optional

from src.agents.state import MusicIntent, TrackConfig
from src.config.llm import LLMConfig, call_llm

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Optional emotion-aware instrument mapper
# ---------------------------------------------------------------------------

try:
    from src.analysis.emotion_instruments import EmotionAwareInstrumentMapper
    _EMOTION_MAPPER_AVAILABLE = True
except ImportError:
    _EMOTION_MAPPER_AVAILABLE = False

# ---------------------------------------------------------------------------
# Genre-aware fill pools (used when adding tracks to match requested count)
# ---------------------------------------------------------------------------

_GENRE_FILL: dict[str, list[tuple[str, str, str]]] = {
    "ambient": [
        ("pad", "synth_pad", "Atmospheric pad"),
        ("lead", "bells", "Melodic bells"),
        ("harmony", "strings", "Harmonic strings"),
        ("harmony", "piano", "Harmonic keys"),
        ("pad", "choir", "Choir pad"),
        ("lead", "harp", "Melodic harp"),
        ("lead", "synth_lead", "Synth melody"),
        ("fx", "fx_atmosphere", "Atmosphere FX"),
    ],
    "cinematic": [
        ("harmony", "strings", "String ensemble"),
        ("lead", "brass", "Brass melody"),
        ("drums", "timpani", "Timpani rhythm"),
        ("harmony", "piano", "Piano harmony"),
        ("pad", "choir", "Choir pad"),
        ("lead", "french_horn", "French horn"),
        ("bass", "electric_bass", "Deep bass"),
        ("fx", "fx_atmosphere", "Cinematic FX"),
    ],
}

_DEFAULT_FILL: list[tuple[str, str, str]] = [
    ("harmony", "electric_piano", "Harmonic support"),
    ("bass", "bass", "Bass line"),
    ("drums", "drums", "Rhythm section"),
    ("arpeggio", "synth_lead", "Arpeggio"),
    ("pad", "synth_pad", "Atmosphere"),
    ("counter_melody", "flute", "Counter melody"),
    ("fx", "fx_atmosphere", "Effects"),
    ("lead", "piano", "Melody"),
]

_BASE_TRACKS: list[tuple[str, str, str]] = [
    ("lead", "piano", "Main melody"),
    ("harmony", "electric_piano", "Harmonic support"),
    ("bass", "bass", "Bass line"),
    ("drums", "drums", "Rhythm section"),
    ("arpeggio", "synth_lead", "Arpeggio pattern"),
    ("pad", "synth_pad", "Atmospheric pad"),
    ("counter_melody", "flute", "Counter melody"),
    ("fx", "fx_atmosphere", "Sound effects"),
]

_RHYTHMIC_GENRES = frozenset({
    "lofi", "rock", "funk", "pop", "rnb", "electronic", "hip hop", "hiphop",
})


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def extract_track_count(text: str) -> Optional[int]:
    """Extract an explicit track-count from a natural-language prompt.

    Supports both digit and word forms ("4 tracks", "four tracks").
    """
    _NUMBER_WORDS = {
        "one": 1, "two": 2, "three": 3, "four": 4,
        "five": 5, "six": 6, "seven": 7, "eight": 8,
    }
    patterns = [
        r"(\d+)\s*tracks?",
        r"(one|two|three|four|five|six|seven|eight)\s*tracks?",
    ]
    text_lower = text.lower()
    for pattern in patterns:
        match = re.search(pattern, text_lower)
        if match:
            value = match.group(1)
            return int(value) if value.isdigit() else _NUMBER_WORDS.get(value)
    return None


def plan_tracks_with_ai(
    intent: MusicIntent,
    *,
    raw_prompt: str = "",
    requested_count: Optional[int] = None,
) -> List[TrackConfig]:
    """AI-based track planning via configured LLM.

    Falls back to :func:`plan_tracks_with_rules` when the LLM call
    fails or returns unparsable output.
    """
    tc = requested_count or intent.track_count
    track_count_req = (
        f"\n**CRITICAL**: User requested EXACTLY {tc} tracks."
        if tc else ""
    )

    system_prompt = (
        "You are a music producer planning track arrangements.\n"
        "Analyze the user request and return ONLY valid JSON:\n"
        "{\n"
        '  "tracks": [\n'
        '    {"type": "<lead|counter_melody|harmony|bass|drums|arpeggio|pad|fx>",\n'
        '      "instrument": "<instrument>",\n'
        '      "role": "<description>",\n'
        '      "priority": <1-8>}\n'
        "  ]\n"
        "}\n"
        "Rules:\n"
        "- Return exactly the number of tracks requested (or infer from description)\n"
        "- Match instruments to genre\n"
        "- Prioritize coherent arrangement\n"
        "- Never exceed 8 tracks"
        f"{track_count_req}"
    )

    prompt = raw_prompt or intent.raw_prompt
    user_message = f"Genre: {intent.genre}, Request: {prompt}"

    try:
        result_text = call_llm(system_prompt, user_message, temperature=0.3, max_tokens=500)
        if not result_text:
            return plan_tracks_with_rules(intent, raw_prompt=prompt, requested_count=tc)

        if "```" in result_text:
            result_text = result_text.split("```")[1].replace("json", "").strip()

        data = json.loads(result_text)
        tracks = [
            TrackConfig(
                track_type=t.get("type", "lead"),
                instrument=t.get("instrument", "piano"),
                role=t.get("role", ""),
                priority=t.get("priority", i + 1),
                channel=i if t.get("type") != "drums" else 9,
            )
            for i, t in enumerate(data.get("tracks", [])[:8])
        ]
        return tracks if tracks else plan_tracks_with_rules(intent, raw_prompt=prompt, requested_count=tc)

    except Exception as exc:
        logger.warning("AI track planning failed: %s — using rules", exc)
        return plan_tracks_with_rules(intent, raw_prompt=prompt, requested_count=tc)


def plan_tracks_with_rules(
    intent: MusicIntent,
    *,
    raw_prompt: str = "",
    requested_count: Optional[int] = None,
) -> List[TrackConfig]:
    """Deterministic, rule-based track planning fallback.

    Handles explicit counts, solo/simple/rich keywords, and genre defaults.
    """
    prompt = (raw_prompt or intent.raw_prompt).lower()
    specific_instruments = intent.specific_instruments or []

    tc = requested_count or intent.track_count
    if tc is not None:
        # Explicit count — fill from base tracks
        tracks = []
        for i in range(min(tc, 8)):
            track_type, instrument, role = _BASE_TRACKS[i % len(_BASE_TRACKS)]
            tracks.append(TrackConfig(
                track_type=track_type,
                instrument=instrument,
                role=role,
                priority=i + 1,
                channel=i if track_type != "drums" else 9,
            ))
        return tracks

    # Keyword-driven sizing
    is_simple = any(w in prompt for w in ("solo", "simple", "minimal", "just", "only"))
    is_rich = any(w in prompt for w in ("epic", "orchestral", "full", "rich", "complex", "cinematic"))
    needs_drums = any(
        kw in " ".join(specific_instruments).lower()
        for kw in ("drums", "percussion", "beat", "drum")
    ) or intent.genre in _RHYTHMIC_GENRES

    if is_simple:
        instrument = "piano"
        for kw, inst in [("guitar", "guitar"), ("string", "strings"), ("synth", "synth_lead")]:
            if kw in prompt:
                instrument = inst
                break
        tracks = [TrackConfig("lead", instrument, "Main melody", 1, 0)]
        if not any(w in prompt for w in ("solo", "just", "only")):
            tracks.append(TrackConfig("harmony", "electric_piano", "Light harmony", 2, 1))
    elif is_rich:
        tracks = [
            TrackConfig("lead", "strings", "Main melody", 1, 0),
            TrackConfig("counter_melody", "flute", "Counter line", 2, 1),
            TrackConfig("harmony", "synth_pad", "Harmonic bed", 3, 2),
            TrackConfig("pad", "choir", "Atmosphere", 4, 3),
            TrackConfig("bass", "synth_bass", "Low end", 5, 4),
            TrackConfig("drums", "drums", "Rhythm", 6, 9),
            TrackConfig("arpeggio", "piano", "Movement", 7, 5),
        ]
    else:
        # Standard arrangement — infer count from energy/mood
        count = infer_track_count(intent.energy, intent.mood)
        tracks = []
        for i in range(min(count, len(_BASE_TRACKS))):
            track_type, instrument, role = _BASE_TRACKS[i]
            tracks.append(TrackConfig(
                track_type=track_type,
                instrument=instrument,
                role=role,
                priority=i + 1,
                channel=i if track_type != "drums" else 9,
            ))

    # Guarantee drums for rhythmic genres / explicit requests
    if needs_drums and not any(t.track_type == "drums" for t in tracks):
        tracks.append(TrackConfig(
            track_type="drums",
            instrument="drums",
            role="Rhythm section",
            priority=len(tracks) + 1,
            channel=9,
        ))

    return tracks


def enhance_with_emotion_instruments(
    base_tracks: List[TrackConfig],
    genre: str,
    emotions: List[str],
    style_descriptors: List[str],
    specific_instruments: Optional[List[str]] = None,
) -> List[TrackConfig]:
    """Layer emotion-aware instrument selection on top of a base plan.

    No-op when the emotion mapper is unavailable or raises.
    """
    if not base_tracks or not _EMOTION_MAPPER_AVAILABLE:
        return base_tracks

    try:
        emotion_instruments = EmotionAwareInstrumentMapper.select_instruments_for_intent(
            genre=genre,
            emotions=emotions,
            style_descriptors=style_descriptors,
            track_count=len(base_tracks),
            specific_instruments=specific_instruments,
        )
        enhanced = []
        for i, base in enumerate(base_tracks):
            if i < len(emotion_instruments):
                ei = emotion_instruments[i]
                enhanced.append(TrackConfig(
                    track_type=ei.get("track_type", base.track_type),
                    instrument=ei.get("instrument", base.instrument),
                    role=f"{base.role} ({ei.get('instrument', 'unknown')})",
                    priority=ei.get("priority", base.priority),
                    channel=ei.get("channel", base.channel),
                ))
            else:
                enhanced.append(base)
        logger.info("Enhanced tracks with emotion-aware instruments")
        return enhanced
    except Exception as exc:
        logger.warning("Emotion instrument mapping failed: %s — using base tracks", exc)
        return base_tracks


def ensure_track_count(
    tracks: List[TrackConfig],
    requested: int,
    genre: str,
) -> List[TrackConfig]:
    """Adjust *tracks* to exactly *requested* length.

    Adds genre-aware filler tracks or trims by lowest priority.
    """
    requested = min(requested, 16)  # MIDI channel limit
    if len(tracks) == requested:
        return tracks

    if len(tracks) < requested:
        fill_pool = _GENRE_FILL.get(genre, _DEFAULT_FILL)
        existing_instruments = {t.instrument for t in tracks}
        current = len(tracks)

        # First pass — unique instruments
        for track_type, instrument, role in fill_pool:
            if current >= requested:
                break
            if instrument not in existing_instruments:
                tracks.append(TrackConfig(
                    track_type=track_type,
                    instrument=instrument,
                    role=role,
                    priority=current + 1,
                    channel=current if track_type != "drums" else 9,
                ))
                existing_instruments.add(instrument)
                current += 1

        # Second pass — duplicate instruments with suffix
        idx = 0
        while current < requested and idx < 16:
            track_type, instrument, role = fill_pool[idx % len(fill_pool)]
            tracks.append(TrackConfig(
                track_type=track_type,
                instrument=instrument,
                role=f"{role} #{current + 1}",
                priority=current + 1,
                channel=current if track_type != "drums" else 9,
            ))
            current += 1
            idx += 1
    else:
        tracks = sorted(tracks, key=lambda t: t.priority)[:requested]

    return tracks


def infer_track_count(energy: str, mood: str) -> int:
    """Infer a reasonable track count from energy level and mood keywords."""
    energy_map = {"low": 2, "medium": 4, "high": 6}
    base = energy_map.get(energy, 4)

    if any(kw in mood.lower() for kw in ("epic", "orchestral")):
        return min(base + 2, 8)
    if any(kw in mood.lower() for kw in ("simple", "solo")):
        return max(base - 2, 1)
    return base
