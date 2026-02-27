# -*- coding: utf-8 -*-
"""
Progress Panel Widget
Shows generation pipeline progress with step indicator and progress bar.
"""

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Label, ProgressBar, Static

# Ordered list of graph nodes
_NODES = [
    "intent_parser",
    "track_planner",
    "theory_validator",
    "track_generator",
    "quality_control",
    "refinement",
    "midi_creator",
    "session_summary",
]

_NODE_LABELS = {
    "intent_parser": "Intent Parser",
    "track_planner": "Track Planner",
    "theory_validator": "Theory Validator",
    "track_generator": "Track Generator",
    "quality_control": "Quality Control",
    "refinement": "Refinement",
    "midi_creator": "MIDI Creator",
    "session_summary": "Session Summary",
}


class ProgressPanel(Static):
    """Displays per-node generation progress."""

    def compose(self) -> ComposeResult:
        with Vertical(id="progress-panel"):
            yield Label("⏳  Generating…", classes="title", id="progress-title")
            yield ProgressBar(
                total=len(_NODES),
                show_eta=False,
                id="progress-bar",
            )
            yield Label("Preparing…", id="progress-label")

    # ------------------------------------------------------------------ #
    # Public API
    # ------------------------------------------------------------------ #

    def show(self) -> None:
        """Make the progress panel visible and reset it."""
        panel = self.query_one("#progress-panel")
        panel.add_class("visible")
        bar = self.query_one("#progress-bar", ProgressBar)
        bar.update(progress=0, total=len(_NODES))
        self.query_one("#progress-label", Label).update("Starting generation pipeline…")
        self.query_one("#progress-title", Label).update("⏳  Generating…")

    def hide(self) -> None:
        panel = self.query_one("#progress-panel")
        panel.remove_class("visible")

    def update_progress(self, node_name: str) -> None:
        """Advance the progress bar to the given node."""
        try:
            step = _NODES.index(node_name) + 1
        except ValueError:
            step = 0
        label_text = _NODE_LABELS.get(node_name, node_name)
        bar = self.query_one("#progress-bar", ProgressBar)
        bar.update(progress=step)
        self.query_one("#progress-label", Label).update(
            f"Step {step}/{len(_NODES)}: {label_text}…"
        )

    def mark_complete(self, quality_score: float | None = None) -> None:
        """Show completion state."""
        bar = self.query_one("#progress-bar", ProgressBar)
        bar.update(progress=len(_NODES))
        score_text = f"— Quality: {quality_score:.2f}/1.0" if quality_score else ""
        self.query_one("#progress-label", Label).update(f"✓ Complete {score_text}")
        self.query_one("#progress-title", Label).update("✅  Generation Complete")

    def mark_error(self, message: str) -> None:
        """Show error state."""
        self.query_one("#progress-label", Label).update(f"✗ Error: {message}")
        self.query_one("#progress-title", Label).update("❌  Generation Failed")
