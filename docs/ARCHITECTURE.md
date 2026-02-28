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
│   │   ├── intent_parser.py    # TUI intent parsing (delegates to LLM Intent Engine)
│   │   └── session.py          # Session management utilities
│   │
│   ├── intent/                 # LLM Intent Parsing Engine (PLAN-003)
│   │   ├── __init__.py
│   │   ├── schema.py           # Pydantic v2 models (ParsedIntent + sub-schemas)
│   │   ├── prompt_templates.py # Chain-of-thought system prompt + 8 few-shot examples
│   │   ├── preprocessor.py     # Deterministic text normalization + number extraction
│   │   └── engine.py           # LLMIntentEngine — unified orchestrator
│   │
│   ├── agents/                 # LangGraph agentic architecture
│   │   ├── graph.py            # Main compiled agent graph
│   │   ├── state.py            # MusicState TypedDict (25+ fields)
│   │   ├── intent_parser_node.py   # Uses LLMIntentEngine
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
│   │   ├── advanced_intent_parser.py  # Legacy (deprecated, kept for compat)
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
│   ├── test_intent_engine.py   # Intent engine tests (50 cases)
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
[Intent Parser] ──► LLM Intent Engine (chain-of-thought + Pydantic validation)
    │                 ├─ Preprocessor: normalize text, extract hard numbers
    │                 ├─ LLM call: 8 few-shot examples, temp=0.1, 1500 tokens
    │                 ├─ Validation: Pydantic v2 schema + coherence checks
    │                 ├─ Retry: auto-correction on validation failure (max 1)
    │                 └─ Fallback: enhanced keyword parser (no LLM needed)
    │
    ▼
[Track Planner] ──► Determine tracks, assign instruments (respects confidence)
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

text2midi supports 15+ AI providers. Auto-selects available provider at startup:

| Priority | Provider | Model | API Key |
|----------|----------|-------|---------|
| 1st | Groq | llama-3.3-70b or llama-4-maverick | `GROQ_API_KEY` |
| 2nd | OpenAI | GPT-4o | `OPENAI_API_KEY` |
| 3rd | Anthropic | Claude 3.5 Sonnet | `ANTHROPIC_API_KEY` |
| ... | **15+ total** | See [docs/GETTING_STARTED.md](GETTING_STARTED.md) for full list | `*_API_KEY` |

First available key is used automatically. User can specify preference in Settings (Ctrl+S in TUI).

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
- `ParsedIntent` — rich Pydantic model from LLM Intent Engine (confidence-scored)
- `TrackConfig` — per-track configuration (instrument, channel, notes)
- `Note` — individual note (pitch, duration, velocity, channel)
- `GenerationSnapshot` — immutable record of a completed generation
- `CompositionSession` — multi-turn session state
