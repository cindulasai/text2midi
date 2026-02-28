# Implementation Plan

> Step-by-step code changes required to integrate the expanded genre hierarchy, scales, rhythms, instruments, and presets into the codebase.

---

## Phase 1: Foundation — `src/config/genre_registry.py` (NEW)

**Purpose:** Single source of truth for all genre, scale, instrument, and rhythm data.

### Design
- `GenreNode` dataclass with all parameters from GENRE_TAXONOMY.md
- `GENRE_TREE` dict: flat registry keyed by dot-notation ID (e.g., `"electronic.house.deep_house"`)
- Root genres also registered at their short key (e.g., `"electronic"`)
- Helper functions: `get_genre()`, `get_root_genres()`, `get_children()`, `find_by_alias()`, `all_genre_ids()`, `get_genre_ids_for_validation()`
- `SCALES` dict: expanded to 30 scales
- `GM_INSTRUMENTS_EXTENDED` dict: merged from constants.py + new world instruments
- Backward-compatible: original 10 genre IDs still work

### Files Created
- `src/config/genre_registry.py`

---

## Phase 2: Update Consumers

### 2a. `src/app/constants.py`
- Import `SCALES` from `genre_registry` (or keep inline but expanded)
- Add new GM_INSTRUMENTS entries
- Keep GENRE_CONFIG for backward compat, but populate from registry
- Keep CHORD_PROGRESSIONS for backward compat, expand with registry data

### 2b. `src/intent/schema.py`
- Replace hardcoded `SUPPORTED_GENRES` tuple with dynamic import from registry
- Replace hardcoded `SUPPORTED_SCALES` tuple with dynamic import
- Change `GenreInfo.primary` from `Literal[...]` to `str` with validator
- Add `sub_genre: Optional[str]` field to `GenreInfo`
- Update `GENRE_TEMPO_RANGES` to load from registry

### 2c. `src/intent/prompt_templates.py`
- Replace hardcoded `_SUPPORTED_GENRES` string with dynamic list from registry
- Replace `_GENRE_CONTEXT` block with dynamically generated genre reference
- Add world music few-shot examples

### 2d. `src/intent/engine.py`
- Expand `_fallback_keyword_parse` genre_keywords dict with 100+ new entries
- Expand `_GENRE_INSTRUMENTS` in `_enrich_defaults` from registry
- Expand `_GENRE_DEFAULT_KEY` from registry
- Add world music context rules

### 2e. `src/intent/preprocessor.py`
- Add world music abbreviations to `_ABBREVIATIONS` dict

### 2f. `src/midigent/genre_validator.py`
- Load `GenreCharacteristic.GENRES` from registry instead of hardcoded dict
- Add missing genres (rnb + all new)

### 2g. `src/tui/widgets/sidebar.py`
- Expand `_PRESETS` dict with hierarchical genre categories
- Add world music presets

---

## Phase 3: Tests

### New test file: `tests/test_genre_registry.py`
- Test registry loads without error
- Test all 210+ genre IDs resolve
- Test backward compat (original 10 IDs)
- Test helper functions
- Test hierarchy traversal

### Update: `tests/test_intent_engine.py`
- Add tests for new genre IDs in schema
- Add tests for world music keyword parsing
- Add tests for new scale validation
