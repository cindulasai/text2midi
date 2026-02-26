# MidiGen v2.0 - LangGraph Agentic Architecture

## Quick Start

### Installation

```bash
# Install dependencies
poetry install --no-root

# Set up API key (optional, for AI-powered intent parsing)
export GROQ_API_KEY="your-api-key-here"
```

### Usage

#### Option 1: Interactive CLI

```bash
poetry run python main.py
```

This launches an interactive prompt where you can describe music you want to generate:

```
📝 Describe the music you want to generate:
   Examples:
   - 'Create a peaceful ambient soundscape'
   - 'Epic cinematic orchestra with full arrangement'
   - 'Simple solo piano piece in D minor'
   - 'Funky electronic beat at 125 BPM'
   - 'Sad lo-fi hip hop in D minor'

🎯 Your prompt: Create a simple lo-fi beat
```

#### Option 2: Programmatic Usage

```python
from src.agents.graph import get_agentic_graph
from src.agents.state import MusicState
import uuid

# Load the graph
graph = get_agentic_graph()

# Create initial state
session_id = str(uuid.uuid4())[:8]
initial_state: MusicState = {
    "user_prompt": "Create a peaceful ambient soundscape",
    "intent": None,
    "track_plan": [],
    "theory_validation": {},
    "theory_valid": False,
    "theory_issues": [],
    "generated_tracks": [],
    "generation_metadata": {},
    "quality_report": None,
    "refinement_attempts": 0,
    "refinement_feedback": "",
    "needs_refinement": False,
    "final_midi_path": None,
    "session_summary": "",
    "messages": [],
    "error": None,
    "error_context": None,
    "session_id": session_id,
    "composition_state": {
        "existing_tracks": [],
        "tempo": 120,
        "key": "C",
        "genre": "pop",
        "mode": "major",
    },
    "max_refinement_iterations": 2,
    "current_iteration": 0,
}

# Run the workflow
config = {"configurable": {"thread_id": session_id}}
result_state = graph.invoke(initial_state, config=config)

# Access results
midi_path = result_state.get("final_midi_path")
quality_report = result_state.get("quality_report")
print(f"Generated MIDI: {midi_path}")
print(f"Quality Score: {quality_report.overall_score:.2f}/1.0 if quality_report else 'N/A')
```

## Architecture

MidiGen uses a LangGraph-based agentic architecture with specialized agents for different aspects of music generation:

### Agent Pipeline

1. **[INTENT AGENT]** - Parses user request to extract musical intent
   - Analyzes genre, mood, energy, tempo, key
   - Uses Groq LLM when available, fallback to rule-based parsing

2. **[TRACK PLANNER]** - Plans optimal track configuration  
   - Determines track types and instruments
   - Adjusts to requested track count
   - AI-powered planning with rule-based fallback

3. **[THEORY VALIDATOR]** - Validates music theory choices
   - Checks genre-instrument compatibility
   - Ensures harmonic/melodic balance
   - Validates rhythm section presence

4. **[TRACK GENERATOR]** - Generates actual musical notes
   - Creates MIDI notes for each track type
   - Respects scale, mode, and genre preferences
   - Generates melody, harmony, bass, drums, pads, etc.

5. **[QUALITY CONTROL]** - Assesses generated tracks
   - Checks track diversity and density
   - Analyzes velocity variation and dynamics
   - Determines if refinement is needed

6. **[REFINEMENT]** (Optional) - Fixes quality issues
   - Regenerates problematic tracks
   - Applies iterative improvements
   - Re-checks quality after changes

7. **[MIDI CREATOR]** - Creates final MIDI file
   - Saves to outputs/ directory
   - Includes metadata and timestamps

8. **[SESSION SUMMARY]** - Generates composition summary
   - Reports final statistics
   - Lists track count, tempo, key, etc.

### Conditional Routing

- **Quality Control Route**: If issues found and iterations remaining → Refine
- **Refinement Route**: If iterations remaining → Re-check quality; Otherwise → Finalize

### Error Handling

- All nodes check for errors in state
- Errors gracefully skip to final summary
- No workflow failure from individual node issues

## Project Structure

```
spec-kit/
├── main.py                          # CLI entry point
├── test_workflow.py                 # Workflow test script
├── app.py                           # Original working implementation
├── pyproject.toml                   # Project dependencies
├── src/
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── state.py                 # MusicState TypedDict definition
│   │   ├── graph.py                 # LangGraph workflow builder
│   │   ├── intent_parser_node.py    # Intent parsing agent
│   │   ├── track_planner_node.py    # Track planning agent
│   │   ├── theory_validator_node.py # Music theory validation
│   │   ├── track_generator_node.py  # Track generation
│   │   ├── quality_control_node.py  # Quality assessment
│   │   ├── refinement_node.py       # Track refinement
│   │   ├── midi_creator_node.py     # MIDI file creation
│   │   └── session_summary_node.py  # Session summary generation
│   └── midigent/
│       ├── duration_parser.py
│       ├── duration_validator.py
│       ├── intent_parser.py
│       └── variation_engine.py
└── outputs/
    └── *.mid                        # Generated MIDI files
```

## Features

### Supported Track Types

- **lead**: Main melody
- **counter_melody**: Secondary melody  
- **harmony**: Chord progressions
- **bass**: Bass line
- **drums**: Drum patterns
- **arpeggio**: Arpeggiated patterns
- **pad**: Atmospheric pads
- **fx**: Sound effects/ambience

### Supported Genres

- Pop
- Rock
- Jazz
- Classical
- Electronic
- Lo-fi
- Ambient
- Cinematic
- Funk
- R&B

### Quality Metrics

- Track diversity (instrument variation)
- Note density (balance across tracks)
- Velocity variation (dynamics)
- Harmonic balance
- Rhythm section presence

## Dependencies

Key packages installed via poetry:

- **langgraph**: LangGraph workflow framework
- **langchain**: LangChain core library
- **langchain-groq**: Groq LLM integration
- **groq**: Groq API client
- **gradio**: Web UI framework
- **mido**: MIDI file creation
- **pydantic**: Data validation

## Testing

Run the workflow test:

```bash
poetry run python test_workflow.py
```

Expected output:
```
Testing MidiGen Workflow...

1. Loading graph...
   [OK] Graph loaded

2. Creating initial state...
   [OK] State created (session: xxxxxxxx)

3. Running workflow...
   [BRAIN] [INTENT AGENT] Analyzing user request...
   [OK] Intent parsed: new pop | Tracks: None | Energy: medium
   ...

4. Checking results...
   [OK] No errors
   [OK] Generated tracks: 2
   [OK] MIDI path: outputs\midigen_pop_xxxxxxxx_20260208_xxxxxx.mid
   [OK] Session summary: True

[SUCCESS] MIDI file created successfully!
   Path: outputs\midigen_pop_xxxxxxxx_20260208_xxxxxx.mid
   Size: 957 bytes
```

## Generated MIDI Files

All generated MIDI files are saved to the `outputs/` directory with format:

```
midigen_{genre}_{session_id}_{timestamp}.mid
```

Example: `midigen_pop_06dc01d5_20260208_215559.mid`

## Future Enhancements

- [ ] Parallel track generation for multiple agents
- [ ] Session persistence and resume capability
- [ ] Web UI with gradio integration
- [ ] Multi-turn composition sessions
- [ ] Track editing and refinement tools
- [ ] Export to other audio formats
- [ ] Real-time synthesis

## References

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Groq API Documentation](https://console.groq.com/docs)
- [MIDI Specification](https://www.midi.org/specifications)
