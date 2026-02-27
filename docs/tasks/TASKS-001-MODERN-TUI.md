# TASKS-001: Modern TUI — Atomic Task Checklist

**Plan:** PLAN-001-MODERN-TUI  
**Spec:** SPEC-001-MODERN-TUI  
**Status:** ✅ **COMPLETE** (33/33 tasks, 32/32 tests passing)  
**Completed:** February 26, 2026  

Each task is atomic — completable in one coding session (15–60 min). Tasks are ordered by dependency.

---

## Phase 1: Foundation

- [x] **T-001.01** — Add `textual>=0.80.0` and `platformdirs>=4.0.0` to `pyproject.toml` `[project.dependencies]` and run `uv sync`
- [x] **T-001.02** — Create `src/config/settings.py` with `AppSettings` class: `load()`, `save()`, `get()`, `set()`, `apply_to_environment()`. Store JSON at `platformdirs.user_config_dir("text2midi")/settings.json`. Keys: `provider`, `api_key`, `custom_endpoint`, `custom_model`, `theme`, `history_max`.
- [x] **T-001.03** — Add `openai_custom` provider support to `src/config/llm.py`: accept `custom_endpoint` and `custom_model` params, add to fallback chain after `groq`
- [x] **T-001.04** — Create `main_tui.py` at project root with minimal `Text2MidiApp(App)` subclass, empty `compose()`, `app.run()` entry point. Add `text2midi-tui = "main_tui:main"` to `pyproject.toml` `[project.scripts]`. Verify: `uv run python main_tui.py` opens a blank Textual app.

## Phase 2: TUI Layout Skeleton

- [x] **T-001.05** — Create directory structure: `src/tui/__init__.py`, `src/tui/widgets/__init__.py`, `src/tui/workers/__init__.py`, `src/tui/suggest/__init__.py`
- [x] **T-001.06** — Create `src/tui/styles.tcss` with Catppuccin Mocha theme: layout grid (sidebar 20%, main 80%), color variables, widget base styles, minimum 80x24 terminal
- [x] **T-001.07** — Create placeholder widget files: `api_key_setup.py`, `prompt_input.py`, `progress_panel.py`, `output_panel.py`, `sidebar.py` — each with a `Static` widget showing the widget name
- [x] **T-001.08** — Implement `main_tui.py` `compose()` method: `Header`, `Horizontal(Sidebar, Vertical(ApiKeySetup, PromptInput, ProgressPanel, OutputPanel))`, `Footer`. Load `styles.tcss`. Verify: layout renders correctly with placeholder text in each panel.

## Phase 3: Core Widgets

- [x] **T-001.09** — Implement `ApiKeySetup` widget: `Select` for provider (4 options), `Input` for API key (password mode), conditional `Input` fields for custom endpoint/model, `Button` "Save & Connect"
- [x] **T-001.10** — Wire `ApiKeySetup` save button: store to `AppSettings`, call `LLMConfig.initialize()`, apply env vars, collapse widget on success, show validation errors on failure
- [x] **T-001.11** — Add auto-show/hide logic for `ApiKeySetup`: show on first launch (no API key), hide after save, show when "Change API Key" is triggered from output panel
- [x] **T-001.12** — Implement `PromptInput` widget: `TextArea` (3 lines, placeholder text), `Button` "🎵 Generate", `Button` "🎲 Surprise Me"
- [x] **T-001.13** — Add keybindings to `PromptInput`: `Ctrl+Enter` → generate, `Ctrl+R` → random prompt (from `generate_dynamic_prompts()`)
- [x] **T-001.14** — Implement `ProgressPanel` widget: `ProgressBar`, `Static` label with node map (`NODES` list of 8 names), `update_progress(node_name)` method. Hidden when not generating.

## Phase 4: Generation Pipeline Integration

- [x] **T-001.15** — Create `src/tui/workers/generation_worker.py`: Textual `Worker` class, constructs `MusicState` initial dict (match `main.py:run_generation_workflow` exactly), runs `graph.stream()` in thread
- [x] **T-001.16** — Define message classes: `NodeStarted(node_name)`, `NodeCompleted(node_name, elapsed)`, `GenerationComplete(final_state)`, `GenerationError(error)` — post from worker to app
- [x] **T-001.17** — Wire generation flow in `main_tui.py`: handle "Generate" button → start worker, handle `NodeStarted`/`NodeCompleted` → update `ProgressPanel`, handle `GenerationComplete` → populate output, handle `GenerationError` → show error
- [x] **T-001.18** — Implement `OutputPanel` widget: `DataTable` (columns: Channel, Instrument, Type, Notes, Duration), `Markdown` for summary, `Static` for quality score with visual bar, `Static` for file path, `Button` "Open Folder" → `os.startfile()`, `Button` "Change API Key"
- [x] **T-001.19** — Disable PromptInput during generation (both TextArea and buttons), re-enable on complete/error. Show RichLog fallback if generation produces warnings.

## Phase 5: LLM Autocomplete

- [x] **T-001.20** — Create `src/tui/suggest/prompt_suggester.py`: implements Textual `Suggester` protocol, calls `call_llm()` with music completion system prompt, 300ms debounce via `asyncio.sleep` + cancellation, 2s timeout, LRU cache (50 entries)
- [x] **T-001.21** — Create fallback `StaticSuggester` in same file: returns genre keyword completions from `constants.GENRE_CONFIG` when LLM is unavailable
- [x] **T-001.22** — Create `src/tui/widgets/suggestion_carousel.py`: horizontal `Button` chips below prompt input, sourced from `GENRE_CONFIG` preset prompts, filtered as user types, `Tab` cycles chips, `Enter`/click selects
- [x] **T-001.23** — Wire autocomplete: attach `PromptSuggester` to `TextArea`, show ghost text for suggestions, `Tab` accepts, `Esc` dismisses, mount `SuggestionCarousel` below prompt

## Phase 6: Preset & History System

- [x] **T-001.24** — Create `src/tui/history.py`: `HistoryManager` class with JSON file storage at `platformdirs.user_data_dir("text2midi")/history.json`, methods: `add_entry()`, `get_entries(limit=50)`, `remove_entry()`, `clear()`, thread-safe with `asyncio.Lock`, auto-prune to 50
- [x] **T-001.25** — Implement `Sidebar` widget: `Tree` with "🎵 Presets" root (genre-grouped presets from `generate_dynamic_prompts()`) and "📂 History" root (from `HistoryManager`). Click preset/history → populate prompt input. `Delete` key on history item → remove.
- [x] **T-001.26** — Wire history: on `GenerationComplete` → call `HistoryManager.add_entry()` → refresh sidebar history tree

## Phase 7: Polish & UX

- [x] **T-001.27** — Add global keybindings to `main_tui.py`: `Ctrl+G` (generate), `Ctrl+R` (random), `Ctrl+H` (toggle sidebar), `Ctrl+S` (settings), `Ctrl+O` (open folder), `Ctrl+Q` (quit), `F1` (help). Show in `Footer`.
- [x] **T-001.28** — Create `src/tui/widgets/help_screen.py`: `ModalScreen` with keybinding table, supported genres, providers, tips. Triggered by `F1`.
- [x] **T-001.29** — Add Textual `Notification` toasts: generation complete (with quality), error messages, settings saved confirmation. Add 120s generation timeout with "still generating..." at 60s.

## Phase 8: Testing

- [x] **T-001.30** — Create `tests/test_tui/test_app_settings.py`: test CRUD, persistence, env var application, default values, edge cases (missing file, corrupt JSON)
- [x] **T-001.31** — Create `tests/test_tui/test_history_manager.py`: test add, retrieve, prune at 50, clear, thread safety, file persistence
- [x] **T-001.32** — Create `tests/test_tui/test_prompt_suggester.py`: test cache hits, debounce behavior, LLM timeout fallback, static suggester
- [x] **T-001.33** — Create `tests/test_tui/test_tui_app.py`: Textual `App.run_test()` pilot tests — app launches, API key flow, generate flow with mocked graph, sidebar interaction, keybindings

---

## Summary

| Phase | Tasks | Est. Time |
|-------|-------|-----------|
| 1. Foundation | T-001.01 – T-001.04 | 2 hours | ✅ Complete |
| 2. Skeleton | T-001.05 – T-001.08 | 2 hours | ✅ Complete |
| 3. Core Widgets | T-001.09 – T-001.14 | 4 hours | ✅ Complete |
| 4. Generation | T-001.15 – T-001.19 | 4 hours | ✅ Complete |
| 5. Autocomplete | T-001.20 – T-001.23 | 3 hours | ✅ Complete |
| 6. History | T-001.24 – T-001.26 | 2 hours | ✅ Complete |
| 7. Polish | T-001.27 – T-001.29 | 2 hours | ✅ Complete |
| 8. Testing | T-001.30 – T-001.33 | 3 hours | ✅ Complete |
| **Total** | **33 tasks** | **~22 hours** | **✅ All Complete** |
