# Quick Start: LangGraph Agentic MidiGen

## Installation

```bash
# Update dependencies
pip install -r requirements.txt

# Or specifically for LangGraph:
pip install langgraph>=0.1.0 langchain>=0.1.0 langchain-groq>=0.1.0
```

## Running the Agentic Version

```bash
# Start the LangGraph-based app
python app_langgraph.py
```

**Output:**
```
======================================================================
🎵 MidiGen v2.0 - Agentic Architecture (LangGraph)
======================================================================

╔════════════════════════════════════════════════════════════════╗
║         MidiGen Agentic Architecture (LangGraph)              ║
╚════════════════════════════════════════════════════════════════╝

WORKFLOW PHASES:
═══════════════════════════════════════════════════════════════

1️⃣  UNDERSTANDING
   └─ intent_parser: Parse user request...
   
[... more workflow description ...]

Open browser to http://localhost:7860
```

## Example Interactions

### 1. Simple Request
```
User: "Create a solo piano piece"

🧠 [INTENT AGENT] → Parsed: new, classical, piano, 1-2 tracks
🎵 [TRACK PLANNER] → 1 track: piano (lead)
🎼 [THEORY VALIDATOR] → ✓ Valid
🎹 [TRACK GENERATOR] → Generated 45 notes
📊 [QUALITY CONTROL] → Score 0.88/1.0 ✓ Acceptable
💾 [MIDI CREATOR] → Saved midigen_classical_a1b2c3d4_20260208_120000.mid
📝 [SESSION SUMMARY] → Ready for download!
```

### 2. Complex Request with Refinement
```
User: "Epic orchestral arrangement with 6 tracks"

[Intent Parser] → 6 tracks requested
[Track Planner] → Plans: strings, brass, choir, piano, bass, drums
[Theory Validator] → ✓ Valid orchestration
[Track Generator] → 6 tracks generated
[Quality Control] → Score 0.72/1.0 ⚠️ Issues found
[Refinement Agent] → Regenerating sparse tracks...
[Quality Control] → Score 0.91/1.0 ✓ Acceptable
[MIDI Creator] → Saved with refinements
[Session Summary] → Epic composition ready!
```

### 3. Multi-turn Composition
```
User 1: "Create a lo-fi beat"
→ [Agents process] → 4 tracks generated

User 2: "Add more bars"
→ [Intent Parser] → Detects "extend" action
→ [Track Generator] → Extends existing tracks
→ Result: 32 bars total

User 3: "Make the drums louder"
→ [Intent Parser] → Detects "modify" action
→ [Refinement] → Adjusts drum velocities
→ Result: Enhanced drums
```

## Agent Console Output

When you run the app, you'll see detailed agent logging:

```
🎯 New session: a1b2c3d4

======================================================================
📨 User: Create a peaceful ambient soundscape...
======================================================================

🧠 [INTENT AGENT] Analyzing user request...
✅ Intent parsed: new ambient | Tracks: None | Energy: low

🎵 [TRACK PLANNER AGENT] Planning track configuration...
✓ Track plan created: 3 tracks
   1. pad              | synth_pad            | Priority: 1
   2. strings          | strings              | Priority: 2
   3. fx_atmosphere    | fx_atmosphere        | Priority: 3

🎼 [MUSIC THEORY VALIDATOR] Validating musical choices...
✅ All music theory checks passed

🎹 [TRACK GENERATOR] Generating musical tracks...
   Generating 3 tracks...
   [1/3] pad (synth_pad)
   [2/3] strings (strings)
   [3/3] fx_atmosphere (fx_atmosphere)
✅ Generated 3 tracks

📊 [QUALITY CONTROL] Assessing track quality...
✅ Quality score: 0.87/1.0
   Positive: Good track type diversity
   Issues: Limited velocity variation
   → Refinement recommended

🔧 [REFINEMENT AGENT] Refining tracks...
   Regenerating track 0: pad
✅ Refinement applied (iteration 1)

📊 [QUALITY CONTROL] Assessing track quality...
✅ Quality score: 0.93/1.0
   Positive: Good track type diversity, Good velocity variation
   → Quality acceptable

💾 [MIDI CREATOR] Creating final MIDI file...
✅ MIDI saved: midigen_ambient_a1b2c3d4_20260208_120000.mid
   Tracks: 3
   Tempo: 65 BPM
   Duration: 16 bars

📝 [SESSION SUMMARY] Generating summary...
✅ Summary generated
```

## Understanding the Agent Output

Each agent logs its activities with emoji indicators:

| Icon | Meaning |
|------|---------|
| 🧠 | Intent understanding |
| 🎵 | Track planning |
| 🎼 | Theory validation |
| 🎹 | Track generation |
| 📊 | Quality assessment |
| 🔧 | Refinement |
| 💾 | MIDI creation |
| 📝 | Summary generation |
| ✅ | Success |
| ⚠️ | Warning |
| ❌ | Error |
| 🔄 | Routing decision |

## Monitoring Agent Decisions

### Check Quality Scores
```
Quality score: 0.87/1.0
```
- **0.7-1.0**: Acceptable (may refine)
- **0.6-0.7**: Needs refinement
- **<0.6**: Multiple issues

### Refinement Loop
```
If quality < threshold AND iterations < max:
  → Trigger refinement
  → Regenerate problematic tracks
  → Re-assess quality
```

Maximum iterations: 2 (prevents infinite loops)

### Routing Decisions
```
🔄 [ROUTER] Quality issues detected → Refinement (iteration 1)
or
🔄 [ROUTER] Quality acceptable → Finalizing
```

## File Locations

```
app_langgraph.py                    ← Main agentic app
src/agents/
├── __init__.py
├── state.py                        ← State definitions
├── nodes.py                        ← Agent implementations
├── graph.py                        ← Graph builder + routing
└── MIGRATION.md                    ← Detailed documentation

outputs/
└── midigen_*.mid                   ← Generated MIDI files
```

## Customizing Agents

### Modify Track Planner
Edit `src/agents/nodes.py`:
```python
def track_planner_node(state: MusicState) -> MusicState:
    # Customize track planning logic here
    intent = state.get("intent")
    track_plan = _plan_tracks_with_ai(intent)
    state["track_plan"] = track_plan
    return state
```

### Adjust Quality Thresholds
In `quality_control_agent_node()`:
```python
needs_refinement = (
    any(issue.severity == "high" for issue in issues) or
    overall_score < 0.6  # Adjust this threshold
) a++nd current_iteration < max_iterations
```

### Add New Agents
1. Create node function in `src/agents/nodes.py`
2. Add node to graph in `src/agents/graph.py`
3. Add edges to define routing
4. Update state if needed

## Troubleshooting

### "ModuleNotFoundError: No module named 'src.agents'"
```bas , m



0h
# Make sure you're running from project root
pwd  # Should be .../spec-kit/
python app_langgraph.py
```

### "Groq API Error"
```python
# Set API key in .env:
GROQ_API_KEY=gsk_your_key_here
```

### "ImportError: cannot import name 'MusicGenerator'"
```bash
# Restart Python, clear cache:
rm -rf __pycache__ src/__pycache__ src/agents/__pycache__
python app_langgraph.py
```

### MIDI File Not Generated
- Check `outputs/` directory exists
- Look for error in agent console output
- Verify track generation completed successfully

## Performance Notes

- **Intent Parsing**: ~1-2s (if using Groq LLM)
- **Track Planning**: ~0.5s (quick with rules-based)
- **Generation**: ~0.5-1s per track
- **Quality Check**: ~0.1s
- **Refinement**: ~0.5-1s (if triggered)
- **MIDI Creation**: ~0.1s

**Total for simple request:** ~3-4 seconds  
**Total with refinement:** ~5-6 seconds

## Next Steps

1. ✅ Run `python app_langgraph.py`
2. 📝 Test with various prompts (simple, complex, multi-turn)
3. 📊 Watch agent console output to understand reasoning
4. 🔧 Customize agents for your needs
5. 📚 Read [MIGRATION.md](./MIGRATION.md) for detailed architecture

## Architecture Summary

```
User Input
    ↓
[Agentic Graph]
├─ Intent Parser (understand)
├─ Track Planner (plan)
├─ Theory Validator (validate)
├─ Track Generator (generate)
├─ Quality Control (assess)
├─ ↻ Refinement Loop (if needed)
├─ MIDI Creator (output)
└─ Session Summary (report)
    ↓
MIDI File + Response
```

## Key Improvements Over Monolithic

| Feature | Monolithic | Agentic |
|---------|-----------|---------|
| Separation of Concerns | Limited | ✅ 8 agents |
| Self-Reflection | None | ✅ Quality-driven |
| Error Recovery | Basic | ✅ Graceful |
| Extensibility | Hard | ✅ Easy |
| State Visibility | Implicit | ✅ Full |
| Debugging | Difficult | ✅ Observable |
| Testability | Coupled | ✅ Independent |

---

**Happy composing! 🎵**

For more info, see [MIGRATION.md](./MIGRATION.md)
