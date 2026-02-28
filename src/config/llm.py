# -*- coding: utf-8 -*-
"""
LLM Configuration and Management
=================================

Handles provider initialization and LLM calls.

Supports **100+ LLM providers** via LiteLLM:
  - Groq, OpenAI, Anthropic, Google Gemini, Mistral, Cohere, DeepSeek,
    Together AI, Fireworks, Perplexity, OpenRouter, Ollama (local), …

Provider priority is determined by registration order.  The *primary*
provider from ``AppSettings`` is registered first; additional configured
providers follow as automatic fallbacks.

Delegates to ``LiteLLMProvider`` in ``src.config.providers``.

Backward compatibility
----------------------
Legacy environment variables (``MINIMAX_API_KEY``, ``GROQ_API_KEY``,
``OPENAI_CUSTOM_*``) are still honoured so existing setups keep working.
"""

import logging
import os
from typing import Optional

from src.config.providers import (
    GroqProvider,
    LiteLLMProvider,
    MinimaxProvider,
    OpenAICustomProvider,
    ProviderRegistry,
)
from src.config.provider_catalog import PROVIDER_MAP, get_provider

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Singleton registry — populated by LLMConfig.initialize()
# ---------------------------------------------------------------------------

_registry = ProviderRegistry()


class LLMConfig:
    """Runtime configuration for LLM provider selection.

    Call ``initialize()`` once at startup (after ``AppSettings.apply_to_environment()``
    if using the TUI).  The method reads configured providers from
    ``AppSettings`` **and** scans legacy env-vars for backward compat.

    Public attributes are kept for backward-compatibility with code that
    reads ``LLMConfig.AVAILABLE_PROVIDERS``, ``LLMConfig.DEFAULT_PROVIDER``,
    etc.
    """

    DEFAULT_PROVIDER: Optional[str] = None
    AVAILABLE_PROVIDERS: list = []

    # Groq helpers (backward compat)
    GROQ_MODELS = ["llama-3.3-70b-versatile", "llama-4-maverick"]
    CURRENT_GROQ_MODEL = "llama-3.3-70b-versatile"

    # Legacy env-var keys (kept so old .env files still work)
    MINIMAX_API_KEY: str = ""
    GROQ_API_KEY: str = ""
    OPENAI_CUSTOM_API_KEY: str = ""
    OPENAI_CUSTOM_ENDPOINT: str = ""
    OPENAI_CUSTOM_MODEL: str = ""

    @classmethod
    def initialize(cls) -> None:
        """Detect and register available LLM providers.

        Resolution order:
        1. Multi-provider list from ``AppSettings["providers"]`` (new format).
        2. Single-provider from ``AppSettings["provider"]`` (migration compat).
        3. Legacy environment variables (``MINIMAX_API_KEY``, ``GROQ_API_KEY``, …).

        The first successfully registered provider becomes the default.
        """
        global _registry
        _registry = ProviderRegistry()
        cls.AVAILABLE_PROVIDERS.clear()

        # ── 1. New multi-provider settings ──────────────────────────
        registered_ids: set[str] = set()
        try:
            from src.config.settings import AppSettings

            providers_list = AppSettings.get("providers", [])
            primary = AppSettings.get("primary_provider", "")

            # Register primary first (highest priority)
            if primary:
                for entry in providers_list:
                    if entry.get("id") == primary:
                        cls._register_from_entry(entry, registered_ids)
                        break

            # Register remaining configured providers as fallbacks
            for entry in providers_list:
                pid = entry.get("id", "")
                if pid and pid not in registered_ids:
                    cls._register_from_entry(entry, registered_ids)
        except Exception as exc:
            logger.debug("[LLM Config] AppSettings multi-provider read: %s", exc)

        # ── 2. Legacy single-provider from AppSettings ──────────────
        try:
            from src.config.settings import AppSettings

            legacy_provider = AppSettings.get("provider", "")
            legacy_key = AppSettings.get("api_key", "")
            if legacy_provider and legacy_key and legacy_provider not in registered_ids:
                cls._register_legacy_single(
                    legacy_provider, legacy_key, registered_ids,
                )
        except Exception:
            pass

        # ── 3. Legacy environment variables ─────────────────────────
        cls.MINIMAX_API_KEY = os.environ.get("MINIMAX_API_KEY", "")
        cls.GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
        cls.OPENAI_CUSTOM_API_KEY = os.environ.get("OPENAI_CUSTOM_API_KEY", "")
        cls.OPENAI_CUSTOM_ENDPOINT = os.environ.get("OPENAI_CUSTOM_ENDPOINT", "")
        cls.OPENAI_CUSTOM_MODEL = os.environ.get("OPENAI_CUSTOM_MODEL", "gpt-4")

        if cls.MINIMAX_API_KEY and "minimax" not in registered_ids:
            try:
                _registry.register(MinimaxProvider(api_key=cls.MINIMAX_API_KEY))
                cls.AVAILABLE_PROVIDERS.append("minimax")
                registered_ids.add("minimax")
            except Exception as exc:
                logger.warning("[LLM Config] Legacy MiniMax init failed: %s", exc)

        if cls.GROQ_API_KEY and "groq" not in registered_ids:
            _registry.register(
                GroqProvider(api_key=cls.GROQ_API_KEY, preferred_model=cls.CURRENT_GROQ_MODEL)
            )
            cls.AVAILABLE_PROVIDERS.append("groq")
            registered_ids.add("groq")

        if (
            cls.OPENAI_CUSTOM_API_KEY
            and cls.OPENAI_CUSTOM_ENDPOINT
            and "openai_custom" not in registered_ids
            and "custom" not in registered_ids
        ):
            _registry.register(
                OpenAICustomProvider(
                    api_key=cls.OPENAI_CUSTOM_API_KEY,
                    base_url=cls.OPENAI_CUSTOM_ENDPOINT,
                    model=cls.OPENAI_CUSTOM_MODEL,
                )
            )
            cls.AVAILABLE_PROVIDERS.append("openai_custom")
            registered_ids.add("openai_custom")

        # ── Set default ─────────────────────────────────────────────
        cls.DEFAULT_PROVIDER = _registry.default
        logger.info(
            "[LLM Config] Providers: %s  Default: %s",
            cls.AVAILABLE_PROVIDERS,
            cls.DEFAULT_PROVIDER,
        )

    # ------------------------------------------------------------------ #
    # Internal helpers
    # ------------------------------------------------------------------ #

    @classmethod
    def _register_from_entry(cls, entry: dict, registered: set[str]) -> None:
        """Register a single provider from the new ``providers`` list format."""
        pid = entry.get("id", "")
        api_key = entry.get("api_key", "")
        model = entry.get("model", "")
        endpoint = entry.get("endpoint", "")

        if not pid:
            return

        catalog = get_provider(pid)

        # Build the litellm model string
        if not model and catalog:
            model = catalog.default_model
        if catalog and "/" not in model and catalog.litellm_prefix:
            model = f"{catalog.litellm_prefix}/{model}"

        # Determine base_url
        base_url = endpoint
        if not base_url and pid == "minimax":
            base_url = "https://api.minimaxi.chat/v1"
        if not base_url and pid == "ollama":
            base_url = "http://localhost:11434"

        # For MiniMax, route through openai compat
        if pid == "minimax" and not model.startswith("openai/"):
            model = f"openai/{model.split('/')[-1]}"

        provider = LiteLLMProvider(
            provider_id=pid,
            api_key=api_key,
            model=model,
            base_url=base_url,
        )
        _registry.register(provider)
        cls.AVAILABLE_PROVIDERS.append(pid)
        registered.add(pid)
        logger.info("[LLM Config] Registered %s (model=%s)", pid, model)

    @classmethod
    def _register_legacy_single(
        cls, provider_id: str, api_key: str, registered: set[str],
    ) -> None:
        """Register from the old single-provider AppSettings format."""
        try:
            from src.config.settings import AppSettings

            endpoint = AppSettings.get("custom_endpoint", "")
            model = AppSettings.get("custom_model", "")
        except Exception:
            endpoint = ""
            model = ""

        entry = {
            "id": provider_id,
            "api_key": api_key,
            "model": model,
            "endpoint": endpoint,
        }
        cls._register_from_entry(entry, registered)

    # ------------------------------------------------------------------ #
    # Public helpers (backward compat)
    # ------------------------------------------------------------------ #

    @classmethod
    def set_provider(cls, provider: str) -> None:
        """Switch to a different provider (no-op when unavailable)."""
        if provider in cls.AVAILABLE_PROVIDERS:
            cls.DEFAULT_PROVIDER = provider
            logger.info("[LLM Config] Switched to %s", provider)
        else:
            logger.warning(
                "[LLM Config] Provider '%s' unavailable. Available: %s",
                provider,
                cls.AVAILABLE_PROVIDERS,
            )

    @classmethod
    def set_groq_model(cls, model: str) -> None:
        """Set the preferred Groq model (tried first; others used as fallback)."""
        groq = _registry.get("groq")
        if groq is not None and isinstance(groq, GroqProvider):
            groq.preferred_model = model
            cls.CURRENT_GROQ_MODEL = model
            logger.info("[LLM Config] Groq model set to %s", model)
        else:
            logger.warning(
                "[LLM Config] Groq provider not available. Cannot set model '%s'.",
                model,
            )


def call_llm(
    system_prompt: str,
    user_message: str,
    provider: Optional[str] = None,
    temperature: float = 0.3,
    max_tokens: int = 500,
) -> Optional[str]:
    """Call the configured LLM provider with automatic fallback.

    Provider resolution order:
      1. ``provider`` argument (explicit override)
      2. ``LLMConfig.DEFAULT_PROVIDER`` (auto-selected at initialisation)
      3. Remaining registered providers as cascading fallbacks

    Args:
        system_prompt: System context and instructions.
        user_message:  User turn content.
        provider:      Override provider; falls back to ``LLMConfig.DEFAULT_PROVIDER``.
        temperature:   Sampling temperature (0-1).
        max_tokens:    Maximum response tokens.

    Returns:
        Response text, or ``None`` when all providers fail.
    """
    resolved = provider or LLMConfig.DEFAULT_PROVIDER
    chain = _registry.get_priority_chain(preferred=resolved)

    for llm_provider in chain:
        try:
            result = llm_provider.call(system_prompt, user_message, temperature, max_tokens)
            if result:
                if llm_provider.name != resolved:
                    logger.info("[LLM] Used fallback provider: %s", llm_provider.name)
                return result
        except Exception as exc:
            logger.warning(
                "[LLM] %s call failed (%s); trying next provider",
                llm_provider.name,
                exc,
            )

    logger.error(
        "[LLM] All providers exhausted. Providers tried: %s",
        [p.name for p in chain],
    )
    return None
