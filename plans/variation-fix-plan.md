# MIDIgent Variation Fix - Implementation Plan

**Created**: 2026-01-31  
**Status**: Ready to Start  
**Sprint Duration**: 1 week sprints  
**Total Duration**: 4 weeks

## Executive Summary

This plan addresses the critical issue where MIDIgent generates nearly identical music regardless of user prompts. The root cause is a combination of deterministic pattern generation, lack of seed management, and failure to translate LLM-parsed intent into musical parameters.

## Phase 1: Quick Win - Seed Management (Days 1-2)

**Goal**: Ensure mathematical uniqueness for each generation

### Tasks

#### 1.1 Create VariationEngine
- [ ] File: `src/variation_engine.py`
- [ ] Implement seed generation from prompt + timestamp
- [ ] Track used seeds to prevent collisions
- [ ] Add seed to generation metadata

#### 1.2 Integrate Seed Throughout Generation
- [ ] Modify `MusicGenerator.__init__()` to accept seed parameter
- [ ] Update all `random.*` calls to use instance Random(seed)
- [ ] Pass seed through generation chain: `process_message` → `_generate_tracks_from_plan` → individual generators

#### 1.3 Testing
- [ ] Unit test: 1000 sequential seeds are unique
- [ ] Integration test: Same prompt generates different outputs

**Deliverable**: Each generation uses unique seed, outputs are mathematically varied

---

## Phase 2: Mood-to-Music Mapping (Days 3-5)

**Goal**: Translate parsed mood/style into generation parameters

### Tasks

#### 2.1 Create Mood Profiles Database
- [ ] File: `src/mood_profiles.py`
- [ ] Define MOOD_PROFILES dictionary (20+ moods)
- [ ] Parameters per mood: syncopation, rhythm_variation, note_density, velocity_range, etc.
- [ ] Add mood detection logic (from LLM intent or fallback keywords)

#### 2.2 Integrate Mood Profiles into Generation
- [ ] Modify `generate_melody()` to accept mood_profile parameter
- [ ] Apply density_modifier from mood profile
- [ ] Apply velocity_range from mood profile
- [ ] Use syncopation factor for rhythm shifts

#### 2.3 Update Intent Parser
- [ ] Ensure mood is captured in LLM response
- [ ] Map mood to MOOD_PROFILES
- [ ] Pass mood_profile to generators

#### 2.4 Testing
- [ ] Test: "happy" vs "sad" same genre produces different velocities
- [ ] Test: "funky" has higher syncopation than "calm"

**Deliverable**: Mood words in prompts affect musical output

---

## Phase 3: Pattern Variation System (Days 6-10)

**Goal**: Generate diverse patterns within style constraints

### Tasks

#### 3.1 Implement Rhythmic Variation
- [ ] Create `_generate_rhythmic_patterns()` method
- [ ] Vary note durations based on mood rhythm_variation
- [ ] Add pattern repetition vs variety logic
- [ ] Support syncopation injection

#### 3.2 Implement Melodic Contour System
- [ ] Define contour types: ascending, descending, arch, valley, random, wave
- [ ] Create `_apply_melodic_contour()` method
- [ ] Bias scale degree selection based on contour
- [ ] Add contour to melody generation

#### 3.3 Add Micro-Timing Variations
- [ ] Add optional "humanization" swing/groove
- [ ] Vary note start times slightly (±0.05 beats)
- [ ] Genre-specific: jazz = swing, electronic = quantized

#### 3.4 Testing
- [ ] Test: 10 melodies from same params have different contours
- [ ] Test: Rhythm variation parameter affects pattern diversity
- [ ] Visual test: Plot 5 melodies, verify different shapes

**Deliverable**: Melodies have varied rhythmic and melodic character

---

## Phase 4: Genre Sub-Styles (Days 11-14)

**Goal**: Multiple distinct sub-styles within each genre

### Tasks

#### 4.1 Create Genre Variations Database
- [ ] File: `src/genre_variations.py`
- [ ] Define 3-5 sub-styles per genre
- [ ] Each sub-style: kick pattern, bass style, synth layers, etc.
- [ ] Implement random sub-style selection (seeded)

#### 4.2 Update Drum Generator
- [ ] Refactor `generate_drums()` to use sub-style patterns
- [ ] Add pattern variations within sub-style
- [ ] Support fills, breaks, variations every N bars

#### 4.3 Update Bass Generator
- [ ] Implement multiple bass styles: walking, pulsing, arpeggiated, wobble
- [ ] Select style based on genre sub-style + mood
- [ ] Add rhythmic variation to bass patterns

#### 4.4 Testing
- [ ] Test: "rock" produces 3+ distinct drum patterns
- [ ] Test: "electronic house" vs "electronic dubstep" sound different

**Deliverable**: Each genre has multiple sonic identities

---

## Phase 5: Dynamic Chord Progressions (Days 15-18)

**Goal**: Replace static progressions with mood-aware variations

### Tasks

#### 5.1 Implement ChordProgressionGenerator
- [ ] File: `src/chord_generator.py`
- [ ] Base progression templates per genre
- [ ] Mood-based chord substitutions (sad → minor, happy → major+7th)
- [ ] Randomized variation of base progressions

#### 5.2 Add Chord Extensions
- [ ] 7th, 9th, sus2, sus4 chord types
- [ ] Mood mapping: cinematic → complex, simple → triads
- [ ] Avoid dissonance unless mood calls for it

#### 5.3 Integrate with Generators
- [ ] Replace static CHORD_PROGRESSIONS lookups
- [ ] Use generated progressions in harmony, arpeggio, bass tracks

#### 5.4 Testing
- [ ] Test: "sad pop" uses different chords than "happy pop"
- [ ] Test: Progressions vary between generations

**Deliverable**: Harmonic variety matches mood and varies across generations

---

## Phase 6: Smart Instrumentation (Days 19-21)

**Goal**: Adapt track selection to prompt specifics

### Tasks

#### 6.1 Implement Instrument Detection
- [ ] Regex/LLM patterns for instrument mentions: "piano", "strings", "synth"
- [ ] Extract track count from prompt: "8-track", "simple", "full orchestra"
- [ ] Mood → instrument suggestions: "cinematic" → strings, brass

#### 6.2 Create Instrument-Mood-Genre Database
- [ ] Map genre+mood → suitable instrument palettes
- [ ] Priority weighting for instrument selection
- [ ] Validate against GM MIDI instrument set

#### 6.3 Refactor Track Planning
- [ ] Upgrade `TrackPlanner.plan_tracks()`
- [ ] Use detected instruments if specified
- [ ] Otherwise intelligently select from palette
- [ ] Respect track count requests

#### 6.4 Testing
- [ ] Test: "simple piano" generates 1-2 tracks
- [ ] Test: "cinematic orchestra" generates 6-12 varied instruments
- [ ] Test: "funky electronic" selects appropriate synths

**Deliverable**: Instrumentation matches prompt descriptions

---

## Phase 7: Integration & Polish (Days 22-28)

**Goal**: Connect all systems and validate end-to-end

### Tasks

#### 7.1 End-to-End Integration
- [ ] Connect: Prompt → Intent → Mood Profile → Seed → Generation → MIDI
- [ ] Add generation metadata to MIDI file (comment track)
- [ ] Log all generation parameters for debugging

#### 7.2 Add Generation Explanation
- [ ] Create `explain_generation()` method
- [ ] Show: seed used, mood profile, sub-style, chord progression, instruments
- [ ] Display in UI (optional collapsible section)

#### 7.3 Comprehensive Testing
- [ ] 100 diverse prompts × 3 generations each = 300 test cases
- [ ] Verify uniqueness, mood adherence, musical quality
- [ ] User acceptance testing with non-musicians

#### 7.4 Performance Optimization
- [ ] Profile generation time
- [ ] Optimize hot paths (if needed)
- [ ] Ensure <3s generation time for 16-bar compositions

#### 7.5 Documentation
- [ ] Update README with new capabilities
- [ ] Document mood keywords and their effects
- [ ] Add examples showing variation

**Deliverable**: Production-ready variation system

---

## Success Metrics

### Quantitative
- [ ] Uniqueness: 100 generations from identical prompt produce 100 distinct MIDI files (hash comparison)
- [ ] Diversity: Avg edit distance between same-prompt generations > 70%
- [ ] Performance: Generation time < 5s for 32-bar compositions

### Qualitative
- [ ] Mood recognition: Blind A/B test "happy" vs "sad" → 90%+ correct identification
- [ ] Prompt sensitivity: Changing one word produces audibly different result
- [ ] Musical quality: 80%+ of generations rated "musically coherent"

---

## Risk Management

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Too much chaos | High | Medium | Maintain music theory constraints, parameterize variation levels |
| Performance degradation | Medium | Low | Profile early, optimize hot paths, consider caching |
| Breaking existing functionality | High | Medium | Comprehensive test suite, feature flags for new system |
| Mood profiles feel arbitrary | Medium | Medium | User testing, iterative tuning, allow user override |
| LLM mood parsing fails | Low | Low | Keyword fallback already in place |

---

## Dependencies

- None (internal refactor)
- Groq API: Already integrated
- MIDI library: mido (already used)

---

## Rollout Strategy

1. **Development**: Complete all 6 phases on feature branch
2. **Alpha Testing**: Deploy to test environment, internal testing
3. **Beta**: Gradual rollout with A/B testing (50% old, 50% new)
4. **Full Release**: Switch 100% to new system
5. **Monitor**: Track user feedback, regeneration rates, session duration

---

## Future Enhancements (Post-Launch)

- Machine learning for mood classification
- User-trainable preferences ("I like funky songs like this")
- Genre blending ("80% jazz, 20% electronic")
- Structural awareness (verse, chorus, bridge)
- Actual LLM-generated melodies (vs rule-based)

---

## Estimated Effort

| Phase | Days | Dev Hours |
|-------|------|-----------|
| 1. Seed Management | 2 | 12 |
| 2. Mood Mapping | 3 | 18 |
| 3. Pattern Variation | 5 | 30 |
| 4. Genre Sub-Styles | 4 | 24 |
| 5. Dynamic Chords | 4 | 24 |
| 6. Smart Instrumentation | 3 | 18 |
| 7. Integration & Testing | 7 | 42 |
| **Total** | **28 days** | **168 hours** |

---

**Priority**: P0 (Critical)  
**Complexity**: High  
**Value**: Critical (Core product differentiation)
