# TASKS-005: Dynamic LLM-Powered Preset System

**Spec:** SPEC-005-DYNAMIC-PRESETS  
**Plan:** PLAN-005-DYNAMIC-PRESETS  

---

## Phase 1: PresetService

- [ ] **T-005.01** — Create `src/services/preset_service.py` with `PresetService` class skeleton: `get_root_categories()`, `get_sub_genres()`, `generate_presets()`, `get_seed_presets()`, `clear_cache()`
- [ ] **T-005.02** — Implement `_build_generation_prompt(genre_node, count)` — system prompt with GenreNode metadata injection (tempo, scale, key, instruments, energy, chord_feel)
- [ ] **T-005.03** — Implement `generate_presets()` — call `call_llm()`, parse JSON, validate prompt lengths, handle errors, fallback to seeds
- [ ] **T-005.04** — Implement LRU cache with `OrderedDict` (max 100 entries, configurable via settings)
- [ ] **T-005.05** — Create `_SEED_PRESETS` constant with ~80 curated prompts covering all 14 root genres + top sub-genres (sourced from `PRESET_PROMPTS_LIBRARY.md`)

## Phase 2: Sidebar Restructure

- [ ] **T-005.06** — Remove static `_PRESETS` dict from `src/tui/widgets/sidebar.py`
- [ ] **T-005.07** — Rewrite `_build_tree()` to build Level 1 (root genres with emoji) and Level 2 (sub-genres) from `PresetService` + `GENRE_TREE`
- [ ] **T-005.08** — Change root tree label from `"text2midi"` to show `"🎵 Presets"` as primary node
- [ ] **T-005.09** — Implement `on_tree_node_expanded` handler with async LLM generation via Textual Worker
- [ ] **T-005.10** — Add "⏳ Generating ideas..." spinner leaf during LLM calls
- [ ] **T-005.11** — Add "🔄 More ideas" refresh leaf at bottom of each expanded sub-genre
- [ ] **T-005.12** — Keep `PresetSelected` / `HistorySelected` message flow intact
- [ ] **T-005.13** — Refactor `refresh_history()` to rebuild only the history section

## Phase 3: Settings & Polish

- [ ] **T-005.14** — Add `"preset_cache_max": 100` to `_DEFAULTS` in `src/config/settings.py`
- [ ] **T-005.15** — Display child count badge on root genre nodes: `"🎷 Jazz (14)"`
- [ ] **T-005.16** — Handle offline mode: show seed presets immediately when LLM unavailable

## Phase 4: Tests

- [ ] **T-005.17** — Create `tests/test_preset_service.py` with tests for all PresetService methods
- [ ] **T-005.18** — Create `tests/test_tui/test_sidebar.py` with tree structure and message tests
- [ ] **T-005.19** — Run full test suite, fix any regressions

## Verification

- [ ] **T-005.20** — Manual test: `uv run main_tui.py` → verify full preset tree, LLM generation, click-to-generate flow
- [ ] **T-005.21** — Offline test: disable API keys → verify seed presets display correctly
