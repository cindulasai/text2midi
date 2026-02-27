# PLAN-002: VST3 Plugin Implementation Plan

**Spec:** SPEC-002-VST3-PLUGIN  
**Estimated Effort:** 5–7 days  
**Prerequisites:** Visual Studio 2022, CMake 3.22+, Python 3.11+, JUCE framework  

---

## Phase 1: Python Backend Server (Day 1)

### Step 1: Create Backend Directory Structure
```
vst-plugin/
├── python-backend/
│   ├── server.py
│   ├── requirements.txt
│   └── __init__.py
└── README.md (placeholder)
```

### Step 2: Implement FastAPI Server
`vst-plugin/python-backend/server.py`:
- Import and reuse `src/agents/graph.py:get_agentic_graph()` directly
- Import `src/config/llm.py:LLMConfig`
- Import `src/config/settings.py:AppSettings` (created in TUI plan)
- Implement 4 endpoints:
  1. `GET /health` — returns status, version, current provider
  2. `POST /configure` — sets provider + API key via AppSettings
  3. `POST /generate` — runs full pipeline, returns JSON result
  4. `GET /generate/stream` — SSE endpoint with per-node progress
- CORS middleware: allow `*` origins (localhost only, but JUCE doesn't send Origin)
- Error handling: all exceptions → 500 with `{error: str}` body

### Step 3: Implement SSE Streaming
In `server.py`:
- Use `graph.stream(initial_state, config, stream_mode="values")` 
- Track which nodes have been visited by comparing state keys before/after each yield
- Yield SSE events: `data: {"node": "intent_parser", "step": 1, "total": 8, "status": "completed"}\n\n`
- Store generation results in an in-memory dict keyed by `session_id`
- Clean up results after 5 minutes (background task)

### Step 4: Test Backend Server Manually
- Run: `cd vst-plugin/python-backend && uv run python server.py`
- Test with curl:
  ```bash
  curl http://127.0.0.1:18323/health
  curl -X POST http://127.0.0.1:18323/configure -H "Content-Type: application/json" -d '{"provider":"minimax","api_key":"sk-xxx"}'
  curl -X POST http://127.0.0.1:18323/generate -H "Content-Type: application/json" -d '{"prompt":"dreamy jazz","session_id":"test1"}'
  ```
- Verify MIDI file is generated and path is correct

### Step 5: Write Backend Unit Tests
`vst-plugin/python-backend/test_server.py`:
- Use `httpx.AsyncClient` with FastAPI's `TestClient`
- Test `/health` returns 200
- Test `/configure` stores settings
- Test `/generate` with mocked graph (patch `get_agentic_graph`)
- Test SSE stream yields correct events

---

## Phase 2: PyInstaller Bundle (Day 2 — Morning)

### Step 6: Create PyInstaller Spec
`vst-plugin/python-backend/build_exe.py`:
- Configure all hidden imports (see SPEC-002 §4.11 for complete list)
- Set `--onefile` for single `.exe`
- Output to `vst-plugin/python-backend/dist/text2midi-server.exe`

### Step 7: Build and Test .exe
- Run: `cd vst-plugin/python-backend && python build_exe.py`
- Test: `dist/text2midi-server.exe` starts and responds to `/health`
- Verify MIDI generation works from the bundled .exe
- Document any hidden import issues or missing modules
- Expected bundle size: ~120-180MB

### Step 8: Create requirements.txt for Backend
`vst-plugin/python-backend/requirements.txt`:
```
fastapi>=0.100.0
uvicorn[standard]>=0.25.0
# Plus all deps from project root requirements.txt that the backend needs
```

---

## Phase 3: JUCE Project Setup (Day 2 — Afternoon)

### Step 9: Initialize JUCE Submodule
```bash
cd vst-plugin
git submodule add https://github.com/juce-framework/JUCE.git libs/JUCE
git submodule update --init --recursive
```

### Step 10: Create CMakeLists.txt
As specified in SPEC-002 §4.13:
- `juce_add_plugin()` with VST3 format, IS_SYNTH=TRUE
- All source files listed in `target_sources()`
- Link `juce_audio_utils`, `juce_gui_extra`
- Set `COPY_PLUGIN_AFTER_BUILD=TRUE` for development

### Step 11: Create Source File Stubs
Create all `.cpp` and `.h` files with minimal class declarations:
- `PluginProcessor.cpp/.h` — inherits `juce::AudioProcessor`, returns silence
- `PluginEditor.cpp/.h` — inherits `juce::AudioProcessorEditor` + `juce::DragAndDropContainer`
- All panel files — inherit `juce::Component`
- Verify CMake builds: `cmake -B build -G "Visual Studio 17 2022" && cmake --build build`

### Step 12: Create .gitignore
```
build/
libs/JUCE/
*.vst3
*.exe
.vs/
CMakeSettings.json
```

---

## Phase 4: JUCE Core Components (Day 3)

### Step 13: Implement PluginProcessor
`source/PluginProcessor.cpp`:
- `processBlock()`: clear all audio buffers
- `getStateInformation()`: serialize ValueTree with api_key, provider, endpoint, model, last_midi_path
- `setStateInformation()`: deserialize ValueTree
- `createEditor()`: return new `Text2MidiEditor(*this)`
- Plugin name: "text2midi", manufacturer: "text2midi"
- Bus layout: stereo output only

### Step 14: Implement HttpClient
`source/HttpClient.cpp`:
- Static methods using `juce::URL` + `juce::URL::InputStreamOptions`
- All calls on background threads using `juce::Thread::launch()`
- `checkHealth()`: GET /health, 2s timeout
- `generate()`: POST /generate, 60s timeout
- `configure()`: POST /configure, 5s timeout
- JSON parsing via `juce::JSON::parse()`
- JSON creation via `juce::DynamicObject` + `juce::JSON::toString()`

### Step 15: Implement BackendLauncher
`source/BackendLauncher.cpp`:
- Search paths for `text2midi-server.exe` (see SPEC-002 §4.8)
- Launch via `juce::ChildProcess::start()`
- Poll `/health` with 500ms interval, 10s total timeout
- Return enum status: `{ServerAlreadyRunning, ServerLaunched, ServerNotFound, ServerFailedToStart}`

### Step 16: Implement PluginConfig.h
```cpp
namespace PluginConfig {
    constexpr int SERVER_PORT = 18323;
    constexpr const char* SERVER_HOST = "127.0.0.1";
    constexpr int HEALTH_CHECK_INTERVAL_MS = 5000;
    constexpr int GENERATION_TIMEOUT_MS = 60000;
    constexpr int LAUNCH_TIMEOUT_MS = 10000;
    constexpr int PLUGIN_WIDTH = 550;
    constexpr int PLUGIN_HEIGHT = 650;
}
```

---

## Phase 5: JUCE UI Components (Day 4)

### Step 17: Implement PluginEditor Layout
`source/PluginEditor.cpp`:
- Inherits `DragAndDropContainer` for external file drag
- Size: 550x650, not resizable
- Dark theme using Catppuccin Mocha colors
- Vertical layout: logo bar → connection status → ApiKeyPanel → PromptPanel → ProgressPanel → OutputPanel
- Health check timer: `startTimerHz(0.2)` polling `/health`
- On construction: call `BackendLauncher::launchIfNeeded()`

### Step 18: Implement ApiKeyPanel
`source/ApiKeyPanel.cpp`:
- `juce::ComboBox` for provider selection (4 items)
- `juce::TextEditor` for API key (password mode)
- `juce::TextEditor` for custom endpoint + model (conditional visibility)
- `juce::TextButton` "Save & Connect"
- On save: call `HttpClient::configure()` on background thread → on success: hide panel
- Panel visible only when API key not set or user requests change

### Step 19: Implement PromptPanel
`source/PromptPanel.cpp`:
- `juce::TextEditor` — multiline (3 lines), placeholder text
- `juce::TextButton` "🎵 Generate" — blue accent color
- Button states: enabled (ready), disabled (generating/offline), error (last gen failed)
- On click: start background thread → `HttpClient::generate()` → post result to message thread

### Step 20: Implement ProgressPanel
`source/ProgressPanel.cpp`:
- `juce::Label` for status text: "Step 3/8: Theory Validator..."
- Simple step counter (no JUCE progress bar needed — just text updates)
- Poll SSE endpoint OR use timer to check generation status
- After complete: show quality score

### Step 21: Implement OutputPanel + DraggableMidiFile
`source/OutputPanel.cpp`:
- Track summary: `juce::Label` — "5 tracks | jazz | 64 bars"
- Track list: `juce::ListBox` with `ListBoxModel` — shows channel, instrument, note count
- Mounts `DraggableMidiFile` component at bottom

`source/DraggableMidiFile.cpp`:
- 200x60px rounded rectangle with gradient
- MIDI icon + filename text + duration text
- `mouseDrag()` → `performExternalDragDropOfFiles({midiFilePath}, true)`
- Visual feedback: semi-transparent during active drag
- Tooltip instruction text

### Step 22: Build and Test in DAW
- Build VST3: `cmake --build build --config Release`
- Copy to `C:\Program Files\Common Files\VST3\`
- Open Ableton Live → Add instrument track → Load "text2midi"
- Verify: UI renders, health check works, generate button triggers backend
- Verify: drag MIDI file from plugin to arrangement → tracks created

---

## Phase 6: Build & Packaging (Day 5–6)

### Step 23: Create build_exe.py
Implement PyInstaller build script as specified in SPEC-002 §4.11:
- All hidden imports for LangGraph, LangChain, and project modules
- `--collect-all` for problematic packages
- `--onefile` mode
- Test: built `.exe` runs independently

### Step 24: Create Inno Setup Installer Script
`vst-plugin/installer/windows/text2midi_setup.iss`:
- Input files: `text2midi.vst3` bundle + `text2midi-server.exe`
- Install locations: 
  - VST3: `{commoncf}\VST3\text2midi.vst3\`
  - Server: `{pf}\text2midi\text2midi-server.exe`
- Start menu shortcuts
- Optional startup registration
- Uninstaller
- License page (MIT)

### Step 25: Test Complete Installation Flow
1. Build `.vst3` with CMake Release
2. Build `text2midi-server.exe` with PyInstaller
3. Build installer with Inno Setup
4. Fresh Windows: run installer → open Ableton → load plugin → generate → drag MIDI
5. Test uninstall: both `.vst3` and `.exe` removed cleanly

---

## Phase 7: Documentation & Polish (Day 6–7)

### Step 26: Write vst-plugin/README.md
Sections:
- Features overview with screenshot
- System requirements (Windows 10+, DAW with VST3 support)
- Installation: download installer → run → open DAW → load plugin
- First-time setup: enter API key → select provider
- Usage: type prompt → click generate → drag MIDI → profit
- Troubleshooting: "Server offline", firewall, SmartScreen
- Supported DAWs: Ableton Live 10+, FL Studio 20+, Bitwig Studio 4+, Reaper 6+
- Known limitations: Windows only, no macOS, 150MB backend size, 5-30s generation time

### Step 27: Write vst-plugin/BUILDING.md
Sections:
- Prerequisites: Visual Studio 2022, CMake 3.22+, JUCE (submodule), Python 3.11+
- Clone and setup: `git submodule update --init`
- Build VST3: CMake commands
- Build Python backend: `uv pip install` + PyInstaller
- Build installer: Inno Setup CLI
- Development workflow: CMake auto-copy to VST3 dir

### Step 28: Test with Multiple DAWs (if available)
- Ableton Live Lite (primary target)
- FL Studio trial
- Reaper (free trial)
- Document any DAW-specific quirks

### Step 29: Code Signing Research
- Document Windows code signing process (self-signed vs. purchased cert)
- Add instructions to BUILDING.md for production builds
- Note: not required for v1 but important for user trust

---

## Dependency Chain

```
Phase 1 (Python Backend) ── ── ── ── ── ── ── ── ── ─┐
  └── Phase 2 (PyInstaller Bundle)                     │
        └── Phase 6 (Build & Packaging)                │
                                                       │
Phase 3 (JUCE Setup) ── ── ── ── ── ── ── ── ── ── ─┤
  └── Phase 4 (Core Components)                        │
        └── Phase 5 (UI Components)                    │
              └── Phase 6 (Build & Packaging)          │
                    └── Phase 7 (Documentation)  ◄── ─ ┘
```

Phases 1-2 (Python) and Phases 3-5 (JUCE C++) can be developed in parallel by different developers.

---

## Critical Path

The longest dependency chain is:
`Phase 3 → Phase 4 → Phase 5 → Phase 6 → Phase 7`

This is 5 phases (~5 days). To minimize calendar time:
- Develop Python backend (Phase 1-2) while setting up JUCE (Phase 3)
- Start testing integration as soon as Phase 4 core components are done
- Documentation (Phase 7) can start as early as Phase 5
