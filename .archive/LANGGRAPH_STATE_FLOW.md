# LangGraph State Flow Visualization

## Complete Request Lifecycle

```
┌─────────────────────────────────────────────────────────────┐
│                      USER INPUT                             │
│        "Create a peaceful ambient soundscape"               │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
        ┌──────────────────────────────┐
        │  [1] INTENT PARSER AGENT     │
        ├──────────────────────────────┤
        │ Input:  user_prompt          │
        │ Output: MusicIntent          │
        │         - action: "new"      │
        │         - genre: "ambient"   │
        │         - energy: "low"      │
        │         - track_count: None  │
        └──────────────────────────────┘
                       │
                       ▼
        ┌──────────────────────────────┐
        │  [2] TRACK PLANNER AGENT     │
        ├──────────────────────────────┤
        │ Input:  intent               │
        │ Output: track_plan (3 items) │
        │         - pad (synth_pad)    │
        │         - strings            │
        │         - fx_atmosphere      │
        └──────────────────────────────┘
                       │
                       ▼
        ┌──────────────────────────────┐
        │  [3] THEORY VALIDATOR        │
        ├──────────────────────────────┤
        │ Input:  intent, track_plan   │
        │ Output: validation_report    │
        │         - theory_valid: True │
        │         - theory_issues: [] │
        └──────────────────────────────┘
                       │
                       ▼
        ┌──────────────────────────────┐
        │  [4] TRACK GENERATOR         │
        ├──────────────────────────────┤
        │ Input:  track_plan, intent   │
        │ Output: generated_tracks     │
        │         - 3 tracks with      │
        │         - MIDI notes         │
        └──────────────────────────────┘
                       │
                       ▼
        ┌──────────────────────────────┐
        │  [5] QUALITY CONTROL         │
        ├──────────────────────────────┤
        │ Input:  generated_tracks     │
        │ Output: quality_report       │
        │         - score: 0.87/1.0    │
        │         - issues: 1 found    │
        │         - needs_refinement:T │
        └──────────────────────────────┘
                       │
        ┌──────────────┴──────────────┐
        │   CONDITIONAL ROUTING        │
        └──────────────┬──────────────┘
                       │
           ┌───────────┴───────────┐
           │                       │
    needs_refinement=T   needs_refinement=F
    iterations < 2       OR iterations >= 2
           │                       │
           ▼                       ▼
        ┌──────────────┐      ┌──────────────────────┐
        │  REFINEMENT  │      │ [7] MIDI CREATOR     │
        │    AGENT     │      ├──────────────────────┤
        │              │      │ Input: tracks        │
        │ Regenerates  │      │ Output: final_path   │
        │ problematic  │      │ ./outputs/midigen... │
        │    tracks    │      │                      │
        └──────────────┘      └──────────────────────┘
           │                           │
           │                           ▼
           │                  ┌──────────────────────┐
           │                  │ [8] SESSION SUMMARY  │
           │                  ├──────────────────────┤
           │                  │ Input: all state     │
           │ (Re-check)       │ Output: summary_text │
           │                  │  Markdown format     │
           └─────────────────→│  Ready for download! │
                              └──────────────────────┘
                                      │
                                      ▼
                              ┌──────────────────────┐
                              │   RESPONSE TO USER   │
                              │                      │
                              │ MIDI file path       │
                              │ Summary text         │
                              │ Quality metrics      │
                              └──────────────────────┘
```

## State Transformations

### Step 1: Intent Parsing
```
MusicState before:
{
  "user_prompt": "Create a peaceful ambient soundscape",
  "intent": None,
  ...
}
        ↓ [Intent Parser Node]
MusicState after:
{
  "user_prompt": "Create a peaceful ambient soundscape",
  "intent": MusicIntent(
    action="new",
    genre="ambient",
    energy="low",
    track_count=None,
    ...
  ),
  ...
}
```

### Step 2: Track Planning
```
MusicState:
{
  "intent": MusicIntent(...),
  "track_plan": [],
  ...
}
        ↓ [Track Planner Node]
MusicState:
{
  "intent": MusicIntent(...),
  "track_plan": [
    TrackConfig(track_type="pad", instrument="synth_pad", ...),
    TrackConfig(track_type="strings", instrument="strings", ...),
    TrackConfig(track_type="fx", instrument="fx_atmosphere", ...),
  ],
  ...
}
```

### Step 3: Theory Validation
```
MusicState:
{
  "track_plan": [...],
  "theory_valid": False,
  "theory_issues": [],
  ...
}
        ↓ [Music Theory Validator Node]
MusicState:
{
  "track_plan": [...],
  "theory_valid": True,
  "theory_issues": [],
  "theory_validation": {
    "genre": "ambient",
    "has_melody": True,
    "has_harmony": True,
    ...
  },
  ...
}
```

### Step 4: Track Generation
```
MusicState:
{
  "generated_tracks": [],
  "generation_metadata": {},
  ...
}
        ↓ [Track Generator Node]
MusicState:
{
  "generated_tracks": [
    Track(name="Pad (synth_pad)", notes=[Note(...), ...], ...),
    Track(name="Strings", notes=[Note(...), ...], ...),
    Track(name="FX (fx_atmosphere)", notes=[Note(...), ...], ...),
  ],
  "generation_metadata": {
    "root": "C",
    "mode": "major",
    "bars": 16,
    "energy": "low",
    "genre": "ambient"
  },
  ...
}
```

### Step 5: Quality Assessment
```
MusicState:
{
  "quality_report": None,
  "needs_refinement": False,
  ...
}
        ↓ [Quality Control Node]
MusicState:
{
  "quality_report": GenerationQualityReport(
    overall_score=0.87,
    issues=[
      TrackQualityIssue(
        track_index=1,
        issue_type="density",
        severity="low",
        description="Limited velocity variation",
        ...
      )
    ],
    needs_refinement=True,
    refinement_suggestions=[...],
    positive_aspects=["Good track diversity"]
  ),
  "needs_refinement": True,
  ...
}
```

### Step 6a: Quality Routing (Needs Refinement)
```
MusicState:
{
  "needs_refinement": True,
  "current_iteration": 0,
  "max_refinement_iterations": 2
}
        ↓ quality_control_router()
Decision: "refine"  (because needs_refinement AND iterations < max)
        ↓
Route to Refinement Agent
```

### Step 6b: Refinement (If Needed)
```
MusicState:
{
  "generated_tracks": [original tracks],
  "current_iteration": 0,
  ...
}
        ↓ [Refinement Agent Node]
MusicState:
{
  "generated_tracks": [regenerated tracks],
  "refinement_attempts": 1,
  "current_iteration": 1,
  "refinement_feedback": "Applied refinements (iteration 1)",
  ...
}
        ↓ refinement_router()
Decision: "recheck" (because iteration 1 < max 2)
        ↓
Loop back to Quality Control Node
```

### Step 7: MIDI Creation
```
MusicState:
{
  "generated_tracks": [finalized tracks],
  "final_midi_path": None,
  ...
}
        ↓ [MIDI Creator Node]
MusicState:
{
  "generated_tracks": [same tracks],
  "final_midi_path": "./outputs/midigen_ambient_a1b2c3d4_20260208_120000.mid",
  ...
}
```

### Step 8: Session Summary
```
MusicState:
{
  "final_midi_path": "./outputs/...",
  "quality_report": GenerationQualityReport(...),
  "generated_tracks": [3 tracks],
  "session_summary": ""
  ...
}
        ↓ [Session Summary Node]
MusicState:
{
  ...same as above...
  "session_summary": """
## Composition Summary
**Action:** New
**Genre:** Ambient
**Total Tracks:** 3
**Duration:** 16 bars
**Tempo:** 65 BPM
**Key:** C major

**Quality Score:** 0.93/1.0

✅ **MIDI file ready for download!**
  """,
}
```

## Conditional Routing Logic

### Quality Control Router
```python
def quality_control_router(state: MusicState) -> Literal["refine", "finalize"]:
    
    if state.get("error"):
        return "finalize"  # On error, skip to end
    
    needs_refinement = state.get("needs_refinement", False)
    current_iteration = state.get("current_iteration", 0)
    max_iterations = state.get("max_refinement_iterations", 2)
    
    if needs_refinement and current_iteration < max_iterations:
        print(f"Quality issues detected → Refinement (iteration {current_iteration + 1})")
        return "refine"
    else:
        print("Quality acceptable or max iterations reached → Finalizing")
        return "finalize"
```

**Decision Matrix:**
| Needs Refinement | Iteration | Max | Decision |
|-----------------|-----------|-----|----------|
| False | 0 | 2 | → finalize |
| True | 0 | 2 | → refine |
| True | 1 | 2 | → refine |
| True | 2 | 2 | → finalize |
| Any | Any | Reached | → finalize |

### Refinement Router
```python
def refinement_router(state: MusicState) -> Literal["recheck", "finalize"]:
    
    current_iteration = state.get("current_iteration", 0)
    max_iterations = state.get("max_refinement_iterations", 2)
    
    if current_iteration < max_iterations:
        print("Rechecking refined tracks...")
        return "recheck"  # Loop back to quality control
    else:
        print("Max iterations reached → Creating MIDI")
        return "finalize"  # Skip to MIDI creation
```

**Decision Matrix:**
| Current Iteration | Max | Decision |
|-------------------|-----|----------|
| 0 | 2 | → recheck |
| 1 | 2 | → recheck |
| 2 | 2 | → finalize |

## Parallel Execution Opportunities

These agents could run in parallel (LangGraph supports this):

```
Parallel Possible:
  [Track Generator] can generate multiple tracks simultaneously
  [Refinement] could fix multiple tracks at once
  
Current Implementation:
  Sequential for simplicity, but architecture supports parallelization
  
Future Upgrade:
  graph.add_edge("track_planner", "generate_track_1")
  graph.add_edge("track_planner", "generate_track_2")
  graph.add_edge("track_planner", "generate_track_3")
  graph.add_edge("generate_track_1", "merge_tracks")
  graph.add_edge("generate_track_2", "merge_tracks")
  graph.add_edge("generate_track_3", "merge_tracks")
```

## Error Handling Flow

```
Any Node Error:
    ↓
state["error"] = "descriptive message"
    ↓
Next node checks: if state.get("error"): return state (skip processing)
    ↓
Propagates through graph
    ↓
Session Summary (or any later node) creates error response
    ↓
User sees: "❌ Error: [message]"
```

## State Checkpoint Points

With SQLite Checkpointer (future upgrade):

```
checkpoint_id_1: After Intent Parser
checkpoint_id_2: After Track Planner
checkpoint_id_3: After Theory Validator
checkpoint_id_4: After Track Generator
checkpoint_id_5: After Quality Control
  ├─ If refine → checkpoint_id_6: After Refinement
  │  └─ Recheck → checkpoint_id_5: Quality Control again
  └─ If finalize → checkpoint_id_7: After MIDI Creator
checkpoint_id_8: After Session Summary

Can resume from any checkpoint!
```

## Memory Management

```
MemorySaver (current):
  └─ In-memory storage
  └─ Lost on process restart
  └─ Perfect for development

SqliteSaver (recommended for production):
  └─ File-based persistence
  └─ Survives process restart
  └─ Can query history
  └─ Thread-safe with multiple users
```

---

This visualization shows how LangGraph orchestrates the agents and manages state transformations throughout the composition process.
