# MidiGen LangGraph Migration Guide

## Overview

MidiGen has been successfully migrated to a **LangGraph-based agentic architecture**. This provides autonomous agent orchestration, self-reflection, and intelligent refinement capabilities.

## What Changed

### Before (Monolithic)
- Single `process_message()` method handling all logic sequentially
- Rigid pipeline: Parse Intent → Plan Tracks → Generate Tracks → Save MIDI
- No self-reflection or quality assessment
- Limited error recovery

### After (Agentic with LangGraph)
- **8 specialized agents** with distinct responsibilities
- **Dynamic routing** based on state evaluation
- **Self-reflection loop**: Quality assessment determines if refinement needed
- **Persistent state**: Full composition history and context
- **Extensible design**: Easy to add new agents or capabilities

## Project Structure

```
src/agents/
├── __init__.py           # Module exports
├── state.py              # MusicState, MusicIntent, TypedDicts
├── nodes.py              # Individual agent implementations (8 agents)
├── graph.py              # LangGraph builder and routing logic
└── MIGRATION.md          # This file

app.py                     # Original monolithic version (kept for reference)
app_langgraph.py          # NEW: LangGraph-based agentic version
requirements.txt          # Updated with langgraph, langchain
```

## Architecture

### Agent Pipeline

```
START
  ↓
[1] Intent Parser
    └─ Parse user request → MusicIntent
  ↓
[2] Track Planner
    └─ Create optimal track configuration
  ↓
[3] Music Theory Validator
    └─ Validate genre fit, harmony, rhythm
  ↓
[4] Track Generator
    └─ Generate MIDI notes for all tracks
  ↓
[5] Quality Control
    └─ Assess quality and decide on refinement
  ↓
  ├─ If needs refinement (and iterations remaining)
  │  └─ [6] Refinement Agent
  │     └─ Fix problematic tracks
  │     └─ Loop back to Quality Control
  │
  └─ If quality acceptable or max iterations
     ↓
[7] MIDI Creator
    └─ Create and save final MIDI file
  ↓
[8] Session Summary
    └─ Generate natural language summary
  ↓
END
```

### Conditional Routing

**Quality Control Router:**
- If `needs_refinement` AND `iterations_remaining` → "refine"
- Otherwise → "finalize"

**Refinement Router:**
- If `iterations_remaining` → "recheck" (loop to quality_control)
- Otherwise → "finalize" (go to midi_creator)

## Agent Specifications

### 1. Intent Parser Agent
**Purpose:** Parse natural language user requests
- Extracts: genre, energy, mood, tempo, key, track count, duration
- Uses: Groq LLM if available, keyword-based fallback
- Output: `MusicIntent` object

### 2. Track Planner Agent
**Purpose:** Design optimal track configuration
- Inputs: Genre, energy, explicit track count from user
- Uses: AI-guided planning (Groq) or rule-based heuristics
- Ensures: Requested track count is met exactly
- Output: `List[TrackConfig]`

### 3. Music Theory Validator Agent
**Purpose:** Validate harmonic and musical choices
- Checks:
  - Genre-appropriate instruments
  - Harmonic balance (has pad/harmony tracks)
  - Rhythm section present (drums/bass)
  - Melodic presence
  - Track priority sequencing
- Output: Validation report + theory issues

### 4. Track Generator Agent
**Purpose:** Generate actual musical content
- Parallelizable: Each track type can be generated independently
- Generates per track type:
  - `lead`: Melody notes
  - `harmony`: Chord progressions
  - `bass`: Bass lines
  - `drums`: Drum patterns
  - `pad`: Sustained atmospheric notes
  - `arpeggio`: Repeated harmonic patterns
  - `counter_melody`: Secondary melody
  - `fx`: Ambient texture
- Output: `List[Track]` with MIDI notes

### 5. Quality Control Agent
**Purpose:** Assess generated music and decide on refinement
- Evaluates:
  - Track diversity
  - Note density (completeness)
  - Track balance (no empty tracks)
  - Velocity variation (dynamics)
- Calculates: Overall quality score (0-1)
- Decides: Refinement needed?
- Output: `GenerationQualityReport`

### 6. Refinement Agent
**Purpose:** Fix issues identified in quality check
- Regenerates tracks with:
  - Higher density (if too sparse)
  - Better parameters (if problematic)
- Uses: Same generator as Track Generator with adjusted parameters
- Limitations: Max 2 iterations to prevent infinite loops
- Output: Improved `List[Track]`

### 7. MIDI Creator Agent
**Purpose:** Create and save final MIDI file
- Integrates: Existing `MIDIGenerator` class
- Saves to: `outputs/midigen_{genre}_{session_id}_{timestamp}.mid`
- Metadata: Genre, session ID, timestamp
- Output: File path

### 8. Session Summary Agent
**Purpose:** Generate human-readable composition summary
- Creates: Markdown summary with:
  - Action performed (new/extend/modify)
  - Genre, tempo, key, mode
  - Track count and duration
  - Quality assessment results
- Output: Summary string for UI display

## State Management

### MusicState TypedDict
Contains all information flowing through the graph:

```python
class MusicState(TypedDict):
    # Input
    user_prompt: str
    
    # From each agent
    intent: MusicIntent                          # Intent Parser output
    track_plan: List[TrackConfig]                # Track Planner output
    theory_validation: Dict[str, Any]            # Validator output
    theory_issues: List[str]
    generated_tracks: List[Track]                # Generator output
    quality_report: GenerationQualityReport      # QA output
    
    # Refinement loop
    refinement_attempts: int
    current_iteration: int
    needs_refinement: bool
    
    # Context
    session_id: str
    composition_state: Dict[str, Any]            # Current session info
    
    # Output
    final_midi_path: Optional[str]
    session_summary: str
    
    # Error handling
    error: Optional[str]
    error_context: Optional[str]
```

## Running the Agentic Version

### Option 1: Run New LangGraph Version
```bash
python app_langgraph.py
```

**Launches:**
- Gradio UI at http://localhost:7860
- Agentic agent pipeline for each request
- Full agent introspection output on startup

### Option 2: Keep Using Original (Monolithic)
```bash
python app.py
```

**Note:** Original `app.py` remains unchanged for backward compatibility.

## How It Works: Example Request Flow

### User Input
```
"Create an epic cinematic orchestra with 6 tracks"
```

### Agent Execution

**[1] Intent Parser**
```
→ Extracts:
  - action: "new"
  - genre: "cinematic"
  - energy: "high"
  - track_count: 6
  - mood: "epic"
```

**[2] Track Planner**
```
→ Plans 6 tracks:
  1. Strings (lead)
  2. Brass (counter_melody)
  3. Choir (harmony)
  4. Piano (arpeggio)
  5. Bass (bass)
  6. Drums (drums)
```

**[3] Theory Validator**
```
→ Validates:
  ✓ Genre-appropriate instruments
  ✓ Has harmony tracks
  ✓ Has rhythm section
  ✓ Has melody
```

**[4] Track Generator**
```
→ Generates tracks:
  • Strings: 47 notes (melody)
  • Brass: 28 notes (counter)
  • Choir: 22 notes (harmony)
  • Piano: 35 notes (arpeggio)
  • Bass: 16 notes (bass line)
  • Drums: 64 notes (pattern)
```

**[5] Quality Control**
```
→ Assessment:
  • Score: 0.85/1.0
  • Positive: Good track diversity, Good velocity variation
  • Issues: Limited density in counter_melody
  • Refinement needed: YES (iteration 1/2)
```

**[6] Refinement Agent**
```
→ Regenerates:
  • Counter_melody: 35 notes (increased density)
→ Re-checks quality
```

**[5] Quality Control (2nd pass)**
```
→ Assessment:
  • Score: 0.92/1.0
  • Positive: Good track diversity, Good velocity variation
  • Refinement needed: NO
```

**[7] MIDI Creator**
```
→ Creates MIDI file:
  • File: midigen_cinematic_a1b2c3d4_20260208_123456.mid
  • Tracks: 6 (+ tempo track)
  • Duration: 16 bars at 90 BPM
```

**[8] Session Summary**
```
→ Summary:
## Composition Summary
**Action:** New
**Genre:** Cinematic
...
✅ **MIDI file ready for download!**
```

## Key Improvements

### 1. Autonomous Decision Making
- Agents decide routing (not hard-coded)
- Quality agent determines refinement
- Theory validator guides corrections

### 2. Self-Reflection
- Quality assessment after generation
- Automatic refinement if issues detected
- Max iterations prevent infinite loops

### 3. Extensibility
- Add new agents by creating new nodes
- Modify routing logic independently
- Swap out agents (e.g., different LLM for intent parsing)

### 4. Observability
- Full state visible at each step
- Agent reasoning printed to console
- State persisted across sessions (with SQLite checkpointer upgrade)

### 5. Error Resilience
- Errors propagated cleanly through state
- Graceful degradation (fallbacks built-in)
- Specific error messages in user response

### 6. Memory & Persistence
- Thread-ID based session management
- Can upgrade to SQLite for persistence
- Full conversation history maintained

## Migration Checklist

If you want to make `app_langgraph.py` your primary app:

- [ ] Test with various user inputs (simple, complex, multi-turn)
- [ ] Verify MIDI output quality matches original
- [ ] Check agent console output for debugging
- [ ] Upgrade from `MemorySaver` to `SqliteSaver` for persistence
- [ ] Add custom agents for specific use cases
- [ ] Rename `app_langgraph.py` → `app.py` when satisfied

## Future Enhancements

### Immediate
- [ ] Add human-in-the-loop approval points before MIDI creation
- [ ] Implement parallel track generation (LangGraph can do this!)
- [ ] Add agent feedback mechanism for continuous improvement

### Medium-term
- [ ] SQLite checkpointing for session persistence
- [ ] Custom tools for agents (music theory, DSP operations)
- [ ] Multi-user support with thread isolation
- [ ] Streaming agent output to UI

### Long-term
- [ ] Mastering agent (EQ, compression, dynamics)
- [ ] Mixing agent (balance, panning, effects)
- [ ] Arrangement agent (intro/verse/chorus structure)
- [ ] Neural network-based quality assessment

## Troubleshooting

### Graph Doesn't Invoke
**Error:** `"No node 'intent_parser' found"`
- **Cause:** Incorrect import in graph.py
- **Fix:** Verify all agent nodes are added to graph

### State Type Errors
**Error:** `"extra fields not permitted"`
- **Cause:** TypedDict strict type checking
- **Fix:** Check MusicState definition, ensure all fields are defined

### Import Circular Dependency
**Error:** `"cannot import name 'MusicGenerator' from 'app'"`
- **Cause:** Circular imports between app.py and agents/
- **Fix:** Move classes to separate utility modules

### Agents Not Running
**Error:** `"AttributeError: 'NoneType' object has no attribute..."`
- **Cause:** Agent tried to access None from previous state
- **Fix:** Check error handling in agent node, add null checks

## Documentation Files

- **AGENTS.md**: General agent integration guide (GitHub Spec Kit)
- **MIGRATION.md**: This file - LangGraph migration specifics
- **src/agents/graph.py**: Contains `describe_graph()` for visual overview
- **app_langgraph.py**: Well-commented implementation

## Contact & Support

For issues:
1. Check console output from agent nodes
2. Run `python -c "from src.agents.graph import describe_graph; print(describe_graph())"`
3. Review error trace in MusicState.error field
4. Check LangGraph documentation: https://github.com/langchain-ai/langgraph

## References

- **LangGraph**: https://github.com/langchain-ai/langgraph
- **LangChain**: https://python.langchain.com
- **Groq API**: https://console.groq.com
- **Music21**: https://web.mit.edu/music21/
- **mido**: https://mido.readthedocs.io

---

**Version:** 2.0 (LangGraph Agentic)  
**Last Updated:** 2026-02-08  
**Status:** Production Ready
