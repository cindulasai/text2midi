# MidiGent V2 - Agentic Generation Implementation Plan

**Spec Reference**: [`midigent-v2-agentic-generation-spec.md`](../specs/midigent-v2-agentic-generation-spec.md)  
**Created**: January 31, 2026  
**Status**: Ready to Implement  

---

## Overview

Complete architectural rewrite of MidiGent to fix the critical randomization bug and implement true agentic music generation. This plan preserves all V1 features while adding intelligent variation and agent-based composition.

---

## Phase 1: Critical Foundation (Day 1-2)

### 1.1 Variation Engine Implementation ⚠️ HIGHEST PRIORITY
**Why First**: This fixes the showstopper bug where all generations are identical.

**Tasks**:
- [ ] Create `src/midigent/variation_engine.py`
- [ ] Implement `VariationEngine` class with proper seeding
- [ ] Add `initialize_generation()` method (time_ns + session_id + counter)
- [ ] Add `get_variation_factor()` for controlled randomization
- [ ] Add `choose_weighted()` for better random selection
- [ ] Add `should_trigger()` for probability-based decisions
- [ ] Write unit tests for seed uniqueness
- [ ] Test: 1000 generations → 1000 unique seeds

**Success Criteria**: Same prompt generates different music every time.

---

### 1.2 Fix Track Count Bug ⚠️ HIGHEST PRIORITY
**Why First**: Users requesting "5 tracks" get only 1 track - critical functionality broken.

**Tasks**:
- [ ] Add debug logging to `_generate_tracks_from_plan()` method
- [ ] Verify `track_plan` list contains correct number of configs
- [ ] Ensure loop iterates over ALL track configs
- [ ] Verify ALL tracks appended to tracks list
- [ ] Add validation: `assert len(tracks) == len(track_plan)`
- [ ] Fix any track loss in MIDI assembly
- [ ] Test: Request 7 tracks → Get 7 tracks in output

**Success Criteria**: Requested track count matches generated count 100%.

---

### 1.3 Session ID Management
**Why Now**: Required for variation engine seeding.

**Tasks**:
- [ ] Add `session_id` generation in `MidiGenApp.__init__()`
- [ ] Use `uuid.uuid4()` for unique session IDs
- [ ] Pass `session_id` to `VariationEngine`
- [ ] Display session ID in UI
- [ ] Test: Each app instance has unique session

**Success Criteria**: Every session has unique ID.

---

## Phase 2: Agentic Architecture (Day 3-5)

### 2.1 Base Agent Framework
**Why Now**: Foundation for all intelligent generators.

**Tasks**:
- [ ] Create `src/midigent/agents/__init__.py`
- [ ] Create `src/midigent/agents/base.py` with `TrackAgent` abstract class
- [ ] Implement `generate()` abstract method
- [ ] Implement `get_musical_context()` helper
- [ ] Add agent memory (dict for working memory)
- [ ] Test: Base class can be subclassed

**Success Criteria**: Agent framework ready for implementation.

---

### 2.2 MelodyAgent Implementation
**Why Now**: Most complex agent - melody with motif development.

**Tasks**:
- [ ] Create `src/midigent/agents/melody_agent.py`
- [ ] Implement `MelodyAgent(TrackAgent)`
- [ ] Implement `_create_motif()` (2-4 note pattern)
- [ ] Implement `_repeat_motif()` (exact repetition)
- [ ] Implement `_transpose_motif()` (musical transposition)
- [ ] Implement `_vary_rhythm()` (rhythmic variation)
- [ ] Implement `_create_new_phrase()` (contrast)
- [ ] Implement `_add_phrasing()` (musical expression)
- [ ] Test: Melody has recognizable motif repetition

**Success Criteria**: Melodies sound composed, not random.

---

### 2.3 BassAgent Implementation
**Why Now**: Must follow harmony intelligently.

**Tasks**:
- [ ] Create `src/midigent/agents/bass_agent.py`
- [ ] Implement `BassAgent(TrackAgent)`
- [ ] Implement `_walking_bass()` (active pattern)
- [ ] Implement `_simple_bass()` (root notes)
- [ ] Implement chord progression following
- [ ] Add energy-based pattern selection
- [ ] Test: Bass follows chord roots correctly

**Success Criteria**: Bass provides solid harmonic foundation.

---

### 2.4 DrumAgent Implementation
**Why Now**: Context-adaptive rhythms essential for variation.

**Tasks**:
- [ ] Create `src/midigent/agents/drum_agent.py`
- [ ] Implement `DrumAgent(TrackAgent)`
- [ ] Implement `_simple_pattern()` (low energy)
- [ ] Implement `_standard_pattern()` (medium energy)
- [ ] Implement `_complex_pattern()` (high energy)
- [ ] Implement `_create_fill()` (section transitions)
- [ ] Add hihat velocity variation
- [ ] Test: Drum patterns adapt to section energy

**Success Criteria**: Drums sound natural with variations.

---

### 2.5 HarmonyAgent Implementation
**Why Now**: Chord progressions with voice leading.

**Tasks**:
- [ ] Create `src/midigent/agents/harmony_agent.py`
- [ ] Implement `HarmonyAgent(TrackAgent)`
- [ ] Implement voice leading logic
- [ ] Implement chord inversion selection
- [ ] Implement sustain vs arpeggiated patterns
- [ ] Test: Chord voicings sound natural

**Success Criteria**: Harmonies follow musical rules.

---

### 2.6 Additional Agents
**Why Now**: Complete the agent ecosystem.

**Tasks**:
- [ ] Create `ArpeggioAgent` (rhythmic melodic patterns)
- [ ] Create `PadAgent` (sustained atmospheric textures)
- [ ] Create `CounterMelodyAgent` (complementary melodies)
- [ ] Test: All agents produce coherent output

**Success Criteria**: Full range of track types available.

---

## Phase 3: Integration (Day 6-7)

### 3.1 Integrate Variation Engine
**Why Now**: All components ready for integration.

**Tasks**:
- [ ] Import `VariationEngine` in `app.py`
- [ ] Create `variation_engine` instance in `__init__()`
- [ ] Call `variation_engine.initialize_generation()` before each generation
- [ ] Pass `variation_engine` to all generators
- [ ] Replace all `random.*` calls with `variation.*` calls
- [ ] Test: Generations use properly seeded randomness

**Success Criteria**: All randomness controlled by variation engine.

---

### 3.2 Integrate Agents
**Why Now**: Replace old generators with intelligent agents.

**Tasks**:
- [ ] Create agent instances in `_generate_tracks_from_plan()`
- [ ] Map track types to agents (lead→MelodyAgent, bass→BassAgent, etc.)
- [ ] Pass context dicts to `agent.generate()`
- [ ] Integrate agent output into track creation
- [ ] Test: Multi-track generation uses agents

**Success Criteria**: All tracks generated by agents.

---

### 3.3 Preserve V1 Features
**Why Now**: Must not lose existing functionality.

**Tasks**:
- [ ] Verify duration parser still works
- [ ] Verify cultural knowledge base integrated
- [ ] Verify humanization engine applied
- [ ] Verify section structure generation works
- [ ] Test: All V1 features functional in V2

**Success Criteria**: Zero V1 features broken.

---

## Phase 4: Testing & Validation (Day 8-9)

### 4.1 Uniqueness Testing
**Why Now**: Verify randomization fix works.

**Tasks**:
- [ ] Generate same prompt 10 times
- [ ] Compute edit distance between outputs
- [ ] Verify >30% difference between any two outputs
- [ ] Test across different prompt types
- [ ] Test with app restarts (not cached randomness)

**Success Criteria**: All outputs measurably unique.

---

### 4.2 Track Count Validation
**Why Now**: Verify track count bug fixed.

**Tasks**:
- [ ] Test requesting 1, 2, 3, 4, 5, 6, 7, 8 tracks
- [ ] Verify each produces exact count requested
- [ ] Test edge case: request 15 tracks (should cap at 8)
- [ ] Verify all tracks present in MIDI file
- [ ] Use MIDI analysis tools to count tracks

**Success Criteria**: 100% accuracy on track count.

---

### 4.3 Cultural Music Testing
**Why Now**: Verify V1 feature preserved.

**Tasks**:
- [ ] Test "Japanese traditional music"
- [ ] Test "Carnatic music"
- [ ] Test "Sufi music"
- [ ] Test "Irish folk music"
- [ ] Test "Brazilian samba"
- [ ] Verify instruments, scales, rhythms culturally appropriate

**Success Criteria**: ≥90% cultural accuracy.

---

### 4.4 Musical Quality Testing
**Why Now**: Verify agents produce good music.

**Tasks**:
- [ ] Listen to 20+ generated samples
- [ ] Verify melodies have recognizable patterns
- [ ] Verify bass follows harmony
- [ ] Verify drums adapt to sections
- [ ] Verify section variation present
- [ ] Get feedback from musicians

**Success Criteria**: ≥80% rated "sounds composed, not random".

---

### 4.5 Duration Testing
**Why Now**: Verify V1 feature preserved.

**Tasks**:
- [ ] Test "30 seconds"
- [ ] Test "2 minutes"
- [ ] Test "5 minutes"
- [ ] Test "32 bars"
- [ ] Verify duration accuracy (±5%)

**Success Criteria**: All durations accurate.

---

## Phase 5: UI & UX Enhancements (Day 10)

### 5.1 Generation Feedback
**Why Now**: Users need to see what's happening.

**Tasks**:
- [ ] Display generation seed in UI
- [ ] Show track-by-track generation progress
- [ ] Confirm track count after generation
- [ ] Display tempo, key, duration, track list
- [ ] Show cultural/occasion interpretation

**Success Criteria**: Clear, informative feedback.

---

### 5.2 Error Handling
**Why Now**: Graceful failure important for UX.

**Tasks**:
- [ ] Add try/except around track generation
- [ ] Provide helpful error messages
- [ ] Validate inputs before generation
- [ ] Handle edge cases gracefully
- [ ] Test error scenarios

**Success Criteria**: No crashes, helpful messages.

---

## Phase 6: Session Management (Optional - Future)

### 6.1 Session State
**Why Later**: Core functionality more important.

**Tasks**:
- [ ] Create `CompositionSession` dataclass
- [ ] Track session history
- [ ] Enable "add track" action
- [ ] Enable "modify track" action
- [ ] Enable "extend duration" action

**Success Criteria**: Conversational workflow works.

---

## Testing Checklist

### Unit Tests
- [ ] `test_variation_engine_uniqueness` (1000 seeds all unique)
- [ ] `test_track_count_accuracy` (1-8 tracks)
- [ ] `test_melody_agent_motif` (motif present)
- [ ] `test_bass_agent_chord_following` (follows harmony)
- [ ] `test_drum_agent_adaptation` (adapts to energy)
- [ ] `test_cultural_detection` (20+ styles)
- [ ] `test_duration_parsing` (all formats)
- [ ] `test_humanization` (timing/velocity variance)

### Integration Tests
- [ ] `test_full_generation_unique` (same prompt → different outputs)
- [ ] `test_multi_track_complete` (7 tracks → 7 in MIDI)
- [ ] `test_cultural_authentic` (Japanese → correct setup)
- [ ] `test_section_variation` (sections differ)
- [ ] `test_agent_coordination` (tracks musically coherent)

### Manual Tests
- [ ] Generate 10 pop songs → All different
- [ ] Request "5 track jazz" → Get exactly 5 tracks
- [ ] Request "Japanese music" → Sounds Japanese
- [ ] Request "2 minute track" → Get ~120 seconds
- [ ] Listen to output → Sounds natural
- [ ] Restart app → Still generates different music

---

## Success Metrics

### Must Have (Go/No-Go)
- ✅ Identical prompts produce different outputs
- ✅ Requested track count matches output
- ✅ Zero crashes during generation
- ✅ All V1 features work

### Should Have
- ✅ >30% variation between identical prompts
- ✅ Cultural accuracy ≥90%
- ✅ Duration accuracy ±5%
- ✅ Musical quality rating ≥4/5

### Nice to Have
- ✅ Session-based conversation
- ✅ Generation <5 seconds
- ✅ User satisfaction ≥4.5/5

---

## Risk Mitigation

### Risk: Agents produce incoherent music
**Mitigation**: Extensive testing and musical rules validation. Fallback to V1 generators if agent fails.

### Risk: Performance degradation with agents
**Mitigation**: Profile and optimize. Target <10s for standard generation.

### Risk: Breaking V1 features during refactor
**Mitigation**: Comprehensive test suite. Keep V1 backup.

### Risk: Randomization still deterministic
**Mitigation**: Use nanosecond timestamps + UUID. Test across restarts.

---

## Rollout Plan

### Development
1. Implement Phase 1 (critical fixes)
2. Test uniqueness and track count
3. Implement Phase 2 (agents)
4. Test musical quality
5. Implement Phase 3 (integration)
6. Full regression testing

### Deployment
1. Backup V1 code (`app.py` → `app.py.v1.backup`)
2. Deploy V2 (`app_v2.py` → `app.py`)
3. Test in production
4. Monitor for issues
5. Iterate based on feedback

### Rollback
- If critical issues: Restore `app.py.v1.backup`
- If minor issues: Hot-fix and redeploy
- Keep V1 available for 1 month

---

## File Structure

```
spec-kit/
├── src/
│   └── midigent/
│       ├── variation_engine.py      [NEW]
│       ├── agents/                  [NEW]
│       │   ├── __init__.py
│       │   ├── base.py             (TrackAgent)
│       │   ├── melody_agent.py     (MelodyAgent)
│       │   ├── bass_agent.py       (BassAgent)
│       │   ├── drum_agent.py       (DrumAgent)
│       │   ├── harmony_agent.py    (HarmonyAgent)
│       │   ├── arpeggio_agent.py   (ArpeggioAgent)
│       │   └── pad_agent.py        (PadAgent)
│       ├── duration_parser.py       [PRESERVE]
│       ├── duration_validator.py    [PRESERVE]
│       └── cultural_knowledge.py    [NEW - extract from app.py]
├── app.py                           [REWRITE]
├── app.py.v1.backup                 [BACKUP V1]
├── tests/
│   ├── test_variation_engine.py     [NEW]
│   ├── test_agents.py               [NEW]
│   ├── test_integration.py          [UPDATE]
│   └── test_cultural.py             [NEW]
└── specs/
    └── midigent-v2-agentic-generation-spec.md
```

---

## Current Task

**Starting with Phase 1.1**: Implement Variation Engine

This is the highest priority as it fixes the critical randomization bug that makes the current system unusable.

---

**Next Steps**: After approval, begin Phase 1 implementation immediately.
