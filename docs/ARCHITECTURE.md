# text2midi - System Architecture

A professional-grade AI-powered text-to-MIDI music generator with a clean, modular LangGraph agentic architecture.

## Project Structure

```
text2midi/
├── main.py                     # CLI entry point
├── src/
│   ├── app/                    # Core application layer
│   │   ├── __init__.py
│   │   ├── models.py           # Data structures (Note, Track, Session, etc.)
│   │   ├── constants.py        # Music theory (scales, instruments, genres)
│   │   ├── generator.py        # Music generation logic (MusicGenerator)
│   │   ├── midi_creator.py     # MIDI file creation (MIDIGenerator)
│   │   ├── track_planner.py    # Track planning engine (TrackPlanner)
│   │   ├── intent_parser.py    # NLP intent parsing (IntentParser)
│   │   └── session.py          # Session management utilities
│   │
│   ├── agents/                 # LangGraph agentic architecture
│   │   ├── graph.py            # Main compiled agent graph
│   │   ├── state.py            # MusicState TypedDict (25+ fields)
│   │   ├── intent_parser_node.py
│   │   ├── track_planner_node.py
│   │   ├── theory_validator_node.py
│   │   ├── track_generator_node.py
│   │   ├── quality_control_node.py
│   │   ├── refinement_node.py
│   │   ├── midi_creator_node.py
│   │   └── session_summary_node.py
│   │
│   ├── midigent/               # Advanced music generation engines
│   │   ├── advanced_generator.py
│   │   ├── emotion_engine.py
│   │   ├── music_theory_engine.py
│   │   ├── creative_variation_engine.py
│   │   ├── cultural_music.py
│   │   ├── duration_models.py
│   │   └── ...
│   │
│   └── config/                 # Configuration
│       ├── llm.py              # LLM provider management
│       └── __init__.py
│
├── tests/                      # Test suite
│   └── midi_generation/        # MIDI generation evaluation tests
│
└── outputs/                    # Generated MIDI files (gitignored)
```

## Agent Graph

The LangGraph state machine processes each user request through a pipeline:

```
User Input
    │
    ▼
[Intent Parser] ──► Parse genre, tempo, mood, instruments, duration
    │
    ▼
[Track Planner] ──► Determine number of tracks, assign instruments
    │
    ▼
[Theory Validator] ──► Validate music theory correctness
    │
    ▼
[Track Generator] ──► Generate notes for each track
    │
    ▼
[Quality Control] ──► Score composition quality (0-100)
    │
    ├── Score < 70 ──► [Refinement] ──► back to Generator
    │
    ▼ Score ≥ 70
[MIDI Creator] ──► Write standard MIDI file to outputs/
    │
    ▼
[Session Summary] ──► Update conversation context for multi-turn
    │
    ▼
Output: outputs/text2midi_{genre}_{hash}_{timestamp}.mid
```

## LLM Provider Stack

| Priority | Provider | Model | API Key |
|----------|----------|-------|---------|
| 1 (default) | MiniMax M2.5 | MiniMax-M2.5 (coding model) | `MINIMAX_API_KEY` |
| 2 (fallback) | Groq | llama-4-maverick | `GROQ_API_KEY` |

Provider is auto-selected at startup based on which API key is present.

## MIDI Output Spec

- Format: Standard MIDI Type 0 (single track) or Type 1 (multi-track)
- Resolution: 480 PPQ (pulses per quarter note)
- Tracks: 1–8 simultaneous tracks
- Channels: Channels 1–8 (GM standard instrument assignment)
- Filename: `text2midi_{genre}_{8-char-hash}_{YYYYMMDD_HHMMSS}.mid`

## Data Flow

```
User text → MusicIntent → MusicState → [Agent Pipeline] → GenerationSnapshot → .mid file
```

Key types in `src/app/models.py`:
- `MusicIntent` — parsed intent (genre, tempo, mood, instruments)
- `TrackConfig` — per-track configuration (instrument, channel, notes)
- `Note` — individual note (pitch, duration, velocity, channel)
- `GenerationSnapshot` — immutable record of a completed generation
- `CompositionSession` — multi-turn session state
