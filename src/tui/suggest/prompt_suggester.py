# -*- coding: utf-8 -*-
"""
Prompt Suggester
LLM-powered autocomplete for the prompt input, with static fallback.
"""

from __future__ import annotations

import asyncio
import logging
from functools import lru_cache
from typing import Optional

from textual.suggester import Suggester

logger = logging.getLogger(__name__)


class PromptSuggester(Suggester):
    """Textual Suggester that calls the LLM for prompt completion.

    Falls back to a static genre-keyword suggester when the LLM is unavailable
    or times out.
    """

    def __init__(self) -> None:
        super().__init__(use_cache=True, case_sensitive=False)
        self._debounce_task: Optional[asyncio.Task] = None
        self._cache: dict[str, str] = {}

    async def get_suggestion(self, value: str) -> Optional[str]:
        """Return a completion suggestion for *value*."""
        if not value or len(value) < 3:
            return None

        # Check local cache first
        lower = value.lower()
        if lower in self._cache:
            return self._cache[lower]

        # Try static suggestions first (instant, no LLM call)
        static = _static_suggestion(lower)
        if static:
            self._cache[lower] = static
            return static

        # Debounced LLM call
        try:
            suggestion = await asyncio.wait_for(
                self._call_llm(value), timeout=2.0
            )
            if suggestion:
                self._cache[lower] = suggestion
                return suggestion
        except (asyncio.TimeoutError, Exception) as exc:
            logger.debug("LLM suggestion failed: %s", exc)

        return None

    async def _call_llm(self, partial: str) -> Optional[str]:
        """Call the LLM in a thread executor for non-blocking behaviour."""
        await asyncio.sleep(0.3)  # debounce

        loop = asyncio.get_running_loop()
        try:
            result = await loop.run_in_executor(None, _llm_complete, partial)
            return result
        except Exception:
            return None


def _llm_complete(partial: str) -> Optional[str]:
    """Synchronous LLM completion call (run in thread)."""
    try:
        from src.config.llm import call_llm, LLMConfig

        if not LLMConfig.DEFAULT_PROVIDER:
            return None

        system_prompt = (
            "You are a music prompt completer. Given a partial music description, "
            "suggest the complete prompt. Respond with ONLY the full completed text, "
            "no explanation. Keep it under 200 characters."
        )
        response = call_llm(system_prompt, partial, temperature=0.7, max_tokens=100)
        if response and len(response) > len(partial):
            return response
    except Exception:
        pass
    return None


def _static_suggestion(partial: str) -> Optional[str]:
    """Return a genre-keyword completion if the partial matches."""
    completions = {
        "amb": "ambient soundscape with floating pads and soft textures",
        "cine": "cinematic orchestral piece with sweeping strings and brass",
        "jaz": "jazz piece with saxophone, piano comping, and brushed drums",
        "lo-": "lo-fi hip hop beat with warm vinyl texture and soft piano",
        "lof": "lo-fi hip hop beat with warm vinyl texture and soft piano",
        "elec": "electronic track with driving synths and punchy drums",
        "class": "classical chamber piece with piano and strings",
        "fun": "funk track with slap bass, wah guitar, and tight drums",
        "pop": "pop song with bright production, vocal melody, and driving beat",
        "rock": "rock track with distorted guitars, powerful drums, and bass",
        "hip": "hip-hop beat with 808 bass, crisp snares, and hi-hats",
        "dream": "dreamy shoegaze soundscape with reverb-drenched guitars",
        "dark": "dark mysterious ambient piece with dissonant textures and drones",
        "epic": "epic cinematic orchestral piece with dramatic builds",
        "peace": "peaceful meditative ambient soundscape with gentle textures",
        "smooth": "smooth jazz improvisation with sultry saxophone and piano",
        "tran": "trance anthem with arpeggiated synths and euphoric build-ups",
    }
    for prefix, completion in completions.items():
        if partial.startswith(prefix):
            return completion
    return None
