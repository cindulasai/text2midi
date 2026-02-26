# -*- coding: utf-8 -*-
"""
LLM Configuration and Management
Handles provider initialization and LLM calls.

Provider priority (highest → lowest):
  1. MiniMax M2.5  (default)
  2. Groq          (fallback)
  3. Gemini        (fallback)
"""

import logging
import os
from typing import Optional

import google.genai as genai
from groq import Groq
from openai import OpenAI

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Model lists
# ---------------------------------------------------------------------------

# Gemini models tried in preference order
_GEMINI_MODELS = ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-pro"]

# MiniMax base URL (international endpoint, OpenAI-compatible)
_MINIMAX_BASE_URL = "https://api.minimaxi.chat/v1"
_MINIMAX_MODEL = "MiniMax-M2.5"


class LLMConfig:
    """Runtime configuration for LLM provider selection.

    Provider priority: minimax → groq → gemini.
    Any provider that is not configured is skipped; the next available one
    becomes the default.
    """

    DEFAULT_PROVIDER: Optional[str] = None
    AVAILABLE_PROVIDERS: list = []

    # Groq
    GROQ_MODELS = ["llama-4-maverick", "llama-3.3-70b-versatile"]
    CURRENT_GROQ_MODEL = "llama-4-maverick"

    # Read from environment only – never hard-code secrets in source.
    MINIMAX_API_KEY: str = os.environ.get("MINIMAX_API_KEY", "")
    GROQ_API_KEY: str = os.environ.get("GROQ_API_KEY", "")
    GEMINI_API_KEY: str = os.environ.get("GEMINI_API_KEY", "")

    @classmethod
    def initialize(cls) -> None:
        """Detect and register available LLM providers.

        Registration order determines fallback priority:
          minimax → groq → gemini
        The first successfully registered provider becomes the default.
        """
        # Reload keys in case .env was loaded after module import
        cls.MINIMAX_API_KEY = os.environ.get("MINIMAX_API_KEY", "")
        cls.GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
        cls.GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

        cls.AVAILABLE_PROVIDERS.clear()

        # 1. MiniMax M2.5 (default / highest priority)
        if cls.MINIMAX_API_KEY:
            try:
                # Light connectivity check – list models endpoint is ideal; a
                # simple client construction is sufficient as a first gate.
                _client = OpenAI(
                    api_key=cls.MINIMAX_API_KEY,
                    base_url=_MINIMAX_BASE_URL,
                )
                cls.AVAILABLE_PROVIDERS.append("minimax")
                logger.info("[LLM Config] MiniMax provider registered (%s)", _MINIMAX_MODEL)
            except Exception as exc:
                logger.warning("[LLM Config] MiniMax init failed: %s", exc)

        # 2. Groq (first fallback)
        if cls.GROQ_API_KEY:
            cls.AVAILABLE_PROVIDERS.append("groq")

        # 3. Gemini (second fallback)
        if cls.GEMINI_API_KEY:
            try:
                genai.Client(api_key=cls.GEMINI_API_KEY)
                cls.AVAILABLE_PROVIDERS.append("gemini")
            except Exception as exc:
                logger.warning("[LLM Config] Gemini init failed: %s", exc)

        # First available provider wins the default slot
        cls.DEFAULT_PROVIDER = (
            cls.AVAILABLE_PROVIDERS[0] if cls.AVAILABLE_PROVIDERS else None
        )
        logger.info(
            "[LLM Config] Providers: %s  Default: %s",
            cls.AVAILABLE_PROVIDERS,
            cls.DEFAULT_PROVIDER,
        )

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
        if model in cls.GROQ_MODELS:
            cls.CURRENT_GROQ_MODEL = model
            logger.info("[LLM Config] Groq model set to %s", model)
        else:
            logger.warning(
                "[LLM Config] Unknown Groq model '%s'. Available: %s",
                model,
                cls.GROQ_MODELS,
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
        temperature:   Sampling temperature (0–1).
        max_tokens:    Maximum response tokens.

    Returns:
        Response text, or ``None`` when all providers fail.
    """
    resolved = provider or LLMConfig.DEFAULT_PROVIDER

    # Build an ordered list: preferred provider first, then remaining fallbacks
    ordered: list[str] = []
    if resolved:
        ordered.append(resolved)
    for p in LLMConfig.AVAILABLE_PROVIDERS:
        if p not in ordered:
            ordered.append(p)

    _DISPATCH = {
        "minimax": _call_minimax,
        "groq":    _call_groq,
        "gemini":  _call_gemini,
    }

    for attempt_provider in ordered:
        fn = _DISPATCH.get(attempt_provider)
        if fn is None:
            logger.warning("[LLM] Unknown provider in AVAILABLE_PROVIDERS: %r", attempt_provider)
            continue
        try:
            result = fn(system_prompt, user_message, temperature, max_tokens)
            if result:
                if attempt_provider != resolved:
                    logger.info("[LLM] Used fallback provider: %s", attempt_provider)
                return result
        except Exception as exc:
            logger.warning("[LLM] %s call failed (%s); trying next provider", attempt_provider, exc)

    logger.error("[LLM] All providers exhausted. Providers tried: %s", ordered)
    return None


# ---------------------------------------------------------------------------
# Private provider helpers
# ---------------------------------------------------------------------------


def _call_minimax(
    system_prompt: str,
    user_message: str,
    temperature: float,
    max_tokens: int,
) -> Optional[str]:
    """Call MiniMax M2.5 via the OpenAI-compatible international endpoint."""
    if not LLMConfig.MINIMAX_API_KEY:
        return None

    client = OpenAI(
        api_key=LLMConfig.MINIMAX_API_KEY,
        base_url=_MINIMAX_BASE_URL,
    )
    resp = client.chat.completions.create(
        model=_MINIMAX_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_message},
        ],
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return resp.choices[0].message.content.strip()


def _call_gemini(
    system_prompt: str,
    user_message: str,
    temperature: float,
    max_tokens: int,
) -> Optional[str]:
    """Call Gemini with automatic model fallback."""
    client = genai.Client(api_key=LLMConfig.GEMINI_API_KEY)
    for model in _GEMINI_MODELS:
        try:
            response = client.models.generate_content(
                model=model,
                contents=user_message,
                config=genai.types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    temperature=temperature,
                    max_output_tokens=max_tokens,
                ),
            )
            return response.text
        except Exception:
            continue
    return None


def _call_groq(
    system_prompt: str,
    user_message: str,
    temperature: float,
    max_tokens: int,
) -> Optional[str]:
    """Call Groq with the preferred model first, then configured fallbacks."""
    if not LLMConfig.GROQ_API_KEY:
        return None

    client = Groq(api_key=LLMConfig.GROQ_API_KEY)
    preferred = LLMConfig.CURRENT_GROQ_MODEL
    models = [preferred] + [m for m in LLMConfig.GROQ_MODELS if m != preferred]

    for model in models:
        try:
            resp = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user",   "content": user_message},
                ],
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return resp.choices[0].message.content.strip()
        except Exception:
            continue
    return None
