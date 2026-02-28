# SPEC-005: Dynamic LLM-Powered Preset System

**Status:** Draft  
**Created:** 2026-02-27  
**Author:** spec-kit  
**Priority:** P1 — Core UX Enhancement  

---

## 1. Overview

Replace the static `_PRESETS` dict in the TUI sidebar with a dynamic, 3-level preset tree driven by the existing `GENRE_TREE` registry (210+ genres). The tree root becomes **Presets** (removing the "text2midi" label), expanding into **14 Root Genres → 196 Sub-genres → LLM-generated prompts on demand**.

When a user expands any genre or sub-genre node, the system calls the LLM to generate 3–5 fresh, musically-coherent prompt suggestions specific to that genre—using `GenreNode` metadata (tempo, scale, instruments, energy) as grounding context. A local in-memory cache prevents redundant LLM calls.

## 2. User Stories

| ID | As a... | I want to... | So that... |
|----|---------|-------------|------------|
| US-01 | Music producer | See all 14 genre categories in the sidebar | I can browse the full genre catalog without leaving the TUI |
| US-02 | Music producer | Expand a genre to see its sub-genres | I can drill into specific styles (e.g., Jazz → Bebop) |
| US-03 | Music producer | Expand a sub-genre node and get LLM-generated prompt ideas | I get fresh, creative, genre-specific prompts without typing |
| US-04 | Music producer | Click "🔄 More ideas" to get additional prompts | I can explore unlimited variations for any genre |
| US-05 | Music producer | Use the system offline with seed presets | The sidebar works even without an API key configured |
| US-06 | First-time user | See a populated tree immediately on startup | I don't have to wait for LLM calls before I can browse |

## 3. Functional Requirements

### 3.1 Tree Structure

```
🎵 Presets                          ← Root node (always expanded)
├─ 🎻 Classical & Orchestral (12)   ← Level 1: root genre + child count
│  ├─ Baroque                       ← Level 2: sub-genre (collapsed)
│  │  ├─ "Compose a baroque harps…" ← Level 3: LLM-generated prompt leaf
│  │  ├─ "Create an ornate barque…"
│  │  ├─ "Write a Bach-inspired…"
│  │  └─ 🔄 More ideas              ← Refresh button leaf
│  ├─ Classical Era
│  ├─ Romantic
│  │  ...
│  └─ Avant-garde
├─ 🎷 Jazz (14)
│  ├─ Swing
│  ├─ Bebop
│  │  ...
│  ...
├─ 📂 History                       ← History section unchanged
│  ├─ "Create a peaceful ambient…"
│  └─ ...
```

### 3.2 Preset Service (`src/services/preset_service.py`)

A new `PresetService` class provides:

| Method | Description |
|--------|-------------|
| `get_root_categories()` | Returns 14 root `GenreNode` objects |
| `get_sub_genres(root_id)` | Returns children of a root genre |
| `generate_presets(genre_id, count=5)` | LLM-generates `count` creative prompts for a genre |
| `get_seed_presets(genre_id)` | Returns static fallback prompts from `_SEED_PRESETS` |
| `clear_cache()` | Clears the in-memory LRU cache |

### 3.3 LLM Prompt Generation

The LLM prompt for generating presets must:

1. Include `GenreNode` metadata as grounding context: name, tempo range, key, scale, instruments, energy, chord feel
2. Request a JSON array of prompt strings
3. Use temperature 0.9 for creative diversity
4. Max tokens: 800
5. Parse and validate the response as JSON
6. Strip any markdown fences
7. Ensure each prompt is 20–200 characters
8. Return at least 3 prompts (fall back to seeds if fewer)

### 3.4 Caching

- In-memory dict cache keyed by `genre_id`
- Max 100 cached genre entries (LRU eviction)
- Cache is preserved across tree rebuilds (e.g., when history refreshes)
- "🔄 More ideas" bypasses cache and appends new prompts

### 3.5 Offline / Fallback Behavior

- Seed presets: curated from `PRESET_PROMPTS_LIBRARY.md` covering all 14 root genres + top sub-genres
- When LLM is unavailable: immediately show seed presets, add "(offline)" to node label
- When LLM returns invalid JSON: retry once, then fall back to seeds

### 3.6 Genre Emoji Mapping

| Root ID | Emoji | Display Name |
|---------|-------|-------------|
| `classical` | 🎻 | Classical & Orchestral |
| `jazz` | 🎷 | Jazz |
| `blues` | 🎵 | Blues & Soul |
| `rock` | 🎸 | Rock |
| `metal` | 🤘 | Metal |
| `electronic` | 🎧 | Electronic & Dance |
| `hiphop` | 🎤 | Hip-Hop & Urban |
| `pop` | 🎹 | Pop |
| `rnb` | 💜 | R&B & Funk |
| `folk` | 🪕 | Folk & Acoustic |
| `latin` | 💃 | Latin & Caribbean |
| `african` | 🌍 | African |
| `asian` | 🌏 | Asian & Middle Eastern |
| `cinematic` | 🎬 | Cinematic & Ambient |

## 4. Non-Functional Requirements

| Requirement | Target |
|-------------|--------|
| Sidebar build time (startup) | < 100ms (no LLM calls, registry only) |
| LLM prompt generation latency | < 3s per genre node |
| Memory usage (cache) | < 5MB for 100 cached genres |
| Offline usability | Full tree browsable with seed presets |

## 5. Files Changed

| File | Change |
|------|--------|
| `src/services/preset_service.py` | **NEW** — `PresetService` class |
| `src/tui/widgets/sidebar.py` | **REWRITE** — Dynamic tree from registry |
| `src/config/settings.py` | **UPDATE** — Add `preset_cache_max` default |
| `tests/test_preset_service.py` | **NEW** — Unit tests |
| `tests/test_tui/test_sidebar.py` | **NEW** — Sidebar tree tests |

## 6. Dependencies

- Existing: `src/config/genre_registry.py` (GenreNode, GENRE_TREE, get_root_genres, get_children)
- Existing: `src/config/llm.py` (call_llm)
- Existing: `textual` (Tree, Worker, Static, Message)
- No new external dependencies required
