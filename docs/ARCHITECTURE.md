# MidiGen v2.0 - Production Architecture

A professional-grade AI-powered MIDI music generator with clean, modular architecture.

## Project Structure

```
spec-kit/
├── src/
│   ├── app/                    # Main application layer
│   │   ├── __init__.py
│   │   ├── models.py           # Data structures (Note, Track, Session, etc.)
│   │   ├── constants.py        # Music theory (scales, instruments, genres)
│   │   ├── generator.py        # Music generation logic (MusicGenerator)
│   │   ├── midi_creator.py     # MIDI file creation (MIDIGenerator)
│   │   ├── track_planner.py    # Track planning engine (TrackPlanner)
│   │   ├── intent_parser.py    # NLP intent parsing (IntentParser)
│   │   ├── session.py          # Session management utilities
│   │   └── ui.py               # Gradio web interface (MidiGenApp)
│   │
│   ├── agents/                 # LangGraph agentic architecture
│   │   ├── graph.py            # Main agent graph
│   │   ├── state.py            # Agent state definitions
│   │   ├── *_node.py           # Individual agent nodes
│   │   └── ...
│   │
│   ├── midigent/               # Music generation engine (legacy)
│   │   ├── *.py                # Various music theory engines
│   │   └── midi/               # MIDI utilities
│   │
│   ├── specify_cli/            # Spec-Kit CLI (separate tool)
│   │   └── ...
│   │
│   └── config/                 # Configuration management
│       ├── __init__.py
│       └── llm.py              # LLM provider configuration
│
├── docs/
│   ├── README.md               # Main documentation
│   ├── ARCHITECTURE.md         # This file
│   ├── API.md                  # API reference
│   └── archive/                # Old/legacy documentation
│
├── memory/
│   │
│   └── skills/                 # Reusable prompts/skills
│       └── README.md           # Skills documentation
│
├── specs/                      # Spec Kit specifications (separate)
│   └── ...
│
├── outputs/                    # MIDI output files (local)
│   └── *.mid
│
├── .archive/                   # Archived files (old code, docs, tests)
│   └── ...
│
├── ui.py                       # Web UI entry point
├── main.py                     # CLI entry point (LangGraph agent mode)
├── pyproject.toml              # Project configuration
├── poetry.lock                 # Dependency lock file
└── README.md                   # Quick start guide
```

## Core Modules

### `src/app/` - Application Layer

The main application layer containing all the MIDI generation logic organized into focused, single-responsibility modules.

#### `models.py`
Data structures for the application:
- `Note` - Individual MIDI note with pitch, timing, duration, velocity
- `Track` - Collection of notes with instrument and channel info  
- `TrackConfig` - Configuration for track generation
- `CompositionSession` - Multi-turn composition state
- `GenerationSnapshot` - Generation history snapshots

#### `constants.py`
Music theory constants:
- Scales (major, minor, pentatonic, blues, etc.)
- MIDI note mappings (C=60, etc.)
- General MIDI instruments (0-127 programs)
- Drum kit mappings
- Genre configurations (tempo ranges, keys, energy levels)
- Chord progressions by genre

#### `generator.py`
Music generation (`MusicGenerator` class):
- `generate_melody()` - Lead melodic lines
- `generate_counter_melody()` - Complementary melodies
- `generate_chords()` - Harmonic progressions
- `generate_bass()` - Bass lines with genre-specific patterns
- `generate_arpeggio()` - Arpeggiated patterns
- `generate_pad()` - Sustained atmospheric textures
- `generate_drums()` - Genre-specific drum patterns
- `generate_fx()` - Ambient sound effects

#### `midi_creator.py`
MIDI file creation (`MIDIGenerator` class):
- `create_midi()` - Convert Track objects to MIDI files
- `merge_midi()` - Combine and extend existing tracks

#### `track_planner.py`
Track planning engine (`TrackPlanner` class):
- `plan_tracks()` - Determine optimal track configuration
- AI-powered planning with fallback to rule-based system
- `_extract_track_count()` - Parse explicit track counts from prompts
- `_ensure_track_count()` - Adjust track counts to match requests

#### `intent_parser.py`
Natural language understanding (`IntentParser` class):
- `parse()` - Convert user input to generation parameters
- `_parse_with_ai()` - LLM-powered intent parsing
- `_parse_with_keywords()` - Rule-based fallback
- Duration parsing with validation
- Genre/key/tempo/energy extraction

#### `session.py`
Session utilities:
- `get_session_summary()` - Format session state for display
- `ensure_output_directory()` - Initialize output directory

#### `ui.py`
Web interface (`MidiGenApp` class):
- `create_ui()` - Builds Gradio interface
- `process_message()` - Handles chat interactions
- Multi-turn composition support
- Real-time MIDI generation and download

### `src/config/` - Configuration

LLM provider management:
- `LLMConfig` - Provider initialization and switching
- `call_llm()` - Unified LLM calling interface
- Support for Gemini and Groq

### `src/agents/` - LangGraph Agents (Optional)

Alternative agentic architecture using LangGraph:
- Multi-agent orchestration
- Self-reflection and refinement
- Quality control and validation
- Available via `main.py`

## Entry Points

### Web UI (Recommended)
```bash
python ui.py
```
Launches Gradio interface at `http://localhost:7860`

### CLI (Agent-based)
```bash
python main.py
```
Command-line interface using LangGraph agents

## Data Flow

```
User Input
    ↓
IntentParser (extract genre, tempo, key, energy, duration)
    ↓
TrackPlanner (determine track configuration)
    ↓
MusicGenerator (generate notes for each track type)
    ↓
MIDIGenerator (convert to MIDI format)
    ↓
Save to outputs/
    ↓
User downloads MIDI file
```

## Configuration

### Environment Variables
- `GROQ_API_KEY` - Groq API key (optional)
- `GEMINI_API_KEY` - Google Gemini API key (optional)

### LLM Providers
- **Gemini (default)** - Google's multimodal model
- **Groq** - Fast inference with Llama 3.3

Switch providers: `LLMConfig.set_provider('groq')`

## Production Checklist

- [x] Modular architecture (single responsibility)
- [x] Type hints throughout
- [x] Comprehensive docstrings
- [x] Error handling and validation
- [x] Configuration management
- [x] Logging infrastructure
- [x] Clean separation of concerns
- [x] Reusable components
- [x] Extensible design
- [x] Production-ready imports

## Add New Features

### Add New Track Type
1. Add generator method to `MusicGenerator` in `generator.py`
2. Update `TrackPlanner._plan_with_rules()` to include new type
3. Add example to `ui.py` docstring

### Add New Genre
1. Add to `GENRE_CONFIG` in `constants.py`
2. Optional: Add genre-specific patterns to `MusicGenerator`
3. Update chord progressions in `CHORD_PROGRESSIONS`

### Add New LLM Provider
1. Create provider function in `config/llm.py`
2. Update `LLMConfig.initialize()`
3. Update `call_llm()` provider switch

## Performance

- **Generation**: 1-3 seconds per composition (10-30 bars)
- **MIDI Size**: 10-50 KB per file
- **Memory**: ~50-100 MB per session
- **Concurrent Users**: Scales horizontally (stateless LLM calls)

## Code Quality

- **Style**: PEP 8 compliant
- **Type Checking**: Full Python 3.11+ type hints
- **Testing**: Unit tests in original `tests/` directory
- **Documentation**: Comprehensive docstrings and README files

## License

See LICENSE file for details.

## Support

For issues or questions:
1. Check `docs/` for additional documentation
2. Review `memory/skills/` for reusable patterns
3. See `memory/constitution.md` for AI assistant guidelines
