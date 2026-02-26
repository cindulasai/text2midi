# MIDIgent Musical Variation Enhancement Specification

## Problem Statement

### Current State
MIDIgent generates nearly identical MIDI compositions despite different user prompts. The system successfully parses user intent via LLM but fails to translate that intent into musically diverse output.

### Root Cause Analysis

**Critical Issues Identified:**

1. **Deterministic Pattern Generation**
   - `generate_melody()`: Uses same random distributions regardless of prompt mood/style
   - `generate_bass()`: Hardcoded patterns per genre with no variation
   - `generate_drums()`: Fixed patterns (kick on 0,2 / snare on 1,3) for each genre
   - **Result**: Every "rock" song sounds identical, every "electronic" song sounds identical

2. **No Seed Diversification**
   - Python's `random` module uses same seed across generations
   - No explicit seed management or variation between requests
   - **Result**: Similar inputs → similar random choices → similar output

3. **Limited Parameter Translation**
   - LLM extracts: mood, energy, tempo, key, genre
   - Generation uses: only energy (as density), genre (as pattern lookup)
   - **Ignored**: mood, specific style requests, descriptors like "funky", "upbeat", "cinematic"
   - **Result**: 90% of parsed intent is thrown away

4. **Overly Constrained Music Theory**
   - Scale-based generation limits melodic variety
   - Chord progressions are static per genre (always I-V-vi-IV for pop)
   - No rhythmic variation within patterns
   - **Result**: Musically "correct" but boring

5. **No Prompt-Specific Customization**
   - "Cinematic 8-track orchestral" generates same tracks as "simple piano"
   - Track planner doesn't adapt to prompt details
   - **Result**: Generic output regardless of specificity

## Proposed Solution Architecture

### Phase 1: Seed & Randomization Management
**Objective**: Ensure each generation is mathematically unique

```python
class VariationEngine:
    """Manages randomization to ensure diverse output."""
    
    def __init__(self):
        self.generation_seeds = set()
    
    def get_unique_seed(self, prompt: str, timestamp: float) -> int:
        """Generate unique seed from prompt hash + timestamp."""
        base_seed = hash(f"{prompt}{timestamp}{random.random()}")
        while base_seed in self.generation_seeds:
            base_seed = hash(f"{base_seed}{random.random()}")
        self.generation_seeds.add(base_seed)
        return abs(base_seed) % (2**32)
```

### Phase 2: Mood-to-Music Parameter Mapping
**Objective**: Translate LLM-parsed mood/style into generation parameters

```python
MOOD_PROFILES = {
    "funky": {
        "syncopation": 0.7,  # Probability of syncopated notes
        "rhythm_variation": 0.8,
        "harmonic_tension": 0.6,
        "velocity_dynamics": "wide",
        "note_density_modifier": 1.2,
    },
    "upbeat": {
        "tempo_boost": 1.1,
        "rhythm_subdivision": "sixteenth",  # Faster note divisions
        "chord_brightness": "major_dominance",
        "velocity_range": (80, 110),
    },
    "cinematic": {
        "dynamic_range": "wide",  # ppp to fff
        "orchestration_layers": 6-12,
        "build_structure": "crescendo",
        "harmonic_complexity": "advanced",  # 7ths, 9ths, suspensions
    },
    "sad": {
        "tempo_reduction": 0.85,
        "minor_preference": 0.9,
        "dissonance_factor": 0.3,
        "note_spacing": "sparse",
    },
    # ... more moods
}
```

### Phase 3: Pattern Variation System
**Objective**: Generate diverse patterns within style constraints

```python
class PatternVariator:
    """Creates pattern variations based on mood profiles."""
    
    def generate_varied_melody(
        self, 
        root: int, 
        mode: str, 
        bars: int, 
        energy: str, 
        mood_profile: dict,
        seed: int
    ) -> List[Note]:
        """Generate melody with mood-specific characteristics."""
        random.seed(seed)
        
        # Apply mood-specific variations
        syncopation = mood_profile.get("syncopation", 0.0)
        density_mod = mood_profile.get("note_density_modifier", 1.0)
        base_density = {"low": 0.3, "medium": 0.5, "high": 0.7}[energy]
        actual_density = base_density * density_mod
        
        # Vary rhythm patterns
        rhythm_var = mood_profile.get("rhythm_variation", 0.3)
        rhythmic_patterns = self._generate_rhythmic_variations(
            bars, rhythm_var, seed
        )
        
        # Vary melodic contours
        contour = random.choice([
            "ascending", "descending", "arch", "valley", "random"
        ])
        
        notes = []
        # ... generation logic using all variation parameters
        return notes
    
    def _generate_rhythmic_variations(self, bars: int, variation: float, seed: int):
        """Create unique rhythmic patterns."""
        patterns = []
        for bar in range(bars):
            if random.random() < variation:
                # Create new pattern
                pattern = [random.choice([0.25, 0.5, 0.75, 1.0, 1.5]) 
                          for _ in range(random.randint(2, 8))]
            else:
                # Repeat previous or use standard
                pattern = patterns[-1] if patterns else [0.5, 0.5, 0.5, 0.5]
            patterns.append(pattern)
        return patterns
```

### Phase 4: Genre-Specific Variation Tables
**Objective**: Multiple sub-styles within each genre

```python
GENRE_VARIATIONS = {
    "electronic": {
        "styles": ["house", "techno", "dubstep", "ambient", "trance"],
        "house": {
            "kick_pattern": [0, 1, 2, 3],  # Four-on-floor
            "bass_style": "arpeggiated",
            "synth_layers": 3-5,
        },
        "dubstep": {
            "kick_pattern": [0, 2],
            "bass_style": "wobble",
            "drop_bars": [8, 16],
        },
        # ... more variations
    },
    "rock": {
        "styles": ["classic", "punk", "progressive", "metal", "indie"],
        # ... each with unique characteristics
    },
}
```

### Phase 5: Dynamic Chord Progression Generator
**Objective**: Replace static progressions with generated variations

```python
class ChordProgressionGenerator:
    """Generate varied chord progressions."""
    
    def generate_progression(
        self, 
        genre: str, 
        mood: str, 
        bars: int,
        seed: int
    ) -> List[List[int]]:
        """Create unique progression fitting mood and genre."""
        random.seed(seed)
        
        # Start with common progressions but add variations
        base = CHORD_PROGRESSIONS[genre]
        
        if mood in ["sad", "melancholic", "dark"]:
            # Add minor substitutions, suspended chords
            progression = self._add_minor_substitutions(base)
        elif mood in ["happy", "upbeat", "bright"]:
            # Use major chords, add 7ths
            progression = self._brighten_progression(base)
        elif mood in ["mysterious", "cinematic"]:
            # Add extensions, altered chords
            progression = self._add_complexity(base)
        else:
            # Variation within genre style
            progression = self._vary_progression(base, variation=0.3)
        
        return progression
```

### Phase 6: Prompt-Aware Track Planning
**Objective**: Adapt instrumentation to prompt specifics

```python
class SmartTrackPlanner:
    """Plans tracks based on detailed prompt analysis."""
    
    def plan_from_prompt(
        self, 
        prompt: str, 
        llm_intent: dict,
        seed: int
    ) -> List[TrackConfig]:
        """Generate track plan from prompt details."""
        
        # Extract track count if specified
        track_count = self._extract_track_count(prompt, llm_intent)
        
        # Detect instrumentation requests
        requested_instruments = self._detect_instruments(prompt)
        
        # Genre + mood → suggested instruments
        genre_instruments = self._get_genre_instruments(
            llm_intent["genre"], llm_intent.get("mood")
        )
        
        # Build track plan with variation
        random.seed(seed)
        tracks = []
        
        if requested_instruments:
            tracks.extend(requested_instruments)
        else:
            # Intelligently select from genre palette
            tracks = self._select_varied_instruments(
                genre_instruments, track_count, seed
            )
        
        return tracks
```

## Implementation Plan

### Sprint 1: Foundation (Week 1)
- [ ] Implement VariationEngine with seed management
- [ ] Add seed parameter to all generation methods
- [ ] Create comprehensive MOOD_PROFILES dictionary
- [ ] Write unit tests for seed uniqueness

### Sprint 2: Pattern Variation (Week 1-2)
- [ ] Implement PatternVariator class
- [ ] Refactor generate_melody() to use mood profiles
- [ ] Add rhythmic variation system
- [ ] Add melodic contour variations
- [ ] Test: 100 generations from same prompt should be unique

### Sprint 3: Genre Variations (Week 2)
- [ ] Create GENRE_VARIATIONS tables
- [ ] Implement sub-style selection logic
- [ ] Update bass/drum generators to use variations
- [ ] Test: Each genre has 3+ distinct sound profiles

### Sprint 4: Dynamic Harmonies (Week 3)
- [ ] Implement ChordProgressionGenerator
- [ ] Add mood-based chord substitutions
- [ ] Integrate with existing generation flow
- [ ] Test: Same genre/different moods use different progressions

### Sprint 5: Smart Instrumentation (Week 3)
- [ ] Implement SmartTrackPlanner
- [ ] Add instrument detection from prompts
- [ ] Create expanded instrument-to-mood mappings
- [ ] Test: "cinematic orchestra" vs "simple piano" use different tracks

### Sprint 6: Integration & Testing (Week 4)
- [ ] Connect all systems: VariationEngine → IntentParser → Generators
- [ ] Add generation metadata (seed, mood profile used, etc.)
- [ ] Comprehensive testing with diverse prompts
- [ ] User acceptance testing

## Success Criteria

1. **Uniqueness**: 100 consecutive generations from "funky upbeat electronic" produce 100 distinct MIDI files
2. **Mood Recognition**: "sad piano" and "happy piano" sound distinctly different
3. **Style Adherence**: "cinematic orchestral" uses 6-12 tracks with orchestral instruments
4. **Prompt Sensitivity**: Changing any word in prompt produces audibly different output
5. **Quality**: Generated music remains musically coherent and listenable

## Technical Debt to Address

- Replace global `random` with instance-based random.Random()
- Add logging of generation parameters for debugging
- Create visualization of what parameters affected each generation
- Add "explain generation" feature showing how prompt → parameters → output

## Risk Mitigation

- **Risk**: Too much randomness → chaos
  - **Mitigation**: Keep music theory constraints, vary within them
- **Risk**: Performance degradation
  - **Mitigation**: Profile code, optimize hot paths
- **Risk**: Breaking existing functionality
  - **Mitigation**: Comprehensive test suite before changes

---

**Estimated Effort**: 3-4 weeks
**Priority**: Critical - Core value proposition
**Dependencies**: None
