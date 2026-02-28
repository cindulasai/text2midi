# Plan: Universal LLM Setup with First-Run Wizard

**Date:** 2026-02-28  
**Status:** In Progress  
**Goal:** Replace the hand-rolled 3-provider system with LiteLLM (100+ providers) and add a first-run wizard for zero-friction onboarding.

---

## Problem

1. **New users get no guidance** — if no API key is configured, CLI just prints a warning; TUI shows a basic panel. Non-technical users are lost.
2. **Only 3 providers supported** — MiniMax, Groq, OpenAI-compatible. Users with keys from Anthropic, Google, Mistral, Cohere, etc. are left out.
3. **No key validation** — users don't know if their key works until generation fails.
4. **No local/free option** — users without cloud API keys can't use the app at all.

## Solution

**LiteLLM** — a single Python library that routes `completion()` calls to 100+ providers using the user's own native API keys (obtained directly from provider sites like groq.com, anthropic.com, etc.). LiteLLM is a routing layer, not a middleman — keys go straight to the provider.

**First-run wizard** — auto-launches on first run in both CLI and TUI. Walks the user through provider selection, key entry, and validation in plain language.

---

## Implementation Phases

### Phase 1: Add LiteLLM Dependency
- Add `litellm>=1.30.0` to `pyproject.toml` and `requirements.txt`
- Remove `groq>=0.4.0` and `langchain-groq>=0.1.0` (LiteLLM handles these internally)
- Keep `openai>=1.0.0` (LiteLLM dependency)

### Phase 2: Create Provider Catalog
Create `src/config/provider_catalog.py` with a static registry of providers:

**Tier 1 (Featured — shown first):**
| Provider | Free Tier | Env Var | Signup URL |
|----------|-----------|---------|------------|
| Groq | ✅ Generous | `GROQ_API_KEY` | https://console.groq.com/keys |
| Ollama | ✅ Local/Free | (none) | https://ollama.com |
| OpenAI | ❌ Paid | `OPENAI_API_KEY` | https://platform.openai.com/api-keys |
| Anthropic | ❌ Paid | `ANTHROPIC_API_KEY` | https://console.anthropic.com |
| Google Gemini | ✅ Free tier | `GEMINI_API_KEY` | https://aistudio.google.com/apikey |
| MiniMax | ❌ Paid | `MINIMAX_API_KEY` | https://platform.minimaxi.com |

**Tier 2 (More providers):**
Mistral, Cohere, DeepSeek, Together AI, Fireworks AI, Perplexity, OpenRouter

**Custom:** Any OpenAI-compatible endpoint (LM Studio, vLLM, etc.)

### Phase 3: Replace Provider Layer with LiteLLM Adapter
- Remove `MinimaxProvider`, `GroqProvider`, `OpenAICustomProvider` classes
- Add single `LiteLLMProvider` class wrapping `litellm.completion()`
- Keep `LLMProvider` Protocol and `ProviderRegistry` for backward compat
- `call()` maps to `litellm.completion(model="<prefix>/<model>", api_key=..., messages=[...])`

### Phase 4: Extend AppSettings for Multi-Provider Storage
New settings structure:
```json
{
  "providers": [
    {"id": "groq", "api_key": "gsk_...", "model": "llama-3.3-70b-versatile"},
    {"id": "anthropic", "api_key": "sk-ant-...", "model": "claude-sonnet-4-20250514"}
  ],
  "primary_provider": "groq",
  "theme": "dark"
}
```
- Auto-migrate old single-provider format on first load
- `apply_to_environment()` sets all provider env vars

### Phase 5: First-Run Wizard (CLI)
Create `src/config/setup_wizard.py`:
1. **Welcome** — Rich-formatted explanation of what the app needs
2. **Provider picker** — Numbered list grouped by Free/Paid/Advanced
3. **Signup URL** — "Get your free key at: https://console.groq.com/keys"
4. **Key input** — Masked `getpass`-style input
5. **Validation** — Test `litellm.completion()` call → ✅ or ❌ with helpful error
6. **Save** — Persist to `settings.json`, confirm success
7. **Ollama auto-detect** — Check `localhost:11434`, offer as free option

Integrate into `main.py`:
- `--setup` flag to re-run wizard anytime
- Auto-launch if no provider configured on first run

### Phase 6: Upgrade TUI ApiKeySetup Widget
- Replace hardcoded 3-provider dropdown with full catalog
- Add "Test Connection" button with spinner → pass/fail
- Show signup URL that updates per selected provider
- Show Ollama auto-detection status

### Phase 7: Update Docs & Templates
- Rewrite `.env.example` with all common env vars
- Rewrite `docs/GETTING_STARTED.md` with quickstart, provider table, Ollama setup

### Phase 8: Backward Compatibility
- Keep scanning legacy env vars (`MINIMAX_API_KEY`, `GROQ_API_KEY`, `OPENAI_CUSTOM_*`)
- Auto-migrate old `settings.json` format silently
- `call_llm()` signature unchanged — zero downstream changes needed

---

## Key Decisions

| Decision | Rationale |
|----------|-----------|
| LiteLLM over hand-rolled | Single dep covers 100+ providers vs N separate SDKs |
| Groq as recommended free default | Most generous free tier among cloud providers |
| Ollama as local fallback | Zero-cost entry for users without cloud API keys |
| Multi-provider settings | Backup providers prevent generation failure |
| Wizard auto-launches once | Stays out of the way after first setup |
| `call_llm()` unchanged | Zero changes in 5+ consumer files |

## How LiteLLM Uses Native API Keys

LiteLLM is NOT a middleman. It accepts keys obtained directly from provider sites:

```python
# Key from groq.com → goes straight to Groq's API
litellm.completion(model="groq/llama-3.3-70b-versatile", api_key="gsk_from_groq_site", ...)

# Key from anthropic.com → goes straight to Anthropic's API
litellm.completion(model="anthropic/claude-sonnet-4-20250514", api_key="sk-ant-from_anthropic", ...)

# Key from minimaxi.com → goes straight to MiniMax's API
litellm.completion(model="minimax/MiniMax-M2.5", api_key="from_minimax_site", api_base="https://api.minimaxi.chat/v1", ...)
```

## Verification Checklist
- [ ] `python main.py` fresh install → wizard launches → validates key → app starts
- [ ] `python main.py --setup` → re-runs wizard
- [ ] `python main_tui.py` fresh install → enhanced setup panel
- [ ] Existing `.env` with `GROQ_API_KEY` → works unchanged (backward compat)
- [ ] Old `settings.json` → auto-migrated silently
- [ ] Ollama running locally → detected and offered, no cloud key needed
- [ ] `pytest tests/` → all tests pass
