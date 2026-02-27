# -*- coding: utf-8 -*-
"""
LLM Intent Engine — Unified, high-accuracy musical intent parser.

Orchestrates the full pipeline:
  PreProcessor → LLM call (chain-of-thought) → Pydantic validation
  → correction loop → enrichment → EnhancedMusicIntent output

Replaces three legacy parsers:
  - src/midigent/advanced_intent_parser.py  (regex-only, no LLM)
  - src/app/intent_parser.py               (weak 15-line prompt)
  - src/agents/intent_parser_node.py        (_parse_intent_basic keyword scan)
"""

from __future__ import annotations

import json
import logging
import math
from typing import Any, Dict, List, Optional

from pydantic import ValidationError

from src.config.llm import LLMConfig, call_llm
from src.intent.preprocessor import PreprocessedInput, preprocess
from src.intent.prompt_templates import (
    CORRECTION_PROMPT_TEMPLATE,
    build_system_prompt,
)
from src.intent.schema import (
    GENRE_TEMPO_RANGES,
    ParsedIntent,
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Compatibility bridge to the legacy EnhancedMusicIntent / MusicIntent types
# used downstream by the agentic graph.
# ---------------------------------------------------------------------------

def _intent_to_enhanced(parsed: ParsedIntent, raw_prompt: str) -> Any:
    """Convert a validated ParsedIntent to the legacy EnhancedMusicIntent dataclass.

    This bridges the new schema to the existing agentic graph that expects
    ``EnhancedMusicIntent`` and ``CompositionStructure`` from
    ``src.midigent.advanced_intent_parser``.
    """
    from src.midigent.advanced_intent_parser import (
        CompositionComplexity,
        CompositionStructure,
        EnhancedMusicIntent,
    )

    # Map complexity string → enum
    _complexity_map = {
        "simple": CompositionComplexity.SIMPLE,
        "moderate": CompositionComplexity.MODERATE,
        "rich": CompositionComplexity.RICH,
        "very_complex": CompositionComplexity.VERY_COMPLEX,
    }

    # Determine bars and tempo
    tempo = parsed.tempo.bpm or 120
    bars = parsed.duration.bars
    seconds = parsed.duration.seconds

    if bars is None and seconds is not None:
        bars = max(4, math.ceil((seconds * tempo) / (4 * 60)))
    elif bars is None:
        bars = 32  # sensible default

    if seconds is None and bars is not None:
        seconds = int((bars * 4 / tempo) * 60)

    # Build composition structure
    structure = _build_composition_structure(bars, tempo, parsed)

    # Map dynamics
    dynamics_map = {
        "minimal": "minimal",
        "gentle": "minimal",
        "moderate": "moderate",
        "strong": "dramatic",
        "powerful": "dramatic",
    }

    enhanced = EnhancedMusicIntent(
        action=parsed.action,
        genre=parsed.genre.primary,
        mood=parsed.mood.primary,
        energy=parsed.energy.level,
        duration_seconds=seconds,
        duration_bars=bars,
        specific_instruments=[inst.name for inst in parsed.instruments],
        instrument_priorities={inst.name: inst.priority for inst in parsed.instruments},
        style_descriptors=parsed.production.descriptors,
        emotions=[parsed.mood.primary] + ([parsed.mood.secondary] if parsed.mood.secondary else []),
        dynamics=dynamics_map.get(parsed.dynamics.intensity, "moderate"),
        tempo_preference=tempo,
        key_preference=parsed.key.root,
        complexity=_complexity_map.get(parsed.production.complexity, CompositionComplexity.MODERATE),
        composition_structure=structure,
        reasoning=[parsed.reasoning] if parsed.reasoning else [],
        raw_prompt=raw_prompt,
    )
    return enhanced


def _build_composition_structure(
    total_bars: int, tempo: int, parsed: ParsedIntent
) -> Any:
    """Build a CompositionStructure from a ParsedIntent."""
    from src.midigent.advanced_intent_parser import CompositionStructure, CompositionComplexity

    _complexity_map = {
        "simple": CompositionComplexity.SIMPLE,
        "moderate": CompositionComplexity.MODERATE,
        "rich": CompositionComplexity.RICH,
        "very_complex": CompositionComplexity.VERY_COMPLEX,
    }

    s = parsed.structure

    # Calculate section lengths proportionally
    sections_present = sum([s.has_intro, s.has_verse, s.has_chorus, s.has_bridge, s.has_outro])
    if sections_present == 0:
        sections_present = 1  # at least verse

    # Proportional weights
    weights = {
        "intro": 1.0 if s.has_intro else 0,
        "verse": 2.0 if s.has_verse else 0,
        "chorus": 2.0 if s.has_chorus else 0,
        "bridge": 1.0 if s.has_bridge else 0,
        "outro": 1.0 if s.has_outro else 0,
    }
    total_weight = sum(weights.values()) or 1.0
    scale_factor = total_bars / total_weight

    # Round to nearest multiple of 4 (musical phrasing)
    def round_to_4(n: float) -> int:
        return max(4, int(round(n / 4)) * 4)

    intro_bars = round_to_4(weights["intro"] * scale_factor) if s.has_intro else 0
    verse_bars = round_to_4(weights["verse"] * scale_factor) if s.has_verse else 0
    chorus_bars = round_to_4(weights["chorus"] * scale_factor) if s.has_chorus else 0
    bridge_bars = round_to_4(weights["bridge"] * scale_factor) if s.has_bridge else 0
    outro_bars = round_to_4(weights["outro"] * scale_factor) if s.has_outro else 0

    # Adjust total to match requested bars
    allocated = intro_bars + verse_bars + chorus_bars + bridge_bars + outro_bars
    if allocated != total_bars and verse_bars > 0:
        diff = total_bars - allocated
        verse_bars = max(4, verse_bars + diff)

    # Determine energy arc
    arc_map = {
        "flat": "smooth",
        "build": "build",
        "decay": "decay",
        "wave": "dynamic",
        "dynamic": "dynamic",
    }

    key_scale = parsed.key.scale or "major"

    return CompositionStructure(
        total_bars=total_bars,
        tempo=tempo,
        time_signature="4/4",
        intro_bars=intro_bars,
        verse_bars=verse_bars,
        chorus_bars=chorus_bars,
        bridge_bars=bridge_bars,
        outro_bars=outro_bars,
        main_scale=key_scale,
        complexity=_complexity_map.get(parsed.production.complexity, CompositionComplexity.MODERATE),
        primary_styles=[],
        energy_arc=arc_map.get(parsed.dynamics.arc, "smooth"),
        intro_density=0.3 if parsed.energy.level in ("very_low", "low") else 0.5,
    )


def _intent_to_music_intent(parsed: ParsedIntent, raw_prompt: str) -> Any:
    """Convert a validated ParsedIntent to the legacy MusicIntent dataclass.

    Used by the agentic graph's MusicState['intent'] field.
    """
    from src.agents.state import MusicIntent

    return MusicIntent(
        action=parsed.action,
        genre=parsed.genre.primary,
        mood=parsed.mood.primary,
        energy=parsed.energy.level,
        track_count=len(parsed.instruments) if parsed.instruments else None,
        duration_requested=parsed.duration.bars,
        specific_instruments=[inst.name for inst in parsed.instruments],
        style_descriptors=parsed.production.descriptors,
        tempo_preference=parsed.tempo.bpm,
        key_preference=parsed.key.root,
        raw_prompt=raw_prompt,
    )


# ---------------------------------------------------------------------------
# Fallback keyword parser (no LLM)
# ---------------------------------------------------------------------------

def _fallback_keyword_parse(text: str, preprocessed: PreprocessedInput) -> ParsedIntent:
    """Enhanced keyword-based fallback when no LLM provider is available.

    Consolidates the best logic from all three legacy parsers into one
    deterministic function. Returns a ParsedIntent with low confidence values.
    """
    from src.intent.schema import (
        DurationInfo,
        DynamicsInfo,
        EnergyInfo,
        GenreInfo,
        InstrumentRequest,
        KeyInfo,
        MoodInfo,
        ParsedIntent,
        ProductionStyle,
        StructureInfo,
        TempoInfo,
    )

    text_lower = text.lower()
    ext = preprocessed.extracted

    # ---- Contextual inference for common scenarios ----
    # These handle vague prompts like "music for studying" that have no
    # explicit genre keywords but strong contextual signals.
    _CONTEXT_RULES: list[tuple[list[str], str, str, str]] = [
        # (keywords, inferred_genre, inferred_mood, inferred_energy)
        (["study", "studying", "homework", "reading", "focus", "concentration"], "lofi", "calm", "low"),
        (["workout", "exercise", "gym", "running", "training"], "electronic", "energetic", "high"),
        (["sleep", "sleeping", "bedtime", "lullaby", "rest"], "ambient", "peaceful", "very_low"),
        (["meditat", "yoga", "mindful", "zen", "breathing"], "ambient", "calm", "low"),
        (["party", "dance", "club", "rave"], "electronic", "energetic", "high"),
        (["wedding", "ceremony"], "classical", "romantic", "medium"),
        (["horror", "scary", "creepy", "spooky", "halloween"], "cinematic", "dark", "medium"),
        (["film", "movie", "trailer", "scene", "score"], "cinematic", "epic", "high"),
        (["game", "gaming", "video game", "boss fight"], "electronic", "intense", "high"),
        (["coffee", "cafe", "morning", "brunch"], "jazz", "warm", "medium"),
        (["driving", "road trip", "highway"], "rock", "energetic", "high"),
        (["sunset", "beach", "ocean", "waves"], "ambient", "peaceful", "low"),
        (["rain", "storm", "thunder"], "ambient", "melancholic", "low"),
        (["night", "late night", "midnight", "nocturnal"], "lofi", "contemplative", "low"),
    ]

    context_genre = None
    context_mood = None
    context_energy = None
    for keywords, c_genre, c_mood, c_energy in _CONTEXT_RULES:
        if any(kw in text_lower for kw in keywords):
            context_genre = c_genre
            context_mood = c_mood
            context_energy = c_energy
            break

    # ---- Genre detection (ordered by specificity) ----
    genre = "pop"
    genre_keywords = {
        "lo-fi": "lofi", "lofi": "lofi", "lo fi": "lofi",
        "ambient": "ambient", "cinematic": "cinematic",
        "classical": "classical", "orchestral": "classical",
        "jazz": "jazz", "swing": "jazz",
        "electronic": "electronic", "edm": "electronic", "techno": "electronic",
        "drum and bass": "electronic",
        "funk": "funk", "funky": "funk",
        "r&b": "rnb", "rnb": "rnb", "soul": "rnb",
        "rock": "rock", "metal": "rock", "punk": "rock",
        "pop": "pop",
    }
    genre_found = False
    for kw, g in genre_keywords.items():
        if kw in text_lower:
            genre = g
            genre_found = True
            break

    # Fall back to contextual genre if no explicit genre keyword matched
    if not genre_found and context_genre:
        genre = context_genre

    # ---- Mood ----
    mood = "neutral"
    mood_keywords = {
        "happy": "happy", "joyful": "happy", "upbeat": "upbeat",
        "sad": "sad", "melancholic": "melancholic", "sorrowful": "sad",
        "dark": "dark", "gloomy": "dark", "brooding": "dark",
        "calm": "calm", "peaceful": "peaceful", "serene": "calm",
        "epic": "epic", "grand": "epic", "majestic": "epic",
        "energetic": "energetic", "intense": "intense", "aggressive": "aggressive",
        "dreamy": "dreamy", "ethereal": "ethereal", "atmospheric": "ethereal",
        "mysterious": "mysterious", "eerie": "mysterious",
        "romantic": "romantic", "tender": "romantic",
        "chill": "chill", "relaxing": "relaxing",
    }
    mood_found = False
    for kw, m in mood_keywords.items():
        if kw in text_lower:
            mood = m
            mood_found = True
            break

    # Fall back to contextual mood
    if not mood_found and context_mood:
        mood = context_mood

    # ---- Energy ----
    energy = "medium"
    if any(w in text_lower for w in ("intense", "energetic", "powerful", "hard", "aggressive", "heavy", "fast")):
        energy = "high"
    elif any(w in text_lower for w in ("chill", "calm", "peaceful", "ambient", "gentle", "soft", "slow", "quiet")):
        energy = "low"
    elif context_energy:
        energy = context_energy

    # ---- Tempo ----
    tempo_bpm = ext.tempo_bpm
    tempo_source = "explicit" if tempo_bpm else "genre_default"
    if not tempo_bpm:
        genre_range = GENRE_TEMPO_RANGES.get(genre, (100, 130))
        tempo_bpm = (genre_range[0] + genre_range[1]) // 2

    # ---- Key ----
    import re as _re
    key_root = None
    key_scale = "major"
    key_match = _re.search(r"\b([A-G][#b]?)\s*(major|minor|m(?:in)?|dorian|blues)?\b", text, _re.IGNORECASE)
    if key_match:
        key_root = key_match.group(1).upper().replace("B", "b" if key_match.group(1)[-1] == "b" else "B")
        if key_match.group(1).endswith("b") and len(key_match.group(1)) == 2:
            key_root = key_match.group(1)[0].upper() + "b"
        else:
            key_root = key_match.group(1).upper()
        mode = (key_match.group(2) or "").lower()
        if mode in ("minor", "m", "min"):
            key_scale = "minor"
        elif mode == "dorian":
            key_scale = "dorian"
        elif mode == "blues":
            key_scale = "blues"

    # ---- Duration ----
    bars = ext.duration_bars
    seconds = ext.duration_seconds
    if bars is None and seconds is not None:
        bars = max(4, math.ceil((seconds * tempo_bpm) / (4 * 60)))
    elif bars is None:
        bars = 32

    # ---- Instruments ----
    instruments: list[InstrumentRequest] = []
    instrument_scan = {
        "piano": ("piano", "harmony"),
        "guitar": ("acoustic_guitar", "melody"),
        "electric guitar": ("electric_guitar", "melody"),
        "bass": ("electric_bass", "bass"),
        "drums": ("drums", "rhythm"),
        "strings": ("strings", "harmony"),
        "violin": ("violin", "melody"),
        "cello": ("cello", "harmony"),
        "trumpet": ("trumpet", "lead"),
        "saxophone": ("saxophone", "lead"),
        "sax": ("saxophone", "lead"),
        "flute": ("flute", "melody"),
        "organ": ("organ", "harmony"),
        "synth": ("synth_pad", "pad"),
        "pad": ("synth_pad", "pad"),
        "choir": ("choir", "harmony"),
    }
    for kw, (name, role) in instrument_scan.items():
        if kw in text_lower:
            instruments.append(InstrumentRequest(name=name, role=role, priority=7))

    return ParsedIntent(
        reasoning="[Keyword fallback — no LLM available]",
        action="new",
        genre=GenreInfo(primary=genre, confidence=0.5),
        mood=MoodInfo(primary=mood, confidence=0.4),
        energy=EnergyInfo(level=energy, confidence=0.5),
        tempo=TempoInfo(bpm=tempo_bpm, source=tempo_source, confidence=0.4 if tempo_source == "genre_default" else 0.9),
        key=KeyInfo(root=key_root, scale=key_scale, confidence=0.3 if not key_root else 0.8),
        duration=DurationInfo(bars=bars, seconds=seconds, confidence=0.4),
        instruments=instruments,
        dynamics=DynamicsInfo(intensity="moderate", arc="flat"),
        structure=StructureInfo(),
        production=ProductionStyle(complexity="moderate"),
        overall_confidence=0.4,
    )


# ---------------------------------------------------------------------------
# Main Engine
# ---------------------------------------------------------------------------

class LLMIntentEngine:
    """Unified LLM-based intent parsing engine.

    Usage::

        engine = LLMIntentEngine()
        parsed, enhanced, music_intent = engine.parse("epic cinematic in D minor")

    The engine returns:
      - ``ParsedIntent``: fully validated Pydantic model (new schema)
      - ``EnhancedMusicIntent``: legacy dataclass for backward compat
      - ``MusicIntent``: legacy dataclass for MusicState["intent"]
    """

    # LLM call parameters (tuned per research: near-deterministic for extraction)
    TEMPERATURE = 0.1
    MAX_TOKENS = 1500
    MAX_RETRIES = 1

    def parse(
        self,
        user_prompt: str,
        session_context: dict | None = None,
        provider: str | None = None,
    ) -> tuple[ParsedIntent, Any, Any]:
        """Parse a user prompt into a validated ParsedIntent + legacy types.

        Args:
            user_prompt: Raw user input text.
            session_context: Optional dict for modification context (genre, key, etc.).
            provider: Override LLM provider.

        Returns:
            Tuple of (ParsedIntent, EnhancedMusicIntent, MusicIntent).
        """
        # Stage 1: Preprocess
        preprocessed = preprocess(user_prompt)
        logger.info("[IntentEngine] Preprocessed: %s", preprocessed.normalized[:120])

        # Stage 2 + 3: LLM call → validation (with fallback)
        parsed = self._try_llm_parse(preprocessed, session_context, provider)

        if parsed is None:
            # All LLM attempts failed — fall back to keyword parsing
            logger.warning("[IntentEngine] LLM parsing failed. Using keyword fallback.")
            parsed = _fallback_keyword_parse(preprocessed.normalized, preprocessed)

        # Stage 5: Enrich and apply preprocessor-extracted hard numbers
        parsed = self._apply_hard_numbers(parsed, preprocessed)

        # Stage 6: Genre-aware default enrichment for low-confidence fields
        parsed = self._enrich_defaults(parsed)

        # Bridge to legacy types
        enhanced = _intent_to_enhanced(parsed, user_prompt)
        music_intent = _intent_to_music_intent(parsed, user_prompt)

        return parsed, enhanced, music_intent

    # ------------------------------------------------------------------
    # Internal stages
    # ------------------------------------------------------------------

    def _try_llm_parse(
        self,
        preprocessed: PreprocessedInput,
        session_context: dict | None,
        provider: str | None,
    ) -> Optional[ParsedIntent]:
        """Attempt LLM-based parsing with one retry on validation failure."""
        if not LLMConfig.AVAILABLE_PROVIDERS:
            logger.warning("[IntentEngine] No LLM providers configured.")
            return None

        system_prompt = build_system_prompt(session_context)

        # First attempt
        raw_json = self._call_llm(system_prompt, preprocessed.enriched_prompt, provider)
        if raw_json is None:
            return None

        parsed, error = self._validate_json(raw_json)
        if parsed is not None:
            return parsed

        # Retry once with error feedback
        if self.MAX_RETRIES > 0:
            logger.info("[IntentEngine] Validation failed (%s). Retrying with error context.", error)
            correction_msg = CORRECTION_PROMPT_TEMPLATE.format(error_message=error)
            combined_prompt = f"{preprocessed.enriched_prompt}\n\n{correction_msg}"

            raw_json_retry = self._call_llm(system_prompt, combined_prompt, provider)
            if raw_json_retry is not None:
                parsed_retry, error_retry = self._validate_json(raw_json_retry)
                if parsed_retry is not None:
                    return parsed_retry
                logger.warning("[IntentEngine] Retry also failed: %s", error_retry)

        return None

    def _call_llm(
        self, system_prompt: str, user_message: str, provider: str | None
    ) -> Optional[str]:
        """Call the LLM and return raw response text."""
        try:
            result = call_llm(
                system_prompt=system_prompt,
                user_message=user_message,
                provider=provider,
                temperature=self.TEMPERATURE,
                max_tokens=self.MAX_TOKENS,
            )
            return result
        except Exception as exc:
            logger.error("[IntentEngine] LLM call exception: %s", exc)
            return None

    def _validate_json(self, raw: str) -> tuple[Optional[ParsedIntent], Optional[str]]:
        """Parse raw LLM output to JSON and validate against the Pydantic schema.

        Returns (ParsedIntent, None) on success or (None, error_string) on failure.
        """
        # Strip markdown fences if present
        text = raw.strip()
        if text.startswith("```"):
            # Remove ```json ... ``` wrapper
            lines = text.split("\n")
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            text = "\n".join(lines)

        try:
            data = json.loads(text)
        except json.JSONDecodeError as exc:
            return None, f"JSON parse error: {exc}"

        try:
            parsed = ParsedIntent.model_validate(data)
            return parsed, None
        except ValidationError as exc:
            return None, str(exc)

    def _apply_hard_numbers(
        self, parsed: ParsedIntent, preprocessed: PreprocessedInput
    ) -> ParsedIntent:
        """Override LLM-inferred values with deterministically extracted hard numbers.

        Explicit numbers from the user always win over LLM inference.
        """
        ext = preprocessed.extracted

        if ext.tempo_bpm is not None:
            parsed.tempo.bpm = ext.tempo_bpm
            parsed.tempo.source = "explicit"
            parsed.tempo.confidence = max(parsed.tempo.confidence, 0.95)

        if ext.duration_bars is not None:
            parsed.duration.bars = ext.duration_bars
            parsed.duration.confidence = max(parsed.duration.confidence, 0.9)

        if ext.duration_seconds is not None:
            parsed.duration.seconds = ext.duration_seconds
            parsed.duration.confidence = max(parsed.duration.confidence, 0.9)

        # Cross-check: if seconds set but bars not, calculate bars
        if parsed.duration.seconds and parsed.duration.bars is None:
            bpm = parsed.tempo.bpm or 120
            parsed.duration.bars = max(4, math.ceil((parsed.duration.seconds * bpm) / (4 * 60)))

        return parsed

    def _enrich_defaults(self, parsed: ParsedIntent) -> ParsedIntent:
        """Fill genre-aware defaults for fields the LLM or fallback left empty.

        When instruments list is empty (common with vague prompts), populate it
        with genre-typical instruments.  When key root is None, use the genre's
        default root.
        """
        from src.intent.schema import InstrumentRequest, GENRE_TEMPO_RANGES

        # Genre → typical default instruments (name, role, priority)
        _GENRE_INSTRUMENTS: dict[str, list[tuple[str, str, int]]] = {
            "pop":        [("piano", "harmony", 7), ("electric_guitar", "melody", 8), ("electric_bass", "bass", 8), ("drums", "rhythm", 9)],
            "rock":       [("electric_guitar", "lead", 9), ("electric_guitar", "harmony", 7), ("electric_bass", "bass", 8), ("drums", "rhythm", 9)],
            "electronic": [("synth_lead", "lead", 8), ("synth_pad", "pad", 7), ("synth_bass", "bass", 8), ("drums", "rhythm", 9), ("arpeggiator", "arpeggio", 6)],
            "lofi":       [("piano", "melody", 8), ("electric_bass", "bass", 7), ("drums", "rhythm", 8), ("synth_pad", "pad", 6)],
            "jazz":       [("piano", "harmony", 8), ("fretless_bass", "bass", 8), ("drums", "rhythm", 8), ("saxophone", "melody", 9)],
            "classical":  [("strings", "harmony", 9), ("piano", "melody", 8), ("cello", "bass", 7), ("flute", "melody", 6)],
            "ambient":    [("synth_pad", "pad", 9), ("strings", "harmony", 7), ("piano", "melody", 5)],
            "cinematic":  [("strings", "harmony", 9), ("brass", "lead", 8), ("drums", "rhythm", 7), ("piano", "melody", 6), ("choir", "pad", 5)],
            "funk":       [("electric_guitar", "melody", 9), ("electric_bass", "bass", 9), ("drums", "rhythm", 9), ("organ", "harmony", 7), ("brass", "lead", 6)],
            "rnb":        [("piano", "harmony", 8), ("electric_bass", "bass", 8), ("drums", "rhythm", 8), ("synth_pad", "pad", 6), ("vocals", "melody", 9)],
        }

        # Genre → default key root
        _GENRE_DEFAULT_KEY: dict[str, str] = {
            "pop": "C", "rock": "E", "electronic": "A", "lofi": "D",
            "jazz": "F", "classical": "G", "ambient": "C", "cinematic": "D",
            "funk": "E", "rnb": "Ab",
        }

        genre = parsed.genre.primary

        # Enrich empty instruments list
        if not parsed.instruments:
            defaults = _GENRE_INSTRUMENTS.get(genre, _GENRE_INSTRUMENTS["pop"])
            parsed.instruments = [
                InstrumentRequest(name=name, role=role, priority=prio)
                for name, role, prio in defaults
            ]
            logger.info(
                "[IntentEngine] Enriched empty instruments with %d genre defaults for '%s'.",
                len(parsed.instruments), genre,
            )

        # Enrich missing key root
        if parsed.key.root is None and parsed.key.confidence < 0.5:
            parsed.key.root = _GENRE_DEFAULT_KEY.get(genre, "C")
            logger.info(
                "[IntentEngine] Enriched missing key root → '%s' (genre default for '%s').",
                parsed.key.root, genre,
            )

        return parsed
