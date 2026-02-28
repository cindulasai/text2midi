# SOLID Refactoring Plan — Production-Grade Code Cleanup

> **Created**: 2026-02-27  
> **Status**: ✅ Completed  
> **Principle**: No logic changes — structural/organizational only  

## Overview

The ~9,800-line codebase has ~2,200 lines (22%) of dead/unused code, 5 major duplication areas, and several SOLID violations. This plan restructures the code into a lean, professional codebase by:

1. Eliminating dead code and duplicates
2. Extracting data into external files
3. Introducing Protocol-based abstractions for LLM providers and generation strategies
4. Consolidating scattered constants and models
5. Fixing packaging issues like `sys.path` hacks

**All changes preserve existing logic — no behavior modifications.**

---

## Discovery Summary

| Metric | Value |
|--------|-------|
| Total source lines | ~9,800 across ~50 Python files |
| Dead/unused code | ~2,200 lines (22%) |
| Duplicate `TrackConfig` definitions | 2 (agents/state.py + app/models.py) |
| Duplicate track planning logic | ~400 lines across 2 files |
| Intent parsers (only 1 needed) | 3 |
| Separate instrument databases | 5 |
| `sys.path.insert` hacks | 12 live occurrences |
| Hardcoded magic numbers | 20+ occurrences of `480`, `64`, `"outputs"` |

---

## Phase 1: Cleanup & Quick Wins

### 1.1 Remove dead code and empty packages
- Delete `src/specify_cli/` (empty package, no references anywhere)
- Delete `src/midigent/midi/` (empty directory)
- Delete `src/agents/nodes.py` (backward-compat shim — only re-exports from real node files)
- Delete `src/app/intent_parser.py` — thin wrapper around `LLMIntentEngine` with dead `_parse_with_keywords()`
- Remove `IntentParser` re-export from `src/app/__init__.py`

### 1.2 Move unintegrated USP features to `src/experimental/`
- Create `src/experimental/__init__.py` with docstring explaining these are not-yet-integrated features
- Move these 4 files (~1,360 lines):
  - `src/midigent/creative_variation_engine.py` → `src/experimental/`
  - `src/midigent/educational_insights.py` → `src/experimental/`
  - `src/midigent/professional_analytics.py` → `src/experimental/`
  - `src/midigent/cultural_music.py` → `src/experimental/`

### 1.3 Consolidate `TrackConfig` into a single definition
- Keep `TrackConfig` in `src/agents/state.py` as the canonical definition
- In `src/app/models.py`, replace the duplicate class with `from src.agents.state import TrackConfig`
- Update `src/app/track_planner.py` to import from `src.agents.state`

### 1.4 Rescue dataclasses from deprecated file, then delete it
- Move `EnhancedMusicIntent`, `CompositionStructure`, and `CompositionComplexity` from `src/midigent/advanced_intent_parser.py` into `src/agents/state.py`
- Update imports in `src/intent/engine.py` (lines 52-53, 115)
- Update string-type references in `src/midigent/intelligent_quality_reviewer.py`
- Delete `src/midigent/advanced_intent_parser.py` (350 lines)

### 1.5 Create shared constants module
- Create `src/config/constants.py` with:
  - `TICKS_PER_BEAT = 480`
  - `DEFAULT_BARS = 64`
  - `OUTPUT_DIR = Path("outputs")`
  - `MAX_REFINEMENT_ITERATIONS = 2`
- Replace all hardcoded occurrences across the codebase

### 1.6 Remove all `sys.path.insert` hacks
- Remove from all 12 live files
- Add `[tool.pytest.ini_options] pythonpath = ["."]` to `pyproject.toml`
- Ensure `pip install -e .` works properly

---

## Phase 2: Structural Refactoring

### 2.7 Externalize large data literals
- **Genre registry**: Extract `GENRE_TREE` dict (~850 lines) into `src/config/data/genre_tree.json`
- **Prompt templates**: Extract large string literals (~500 lines) into `src/intent/templates/` as `.txt` files
- **Sidebar presets**: Extract preset prompts (~150 lines) into `src/tui/data/presets.json`

### 2.8 Introduce LLM Provider Protocol
- Create `src/config/providers.py`:
  - `LLMProvider` Protocol with `call()` method
  - `MinimaxProvider`, `GroqProvider`, `OpenAICustomProvider` implementations
  - `ProviderRegistry` class with registration and priority chain
- Refactor `src/config/llm.py` to use the registry
- Cache LLM clients (currently re-created per call)

### 2.9 Merge track planners into shared service
- Create `src/services/track_planning.py` with unified `TrackPlanningService`
- Slim down both `track_planner_node.py` and `track_planner.py` to thin delegates

### 2.10 Consolidate instrument data into single source of truth
- Make `src/config/genre_registry.py` the canonical instrument repository
- Remove hardcoded `_get_genre_instruments()` from `src/agents/theory_validator_node.py`
- Update other modules to query `genre_registry` instead of maintaining separate databases

---

## Phase 3: Strategy Pattern for Generators

### 3.11 Extract generation strategies into composable classes
- Create `src/generation/strategies/` package:
  - `melody.py` — `MelodyStrategy` Protocol + 6 concrete implementations
  - `bass.py` — `BassStrategy` Protocol + 7 implementations
  - `drums.py` — `DrumStrategy` Protocol + 6 implementations
  - `pad.py` — `PadStrategy` Protocol + 4 implementations
  - `registry.py` — `StrategyRegistry` mapping genre/style/emotion to strategy classes

### 3.12 Consolidate generators
- Create `src/generation/generator.py` — single `MusicGenerator` using strategy injection
- Delete `src/app/generator.py` (210 lines) and `src/midigent/advanced_generator.py` (530 lines)
- Update all imports

---

## Phase 4: Consistency & Polish

### 4.13 Standardize logging
- Replace `print()` in `src/` modules with `logging.getLogger(__name__)`
- Keep `rich.print()` only in CLI-facing and TUI code

### 4.14 Standardize error handling
- Replace plain `str` error in `MusicState` with typed `PipelineError` dataclass

### 4.15 Clean up `__init__.py` re-exports
- Update all package `__init__.py` files to reflect new structure

### 4.16 Rename `midigent` → `analysis`
- Rename package after generation code moves out
- Update all imports project-wide

---

## Resulting Package Structure

```
src/
├── agents/          # LangGraph nodes + state definitions
├── analysis/        # Music theory, emotion, quality, genre validation (was midigent/)
├── app/             # Lightweight app-level orchestration (models, session, midi_creator)
├── config/          # Settings, LLM providers, genre registry, constants
│   ├── data/        # genre_tree.json
│   └── providers.py # Protocol-based LLM providers
├── experimental/    # Unintegrated USP features
├── generation/      # Music generator + strategy classes
│   └── strategies/  # Melody, bass, drums, pad strategies
├── intent/          # Intent engine, preprocessor, schema
│   └── templates/   # Externalized prompt templates
├── services/        # Shared services (track planning)
└── tui/             # Textual UI components
    └── data/        # presets.json
```

---

## Backlog (Logic Improvements — NOT in scope)

These were identified during analysis but require logic changes, so they are deferred:

1. **Async LLM support**: Add `async call_llm()` for concurrent provider calls
2. **Connection pooling**: Use `httpx` connection pooling for LLM HTTP clients
3. **Richer error context**: Preserve tracebacks in `MusicState["error"]` 
4. **Test coverage gaps**: Add unit tests for `MusicGenerator`, `MIDIGenerator`, `EmotionEngine`, `MusicTheoryEngine`, `LLMConfig.call_llm()`
5. **TUI widget interaction tests**: Currently only smoke tests
6. **Integrate USP features**: Wire `CreativeVariationEngine`, `EducationalInsightsEngine`, `ProfessionalAnalyticsEngine`, `CulturalMusicDetector` into the pipeline
7. **External genre definition files**: Allow users to add custom genres via config files
8. **Smart Groq model fallback**: Currently tries multiple models sequentially — could use health checks
9. **Duration parser consolidation**: `src/midigent/duration_parser.py` overlaps with `src/intent/preprocessor.py` — verify which is used and remove the other
10. **Packaging fix**: Move `main.py`/`main_tui.py` into a proper package so entry points work with `pip install`

---

## Verification Plan

1. After each phase: `python -m pytest tests/`
2. After Phase 1: verify `python main.py` and `python main_tui.py` still launch
3. After Phase 2: run MIDI generation test cases
4. After Phase 3: generate MIDI for each major genre and verify
5. Final: `pip install -e .` in clean venv, verify entry points
