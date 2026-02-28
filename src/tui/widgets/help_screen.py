# -*- coding: utf-8 -*-
"""
Help Screen — Modal overlay with keybinding reference and tips.
"""

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, DataTable, Label, Markdown


_HELP_MARKDOWN = """\
## Supported Genres
ambient · cinematic · classical · electronic · funk ·
jazz · lo-fi · pop · rock · hip-hop

## Supported Providers
- **MiniMax M2.5** — high-quality coding/music model
- **Groq (Llama 4 Maverick)** — fast inference
- **OpenAI-compatible** — any custom endpoint (Ollama, LM Studio, etc.)

## Tips for Best Results
- Be specific: *"melancholy jazz with muted trumpet and brushed drums"*
- Mention tempo: *"upbeat 140 BPM trance anthem"*
- Describe mood: *"dark, mysterious, eerie ambient"*
- Name instruments: *"piano, cello, and soft strings"*
- State key/scale: *"D minor, harmonic minor scale"*
"""


class HelpScreen(ModalScreen[None]):
    """Full-screen modal with keybinding reference."""

    BINDINGS = [("escape", "dismiss", "Close")]

    def compose(self) -> ComposeResult:
        with Vertical(id="help-dialog"):
            yield Label("text2midi — Help", classes="title")
            table = DataTable(id="help-table", show_cursor=False)
            table.add_columns("Shortcut", "Action")
            yield table
            yield Markdown(_HELP_MARKDOWN)
            yield Button("Close (Esc)", id="btn-close-help")

    def on_mount(self) -> None:
        table = self.query_one("#help-table", DataTable)
        shortcuts = [
            ("Ctrl+G", "Focus prompt & generate"),
            ("Ctrl+R", "Random (Surprise Me) prompt"),
            ("Ctrl+D", "Copy MIDI to DAW clipboard"),
            ("Ctrl+H", "Toggle sidebar"),
            ("Ctrl+S", "Open settings (API key)"),
            ("Ctrl+O", "Open output folder"),
            ("Ctrl+Q", "Quit"),
            ("F1", "This help screen"),
        ]
        for key, desc in shortcuts:
            table.add_row(key, desc)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-close-help":
            self.dismiss(None)
