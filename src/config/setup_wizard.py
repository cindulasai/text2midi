# -*- coding: utf-8 -*-
"""
Setup Wizard
============

Interactive first-run setup for configuring an LLM provider.
Works in both CLI (``main.py --setup``) and is called automatically
when no provider is configured.

Designed for **non-technical users** — plain language, numbered menus,
direct signup URLs, and instant key validation.
"""

from __future__ import annotations

import getpass
import logging
import os
import sys
from typing import Optional

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Ollama auto-detection
# ---------------------------------------------------------------------------

def detect_ollama(timeout: float = 2.0) -> Optional[list[str]]:
    """Check if Ollama is running locally and return available model names.

    Returns ``None`` if Ollama is not reachable, or a list of model name
    strings (possibly empty) if the server responds.
    """
    try:
        import httpx

        resp = httpx.get("http://localhost:11434/api/tags", timeout=timeout)
        if resp.status_code == 200:
            data = resp.json()
            models = [m.get("name", "") for m in data.get("models", [])]
            return [m for m in models if m]
        return None
    except Exception:
        return None


# ---------------------------------------------------------------------------
# First-run detection
# ---------------------------------------------------------------------------

def is_first_run() -> bool:
    """Return True if no provider is configured anywhere."""
    try:
        from src.config.settings import AppSettings

        AppSettings.load()
        if AppSettings.is_configured():
            return False
    except Exception:
        pass

    # Also check if legacy env vars are set
    for var in ("MINIMAX_API_KEY", "GROQ_API_KEY", "OPENAI_API_KEY", "ANTHROPIC_API_KEY"):
        if os.environ.get(var):
            return False

    return True


# ---------------------------------------------------------------------------
# Rich console helpers
# ---------------------------------------------------------------------------

def _get_console():
    """Lazy-import Rich console."""
    try:
        from rich.console import Console
        return Console()
    except ImportError:
        return None


def _print(text: str = "", style: str = "") -> None:
    """Print with Rich if available, otherwise plain print."""
    console = _get_console()
    if console and style:
        console.print(text, style=style)
    elif console:
        console.print(text)
    else:
        print(text)


def _input(prompt: str) -> str:
    """Read a line of input."""
    try:
        return input(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        print()
        return ""


def _secure_input(prompt: str) -> str:
    """Read a password/API key without echoing."""
    try:
        return getpass.getpass(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        print()
        return ""


# ---------------------------------------------------------------------------
# Main wizard
# ---------------------------------------------------------------------------

def run_setup_wizard() -> bool:
    """Run the interactive setup wizard.

    Returns True if a provider was configured successfully, False if
    the user cancelled or no provider was set up.
    """
    from src.config.provider_catalog import (
        ALL_PROVIDERS,
        PROVIDER_MAP,
        TIER1_PROVIDERS,
        TIER2_PROVIDERS,
        ProviderInfo,
    )
    from src.config.settings import AppSettings
    from src.config.providers import validate_api_key

    # ── Welcome banner ──────────────────────────────────────────────
    print()
    _print("=" * 64, "bold cyan")
    _print("  Welcome to text2midi!", "bold cyan")
    _print("  AI-Powered MIDI Composer", "cyan")
    _print("=" * 64, "bold cyan")
    print()
    _print(
        "  This app uses an AI model to turn your text descriptions\n"
        "  into music. To get started, you need an API key from one\n"
        "  of the supported AI providers.\n",
    )
    _print(
        "  An API key is like a password that lets this app talk to\n"
        "  an AI service. Most providers offer a FREE tier — you\n"
        "  won't need a credit card to get started.\n",
    )

    # ── Ollama detection ────────────────────────────────────────────
    ollama_models = detect_ollama()
    if ollama_models:
        _print(
            f"  [Auto-detected] Ollama is running locally with "
            f"{len(ollama_models)} model(s)!",
            "bold green",
        )
        print()

    # ── Provider selection ──────────────────────────────────────────
    _print("Choose your AI provider:", "bold")
    print()

    # Tier 1
    _print("  ── Recommended (easy to start) ──", "dim")
    menu_items: list[ProviderInfo] = []
    idx = 1
    for p in TIER1_PROVIDERS:
        tag = "[FREE] " if p.is_free else "[PAID] "
        extra = ""
        if p.id == "ollama" and ollama_models:
            extra = f"  ({len(ollama_models)} models ready)"
        elif p.id == "ollama":
            extra = "  (not detected — install from ollama.com)"
        _print(f"  {idx}. {tag}{p.display_name:<22} {p.description}{extra}")
        menu_items.append(p)
        idx += 1

    print()
    _print("  ── More providers ──", "dim")
    for p in TIER2_PROVIDERS:
        _print(f"  {idx}. {p.display_name:<22} {p.description}")
        menu_items.append(p)
        idx += 1

    print()
    _print(f"  0. Skip setup (configure later with --setup)")
    print()

    # ── Get choice ──────────────────────────────────────────────────
    while True:
        choice_str = _input("Enter number [1]: ")
        if not choice_str:
            choice_str = "1"  # default to Groq
        if choice_str == "0":
            _print("\nSetup skipped. Run again with --setup when ready.", "yellow")
            return False
        try:
            choice = int(choice_str)
            if 1 <= choice <= len(menu_items):
                selected = menu_items[choice - 1]
                break
            else:
                _print(f"  Please enter a number between 0 and {len(menu_items)}.", "red")
        except ValueError:
            _print("  Please enter a number.", "red")

    _print(f"\n  Selected: {selected.display_name}", "bold green")

    # ── Special handling: Ollama (no API key needed) ────────────────
    if selected.id == "ollama":
        return _setup_ollama(selected, ollama_models)

    # ── Show signup URL ─────────────────────────────────────────────
    if selected.signup_url:
        print()
        _print(f"  Get your API key here:", "bold")
        _print(f"  {selected.signup_url}", "underline blue")
        print()
        _print(
            "  1. Open the URL above in your browser\n"
            "  2. Sign up or log in\n"
            "  3. Create an API key\n"
            "  4. Copy it and paste it below\n",
        )

    # ── API key input ───────────────────────────────────────────────
    api_key = ""
    while not api_key:
        api_key = _input("  Paste your API key: ")
        if not api_key:
            retry = _input("  No key entered. Try again? [Y/n]: ")
            if retry.lower() == "n":
                _print("\nSetup cancelled.", "yellow")
                return False

    # Show masked key so user can confirm it was pasted correctly
    if len(api_key) > 10:
        masked = api_key[:6] + "..." + api_key[-4:]
    else:
        masked = "*" * len(api_key)
    _print(f"  Key received: {masked}", "dim")

    # ── Model selection ─────────────────────────────────────────────
    model = selected.default_model
    if selected.example_models and len(selected.example_models) > 1:
        print()
        _print(f"  Available models for {selected.display_name}:", "bold")
        for i, m in enumerate(selected.example_models, 1):
            default_tag = " (default)" if m == selected.default_model else ""
            _print(f"    {i}. {m}{default_tag}")
        model_choice = _input(f"  Choose model [1]: ")
        if model_choice:
            try:
                mi = int(model_choice)
                if 1 <= mi <= len(selected.example_models):
                    model = selected.example_models[mi - 1]
            except ValueError:
                pass
    print()

    # Build the litellm model string
    litellm_model = model
    if selected.litellm_prefix and "/" not in model:
        litellm_model = f"{selected.litellm_prefix}/{model}"

    # For MiniMax, route through openai compat prefix
    base_url = ""
    if selected.id == "minimax":
        litellm_model = f"openai/{model}"
        base_url = "https://api.minimaxi.chat/v1"

    # Custom endpoint for providers that need it
    if selected.needs_endpoint and selected.id != "ollama" and selected.id != "minimax":
        endpoint = _input("  Enter endpoint URL: ")
        if endpoint:
            base_url = endpoint

    # ── Validate key ────────────────────────────────────────────────
    _print("  Testing connection...", "dim")
    success, message = validate_api_key(
        provider_id=selected.id,
        api_key=api_key,
        model=litellm_model,
        base_url=base_url,
    )

    if success:
        _print(f"  ✅ {message}", "bold green")
    else:
        _print(f"  ❌ {message}", "bold red")
        retry = _input("  Save anyway? [y/N]: ")
        if retry.lower() != "y":
            _print("\nSetup cancelled. Run --setup to try again.", "yellow")
            return False

    # ── Save ────────────────────────────────────────────────────────
    AppSettings.load()
    AppSettings.add_provider(
        provider_id=selected.id,
        api_key=api_key,
        model=model,
        endpoint=base_url,
        set_primary=True,
    )
    AppSettings.save()
    AppSettings.apply_to_environment()

    print()
    _print("=" * 64, "bold green")
    _print("  ✅ Setup complete!", "bold green")
    _print(f"  Provider: {selected.display_name}", "green")
    _print(f"  Model:    {model}", "green")
    _print("=" * 64, "bold green")
    _print(
        "\n  You're all set! Start creating music by typing a description.\n"
        "  Run --setup anytime to change providers or add backups.\n",
    )

    return True


# ---------------------------------------------------------------------------
# Ollama-specific setup
# ---------------------------------------------------------------------------

def _setup_ollama(
    provider: "ProviderInfo",
    detected_models: Optional[list[str]],
) -> bool:
    """Handle Ollama setup (no API key needed)."""
    from src.config.settings import AppSettings

    if not detected_models:
        _print(
            "\n  Ollama is not running or not installed.\n"
            "  Install it from: https://ollama.com\n"
            "\n"
            "  After installing, run these commands:\n"
            "    ollama serve        (start the server)\n"
            "    ollama pull llama3.2  (download a model)\n"
            "\n"
            "  Then run --setup again.\n",
            "yellow",
        )
        return False

    print()
    _print(f"  Ollama is running with {len(detected_models)} model(s):", "bold green")
    for i, m in enumerate(detected_models, 1):
        _print(f"    {i}. {m}")

    model = detected_models[0]
    if len(detected_models) > 1:
        choice = _input(f"  Choose model [1]: ")
        if choice:
            try:
                idx = int(choice)
                if 1 <= idx <= len(detected_models):
                    model = detected_models[idx - 1]
            except ValueError:
                pass

    # Test connection
    _print("\n  Testing connection...", "dim")
    from src.config.providers import validate_api_key

    success, message = validate_api_key(
        provider_id="ollama",
        api_key="ollama",  # LiteLLM uses "ollama" as a dummy key
        model=f"ollama/{model}",
        base_url="http://localhost:11434",
    )

    if success:
        _print(f"  ✅ {message}", "bold green")
    else:
        _print(f"  ❌ {message}", "bold red")
        _print("  Make sure 'ollama serve' is running.", "yellow")
        return False

    # Save
    AppSettings.load()
    AppSettings.add_provider(
        provider_id="ollama",
        api_key="",
        model=model,
        endpoint="http://localhost:11434",
        set_primary=True,
    )
    AppSettings.save()
    AppSettings.apply_to_environment()

    print()
    _print("=" * 64, "bold green")
    _print("  ✅ Setup complete!", "bold green")
    _print(f"  Provider: Ollama (local)", "green")
    _print(f"  Model:    {model}", "green")
    _print("  No API key needed — everything runs on your machine!", "green")
    _print("=" * 64, "bold green")
    print()

    return True
