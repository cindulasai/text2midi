# -*- coding: utf-8 -*-
"""
text2midi TUI — Modern Terminal User Interface
Powered by Textual with Catppuccin Mocha theme.

Launch: uv run python main_tui.py
   or: uv run text2midi-tui
"""

import sys
import os
from pathlib import Path

# Ensure project root is on sys.path
sys.path.insert(0, str(Path(__file__).parent))

# Load .env before anything else
from dotenv import load_dotenv
load_dotenv()

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.widgets import Footer, Header

from src.config.settings import AppSettings
from src.config.llm import LLMConfig
from src.tui.widgets.api_key_setup import ApiKeySetup
from src.tui.widgets.prompt_input import PromptInput
from src.tui.widgets.progress_panel import ProgressPanel
from src.tui.widgets.output_panel import OutputPanel
from src.tui.widgets.sidebar import Sidebar
from src.tui.widgets.suggestion_carousel import SuggestionCarousel
from src.tui.widgets.help_screen import HelpScreen
from src.tui.history import HistoryManager
from src.tui.workers.generation_worker import (
    run_generation,
    NodeCompleted,
    GenerationComplete,
    GenerationError,
)


class Text2MidiApp(App):
    """text2midi — AI-Powered MIDI Composer TUI."""

    TITLE = "text2midi"
    SUB_TITLE = "AI-Powered MIDI Composer"
    CSS_PATH = "src/tui/styles.tcss"

    BINDINGS = [
        Binding("ctrl+g", "generate", "Generate", show=True),
        Binding("ctrl+r", "surprise", "Random Prompt", show=True),
        Binding("ctrl+h", "toggle_sidebar", "Toggle Sidebar", show=True),
        Binding("ctrl+s", "show_settings", "Settings", show=True),
        Binding("ctrl+o", "open_output", "Open Output", show=True),
        Binding("f1", "show_help", "Help", show=True),
        Binding("ctrl+q", "quit", "Quit", show=True),
    ]

    # ------------------------------------------------------------------ #
    # Layout
    # ------------------------------------------------------------------ #

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Horizontal(id="main-horizontal"):
            yield Sidebar(id="sidebar")
            with Vertical(id="main-content"):
                yield ApiKeySetup(id="api-key-widget")
                yield PromptInput(id="prompt-widget")
                yield SuggestionCarousel(id="carousel-widget")
                yield ProgressPanel(id="progress-widget")
                yield OutputPanel(id="output-widget")
        yield Footer()

    # ------------------------------------------------------------------ #
    # Lifecycle
    # ------------------------------------------------------------------ #

    def on_mount(self) -> None:
        """Initialise LLM and conditionally show the API key panel."""
        # Load persistent settings and push to environment
        AppSettings.load()
        if AppSettings.is_configured():
            AppSettings.apply_to_environment()

        LLMConfig.initialize()

        # If already configured, collapse the API key panel
        if AppSettings.is_configured() and LLMConfig.DEFAULT_PROVIDER:
            self._collapse_api_panel()
            provider = LLMConfig.DEFAULT_PROVIDER.upper()
            self.notify(f"Connected to {provider}", severity="information")
        else:
            self.notify("Please configure your LLM provider to get started.", severity="warning")

    # ------------------------------------------------------------------ #
    # Message handlers
    # ------------------------------------------------------------------ #

    def on_api_key_setup_configured(self, event: ApiKeySetup.Configured) -> None:
        """API key was saved successfully."""
        self._collapse_api_panel()

    def on_output_panel_change_api_key_requested(
        self, event: OutputPanel.ChangeApiKeyRequested
    ) -> None:
        """User wants to re-enter API key."""
        self._expand_api_panel()

    def on_prompt_input_generate_requested(
        self, event: PromptInput.GenerateRequested
    ) -> None:
        """The user clicked Generate."""
        self._start_generation(event.prompt)

    def on_sidebar_preset_selected(self, event: Sidebar.PresetSelected) -> None:
        self.query_one("#prompt-widget", PromptInput).set_prompt(event.prompt)

    def on_sidebar_history_selected(self, event: Sidebar.HistorySelected) -> None:
        self.query_one("#prompt-widget", PromptInput).set_prompt(event.prompt)

    def on_suggestion_carousel_chip_selected(
        self, event: SuggestionCarousel.ChipSelected
    ) -> None:
        self.query_one("#prompt-widget", PromptInput).set_prompt(event.text)

    # ---- Worker messages ---- #

    def on_node_completed(self, event: NodeCompleted) -> None:
        self.query_one("#progress-widget", ProgressPanel).update_progress(event.node_name)

    def on_generation_complete(self, event: GenerationComplete) -> None:
        state = event.result_state
        prompt_widget = self.query_one("#prompt-widget", PromptInput)
        progress_widget = self.query_one("#progress-widget", ProgressPanel)
        output_widget = self.query_one("#output-widget", OutputPanel)

        # Extract quality score
        quality = None
        qr = state.get("quality_report")
        if qr:
            quality = qr.overall_score

        progress_widget.mark_complete(quality)
        output_widget.show_results(state)
        prompt_widget.set_generating(False)

        # Save to history
        genre = ""
        intent = state.get("intent")
        if intent:
            genre = getattr(intent, "genre", "")
        midi_path = state.get("final_midi_path", "")
        HistoryManager.add_entry(
            prompt=state.get("user_prompt", ""),
            genre=genre,
            quality=quality or 0.0,
            midi_path=midi_path,
        )
        self.query_one("#sidebar", Sidebar).refresh_history()

        self.notify("Generation complete!", severity="information")

    def on_generation_error(self, event: GenerationError) -> None:
        prompt_widget = self.query_one("#prompt-widget", PromptInput)
        progress_widget = self.query_one("#progress-widget", ProgressPanel)

        progress_widget.mark_error(event.error)
        prompt_widget.set_generating(False)
        self.notify(f"Error: {event.error}", severity="error")

    # ------------------------------------------------------------------ #
    # Actions (keybindings)
    # ------------------------------------------------------------------ #

    def action_generate(self) -> None:
        prompt_widget = self.query_one("#prompt-widget", PromptInput)
        prompt_widget._do_generate()

    def action_surprise(self) -> None:
        prompt_widget = self.query_one("#prompt-widget", PromptInput)
        prompt_widget._do_surprise()

    def action_toggle_sidebar(self) -> None:
        sidebar = self.query_one("#sidebar", Sidebar)
        sidebar.display = not sidebar.display

    def action_show_settings(self) -> None:
        self._expand_api_panel()

    def action_open_output(self) -> None:
        output_widget = self.query_one("#output-widget", OutputPanel)
        output_widget._open_folder()

    def action_show_help(self) -> None:
        self.push_screen(HelpScreen())

    # ------------------------------------------------------------------ #
    # Internal helpers
    # ------------------------------------------------------------------ #

    def _collapse_api_panel(self) -> None:
        widget = self.query_one("#api-key-widget", ApiKeySetup)
        widget.display = False

    def _expand_api_panel(self) -> None:
        widget = self.query_one("#api-key-widget", ApiKeySetup)
        widget.display = True

    def _start_generation(self, prompt: str) -> None:
        """Kick off the generation pipeline in a background worker."""
        if not LLMConfig.DEFAULT_PROVIDER:
            self.notify(
                "No LLM provider configured. Press Ctrl+S to set up.",
                severity="error",
            )
            return

        prompt_widget = self.query_one("#prompt-widget", PromptInput)
        progress_widget = self.query_one("#progress-widget", ProgressPanel)
        output_widget = self.query_one("#output-widget", OutputPanel)

        prompt_widget.set_generating(True)
        progress_widget.show()
        output_widget.hide()

        # Run the pipeline in a background thread
        self.run_worker(
            run_generation(prompt, self),
            name="generation",
            thread=True,
            exclusive=True,
        )


def main() -> None:
    """Entry point for the TUI application."""
    app = Text2MidiApp()
    app.run()


if __name__ == "__main__":
    main()
