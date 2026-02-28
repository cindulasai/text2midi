# -*- coding: utf-8 -*-
"""
Progress Panel Widget
Shows generation pipeline progress with animated step indicators.
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
    "intent_parser": "Parse",
    "track_planner": "Plan",
    "theory_validator": "Validate",
    "track_generator": "Generate",
    "quality_control": "QC",
    "refinement": "Refine",
    "midi_creator": "MIDI",
    "session_summary": "Summary",
}


class ProgressPanel(Static):
    """Displays per-node generation progress with animated step indicators."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._completed_nodes: list[str] = []
        self._current_node: str | None = None

    def compose(self) -> ComposeResult:
        with Vertical(id="progress-panel"):
            yield ProgressBar(
                total=len(_NODES),
                show_eta=False,
                id="progress-bar",
            )
            yield Label("Preparing…", id="progress-label")
            yield Label("", id="progress-steps")

    # ------------------------------------------------------------------ #
    # Public API
    # ------------------------------------------------------------------ #

    def show(self) -> None:
        """Make the progress panel visible and reset it."""
        self._completed_nodes = []
        self._current_node = None
        panel = self.query_one("#progress-panel")
        panel.add_class("visible")
        bar = self.query_one("#progress-bar", ProgressBar)
        bar.update(progress=0, total=len(_NODES))
        self.query_one("#progress-label", Label).update("Starting pipeline…")
        self._render_steps()

    def hide(self) -> None:
        panel = self.query_one("#progress-panel")
        panel.remove_class("visible")

    def update_progress(self, node_name: str) -> None:
        """Advance the progress bar to the given node."""
        # Mark previous node as complete
        if self._current_node and self._current_node not in self._completed_nodes:
            self._completed_nodes.append(self._current_node)
        self._current_node = node_name

        try:
            step = _NODES.index(node_name) + 1
        except ValueError:
            step = 0
        label_text = _NODE_LABELS.get(node_name, node_name)
        bar = self.query_one("#progress-bar", ProgressBar)
        bar.update(progress=step)
        self.query_one("#progress-label", Label).update(
            f"{step}/{len(_NODES)} {label_text}…"
        )
        self._render_steps()

    def mark_complete(self, quality_score: float | None = None) -> None:
        """Show completion state."""
        # Mark last node as complete
        if self._current_node and self._current_node not in self._completed_nodes:
            self._completed_nodes.append(self._current_node)
        self._current_node = None

        bar = self.query_one("#progress-bar", ProgressBar)
        bar.update(progress=len(_NODES))
        score_text = f" · {quality_score:.0%}" if quality_score else ""
        self.query_one("#progress-label", Label).update(
            f"✓ Done{score_text}"
        )
        self._render_steps()

    def mark_error(self, message: str) -> None:
        """Show error state."""
        self.query_one("#progress-label", Label).update(f"✗ {message[:60]}")

    # ------------------------------------------------------------------ #
    # Step rendering
    # ------------------------------------------------------------------ #

    def _render_steps(self) -> None:
        """Render the visual step indicators inline."""
        parts: list[str] = []
        for node in _NODES:
            label = _NODE_LABELS.get(node, node)
            if node in self._completed_nodes:
                parts.append(f"[#a6e3a1]✓{label}[/]")
            elif node == self._current_node:
                parts.append(f"[#89b4fa bold]▸{label}[/]")
            else:
                parts.append(f"[#6c7086]·{label}[/]")
        steps_label = self.query_one("#progress-steps", Label)
        steps_label.update(" ".join(parts))
