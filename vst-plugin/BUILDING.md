# Building text2midi VST3 Plugin

Developer instructions for building the plugin from source.

## Prerequisites

| Tool | Version | Download |
|------|---------|----------|
| Visual Studio 2022 | 17.x | [visualstudio.microsoft.com](https://visualstudio.microsoft.com/) |
| CMake | 3.22+ | [cmake.org](https://cmake.org/download/) |
| Git | Latest | [git-scm.com](https://git-scm.com/) |
| Python | 3.11+ | [python.org](https://www.python.org/) |
| uv (optional) | Latest | `pip install uv` |

**Visual Studio workloads:** "Desktop development with C++" must be installed.

## Setup

### 1. Clone with submodules

```bash
git clone --recurse-submodules https://github.com/your-repo/spec-kit.git
cd spec-kit/vst-plugin
```

### 2. Add JUCE as submodule (if not already present)

```bash
git submodule add https://github.com/juce-framework/JUCE.git libs/JUCE
git submodule update --init --recursive
```

### 3. Install Python backend dependencies

```bash
cd python-backend
pip install -r requirements.txt
# Or with uv:
uv pip install -r requirements.txt
```

## Building the VST3 Plugin

### Configure CMake

```bash
cd vst-plugin
cmake -B build -G "Visual Studio 17 2022" -A x64
```

### Build (Debug)

```bash
cmake --build build --config Debug
```

### Build (Release)

```bash
cmake --build build --config Release
```

The built `.vst3` bundle will be at:
```
build/text2midi_artefacts/Release/VST3/text2midi.vst3/
```

If `COPY_PLUGIN_AFTER_BUILD` is `TRUE` in CMakeLists.txt, it will also be copied to:
```
C:\Program Files\Common Files\VST3\text2midi.vst3\
```

## Building the Backend Server Executable

```bash
cd python-backend
python build_backend.py
```

Output: `python-backend/dist/text2midi-backend/text2midi-backend.exe`

### Testing the backend

```bash
# Start the server
python server.py

# In another terminal, test endpoints
curl http://127.0.0.1:18323/health
curl -X POST http://127.0.0.1:18323/configure \
  -H "Content-Type: application/json" \
  -d '{"provider":"groq","api_key":"your-key"}'
```

## Building the Installer

### Prerequisites

- [Inno Setup 6](https://jrsoftware.org/isdl.php) installed
- VST3 plugin built (Release)
- Backend server built (PyInstaller)

### Build

```bash
cd installer/windows
iscc text2midi_setup.iss
```

Output: `installer/windows/Output/text2midi_setup.exe`

## Running Tests

### Backend server tests

```bash
cd python-backend
pytest test_server.py -v
```

### Full project test suite

```bash
# From project root
pytest tests/ -v
```

## Development Workflow

1. **Backend changes:** Edit `python-backend/server.py` → restart `python server.py`
2. **C++ changes:** Edit source files → `cmake --build build --config Debug`
3. **Test in DAW:** Rescan plugins → load text2midi on instrument track
4. **Quick iteration:** Keep the backend server running separately from the plugin

### Debugging the plugin in Visual Studio

1. Open `build/text2midi.sln` in Visual Studio
2. Set the startup project to `text2midi_VST3`
3. In project properties → Debugging:
   - Command: path to your DAW executable
   - Working Directory: `$(ProjectDir)`
4. Set breakpoints and F5 to debug

### Debugging the backend

```bash
cd python-backend
python -m uvicorn server:app --host 127.0.0.1 --port 18323 --reload --log-level debug
```

## Project Structure

```
vst-plugin/
├── CMakeLists.txt          # JUCE CMake build configuration
├── .gitignore              # Build artifacts, IDE files
├── README.md               # User-facing docs
├── BUILDING.md             # This file
│
├── libs/JUCE/              # JUCE framework (git submodule)
│
├── source/                 # C++ source files
│   ├── PluginConfig.h      # Constants (port, colours, sizes)
│   ├── PluginProcessor.*   # Audio processor (silence, state)
│   ├── PluginEditor.*      # Main UI container
│   ├── ApiKeyPanel.*       # API key configuration
│   ├── PromptPanel.*       # Prompt input + generate
│   ├── ProgressPanel.*     # Generation progress
│   ├── OutputPanel.*       # Results + track list
│   ├── DraggableMidiFile.* # Drag-and-drop MIDI element
│   ├── HttpClient.*        # HTTP communication
│   └── BackendLauncher.*   # Auto-launch backend
│
├── python-backend/         # Python FastAPI server
│   ├── server.py           # Main server
│   ├── requirements.txt    # Dependencies
│   ├── build_backend.py    # PyInstaller build script
│   └── test_server.py      # Server tests
│
├── installer/windows/      # Inno Setup installer
│   └── text2midi_setup.iss
│
└── assets/                 # Images (placeholder)
```

## Troubleshooting Build Issues

### CMake can't find JUCE

Make sure the JUCE submodule is initialized:
```bash
git submodule update --init --recursive
```

### Missing Visual Studio components

Install the "Desktop development with C++" workload via Visual Studio Installer.

### PyInstaller missing hidden imports

If the bundled .exe fails to start, check the error log and add missing modules to `build_backend.py`'s `hidden_imports` list.

### Plugin doesn't appear in DAW

1. Check that the `.vst3` is in `C:\Program Files\Common Files\VST3\`
2. Rescan plugins in your DAW
3. Look for "text2midi" under Instruments (not Effects)
