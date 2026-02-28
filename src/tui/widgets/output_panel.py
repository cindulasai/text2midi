# -*- coding: utf-8 -*-
"""
Output Panel Widget
Displays generation results: track table, quality score, compact info,
and quick-action buttons for clipboard/DAW integration.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Button, DataTable, Label, Static

from src.tui.clipboard import copy_file_to_clipboard, copy_path_to_clipboard
from src.tui.daw_launcher import open_in_default_app, open_folder
from src.config.constants import TICKS_PER_BEAT


class OutputPanel(Static):
    """Displays completed generation results with quick-action toolbar."""

    def compose(self) -> ComposeResult:
        with Vertical(id="output-panel"):
            yield Label("", id="result-header")
            yield DataTable(id="track-table", show_cursor=False)
            with Horizontal(id="result-footer"):
                yield Label("", id="output-file-path")
                yield Button("Copy to DAW", id="btn-copy-to-daw", classes="pill primary-pill")
                yield Button("📂", id="btn-open-folder", classes="pill")
                yield Button("📋", id="btn-copy-path", classes="pill")

    def on_mount(self) -> None:
        table = self.query_one("#track-table", DataTable)
        table.add_columns("Ch", "Instrument", "Type", "Notes", "Dur")

    # ------------------------------------------------------------------ #
    # Public API
    # ------------------------------------------------------------------ #

    def show_results(self, result_state: Dict[str, Any]) -> None:
        """Populate the panel from a completed generation state dict."""
        panel = self.query_one("#output-panel")
        panel.add_class("visible")

        # Quality score text
        quality_text = ""
        quality_report = result_state.get("quality_report")
        if quality_report:
            score = quality_report.overall_score
            filled = int(score * 10)
            bar = "█" * filled + "░" * (10 - filled)
            quality_text = f"{bar} {score:.0%}"

        # Track table
        table = self.query_one("#track-table", DataTable)
        table.clear()
        tracks: List[Any] = result_state.get("generated_tracks", [])
        total_notes = 0
        max_dur_ticks = 0
        for i, track in enumerate(tracks):
            ch = getattr(track, "channel", i)
            instr = getattr(track, "name", "unknown")
            ttype = getattr(track, "track_type", "")
            notes = len(getattr(track, "notes", []))
            total_notes += notes
            dur_ticks = 0
            for n in getattr(track, "notes", []):
                end = getattr(n, "start_time", 0) + getattr(n, "duration", 0)
                if end > dur_ticks:
                    dur_ticks = end
            if dur_ticks > max_dur_ticks:
                max_dur_ticks = dur_ticks
            dur_sec = f"{dur_ticks / TICKS_PER_BEAT / 2:.0f}s" if dur_ticks else "–"
            table.add_row(str(ch), str(instr), str(ttype), str(notes), dur_sec)

        # Build merged result header (quality + file badge)
        midi_path = result_state.get("final_midi_path", "")
        self._midi_path = midi_path
        badge_parts = self._build_badge_parts(
            midi_path, len(tracks), total_notes, max_dur_ticks, result_state,
        )
        badge_text = " · ".join(badge_parts)
        header = f"{quality_text}  {badge_text}" if quality_text else badge_text
        self.query_one("#result-header", Label).update(header)

        # Filename in footer
        if midi_path:
            short = Path(midi_path).name
            self.query_one("#output-file-path", Label).update(f"📁 {short}")
        else:
            self.query_one("#output-file-path", Label).update("")

    def hide(self) -> None:
        panel = self.query_one("#output-panel")
        panel.remove_class("visible")

    # ------------------------------------------------------------------ #
    # File info badge
    # ------------------------------------------------------------------ #

    def _build_badge_parts(
        self,
        midi_path: str,
        track_count: int,
        total_notes: int,
        max_dur_ticks: int,
        result_state: Dict[str, Any],
    ) -> List[str]:
        """Return compact info parts about the generated MIDI."""
        parts: List[str] = []

        if midi_path and Path(midi_path).exists():
            size_bytes = Path(midi_path).stat().st_size
            if size_bytes < 1024:
                parts.append(f"{size_bytes}B")
            else:
                parts.append(f"{size_bytes / 1024:.1f}KB")

        parts.append(f"{track_count}trk")
        parts.append(f"{total_notes}n")

        if max_dur_ticks > 0:
            dur_seconds = max_dur_ticks / TICKS_PER_BEAT / 2
            minutes = int(dur_seconds // 60)
            seconds = int(dur_seconds % 60)
            if minutes > 0:
                parts.append(f"{minutes}m{seconds}s")
            else:
                parts.append(f"{seconds}s")

        intent = result_state.get("intent")
        if intent:
            genre = getattr(intent, "genre", "")
            if genre:
                parts.append(genre)

        return parts

    # ------------------------------------------------------------------ #
    # Quick action handlers
    # ------------------------------------------------------------------ #

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-copy-to-daw":
            self._copy_to_daw()
        elif event.button.id == "btn-open-folder":
            self._open_folder()
        elif event.button.id == "btn-copy-path":
            self._copy_path()

    def _copy_to_daw(self) -> None:
        """Copy the MIDI file to clipboard in CF_HDROP format for DAW paste."""
        path = getattr(self, "_midi_path", None)
        if not path:
            self.notify("No output file yet.", severity="warning")
            return
        if copy_file_to_clipboard(path):
            self.notify(
                "✅ MIDI copied! Paste (Ctrl+V) in your DAW.",
                severity="information",
            )
        else:
            self.notify(
                "❌ Could not copy to clipboard.",
                severity="error",
            )

    def _open_folder(self) -> None:
        """Open the containing folder, highlighting the MIDI file."""
        path = getattr(self, "_midi_path", None)
        if not path:
            self.notify("No output file yet.", severity="warning")
            return
        if open_folder(path):
            self.notify("📂 Opening folder...", severity="information")
        else:
            self.notify("❌ Could not open folder.", severity="error")

    def _copy_path(self) -> None:
        """Copy the MIDI file path as plain text to clipboard."""
        path = getattr(self, "_midi_path", None)
        if not path:
            self.notify("No output file yet.", severity="warning")
            return
        if copy_path_to_clipboard(path):
            self.notify("📝 Path copied!", severity="information")
        else:
            self.notify("❌ Could not copy path.", severity="error")
