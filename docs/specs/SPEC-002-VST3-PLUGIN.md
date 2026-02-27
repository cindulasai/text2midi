# SPEC-002: VST3 Plugin for DAW Integration (`vst-plugin/`)

**Status:** Draft  
**Created:** 2026-02-26  
**Author:** spec-kit  
**Priority:** P1 — DAW Integration  

---

## 1. Overview

Create a JUCE-based VST3 instrument plugin that lives in a completely isolated `vst-plugin/` directory at the project root. The plugin provides a minimal GUI inside the DAW: one-time API key configuration, a text prompt input, a generate button, and a **draggable MIDI file element** that the user can drag-and-drop from the plugin's UI panel directly onto the DAW's arrangement view. When a Type 1 (multi-track) MIDI file is dropped into Ableton Live, it automatically creates one track per MIDI channel — achieving the multi-track population goal without violating VST3's single-track sandbox constraint.

The plugin communicates with a Python backend server (bundled as a standalone `.exe` via PyInstaller) over HTTP localhost.

## 2. Architecture

```
┌──────────────────────────┐     HTTP (127.0.0.1:18323)     ┌─────────────────────────┐
│  JUCE VST3 Plugin        │ ◄──────────────────────────────► │  Python Backend (.exe)  │
│  (inside DAW)            │                                  │  (standalone process)   │
│                          │  POST /generate                  │                         │
│  ┌────────────────────┐  │  ──────────────────►             │  FastAPI server         │
│  │ API Key Panel      │  │                                  │  ├── src/agents/graph   │
│  │ Prompt Input       │  │  ◄──────────────────             │  ├── src/config/llm     │
│  │ Generate Button    │  │  SSE: node progress              │  ├── src/app/*          │
│  │ Progress Status    │  │                                  │  └── src/midigent/*     │
│  │ ┌────────────────┐ │  │  ◄──────────────────             │                         │
│  │ │ Draggable MIDI │ │  │  JSON: {midi_path, tracks,      │  Writes .mid to temp dir│
│  │ │ File Element   │ │  │         quality, summary}        │                         │
│  │ └──────┬─────────┘ │  │                                  └─────────────────────────┘
│  └────────┼───────────┘  │
│           │ drag         │
└───────────┼──────────────┘
            │
            ▼  (OS-native file drag)
┌──────────────────────────────────────────────────────────────────────┐
│  DAW (Ableton Live, FL Studio, Bitwig, etc.)                        │
│  ─────────────────────────────────────────────                       │
│  Drops Type 1 MIDI → auto-creates tracks per channel                │
│  Track 1: Lead (Ch 1)    │  Track 2: Bass (Ch 2)  │  Track 3: ...  │
└──────────────────────────────────────────────────────────────────────┘
```

## 3. Reliability Assessment (Honest)

### 3.1 What Works Reliably
| Aspect | Confidence | Notes |
|--------|------------|-------|
| JUCE VST3 builds on Windows | HIGH | JUCE is industry standard; extensive documentation |
| Plugin loads in Ableton Live 10+ | HIGH | VST3 instrument category is universally supported |
| HTTP localhost communication | HIGH | `127.0.0.1` loopback bypasses most firewalls |
| JUCE `performExternalDragDropOfFiles()` | HIGH | Native OS drag-and-drop; well-tested JUCE API |
| Ableton auto-splits Type 1 MIDI on drop | HIGH | Native Ableton behavior since Live 9 |
| PyInstaller .exe bundling | MEDIUM-HIGH | Works for straightforward projects; occasional hidden import issues |

### 3.2 Known Risks
| Risk | Severity | Likelihood | Mitigation |
|------|----------|------------|------------|
| Python backend not running when plugin loads | HIGH | HIGH | Plugin auto-launches .exe via `juce::ChildProcess`; clear "Server offline" indicator; health check polling |
| Windows SmartScreen blocks unsigned .exe | MEDIUM | MEDIUM | Document "More info → Run anyway"; plan code signing for production |
| PyInstaller bundle size (~150MB) | LOW | CERTAIN | Acceptable for music production tool; can optimize with UPX |
| First-time firewall prompt for HTTP | LOW | MEDIUM | Use `127.0.0.1` (often exempt); document if prompted |
| Ableton Lite 8-track limit | LOW | N/A | Generator already caps at 8 tracks |
| macOS requires notarization | HIGH | CERTAIN (on macOS) | Windows-only for v1; macOS planned for v2 |
| Generation takes 5-30 seconds | MEDIUM | CERTAIN | Progress indicator via SSE; clear "Generating..." status |

### 3.3 Target Audience Compatibility
| User Type | % of Producers | Expected Experience |
|-----------|---------------|-------------------|
| Developer-musicians | 10-15% | Smooth — understands the setup |
| Tech-savvy producers | 20-25% | Fine with installer + one-time setup |
| Average Ableton users | 40-50% | Needs clear installer + docs; may need support |
| Casual/beginner producers | 15-25% | May struggle with SmartScreen / backend concept |

**Mitigation for non-technical users:** One-click installer that handles everything. Plugin auto-launches backend. User never sees a terminal.

## 4. Functional Requirements

### 4.1 Directory Structure

```
vst-plugin/
├── README.md                         # User-facing installation & usage guide
├── BUILDING.md                       # Developer build instructions
├── CMakeLists.txt                    # Top-level CMake build file
├── .gitignore                        # Build artifacts, IDE files
│
├── libs/
│   └── JUCE/                         # JUCE framework (git submodule)
│
├── source/
│   ├── PluginProcessor.cpp           # Audio processor (silence pass-through)
│   ├── PluginProcessor.h
│   ├── PluginEditor.cpp              # Main plugin UI
│   ├── PluginEditor.h
│   ├── ApiKeyPanel.cpp               # API key setup UI component
│   ├── ApiKeyPanel.h
│   ├── PromptPanel.cpp               # Prompt input + generate button
│   ├── PromptPanel.h
│   ├── OutputPanel.cpp               # Generation results + draggable MIDI
│   ├── OutputPanel.h
│   ├── DraggableMidiFile.cpp         # Drag-and-drop MIDI file component
│   ├── DraggableMidiFile.h
│   ├── HttpClient.cpp                # HTTP client for backend communication
│   ├── HttpClient.h
│   ├── ProgressPanel.cpp             # Generation progress display
│   ├── ProgressPanel.h
│   ├── BackendLauncher.cpp           # Python backend auto-launch logic
│   ├── BackendLauncher.h
│   └── PluginConfig.h                # Constants (port, paths, version)
│
├── python-backend/
│   ├── server.py                     # FastAPI server wrapping existing pipeline
│   ├── requirements.txt              # Pinned deps for backend
│   ├── build_exe.py                  # PyInstaller build script
│   └── text2midi_server.spec         # PyInstaller spec file
│
├── installer/
│   └── windows/
│       ├── text2midi_setup.iss       # Inno Setup script
│       └── icon.ico                  # Installer icon
│
└── assets/
    ├── logo.png                      # Plugin GUI logo (128x128)
    └── screenshot.png                # README screenshot
```

### 4.2 Plugin Processor (`PluginProcessor.cpp/.h`)

```cpp
class Text2MidiProcessor : public juce::AudioProcessor
```

- **Plugin name:** `"text2midi"`
- **Plugin category:** Instrument (`createPluginFilter()` returns `Text2MidiProcessor`)
  - `isMidiEffect()` returns `false`
  - `acceptsMidi()` returns `true` (so DAW puts it on an instrument track)
  - `producesMidi()` returns `false`
  - `isSynth()` returns `true`
- **`processBlock()`:** Clears audio buffer (outputs silence). Does NOT process MIDI events. This plugin is a UI-only tool.
- **`getStateInformation()` / `setStateInformation()`:** Serialize/deserialize with `juce::ValueTree`:
  - `api_key` (string, encrypted with simple XOR + base64 for minimal obfuscation)
  - `provider` (string: "minimax", "groq", "openai_custom", "custom")
  - `custom_endpoint` (string)
  - `custom_model` (string)
  - `last_midi_path` (string)
- **BusesProperties:** `BusesProperties().withOutput("Output", juce::AudioChannelSet::stereo(), true)` — stereo output required for instrument category

### 4.3 Plugin Editor (`PluginEditor.cpp/.h`)

```cpp
class Text2MidiEditor : public juce::AudioProcessorEditor,
                         public juce::DragAndDropContainer
```

- **Size:** 550 x 650 pixels, resizable: false
- **Inherits `DragAndDropContainer`** — required for `performExternalDragDropOfFiles()`
- **Layout (top to bottom):**
  1. Logo + title bar (40px height)
  2. Connection status indicator (20px)
  3. ApiKeyPanel (120px, collapsible — hidden after first save)
  4. PromptPanel (100px)
  5. ProgressPanel (80px)
  6. OutputPanel with DraggableMidiFile (200px)
- **Background:** Dark theme (`Colour(0xFF1E1E2E)` — Catppuccin Mocha base)
- **Font:** `juce::Font("Segoe UI", 14.0f, juce::Font::plain)` (Windows system font)
- **Health check timer:** `startTimerHz(0.2)` — polls `GET http://127.0.0.1:18323/health` every 5 seconds. Updates connection indicator.
- **Backend auto-launch:** On construction, if health check fails, attempt to launch `text2midi-server.exe` via `BackendLauncher::launchIfNeeded()`

### 4.4 API Key Panel (`ApiKeyPanel.cpp/.h`)

- **Shown:** On first load when no API key is stored in plugin state, OR when user clicks "Change API Key" in output panel
- **Hidden:** After successful save + health check confirms connectivity
- **Components:**
  - `juce::ComboBox` for provider selection: items `{"MiniMax M2.5", "Groq (Llama)", "OpenAI-compatible", "Custom Endpoint"}`
  - `juce::TextEditor` for API key (password character: `•`, single line)
  - `juce::TextEditor` for custom endpoint URL (visible only when provider = "Custom Endpoint")
  - `juce::TextEditor` for custom model name (visible only when provider = "Custom Endpoint")
  - `juce::TextButton` "Save & Connect"
- **On save:**
  1. Store values in processor's `ValueTree` state (persisted with DAW project)
  2. Send `POST /configure` to backend with `{provider, api_key, endpoint?, model?}`
  3. Backend stores the key in `platformdirs` config and applies to `LLMConfig`
  4. On success → collapse ApiKeyPanel, show PromptPanel

### 4.5 Prompt Panel (`PromptPanel.cpp/.h`)

- `juce::TextEditor` — multi-line text input (3 lines visible), with placeholder: "Describe your music..."
- `juce::TextButton` "🎵 Generate" — large, colored (`Colour(0xFF89B4FA)` — blue accent)
- Button disabled when: prompt is empty, generation in progress, or backend offline
- On click: sends `POST /generate` to backend with `{prompt: text, session_id: uuid}`
- During generation: button text changes to "Generating..." and shows a progress indicator

### 4.6 Progress Panel (`ProgressPanel.cpp/.h`)

- Simple status text: shows current agent node name
- Format: `"Step 3/8: Theory Validator..."`
- Updated via SSE stream from `GET /generate/stream?session_id=xxx`
- After completion: shows `"✓ Complete — Quality: 0.87/1.0"`
- On error: shows `"✗ Error: {message}"` in red

### 4.7 Output Panel with Draggable MIDI (`OutputPanel.cpp/.h`, `DraggableMidiFile.cpp/.h`)

#### OutputPanel
- Shown after generation completes
- Contains:
  - Track summary text: `"5 tracks | jazz | 64 bars | 120 BPM"`
  - Track list (scrollable `juce::ListBox`): each row = `"Ch {n}: {instrument} ({note_count} notes)"`
  - DraggableMidiFile component
  - "Change API Key" text button (to re-show ApiKeyPanel)

#### DraggableMidiFile
```cpp
class DraggableMidiFile : public juce::Component
```

- **Size:** 200 x 60 pixels
- **Appearance:** Styled like a MIDI clip — rounded rectangle with gradient background (`Colour(0xFF45475A)` to `Colour(0xFF585B70)`), MIDI icon, filename text, duration text
- **Drag behavior:**
  ```cpp
  void mouseDrag(const juce::MouseEvent& event) override {
      if (midiFilePath.isNotEmpty()) {
          auto* container = juce::DragAndDropContainer::findParentDragContainerFor(this);
          if (container != nullptr && !container->isDragAndDropActive()) {
              juce::StringArray files;
              files.add(midiFilePath);
              container->performExternalDragDropOfFiles(files, true, this, nullptr);
          }
      }
  }
  ```
- **Visual feedback during drag:** Component becomes semi-transparent (alpha 0.5) while drag is active
- **Tooltip:** "Drag this MIDI file to your DAW's arrangement view. Multi-channel MIDI will auto-create separate tracks."
- **File path:** Set by the generate response. Points to the `.mid` file in a temp directory (e.g., `%TEMP%/text2midi/`) or the project's `outputs/` folder.

### 4.8 Backend Launcher (`BackendLauncher.cpp/.h`)

```cpp
class BackendLauncher
```

- **Static method:** `static bool launchIfNeeded()`
- **Logic:**
  1. Try `GET http://127.0.0.1:18323/health` with 2-second timeout
  2. If server responds → return true (already running)
  3. If server not reachable → look for `text2midi-server.exe` in:
     - Same directory as the VST3 bundle: `File::getSpecialLocation(File::currentApplicationFile).getParentDirectory()`
     - `C:\Program Files\text2midi\text2midi-server.exe`
     - PATH environment variable
  4. Launch via `juce::ChildProcess::start(exePath)` with flag `wantStdOut=false`
  5. Wait up to 10 seconds, polling `/health` every 500ms
  6. Return true if server starts, false otherwise
- **Error reporting:** Returns enum `{ServerAlreadyRunning, ServerLaunched, ServerNotFound, ServerFailedToStart}`

### 4.9 HTTP Client (`HttpClient.cpp/.h`)

```cpp
class HttpClient
```

- **Base URL:** `http://127.0.0.1:18323`
- **Methods:**
  - `static bool checkHealth()` — `GET /health`, returns true if 200
  - `static juce::var generate(const juce::String& prompt, const juce::String& sessionId)` — `POST /generate`, returns JSON response as `juce::var`
  - `static bool configure(const juce::String& provider, const juce::String& apiKey, const juce::String& endpoint, const juce::String& model)` — `POST /configure`, returns success bool
- **Implementation:** Use `juce::URL` with `juce::URL::InputStreamOptions`:
  ```cpp
  juce::URL url("http://127.0.0.1:18323/generate");
  url = url.withPOSTData(jsonBody);
  auto stream = url.createInputStream(
      juce::URL::InputStreamOptions(juce::URL::ParameterHandling::inPostBody)
          .withConnectionTimeoutMs(60000)   // 60s for generation
          .withExtraHeaders("Content-Type: application/json")
  );
  ```
- **Threading:** All HTTP calls MUST run on a background thread (never the message thread). Use `juce::Thread` or `juce::ThreadPool`.

### 4.10 Python Backend Server (`vst-plugin/python-backend/server.py`)

**Framework:** FastAPI (add `fastapi>=0.100.0` and `uvicorn>=0.25.0` to backend requirements)

**Endpoints:**

#### `GET /health`
```json
{
  "status": "ok",
  "version": "0.1.0",
  "provider": "minimax",
  "available_providers": ["minimax", "groq"]
}
```

#### `POST /configure`
```json
Request: {
  "provider": "minimax",
  "api_key": "sk-xxx",
  "endpoint": "",
  "model": ""
}
Response: {
  "status": "configured",
  "provider": "minimax"
}
```
- Stores API key in `platformdirs` config (same `AppSettings` from SPEC-001)
- Calls `apply_to_environment()` + `LLMConfig.initialize()`

#### `POST /generate`
```json
Request: {
  "prompt": "dreamy jazz with piano",
  "session_id": "abc12345"
}
Response: {
  "status": "completed",
  "midi_path": "C:/Users/.../outputs/midigen_jazz_abc12345_20260226_143022.mid",
  "tracks": [
    {"name": "lead", "instrument": "piano", "channel": 1, "note_count": 127, "type": "lead"},
    {"name": "bass", "instrument": "bass", "channel": 2, "note_count": 64, "type": "bass"}
  ],
  "quality_score": 0.87,
  "genre": "jazz",
  "tempo": 120,
  "bars": 64,
  "summary": "## Composition Summary\n..."
}
```
- Creates `MusicState` initial dict (same structure as `main.py:run_generation_workflow`)
- Calls `get_agentic_graph().invoke(initial_state, config)`
- Extracts results from final state

#### `GET /generate/stream?session_id=xxx` (SSE — Server-Sent Events)
```
data: {"node": "intent_parser", "status": "started"}
data: {"node": "intent_parser", "status": "completed", "elapsed": 0.8}
data: {"node": "track_planner", "status": "started"}
...
data: {"node": "session_summary", "status": "completed", "elapsed": 0.2}
data: {"status": "done", "midi_path": "...", "quality_score": 0.87}
```
- Uses `graph.stream()` to yield per-node progress
- SSE format: `text/event-stream` with `data:` prefix per line

#### Server startup
```python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=18323, log_level="info")
```

### 4.11 PyInstaller Bundle (`vst-plugin/python-backend/build_exe.py`)

```python
"""Build script for creating standalone text2midi-server.exe"""
import PyInstaller.__main__
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent  # spec-kit root

PyInstaller.__main__.run([
    str(Path(__file__).parent / "server.py"),
    "--onefile",
    "--name=text2midi-server",
    "--paths", str(REPO_ROOT),                    # Add repo root to sys.path
    "--hidden-import=src.agents",
    "--hidden-import=src.agents.graph",
    "--hidden-import=src.agents.state",
    "--hidden-import=src.agents.intent_parser_node",
    "--hidden-import=src.agents.track_planner_node",
    "--hidden-import=src.agents.theory_validator_node",
    "--hidden-import=src.agents.track_generator_node",
    "--hidden-import=src.agents.quality_control_node",
    "--hidden-import=src.agents.refinement_node",
    "--hidden-import=src.agents.midi_creator_node",
    "--hidden-import=src.agents.session_summary_node",
    "--hidden-import=src.app",
    "--hidden-import=src.app.models",
    "--hidden-import=src.app.constants",
    "--hidden-import=src.app.generator",
    "--hidden-import=src.app.midi_creator",
    "--hidden-import=src.app.intent_parser",
    "--hidden-import=src.app.track_planner",
    "--hidden-import=src.config",
    "--hidden-import=src.config.llm",
    "--hidden-import=src.midigent.advanced_generator",
    "--hidden-import=src.midigent.advanced_intent_parser",
    "--hidden-import=src.midigent.creative_variation_engine",
    "--hidden-import=src.midigent.cultural_music",
    "--hidden-import=src.midigent.duration_models",
    "--hidden-import=src.midigent.duration_parser",
    "--hidden-import=src.midigent.duration_validator",
    "--hidden-import=src.midigent.educational_insights",
    "--hidden-import=src.midigent.emotion_engine",
    "--hidden-import=src.midigent.emotion_instruments",
    "--hidden-import=src.midigent.genre_validator",
    "--hidden-import=src.midigent.intelligent_quality_reviewer",
    "--hidden-import=src.midigent.music_theory_engine",
    "--hidden-import=src.midigent.variation_engine",
    "--hidden-import=src.midigent.zero_repetition",
    "--hidden-import=langgraph",
    "--hidden-import=langchain",
    "--hidden-import=langchain_groq",
    "--hidden-import=groq",
    "--hidden-import=openai",
    "--hidden-import=mido",
    "--hidden-import=pydantic",
    "--hidden-import=dotenv",
    "--hidden-import=loguru",
    "--hidden-import=tenacity",
    "--hidden-import=fastapi",
    "--hidden-import=uvicorn",
    "--collect-all=langgraph",
    "--collect-all=langchain",
    "--collect-all=langchain_groq",
    "--noconfirm",
    "--clean",
    f"--distpath={Path(__file__).parent / 'dist'}",
])
```

### 4.12 Windows Installer (`vst-plugin/installer/windows/text2midi_setup.iss`)

Inno Setup script that:
1. Copies `text2midi.vst3` bundle to `C:\Program Files\Common Files\VST3\text2midi.vst3\`
2. Copies `text2midi-server.exe` to `C:\Program Files\text2midi\`
3. Creates Start Menu entries:
   - "text2midi Server" → launches `text2midi-server.exe`
   - "Uninstall text2midi" → uninstaller
4. Optional: adds `text2midi-server.exe` to Windows startup (user-choice checkbox during install)
5. Creates uninstaller that removes both `.vst3` and `.exe`

### 4.13 JUCE CMake Build Configuration

```cmake
cmake_minimum_required(VERSION 3.22)
project(text2midi VERSION 0.1.0)

add_subdirectory(libs/JUCE)

juce_add_plugin(text2midi
    COMPANY_NAME "text2midi"
    PLUGIN_MANUFACTURER_CODE Tx2M
    PLUGIN_CODE Tx2m
    FORMATS VST3
    PRODUCT_NAME "text2midi"
    IS_SYNTH TRUE
    NEEDS_MIDI_INPUT TRUE
    NEEDS_MIDI_OUTPUT FALSE
    IS_MIDI_EFFECT FALSE
    EDITOR_WANTS_KEYBOARD_FOCUS TRUE
    COPY_PLUGIN_AFTER_BUILD TRUE
    VST3_COPY_DIR "C:/Program Files/Common Files/VST3"
)

target_sources(text2midi PRIVATE
    source/PluginProcessor.cpp
    source/PluginEditor.cpp
    source/ApiKeyPanel.cpp
    source/PromptPanel.cpp
    source/OutputPanel.cpp
    source/DraggableMidiFile.cpp
    source/HttpClient.cpp
    source/ProgressPanel.cpp
    source/BackendLauncher.cpp
)

target_compile_definitions(text2midi PUBLIC
    JUCE_WEB_BROWSER=0
    JUCE_USE_CURL=1
    JUCE_VST3_CAN_REPLACE_VST2=0
)

target_link_libraries(text2midi PRIVATE
    juce::juce_audio_utils
    juce::juce_gui_extra
    juce::juce_recommended_config_flags
    juce::juce_recommended_lto_flags
    juce::juce_recommended_warning_flags
)
```

## 5. Files Created

| File | Description |
|------|-------------|
| `vst-plugin/README.md` | Installation & usage guide |
| `vst-plugin/BUILDING.md` | Build instructions |
| `vst-plugin/CMakeLists.txt` | JUCE CMake config |
| `vst-plugin/.gitignore` | Ignore build/, libs/JUCE (submodule) |
| `vst-plugin/source/PluginProcessor.cpp/.h` | Audio processor |
| `vst-plugin/source/PluginEditor.cpp/.h` | Main UI |
| `vst-plugin/source/ApiKeyPanel.cpp/.h` | API key setup |
| `vst-plugin/source/PromptPanel.cpp/.h` | Prompt + generate button |
| `vst-plugin/source/OutputPanel.cpp/.h` | Results display |
| `vst-plugin/source/DraggableMidiFile.cpp/.h` | Drag-and-drop MIDI element |
| `vst-plugin/source/HttpClient.cpp/.h` | HTTP client |
| `vst-plugin/source/ProgressPanel.cpp/.h` | Progress display |
| `vst-plugin/source/BackendLauncher.cpp/.h` | Auto-launch backend |
| `vst-plugin/source/PluginConfig.h` | Constants |
| `vst-plugin/python-backend/server.py` | FastAPI backend |
| `vst-plugin/python-backend/requirements.txt` | Backend deps |
| `vst-plugin/python-backend/build_exe.py` | PyInstaller build |
| `vst-plugin/installer/windows/text2midi_setup.iss` | Inno Setup installer |

## 6. Acceptance Criteria

- [ ] `vst-plugin/` is completely self-contained — no imports from parent project at source level (Python backend imports `src/` at runtime)
- [ ] CMake builds successfully with Visual Studio 2022 + JUCE
- [ ] `.vst3` file loads in Ableton Live 10+ Lite as an instrument
- [ ] API key entered once → persisted in plugin state → never re-asked (survives DAW restart)
- [ ] Custom endpoint works with any OpenAI-compatible API (e.g., Ollama, LM Studio)
- [ ] "Generate" button calls Python backend and shows progress
- [ ] Draggable MIDI element can be dragged from plugin UI to Ableton arrangement
- [ ] Dropping Type 1 MIDI in Ableton creates separate tracks per MIDI channel
- [ ] Backend auto-launches when plugin detects it's offline
- [ ] Plugin shows clear "Server offline" when backend isn't reachable
- [ ] `text2midi-server.exe` builds with PyInstaller and runs standalone
- [ ] Inno Setup installer copies both `.vst3` and `.exe` to correct locations
- [ ] `vst-plugin/README.md` covers installation, usage, troubleshooting, and limitations
