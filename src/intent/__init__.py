# -*- coding: utf-8 -*-
"""
Intent Parsing Engine — High-accuracy LLM-based musical intent extraction.

This package replaces the legacy multi-parser architecture with a unified
LLM-first engine backed by Pydantic v2 schema validation, chain-of-thought
prompting, and musical coherence checks.
"""

from src.intent.schema import ParsedIntent, GenreInfo, MoodInfo, TempoInfo, KeyInfo, DurationInfo
from src.intent.engine import LLMIntentEngine

__all__ = [
    "LLMIntentEngine",
    "ParsedIntent",
    "GenreInfo",
    "MoodInfo",
    "TempoInfo",
    "KeyInfo",
    "DurationInfo",
]
