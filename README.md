# text2midi - AI-Powered MIDI Composer

**text2midi**: Transform text descriptions into professional multi-track MIDI compositions using AI. Generate music instantly through natural language conversation.

## 🎵 Quick Start

```bash
# Install with uv (recommended)
uv sync

# Run the Web UI (Gradio)
python main.py

# Run the Terminal UI
python main_tui.py
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
├── session.py              # Session utilities

src/config/                 # Configuration
└── llm.py                  # LLM provider management

src/agents/                 # LangGraph agents
src/midigent/               # Advanced music generation engines
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

🤖 **Powered by MiniMax M2.5**
- Default LLM: [MiniMax M2.5](https://platform.minimaxi.com/) (state-of-the-art coding model)
- Fallback: Groq (llama-4-maverick / llama-3.3-70b)

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

### LLM Providers

text2midi uses **MiniMax M2.5** by default — a state-of-the-art coding model. Set your API key and it will be used automatically. Groq serves as fallback.

| Priority | Provider | Model | Get Key |
|----------|----------|-------|---------|
| 1st (default) | **MiniMax M2.5** | MiniMax-M2.5 | [platform.minimaxi.com](https://platform.minimaxi.com/) |
| 2nd (fallback) | Groq | llama-4-maverick | [console.groq.com](https://console.groq.com/) |

### Environment Variables

Copy `.env.example` to `.env` and fill in your keys:

```bash
MINIMAX_API_KEY=your-key-here   # Default provider
GROQ_API_KEY=your-key-here      # Fallback
```

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
- **LLM**: At least one of: MiniMax or Groq API key

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

**Created with ❤️ by developers for musicians and music developers**

## Tech Stack

- **MIDI**: mido
- **LLM**: MiniMax M2.5 coding model (default), Groq
- **Agents**: LangGraph
- **TUI**: Textual (Python)
- **VST3**: JUCE 6.0.8 (C++) + FastAPI backend (Python)
- **Build**: uv, CMake, PyInstaller, MSVC 2022

## License

MIT
