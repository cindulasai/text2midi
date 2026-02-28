# -*- coding: utf-8 -*-
"""
API Key Setup Widget
One-time configuration for LLM provider and API key.
Supports 15+ providers via the provider catalog.
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
from src.config.provider_catalog import (
    ALL_PROVIDERS,
    PROVIDER_MAP,
    TIER1_PROVIDERS,
    TIER2_PROVIDERS,
)


def _build_provider_options() -> list[tuple[str, str]]:
    """Build the Select widget options from the provider catalog."""
    options: list[tuple[str, str]] = []
    # Tier 1 — Featured
    for p in TIER1_PROVIDERS:
        tag = "★ FREE" if p.is_free else "★"
        options.append((f"{tag} {p.display_name}", p.id))
    # Tier 2 — More
    for p in TIER2_PROVIDERS:
        options.append((f"  {p.display_name}", p.id))
    return options


_PROVIDERS = _build_provider_options()


class ApiKeySetup(Static):
    """Panel for first-time LLM provider + API key configuration."""

    class Configured(Message):
        """Posted when the user successfully saves credentials."""

    class RequestShow(Message):
        """Posted when the user wants to change their API key."""

    show_custom = reactive(False)
    show_key = reactive(True)

    def compose(self) -> ComposeResult:
        saved_provider = AppSettings.get("primary_provider", "") or AppSettings.get("provider", "")
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

            # Signup URL hint
            yield Label("", id="signup-url-label", classes="dim-label")

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

            yield Button("Test & Save", id="btn-save-key", variant="primary")
            yield Label("", id="status-label")

    # -------------------------------------------------------------- #
    # Reactivity
    # -------------------------------------------------------------- #

    def on_select_changed(self, event: Select.Changed) -> None:
        if event.select.id != "provider-select":
            return

        provider_id = event.value
        info = PROVIDER_MAP.get(provider_id) if provider_id is not Select.BLANK else None

        # Show/hide custom fields
        needs_custom = info.needs_endpoint if info else False
        is_ollama = info.id == "ollama" if info else False
        try:
            fields = self.query_one("#custom-fields")
            if needs_custom or provider_id in ("custom", "openai_custom"):
                fields.add_class("visible")
            else:
                fields.remove_class("visible")
        except NoMatches:
            pass

        # Show/hide API key field (Ollama doesn't need one)
        try:
            key_input = self.query_one("#api-key-input", Input)
            if is_ollama:
                key_input.display = False
            else:
                key_input.display = True
        except NoMatches:
            pass

        # Update signup URL
        try:
            url_label = self.query_one("#signup-url-label", Label)
            if info and info.signup_url:
                url_label.update(f"Get key: {info.signup_url}")
            elif info and info.is_local:
                url_label.update(f"Install: {info.signup_url}" if info.signup_url else "No API key needed")
            else:
                url_label.update("")
        except NoMatches:
            pass

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id != "btn-save-key":
            return

        provider_sel = self.query_one("#provider-select", Select)
        key_input = self.query_one("#api-key-input", Input)

        provider_id = provider_sel.value
        api_key = key_input.value.strip()
        info = PROVIDER_MAP.get(provider_id) if provider_id is not Select.BLANK else None

        if provider_id is Select.BLANK:
            self.notify("Please select a provider.", severity="error")
            return

        # Ollama doesn't need an API key
        is_ollama = info.id == "ollama" if info else False
        if not is_ollama and not api_key:
            self.notify("Please enter your API key.", severity="error")
            return

        # Gather optional fields
        custom_endpoint = ""
        custom_model = ""
        try:
            custom_endpoint = self.query_one("#custom-endpoint-input", Input).value.strip()
            custom_model = self.query_one("#custom-model-input", Input).value.strip()
        except NoMatches:
            pass

        if info and info.needs_endpoint and not is_ollama and not custom_endpoint:
            if provider_id == "minimax":
                custom_endpoint = "https://api.minimaxi.chat/v1"
            elif provider_id not in ("minimax",):
                self.notify("Endpoint URL is required for this provider.", severity="error")
                return

        # Default endpoint for Ollama
        if is_ollama and not custom_endpoint:
            custom_endpoint = "http://localhost:11434"

        # Default model from catalog
        if not custom_model and info:
            custom_model = info.default_model

        # Build litellm model string for validation
        litellm_model = custom_model
        if info and info.litellm_prefix and "/" not in custom_model:
            litellm_model = f"{info.litellm_prefix}/{custom_model}"
        if provider_id == "minimax":
            litellm_model = f"openai/{custom_model}"

        # Update status
        try:
            status = self.query_one("#status-label", Label)
            status.update("⏳ Testing connection...")
        except NoMatches:
            pass

        # Validate
        from src.config.providers import validate_api_key

        test_key = api_key if api_key else ("ollama" if is_ollama else "")
        success, message = validate_api_key(
            provider_id=provider_id,
            api_key=test_key,
            model=litellm_model,
            base_url=custom_endpoint,
        )

        try:
            status = self.query_one("#status-label", Label)
            if success:
                status.update(f"✅ {message}")
            else:
                status.update(f"❌ {message}")
        except NoMatches:
            pass

        if not success:
            self.notify(f"Connection failed: {message}", severity="error")
            # Still allow saving if user wants
            return

        # Persist using new multi-provider API
        AppSettings.add_provider(
            provider_id=provider_id,
            api_key=api_key,
            model=custom_model,
            endpoint=custom_endpoint,
            set_primary=True,
        )

        # Also update legacy fields for backward compat
        AppSettings.update(
            provider=provider_id,
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
