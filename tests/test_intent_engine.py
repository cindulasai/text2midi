# -*- coding: utf-8 -*-
"""
Test suite for the LLM Intent Parsing Engine.

Covers:
  - Pydantic schema validation (ParsedIntent, sub-models)
  - Musical coherence validators
  - Preprocessor (normalization, abbreviation expansion, hard-number extraction)
  - Keyword fallback parser
  - Engine integration (mock LLM for deterministic testing)

Run with: pytest tests/test_intent_engine.py -v
"""

import json
import math
from unittest.mock import patch

import pytest

from src.intent.preprocessor import (
    ExtractedNumbers,
    PreprocessedInput,
    expand_abbreviations,
    extract_hard_numbers,
    normalize_text,
    preprocess,
)
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
from src.intent.engine import LLMIntentEngine, _fallback_keyword_parse


# =====================================================================
# SECTION 1: Schema Validation Tests
# =====================================================================


class TestParsedIntentSchema:
    """Verify that the Pydantic schema accepts valid data and rejects invalid data."""

    def test_minimal_valid_intent(self):
        """Parsing the absolute minimum should succeed with defaults."""
        intent = ParsedIntent()
        assert intent.action == "new"
        assert intent.genre.primary == "pop"
        assert intent.energy.level == "medium"
        assert intent.overall_confidence == 0.7

    def test_full_valid_intent(self):
        """Complete JSON with all fields should parse correctly."""
        data = {
            "reasoning": "Test reasoning",
            "action": "new",
            "genre": {"primary": "jazz", "secondary": "funk", "confidence": 0.9},
            "mood": {"primary": "groovy", "secondary": "warm", "valence": 0.4, "confidence": 0.8},
            "energy": {"level": "medium", "confidence": 0.85},
            "tempo": {"bpm": 120, "source": "explicit", "confidence": 0.99},
            "key": {"root": "Bb", "scale": "dorian", "confidence": 0.9},
            "duration": {"bars": 48, "seconds": 96, "descriptor": "medium", "confidence": 0.9},
            "instruments": [
                {"name": "piano", "role": "harmony", "priority": 8},
                {"name": "drums", "role": "rhythm", "priority": 9},
            ],
            "dynamics": {"intensity": "moderate", "arc": "wave"},
            "structure": {
                "has_intro": True,
                "has_verse": True,
                "has_chorus": False,
                "has_bridge": True,
                "has_outro": True,
                "form_hint": "AABA",
            },
            "production": {"descriptors": ["swing-feel", "acoustic"], "complexity": "rich"},
            "reference": None,
            "overall_confidence": 0.92,
        }
        intent = ParsedIntent.model_validate(data)
        assert intent.genre.primary == "jazz"
        assert intent.tempo.bpm == 120
        assert intent.key.root == "Bb"
        assert len(intent.instruments) == 2

    def test_invalid_genre_rejected(self):
        """An unsupported genre value should fail validation."""
        with pytest.raises(Exception):
            ParsedIntent.model_validate({
                "genre": {"primary": "dubstep", "confidence": 0.9},
            })

    def test_invalid_energy_rejected(self):
        """An unsupported energy level should fail validation."""
        with pytest.raises(Exception):
            ParsedIntent.model_validate({
                "energy": {"level": "extreme", "confidence": 0.5},
            })

    def test_tempo_out_of_range(self):
        """BPM below 30 or above 300 should fail validation."""
        with pytest.raises(Exception):
            ParsedIntent.model_validate({
                "tempo": {"bpm": 5, "source": "explicit", "confidence": 0.9},
            })

    def test_confidence_out_of_range(self):
        """Confidence > 1.0 should fail validation."""
        with pytest.raises(Exception):
            ParsedIntent.model_validate({"overall_confidence": 1.5})


class TestMusicalCoherenceValidators:
    """Test the @model_validator coherence checks."""

    def test_ambient_tempo_clamped_when_inferred(self):
        """Ambient genre with inferred tempo > 80 should be clamped."""
        intent = ParsedIntent.model_validate({
            "genre": {"primary": "ambient", "confidence": 0.9},
            "tempo": {"bpm": 140, "source": "inferred", "confidence": 0.5},
        })
        # Ambient range is 60-80
        assert intent.tempo.bpm <= 80

    def test_explicit_tempo_not_clamped(self):
        """Explicit tempo should NOT be clamped even if outside genre range."""
        intent = ParsedIntent.model_validate({
            "genre": {"primary": "ambient", "confidence": 0.9},
            "tempo": {"bpm": 160, "source": "explicit", "confidence": 0.99},
        })
        assert intent.tempo.bpm == 160

    def test_low_energy_powerful_dynamics_downgraded(self):
        """Low energy + powerful dynamics should be corrected."""
        intent = ParsedIntent.model_validate({
            "energy": {"level": "low", "confidence": 0.8},
            "dynamics": {"intensity": "powerful", "arc": "flat"},
        })
        assert intent.dynamics.intensity != "powerful"

    def test_duration_bars_seconds_mismatch_corrected(self):
        """Major bars/seconds mismatch should auto-correct bars."""
        intent = ParsedIntent.model_validate({
            "tempo": {"bpm": 120, "source": "explicit", "confidence": 0.9},
            "duration": {"bars": 16, "seconds": 300, "confidence": 0.8},
        })
        # 300s at 120 BPM ≈ 150 bars, not 16 → bars should be recalculated
        assert intent.duration.bars > 16


# =====================================================================
# SECTION 2: Preprocessor Tests
# =====================================================================


class TestNormalization:

    def test_collapse_whitespace(self):
        assert normalize_text("  hello   world  ") == "hello world"

    def test_unicode_normalization(self):
        # Combining acute accent should be normalized
        result = normalize_text("café")
        assert "café" in result or "cafe" in result

    def test_tabs_and_newlines(self):
        assert normalize_text("hello\t\n  world") == "hello world"


class TestAbbreviationExpansion:

    def test_bpm_expanded(self):
        assert "beats per minute" in expand_abbreviations("120 bpm track")

    def test_lofi_normalized(self):
        result = expand_abbreviations("lofi beats")
        assert "lo-fi" in result

    def test_sax_expanded(self):
        assert "saxophone" in expand_abbreviations("add some sax")


class TestHardNumberExtraction:

    def test_tempo_bpm(self):
        nums = extract_hard_numbers("play at 120 bpm")
        assert nums.tempo_bpm == 120

    def test_tempo_beats_per_minute(self):
        nums = extract_hard_numbers("set tempo to 85 beats per minute")
        assert nums.tempo_bpm == 85

    def test_duration_minutes(self):
        nums = extract_hard_numbers("make a 3 minute song")
        assert nums.duration_seconds == 180

    def test_duration_mm_ss(self):
        nums = extract_hard_numbers("create a 2:30 track")
        assert nums.duration_seconds == 150

    def test_duration_bars(self):
        nums = extract_hard_numbers("extend to 64 bars")
        assert nums.duration_bars == 64

    def test_time_signature(self):
        nums = extract_hard_numbers("waltz in 3/4 time")
        assert nums.time_signature == "3/4"

    def test_track_count(self):
        nums = extract_hard_numbers("composition with 5 tracks")
        assert nums.track_count == 5

    def test_no_numbers(self):
        nums = extract_hard_numbers("something chill and ambient")
        assert nums.tempo_bpm is None
        assert nums.duration_seconds is None

    def test_full_preprocess_pipeline(self):
        result = preprocess("make a 2 min lofi track at 80 bpm with sax")
        assert result.extracted.tempo_bpm == 80
        assert result.extracted.duration_seconds == 120
        assert "lo-fi" in result.normalized
        assert "saxophone" in result.normalized
        assert "Tempo: 80 BPM" in result.enriched_prompt


# =====================================================================
# SECTION 3: Keyword Fallback Tests
# =====================================================================


class TestKeywordFallback:

    def _run_fallback(self, text: str) -> ParsedIntent:
        preprocessed = preprocess(text)
        return _fallback_keyword_parse(preprocessed.normalized, preprocessed)

    def test_genre_detection_lofi(self):
        result = self._run_fallback("make a lofi beat")
        assert result.genre.primary == "lofi"

    def test_genre_detection_jazz(self):
        result = self._run_fallback("smooth jazz quartet")
        assert result.genre.primary == "jazz"

    def test_genre_detection_ambient(self):
        result = self._run_fallback("ambient soundscape")
        assert result.genre.primary == "ambient"

    def test_energy_high(self):
        result = self._run_fallback("intense energetic rock")
        assert result.energy.level == "high"

    def test_energy_low(self):
        result = self._run_fallback("calm peaceful melody")
        assert result.energy.level == "low"

    def test_tempo_extraction(self):
        result = self._run_fallback("electronic track at 128 bpm")
        assert result.tempo.bpm == 128
        assert result.tempo.source == "explicit"

    def test_instrument_detection(self):
        result = self._run_fallback("add piano and drums")
        names = [i.name for i in result.instruments]
        assert "piano" in names
        assert "drums" in names

    def test_key_detection(self):
        result = self._run_fallback("jazz in Bb minor")
        assert result.key.root is not None
        assert result.key.scale == "minor"

    def test_duration_bars(self):
        result = self._run_fallback("32 bars of funk")
        assert result.duration.bars == 32

    def test_vague_prompt_defaults(self):
        result = self._run_fallback("play something nice")
        assert result.genre.primary == "pop"
        assert result.overall_confidence <= 0.5

    # -- Contextual inference tests (no explicit genre keyword) --

    def test_context_studying_maps_to_lofi(self):
        result = self._run_fallback("music for studying late at night")
        assert result.genre.primary == "lofi"
        assert result.mood.primary == "calm"
        assert result.energy.level == "low"

    def test_context_workout_maps_to_electronic(self):
        result = self._run_fallback("something for my workout session")
        assert result.genre.primary == "electronic"
        assert result.energy.level == "high"

    def test_context_meditation_maps_to_ambient(self):
        result = self._run_fallback("meditation background sounds")
        assert result.genre.primary == "ambient"
        assert result.energy.level == "low"

    def test_context_party_maps_to_electronic(self):
        result = self._run_fallback("something for the party tonight")
        assert result.genre.primary == "electronic"
        assert result.energy.level == "high"

    def test_context_sleeping_maps_to_ambient(self):
        result = self._run_fallback("gentle music for sleeping")
        assert result.genre.primary == "ambient"

    def test_context_coffee_maps_to_jazz(self):
        result = self._run_fallback("background music for a coffee shop")
        assert result.genre.primary == "jazz"

    def test_context_horror_maps_to_cinematic(self):
        result = self._run_fallback("creepy music for a horror scene")
        assert result.genre.primary == "cinematic"

    def test_context_film_maps_to_cinematic(self):
        result = self._run_fallback("music for a movie trailer")
        assert result.genre.primary == "cinematic"

    def test_explicit_genre_overrides_context(self):
        """Explicit genre keyword should win over contextual inference."""
        result = self._run_fallback("classical music for studying")
        assert result.genre.primary == "classical"

    def test_context_driving_maps_to_rock(self):
        result = self._run_fallback("something for a road trip")
        assert result.genre.primary == "rock"


# =====================================================================
# SECTION 4: Engine Integration Tests (with mock LLM)
# =====================================================================


class TestLLMIntentEngine:
    """Test the full engine pipeline with mocked LLM responses."""

    def _make_valid_llm_response(self, **overrides) -> str:
        """Build a valid JSON response that ParsedIntent will accept."""
        base = {
            "reasoning": "Mock LLM reasoning",
            "action": "new",
            "genre": {"primary": "cinematic", "secondary": None, "confidence": 0.9},
            "mood": {"primary": "epic", "secondary": "dramatic", "valence": 0.6, "confidence": 0.9},
            "energy": {"level": "high", "confidence": 0.85},
            "tempo": {"bpm": 90, "source": "explicit", "confidence": 0.99},
            "key": {"root": "D", "scale": "minor", "confidence": 0.95},
            "duration": {"bars": 45, "seconds": 120, "descriptor": "medium", "confidence": 0.9},
            "instruments": [
                {"name": "strings", "role": "harmony", "priority": 9},
                {"name": "brass", "role": "lead", "priority": 8},
            ],
            "dynamics": {"intensity": "powerful", "arc": "build"},
            "structure": {
                "has_intro": True,
                "has_verse": True,
                "has_chorus": True,
                "has_bridge": True,
                "has_outro": True,
                "form_hint": None,
            },
            "production": {"descriptors": ["orchestral"], "complexity": "rich"},
            "reference": None,
            "overall_confidence": 0.92,
        }
        base.update(overrides)
        return json.dumps(base)

    @patch("src.intent.engine.call_llm")
    @patch("src.intent.engine.LLMConfig")
    def test_successful_parse(self, mock_config, mock_call_llm):
        """Full pipeline with a valid LLM response."""
        mock_config.AVAILABLE_PROVIDERS = ["minimax"]
        mock_call_llm.return_value = self._make_valid_llm_response()

        engine = LLMIntentEngine()
        parsed, enhanced, music_intent = engine.parse("epic cinematic piece in D minor at 90 BPM")

        assert parsed.genre.primary == "cinematic"
        assert parsed.tempo.bpm == 90
        assert parsed.key.root == "D"
        assert music_intent.genre == "cinematic"
        assert enhanced.tempo_preference == 90

    @patch("src.intent.engine.call_llm")
    @patch("src.intent.engine.LLMConfig")
    def test_fallback_on_llm_failure(self, mock_config, mock_call_llm):
        """When LLM returns None, fallback to keywords."""
        mock_config.AVAILABLE_PROVIDERS = ["minimax"]
        mock_call_llm.return_value = None

        engine = LLMIntentEngine()
        parsed, enhanced, music_intent = engine.parse("ambient soundscape")

        # Should still produce a valid result via keyword fallback
        assert parsed.genre.primary == "ambient"
        assert parsed.overall_confidence <= 0.5

    @patch("src.intent.engine.call_llm")
    @patch("src.intent.engine.LLMConfig")
    def test_retry_on_validation_error(self, mock_config, mock_call_llm):
        """When first LLM response is invalid, engine retries once."""
        mock_config.AVAILABLE_PROVIDERS = ["minimax"]

        # First call returns invalid JSON, second call returns valid
        invalid_response = '{"genre": {"primary": "dubstep"}}'  # invalid genre
        valid_response = self._make_valid_llm_response()
        mock_call_llm.side_effect = [invalid_response, valid_response]

        engine = LLMIntentEngine()
        parsed, enhanced, music_intent = engine.parse("cinematic piece")

        assert parsed.genre.primary == "cinematic"
        assert mock_call_llm.call_count == 2

    @patch("src.intent.engine.call_llm")
    @patch("src.intent.engine.LLMConfig")
    def test_hard_numbers_override_llm(self, mock_config, mock_call_llm):
        """Preprocessor-extracted tempo should override LLM-inferred tempo."""
        mock_config.AVAILABLE_PROVIDERS = ["minimax"]
        # LLM says 90 BPM but the prompt says "128 bpm"
        mock_call_llm.return_value = self._make_valid_llm_response(
            tempo={"bpm": 90, "source": "inferred", "confidence": 0.5}
        )

        engine = LLMIntentEngine()
        parsed, enhanced, music_intent = engine.parse("electronic track at 128 bpm")

        # Preprocessor should catch "128 bpm" and override
        assert parsed.tempo.bpm == 128
        assert parsed.tempo.source == "explicit"

    @patch("src.intent.engine.LLMConfig")
    def test_no_providers_uses_fallback(self, mock_config):
        """When no LLM providers are configured, use keyword fallback."""
        mock_config.AVAILABLE_PROVIDERS = []

        engine = LLMIntentEngine()
        parsed, enhanced, music_intent = engine.parse("jazz in Bb")

        assert parsed.genre.primary == "jazz"
        assert parsed.overall_confidence <= 0.5

    @patch("src.intent.engine.call_llm")
    @patch("src.intent.engine.LLMConfig")
    def test_markdown_fences_stripped(self, mock_config, mock_call_llm):
        """LLM wrapping JSON in ```json fences should still parse."""
        mock_config.AVAILABLE_PROVIDERS = ["minimax"]
        mock_call_llm.return_value = f"```json\n{self._make_valid_llm_response()}\n```"

        engine = LLMIntentEngine()
        parsed, _, _ = engine.parse("cinematic piece")
        assert parsed.genre.primary == "cinematic"


# =====================================================================
# SECTION 5: Edge Case / Accuracy Tests (prompt-level)
# =====================================================================


class TestPromptAccuracy:
    """Test keyword fallback accuracy against diverse prompt types.

    These verify the fallback parser handles the kinds of prompts that the
    LLM engine is designed for, ensuring reasonable defaults even without an LLM.
    """

    def _parse(self, text: str) -> ParsedIntent:
        preprocessed = preprocess(text)
        return _fallback_keyword_parse(preprocessed.normalized, preprocessed)

    def test_compound_dark_ambient(self):
        result = self._parse("dark ambient drone")
        assert result.genre.primary == "ambient"
        assert result.mood.primary == "dark"

    def test_compound_hard_rock(self):
        result = self._parse("hard rock track")
        assert result.genre.primary == "rock"

    def test_study_music_context(self):
        result = self._parse("music for studying late at night")
        # Keyword fallback cannot contextually infer "studying" → lofi.
        # The LLM engine handles this case. Fallback should still produce
        # a valid intent with low confidence.
        assert result.overall_confidence <= 0.5
        assert result.genre.primary in ("pop", "lofi", "ambient")

    def test_explicit_duration_minutes(self):
        result = self._parse("3 minute classical piece")
        assert result.duration.seconds == 180

    def test_multiple_instruments(self):
        result = self._parse("add piano, guitar, and drums")
        names = [i.name for i in result.instruments]
        assert len(names) >= 2

    def test_modification_vocabulary(self):
        """Modification keywords should still produce a valid parse."""
        result = self._parse("make it faster and louder")
        # Fallback defaults to "new" action (no session context)
        assert result.action == "new"

    def test_very_vague_prompt(self):
        result = self._parse("something")
        assert result.genre.primary == "pop"
        assert result.overall_confidence <= 0.5

    def test_tempo_from_bpm(self):
        result = self._parse("funky groove at 105 bpm")
        assert result.genre.primary == "funk"
        assert result.tempo.bpm == 105

    def test_key_with_flat(self):
        result = self._parse("ballad in Eb minor")
        assert result.key.root is not None
        assert result.key.scale == "minor"
