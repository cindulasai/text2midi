# PLAN-001: Modern TUI Implementation Plan

**Spec:** SPEC-001-MODERN-TUI  
**Estimated Effort:** 3–4 days  
**Prerequisites:** Python 3.11+, `uv` package manager installed  

---

## Phase 1: Foundation (Day 1 — Morning)

### Step 1: Add Dependencies to pyproject.toml
Add to `[project.dependencies]`:
```
"textual>=0.80.0",
"platformdirs>=4.0.0",
```

Run `uv sync` to install.

### Step 2: Create AppSettings Class
Create `src/config/settings.py`:
- `AppSettings` singleton class
- Uses `platformdirs.user_config_dir("text2midi")` for config path
- Stores to `settings.json`: `{provider, api_key, custom_endpoint, custom_model, theme, history_max}`
- Methods: `load()`, `save()`, `get(key, default)`, `set(key, value)`, `apply_to_environment()`
- `apply_to_environment()` sets env vars (`MINIMAX_API_KEY`, `GROQ_API_KEY`, `OPENAI_API_KEY`) based on provider

### Step 3: Create Multi-Provider LLM Config Extension
Modify `src/config/llm.py`:
- Add `openai_custom` provider handling in `LLMConfig` class
- Accept `custom_endpoint` and `custom_model` parameters
- Fallback chain: selected provider → groq → minimax → openai_custom

### Step 4: Create main_tui.py Entry Scaffold
Create `main_tui.py` at project root:
- Minimal Textual `App` subclass: `class Text2MidiApp(App)`
- Empty `compose()` method (placeholder)
- `app.run()` entry point
- Add entry point to pyproject.toml: `text2midi-tui = "main_tui:main"`

---

## Phase 2: TUI Layout Skeleton (Day 1 — Afternoon)

### Step 5: Define CSS Styles
Create `src/tui/styles.tcss` (Textual CSS):
- Define layout grid: sidebar (20%) + main area (80%)
- Color scheme: Catppuccin Mocha palette (dark mode)
- Widget styles: input fields, buttons, panels, progress bars
- Responsive: minimum 80x24 terminal size

### Step 6: Build Main Layout Containers
In `main_tui.py`, implement `compose()`:
```python
def compose(self) -> ComposeResult:
    yield Header(show_clock=True)
    with Horizontal():
        yield Sidebar(id="sidebar")       # Genre presets, history
        with Vertical(id="main"):
            yield ApiKeySetup(id="setup")  # Shown conditionally
            yield PromptInput(id="prompt")
            yield ProgressPanel(id="progress")
            yield OutputPanel(id="output")
    yield Footer()
```

### Step 7: Create Widget Source Files
Create directory `src/tui/` with:
- `__init__.py`
- `widgets/__init__.py`
- `widgets/api_key_setup.py` — placeholder Static widget
- `widgets/prompt_input.py` — placeholder Static widget
- `widgets/progress_panel.py` — placeholder Static widget
- `widgets/output_panel.py` — placeholder Static widget
- `widgets/sidebar.py` — placeholder Static widget

Verify the app launches with `uv run python main_tui.py` and shows the layout skeleton.

---

## Phase 3: Core Widgets (Day 2 — Morning)

### Step 8: Implement ApiKeySetup Widget
`src/tui/widgets/api_key_setup.py`:
- `Select` widget for provider choice: MiniMax M2.5 / Groq Llama / OpenAI-compatible / Custom
- `Input` widget for API key (password=True)
- Conditional `Input` widgets for custom endpoint + model (shown when provider = "Custom")
- `Button` "Save & Connect" — stores to `AppSettings`, calls `LLMConfig.initialize()`
- Auto-hide after successful configuration
- Show on first launch when `AppSettings.get("api_key")` is empty

### Step 9: Implement PromptInput Widget
`src/tui/widgets/prompt_input.py`:
- `TextArea` widget (3 lines) with placeholder "Describe your music... (e.g., 'dreamy jazz with piano and soft drums')"
- `Button` "🎵 Generate" — posts `GenerateRequest` message
- `Button` "🎲 Surprise Me" — picks random prompt from `generate_dynamic_prompts()`
- Keybinding: `Ctrl+Enter` → generate, `Ctrl+R` → random prompt
- Disable inputs during generation

### Step 10: Implement ProgressPanel Widget
`src/tui/widgets/progress_panel.py`:
- `ProgressBar` widget (Textual built-in)
- `Static` label showing current agent node: `"Step 3/8: Theory Validator..."`
- Node map: `NODES = ["Intent Parser", "Track Planner", "Theory Validator", "Track Generator", "Quality Control", "Refinement", "MIDI Creator", "Session Summary"]`
- Method: `update_progress(node_name: str)` — advances progress bar + updates label
- Hidden when not generating

---

## Phase 4: Generation Pipeline Integration (Day 2 — Afternoon)

### Step 11: Create Generation Worker
`src/tui/workers/generation_worker.py`:
- Textual `Worker` class that runs `graph.stream()` in a thread
- Constructs `MusicState` initial dict (identical to `main.py:run_generation_workflow`)
- Uses `graph.stream(initial_state, config, stream_mode="values")` to yield per-node state
- Posts messages to the app: `NodeStarted(node_name)`, `NodeCompleted(node_name, elapsed)`, `GenerationComplete(final_state)`, `GenerationError(error)`
- Handles exceptions with full traceback logging

### Step 12: Wire Generation Flow in App
In `main_tui.py`:
- `on_button_pressed(event)` handler for "Generate" button
- Starts `GenerationWorker.run()` via `self.run_worker()`
- Updates `ProgressPanel` on `NodeStarted`/`NodeCompleted` messages
- On `GenerationComplete`: populate `OutputPanel`, save to history, show completion message
- On `GenerationError`: show error in `OutputPanel` with retry button

### Step 13: Implement OutputPanel Widget
`src/tui/widgets/output_panel.py`:
- `DataTable` showing generated tracks: columns = `[Channel, Instrument, Type, Notes, Duration]`
- `Markdown` widget showing composition summary (from `session_summary_node` output)
- `Static` showing quality score: `"Quality: 0.87/1.0 ■■■■■■■■□□"`
- `Static` showing file path with "Open Folder" button
- "Open Folder" button opens Explorer to the output directory via `os.startfile()`

---

## Phase 5: LLM Autocomplete (Day 3 — Morning)

### Step 14: Create PromptSuggester
`src/tui/suggest/prompt_suggester.py`:
- Implements Textual `Suggester` protocol (abstract class with `get_suggestion(value: str) -> str | None`)
- Connects to LLM via `call_llm()` for intelligent suggestions
- System prompt: `"You are a music prompt completer. Given a partial text, suggest the complete prompt. Respond with ONLY the completion text, no explanation."`
- **Debounce:** Only call LLM after 300ms of no typing (using `asyncio.sleep` + cancellation)
- **Fallback:** If LLM fails or timeout (2s), use `StaticSuggester` with genre keywords
- **Cache:** LRU cache (maxsize=50) of prefix → suggestion pairs

### Step 15: Create SuggestionCarousel Widget
`src/tui/widgets/suggestion_carousel.py`:
- Horizontal list of clickable suggestion chips rendered below the prompt input
- Each chip: `Button` with genre-specific suggestion text
- Sources: preloaded genre prompts from `constants.GENRE_CONFIG`
- Updates dynamically when user types: shows filtered matches
- Click → populates prompt input with chip text
- Keybinding: `Tab` cycles through visible chips, `Enter` selects

### Step 16: Wire Autocomplete to PromptInput
In `prompt_input.py`:
- Attach `PromptSuggester` to `TextArea` via Textual's `Suggester` API
- Show ghost text (dimmed) for the current suggestion
- `Tab` accepts the suggestion into the input
- `Esc` dismisses the suggestion
- Mount `SuggestionCarousel` below the input area

---

## Phase 6: Preset & History System (Day 3 — Afternoon)

### Step 17: Implement Sidebar Widget
`src/tui/widgets/sidebar.py`:
- `Tree` widget with two root nodes: "🎵 Presets" and "📂 History"
- **Presets section:** Loads from `generate_dynamic_prompts()` — grouped by genre
  - Each genre: expandable tree node with 3 preset prompts
  - Click preset → populates prompt input
- **History section:** Loads from `AppSettings.get("history", [])`
  - Each entry: `{timestamp, prompt, genre, quality, midi_path}`
  - Most recent first, max 50 entries
  - Click entry → populates prompt input with that prompt
  - Right-click (Textual doesn't support right-click, so use keybinding `Delete` on selected) → remove from history

### Step 18: Create History Manager
`src/tui/history.py`:
- `HistoryManager` class with JSON file storage (`platformdirs.user_data_dir("text2midi") / "history.json"`)
- Methods: `add_entry(prompt, genre, quality, midi_path)`, `get_entries(limit=50)`, `remove_entry(timestamp)`, `clear()`
- Auto-prunes to 50 entries (configurable via `AppSettings`)
- Thread-safe (uses `asyncio.Lock`)

---

## Phase 7: Polish & UX (Day 4 — Morning)

### Step 19: Add Keybinding System
In `main_tui.py`:
- Global keybindings:
  - `Ctrl+G` — Focus prompt input + generate
  - `Ctrl+R` — Random prompt
  - `Ctrl+H` — Toggle sidebar
  - `Ctrl+S` — Open settings (API key)
  - `Ctrl+O` — Open output folder
  - `Ctrl+Q` — Quit
  - `F1` — Help screen
- Show keybindings in Textual `Footer` widget

### Step 20: Add Error Handling & Notifications
- Textual `Notification` toasts for: generation complete, errors, settings saved
- Generation timeout: 120 seconds → show "still generating..." at 60s
- Network errors: clear message + "Check API key" button
- Invalid prompt: show warning in PromptInput validation

### Step 21: Add Help Screen
`src/tui/widgets/help_screen.py`:
- `ModalScreen` overlay showing:
  - Keybinding reference table
  - Supported genres list
  - Supported providers list
  - Tips for getting best results
  - Link to documentation

---

## Phase 8: Testing & Integration (Day 4 — Afternoon)

### Step 22: Unit Tests
`tests/test_tui/`:
- `test_app_settings.py` — Settings CRUD, persistence, environment variable application
- `test_history_manager.py` — Add, retrieve, prune, clear
- `test_prompt_suggester.py` — Cache, debounce, LLM-free fallback
- `test_generation_worker.py` — Mock graph, verify message sequence

### Step 23: Integration Tests
`tests/test_tui/`:
- `test_tui_app.py` — Uses Textual's `App.run_test()` pilot:
  - Test: app launches without errors
  - Test: API key flow → save → collapse
  - Test: type prompt → click generate → see progress → see output
  - Test: sidebar preset click → populates prompt
  - Test: keybindings work

### Step 24: Update pyproject.toml
- Add `text2midi-tui = "main_tui:main"` entry point
- Add `textual`, `platformdirs` to dependencies
- Add `textual-dev` to `[project.optional-dependencies.dev]`
- Verify `uv run text2midi-tui` launches the app

---

## Dependency Chain

```
Phase 1 (Foundation)
  └── Phase 2 (Skeleton)
        ├── Phase 3 (Core Widgets) ── ── ── ── ─┐
        │     └── Phase 4 (Generation Pipeline)  │
        │           └── Phase 7 (Polish)         │
        ├── Phase 5 (LLM Autocomplete) ── ── ── ─┤
        └── Phase 6 (Presets & History) ── ── ── ─┘
                                                  │
                                                  └── Phase 8 (Testing)
```

Phases 3, 5, and 6 can be developed in parallel after Phase 2 is complete. Phase 4 depends on Phase 3. Phase 7 depends on Phases 3-6. Phase 8 depends on all prior phases.
