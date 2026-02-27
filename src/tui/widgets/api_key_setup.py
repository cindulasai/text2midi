# -*- coding: utf-8 -*-
"""
API Key Setup Widget
One-time configuration for LLM provider and API key.
Collapses after successful save; re-appears on demand.
"""

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.css.query import NoMatches
from textual.message import Message
from textual.reactive import reactive
from textual.widgets import Button, Input, Label, Select, Static

from src.config.settings import AppSettings
from src.config.llm import LLMConfig


_PROVIDERS = [
    ("MiniMax M2.5", "minimax"),
    ("Groq (Llama)", "groq"),
    ("OpenAI-compatible", "openai_custom"),
]


class ApiKeySetup(Static):
    """Panel for first-time LLM provider + API key configuration."""

    class Configured(Message):
        """Posted when the user successfully saves credentials."""

    class RequestShow(Message):
        """Posted when the user wants to change their API key."""

    show_custom = reactive(False)

    def compose(self) -> ComposeResult:
        saved_provider = AppSettings.get("provider")
        with Vertical(id="api-key-setup"):
            yield Label("🔑  LLM Provider Setup", classes="title")
            select_kwargs = {
                "id": "provider-select",
                "prompt": "Choose a provider",
                "allow_blank": True,
            }
            if saved_provider and saved_provider in [v for _, v in _PROVIDERS]:
                select_kwargs["value"] = saved_provider
            yield Select(
                _PROVIDERS,
                **select_kwargs,
            )
            yield Input(
                placeholder="Paste your API key here",
                password=True,
                id="api-key-input",
                value=AppSettings.get("api_key", ""),
            )
            with Vertical(id="custom-fields", classes="conditional-fields"):
                yield Input(
                    placeholder="Endpoint URL (e.g. http://localhost:1234/v1)",
                    id="custom-endpoint-input",
                    value=AppSettings.get("custom_endpoint", ""),
                )
                yield Input(
                    placeholder="Model name (e.g. gpt-4, llama3)",
                    id="custom-model-input",
                    value=AppSettings.get("custom_model", ""),
                )
            yield Button("Save & Connect", id="btn-save-key", variant="primary")

    # -------------------------------------------------------------- #
    # Reactivity
    # -------------------------------------------------------------- #

    def on_select_changed(self, event: Select.Changed) -> None:
        if event.select.id == "provider-select":
            self.show_custom = event.value == "openai_custom"
            try:
                fields = self.query_one("#custom-fields")
                if self.show_custom:
                    fields.add_class("visible")
                else:
                    fields.remove_class("visible")
            except NoMatches:
                pass

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id != "btn-save-key":
            return

        provider_sel = self.query_one("#provider-select", Select)
        key_input = self.query_one("#api-key-input", Input)

        provider = provider_sel.value
        api_key = key_input.value.strip()

        if provider is Select.BLANK or not api_key:
            self.notify("Please select a provider and enter your API key.", severity="error")
            return

        # Gather optional fields
        custom_endpoint = ""
        custom_model = ""
        if provider == "openai_custom":
            try:
                custom_endpoint = self.query_one("#custom-endpoint-input", Input).value.strip()
                custom_model = self.query_one("#custom-model-input", Input).value.strip()
            except NoMatches:
                pass
            if not custom_endpoint:
                self.notify("Custom endpoint URL is required.", severity="error")
                return

        # Persist
        AppSettings.update(
            provider=provider,
            api_key=api_key,
            custom_endpoint=custom_endpoint,
            custom_model=custom_model,
        )
        AppSettings.save()
        AppSettings.apply_to_environment()

        # Re-initialize LLM
        LLMConfig.initialize()

        active = LLMConfig.DEFAULT_PROVIDER or "none"
        self.notify(f"Connected to {active.upper()}", severity="information")
        self.post_message(self.Configured())
