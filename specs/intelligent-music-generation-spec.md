# Feature Specification: Intelligent Music Generation System

**Feature Branch**: `intelligent-music-gen`  
**Created**: January 31, 2026  
**Status**: Draft  
**Input**: User request: "Fix multi-track generation, dynamic variations, cultural music understanding, and humanization"

## Executive Summary

Transform MidiGen into an intelligent music generation system that:
1. **Correctly generates multiple tracks** as requested (fixing the current 1-track bug)
2. **Understands diverse music requests** (country, culture, region, instrument, occasion-based)
3. **Creates dynamic, section-based variations** (intro, verse, chorus, bridge, outro)
4. **Produces human-like music** (timing/velocity variations, not robotic)
5. **Handles any duration** (from 30 seconds to 10 minutes)

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Multi-Track Generation Works Correctly (Priority: P1)

**User Journey**: As a music creator, when I request "5 tracks" or "6 tracks," the system should generate exactly that many tracks, not just 1 track.

**Why this priority**: This is the most critical bug - the system is currently broken and doesn't generate the requested number of tracks.

**Independent Test**: Request "generate 5 track pop music" → System generates exactly 5 distinct tracks with different instruments and roles.

**Acceptance Scenarios**:

1. **Given** user requests "5 track pop music", **When** generation completes, **Then** MIDI file contains exactly 5 tracks
2. **Given** user requests "6 track Japan music", **When** generation completes, **Then** MIDI file contains exactly 6 tracks with Japanese instruments
3. **Given** user requests "3 track minimal", **When** generation completes, **Then** MIDI file contains exactly 3 tracks
4. **Given** AI track planner suggests 7 tracks, **When** generation runs, **Then** all 7 tracks are generated and saved to MIDI

---

### User Story 2 - Cultural & Regional Music Understanding (Priority: P1)

**User Journey**: As a global music creator, I want to request music by culture, country, region, or tradition (e.g., "Japanese music," "Carnatic music," "Sufi music," "Brazilian samba") and get appropriate instruments, scales, and rhythms.

**Why this priority**: Makes the system universally accessible and culturally aware - essential for a world-class music generator.

**Independent Test**: Request "Japanese traditional music" → System selects koto, shamisen, shakuhachi instruments and uses Japanese pentatonic scales.

**Acceptance Scenarios**:

1. **Given** "Japanese music" request, **When** generated, **Then** uses Japanese instruments (koto, shamisen, shakuhachi) and pentatonic/yo scales
2. **Given** "Carnatic music" request, **When** generated, **Then** uses South Indian classical elements (veena-like strings, tabla, tambura drone)
3. **Given** "Sufi music" request, **When** generated, **Then** uses Middle Eastern instruments (oud, ney, qanun) and maqam-based scales
4. **Given** "Brazilian music" request, **When** generated, **Then** uses Latin percussion, nylon guitar, and samba/bossa rhythms
5. **Given** "Irish folk" request, **When** generated, **Then** uses fiddle, tin whistle, bodhrán, and Celtic scales
6. **Given** "Indian Hindustani" request, **When** generated, **Then** uses sitar, tabla, tanpura drone, and raga-based patterns

---

### User Story 3 - Occasion & Context-Based Generation (Priority: P2)

**User Journey**: As a content creator, I want to request music by occasion or use-case (e.g., "party music," "cinema background," "meditation," "workout") and get contextually appropriate music.

**Why this priority**: Makes the system intuitive for non-musicians who think in terms of use-cases rather than musical theory.

**Independent Test**: Request "party music" → System generates upbeat, energetic dance music with strong rhythm section.

**Acceptance Scenarios**:

1. **Given** "party music" request, **When** generated, **Then** high tempo (120-130 BPM), strong drums, bass, energetic feel
2. **Given** "cinema background" request, **When** generated, **Then** cinematic/orchestral elements, dynamic range, emotional depth
3. **Given** "meditation music" request, **When** generated, **Then** slow tempo (60-70 BPM), ambient pads, minimal percussion, calming
4. **Given** "workout music" request, **When** generated, **Then** high energy (130-150 BPM), driving rhythm, motivational
5. **Given** "restaurant background" request, **When** generated, **Then** moderate tempo, jazz/lounge style, non-intrusive
6. **Given** "dramatic scene" request, **When** generated, **Then** tension-building elements, dynamic swells, emotional intensity

---

### User Story 4 - Dynamic Section-Based Variation (Priority: P2)

**User Journey**: As a music producer, I want my generated music to have dynamic sections (intro, verse, chorus, bridge, outro) where **ALL tracks** change and evolve, not just one track staying static.

**Why this priority**: Makes music sound professional and engaging rather than repetitive and boring.

**Independent Test**: Generate 2-minute track → Listen and verify intro is different from verse, chorus is more intense, bridge provides contrast, outro winds down. All tracks participate in changes.

**Acceptance Scenarios**:

1. **Given** 2-minute composition, **When** generated, **Then** has distinct intro (8 bars), verse (16 bars), chorus (16 bars), bridge (8 bars), outro (8 bars)
2. **Given** chorus section, **When** playing, **Then** ALL tracks increase energy/density compared to verse
3. **Given** bridge section, **When** playing, **Then** ALL tracks provide musical contrast (different patterns/harmonies)
4. **Given** intro section, **When** playing, **Then** gradually builds up (not all tracks start at once)
5. **Given** outro section, **When** playing, **Then** gradually fades/simplifies (tracks drop out progressively)
6. **Given** any section transition, **When** crossing boundary, **Then** changes are noticeable across all active tracks

---

### User Story 5 - Human-Like Timing & Feel (Priority: P2)

**User Journey**: As a musician, I want generated music to sound like it was played by a human, with natural timing variations, velocity dynamics, and groove - not robotic quantization.

**Why this priority**: Distinguishes professional-sounding output from obviously computer-generated music.

**Independent Test**: Generate any track → Examine MIDI note timings and velocities → Verify micro-timing variations (±5-20ms) and velocity variations (±5-15 velocity) present.

**Acceptance Scenarios**:

1. **Given** any melody track, **When** examining note timings, **Then** notes have ±5-20ms micro-timing variations (not perfectly quantized)
2. **Given** any melody track, **When** examining velocities, **Then** notes have velocity variations (not all the same velocity)
3. **Given** drum track, **When** examining hi-hats, **Then** has natural velocity variations simulating human hi-hat playing
4. **Given** sustained notes, **When** examining, **Then** has slight velocity swells/decays (not flat velocity)
5. **Given** rhythmic elements, **When** playing, **Then** has subtle swing/groove (not rigid grid)
6. **Given** fast passages, **When** playing, **Then** has natural acceleration/deceleration (not constant tempo)

---

### User Story 6 - Flexible Duration Handling (Priority: P3)

**User Journey**: As a creator, I want to specify any duration (30 seconds to 10 minutes) and get properly structured music that fits the timeframe.

**Why this priority**: Essential for real-world applications (ads, videos, installations, performances).

**Independent Test**: Request "30 second jazz intro" → Gets exactly 30 seconds. Request "5 minute ambient piece" → Gets exactly 5 minutes with proper structure.

**Acceptance Scenarios**:

1. **Given** "30 seconds" request, **When** generated, **Then** creates concise intro-verse-outro structure fitting exactly 30 seconds
2. **Given** "2 minutes" request, **When** generated, **Then** creates full song structure (intro-verse-chorus-bridge-outro)
3. **Given** "5 minutes" request, **When** generated, **Then** creates extended arrangement with multiple repetitions and variations
4. **Given** no duration specified, **When** generated, **Then** defaults to 2 minutes (industry standard)

---

## Technical Design

### Architecture Overview

```
User Prompt
    ↓
[Cultural Music Interpreter] ← Knowledge Base (instruments, scales, rhythms by region/culture)
    ↓
[Enhanced Intent Parser] → {genre, culture, occasion, num_tracks, duration, mood, energy}
    ↓
[Smart Track Planner] → [Track1, Track2, Track3, Track4, Track5, ...]
    ↓
[Section Structure Generator] → {intro, verse, chorus, bridge, outro} sections
    ↓
[Multi-Track Generator] → For EACH track + EACH section:
    ├─ [Melody Generator] + [Humanizer]
    ├─ [Harmony Generator] + [Humanizer]
    ├─ [Bass Generator] + [Humanizer]
    ├─ [Drums Generator] + [Humanizer]
    └─ [Variation Mixer] (adjusts density, rhythm, harmony per section)
    ↓
[MIDI Assembly] → Complete multi-track MIDI file
```

### Core Components

#### 1. Cultural Music Knowledge Base

```python
CULTURAL_MUSIC_DATABASE = {
    "japanese": {
        "scales": ["pentatonic_minor", "yo_scale", "in_scale"],
        "instruments": ["koto", "shamisen", "shakuhachi", "taiko"],
        "rhythm_patterns": ["ma" (spacing), "jo-ha-kyu" (acceleration)],
        "characteristics": "emphasis on silence, nature sounds, pentatonic"
    },
    "carnatic": {
        "scales": ["kalyani", "sankarabharanam", "kharaharapriya"],
        "instruments": ["veena", "mridangam", "ghatam", "violin"],
        "rhythm_patterns": ["adi_tala", "rupaka_tala"],
        "characteristics": "complex rhythms, improvisation, drone"
    },
    "sufi": {
        "scales": ["hijaz_kar", "rast", "bayati"],
        "instruments": ["oud", "ney", "qanun", "daf", "tabla"],
        "rhythm_patterns": ["sama_rhythm", "dhikr_patterns"],
        "characteristics": "spiritual, repetitive, trance-inducing, maqam-based"
    },
    # ... 50+ more cultural/regional music styles
}
```

#### 2. Enhanced Intent Parser

**Current Problem**: AI track planner returns track configs but generation doesn't respect the count.

**Solution**: Extract explicit track count from prompt AND ensure all planned tracks are generated.

```python
def parse(self, user_input: str) -> Dict[str, Any]:
    """Enhanced parsing with cultural awareness."""
    
    # 1. Extract explicit track count
    track_count = self._extract_track_count(user_input)  # "5 track" → 5
    
    # 2. Detect cultural/regional context
    culture_info = self._detect_cultural_context(user_input)
    
    # 3. Detect occasion/use-case
    occasion = self._detect_occasion(user_input)
    
    # 4. Get AI track plan
    track_plan = self.track_planner.plan_tracks(
        user_input, 
        requested_count=track_count,
        culture=culture_info,
        occasion=occasion
    )
    
    # 5. Ensure track_count matches plan
    if track_count and len(track_plan) != track_count:
        track_plan = self._adjust_track_plan(track_plan, track_count)
    
    return {
        "track_plan": track_plan,
        "track_count": len(track_plan),  # CRITICAL: Pass this through
        "culture": culture_info,
        "occasion": occasion,
        # ... other params
    }
```

#### 3. Section Structure Generator

**Current Problem**: No section awareness - music is uniform throughout.

**Solution**: Define section structure based on duration, create section-specific variations.

```python
@dataclass
class Section:
    name: str  # intro, verse, chorus, bridge, outro
    start_bar: int
    end_bar: int
    energy_level: float  # 0.0-1.0
    density_level: float  # 0.0-1.0 (how many tracks/notes active)
    characteristics: Dict[str, Any]

class SectionStructureGenerator:
    def generate_structure(self, total_bars: int, genre: str) -> List[Section]:
        """Create song structure based on duration."""
        
        if total_bars <= 16:  # Short (< 1 minute)
            return [
                Section("intro", 0, 4, 0.4, 0.5, {"build": True}),
                Section("main", 4, 12, 0.8, 0.8, {}),
                Section("outro", 12, 16, 0.5, 0.6, {"fade": True})
            ]
        
        elif total_bars <= 32:  # Medium (~2 minutes) - STANDARD
            return [
                Section("intro", 0, 8, 0.4, 0.5, {"build": True}),
                Section("verse", 8, 16, 0.6, 0.7, {}),
                Section("chorus", 16, 24, 0.9, 0.9, {"peak": True}),
                Section("bridge", 24, 28, 0.7, 0.6, {"contrast": True}),
                Section("outro", 28, 32, 0.5, 0.5, {"fade": True})
            ]
        
        else:  # Long (> 2 minutes)
            # Extended structure with verse-chorus repetitions
            sections = [Section("intro", 0, 8, 0.4, 0.5, {"build": True})]
            current_bar = 8
            
            # Verse-Chorus pattern
            while current_bar < total_bars - 12:
                sections.append(Section("verse", current_bar, current_bar+8, 0.6, 0.7, {}))
                sections.append(Section("chorus", current_bar+8, current_bar+16, 0.9, 0.9, {"peak": True}))
                current_bar += 16
            
            sections.append(Section("bridge", current_bar, current_bar+8, 0.7, 0.6, {"contrast": True}))
            sections.append(Section("outro", current_bar+8, total_bars, 0.5, 0.5, {"fade": True}))
            
            return sections
```

#### 4. Multi-Track Generator with Section Awareness

**Current Problem**: Even when track plan has multiple tracks, only 1 track is generated.

**Root Cause**: The `_generate_tracks_from_plan` method IS generating multiple tracks correctly, but somewhere the tracks are being lost or only 1 is being saved.

**Solution**: Debug the track flow and ensure ALL tracks make it to MIDI file.

```python
def _generate_tracks_from_plan(self, track_plan: List[TrackConfig], 
                               root: int, mode: str, bars: int, 
                               energy: str, genre: str,
                               sections: List[Section]) -> List[Track]:
    """Generate tracks with section-based variations."""
    
    tracks = []
    
    print(f"🎵 Generating {len(track_plan)} tracks...")  # DEBUG
    
    for i, config in enumerate(track_plan):
        print(f"  Track {i+1}/{len(track_plan)}: {config.track_type} - {config.instrument}")  # DEBUG
        
        # Assign channel
        channel = 9 if config.track_type == "drums" else (i % 9)
        if channel == 9 and config.track_type != "drums":
            channel = (channel + 1) % 16
        
        # Get instrument program
        instrument = config.instrument.lower().replace(" ", "_")
        program = GM_INSTRUMENTS.get(instrument, 0)
        
        # Generate notes FOR EACH SECTION
        all_notes = []
        for section in sections:
            section_notes = self._generate_section_notes(
                config, section, root, mode, genre, energy
            )
            all_notes.extend(section_notes)
        
        # Apply humanization
        all_notes = self._humanize_notes(all_notes, config.track_type)
        
        # Create track
        track = Track(
            name=f"{config.instrument.title()} ({config.track_type})",
            notes=all_notes,
            midi_program=program,
            channel=channel,
            track_type=config.track_type
        )
        
        tracks.append(track)
        print(f"    ✓ Generated {len(all_notes)} notes")  # DEBUG
    
    print(f"✓ Total tracks generated: {len(tracks)}")  # DEBUG
    return tracks

def _generate_section_notes(self, config: TrackConfig, section: Section,
                            root: int, mode: str, genre: str, energy: str) -> List[Note]:
    """Generate notes for a specific track in a specific section."""
    
    # Calculate section parameters
    section_bars = section.end_bar - section.start_bar
    section_energy = self._blend_energy(energy, section.energy_level)
    section_density = section.density_level
    
    # Adjust generation based on section characteristics
    if "build" in section.characteristics:
        # Gradual introduction
        section_density *= 0.7
    elif "fade" in section.characteristics:
        # Gradual reduction
        section_density *= 0.6
    elif "peak" in section.characteristics:
        # Maximum intensity
        section_energy = "high"
        section_density *= 1.1
    elif "contrast" in section.characteristics:
        # Different pattern/harmony
        mode = self._get_contrasting_mode(mode)
    
    # Generate notes based on track type
    if config.track_type == "lead":
        notes = self.generator.generate_melody(
            root, mode, section_bars, section_energy, genre, density=section_density
        )
    # ... similar for other track types
    
    # Offset notes to section start time
    section_offset = section.start_bar * 4  # Convert bars to beats
    for note in notes:
        note.start_time += section_offset
    
    return notes
```

#### 5. Humanization Engine

**Current Problem**: All notes are perfectly quantized and have uniform velocity.

**Solution**: Add micro-timing variations, velocity variations, and groove.

```python
class HumanizationEngine:
    def __init__(self):
        self.timing_variance = 0.03  # ±30ms at 120 BPM
        self.velocity_variance = 10   # ±10 MIDI velocity
    
    def humanize_notes(self, notes: List[Note], track_type: str) -> List[Note]:
        """Add human-like variations to notes."""
        
        for i, note in enumerate(notes):
            # 1. Micro-timing variations
            timing_offset = random.gauss(0, self.timing_variance)
            note.start_time += timing_offset
            
            # 2. Velocity variations
            velocity_offset = int(random.gauss(0, self.velocity_variance))
            note.velocity = max(30, min(120, note.velocity + velocity_offset))
            
            # 3. Add groove (slight swing for certain beats)
            beat_position = note.start_time % 1.0
            if 0.4 < beat_position < 0.6:  # On the offbeat
                if track_type in ["drums", "bass"]:
                    note.start_time += 0.05  # Slight swing
            
            # 4. Dynamic accents (emphasize certain beats)
            if note.start_time % 4.0 < 0.1:  # Downbeat
                note.velocity = min(127, int(note.velocity * 1.2))
            
            # 5. Slight duration variations
            duration_variance = random.gauss(0, 0.05)
            note.duration = max(0.1, note.duration + duration_variance)
        
        return notes
    
    def add_expression(self, notes: List[Note], track_type: str) -> List[Note]:
        """Add musical expression (crescendos, decrescendos, etc.)."""
        
        if not notes:
            return notes
        
        # Add velocity curves
        for i, note in enumerate(notes):
            progress = i / len(notes)
            
            # Crescendo in first quarter
            if progress < 0.25:
                note.velocity = int(note.velocity * (0.7 + 0.3 * (progress * 4)))
            
            # Decrescendo in last quarter
            elif progress > 0.75:
                note.velocity = int(note.velocity * (1.0 - 0.3 * ((progress - 0.75) * 4)))
        
        return notes
```

### Critical Fix: Track Count Bug

**Diagnosis**: After reviewing the code, the issue is likely in how tracks are being passed or how many are actually being generated. Let me trace the flow:

1. User requests "5 track music"
2. `IntentParser.parse()` calls `track_planner.plan_tracks()`
3. `plan_tracks()` returns a list of `TrackConfig` objects
4. `_generate_tracks_from_plan()` iterates over this list
5. Each iteration should create ONE track
6. All tracks should be returned and saved to MIDI

**Potential Issues**:
- Track planner might not be extracting the track count from prompt
- Track planner AI might be ignoring the request
- Generated tracks might be getting overwritten instead of accumulated

**Fix Strategy**:
1. Add explicit track count extraction
2. Pass track count to track planner as a requirement
3. Ensure track planner respects the count
4. Add validation that generated tracks match requested count
5. Add debug logging to trace where tracks are lost

## Implementation Priority

### Phase 1: Critical Fixes (P1) - **DO THIS FIRST**
1. ✅ Fix multi-track generation bug
2. ✅ Add cultural music knowledge base
3. ✅ Enhance intent parser with cultural awareness

### Phase 2: Quality Improvements (P2)
4. ✅ Implement section-based structure
5. ✅ Add humanization engine
6. ✅ Implement occasion-based generation

### Phase 3: Polish (P3)
7. ✅ Extended duration handling
8. ✅ Advanced variation techniques

## Testing Strategy

### Unit Tests
- Track count extraction: "5 track" → 5, "six tracks" → 6
- Cultural detection: "Japanese music" → {culture: "japanese"}
- Section generation: 32 bars → [intro, verse, chorus, bridge, outro]
- Humanization: Notes have timing/velocity variations

### Integration Tests
- Full generation: "5 track Japanese party music 2 minutes" → 5 tracks, Japanese instruments, upbeat, 2min, sections vary
- Cultural accuracy: "Carnatic music" → Indian scales, instruments, rhythms
- Humanization: Generated MIDI sounds natural, not robotic

### User Acceptance Tests
- Non-musician tests: Can non-musicians request music naturally?
- Cultural tests: Do cultural music experts recognize their traditions?
- Quality tests: Does music sound professional and engaging?

## Success Metrics

1. **Correctness**: Requested track count matches generated track count (100% accuracy)
2. **Cultural Awareness**: System recognizes 50+ cultural music styles
3. **Dynamic Range**: Sections have measurably different energy/density levels
4. **Humanization**: MIDI notes have ±5-20ms timing variance, ±5-15 velocity variance
5. **User Satisfaction**: Users rate music as "natural" and "engaging" (>4/5 stars)

## Non-Goals

- Real-time generation (acceptable to take 5-10 seconds)
- Audio rendering (MIDI only, user can render in their DAW)
- Music notation display (MIDI only)
- User authentication/saving (local file output only)

## Appendix: Cultural Music Reference

### Japanese Traditional
- **Scales**: Yo (pentatonic), In (pentatonic), Hirajoshi
- **Instruments**: Koto (zither), Shamisen (lute), Shakuhachi (flute), Taiko (drum)
- **Characteristics**: Ma (negative space), Jo-ha-kyu (introduction-development-climax)

### Carnatic (South Indian Classical)
- **Scales**: 72 melakarta ragas
- **Instruments**: Veena, Mridangam, Ghatam, Violin
- **Rhythms**: Adi tala (8-beat), Rupaka tala (6-beat)
- **Characteristics**: Gamakas (ornamentations), drone (tanpura)

### Sufi (Islamic Mystical)
- **Scales**: Hijaz kar, Rast, Bayati, Saba
- **Instruments**: Oud, Ney, Qanun, Daf, Tabla
- **Rhythms**: Sama rhythm (spiritual trance)
- **Characteristics**: Repetitive phrases, spiritual devotion, trance-inducing

### Brazilian
- **Styles**: Samba, Bossa Nova, Forró
- **Instruments**: Nylon guitar, Cavaquinho, Pandeiro, Surdo
- **Rhythms**: Samba (2/4), Bossa Nova (syncopated), Forró (2/4)

### Irish Folk
- **Scales**: Mixolydian, Dorian modes
- **Instruments**: Fiddle, Tin Whistle, Bodhrán, Uilleann Pipes
- **Rhythms**: Jigs (6/8), Reels (4/4), Hornpipes

*(Continue with 45+ more cultural/regional styles...)*

---

**End of Specification**

This specification provides a complete blueprint for transforming MidiGen into an intelligent, culturally-aware, dynamic music generation system that fixes all current issues and future-proofs the system for diverse global use-cases.
