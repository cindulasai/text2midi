# -*- coding: utf-8 -*-
"""
Provider Catalog
================

Static registry of supported LLM providers with human-friendly metadata.
Used by the setup wizard and TUI to present provider choices, signup URLs,
and default models.

Each entry uses LiteLLM's model naming convention:
    ``<provider_prefix>/<model_name>``

For example::

    litellm.completion(model="groq/llama-3.3-70b-versatile", api_key="gsk_...")
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass(frozen=True)
class ProviderInfo:
    """Metadata for a single LLM provider."""

    id: str
    display_name: str
    description: str
    env_var: str
    signup_url: str
    default_model: str
    litellm_prefix: str
    example_models: List[str] = field(default_factory=list)
    needs_endpoint: bool = False
    is_local: bool = False
    is_free: bool = False
    tier: int = 1  # 1 = Featured, 2 = More providers


# ---------------------------------------------------------------------------
# Tier 1 — Featured providers (shown first in wizard & TUI)
# ---------------------------------------------------------------------------

GROQ = ProviderInfo(
    id="groq",
    display_name="Groq",
    description="Ultra-fast inference, generous free tier. Best for getting started.",
    env_var="GROQ_API_KEY",
    signup_url="https://console.groq.com/keys",
    default_model="llama-3.3-70b-versatile",
    litellm_prefix="groq",
    example_models=["llama-3.3-70b-versatile", "llama-4-maverick", "mixtral-8x7b-32768"],
    is_free=True,
    tier=1,
)

OLLAMA = ProviderInfo(
    id="ollama",
    display_name="Ollama (Local)",
    description="Run AI models on your own computer. Free, private, no internet needed.",
    env_var="",  # no key needed
    signup_url="https://ollama.com",
    default_model="llama3.2",
    litellm_prefix="ollama",
    example_models=["llama3.2", "llama3.1", "mistral", "codellama", "gemma2"],
    needs_endpoint=True,  # http://localhost:11434
    is_local=True,
    is_free=True,
    tier=1,
)

OPENAI = ProviderInfo(
    id="openai",
    display_name="OpenAI",
    description="GPT-4o, GPT-4, GPT-3.5. Industry-leading quality.",
    env_var="OPENAI_API_KEY",
    signup_url="https://platform.openai.com/api-keys",
    default_model="gpt-4o",
    litellm_prefix="openai",
    example_models=["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-3.5-turbo"],
    tier=1,
)

ANTHROPIC = ProviderInfo(
    id="anthropic",
    display_name="Anthropic",
    description="Claude models. Excellent reasoning and instruction following.",
    env_var="ANTHROPIC_API_KEY",
    signup_url="https://console.anthropic.com/settings/keys",
    default_model="claude-sonnet-4-20250514",
    litellm_prefix="anthropic",
    example_models=["claude-sonnet-4-20250514", "claude-3-5-haiku-20241022", "claude-3-opus-20240229"],
    tier=1,
)

GEMINI = ProviderInfo(
    id="gemini",
    display_name="Google Gemini",
    description="Google's Gemini models. Free tier available.",
    env_var="GEMINI_API_KEY",
    signup_url="https://aistudio.google.com/apikey",
    default_model="gemini/gemini-2.0-flash",
    litellm_prefix="gemini",
    example_models=["gemini/gemini-2.0-flash", "gemini/gemini-1.5-pro", "gemini/gemini-1.5-flash"],
    is_free=True,
    tier=1,
)

MINIMAX = ProviderInfo(
    id="minimax",
    display_name="MiniMax",
    description="MiniMax M2.5 coding model. Strong at structured output.",
    env_var="MINIMAX_API_KEY",
    signup_url="https://platform.minimaxi.com/",
    default_model="MiniMax-M2.5",
    litellm_prefix="minimax",
    example_models=["MiniMax-M2.5"],
    needs_endpoint=True,  # uses custom base URL
    tier=1,
)


# ---------------------------------------------------------------------------
# Tier 2 — More providers
# ---------------------------------------------------------------------------

MISTRAL = ProviderInfo(
    id="mistral",
    display_name="Mistral AI",
    description="European AI lab. Fast, multilingual models.",
    env_var="MISTRAL_API_KEY",
    signup_url="https://console.mistral.ai/api-keys/",
    default_model="mistral-large-latest",
    litellm_prefix="mistral",
    example_models=["mistral-large-latest", "mistral-medium-latest", "open-mixtral-8x22b"],
    tier=2,
)

COHERE = ProviderInfo(
    id="cohere",
    display_name="Cohere",
    description="Enterprise-focused. Command R+ for complex reasoning.",
    env_var="COHERE_API_KEY",
    signup_url="https://dashboard.cohere.com/api-keys",
    default_model="command-r-plus",
    litellm_prefix="cohere_chat",
    example_models=["command-r-plus", "command-r", "command-light"],
    tier=2,
)

DEEPSEEK = ProviderInfo(
    id="deepseek",
    display_name="DeepSeek",
    description="Affordable, high-quality Chinese AI lab. Great for coding tasks.",
    env_var="DEEPSEEK_API_KEY",
    signup_url="https://platform.deepseek.com/api_keys",
    default_model="deepseek-chat",
    litellm_prefix="deepseek",
    example_models=["deepseek-chat", "deepseek-coder"],
    tier=2,
)

TOGETHER = ProviderInfo(
    id="together_ai",
    display_name="Together AI",
    description="Run open-source models. Good selection of free/cheap models.",
    env_var="TOGETHERAI_API_KEY",
    signup_url="https://api.together.xyz/settings/api-keys",
    default_model="together_ai/meta-llama/Llama-3.3-70B-Instruct-Turbo",
    litellm_prefix="together_ai",
    example_models=[
        "together_ai/meta-llama/Llama-3.3-70B-Instruct-Turbo",
        "together_ai/mistralai/Mixtral-8x7B-Instruct-v0.1",
    ],
    tier=2,
)

FIREWORKS = ProviderInfo(
    id="fireworks_ai",
    display_name="Fireworks AI",
    description="Fast serverless inference for open models.",
    env_var="FIREWORKS_AI_API_KEY",
    signup_url="https://fireworks.ai/api-keys",
    default_model="fireworks_ai/accounts/fireworks/models/llama-v3p3-70b-instruct",
    litellm_prefix="fireworks_ai",
    example_models=["fireworks_ai/accounts/fireworks/models/llama-v3p3-70b-instruct"],
    tier=2,
)

PERPLEXITY = ProviderInfo(
    id="perplexity",
    display_name="Perplexity",
    description="Search-augmented AI. Great for factual queries.",
    env_var="PERPLEXITYAI_API_KEY",
    signup_url="https://www.perplexity.ai/settings/api",
    default_model="perplexity/sonar-pro",
    litellm_prefix="perplexity",
    example_models=["perplexity/sonar-pro", "perplexity/sonar"],
    tier=2,
)

OPENROUTER = ProviderInfo(
    id="openrouter",
    display_name="OpenRouter",
    description="Meta-provider: access 100+ models through one API key.",
    env_var="OPENROUTER_API_KEY",
    signup_url="https://openrouter.ai/keys",
    default_model="openrouter/auto",
    litellm_prefix="openrouter",
    example_models=[
        "openrouter/auto",
        "openrouter/anthropic/claude-sonnet-4-20250514",
        "openrouter/openai/gpt-4o",
    ],
    tier=2,
)

CUSTOM = ProviderInfo(
    id="custom",
    display_name="Custom (OpenAI-compatible)",
    description="Any OpenAI-compatible endpoint: LM Studio, vLLM, text-gen-webui, etc.",
    env_var="OPENAI_CUSTOM_API_KEY",
    signup_url="",
    default_model="gpt-4",
    litellm_prefix="openai",  # use openai compat
    example_models=[],
    needs_endpoint=True,
    tier=2,
)


# ---------------------------------------------------------------------------
# Ordered catalog
# ---------------------------------------------------------------------------

ALL_PROVIDERS: List[ProviderInfo] = [
    # Tier 1 — Featured
    GROQ,
    OLLAMA,
    OPENAI,
    ANTHROPIC,
    GEMINI,
    MINIMAX,
    # Tier 2 — More
    MISTRAL,
    COHERE,
    DEEPSEEK,
    TOGETHER,
    FIREWORKS,
    PERPLEXITY,
    OPENROUTER,
    CUSTOM,
]

PROVIDER_MAP: Dict[str, ProviderInfo] = {p.id: p for p in ALL_PROVIDERS}

TIER1_PROVIDERS: List[ProviderInfo] = [p for p in ALL_PROVIDERS if p.tier == 1]
TIER2_PROVIDERS: List[ProviderInfo] = [p for p in ALL_PROVIDERS if p.tier == 2]

FREE_PROVIDERS: List[ProviderInfo] = [p for p in ALL_PROVIDERS if p.is_free]


def get_provider(provider_id: str) -> Optional[ProviderInfo]:
    """Look up a provider by id. Returns ``None`` if not found."""
    return PROVIDER_MAP.get(provider_id)


def get_env_var_for_provider(provider_id: str) -> str:
    """Return the environment variable name for a given provider."""
    info = PROVIDER_MAP.get(provider_id)
    return info.env_var if info else ""
