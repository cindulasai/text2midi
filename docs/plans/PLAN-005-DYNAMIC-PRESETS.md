# PLAN-005: Dynamic LLM-Powered Preset System

**Spec:** SPEC-005-DYNAMIC-PRESETS  
**Estimated Effort:** 2–3 days  
**Prerequisites:** Python 3.11+, existing genre_registry.py, TUI sidebar  
**Status:** DRAFT  

---

## Problem Statement

The current TUI sidebar has a hardcoded `_PRESETS` dict with ~60 static prompts across 29 categories. These are disconnected from the 210-node `GENRE_TREE` in `genre_registry.py`. The tree root says "text2midi" rather than surfacing presets as the primary navigation. Sub-genres (e.g., Jazz → Bebop, Swing, Modal) are invisible to users. There is no way to get fresh prompt ideas without typing manually.

## Solution

Replace the static dict with a `PresetService` that:
1. Builds the sidebar tree from `GENRE_TREE` (14 roots → 196 sub-genres)
2. Generates prompt ideas on-demand via LLM when a user expands a sub-genre node
3. Falls back to curated seed presets when offline
4. Caches results in-memory to avoid redundant LLM calls

---

## Phase 1: PresetService (Core Logic)

**Files:** `src/services/preset_service.py`

1. Create `PresetService` class with:
   - `get_root_categories()` → delegates to `get_root_genres()` from registry
   - `get_sub_genres(root_id)` → delegates to `get_children(root_id)` from registry
   - `generate_presets(genre_id, count=5, bypass_cache=False)` → builds grounded LLM prompt from `GenreNode` metadata, calls `call_llm()`, parses JSON response, caches result
   - `get_seed_presets(genre_id)` → returns static fallback prompts
   - `clear_cache()` → clears in-memory cache

2. Implement `_build_generation_prompt(genre_node, count)`:
   - System prompt: music production expert persona
   - Inject GenreNode context: name, tempo_range, default_key, default_scale, energy, instruments, chord_feel
   - Request JSON array output
   - Temperature 0.9, max_tokens 800

3. Implement LRU cache (OrderedDict, max 100 entries)

4. Implement `_SEED_PRESETS` constant: ~80 curated prompts covering all 14 roots + top sub-genres, sourced from `PRESET_PROMPTS_LIBRARY.md`

---

## Phase 2: Sidebar Restructure

**Files:** `src/tui/widgets/sidebar.py`

1. Remove the static `_PRESETS` dict entirely
2. Import `PresetService` and instantiate as module-level singleton
3. Change tree root label from `"text2midi"` to use `"🎵 Presets"` as primary node
4. Build Level 1 nodes from `PresetService.get_root_categories()` with emoji mapping
5. Build Level 2 nodes from `PresetService.get_sub_genres(root_id)` — all collapsed by default
6. Implement `on_tree_node_expanded` handler:
   - When a Level 2 sub-genre node is expanded and has no children yet:
     - Add temporary "⏳ Generating ideas..." leaf
     - Launch a Textual `Worker` to call `PresetService.generate_presets(genre_id)`
     - On worker completion: remove spinner, add prompt leaves + "🔄 More ideas" refresh leaf
   - When "🔄 More ideas" is selected: append new prompts to existing ones
7. Keep `PresetSelected` / `HistorySelected` message flow unchanged
8. Keep `refresh_history()` but rebuild only the history section (not the entire tree)

---

## Phase 3: Settings & Polish

**Files:** `src/config/settings.py`

1. Add `"preset_cache_max": 100` to `_DEFAULTS` dict
2. Sidebar reads this setting to configure cache size

**UX Polish:**
- Root genre nodes show child count: `"🎷 Jazz (14)"`
- Loading state with spinner leaf
- Offline indicator when LLM unavailable

---

## Phase 4: Tests

**Files:** `tests/test_preset_service.py`, `tests/test_tui/test_sidebar.py`

1. `test_preset_service.py`:
   - Test `get_root_categories()` returns 14 genres
   - Test `get_sub_genres("jazz")` returns 14 sub-genres
   - Test `generate_presets()` with mocked LLM
   - Test cache hit behavior
   - Test seed fallback when LLM returns None
   - Test `bypass_cache` generates fresh prompts

2. `tests/test_tui/test_sidebar.py`:
   - Test tree builds with 14 root nodes + History
   - Test `PresetSelected` message fires correctly

---

## Verification Criteria

- `pytest tests/test_preset_service.py -v` — all tests pass
- `pytest tests/test_tui/test_sidebar.py -v` — all tests pass
- Manual: `uv run main_tui.py` → sidebar shows "🎵 Presets" → 14 genres → expand Jazz → 14 sub-genres → expand Bebop → prompts appear → click one → generates MIDI
- Offline: remove API keys → expand genre → seed presets shown instantly
- Performance: sidebar builds in <100ms on startup
