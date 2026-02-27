# TASKS-002: VST3 Plugin — Atomic Task Checklist

**Plan:** PLAN-002-VST3-PLUGIN  
**Spec:** SPEC-002-VST3-PLUGIN  
**Status:** ✅ **COMPLETE** (33/33 tasks, 12/12 backend tests passing, 0 C++ warnings)  
**Completed:** February 26, 2026  

Each task is atomic — completable in one coding session (15–90 min). Tasks are ordered by dependency.

---

## Phase 1: Python Backend Server

- [x] **T-002.01** — Create `vst-plugin/` directory with `python-backend/` subdirectory. Create `vst-plugin/python-backend/requirements.txt` with `fastapi>=0.100.0`, `uvicorn[standard]>=0.25.0`, and all deps from root `requirements.txt`.
- [x] **T-002.02** — Create `vst-plugin/python-backend/server.py` with FastAPI app scaffold: `app = FastAPI()`, uvicorn entrypoint on `127.0.0.1:18323`, CORS middleware (allow all).
- [x] **T-002.03** — Implement `GET /health` endpoint: returns `{status, version, provider, available_providers}`. Import `LLMConfig` to detect current provider.
- [x] **T-002.04** — Implement `POST /configure` endpoint: accepts `{provider, api_key, endpoint?, model?}`, stores via `AppSettings`, calls `apply_to_environment()` + `LLMConfig.initialize()`, returns `{status: "configured"}`.
- [x] **T-002.05** — Implement `POST /generate` endpoint: accepts `{prompt, session_id}`, constructs `MusicState` initial dict (match `main.py:run_generation_workflow` exactly), calls `get_agentic_graph().invoke()`, extracts results, returns full JSON response with `{midi_path, tracks[], quality_score, genre, tempo, bars, summary}`.
- [x] **T-002.06** — Implement `GET /generate/stream` SSE endpoint: uses `graph.stream()` with `stream_mode="values"`, yields per-node progress events as `text/event-stream`, tracks visited nodes by comparing state diffs.
- [x] **T-002.07** — Add generation result caching: store results in-memory dict keyed by `session_id`, background task cleans up after 5 minutes. Add error handling: all exceptions → HTTP 500 with `{error: str}`.
- [x] **T-002.08** — Manual testing: run server with `uv run python server.py`, test all 4 endpoints with curl, verify MIDI file is created in `outputs/` directory.
- [x] **T-002.09** — Create `vst-plugin/python-backend/test_server.py`: unit tests with `httpx.AsyncClient` + FastAPI `TestClient`. Test `/health` (200), `/configure` (stores settings), `/generate` (mocked graph), SSE stream events.

## Phase 2: PyInstaller Bundle

- [x] **T-002.10** — Create `vst-plugin/python-backend/build_exe.py` with all hidden imports (see SPEC-002 §4.11 for complete list). Configure `--onefile`, `--name=text2midi-server`, `--collect-all` for langgraph/langchain.
- [x] **T-002.11** — Run `python build_exe.py`, test `dist/text2midi-server.exe` starts and responds to `GET /health`. Document any missing hidden imports and fix.
- [x] **T-002.12** — Test full generation from bundled .exe: `POST /generate` → verify MIDI output. Note bundle size. Document troubleshooting for any issues.

## Phase 3: JUCE Project Setup

- [x] **T-002.13** — Create `vst-plugin/CMakeLists.txt` as specified in SPEC-002 §4.13. Create `vst-plugin/.gitignore` for build/, libs/JUCE/, *.vst3, *.exe, .vs/.
- [x] **T-002.14** — Add JUCE as git submodule: `git submodule add https://github.com/juce-framework/JUCE.git vst-plugin/libs/JUCE`.
- [x] **T-002.15** — Create all source file stubs in `vst-plugin/source/`: `PluginProcessor.cpp/.h`, `PluginEditor.cpp/.h`, `ApiKeyPanel.cpp/.h`, `PromptPanel.cpp/.h`, `OutputPanel.cpp/.h`, `DraggableMidiFile.cpp/.h`, `HttpClient.cpp/.h`, `ProgressPanel.cpp/.h`, `BackendLauncher.cpp/.h`, `PluginConfig.h`. Minimal class declarations only.
- [x] **T-002.16** — Verify CMake builds: `cmake -B build -G "Visual Studio 17 2022"` then `cmake --build build`. Fix any build errors. Confirm `.vst3` output is created.

## Phase 4: JUCE Core Components

- [x] **T-002.17** — Implement `PluginConfig.h`: all constants (port 18323, host, timeouts, plugin dimensions 550x650).
- [x] **T-002.18** — Implement `PluginProcessor`: `processBlock()` clears audio, `isSynth()=true`, `acceptsMidi()=true`, `getStateInformation()`/`setStateInformation()` with ValueTree (api_key, provider, endpoint, model, last_midi_path). Bus layout: stereo output.
- [x] **T-002.19** — Implement `HttpClient`: static methods using `juce::URL` + `InputStreamOptions`. `checkHealth()` (2s timeout), `generate()` (60s timeout), `configure()` (5s timeout). All on background threads via `juce::Thread::launch()`. JSON parse/create via `juce::JSON`.
- [x] **T-002.20** — Implement `BackendLauncher`: search for `text2midi-server.exe` in 3 locations (next to VST3, Program Files, PATH), launch via `juce::ChildProcess`, poll `/health` every 500ms for 10s. Return status enum.
- [x] **T-002.21** — Build and test core components: verify plugin loads in DAW (shows blank editor), health check detects running/not-running backend, backend auto-launches from known path.

## Phase 5: JUCE UI Components

- [x] **T-002.22** — Implement `PluginEditor`: inherits `DragAndDropContainer`, 550x650 size, dark theme (Catppuccin Mocha `0xFF1E1E2E`), vertical layout with all panels, health check timer `startTimerHz(0.2)`, connection status indicator (green/red dot), `BackendLauncher::launchIfNeeded()` on construction.
- [x] **T-002.23** — Implement `ApiKeyPanel`: `ComboBox` (4 providers), `TextEditor` password mode, conditional endpoint/model fields, "Save & Connect" button. On save → `HttpClient::configure()` on background thread → collapse panel.
- [x] **T-002.24** — Implement `PromptPanel`: multiline `TextEditor` (3 lines, placeholder), "🎵 Generate" button (blue accent `0xFF89B4FA`). Button disabled when empty/generating/offline. On click → `HttpClient::generate()` on background thread.
- [x] **T-002.25** — Implement `ProgressPanel`: `Label` with "Step N/8: NodeName..." text. Updated from generate response or SSE poll. Show "✓ Complete — Quality: X.XX/1.0" after generation.
- [x] **T-002.26** — Implement `OutputPanel`: track summary `Label`, `ListBox` with `ListBoxModel` (channel, instrument, note count per row), mounts `DraggableMidiFile` component, "Change API Key" text button.
- [x] **T-002.27** — Implement `DraggableMidiFile`: 200x60 rounded rectangle with gradient (`0xFF45475A` → `0xFF585B70`), MIDI icon + filename + duration text. `mouseDrag()` → `performExternalDragDropOfFiles({midiFilePath}, true)`. Semi-transparent during drag. Tooltip text.
- [x] **T-002.28** — End-to-end DAW test: load plugin in Ableton Live → enter API key → type prompt → generate → see progress → drag MIDI file to arrangement → verify multi-track creation.

## Phase 6: Build & Packaging

- [x] **T-002.29** — Create `vst-plugin/installer/windows/text2midi_setup.iss` Inno Setup script: install VST3 to `{commoncf}\VST3\`, server to `{pf}\text2midi\`, Start Menu shortcuts, optional startup registration, uninstaller, MIT license page.
- [x] **T-002.30** — Build release package: CMake Release build → `.vst3`, PyInstaller → `.exe`, Inno Setup → `text2midi_setup.exe`. Test full install/uninstall cycle on clean Windows.

## Phase 7: Documentation

- [x] **T-002.31** — Create `vst-plugin/README.md`: features, system requirements, installation guide (with screenshots placeholder), first-time setup, usage workflow, troubleshooting (server offline, SmartScreen, firewall), supported DAWs, known limitations.
- [x] **T-002.32** — Create `vst-plugin/BUILDING.md`: prerequisites (VS2022, CMake, JUCE, Python), git submodule setup, CMake build commands, PyInstaller build, Inno Setup build, dev workflow tips.
- [x] **T-002.33** — Create `vst-plugin/assets/` directory with placeholder `logo.png` note and `screenshot.png` note (text files describing what images are needed).

---

## Summary

| Phase | Tasks | Est. Time |
|-------|-------|-----------|
| 1. Python Backend | T-002.01 – T-002.09 | 6 hours | ✅ Complete |
| 2. PyInstaller | T-002.10 – T-002.12 | 3 hours | ✅ Complete |
| 3. JUCE Setup | T-002.13 – T-002.16 | 3 hours | ✅ Complete |
| 4. Core Components | T-002.17 – T-002.21 | 6 hours | ✅ Complete |
| 5. UI Components | T-002.22 – T-002.28 | 8 hours | ✅ Complete |
| 6. Build & Packaging | T-002.29 – T-002.30 | 4 hours | ✅ Complete |
| 7. Documentation | T-002.31 – T-002.33 | 3 hours | ✅ Complete |
| **Total** | **33 tasks** | **~33 hours** | **✅ All Complete** |

---

## Parallel Tracks

These task groups can be developed simultaneously:

**Track A (Python):** T-002.01 → T-002.09 → T-002.10 → T-002.12  
**Track B (C++/JUCE):** T-002.13 → T-002.16 → T-002.17 → T-002.21 → T-002.22 → T-002.28  

Track A and Track B converge at T-002.28 (end-to-end DAW test) and T-002.29 (installer).
