# text2midi - AI-Powered MIDI Composer

**text2midi**: Transform text descriptions into professional multi-track MIDI compositions using AI. Generate music instantly through natural language conversation.

## 🚀 Quick Start

### One-Touch Installer (Easiest)

**First time?** Use the installer for automated setup:

**Windows:**
```bash
# Run installer
installer/install.bat
```

**macOS/Linux:**
```bash
# Run installer
bash installer/install.sh
```

The installer will:
- Detect/install Python 3.11+ automatically
- Install uv and dependencies
- Help you set up a free API key (Groq/Gemini/OpenRouter)
- Create a desktop launcher and shortcuts

📖 [**Full Installer Guide**](installer/README.md)

### Developer Setup (Manual)

```bash
# Install with uv
uv sync

# Run the Terminal UI (with settings: Ctrl+S)
python main_tui.py

# Or run the CLI
python main.py
```

### VST3 Plugin

See [vst-plugin/README.md](vst-plugin/README.md) for installation — load `text2midi.vst3` in any DAW, type a prompt, and drag the generated MIDI directly into your arrangement.

### Example Prompts

- `Solo piano ballad in F minor`
- `Upbeat pop song with drums, bass, and bright synth`
- `Epic cinematic orchestra with full arrangement`
- `Chill lo-fi beat in D minor with vinyl warmth`
- `Add soaring strings to support the melody`
- `Make it faster and more energetic`
- `Reduce complexity and make it minimal`

**Full documentation**: [text2midi Documentation Hub](docs/DOCUMENTATION_HUB.md)

## 🔒 Security Features

Your API keys are **never** saved as plain text. text2midi uses industry-standard secure storage:

- **Windows**: Keys stored in Windows Credential Manager
- **macOS**: Keys stored in Keychain
- **Linux**: Keys stored in Secret Service (GNOME Keyring, etc.)

Additional security:
- **Automatic Redaction**: API keys are redacted from all logs (patterns: `gsk_`, `sk-`, `key-`, `AIza`, `xai-`, etc.)
- **Secure Permissions**: Config files are restricted to your user only (Unix: `chmod 600`, Windows: `icacls`)
- **No `.env` Distribution**: Default `.env` is never versioned with real keys
- **Zero Key Leakage**: The logging system automatically detects and masks sensitive data

See [Security Guide](docs/SECURITY.md) for more details.

## 📂 What's Inside

### Project Structure

```
src/app/                    # Main application
├── models.py               # Data structures (Note, Track, Session)
├── constants.py            # Music theory (scales, instruments, genres)
├── generator.py            # Music generation (MusicGenerator)
├── midi_creator.py         # MIDI file creation (MIDIGenerator)
├── track_planner.py        # Track planning (TrackPlanner)
├── intent_parser.py        # NLP understanding (IntentParser)
└── session.py              # Session utilities

src/config/                 # Configuration & Security
├── keyring_store.py        # Secure OS keyring integration [NEW]
├── settings.py             # Settings manager with keyring
├── log.py                  # Logging with API key redaction [NEW]
├── provider_catalog.py     # LLM provider configurations
├── setup_wizard.py         # Interactive setup wizard
└── llm.py                  # LLM provider management

src/agents/                 # LangGraph agents
├── base_agent.py           # Base agent structure
├── music_agent.py          # Music composition agent
├── generation_agent.py     # MIDI generation agent
└── refinement_agent.py     # Composition refinement agent

src/midigent/              # Advanced music generation engines
├── engines/
│   ├── ambient_engine.py   # Ambient soundscape generation
│   ├── orchestral_engine.py # Orchestral composition
│   └── ...                 # Genre-specific engines
└── utils/

installer/                 # One-touch installer [NEW]
├── install.bat             # Windows installer
├── install.sh              # macOS/Linux installer
├── build_launcher.py       # PyInstaller exe builder
├── README.md               # Installation guide
└── checksums.json          # Verification hashes

docs/                      # Documentation
├── SECURITY.md             # Security & keyring guide [NEW]
├── GETTING_STARTED.md      # Quick start guide
├── MIDI_GENERATION_GUIDE.md # Full guide
├── ARCHITECTURE.md         # System architecture
├── DAW_*.md                # DAW integration guides
├── plans/                  # Implementation details
│   └── ONE_TOUCH_INSTALLER_PLAN.md
└── specs/                  # Specifications

vst-plugin/                # VST3 plugin (C++ JUCE)
├── src/                    # Plugin source code
├── python-backend/         # Python music generation backend
└── BUILDING.md             # Build instructions
```

## 🎯 Features

✨ **Natural Language Music Creation**
- Describe music in plain English
- AI understands genre, tempo, key, emotion
- Generates MIDI files automatically

🎼 **Smart Composition**
- Dynamic track generation (1-8 tracks)
- Multi-turn conversations for iterative building
- Music theory-aware generation

🤖 **Powered by 15+ AI Providers**
- Recommended: Groq (free, ultra-fast, excellent quality)
- Also supports: OpenAI, Claude, Gemini, Ollama, OpenRouter, and more
- Choose your provider, use any API key

🎛️ **Professional Output**
- Standard MIDI format (compatible with all DAWs)
- Multiple genre support (pop, rock, classical, lo-fi, jazz, electronic, cinematic)
- Proper music theory implementation

## 🚀 Usage

### Web UI (Gradio)

```bash
python main.py
# Opens http://localhost:7860 — interactive music generation with self-refining agents
```

### Terminal UI (Textual)

```bash
python main_tui.py
# Full-featured TUI: API key management, prompt suggestions, history, keyboard shortcuts
# Keybindings: Ctrl+G (generate), Ctrl+R (random), F1 (help), Ctrl+Q (quit)
```

### VST3 Plugin (DAW Integration)

```bash
# Build from source (requires Visual Studio 2022 + CMake)
cd vst-plugin && cmake -B build -G "Visual Studio 17 2022" -A x64
cmake --build build --config Release
# Copy text2midi.vst3 to your VST3 folder, load in any DAW
```

See [vst-plugin/BUILDING.md](vst-plugin/BUILDING.md) for full build instructions.

### Programmatic

```python
from src.app import MusicGenerator, MIDIGenerator
from src.config import LLMConfig

LLMConfig.initialize()
generator = MusicGenerator()
```

## 🔧 Configuration

### Setup Wizard (Recommended)

On first run, text2midi launches an interactive wizard:

```bash
python main_tui.py     # Press Ctrl+S to open Settings
```

The wizard will:
1. Show available AI providers (Groq, OpenAI, Claude, Gemini, etc.)
2. Provide direct links to get free API keys
3. Validate your key instantly
4. **Securely store your key in OS Keyring** (never plain text!)

### LLM Providers

text2midi supports **15+ AI providers**, including:

| Provider | Free Option | Speed | Quality | Setup |
|----------|-------------|-------|---------|-------|
| **Groq** | ⭐ Yes | Ultra-fast | Excellent | [console.groq.com](https://console.groq.com/) |
| **Google Gemini** | ⭐ Yes | Fast | Very Good | [aistudio.google.com](https://aistudio.google.com/) |
| **Ollama** | ⭐ Yes (offline) | Depends on PC | Good | [ollama.com](https://ollama.com/) |
| **OpenAI** | GPT-4o | Fast | Excellent | [platform.openai.com](https://platform.openai.com/) |
| **Anthropic** | Claude | Fast | Excellent | [console.anthropic.com](https://console.anthropic.com/) |
| **OpenRouter** | 100+ models | Varies | High | [openrouter.ai](https://openrouter.ai/) |

### Manual Configuration

You can also configure via `.env` file (though keyring is recommended):

```bash
cp .env.example .env
```

Add your API keys:
```bash
# You only need ONE of these:
GROQ_API_KEY=gsk_your_key_here          # Free
OPENAI_API_KEY=sk-your_key_here         # Paid
ANTHROPIC_API_KEY=sk-ant-your_key_here  # Paid
GEMINI_API_KEY=your_key_here            # Free tier
OLLAMA_API_BASE=http://localhost:11434  # Offline
```

> **Note**: Keys are automatically moved to OS Keyring on first run. The `.env` is only read if keyring is unavailable.

## 📊 Output

MIDI files are saved to `outputs/` with naming format:
```
text2midi_<genre>_<session_id>_<timestamp>.mid
```

Open with any MIDI-compatible tool:
- **DAWs**: Ableton, Logic Pro, FL Studio, Reaper
- **Players**: GarageBand, VLC, Windows Media Player
- **Converters**: Online MIDI to MP3/WAV tools

## 📚 Documentation

| Topic | Link |
|-------|------|
| Getting Started | [docs/GETTING_STARTED.md](docs/GETTING_STARTED.md) |
| Security & API Keys | [docs/SECURITY.md](docs/SECURITY.md) |
| One-Touch Installer | [installer/README.md](installer/README.md) |
| MIDI Generation Guide | [docs/MIDI_GENERATION_GUIDE.md](docs/MIDI_GENERATION_GUIDE.md) |
| Ableton Live | [docs/DAW_ABLETON_LIVE.md](docs/DAW_ABLETON_LIVE.md) |
| Surge XT | [docs/DAW_SURGE_XT.md](docs/DAW_SURGE_XT.md) |
| Track Types Reference | [docs/TRACK_TYPES_REFERENCE.md](docs/TRACK_TYPES_REFERENCE.md) |
| Architecture | [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) |
| VST3 Plugin | [vst-plugin/README.md](vst-plugin/README.md) |
| VST3 Building | [vst-plugin/BUILDING.md](vst-plugin/BUILDING.md) |
| Project Summary | [docs/PROJECT_SUMMARY.md](docs/PROJECT_SUMMARY.md) |

## 🛠️ Development

### Install Development Dependencies

```bash
uv sync
```

### Code Quality

```bash
# Format code
uv run ruff format .

# Lint
uv run ruff check .

# Type check
uv run mypy src/

# Run tests
uv run pytest tests/
```

### Running Tests

```bash
uv run pytest tests/                       # All tests
uv run pytest tests/test_tui/ -v           # TUI tests (32 tests)
uv run pytest tests/ --cov=src             # With coverage
cd vst-plugin/python-backend && python -m pytest test_server.py -v  # Backend tests (12 tests)
```

## 🔌 Requirements

- **Python**: 3.11+
- **Dependencies**: See [pyproject.toml](pyproject.toml)
- **MIDI**: mido library
- **LLM**: One of 15+ supported providers (Groq recommended - free)

## 📦 Installation Methods

### UV (Recommended)
```bash
uv sync
```

### Pip
```bash
pip install -r requirements.txt
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing`)
3. Make your changes
4. Submit a pull request

## 📜 License

See [LICENSE](LICENSE) for details.

## 🆘 Support

- Check [docs/GETTING_STARTED.md](docs/GETTING_STARTED.md) for troubleshooting
- Review [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for design details
- Open a [GitHub issue](https://github.com/cindulasai/text2midi/issues/new) for bugs or feature requests

## 🎵 What Can You Create?

- Piano ballads
- Pop songs
- Electronic beats
- Orchestral compositions
- Lo-fi hip hop
- Ambient soundscapes
- Jazz standards
- Cinematic scores
- And much more!

---

**Built with ❤️ by Sai Cindula (vision & design) and AI agents (code) — for the music tech community.**

## Tech Stack

- **LLM**: 15+ providers supported (Groq, OpenAI, Claude, Gemini, etc.)
- **Keyring**: Windows Credential Manager, macOS Keychain, Linux Secret Service
- **Agents**: LangGraph
- **TUI**: Textual (Python)
- **VST3**: JUCE 6.0.8 (C++) + FastAPI backend (Python)
- **Build**: uv, CMake, PyInstaller, MSVC 2022

## License

MIT
