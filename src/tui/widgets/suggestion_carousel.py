# -*- coding: utf-8 -*-
"""
Suggestion Carousel Widget
Horizontal row of clickable genre suggestion chips below the prompt input.
"""

from __future__ import annotations

import random
from typing import List

from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.message import Message
from textual.widgets import Button, Static

_QUICK_SUGGESTIONS: List[str] = [
    "ambient",
    "cinematic",
    "jazz",
    "lo-fi",
    "electronic",
    "classical",
    "funk",
    "pop",
    "rock",
    "hip-hop",
]


class SuggestionCarousel(Static):
    """Horizontally scrollable row of genre chips."""

    class ChipSelected(Message):
        """A suggestion chip was clicked."""
        def __init__(self, text: str) -> None:
            super().__init__()
            self.text = text

    def compose(self) -> ComposeResult:
        with Horizontal(id="suggestion-carousel"):
            shuffled = _QUICK_SUGGESTIONS[:]
            random.shuffle(shuffled)
            for genre in shuffled[:8]:
                yield Button(
                    genre,
                    classes="suggestion-chip",
                    id=f"chip-{genre}",
                )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.has_class("suggestion-chip"):
            genre = str(event.button.label)
            prompt = self._expand_genre(genre)
            self.post_message(self.ChipSelected(prompt))

    @staticmethod
    def _expand_genre(genre: str) -> str:
        """Expand a genre keyword into a full prompt."""
        expansions = {
            "ambient": "Create a peaceful ambient soundscape with floating pads and soft textures",
            "cinematic": "Compose an epic cinematic orchestral piece with sweeping strings and brass",
            "jazz": "Write a smooth jazz piece with saxophone, piano comping, and brushed drums",
            "lo-fi": "Generate a chill lo-fi hip hop beat with warm vinyl texture and soft piano",
            "electronic": "Create an energetic electronic track with driving synths and punchy drums",
            "classical": "Compose an elegant classical chamber piece with piano and strings",
            "funk": "Generate a groovy funk track with slap bass, wah guitar, and tight drums",
            "pop": "Create a catchy pop song with bright production, vocal melody, and driving beat",
            "rock": "Write a rock track with distorted guitars, powerful drums, and bass",
            "hip-hop": "Generate a hard-hitting hip-hop beat with 808 bass, crisp snares, and hi-hats",
        }
        return expansions.get(genre, f"Create a {genre} composition with rich instrumentation")
