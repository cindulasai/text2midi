# 🗺️ MidiGen v2.0 - Quick Navigation Guide

## Where's My Code?

**I want to...** | **Go to...**
---|---
Change how music is generated | [`src/app/generator.py`](src/app/generator.py)
Add a new genre or scale | [`src/app/constants.py`](src/app/constants.py)
Modify the web interface | [`src/app/ui.py`](src/app/ui.py)
Understand user input (NLP) | [`src/app/intent_parser.py`](src/app/intent_parser.py)
Decide how many tracks to create | [`src/app/track_planner.py`](src/app/track_planner.py)
Change data structures | [`src/app/models.py`](src/app/models.py)
Create or modify MIDI | [`src/app/midi_creator.py`](src/app/midi_creator.py)
Manage LLM providers | [`src/config/llm.py`](src/config/llm.py)
Understand the overall design | [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)
Get started quickly | [`docs/QUICKSTART_MIDIGEN.md`](docs/QUICKSTART_MIDIGEN.md)
See what changed | [`REFACTORING_COMPLETE.md`](REFACTORING_COMPLETE.md)

## Entry Points

```bash
# Web UI (Recommended)
python ui.py                   # Gradio interface @ http://localhost:7860

# CLI (LangGraph Agents)
python main.py                 # Interactive command-line mode
```

## Quick Code Examples

### Generate Music Programmatically
```python
from src.app import MidiGenApp
from src.config import LLMConfig

LLMConfig.initialize()
app = MidiGenApp()
_, filepath, _, summary = app.process_message("Create pop song", [])
print(f"Generated: {filepath}")
```

### Access Music Generator
```python
from src.app.generator import MusicGenerator

gen = MusicGenerator()
notes = gen.generate_melody(root=60, mode="major", bars=8, energy="high", genre="pop")
print(f"Generated {len(notes)} notes")
```

### Work with Models
```python
from src.app.models import Note, Track, CompositionSession

note = Note(pitch=60, start_time=0.0, duration=1.0, velocity=80)
session = CompositionSession(genre="pop", tempo=120)
```

### Configure LLM
```python
from src.config import LLMConfig

LLMConfig.initialize()
print(LLMConfig.AVAILABLE_PROVIDERS)  # ['gemini', 'groq']
LLMConfig.set_provider('groq')
```

## File Locations

### Data Models
- **Note**: `src/app/models.py` - Single MIDI note
- **Track**: `src/app/models.py` - Collection of notes
- **CompositionSession**: `src/app/models.py` - Multi-turn session

### Music Theory
- **Scales**: `src/app/constants.py` - Major, minor, pentatonic, etc.
- **Instruments**: `src/app/constants.py` - MIDI program numbers
- **Genres**: `src/app/constants.py` - Genre configurations
- **Chords**: `src/app/constants.py` - Genre chord progressions

### Generation Engines
- **Music Generation**: `src/app/generator.py` - MusicGenerator class
- **MIDI Creation**: `src/app/midi_creator.py` - MIDIGenerator class  
- **Track Planning**: `src/app/track_planner.py` - TrackPlanner class
- **Intent Parsing**: `src/app/intent_parser.py` - IntentParser class

### Configuration
- **LLM Management**: `src/config/llm.py` - LLMConfig class

### User Interface
- **Gradio Web UI**: `src/app/ui.py` - MidiGenApp web interface
- **Web Entry Point**: `ui.py` - Application launcher

## Import Reference

```python
# Data models
from src.app.models import Note, Track, CompositionSession, GenerationSnapshot, TrackConfig

# Constants
from src.app.constants import SCALES, NOTE_TO_MIDI, DRUM_MAP, GM_INSTRUMENTS, GENRE_CONFIG

# Generation
from src.app.generator import MusicGenerator
from src.app.midi_creator import MIDIGenerator
from src.app.track_planner import TrackPlanner
from src.app.intent_parser import IntentParser

# Application
from src.app import MidiGenApp

# Configuration
from src.config import LLMConfig, call_llm
```

## Common Patterns

### Add a New Genre
1. Add to `GENRE_CONFIG` in `src/app/constants.py`
2. Add chord progressions to `CHORD_PROGRESSIONS`
3. Optional: Add specific patterns in `src/app/generator.py`

### Add a New Track Type
1. Add generation method in `src/app/generator.py`
2. Update `src/app/track_planner.py` to use it
3. Test with a manual call to `MusicGenerator`

### Modify Music Generation
Edit `src/app/generator.py` - each method is independent and focuses on one track type

### Change LLM Provider
```python
from src.config import LLMConfig
LLMConfig.set_provider('groq')  # or 'gemini'
```

### Access Session State
```python
session = app.session  # CompositionSession object
print(session.genre, session.tempo, session.key, session.mode)
print([t.name for t in session.tracks])
```

## Project Statistics

- **Total Python Files**: ~65 files
- **Application Files**: 10 modules in `src/app/`
- **Configuration**: 2 files in `src/config/`
- **Total App Lines**: ~1100 (refactored from 1440)
- **Module Size**: 65-300 lines each
- **Test Files**: Ready for pytest
- **Documentation**: 5+ comprehensive guides

## Archived Files Location

- **Old Code**: `.archive/app.py.refactored`
- **Old Tests**: `.archive/test_*.py`
- **Old Docs**: `.archive/*.md` (30+ files)
- **Backups**: `.archive/app.py.backup`, `app_langgraph.py`

## Documentation Map

| Document | Purpose |
|----------|---------|
| [README.md](README.md) | Project overview and quick start |
| [REFACTORING.md](REFACTORING.md) | What changed and how |
| [REFACTORING_COMPLETE.md](REFACTORING_COMPLETE.md) | Detailed refactoring report |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | System design and components |
| [docs/QUICKSTART_MIDIGEN.md](docs/QUICKSTART_MIDIGEN.md) | Music generation quick start |
| [docs/README.md](docs/README.md) | Documentation hub |

## Key Classes Summary

| Class | File | Purpose |
|-------|------|---------|
| `MidiGenApp` | `src/app/ui.py` | Main application, Gradio interface |
| `MusicGenerator` | `src/app/generator.py` | Generates musical notes |
| `MIDIGenerator` | `src/app/midi_creator.py` | Creates MIDI files |
| `TrackPlanner` | `src/app/track_planner.py` | Plans track configuration |
| `IntentParser` | `src/app/intent_parser.py` | Parses user input |
| `CompositionSession` | `src/app/models.py` | Maintains session state |
| `LLMConfig` | `src/config/llm.py` | Manages LLM providers |

## Performance Tips

- **Faster Generation**: Use `groq` provider (faster inference)
- **Better Music**: Use `gemini` provider (more sophisticated)
- **Batch Generation**: Reuse `MidiGenApp` instance
- **Less Memory**: Limit sessions, clean up old sessions

## Debugging Tips

1. **Check imports**: `python -c "from src.app import MidiGenApp"`
2. **Check dependencies**: `pip list | grep -E "mido|gradio|groq|google"`
3. **Check API keys**: `echo $GEMINI_API_KEY` and `echo $GROQ_API_KEY`
4. **Check LLM status**: `LLMConfig.AVAILABLE_PROVIDERS`
5. **Enable verbose**: Check console output during generation

## Common Commands

```bash
# Run web UI
python ui.py

# Run CLI
python main.py

# Test imports
python -c "from src.app import MidiGenApp; print('✅ OK')"

# Check structure
find src/app -name "*.py" | sort

# View archived files
ls -la .archive/ | head -20

# Check documentation
ls -la docs/

# Run with poetry
poetry run python ui.py
```

---

**This guide helps you navigate the refactored MidiGen codebase. Everything is organized, documented, and ready to use!**
