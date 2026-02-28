# -*- coding: utf-8 -*-
"""
API Key Setup & Provider Switcher Widget
=========================================

Configuration for LLM provider and API key.
Supports 15+ providers via the provider catalog.
Collapses after successful save; re-appears on demand (Ctrl+S).

Features
--------
- **Quick-switch buttons** for already-configured providers (one click)
- **Auto-fills saved API keys** when selecting a provider from dropdown
- **Show/Hide key toggle** for verification before saving
- Instant provider switching without re-entering keys
- All changes take effect immediately for subsequent LLM calls
"""

from __future__ import annotations

import logging

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
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

logger = logging.getLogger(__name__)


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
    """Panel for LLM provider setup and quick switching.

    Provides two workflows:
    1. **Quick-switch** — click a button for a previously-configured provider
       to make it the active default instantly (no re-validation needed).
    2. **Configure new** — pick a provider from the dropdown, enter an API
       key, test the connection, and save.  The new provider appears in the
       quick-switch bar for future one-click switching.
    """

    class Configured(Message):
        """Posted when the user successfully saves or switches providers."""

    class RequestShow(Message):
        """Posted when the user wants to change their API key."""

    show_custom = reactive(False)
    show_key = reactive(True)

    # ================================================================== #
    # Layout
    # ================================================================== #

    def compose(self) -> ComposeResult:
        saved_provider = (
            AppSettings.get("primary_provider", "")
            or AppSettings.get("provider", "")
        )
        with Vertical(id="api-key-setup"):
            yield Label("🔑  LLM Provider Settings", classes="title")

            # ── Current provider status line ──
            yield Label("", id="current-provider-label", classes="status-info")

            # ── Quick-switch bar for already-configured providers ──
            yield Label(
                "Quick Switch (configured providers):",
                id="quick-switch-label",
                classes="dim-label",
            )
            yield Horizontal(id="quick-switch-bar")

            # ── Divider before the new/edit section ──
            yield Label(
                "─" * 40 + "  Configure / Edit  ",
                id="divider-label",
                classes="dim-label",
            )

            # ── Provider dropdown ──
            select_kwargs: dict = {
                "id": "provider-select",
                "prompt": "Choose a provider",
                "allow_blank": True,
            }
            if saved_provider and saved_provider in [v for _, v in _PROVIDERS]:
                select_kwargs["value"] = saved_provider
            yield Select(_PROVIDERS, **select_kwargs)

            # Signup URL hint
            yield Label("", id="signup-url-label", classes="dim-label")

            # ── Key input + toggle ──
            yield Input(
                placeholder="Paste your API key here",
                password=False,
                id="api-key-input",
                value=AppSettings.get("api_key", ""),
            )
            yield Button(
                "🙈 Hide Key",
                id="btn-toggle-key",
                variant="default",
                classes="toggle-key-btn",
            )

            # ── Custom endpoint / model (shown conditionally) ──
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

    # ================================================================== #
    # Lifecycle
    # ================================================================== #

    def on_mount(self) -> None:
        """Populate the quick-switch bar and current-provider label."""
        try:
            self._refresh_current_provider_label()
        except Exception:
            logger.debug("Could not refresh provider label on mount", exc_info=True)
        try:
            self._refresh_quick_switch_bar()
        except Exception:
            logger.debug("Could not refresh quick-switch bar on mount", exc_info=True)

    # ================================================================== #
    # Quick-switch bar helpers
    # ================================================================== #

    def _refresh_quick_switch_bar(self) -> None:
        """Rebuild the quick-switch buttons from saved provider list."""
        try:
            bar = self.query_one("#quick-switch-bar", Horizontal)
        except NoMatches:
            return

        # Remove all existing children — Textual ≥ 0.40 exposes
        # remove_children(); fall back gracefully for older versions.
        try:
            bar.remove_children()
        except Exception:
            # Fallback: remove one-by-one
            for child in list(bar.children):
                try:
                    child.remove()
                except Exception:
                    pass

        configured = AppSettings.get_configured_providers()
        primary = AppSettings.get_primary_provider_id()

        if not configured:
            # Nothing configured — hide the section entirely
            try:
                self.query_one("#quick-switch-label", Label).display = False
                bar.display = False
            except NoMatches:
                pass
            return

        # Ensure section is visible
        try:
            self.query_one("#quick-switch-label", Label).display = True
            bar.display = True
        except NoMatches:
            pass

        for entry in configured:
            pid = entry.get("id", "")
            if not pid:
                continue
            info = PROVIDER_MAP.get(pid)
            display_name = info.display_name if info else pid.title()
            is_active = pid == primary
            variant = "success" if is_active else "default"
            label_text = f"✓ {display_name}" if is_active else display_name
            btn = Button(
                label_text,
                id=f"quick-switch-{pid}",
                variant=variant,
                classes="quick-switch-btn",
            )
            bar.mount(btn)

    def _refresh_current_provider_label(self) -> None:
        """Update the label that shows the currently active provider."""
        try:
            label = self.query_one("#current-provider-label", Label)
        except NoMatches:
            return

        active = LLMConfig.DEFAULT_PROVIDER
        if not active:
            label.update("⚠️  No provider active — configure one below.")
            return

        info = PROVIDER_MAP.get(active)
        name = info.display_name if info else active.title()

        # Try to find the model name
        model = ""
        for entry in AppSettings.get_configured_providers():
            if entry.get("id") == active:
                model = entry.get("model", "")
                break
        if not model and info:
            model = info.default_model

        count = len(AppSettings.get_configured_providers())
        label.update(
            f"✅ Active: {name} ({model})  │  {count} provider(s) configured"
        )

    # ================================================================== #
    # Saved-key lookup
    # ================================================================== #

    def _get_saved_provider_data(
        self, provider_id: str
    ) -> tuple[str, str, str]:
        """Return ``(api_key, endpoint, model)`` saved for *provider_id*.

        Returns ``("", "", "")`` when the provider has no saved entry.
        """
        for entry in AppSettings.get_configured_providers():
            if entry.get("id") == provider_id:
                return (
                    entry.get("api_key", ""),
                    entry.get("endpoint", ""),
                    entry.get("model", ""),
                )
        return ("", "", "")

    # ================================================================== #
    # Select-changed  (dropdown)
    # ================================================================== #

    def on_select_changed(self, event: Select.Changed) -> None:
        """React to a provider being chosen in the dropdown.

        - Shows/hides optional fields (endpoint, model, API key).
        - **Auto-fills** saved API key, endpoint, and model when available
          so returning users don't have to paste the key again.
        - Updates the signup-URL hint.
        """
        if event.select.id != "provider-select":
            return

        provider_id = event.value
        info = (
            PROVIDER_MAP.get(provider_id)
            if provider_id is not Select.BLANK
            else None
        )

        # ── Show/hide custom fields ──────────────────────────
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

        # ── Show/hide API-key input + toggle (Ollama needs none) ──
        try:
            key_input = self.query_one("#api-key-input", Input)
            toggle_btn = self.query_one("#btn-toggle-key", Button)
            if is_ollama:
                key_input.display = False
                toggle_btn.display = False
            else:
                key_input.display = True
                toggle_btn.display = True
        except NoMatches:
            pass

        # ── Auto-fill saved key / endpoint / model ────────────
        if provider_id is not Select.BLANK:
            saved_key, saved_endpoint, saved_model = self._get_saved_provider_data(
                provider_id
            )
            try:
                ki = self.query_one("#api-key-input", Input)
                ki.value = saved_key  # empty string resets the field
            except NoMatches:
                pass
            try:
                ei = self.query_one("#custom-endpoint-input", Input)
                ei.value = saved_endpoint if saved_endpoint else ""
            except NoMatches:
                pass
            try:
                mi = self.query_one("#custom-model-input", Input)
                mi.value = saved_model if saved_model else ""
            except NoMatches:
                pass

        # ── Signup URL hint ───────────────────────────────────
        try:
            url_label = self.query_one("#signup-url-label", Label)
            if info and info.signup_url:
                if info.is_local:
                    url_label.update(f"Install: {info.signup_url}")
                else:
                    url_label.update(f"Get key: {info.signup_url}")
            elif info and info.is_local:
                url_label.update("No API key needed")
            else:
                url_label.update("")
        except NoMatches:
            pass

    # ================================================================== #
    # Button pressed
    # ================================================================== #

    def on_button_pressed(self, event: Button.Pressed) -> None:
        btn_id = event.button.id or ""

        # ── Toggle key visibility ──
        if btn_id == "btn-toggle-key":
            try:
                key_input = self.query_one("#api-key-input", Input)
                key_input.password = not key_input.password
                event.button.label = (
                    "👁 Show Key" if key_input.password else "🙈 Hide Key"
                )
            except NoMatches:
                pass
            return

        # ── Quick-switch button ──
        if btn_id.startswith("quick-switch-"):
            target_pid = btn_id[len("quick-switch-"):]
            self._do_quick_switch(target_pid)
            return

        # ── Test & Save ───────────
        if btn_id == "btn-save-key":
            self._do_test_and_save()
            return

    # ================================================================== #
    # Quick switch (one-click provider change)
    # ================================================================== #

    def _do_quick_switch(self, provider_id: str) -> None:
        """Switch the default provider to *provider_id* instantly.

        The provider must already have a saved API key (or be a local
        provider like Ollama).  No re-validation is performed — the key
        was already validated when it was first saved.
        """
        saved_key, saved_endpoint, saved_model = self._get_saved_provider_data(
            provider_id
        )
        info = PROVIDER_MAP.get(provider_id)
        is_local = info.is_local if info else False

        if not saved_key and not is_local:
            display_name = info.display_name if info else provider_id.title()
            self.notify(
                f"No saved API key for {display_name}. "
                "Please configure it using the form below.",
                severity="warning",
            )
            # Pre-select the provider in the dropdown so user can fill it in
            try:
                self.query_one("#provider-select", Select).value = provider_id
            except NoMatches:
                pass
            return

        # Already the active provider?
        if AppSettings.get_primary_provider_id() == provider_id:
            display_name = info.display_name if info else provider_id.title()
            self.notify(f"{display_name} is already active.", severity="information")
            return

        self._set_status("⏳ Switching provider…")

        try:
            # Persist the switch
            AppSettings.set("primary_provider", provider_id)
            AppSettings.update(
                provider=provider_id,
                api_key=saved_key,
                custom_endpoint=saved_endpoint,
                custom_model=saved_model,
            )
            AppSettings.save()
            AppSettings.apply_to_environment()

            # Re-initialise LLM runtime
            LLMConfig.initialize()

            active = LLMConfig.DEFAULT_PROVIDER or "none"
            display_name = info.display_name if info else active.title()

            # Refresh all UI elements
            self._refresh_quick_switch_bar()
            self._refresh_current_provider_label()
            self._set_status(f"✅ Switched to {display_name}")

            logger.info("Quick-switched to provider %s", provider_id)
            self.notify(f"Switched to {display_name.upper()}", severity="information")
            self.post_message(self.Configured())
        except Exception as exc:
            logger.exception("Quick-switch to %s failed: %s", provider_id, exc)
            self._set_status(f"❌ Switch failed: {str(exc)[:100]}")
            self.notify(f"Switch failed: {str(exc)[:60]}", severity="error")

    # ================================================================== #
    # Test & Save flow
    # ================================================================== #

    def _do_test_and_save(self) -> None:
        """Validate the API key via a real LLM call, then save."""
        try:
            provider_sel = self.query_one("#provider-select", Select)
            key_input = self.query_one("#api-key-input", Input)
        except NoMatches:
            self.notify("UI error: widgets not found.", severity="error")
            return

        provider_id = provider_sel.value
        api_key = key_input.value.strip()
        info = (
            PROVIDER_MAP.get(provider_id)
            if provider_id is not Select.BLANK
            else None
        )

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
            custom_endpoint = self.query_one(
                "#custom-endpoint-input", Input
            ).value.strip()
            custom_model = self.query_one(
                "#custom-model-input", Input
            ).value.strip()
        except NoMatches:
            pass

        # Auto-set endpoint for minimax if missing
        if info and info.needs_endpoint and not is_ollama and not custom_endpoint:
            if provider_id == "minimax":
                custom_endpoint = "https://api.minimaxi.chat/v1"
            elif provider_id not in ("minimax",):
                self.notify(
                    "Endpoint URL is required for this provider.",
                    severity="error",
                )
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

        self._set_status("⏳ Testing connection…")

        # Validate via a real API call
        from src.config.providers import validate_api_key

        test_key = api_key if api_key else ("ollama" if is_ollama else "")
        try:
            success, message = validate_api_key(
                provider_id=provider_id,
                api_key=test_key,
                model=litellm_model,
                base_url=custom_endpoint,
            )
        except Exception as exc:
            logger.exception("validate_api_key raised: %s", exc)
            success, message = False, f"Validation error: {str(exc)[:150]}"

        if success:
            self._set_status(f"✅ {message}")
        else:
            self._set_status(f"❌ {message}")
            self.notify(f"Connection failed: {message}", severity="error")
            return

        # ── Persist ──────────────────────────────────────────
        try:
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

            # Re-initialise LLM runtime
            LLMConfig.initialize()

            active = LLMConfig.DEFAULT_PROVIDER or "none"
            display_name = info.display_name if info else active.title()

            # Refresh UI
            self._refresh_quick_switch_bar()
            self._refresh_current_provider_label()

            logger.info("Saved provider %s as primary", provider_id)
            self.notify(
                f"Connected to {display_name.upper()}", severity="information"
            )
            self.post_message(self.Configured())
        except Exception as exc:
            logger.exception("Failed to save provider %s: %s", provider_id, exc)
            self._set_status(f"❌ Save failed: {str(exc)[:100]}")
            self.notify(f"Save failed: {str(exc)[:60]}", severity="error")

    # ================================================================== #
    # Status label helper
    # ================================================================== #

    def _set_status(self, text: str) -> None:
        """Update the ``#status-label`` safely."""
        try:
            self.query_one("#status-label", Label).update(text)
        except NoMatches:
            pass
