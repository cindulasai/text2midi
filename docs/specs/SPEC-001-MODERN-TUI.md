# SPEC-001: Modern TUI Interface (`main_tui.py`)

**Status:** Draft  
**Created:** 2026-02-26  
**Author:** spec-kit  
**Priority:** P0 — Core UX Enhancement  

---

## 1. Overview

Replace the basic `input()`-based interactive CLI in `main.py` with a full Textual TUI application in `main_tui.py` at the project root. The TUI provides a rich, mouse-enabled terminal interface with LLM-powered inline autocomplete, auto-rotating prompt suggestions, real-time agent pipeline progress, Rich-formatted output panels, and one-click file explorer access for drag-and-drop MIDI files into DAWs.

## 2. User Stories

| ID | As a... | I want to... | So that... |
|----|---------|-------------|------------|
| US-01 | Music producer | Type a prompt and see LLM-powered autocomplete suggestions inline | I can write prompts faster and get creative ideas |
| US-02 | Music producer | See rotating prompt suggestions that auto-cycle every 4 seconds | I can pick one with a single keypress instead of thinking from scratch |
| US-03 | Music producer | Click a "Generate" button with my mouse | I don't need to memorize keyboard shortcuts |
| US-04 | Music producer | See real-time progress as each agent node completes | I know the system is working and how far along it is |
| US-05 | Music producer | See a summary of generated tracks (instrument, channel, note count) | I understand what was generated before importing to DAW |
| US-06 | Music producer | Click "Open Folder" to open the output directory in Explorer | I can immediately drag-and-drop the MIDI file into Ableton |
| US-07 | Music producer | Configure my API key and LLM provider once in a settings modal | I don't have to edit `.env` files manually |
| US-08 | Music producer | See my generation history in a sidebar | I can review and compare past generations |
| US-09 | First-time user | Be guided through API key setup on first launch | I can start generating without reading documentation |

## 3. Functional Requirements

### 3.1 Application Framework

- **Framework:** Textual >= 0.80.0
- **Entry point:** `main_tui.py` at project root (same level as `main.py`)
- **Entry point function:** `def main() -> None` — instantiates and runs the Textual App
- **pyproject.toml script:** `text2midi-tui = "main_tui:main"`
- **New dependency:** Add `textual>=0.80.0` to `[project.dependencies]` in `pyproject.toml`

### 3.2 Screen Layout (Single Screen App)

The TUI uses ONE main screen with this layout:

```
┌─────────────────────────────────────────────────────────────┐
│ [Header]  text2midi v2.0 │ Provider: MiniMax ● │ ⚙ Settings │
├──────────────────────────────────────────────┬──────────────┤
│                                              │  [History]   │
│  [Suggestion Carousel]                       │  ─────────── │
│  💡 "Create a dreamy lofi beat with soft..." │  1. Jazz...  │
│      ← auto-rotates every 4s →              │  2. Ambient..│
│      [Click or Enter to use]                 │  3. Pop...   │
│                                              │  (click to   │
│  [Prompt Input]                              │   re-view)   │
│  ┌─────────────────────────────────────────┐ │              │
│  │ Type your music description...  [ghost] │ │              │
│  └─────────────────────────────────────────┘ │              │
│                                              │              │
│  [Generate Button]  🎵 Generate              │              │
│                                              │              │
│  [Progress Panel]                            │              │
│  ████████████░░░░ 5/8 nodes │ Quality Ctrl   │              │
│  ✓ Intent Parser (0.8s)                      │              │
│  ✓ Track Planner (1.2s)                      │              │
│  ✓ Theory Validator (0.3s)                   │              │
│  ✓ Track Generator (2.1s)                    │              │
│  ⟳ Quality Control...                        │              │
│                                              │              │
│  [Output Panel] (shown after generation)     │              │
│  ┌─────────────────────────────────────────┐ │              │
│  │ Genre: jazz │ Quality: 0.87 │ 5 tracks  │ │              │
│  │ Track │ Instrument │ Ch │ Notes │ Bars  │ │              │
│  │ lead  │ piano      │ 1  │ 127   │ 64    │ │              │
│  │ bass  │ bass       │ 2  │ 64    │ 64    │ │              │
│  │ drums │ drums      │ 10 │ 256   │ 64    │ │              │
│  │ ...   │            │    │       │       │ │              │
│  │                                         │ │              │
│  │ File: outputs/midigen_jazz_abc123...mid │ │              │
│  │ [📂 Open Folder]                        │ │              │
│  └─────────────────────────────────────────┘ │              │
├──────────────────────────────────────────────┴──────────────┤
│ [Footer]  Tab: accept suggestion │ Ctrl+G: generate │ F1: help│
└─────────────────────────────────────────────────────────────┘
```

### 3.3 Widget Specifications

#### 3.3.1 Header Bar
- Textual `Header` widget with app title: `"text2midi v2.0"`
- Right-aligned status indicators:
  - LLM provider name + colored circle: green = connected, red = no API key, yellow = fallback provider active
  - Settings gear icon button (opens Settings modal on click)

#### 3.3.2 Suggestion Carousel
- Custom `Static` widget subclass: `SuggestionCarousel(Static)`
- On app mount: calls `_refresh_suggestions()` via `@work(thread=True)` decorator to generate 5 prompts using existing `generate_dynamic_prompts()` logic from `main.py` lines 90-150
- Displays ONE suggestion at a time with title + prompt text
- Auto-rotates every 4 seconds via `self.set_interval(4.0, self._next_suggestion)`
- Manual rotation: Left/Right arrow keys when focused
- **Accept action:** Click on the carousel OR press `Enter` when focused → copies the prompt text to the Prompt Input widget via `self.app.query_one(PromptInput).value = prompt`
- Falls back to 5 static presets if LLM unavailable (same presets from `main.py` `get_preset_prompts()`)
- Styled with a subtle border and `💡` icon prefix

#### 3.3.3 Prompt Input Widget
- Custom subclass: `PromptInput(Input)` with `suggester=LLMSuggester()`
- Placeholder text: `"Describe your music... (e.g., 'mellow jazz with piano and bass')"`
- Max length: 500 characters
- Ghost text (inline completion) appears as the user types, styled with dim opacity via Textual's built-in `input--suggestion` CSS component class
- Accept suggestion: `Right` arrow key or `Tab` key (Tab requires binding override)
- Multi-line NOT needed — single-line Input is sufficient (prompts are 1-2 sentences)

#### 3.3.4 LLM Suggester (Autocomplete Engine)
- **File:** `src/app/llm_suggester.py` — new file
- **Class:** `LLMSuggester(Suggester)` — subclass of `textual.widgets._input.Suggester`
- **Method:** `async def get_suggestion(self, value: str) -> str | None`
- **Debounce:** Internal `asyncio.Event` + timer pattern. Only calls LLM after 600ms of no new keystrokes. Each new keystroke cancels the pending timer.
- **LLM call:** Uses `call_llm(system_prompt, user_message, temperature=0.9, max_tokens=50)` from `src.config.llm`
  - System prompt: `"You are an autocomplete engine for a music generation tool. The user is typing a music description prompt. Complete their sentence naturally. Return ONLY the completion text (the remaining words), not the original text. Keep it under 20 words. Be creative and musically descriptive."`
  - User message: `f"Complete this music prompt: '{value}'"`
- **Return:** The completion text (not including the original value). Textual displays it as ghost text after the cursor.
- **Fallback:** If LLM is unavailable or times out (2s), fall back to `SuggestFromList` with a static list of 50 genre/mood/instrument keywords: `["ambient", "jazz", "lofi", "cinematic", "epic orchestral", "funky bass", "dreamy pads", "aggressive drums", ...]`
- **Cache:** LRU cache of last 20 completions (keyed by value) to avoid redundant LLM calls
- **Error handling:** All exceptions caught and return `None` (no suggestion shown, no crash)

#### 3.3.5 Generate Button
- `Button("🎵 Generate", id="generate-btn", variant="primary")`
- Disabled state: when backend is generating (prevent double-submit) or when prompt input is empty
- On click OR `Ctrl+G` keybinding: triggers `self.action_generate()`
- Visually: large, centered, high-contrast button

#### 3.3.6 Progress Panel
- Custom `Widget` subclass: `ProgressPanel(Widget)`
- Contains:
  - `ProgressBar` — 8 steps total (one per agent node)
  - Per-node status list rendered as `RichLog`:
    - Pending: `○ Node Name`
    - Running: `⟳ Node Name...` (with Rich Spinner)
    - Completed: `✓ Node Name (X.Xs)` (green, with elapsed time)
    - Failed: `✗ Node Name — error message` (red)
- Hidden when no generation is in progress
- Node names (in order): `"Intent Parser"`, `"Track Planner"`, `"Theory Validator"`, `"Track Generator"`, `"Quality Control"`, `"Refinement"` (conditional), `"MIDI Creator"`, `"Session Summary"`
- Updates via Textual `Message` system — worker thread posts `NodeProgress(name, status, elapsed)` messages

#### 3.3.7 Output Panel
- Custom `Widget` subclass: `OutputPanel(Widget)`
- Hidden until generation completes
- Contains:
  - Summary line: `"Genre: {genre} │ Quality: {score:.2f}/1.0 │ {n} tracks │ {bars} bars │ {tempo} BPM"`
  - `DataTable` with columns: `Track`, `Instrument`, `Channel`, `Notes`, `Type`
    - Rows populated from `state["generated_tracks"]` — each `Track` object has `.name`, `.midi_program`, `.channel`, `.notes` (list length = note count), `.track_type`
  - File path display: full path to the `.mid` file
  - `Button("📂 Open Folder", id="open-folder-btn")` — on click calls `os.startfile(output_dir)` on Windows (use `subprocess.Popen(["explorer", output_dir])` as fallback)
  - Quality score color-coded: green >= 0.8, yellow >= 0.6, red < 0.6

#### 3.3.8 History Sidebar
- `ListView` widget in a collapsible right panel (Textual `Horizontal` layout, right column ~25% width)
- Each `ListItem` shows: generation number, genre, quality score, truncated prompt (first 30 chars)
- Click item → re-populates OutputPanel with that generation's data (stored in a session list `self.generations: list[dict]`)
- Scrollable, most recent at top
- Max 50 items per session

#### 3.3.9 Settings Modal
- `Screen` subclass: `SettingsScreen(Screen)` — displayed as modal overlay via `self.app.push_screen(SettingsScreen())`
- Opened by: clicking gear icon in header, OR pressing `F2`
- Contents:
  - **Provider radio group:** `RadioSet` with options: `"MiniMax M2.5"`, `"Groq (Llama)"`, `"OpenAI-compatible"`, `"Custom Endpoint"`
  - **API Key input:** `Input(password=True, placeholder="Enter API key...")` — masked by default
  - **Custom endpoint URL:** `Input(placeholder="https://api.example.com/v1")` — shown ONLY when "Custom Endpoint" is selected (toggle visibility via `watch_` reactive)
  - **Custom model name:** `Input(placeholder="model-name")` — shown ONLY with custom endpoint
  - **Output directory:** `Input(value="outputs/")` — pre-filled with current output dir
  - **Save button:** `Button("Save & Close", variant="primary")` — persists to config file and closes modal
  - **Cancel button:** `Button("Cancel")` — closes without saving
- **Persistence:** JSON file at `platformdirs.user_config_dir("text2midi") / "config.json"`
  ```json
  {
    "provider": "minimax",
    "api_keys": {
      "minimax": "sk-...",
      "groq": "gsk_...",
      "custom": "sk-..."
    },
    "custom_endpoint": "",
    "custom_model": "",
    "output_dir": "outputs/",
    "theme": "dark"
  }
  ```
- **First-run behavior:** If config file doesn't exist on app launch, auto-open SettingsScreen with a welcome message: "Welcome to text2midi! Enter your API key to get started."
- **API key storage:** Store in plaintext in user config dir (add comment in code noting this is local machine only). Do NOT use encryption — it adds complexity with no real security benefit for local API keys.

#### 3.3.10 Footer
- Textual `Footer` widget with keybindings display
- Bindings: `Tab` (accept suggestion), `Ctrl+G` (generate), `F1` (help/about), `F2` (settings), `Ctrl+Q` (quit)

### 3.4 Generation Workflow Integration

The TUI reuses the existing LangGraph pipeline from `src/agents/graph.py`. The generation workflow runs in a Textual `Worker` to avoid blocking the UI:

```
User clicks Generate
  → self.run_worker(self._generate_worker(prompt), thread=True)
    → Worker thread:
      1. Import get_agentic_graph from src.agents.graph
      2. Build initial MusicState dict (same structure as main.py run_generation_workflow)
      3. Use graph.stream() instead of graph.invoke() for node-level progress
         - For each chunk yielded by stream(), post a NodeProgress message to the app
      4. On completion, extract final state and post GenerationComplete message
    → Main thread:
      - NodeProgress messages update ProgressPanel
      - GenerationComplete message populates OutputPanel, adds to history
```

**Critical implementation detail for streaming:** The LangGraph `CompiledGraph.stream()` method yields `dict` chunks where each key is a node name and value is the state update from that node. Example:

```python
graph = get_agentic_graph()
config = {"configurable": {"thread_id": session_id}}
for chunk in graph.stream(initial_state, config=config):
    for node_name, node_output in chunk.items():
        # node_name is e.g. "intent_parser", "track_planner" etc.
        # node_output is the partial state dict returned by that node
        self.post_message(NodeProgress(node_name, "completed"))
```

### 3.5 Configuration and Settings Management

**New file:** `src/config/settings.py`

```python
"""Persistent settings manager using platformdirs."""

import json
from pathlib import Path
from platformdirs import user_config_dir
from dataclasses import dataclass, field, asdict
from typing import Optional, Dict

CONFIG_DIR = Path(user_config_dir("text2midi"))
CONFIG_FILE = CONFIG_DIR / "config.json"

@dataclass
class AppSettings:
    provider: str = "minimax"
    api_keys: Dict[str, str] = field(default_factory=dict)
    custom_endpoint: str = ""
    custom_model: str = ""
    output_dir: str = "outputs/"
    theme: str = "dark"

    @classmethod
    def load(cls) -> "AppSettings":
        if CONFIG_FILE.exists():
            data = json.loads(CONFIG_FILE.read_text())
            return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})
        return cls()

    def save(self) -> None:
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        CONFIG_FILE.write_text(json.dumps(asdict(self), indent=2))

    def apply_to_environment(self) -> None:
        """Set environment variables from stored API keys so LLMConfig can read them."""
        import os
        key_map = {"minimax": "MINIMAX_API_KEY", "groq": "GROQ_API_KEY"}
        for provider, env_var in key_map.items():
            if provider in self.api_keys and self.api_keys[provider]:
                os.environ[env_var] = self.api_keys[provider]
        # Custom endpoint: set as OPENAI-compatible
        if self.custom_endpoint and "custom" in self.api_keys:
            os.environ["OPENAI_API_KEY"] = self.api_keys.get("custom", "")
            os.environ["OPENAI_BASE_URL"] = self.custom_endpoint
```

**Integration with LLMConfig:** After loading settings and calling `apply_to_environment()`, call `LLMConfig.initialize()`. For custom endpoints, extend `src/config/llm.py` to support an `"openai_custom"` provider that reads `OPENAI_API_KEY` and `OPENAI_BASE_URL` env vars and uses the standard OpenAI client.

### 3.6 LLM Provider Extension (Custom Endpoint Support)

**Modify:** `src/config/llm.py` — add support for a third provider `"openai_custom"`:

- Add class variables:
  ```python
  OPENAI_CUSTOM_API_KEY: str = os.environ.get("OPENAI_API_KEY", "")
  OPENAI_CUSTOM_BASE_URL: str = os.environ.get("OPENAI_BASE_URL", "")
  OPENAI_CUSTOM_MODEL: str = os.environ.get("OPENAI_MODEL", "gpt-4")
  ```
- In `initialize()`: check if `OPENAI_CUSTOM_API_KEY` and `OPENAI_CUSTOM_BASE_URL` are set → add `"openai_custom"` to `AVAILABLE_PROVIDERS`
- Add `_call_openai_custom()` function: use `openai.OpenAI(api_key=..., base_url=...)` client (already a dependency)
- Provider priority becomes: minimax → groq → openai_custom
- Add `set_custom_endpoint(api_key, base_url, model)` class method for runtime configuration

### 3.7 CSS Styling

**New file:** `main_tui.tcss` (Textual CSS file, same directory as `main_tui.py`)

Textual CSS defines widget styling. Key rules:

```css
Screen {
    background: $surface;
}

#suggestion-carousel {
    height: 5;
    border: solid $primary;
    margin: 1 2;
    padding: 0 1;
}

#prompt-input {
    margin: 0 2;
}

#generate-btn {
    margin: 1 2;
    width: 100%;
    max-width: 40;
}

#progress-panel {
    height: auto;
    max-height: 16;
    margin: 0 2;
    border: solid $secondary;
}

#output-panel {
    margin: 1 2;
    border: solid $success;
    height: auto;
}

#history-sidebar {
    width: 30;
    border-left: solid $primary;
}

DataTable {
    height: auto;
    max-height: 12;
}
```

### 3.8 Keybindings

| Key | Action | Context |
|-----|--------|---------|
| `Tab` | Accept inline LLM suggestion | When prompt input is focused |
| `Enter` | Accept carousel suggestion OR submit prompt (context-dependent) | Carousel focused / Prompt focused |
| `Ctrl+G` | Trigger generation | Global |
| `F1` | Show help/about dialog | Global |
| `F2` | Open settings modal | Global |
| `Ctrl+Q` | Quit application | Global |
| `Left`/`Right` | Navigate carousel manually | Carousel focused |
| `Ctrl+O` | Open output folder | After generation |

### 3.9 Error Handling

- **No API key:** First-run wizard opens. If user cancels, show banner: "⚠ No API key configured. Press F2 to open settings."
- **LLM call failure:** Suggestions fall back to static list. Generation uses LangGraph's built-in error handling (nodes set `state["error"]`). Show error in OutputPanel with red styling.
- **Network timeout:** 30-second timeout on LLM calls. Show "Generation timed out" in progress panel.
- **Graph exception:** Catch all exceptions in the worker thread, post `GenerationError(message)` to the app, show in progress panel.

## 4. Non-Functional Requirements

- **Startup time:** < 2 seconds to show the TUI (lazy-import heavy modules)
- **LLM autocomplete latency:** < 1.5 seconds for suggestion to appear (with debounce)
- **Memory:** < 200MB RSS during generation
- **Terminal compatibility:** Optimized for Windows Terminal. Functional in PowerShell/CMD (degraded styling acceptable).
- **Python version:** 3.11+ (same as project)

## 5. Files Created / Modified

| File | Action | Description |
|------|--------|-------------|
| `main_tui.py` | **CREATE** | Main TUI application (Textual App subclass) |
| `main_tui.tcss` | **CREATE** | Textual CSS stylesheet |
| `src/app/llm_suggester.py` | **CREATE** | LLM-powered Suggester for autocomplete |
| `src/config/settings.py` | **CREATE** | Persistent settings manager |
| `src/config/llm.py` | **MODIFY** | Add openai_custom provider support |
| `src/config/__init__.py` | **MODIFY** | Export AppSettings |
| `pyproject.toml` | **MODIFY** | Add textual dependency, add tui script entry |
| `Makefile` | **MODIFY** | Add `tui` target: `python main_tui.py` |
| `.env.example` | **MODIFY** | Add OPENAI_API_KEY, OPENAI_BASE_URL, OPENAI_MODEL vars |

## 6. Acceptance Criteria

- [ ] `python main_tui.py` launches the TUI in Windows Terminal with all widgets visible
- [ ] Typing in prompt input shows LLM-powered ghost text suggestion within 1.5s
- [ ] Pressing Tab accepts the suggestion into the input
- [ ] Suggestion carousel auto-rotates every 4 seconds showing 5 different prompts
- [ ] Clicking a carousel suggestion fills the prompt input
- [ ] Clicking "Generate" runs the full LangGraph pipeline
- [ ] Progress panel shows each node's status in real-time with elapsed times
- [ ] Output panel shows track summary DataTable, quality score, and file path
- [ ] "Open Folder" button opens Windows Explorer to the output directory
- [ ] History sidebar shows all generations in the session; clicking one shows its output
- [ ] Settings modal opens on first run if no config.json exists
- [ ] Settings modal saves/loads provider, API keys, custom endpoint, output dir
- [ ] Custom endpoint provider works with any OpenAI-compatible API
- [ ] Pressing Ctrl+Q cleanly exits the application
- [ ] All errors display gracefully in the UI (no crashes to terminal)
