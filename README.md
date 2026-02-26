# text2midi - AI-Powered MIDI Composer

**text2midi**: Transform text descriptions into professional multi-track MIDI compositions using AI. Generate music instantly through natural language conversation.

## 🎵 Quick Start

```bash
# Install with Poetry (recommended)
poetry install

# Run the CLI
python main.py
```

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

### MidiGen Components

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

src/agents/                 # LangGraph agents (optional)
src/midigent/               # Additional music engines
```

### Additional Features

```
memory/                     # Knowledge base and preferences
outputs/                    # Generated MIDI files
tasks/                      # Task templates and workflows
```

## 🎯 Features

### MidiGen

✨ **Natural Language Music Creation**
- Describe music in plain English
- AI understands genre, tempo, key, emotion
- Generates MIDI files automatically

🎼 **Smart Composition**
- Dynamic track generation (1-8 tracks)
- Multi-turn conversations for iterative building
- Music theory-aware generation

🎛️ **Professional Output**
- Standard MIDI format (compatible with all DAWs)
- Multiple genre support (pop, rock, classical, etc.)
- Proper music theory implementation

### Spec-Kit

📝 **Specification-First Development**
- Define requirements clearly before coding
- AI agents implement based on specifications
- Automated context management

🤖 **AI Integration**
- Works with any LLM (Claude, Gemini, Groq, etc.)
- Context-aware code generation
- Self-refining agent workflows

## 🚀 Usage

### CLI

```bash
python main.py
# Interactive music generation with self-refining agents
```

### Programmatic

```python
from src.app import MidiGenApp

app = MidiGenApp()
app.process_message("Create a pop song", [])
```

## 🔧 Configuration

### LLM Providers

```python
from src.config import LLMConfig

# Available: 'gemini' (default), 'groq'
LLMConfig.set_provider('groq')
```

### Environment Variables

```bash
export GEMINI_API_KEY="your-key"    # Google Gemini
export GROQ_API_KEY="your-key"      # Groq
```

## 📊 Output

MIDI files are saved to `outputs/` with naming format:
```
midigen_<genre>_<session_id>_<timestamp>.mid
```

Open with any MIDI-compatible tool:
- **DAWs**: Ableton, Logic Pro, FL Studio, Reaper
- **Players**: GarageBand, VLC, Windows Media Player
- **Converters**: Online MIDI to MP3/WAV tools

## 📚 Documentation

| Topic | Link |
|-------|------|
| MidiGen Quick Start | [docs/QUICKSTART_MIDIGEN.md](docs/QUICKSTART_MIDIGEN.md) |
| Architecture | [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) |
| API Reference | [docs/API.md](docs/API.md) |
| Spec-Kit Quick Start | [docs/QUICKSTART.md](docs/QUICKSTART.md) |
| Installation | [docs/installation.md](docs/installation.md) |

## 🛠️ Development

### Install Development Dependencies

```bash
poetry install --with dev
```

### Code Quality

```bash
# Format code
black src/

# Lint
ruff check src/

# Type check
mypy src/

# Run tests
pytest tests/
```

### Running Tests

```bash
pytest tests/
pytest tests/test_generator.py -v
pytest --cov=src tests/        # With coverage
```

## 🔌 Requirements

- **Python**: 3.11+
- **Dependencies**: See [pyproject.toml](pyproject.toml)
- **MIDI**: mido library
- **Web UI**: Gradio
- **LLM**: Groq or Google Generative AI API key (optional)

## 📦 Installation Methods

### Poetry (Recommended)
```bash
poetry install
```

### Pip
```bash
pip install -r requirements.txt
```

### UV (Fast)
```bash
uv pip install -r requirements.txt
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing`)
3. Make your changes
4. Submit a pull request

## 📜 License

This project is built on top of [GitHub Spec-Kit](https://github.com/github/spec-kit).

See [LICENSE](LICENSE) for details.

## 🆘 Support

**MidiGen Issues?**
- Check [docs/QUICKSTART_MIDIGEN.md](docs/QUICKSTART_MIDIGEN.md) troubleshooting
- Review [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for design details
- Check error messages in console output

**Spec-Kit Questions?**
- See [AGENTS.md](AGENTS.md) for agent integration
- Review [docs/](docs/) for comprehensive guides
- Check [memory/](memory/) for skills and patterns

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

*MidiGen: Generate music with AI | Spec-Kit: Build software with specs*

## Tech Stack

- **UI**: Gradio
- **MIDI**: mido
- **LLM**: Groq (llama-3.3-70b-versatile)
- **Methodology**: Spec-Driven Development (spec-kit)

## License

MIT
