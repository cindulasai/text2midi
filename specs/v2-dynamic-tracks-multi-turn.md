# MidiGen v2.0 - Dynamic Tracks & Multi-Turn Conversations

## Overview

Enhancement specification for intelligent track generation and conversational MIDI composition workflow.

---

## Feature 1: Dynamic Track Generation (1-8 tracks)

### Problem Statement
Current system generates fixed 3-4 tracks (melody, chords, bass, drums) regardless of user intent. This limits creative expression and doesn't adapt to the musical complexity implied by the prompt.

### Solution
LLM-powered track planning that analyzes the prompt to determine:
- How many tracks are needed (1-8 max)
- What type of tracks (lead, harmony, rhythm, texture, effects)
- Instrument selection for each track
- Track relationships and layering

### Track Types Available
| Track Type | Purpose | Example Instruments |
|------------|---------|---------------------|
| Lead/Melody | Primary melodic content | Piano, Synth Lead, Guitar, Flute |
| Counter-Melody | Secondary melodic line | Strings, Vibraphone, Clarinet |
| Harmony/Chords | Harmonic foundation | Electric Piano, Organ, Pad |
| Bass | Low-end foundation | Bass, Synth Bass |
| Drums/Percussion | Rhythmic foundation | Drum Kit, Percussion |
| Arpeggio | Rhythmic melodic texture | Synth, Harp, Marimba |
| Pad/Atmosphere | Sustained texture | Synth Pad, Strings, Choir |
| Effects/FX | Sonic embellishment | Synth Effects, Bells |

### AI Track Planning Prompt
```
Analyze this music request and determine the optimal track configuration:
"{user_prompt}"

Return JSON with:
{
  "total_tracks": <1-8>,
  "tracks": [
    {
      "type": "<lead|counter_melody|harmony|bass|drums|arpeggio|pad|fx>",
      "instrument": "<GM instrument name>",
      "role": "<description of this track's purpose>",
      "priority": <1-8, 1 being most important>
    }
  ],
  "reasoning": "<why this configuration fits the request>"
}

Rules:
- Simple requests (solo piano) = 1-2 tracks
- Standard pop/rock = 4-5 tracks  
- Rich orchestral/electronic = 6-8 tracks
- Never exceed 8 tracks
- Always consider genre conventions
```

### Implementation Changes
1. Update `IntentParser` to include track planning
2. Create `TrackPlanner` class to manage track configuration
3. Modify `MidiGenApp.process_message()` to use dynamic tracks
4. Add new generator methods for counter-melody, arpeggio, pad

---

## Feature 2: Multi-Turn Conversation & Session Management

### Problem Statement
Each generation is stateless. Users cannot:
- Build upon previous generations
- Modify existing tracks
- Create continuous compositions
- Reference earlier context

### Solution
Session-based composition with conversation memory and MIDI state management.

### Conversation Modes

#### Mode 1: Extend Current Composition
User continues building on the same piece.
- "Now add some strings"
- "Make the drums more intense"
- "Add 16 more bars with a key change"

#### Mode 2: Modify Existing Track
User wants to change something already generated.
- "Make the bass line funkier"
- "Change the melody to minor key"
- "Slow down the tempo"

#### Mode 3: Fresh Start (Same Session)
User wants something new but related.
- "Now create a B section"
- "Make a contrasting verse"
- "Create the chorus version"

#### Mode 4: Complete Reset
User starts fresh composition.
- "Start over"
- "New song"
- "Forget that, let's make something different"

### Session State Schema
```python
@dataclass
class CompositionSession:
    session_id: str
    created_at: datetime
    
    # Current composition state
    tracks: List[Track]
    tempo: int
    key: str
    mode: str
    genre: str
    total_bars: int
    
    # Conversation history for context
    messages: List[Dict[str, str]]
    
    # Generation history (for undo/reference)
    generations: List[GenerationSnapshot]
    
    # User preferences learned during session
    preferences: Dict[str, Any]
```

### AI Context Prompt for Multi-Turn
```
You are continuing a music composition session.

CURRENT COMPOSITION STATE:
- Genre: {genre}
- Key: {key} {mode}
- Tempo: {tempo} BPM
- Current Duration: {bars} bars
- Active Tracks: {track_summary}

CONVERSATION HISTORY:
{previous_messages}

NEW USER REQUEST:
"{user_message}"

Determine the action type and parameters:
{
  "action": "<extend|modify|section|reset>",
  "target_tracks": [<track indices to modify, or "all", or "new">],
  "changes": {
    "tempo_change": <null or new tempo>,
    "key_change": <null or new key>,
    "bars_to_add": <0 or number>,
    "energy_shift": <null or "increase"|"decrease">,
    "mood_shift": <null or new mood descriptor>
  },
  "new_elements": [<list of new tracks/instruments to add>],
  "reasoning": "<interpretation of user intent>"
}
```

### UI Enhancements for Multi-Turn
1. **Session Panel**: Shows current composition state
2. **Track List**: Visual list of active tracks with mute/solo hints
3. **Timeline Indicator**: Shows current duration
4. **Export Options**: 
   - Export current state
   - Export specific section
   - Export individual tracks

---

## Feature 3: Intelligent Musical Intuition (Bonus)

### Auto-Suggested Enhancements
After each generation, suggest logical next steps:
- "Add a bridge section?"
- "Try a key change to relative minor?"
- "Add string accompaniment?"
- "Create a stripped-down breakdown?"

### Musical Coherence Engine
- Maintain consistent harmonic language across turns
- Ensure smooth transitions between sections
- Auto-adjust velocity curves for dynamic flow
- Smart instrument doubling suggestions

### Variation Generation
- "Create 3 variations of this melody"
- "Generate alternative chord voicings"
- "Try different drum patterns"

---

## Technical Implementation Plan

### Phase 1: Dynamic Track Planning
1. Create `TrackPlanner` class
2. Extend AI prompt for track analysis
3. Add new generator methods (counter_melody, arpeggio, pad)
4. Update `process_message()` to use planned tracks

### Phase 2: Session Management
1. Create `CompositionSession` dataclass
2. Implement session storage (in-memory for MVP)
3. Add session state to UI
4. Modify AI prompts to include context

### Phase 3: Multi-Turn Actions
1. Implement action detection (extend/modify/section/reset)
2. Create track modification methods
3. Add MIDI merging/extension logic
4. Implement section management

### Phase 4: UI Polish
1. Add session state display
2. Track list visualization
3. Suggested actions panel
4. Export options

---

## Success Criteria

1. **Dynamic Tracks**: "solo piano piece" generates 1-2 tracks; "epic orchestral" generates 6-8 tracks
2. **Context Awareness**: Second prompt correctly builds on first
3. **Track Modification**: "make drums louder" affects only drums
4. **Section Creation**: "add a chorus" creates connected section
5. **Reset Detection**: "new song" clears session properly

---

## API Changes

### New IntentParser Response
```python
{
  "genre": str,
  "mood": str,
  "tempo": int,
  "key": str,
  "energy": str,
  "duration_bars": int,
  # NEW FIELDS
  "track_plan": {
    "total_tracks": int,
    "tracks": List[TrackConfig]
  },
  "action": str,  # extend|modify|section|reset|new
  "target_tracks": List[int],
  "modifications": Dict
}
```

### New Session Endpoints
- `create_session()` - Initialize new composition
- `get_session_state()` - Current composition info
- `extend_composition()` - Add to existing
- `modify_tracks()` - Change existing tracks
- `reset_session()` - Start fresh
