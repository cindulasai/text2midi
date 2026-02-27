# -*- coding: utf-8 -*-
"""
Output Panel Widget
Displays generation results: track table, quality score, summary, file path.
"""

from __future__ import annotations

import os
import platform
import subprocess
from pathlib import Path
from typing import Any, Dict, List

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.message import Message
from textual.widgets import Button, DataTable, Label, Markdown, Static


class OutputPanel(Static):
    """Displays completed generation results."""

    class ChangeApiKeyRequested(Message):
        """User wants to change the API key."""

    def compose(self) -> ComposeResult:
        with Vertical(id="output-panel"):
            yield Label("🎶  Generation Results", classes="title")
            yield Label("", id="quality-display")
            yield DataTable(id="track-table", show_cursor=False)
            yield Markdown("", id="output-summary")
            yield Label("", id="output-file-path")
            with Horizontal(id="output-buttons"):
                yield Button("📂 Open Folder", id="btn-open-folder")
                yield Button("🔑 Change API Key", id="btn-change-key")

    def on_mount(self) -> None:
        table = self.query_one("#track-table", DataTable)
        table.add_columns("Ch", "Instrument", "Type", "Notes", "Duration")

    # ------------------------------------------------------------------ #
    # Public API
    # ------------------------------------------------------------------ #

    def show_results(self, result_state: Dict[str, Any]) -> None:
        """Populate the panel from a completed generation state dict."""
        panel = self.query_one("#output-panel")
        panel.add_class("visible")

        # Quality score
        quality_report = result_state.get("quality_report")
        if quality_report:
            score = quality_report.overall_score
            filled = int(score * 10)
            bar = "■" * filled + "□" * (10 - filled)
            self.query_one("#quality-display", Label).update(
                f"Quality: {score:.2f}/1.0  {bar}"
            )
        else:
            self.query_one("#quality-display", Label).update("")

        # Track table
        table = self.query_one("#track-table", DataTable)
        table.clear()
        tracks: List[Any] = result_state.get("generated_tracks", [])
        for i, track in enumerate(tracks):
            ch = getattr(track, "channel", i)
            instr = getattr(track, "name", "unknown")
            ttype = getattr(track, "track_type", "")
            notes = len(getattr(track, "notes", []))
            dur_ticks = 0
            for n in getattr(track, "notes", []):
                end = getattr(n, "start_time", 0) + getattr(n, "duration", 0)
                if end > dur_ticks:
                    dur_ticks = end
            dur_sec = f"{dur_ticks / 480 / 2:.1f}s" if dur_ticks else "–"
            table.add_row(str(ch), str(instr), str(ttype), str(notes), dur_sec)

        # Summary
        summary = result_state.get("session_summary", "")
        self.query_one("#output-summary", Markdown).update(summary or "_No summary available._")

        # File path
        midi_path = result_state.get("final_midi_path", "")
        if midi_path:
            self.query_one("#output-file-path", Label).update(f"📁 {midi_path}")
        else:
            self.query_one("#output-file-path", Label).update("")

        self._midi_path = midi_path

    def hide(self) -> None:
        panel = self.query_one("#output-panel")
        panel.remove_class("visible")

    # ------------------------------------------------------------------ #
    # Button handlers
    # ------------------------------------------------------------------ #

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-open-folder":
            self._open_folder()
        elif event.button.id == "btn-change-key":
            self.post_message(self.ChangeApiKeyRequested())

    def _open_folder(self) -> None:
        path = getattr(self, "_midi_path", None)
        if not path:
            self.notify("No output file yet.", severity="warning")
            return
        folder = str(Path(path).parent)
        try:
            if platform.system() == "Windows":
                os.startfile(folder)
            elif platform.system() == "Darwin":
                subprocess.Popen(["open", folder])
            else:
                subprocess.Popen(["xdg-open", folder])
        except Exception as exc:
            self.notify(f"Could not open folder: {exc}", severity="error")
