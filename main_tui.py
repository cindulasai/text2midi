# -*- coding: utf-8 -*-
"""
text2midi TUI — Modern Terminal User Interface
Powered by Textual with Catppuccin Mocha theme.

Launch: uv run python main_tui.py
   or: uv run text2midi-tui
"""

import logging
import sys
import os
from pathlib import Path

# Load .env before anything else
from dotenv import load_dotenv
load_dotenv()

# ── TUI-safe logging ──────────────────────────────────────────────
# Redirect ALL logging to a file so nothing corrupts the Textual TUI.
# The regular CLI (main.py) still uses stdout via setup_logging().
from src.config.log import setup_logging_for_tui
setup_logging_for_tui()

logger = logging.getLogger(__name__)

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.widgets import Footer, Header

from src.config.settings import AppSettings
from src.config.llm import LLMConfig
from src.tui.widgets.api_key_setup import ApiKeySetup
from src.tui.widgets.prompt_input import PromptInput
from src.tui.widgets.output_panel import OutputPanel
from src.tui.widgets.sidebar import Sidebar
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
        Binding("ctrl+d", "copy_to_daw", "Copy to DAW", show=True),
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
            self._push_model_info()
            provider = LLMConfig.DEFAULT_PROVIDER.upper()
            avail = ", ".join(LLMConfig.AVAILABLE_PROVIDERS)
            self.notify(f"Connected to {provider} (available: {avail})", severity="information")
        else:
            self.notify(
                "Welcome! Choose an AI provider below to get started. "
                "Groq is free and recommended.",
                severity="warning",
            )

    # ------------------------------------------------------------------ #
    # Message handlers
    # ------------------------------------------------------------------ #

    def on_api_key_setup_configured(self, event: ApiKeySetup.Configured) -> None:
        """API key was saved successfully."""
        self._collapse_api_panel()
        self._push_model_info()

    def on_prompt_input_generate_requested(
        self, event: PromptInput.GenerateRequested
    ) -> None:
        """The user clicked Generate."""
        self._start_generation(event.prompt)

    def on_sidebar_preset_selected(self, event: Sidebar.PresetSelected) -> None:
        self.query_one("#prompt-widget", PromptInput).set_prompt(event.prompt)

    def on_sidebar_history_selected(self, event: Sidebar.HistorySelected) -> None:
        self.query_one("#prompt-widget", PromptInput).set_prompt(event.prompt)

    # ---- Worker messages ---- #

    def on_node_completed(self, event: NodeCompleted) -> None:
        self.query_one("#prompt-widget", PromptInput).update_progress(event.node_name)

    def on_generation_complete(self, event: GenerationComplete) -> None:
        state = event.result_state
        prompt_widget = self.query_one("#prompt-widget", PromptInput)
        output_widget = self.query_one("#output-widget", OutputPanel)

        # Extract quality score
        quality = None
        qr = state.get("quality_report")
        if qr:
            quality = qr.overall_score

        prompt_widget.mark_complete(quality)
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

        prompt_widget.mark_error(event.error)
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

    def action_copy_to_daw(self) -> None:
        output_widget = self.query_one("#output-widget", OutputPanel)
        output_widget._copy_to_daw()

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
        # Refresh the quick-switch bar and provider label when panel opens
        try:
            widget._refresh_current_provider_label()
            widget._refresh_quick_switch_bar()
        except Exception:
            pass

    def _push_model_info(self) -> None:
        """Send the active model name to the prompt widget."""
        provider = LLMConfig.DEFAULT_PROVIDER or ""
        if not provider:
            return

        # Try to get model name from AppSettings first
        try:
            from src.config.settings import AppSettings as _AS
            from src.config.provider_catalog import get_provider as _gp

            providers_list = _AS.get("providers", [])
            for entry in providers_list:
                if entry.get("id") == provider:
                    model = entry.get("model", "")
                    if model:
                        self.query_one("#prompt-widget", PromptInput).set_model_info(provider, model)
                        return

            # Fallback: use catalog default
            info = _gp(provider)
            if info:
                self.query_one("#prompt-widget", PromptInput).set_model_info(provider, info.default_model)
                return
        except Exception:
            pass

        # Legacy fallback
        if provider == "minimax":
            model = "MiniMax-M2.5"
        elif provider == "groq":
            model = LLMConfig.CURRENT_GROQ_MODEL
        elif provider == "openai_custom":
            model = LLMConfig.OPENAI_CUSTOM_MODEL
        else:
            model = provider
        self.query_one("#prompt-widget", PromptInput).set_model_info(provider, model)

    # ------------------------------------------------------------------ #
    # Global safety net — catch any unhandled exception so the TUI
    # never crashes with an ugly traceback.
    # ------------------------------------------------------------------ #

    def on_exception(self, error: Exception) -> None:  # type: ignore[override]
        """Last-resort handler — log and show a brief toast instead of crashing."""
        logger.exception("Unhandled TUI error: %s", error)
        try:
            self.notify(str(error)[:80], severity="error")
        except Exception:
            pass  # if even notify fails, swallow silently

    def _start_generation(self, prompt: str) -> None:
        """Kick off the generation pipeline in a background worker."""
        if not LLMConfig.DEFAULT_PROVIDER:
            self.notify(
                "No LLM provider configured. Press Ctrl+S to set up.",
                severity="error",
            )
            return

        prompt_widget = self.query_one("#prompt-widget", PromptInput)
        output_widget = self.query_one("#output-widget", OutputPanel)

        prompt_widget.set_generating(True)
        prompt_widget.show_progress()
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
