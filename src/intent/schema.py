# -*- coding: utf-8 -*-
"""
Pydantic v2 schema for structured LLM intent output.

Every field the LLM must produce is defined here with types, constraints,
defaults, and musical-coherence validators.  This file is the single source
of truth — the JSON schema exported from these models is embedded verbatim
in the system prompt so the LLM knows exactly what to return.
"""

from __future__ import annotations

import logging
from typing import List, Literal, Optional

from pydantic import BaseModel, Field, field_validator, model_validator

from src.config.genre_registry import (
    get_genre_ids_for_validation,
    get_tempo_ranges,
    SCALES_EXTENDED,
    SCALE_ALIASES,
    find_by_alias,
)

logger = logging.getLogger(__name__)

# ---- Supported values (dynamically built from genre_registry) ----------

SUPPORTED_GENRES: tuple[str, ...] = get_genre_ids_for_validation()

SUPPORTED_SCALES: tuple[str, ...] = tuple(sorted(SCALES_EXTENDED.keys()))

SUPPORTED_ACTIONS = ("new", "extend", "modify", "analyze")

ENERGY_LEVELS = ("very_low", "low", "medium", "high", "very_high")

DYNAMICS_LEVELS = ("minimal", "gentle", "moderate", "strong", "powerful")

# Genre → typical BPM range (dynamically from genre_registry)
GENRE_TEMPO_RANGES: dict[str, tuple[int, int]] = get_tempo_ranges()


# ---- Sub-models ----------------------------------------------------------

class GenreInfo(BaseModel):
    """Primary and secondary genre classification.

    Accepts any genre ID from the registry (e.g. 'pop', 'electronic.house',
    'african.afrobeat').  Aliases are resolved automatically.
    """
    primary: str = Field(
        default="pop",
        description="Genre ID from registry (e.g. 'pop', 'jazz.bebop', 'electronic.house').",
    )
    secondary: Optional[str] = Field(
        default=None,
        description="Optional secondary genre ID.",
    )
    confidence: float = Field(ge=0.0, le=1.0, default=0.8)

    @field_validator("primary", "secondary", mode="before")
    @classmethod
    def resolve_genre_alias(cls, v: Optional[str]) -> Optional[str]:
        """Resolve genre aliases and validate against registry."""
        if v is None:
            return None
        v_lower = v.strip().lower().replace("-", "_").replace(" ", "_")
        # Direct match
        if v_lower in SUPPORTED_GENRES:
            return v_lower
        # Alias lookup
        node = find_by_alias(v)
        if node is not None:
            return node.id
        # Root match (e.g. "house" → check all sub-genres)
        for gid in SUPPORTED_GENRES:
            parts = gid.split(".")
            if len(parts) > 1 and parts[-1] == v_lower:
                return gid
        # Fall back to pop for unknown genres (with warning)
        logger.warning("Unknown genre '%s', falling back to 'pop'.", v)
        return "pop"


class MoodInfo(BaseModel):
    """Mood / emotional content."""
    primary: str = Field(description="Main mood descriptor (e.g. 'melancholic', 'euphoric')")
    secondary: Optional[str] = None
    valence: float = Field(
        ge=-1.0, le=1.0, default=0.0,
        description="Emotional valence: -1 negative … +1 positive",
    )
    confidence: float = Field(ge=0.0, le=1.0, default=0.7)


class EnergyInfo(BaseModel):
    """Energy / intensity level."""
    level: Literal["very_low", "low", "medium", "high", "very_high"] = "medium"
    confidence: float = Field(ge=0.0, le=1.0, default=0.7)


class TempoInfo(BaseModel):
    """Tempo specification."""
    bpm: int = Field(ge=30, le=300, default=120)
    source: Literal["explicit", "inferred", "genre_default"] = "genre_default"
    confidence: float = Field(ge=0.0, le=1.0, default=0.5)


class KeyInfo(BaseModel):
    """Key and scale information."""
    root: Optional[str] = Field(
        default=None,
        description="Root note: C, C#, Db, D, … B",
    )
    scale: str = Field(
        default="major",
        description="Scale name from registry (e.g. 'major', 'dorian', 'hijaz', 'raga_bhairav').",
    )
    confidence: float = Field(ge=0.0, le=1.0, default=0.5)


class DurationInfo(BaseModel):
    """Duration specification."""
    bars: Optional[int] = Field(ge=4, le=512, default=None)
    seconds: Optional[int] = Field(ge=5, le=3600, default=None)
    descriptor: Optional[Literal["short", "medium", "long", "very_long"]] = None
    confidence: float = Field(ge=0.0, le=1.0, default=0.5)


class TrackChannelInfo(BaseModel):
    """Explicit track count and channel count requested by the user.

    These are separate from the instruments list because a user may say
    "5 tracks" without naming all 5 instruments, or "8 channels" to request
    a wider MIDI channel spread.
    """
    track_count: Optional[int] = Field(
        ge=1, le=16, default=None,
        description="Number of tracks explicitly requested (e.g. '5 tracks').",
    )
    channel_count: Optional[int] = Field(
        ge=1, le=16, default=None,
        description="Number of MIDI channels explicitly requested (e.g. '8 channels').",
    )
    confidence: float = Field(ge=0.0, le=1.0, default=0.5)


class InstrumentRequest(BaseModel):
    """A requested instrument with role and priority."""
    name: str = Field(description="Instrument name (e.g. 'piano', 'synth_pad')")
    role: Literal["melody", "harmony", "bass", "rhythm", "pad", "lead", "arpeggio", "fx"] = "harmony"
    priority: int = Field(ge=1, le=10, default=5)


class DynamicsInfo(BaseModel):
    """Dynamics / expressiveness."""
    intensity: Literal["minimal", "gentle", "moderate", "strong", "powerful"] = "moderate"
    arc: Literal["flat", "build", "decay", "wave", "dynamic"] = "flat"


class StructureInfo(BaseModel):
    """High-level song structure."""
    has_intro: bool = True
    has_verse: bool = True
    has_chorus: bool = True
    has_bridge: bool = False
    has_outro: bool = True
    form_hint: Optional[str] = Field(
        default=None,
        description="Freeform structure hint, e.g. 'ABAB', 'through-composed'",
    )


class ProductionStyle(BaseModel):
    """Production / sonic character."""
    descriptors: List[str] = Field(
        default_factory=list,
        description="Style tags, e.g. ['reverb-heavy', 'lo-fi', 'distorted']",
    )
    complexity: Literal["simple", "moderate", "rich", "very_complex"] = "moderate"


class ReferenceInfo(BaseModel):
    """Artist / song reference the user mentioned."""
    artist: Optional[str] = None
    song: Optional[str] = None
    description: Optional[str] = Field(
        default=None,
        description="How the reference should influence the output",
    )


# ---- Top-level output model -----------------------------------------------

class ParsedIntent(BaseModel):
    """
    Complete structured intent extracted from a user prompt.

    The LLM must return JSON conforming to this schema.  Every field has a
    sensible default so partial extraction still succeeds.
    """

    # ---- Chain-of-thought reasoning (LLM fills this first) ----
    reasoning: str = Field(
        default="",
        description=(
            "Step-by-step reasoning the LLM performed before committing to "
            "parameter values.  Not used downstream — purely for transparency."
        ),
    )

    # ---- Core fields ----
    action: Literal["new", "extend", "modify", "analyze"] = "new"
    genre: GenreInfo = Field(default_factory=lambda: GenreInfo(primary="pop"))
    mood: MoodInfo = Field(default_factory=lambda: MoodInfo(primary="neutral"))
    energy: EnergyInfo = Field(default_factory=EnergyInfo)
    tempo: TempoInfo = Field(default_factory=TempoInfo)
    key: KeyInfo = Field(default_factory=KeyInfo)
    duration: DurationInfo = Field(default_factory=DurationInfo)

    # ---- Track / Channel count (explicit user request) ----
    track_channel: TrackChannelInfo = Field(default_factory=TrackChannelInfo)

    # ---- Instruments ----
    instruments: List[InstrumentRequest] = Field(default_factory=list)

    # ---- Musical character ----
    dynamics: DynamicsInfo = Field(default_factory=DynamicsInfo)
    structure: StructureInfo = Field(default_factory=StructureInfo)
    production: ProductionStyle = Field(default_factory=ProductionStyle)

    # ---- Optional reference ----
    reference: Optional[ReferenceInfo] = None

    # ---- Confidence (overall) ----
    overall_confidence: float = Field(
        ge=0.0, le=1.0, default=0.7,
        description="How confident the model is in the full extraction (0–1).",
    )

    # ==================================================================
    # Musical-coherence validators
    # ==================================================================

    @model_validator(mode="after")
    def validate_tempo_genre_coherence(self) -> "ParsedIntent":
        """Warn (but don't reject) if tempo falls outside the genre's typical range."""
        genre_key = self.genre.primary
        tempo_range = GENRE_TEMPO_RANGES.get(genre_key)
        if tempo_range and self.tempo.source != "explicit":
            lo, hi = tempo_range
            if self.tempo.bpm < lo or self.tempo.bpm > hi:
                logger.warning(
                    "Tempo %d BPM outside typical range for '%s' (%d–%d). "
                    "Clamping to genre range.",
                    self.tempo.bpm, genre_key, lo, hi,
                )
                self.tempo.bpm = max(lo, min(hi, self.tempo.bpm))
        return self

    @model_validator(mode="after")
    def validate_energy_dynamics_alignment(self) -> "ParsedIntent":
        """If energy is very_low/low, dynamics intensity should not be 'powerful'."""
        if self.energy.level in ("very_low", "low") and self.dynamics.intensity == "powerful":
            logger.warning(
                "Energy '%s' conflicts with dynamics intensity 'powerful'. "
                "Downgrading dynamics to 'moderate'.",
                self.energy.level,
            )
            self.dynamics.intensity = "moderate"
        return self

    @model_validator(mode="after")
    def validate_duration_bars_seconds_coherence(self) -> "ParsedIntent":
        """Cross-check bars ↔ seconds when both are provided."""
        d = self.duration
        if d.bars is not None and d.seconds is not None and self.tempo.bpm:
            expected_seconds = (d.bars * 4 / self.tempo.bpm) * 60
            ratio = d.seconds / expected_seconds if expected_seconds else 0
            if ratio < 0.5 or ratio > 2.0:
                # Major mismatch — trust seconds, recalculate bars
                new_bars = max(4, round((d.seconds * self.tempo.bpm) / (4 * 60)))
                logger.warning(
                    "Duration mismatch: %d bars ≈ %.0fs but user said %ds. "
                    "Recalculating bars → %d.",
                    d.bars, expected_seconds, d.seconds, new_bars,
                )
                d.bars = new_bars
        return self

    @model_validator(mode="after")
    def validate_instrument_role_uniqueness(self) -> "ParsedIntent":
        """Warn and de-duplicate when two instruments share the same role.

        Roles 'harmony' and 'pad' are exempted since layering is common.
        """
        if not self.instruments:
            return self
        exempt_roles = {"harmony", "pad"}
        seen: dict[str, str] = {}  # role → first instrument name
        deduped: list = []
        for inst in self.instruments:
            if inst.role in exempt_roles or inst.role not in seen:
                seen[inst.role] = inst.name
                deduped.append(inst)
            else:
                logger.warning(
                    "Duplicate role '%s': '%s' conflicts with '%s'. "
                    "Keeping first, dropping duplicate.",
                    inst.role, inst.name, seen[inst.role],
                )
        self.instruments = deduped
        return self

    @model_validator(mode="after")
    def validate_key_scale_coherence(self) -> "ParsedIntent":
        """Ensure the scale value is in SUPPORTED_SCALES or is a known alias.

        If the LLM returns an unsupported scale, fall back to 'major'.
        """
        scale = self.key.scale
        # Check direct match
        if scale in SCALES_EXTENDED:
            return self
        # Check aliases
        canonical = SCALE_ALIASES.get(scale)
        if canonical:
            self.key.scale = canonical
            return self
        # Normalize: try lowercase/underscore
        normalized = scale.strip().lower().replace("-", "_").replace(" ", "_")
        if normalized in SCALES_EXTENDED:
            self.key.scale = normalized
            return self
        canonical = SCALE_ALIASES.get(normalized)
        if canonical:
            self.key.scale = canonical
            return self
        logger.warning(
            "Scale '%s' not in supported scales. Falling back to 'major'.",
            scale,
        )
        self.key.scale = "major"
        return self


# ---- Utility: produce a JSON-schema string for embedding in prompts -----

def get_intent_json_schema() -> str:
    """Return the JSON schema for ParsedIntent as a compact string.

    Used by prompt_templates to embed the expected output format directly
    into the system prompt so the LLM knows the exact structure to produce.
    """
    import json
    schema = ParsedIntent.model_json_schema()
    return json.dumps(schema, indent=2)
