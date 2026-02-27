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

from pydantic import BaseModel, Field, model_validator

logger = logging.getLogger(__name__)

# ---- Supported values (kept in sync with src/app/constants.py) ----------

SUPPORTED_GENRES = (
    "pop", "rock", "electronic", "lofi", "jazz",
    "classical", "ambient", "cinematic", "funk", "rnb",
)

SUPPORTED_SCALES = (
    "major", "minor", "dorian", "mixolydian",
    "pentatonic_major", "pentatonic_minor", "blues", "harmonic_minor",
)

SUPPORTED_ACTIONS = ("new", "extend", "modify", "analyze")

ENERGY_LEVELS = ("very_low", "low", "medium", "high", "very_high")

DYNAMICS_LEVELS = ("minimal", "gentle", "moderate", "strong", "powerful")

# Genre → typical BPM range (from GENRE_CONFIG)
GENRE_TEMPO_RANGES: dict[str, tuple[int, int]] = {
    "pop": (100, 130),
    "rock": (110, 140),
    "electronic": (120, 135),
    "lofi": (70, 90),
    "jazz": (80, 140),
    "classical": (60, 120),
    "ambient": (60, 80),
    "cinematic": (70, 100),
    "funk": (95, 115),
    "rnb": (70, 100),
}


# ---- Sub-models ----------------------------------------------------------

class GenreInfo(BaseModel):
    """Primary and secondary genre classification."""
    primary: Literal[
        "pop", "rock", "electronic", "lofi", "jazz",
        "classical", "ambient", "cinematic", "funk", "rnb",
    ]
    secondary: Optional[Literal[
        "pop", "rock", "electronic", "lofi", "jazz",
        "classical", "ambient", "cinematic", "funk", "rnb",
    ]] = None
    confidence: float = Field(ge=0.0, le=1.0, default=0.8)


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
    scale: Literal[
        "major", "minor", "dorian", "mixolydian",
        "pentatonic_major", "pentatonic_minor", "blues", "harmonic_minor",
    ] = "major"
    confidence: float = Field(ge=0.0, le=1.0, default=0.5)


class DurationInfo(BaseModel):
    """Duration specification."""
    bars: Optional[int] = Field(ge=4, le=512, default=None)
    seconds: Optional[int] = Field(ge=5, le=3600, default=None)
    descriptor: Optional[Literal["short", "medium", "long", "very_long"]] = None
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
        """Ensure the scale value is in SUPPORTED_SCALES.

        If the LLM returns an unsupported scale, fall back to 'major'.
        """
        if self.key.scale not in SUPPORTED_SCALES:
            logger.warning(
                "Scale '%s' not in supported scales. Falling back to 'major'.",
                self.key.scale,
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
