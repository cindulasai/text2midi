# -*- coding: utf-8 -*-
"""
LLM Provider Protocol and Implementations
==========================================

Defines a ``LLMProvider`` protocol and a unified ``LiteLLMProvider`` class
that routes to 100+ LLM providers (OpenAI, Anthropic, Groq, Google, Ollama,
Mistral, Cohere, …) via the `litellm <https://github.com/BerriAI/litellm>`_
library.

Users supply their **native** API key — obtained directly from each
provider's website — and LiteLLM routes the call to that provider's API.
No middleman; the key goes straight to the provider.

Usage::

    provider = LiteLLMProvider(
        provider_id="groq",
        api_key="gsk_...",
        model="groq/llama-3.3-70b-versatile",
    )
    response = provider.call("You are a music expert.", "Write a chord progression.", 0.3, 500)

Legacy provider classes (``MinimaxProvider``, ``GroqProvider``,
``OpenAICustomProvider``) are kept as thin wrappers that delegate to
``LiteLLMProvider`` for backward compatibility.
"""

from __future__ import annotations

import logging
from typing import List, Optional, Protocol, runtime_checkable

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Protocol
# ---------------------------------------------------------------------------


@runtime_checkable
class LLMProvider(Protocol):
    """Interface that every LLM provider must satisfy."""

    name: str

    def call(
        self,
        system_prompt: str,
        user_message: str,
        temperature: float,
        max_tokens: int,
    ) -> Optional[str]:
        """Send a chat completion request and return the response text.

        Returns ``None`` when the provider fails or is not configured.
        """
        ...


# ---------------------------------------------------------------------------
# Unified LiteLLM provider
# ---------------------------------------------------------------------------


class LiteLLMProvider:
    """Universal LLM provider powered by LiteLLM.

    Accepts API keys obtained directly from any provider's website
    (Groq, OpenAI, Anthropic, etc.) and routes the call to the correct API.

    Parameters
    ----------
    provider_id:
        Identifier matching a ``ProviderInfo.id`` from the catalog
        (e.g. ``"groq"``, ``"openai"``, ``"anthropic"``).
    api_key:
        Native API key from the provider's site.
    model:
        LiteLLM model string, e.g. ``"groq/llama-3.3-70b-versatile"``.
    base_url:
        Optional custom endpoint (required for Ollama, MiniMax, custom).
    """

    def __init__(
        self,
        provider_id: str,
        api_key: str = "",
        model: str = "",
        base_url: str = "",
    ) -> None:
        self.name = provider_id
        self._api_key = api_key
        self._model = model
        self._base_url = base_url

    def call(
        self,
        system_prompt: str,
        user_message: str,
        temperature: float,
        max_tokens: int,
    ) -> Optional[str]:
        """Make a chat completion via LiteLLM."""
        if not self._model:
            logger.warning("[%s] No model configured", self.name)
            return None
        # Local providers (Ollama) don't need an API key
        if not self._api_key and not self._base_url:
            logger.warning("[%s] No API key or base_url set", self.name)
            return None
        try:
            import litellm

            # Suppress litellm's noisy default logging
            litellm.suppress_debug_info = True

            kwargs: dict = {
                "model": self._model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message},
                ],
                "temperature": temperature,
                "max_tokens": max_tokens,
            }
            if self._api_key:
                kwargs["api_key"] = self._api_key
            if self._base_url:
                kwargs["api_base"] = self._base_url

            resp = litellm.completion(**kwargs)
            content = resp.choices[0].message.content
            if content is None:
                logger.warning("[%s] API returned empty content", self.name)
                return None
            return content.strip()
        except Exception as exc:
            logger.warning("[%s] API call failed: %s", self.name, exc)
            return None


# ---------------------------------------------------------------------------
# Legacy provider aliases (backward compat — delegate to LiteLLMProvider)
# ---------------------------------------------------------------------------

_MINIMAX_BASE_URL = "https://api.minimaxi.chat/v1"
_MINIMAX_MODEL = "MiniMax-M2.5"


class MinimaxProvider(LiteLLMProvider):
    """Legacy wrapper: MiniMax M2.5 via LiteLLM + OpenAI compat endpoint."""

    def __init__(self, api_key: str) -> None:
        super().__init__(
            provider_id="minimax",
            api_key=api_key,
            model=f"openai/{_MINIMAX_MODEL}",
            base_url=_MINIMAX_BASE_URL,
        )


class GroqProvider(LiteLLMProvider):
    """Legacy wrapper: Groq via LiteLLM."""

    MODELS: List[str] = ["llama-3.3-70b-versatile", "llama-4-maverick"]

    def __init__(
        self,
        api_key: str,
        preferred_model: str = "llama-3.3-70b-versatile",
    ) -> None:
        self._preferred_model = preferred_model
        super().__init__(
            provider_id="groq",
            api_key=api_key,
            model=f"groq/{preferred_model}",
        )

    @property
    def preferred_model(self) -> str:
        return self._preferred_model

    @preferred_model.setter
    def preferred_model(self, model: str) -> None:
        if model in self.MODELS:
            self._preferred_model = model
            self._model = f"groq/{model}"
        else:
            logger.warning("Unknown Groq model %r. Available: %s", model, self.MODELS)


class OpenAICustomProvider(LiteLLMProvider):
    """Legacy wrapper: OpenAI-compatible custom endpoint via LiteLLM."""

    def __init__(
        self,
        api_key: str,
        base_url: str,
        model: str = "gpt-4",
    ) -> None:
        super().__init__(
            provider_id="openai_custom",
            api_key=api_key,
            model=f"openai/{model}",
            base_url=base_url,
        )


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------


class ProviderRegistry:
    """Registry of available LLM providers with priority-based fallback.

    Providers are tried in registration order.
    """

    def __init__(self) -> None:
        self._providers: dict[str, LLMProvider] = {}
        self._order: list[str] = []

    def register(self, provider: LLMProvider) -> None:
        """Register a provider.  First registered = highest priority."""
        self._providers[provider.name] = provider
        if provider.name not in self._order:
            self._order.append(provider.name)
        logger.info("[ProviderRegistry] Registered: %s", provider.name)

    def get(self, name: str) -> Optional[LLMProvider]:
        return self._providers.get(name)

    @property
    def available(self) -> list[str]:
        return list(self._order)

    @property
    def default(self) -> Optional[str]:
        return self._order[0] if self._order else None

    def get_priority_chain(self, preferred: Optional[str] = None) -> list[LLMProvider]:
        """Return providers in fallback order, optionally starting with *preferred*."""
        ordered_names: list[str] = []
        if preferred and preferred in self._providers:
            ordered_names.append(preferred)
        for name in self._order:
            if name not in ordered_names:
                ordered_names.append(name)
        return [self._providers[n] for n in ordered_names]


# ---------------------------------------------------------------------------
# Validation helper
# ---------------------------------------------------------------------------


def _validate_via_http(
    provider_id: str,
    api_key: str,
    model: str,
    base_url: str,
) -> tuple[bool, str]:
    """Fallback validation using a direct HTTP request.

    This avoids LiteLLM's error-message mangling so we can inspect
    the actual HTTP status code returned by the provider.
    """
    try:
        import httpx
    except ImportError:
        return False, "httpx not installed — cannot validate directly."

    # Build the OpenAI-compatible chat completion payload
    url = (base_url.rstrip("/") + "/chat/completions") if base_url else ""
    if not url:
        return False, "No endpoint URL to validate against."

    headers = {
        "Content-Type": "application/json",
    }
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    # Strip any litellm prefixes like "openai/", "groq/" from model name
    raw_model = model.split("/", 1)[-1] if "/" in model else model

    payload = {
        "model": raw_model,
        "messages": [{"role": "user", "content": "Say OK"}],
        "max_tokens": 16,
        "temperature": 0,
    }

    try:
        resp = httpx.post(url, json=payload, headers=headers, timeout=30.0)
        if resp.status_code == 200:
            return True, f"Connected to {provider_id}."
        if resp.status_code == 401:
            return False, "Invalid API key (HTTP 401). Please check and try again."
        if resp.status_code == 403:
            return False, "Access denied (HTTP 403). Check your API key permissions."
        if resp.status_code == 404:
            return False, f"Model '{raw_model}' not found (HTTP 404). Check the model name."
        if resp.status_code == 429:
            return False, "Rate limited (HTTP 429). Wait a moment and try again."
        # Try to extract a message from the response body
        try:
            body = resp.json()
            detail = body.get("error", {}).get("message", "") or body.get("message", "")
        except Exception:
            detail = resp.text[:200]
        return False, f"HTTP {resp.status_code}: {detail[:200]}"
    except httpx.ConnectError:
        return False, "Cannot connect. Check your internet or endpoint URL."
    except httpx.TimeoutException:
        return False, "Connection timed out. Check your internet or endpoint URL."
    except Exception as exc:
        return False, f"HTTP error: {str(exc)[:200]}"


def validate_api_key(
    provider_id: str,
    api_key: str = "",
    model: str = "",
    base_url: str = "",
) -> tuple[bool, str]:
    """Test an API key by making a tiny LiteLLM completion call.

    Returns ``(success, message)``.

    Uses direct HTTP validation as a fallback for providers where
    LiteLLM's error handling is unreliable (e.g. MiniMax, custom
    OpenAI-compatible endpoints).
    """
    # -----------------------------------------------------------
    # For providers routed through OpenAI-compat (minimax, custom
    # endpoints, etc.) use a direct HTTP call for more reliable
    # status-code inspection.
    # -----------------------------------------------------------
    use_direct_http = provider_id in (
        "minimax", "openai_custom", "custom",
    ) or (base_url and "openai" in model.split("/")[0].lower())

    if use_direct_http and base_url:
        ok, msg = _validate_via_http(provider_id, api_key, model, base_url)
        if ok:
            return ok, msg
        # If HTTP validation returned an auth error, trust it
        if "401" in msg or "403" in msg:
            return False, msg
        # For non-auth errors, fall through to LiteLLM as second try
        logger.debug("Direct HTTP validation failed (%s), trying LiteLLM...", msg)

    try:
        import litellm

        litellm.suppress_debug_info = True

        kwargs: dict = {
            "model": model,
            "messages": [{"role": "user", "content": "Say OK"}],
            "max_tokens": 16,
            "temperature": 0,
        }
        if api_key:
            kwargs["api_key"] = api_key
        if base_url:
            kwargs["api_base"] = base_url

        resp = litellm.completion(**kwargs)
        # If we got a response object at all (HTTP 200), the key is valid.
        # Some providers (e.g. MiniMax) may return empty/whitespace
        # content for very short prompts — that's still a valid auth.
        content = resp.choices[0].message.content or ""
        if content.strip():
            return True, f"Connected to {provider_id}."
        # HTTP 200 with empty content — key is still valid
        return True, f"Connected to {provider_id} (key accepted)."
    except Exception as exc:
        msg = str(exc)
        # Provide user-friendly error messages based on HTTP codes
        if "401" in msg or "unauthorized" in msg.lower():
            return False, "Invalid API key (401 Unauthorized). Please check and try again."
        if "403" in msg:
            return False, "Access denied (403 Forbidden). Check your API key permissions."
        if "404" in msg:
            return False, f"Model '{model}' not found. Check the model name."
        if "429" in msg or "rate limit" in msg.lower():
            return False, "Rate limited. Wait a moment and try again."
        if "connection" in msg.lower() or "connect" in msg.lower():
            return False, "Cannot connect. Check your internet or endpoint URL."
        if "timeout" in msg.lower():
            return False, "Connection timed out. Check your internet or endpoint URL."
        # Don't flag "invalid" generically — it catches non-auth errors
        if "invalid api key" in msg.lower() or "invalid_api_key" in msg.lower():
            return False, "Invalid API key. Please check and try again."
        return False, f"Error: {msg[:200]}"
