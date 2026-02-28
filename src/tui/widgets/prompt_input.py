# -*- coding: utf-8 -*-
"""
Prompt Input Widget
Text area for music description + Generate / Surprise Me buttons.
"""

from __future__ import annotations

import random
from typing import TYPE_CHECKING

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.message import Message
from textual.widgets import Button, Label, ProgressBar, Static, TextArea

if TYPE_CHECKING:
    pass


class PromptInput(Static):
    """Prompt text area with generate and surprise buttons."""

    class GenerateRequested(Message):
        """Fired when the user clicks Generate or presses Ctrl+Enter."""
        def __init__(self, prompt: str) -> None:
            super().__init__()
            self.prompt = prompt

    def compose(self) -> ComposeResult:
        with Vertical(id="prompt-panel"):
            yield TextArea(
                "",
                id="prompt-input",
                language=None,
                soft_wrap=True,
                show_line_numbers=False,
            )
            with Horizontal(id="prompt-buttons"):
                yield Button("Generate", id="btn-generate", variant="primary")
                yield Button("🎲", id="btn-surprise", variant="warning")
            yield Label("", id="model-info")
            yield ProgressBar(total=8, show_eta=False, id="inline-bar")
            yield Label("", id="inline-status")

    def on_mount(self) -> None:
        ta = self.query_one("#prompt-input", TextArea)
        ta.text = ""
        # Hide inline progress until generation starts
        self.query_one("#inline-bar", ProgressBar).display = False
        self.query_one("#inline-status", Label).display = False
        self.query_one("#model-info", Label).display = False

    # ------------------------------------------------------------------ #
    # Button handlers
    # ------------------------------------------------------------------ #

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-generate":
            self._do_generate()
        elif event.button.id == "btn-surprise":
            self._do_surprise()

    # ------------------------------------------------------------------ #
    # Actions
    # ------------------------------------------------------------------ #

    def _do_generate(self) -> None:
        ta = self.query_one("#prompt-input", TextArea)
        prompt = ta.text.strip()
        if not prompt:
            self.notify("Please enter a music description first.", severity="warning")
            return
        self.post_message(self.GenerateRequested(prompt))

    def _do_surprise(self) -> None:
        """Pick a random preset prompt and populate the input."""
        surprises = [
            "Create a peaceful, meditative ambient soundscape with floating pads and soft bells",
            "Compose an epic cinematic orchestral piece with sweeping strings and brass",
            "Generate a funky electronic groove with synth leads and syncopated bass",
            "Write a smooth jazz improvisation with sultry saxophone and piano comping",
            "Create a melancholy lo-fi hip hop beat with warm vinyl crackle and gentle piano",
            "Compose a high-energy pop track with catchy vocal melody and driving drums",
            "Generate a dark mysterious ambient piece with dissonant textures and drones",
            "Write a classical chamber piece with elegant piano and sweeping cello",
            "Create a dreamy shoegaze soundscape with reverb-drenched guitars and slow drums",
            "Compose an uplifting trance anthem with arpeggiated synths and euphoric build-ups",
        ]
        ta = self.query_one("#prompt-input", TextArea)
        ta.text = random.choice(surprises)
        ta.focus()

    # ------------------------------------------------------------------ #
    # External control
    # ------------------------------------------------------------------ #

    def set_model_info(self, provider: str, model: str) -> None:
        """Show the active LLM provider/model below the buttons."""
        lbl = self.query_one("#model-info", Label)
        lbl.update(f"via {model}")
        lbl.display = True

    def set_prompt(self, text: str) -> None:
        """Programmatically set the prompt text (e.g. from sidebar click)."""
        ta = self.query_one("#prompt-input", TextArea)
        ta.text = text
        ta.focus()

    def set_generating(self, generating: bool) -> None:
        """Disable/enable controls during generation."""
        btn = self.query_one("#btn-generate", Button)
        surprise = self.query_one("#btn-surprise", Button)
        ta = self.query_one("#prompt-input", TextArea)

        btn.disabled = generating
        surprise.disabled = generating
        ta.read_only = generating

        if generating:
            btn.label = "Generating…"
            btn.add_class("disabled-look")
        else:
            btn.label = "Generate"
            btn.remove_class("disabled-look")

    # ------------------------------------------------------------------ #
    # Inline progress
    # ------------------------------------------------------------------ #

    _PIPELINE_NODES = [
        "intent_parser", "track_planner", "theory_validator",
        "track_generator", "quality_control", "refinement",
        "midi_creator", "session_summary",
    ]

    _NODE_LABELS = {
        "intent_parser": "Parse", "track_planner": "Plan",
        "theory_validator": "Validate", "track_generator": "Generate",
        "quality_control": "QC", "refinement": "Refine",
        "midi_creator": "MIDI", "session_summary": "Summary",
    }

    def show_progress(self) -> None:
        """Reset and reveal the inline progress bar."""
        bar = self.query_one("#inline-bar", ProgressBar)
        bar.update(progress=0, total=len(self._PIPELINE_NODES))
        bar.display = True
        status = self.query_one("#inline-status", Label)
        status.update("Starting…")
        status.display = True

    def hide_progress(self) -> None:
        self.query_one("#inline-bar", ProgressBar).display = False
        self.query_one("#inline-status", Label).display = False

    def update_progress(self, node_name: str) -> None:
        """Advance the inline progress bar to *node_name*."""
        try:
            step = self._PIPELINE_NODES.index(node_name) + 1
        except ValueError:
            step = 0
        label = self._NODE_LABELS.get(node_name, node_name)
        self.query_one("#inline-bar", ProgressBar).update(progress=step)
        self.query_one("#inline-status", Label).update(
            f"{step}/{len(self._PIPELINE_NODES)} {label}…"
        )

    def mark_complete(self, quality_score: float | None = None) -> None:
        bar = self.query_one("#inline-bar", ProgressBar)
        bar.update(progress=len(self._PIPELINE_NODES))
        score = f" · {quality_score:.0%}" if quality_score else ""
        self.query_one("#inline-status", Label).update(f"✓ Done{score}")

    def mark_error(self, message: str) -> None:
        self.query_one("#inline-status", Label).update(f"✗ {message[:60]}")
