# -*- coding: utf-8 -*-
"""Tests for the prompt suggester (static fallback only — no live LLM)."""

import pytest

from src.tui.suggest.prompt_suggester import _static_suggestion


class TestStaticSuggestion:
    def test_ambient_prefix(self):
        result = _static_suggestion("amb")
        assert result is not None
        assert "ambient" in result.lower()

    def test_jazz_prefix(self):
        result = _static_suggestion("jaz")
        assert result is not None
        assert "jazz" in result.lower()

    def test_electronic_prefix(self):
        result = _static_suggestion("elec")
        assert result is not None
        assert "electronic" in result.lower() or "synth" in result.lower()

    def test_unknown_prefix_returns_none(self):
        assert _static_suggestion("zzz") is None

    def test_short_prefix_returns_none(self):
        assert _static_suggestion("") is None

    def test_dark_prefix(self):
        result = _static_suggestion("dark")
        assert result is not None
        assert "dark" in result.lower()

    def test_pop_prefix(self):
        result = _static_suggestion("pop")
        assert result is not None
        assert "pop" in result.lower()
