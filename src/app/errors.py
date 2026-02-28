# -*- coding: utf-8 -*-
"""
Custom exception hierarchy for the text2midi pipeline.

Usage:
    from src.app.errors import IntentParsingError, GenerationError

These exceptions give callers the ability to distinguish pipeline
failure modes without parsing error strings.
"""


class PipelineError(Exception):
    """Base class for all pipeline errors."""


class IntentParsingError(PipelineError):
    """Raised when user prompt cannot be parsed into a valid intent."""


class TrackPlanningError(PipelineError):
    """Raised when track configuration planning fails."""


class TheoryValidationError(PipelineError):
    """Raised when music theory validation detects fatal issues."""


class GenerationError(PipelineError):
    """Raised when music generation (melody/bass/drums/pad) fails."""


class MIDICreationError(PipelineError):
    """Raised when MIDI file creation or export fails."""


class QualityAssessmentError(PipelineError):
    """Raised when quality review fails critically."""


class LLMProviderError(PipelineError):
    """Raised when an LLM provider call fails."""
