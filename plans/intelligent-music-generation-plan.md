# Implementation Plan: Intelligent Music Generation System

**Branch**: `intelligent-music-gen` | **Date**: January 31, 2026 | **Spec**: [intelligent-music-generation-spec.md](../specs/intelligent-music-generation-spec.md)

## Summary

Transform MidiGen into an intelligent, culturally-aware music generation system that:
1. **Fixes critical bug**: Correctly generates requested number of tracks (5 track → 5 tracks, not 1)
2. **Adds cultural intelligence**: Understands 50+ global music styles (Japanese, Carnatic, Sufi, etc.)
3. **Creates dynamic music**: Section-based variations (intro/verse/chorus/bridge/outro) across ALL tracks
4. **Sounds human**: Micro-timing and velocity variations, not robotic quantization
5. **Handles any duration**: 30 seconds to 10 minutes with proper structure

**Technical Approach**: Enhance existing MidiGen architecture with:
- Cultural music knowledge database
- Enhanced multi-step intent parsing pipeline
- Section structure generator
- Per-track, per-section note generation
- Humanization post-processing engine

## Technical Context

**Language/Version**: Python 3.10+  
**Primary Dependencies**: 
- `mido` (MIDI file I/O)
- `groq` (LLM intent parsing)
- `gradio` (UI)
- Custom `midigent` package (duration parsing, music generation)

**Storage**: Local filesystem (outputs/ folder for MIDI files)  
**Testing**: Manual testing + pytest for unit tests  
**Target Platform**: Desktop (Gradio web UI), CLI potential  
**Project Type**: Single application (app.py + src/midigent/)  
**Performance Goals**: 
- Generate 2-minute, 6-track composition in <10 seconds
- Support up to 8 simultaneous tracks
- Duration range: 30 seconds to 10 minutes

**Constraints**: 
- MIDI output only (no audio rendering)
- Local execution (no cloud deployment required)
- Groq API available for intelligent parsing (fallback to rule-based)

**Scale/Scope**: 
- 50+ cultural music styles
- 8 track types (lead, harmony, bass, drums, arpeggio, pad, counter_melody, fx)
- 5 section types (intro, verse, chorus, bridge, outro)
- 100+ GM instruments

## Constitution Check

✅ **User Value First**: Fixes critical bug and adds requested cultural intelligence  
✅ **Working Software**: Incremental implementation - each phase delivers working feature  
✅ **Simple Design**: Leverages existing architecture, adds modular components  
✅ **Testing**: Will include unit tests for cultural detection, section generation, humanization  
✅ **Maintainable**: Clear separation of concerns (parsing → planning → generation → humanization)

## Project Structure

### Documentation (this feature)

```text
specs/intelligent-music-gen/
├── spec.md              # Feature specification (CREATED)
├── plan.md              # This file (CREATING NOW)
└── tasks.md             # Implementation tasks (WILL CREATE NEXT)
```

### Source Code (repository root)

```text
app.py                   # Main Gradio application (WILL MODIFY)

src/midigent/
├── __init__.py
├── cultural_music.py    # NEW: Cultural music knowledge database
├── intent_parser.py     # WILL EXTRACT from app.py
├── track_planner.py     # WILL EXTRACT from app.py
├── section_structure.py # NEW: Section-based structure generator
├── music_generator.py   # WILL EXTRACT from app.py + enhance
├── humanizer.py         # NEW: Timing/velocity humanization
├── duration_parser.py   # EXISTING
├── duration_validator.py # EXISTING
└── duration_models.py   # EXISTING

tests/
├── test_cultural_music.py  # NEW
├── test_intent_parser.py   # NEW
├── test_section_structure.py # NEW
├── test_humanizer.py       # NEW
├── test_integration.py     # EXISTING (will enhance)
└── test_realworld.py       # EXISTING (will enhance)

outputs/                 # Generated MIDI files
```

## Implementation Phases

### Phase 0: Debug & Fix Critical Bug (P1 - Priority 1)

**Goal**: Identify and fix why track count doesn't match request.

**Investigation Steps**:
1. Add debug logging to trace track generation flow
2. Verify track_planner output (how many TrackConfig objects?)
3. Verify _generate_tracks_from_plan loop (how many iterations?)
4. Verify MIDI assembly (how many tracks in final MIDI?)
5. Test with explicit track counts (1, 3, 5, 6, 8 tracks)

**Expected Finding**: One of these scenarios:
- Track planner not extracting count from prompt → **Fix**: Add track count extraction
- Track planner AI ignoring count → **Fix**: Make count mandatory in AI prompt
- Loop only running once → **Fix**: Fix loop condition
- Tracks being overwritten → **Fix**: Use list.append() not assignment
- MIDI file only saving first track → **Fix**: Verify MIDI save logic

**Deliverable**: Multi-track generation works correctly (5 track request → 5 tracks generated)

**Time Estimate**: 1-2 hours

---

### Phase 1: Cultural Music Knowledge Base (P1)

**Goal**: Create comprehensive database of cultural/regional music characteristics.

**Components**:

1. **Cultural Music Database** (`src/midigent/cultural_music.py`):

```python
@dataclass
class CulturalMusicStyle:
    name: str
    aliases: List[str]  # e.g., ["japanese", "japan", "nihon", "wagaku"]
    scales: List[str]   # Pentatonic, yo, in, etc.
    instruments: List[str]  # Koto, shamisen, shakuhachi, taiko
    typical_tempo_range: Tuple[int, int]
    rhythm_patterns: List[str]
    characteristics: str

CULTURAL_MUSIC_DATABASE: Dict[str, CulturalMusicStyle] = {
    "japanese": CulturalMusicStyle(
        name="Japanese Traditional",
        aliases=["japanese", "japan", "nihon", "wagaku", "japanese traditional"],
        scales=["pentatonic_minor", "yo_scale", "in_scale", "hirajoshi"],
        instruments=["koto", "shamisen", "shakuhachi", "taiko"],
        typical_tempo_range=(60, 100),
        rhythm_patterns=["ma", "jo_ha_kyu"],
        characteristics="Emphasis on ma (silence), nature-inspired, pentatonic"
    ),
    "carnatic": CulturalMusicStyle(...),
    "sufi": CulturalMusicStyle(...),
    # ... 50+ more styles
}
```

2. **Cultural Detector**:

```python
class CulturalMusicDetector:
    def detect(self, prompt: str) -> Optional[CulturalMusicStyle]:
        """Detect cultural music style from user prompt."""
        prompt_lower = prompt.lower()
        
        for style_key, style in CULTURAL_MUSIC_DATABASE.items():
            if any(alias in prompt_lower for alias in style.aliases):
                return style
        
        return None
```

3. **Occasion Detector**:

```python
OCCASION_MUSIC_MAP = {
    "party": {"energy": "high", "tempo_range": (120, 140), "genre": "electronic"},
    "meditation": {"energy": "low", "tempo_range": (60, 75), "genre": "ambient"},
    "cinema": {"energy": "medium", "tempo_range": (70, 100), "genre": "cinematic"},
    "workout": {"energy": "high", "tempo_range": (130, 160), "genre": "electronic"},
    # ... more occasions
}

class OccasionDetector:
    def detect(self, prompt: str) -> Optional[Dict[str, Any]]:
        """Detect occasion/use-case from prompt."""
        prompt_lower = prompt.lower()
        
        for occasion, config in OCCASION_MUSIC_MAP.items():
            if occasion in prompt_lower:
                return {"occasion": occasion, **config}
        
        return None
```

**Deliverable**: 
- `src/midigent/cultural_music.py` with 50+ styles
- Unit tests for cultural detection
- Occasion-based music mapping

**Time Estimate**: 3-4 hours

---

### Phase 2: Enhanced Intent Parser (P1)

**Goal**: Extract track count, detect culture, detect occasion, pass to track planner.

**Changes to `src/midigent/intent_parser.py`** (extract from app.py):

```python
class IntentParser:
    def __init__(self):
        self.cultural_detector = CulturalMusicDetector()
        self.occasion_detector = OccasionDetector()
        self.track_planner = TrackPlanner()
        # ... existing init
    
    def parse(self, user_input: str, session: Optional[CompositionSession] = None) -> Dict[str, Any]:
        """Enhanced parsing with cultural awareness."""
        
        # 1. Extract explicit track count
        track_count = self._extract_track_count(user_input)
        
        # 2. Detect cultural context
        cultural_style = self.cultural_detector.detect(user_input)
        
        # 3. Detect occasion
        occasion_config = self.occasion_detector.detect(user_input)
        
        # 4. Determine genre (from culture, occasion, or keyword)
        genre = self._determine_genre(cultural_style, occasion_config, user_input)
        
        # 5. Get track plan with cultural/occasion influence
        track_plan = self.track_planner.plan_tracks(
            user_input,
            genre=genre,
            requested_count=track_count,
            cultural_style=cultural_style,
            occasion=occasion_config.get("occasion") if occasion_config else None
        )
        
        # 6. Build result with all context
        result = {
            "track_count": len(track_plan),  # CRITICAL: Explicit count
            "track_plan": track_plan,
            "genre": genre,
            "cultural_style": cultural_style.name if cultural_style else None,
            "occasion": occasion_config.get("occasion") if occasion_config else None,
            # ... other params
        }
        
        # Apply cultural tempo/energy overrides
        if cultural_style:
            result["tempo"] = result.get("tempo") or random.randint(*cultural_style.typical_tempo_range)
        
        if occasion_config:
            result["energy"] = occasion_config.get("energy", result.get("energy"))
            if not result.get("tempo"):
                result["tempo"] = random.randint(*occasion_config["tempo_range"])
        
        return result
    
    def _extract_track_count(self, text: str) -> Optional[int]:
        """Extract explicit track count from prompt."""
        # Match: "5 track", "six tracks", "5-track", etc.
        patterns = [
            r'(\d+)\s*track',
            r'(one|two|three|four|five|six|seven|eight)\s*track',
        ]
        
        number_words = {
            "one": 1, "two": 2, "three": 3, "four": 4,
            "five": 5, "six": 6, "seven": 7, "eight": 8
        }
        
        text_lower = text.lower()
        
        for pattern in patterns:
            match = re.search(pattern, text_lower)
            if match:
                value = match.group(1)
                if value.isdigit():
                    return int(value)
                elif value in number_words:
                    return number_words[value]
        
        return None
```

**Deliverable**:
- Enhanced `IntentParser` with cultural/occasion detection
- Track count extraction
- Unit tests for all extraction methods

**Time Estimate**: 2-3 hours

---

### Phase 3: Enhanced Track Planner (P1)

**Goal**: Respect requested track count, select culturally-appropriate instruments.

**Changes to `src/midigent/track_planner.py`**:

```python
class TrackPlanner:
    def plan_tracks(self, user_prompt: str, genre: str,
                   requested_count: Optional[int] = None,
                   cultural_style: Optional[CulturalMusicStyle] = None,
                   occasion: Optional[str] = None) -> List[TrackConfig]:
        """Plan tracks with cultural awareness and explicit count."""
        
        if self.client:
            plan = self._plan_with_ai(
                user_prompt, genre, requested_count, cultural_style, occasion
            )
        else:
            plan = self._plan_with_rules(
                user_prompt, genre, requested_count, cultural_style, occasion
            )
        
        # Validate and adjust
        if requested_count:
            plan = self._ensure_track_count(plan, requested_count, genre, cultural_style)
        
        return plan
    
    def _plan_with_ai(self, user_prompt: str, genre: str,
                     requested_count: Optional[int],
                     cultural_style: Optional[CulturalMusicStyle],
                     occasion: Optional[str]) -> List[TrackConfig]:
        """Enhanced AI planning with cultural context."""
        
        # Build cultural context for AI
        cultural_context = ""
        if cultural_style:
            instruments = ", ".join(cultural_style.instruments)
            cultural_context = f"\nCultural Style: {cultural_style.name}\nTraditional Instruments: {instruments}\nScales: {', '.join(cultural_style.scales)}"
        
        occasion_context = ""
        if occasion:
            occasion_context = f"\nOccasion/Use-case: {occasion}"
        
        track_count_requirement = ""
        if requested_count:
            track_count_requirement = f"\nREQUIRED TRACK COUNT: Exactly {requested_count} tracks"
        
        system_prompt = f"""Analyze this music request and determine the optimal track configuration.
Return ONLY valid JSON (no markdown, no explanation):
{{
  "total_tracks": <1-8>,
  "tracks": [
    {{"type": "<lead|counter_melody|harmony|bass|drums|arpeggio|pad|fx>", "instrument": "<instrument>", "role": "<purpose>", "priority": <1-8>}}
  ]
}}

Rules:
- MUST return EXACTLY the requested number of tracks if specified
- Match instruments to genre AND cultural style
- Types: lead (melody), counter_melody, harmony (chords), bass, drums, arpeggio, pad, fx
{cultural_context}
{occasion_context}
{track_count_requirement}"""

        # ... rest of AI logic
    
    def _ensure_track_count(self, plan: List[TrackConfig], 
                           requested_count: int,
                           genre: str,
                           cultural_style: Optional[CulturalMusicStyle]) -> List[TrackConfig]:
        """Ensure plan has exactly requested_count tracks."""
        
        current_count = len(plan)
        
        if current_count == requested_count:
            return plan
        
        elif current_count < requested_count:
            # Add tracks
            additional_needed = requested_count - current_count
            for i in range(additional_needed):
                # Add appropriate filler tracks
                track_type = self._get_next_track_type(plan, genre)
                instrument = self._get_appropriate_instrument(track_type, genre, cultural_style)
                plan.append(TrackConfig(
                    track_type=track_type,
                    instrument=instrument,
                    role=f"Additional {track_type}",
                    priority=current_count + i + 1,
                    channel=(current_count + i) % 9
                ))
        
        else:
            # Remove lowest priority tracks
            plan = sorted(plan, key=lambda t: t.priority)[:requested_count]
        
        return plan
    
    def _get_appropriate_instrument(self, track_type: str, genre: str,
                                    cultural_style: Optional[CulturalMusicStyle]) -> str:
        """Select culturally-appropriate instrument."""
        
        if cultural_style:
            # Map track types to cultural instruments
            if track_type == "lead" and len(cultural_style.instruments) > 0:
                return cultural_style.instruments[0]  # Primary melodic instrument
            elif track_type == "drums" and len(cultural_style.instruments) > 1:
                # Look for percussion
                for inst in cultural_style.instruments:
                    if any(perc in inst.lower() for perc in ["drum", "tabla", "taiko", "percussion"]):
                        return inst
            elif track_type == "harmony" and len(cultural_style.instruments) > 2:
                return cultural_style.instruments[1]  # Secondary instrument for harmony
        
        # Fallback to genre-based defaults
        return self._get_default_instrument_for_type(track_type, genre)
```

**Deliverable**:
- Enhanced track planner with cultural instrument selection
- Track count validation and adjustment
- Unit tests

**Time Estimate**: 2-3 hours

---

### Phase 4: Section Structure Generator (P2)

**Goal**: Define musical sections with varying energy/density levels.

**New file**: `src/midigent/section_structure.py`

```python
@dataclass
class Section:
    """Musical section definition."""
    name: str  # intro, verse, chorus, bridge, outro
    start_bar: int
    end_bar: int
    energy_level: float  # 0.0-1.0 (relative intensity)
    density_level: float  # 0.0-1.0 (how many notes/tracks active)
    characteristics: Dict[str, Any]  # {build: True}, {fade: True}, {peak: True}, etc.

class SectionStructureGenerator:
    """Generate song structure based on duration."""
    
    def generate_structure(self, total_bars: int, genre: str, 
                          cultural_style: Optional[CulturalMusicStyle] = None) -> List[Section]:
        """Create section structure for composition."""
        
        if total_bars <= 16:  # Short (< 1 minute)
            return self._short_structure(total_bars)
        elif total_bars <= 32:  # Standard (~2 minutes)
            return self._standard_structure(total_bars, genre)
        elif total_bars <= 64:  # Medium (~4 minutes)
            return self._medium_structure(total_bars, genre)
        else:  # Long (> 4 minutes)
            return self._extended_structure(total_bars, genre)
    
    def _standard_structure(self, total_bars: int, genre: str) -> List[Section]:
        """Standard song structure: Intro-Verse-Chorus-Bridge-Outro."""
        return [
            Section("intro", 0, 8, 0.4, 0.5, {"build": True}),
            Section("verse", 8, 16, 0.6, 0.7, {}),
            Section("chorus", 16, 24, 0.9, 0.9, {"peak": True}),
            Section("bridge", 24, 28, 0.7, 0.6, {"contrast": True}),
            Section("outro", 28, 32, 0.5, 0.5, {"fade": True})
        ]
    
    # ... other structure methods
```

**Deliverable**:
- Section structure generator with 4 duration templates
- Energy/density curves for each section type
- Unit tests

**Time Estimate**: 2-3 hours

---

### Phase 5: Multi-Track Generator with Section Awareness (P2)

**Goal**: Generate notes for EACH track in EACH section, with variations.

**Changes to `app.py` and `src/midigent/music_generator.py`**:

```python
class MidiGenApp:
    def _generate_tracks_from_plan(self, track_plan: List[TrackConfig], 
                                   root: int, mode: str, total_bars: int,
                                   energy: str, genre: str,
                                   cultural_style: Optional[CulturalMusicStyle] = None) -> List[Track]:
        """Generate tracks with section-based variations."""
        
        # 1. Generate section structure
        sections = self.section_generator.generate_structure(total_bars, genre, cultural_style)
        
        print(f"🎵 Generating {len(track_plan)} tracks with {len(sections)} sections...")
        
        tracks = []
        
        # 2. For EACH track in plan
        for i, config in enumerate(track_plan):
            print(f"  Track {i+1}/{len(track_plan)}: {config.track_type} - {config.instrument}")
            
            # Assign channel
            channel = 9 if config.track_type == "drums" else (i % 9)
            if channel == 9 and config.track_type != "drums":
                channel = (channel + 1) % 16
            
            # Get instrument program (culturally-aware if applicable)
            instrument = config.instrument.lower().replace(" ", "_")
            program = GM_INSTRUMENTS.get(instrument, 0)
            
            # 3. Generate notes FOR EACH SECTION
            all_notes = []
            for section in sections:
                section_notes = self._generate_section_notes(
                    config, section, root, mode, genre, energy, cultural_style
                )
                all_notes.extend(section_notes)
            
            print(f"    Generated {len(all_notes)} notes across {len(sections)} sections")
            
            # 4. Apply humanization
            all_notes = self.humanizer.humanize_notes(all_notes, config.track_type)
            
            # 5. Create track
            track = Track(
                name=f"{config.instrument.title()} ({config.track_type})",
                notes=all_notes,
                midi_program=program,
                channel=channel,
                track_type=config.track_type
            )
            
            tracks.append(track)
        
        print(f"✓ Total tracks generated: {len(tracks)}")
        return tracks
    
    def _generate_section_notes(self, config: TrackConfig, section: Section,
                                root: int, mode: str, genre: str, 
                                base_energy: str,
                                cultural_style: Optional[CulturalMusicStyle]) -> List[Note]:
        """Generate notes for one track in one section."""
        
        # Calculate section-specific parameters
        section_bars = section.end_bar - section.start_bar
        section_energy = self._blend_energy(base_energy, section.energy_level)
        section_density = section.density_level
        
        # Adjust based on section characteristics
        if "build" in section.characteristics:
            section_density *= 0.7  # Fewer notes in intro
        elif "fade" in section.characteristics:
            section_density *= 0.6  # Fewer notes in outro
        elif "peak" in section.characteristics:
            section_energy = "high"
            section_density *= 1.1  # More notes in chorus
        elif "contrast" in section.characteristics:
            # Use contrasting scale/mode
            mode = self._get_contrasting_mode(mode)
        
        # Use cultural scale if available
        if cultural_style:
            scale = cultural_style.scales[0] if cultural_style.scales else mode
        else:
            scale = mode
        
        # Generate notes based on track type
        if config.track_type == "lead":
            notes = self.generator.generate_melody(
                root, scale, section_bars, section_energy, genre, density=section_density
            )
        elif config.track_type == "counter_melody":
            notes = self.generator.generate_counter_melody(
                root, scale, section_bars, section_energy, density=section_density
            )
        elif config.track_type == "harmony":
            notes = self.generator.generate_chords(
                root, genre, section_bars, density=section_density
            )
        elif config.track_type == "bass":
            notes = self.generator.generate_bass(
                root, genre, section_bars, section_energy, density=section_density
            )
        elif config.track_type == "drums":
            notes = self.generator.generate_drums(
                genre, section_bars, section_energy, cultural_style=cultural_style
            )
        elif config.track_type == "arpeggio":
            notes = self.generator.generate_arpeggio(
                root, genre, section_bars, section_energy, density=section_density
            )
        elif config.track_type == "pad":
            notes = self.generator.generate_pad(
                root, scale, section_bars, density=section_density
            )
        elif config.track_type == "fx":
            notes = self.generator.generate_fx(
                root, section_bars, density=section_density
            )
        else:
            notes = []
        
        # Offset notes to section start time
        section_offset = section.start_bar * 4  # Convert bars to beats
        for note in notes:
            note.start_time += section_offset
        
        return notes
    
    def _blend_energy(self, base_energy: str, section_energy_level: float) -> str:
        """Convert section energy level to energy string."""
        if section_energy_level < 0.4:
            return "low"
        elif section_energy_level < 0.7:
            return "medium"
        else:
            return "high"
```

**Deliverable**:
- Section-aware track generation
- All tracks vary across sections
- Debug logging for track count verification

**Time Estimate**: 3-4 hours

---

### Phase 6: Humanization Engine (P2)

**Goal**: Add micro-timing and velocity variations to make music sound human-played.

**New file**: `src/midigent/humanizer.py`

```python
import random
from typing import List
from dataclasses import dataclass

@dataclass
class HumanizationConfig:
    """Configuration for humanization parameters."""
    timing_variance: float = 0.03  # ±30ms at 120 BPM (in beats)
    velocity_variance: int = 10    # ±10 MIDI velocity units
    swing_amount: float = 0.05     # Swing timing offset
    accent_boost: float = 1.2      # Downbeat velocity multiplier
    duration_variance: float = 0.05  # Duration variation

class HumanizationEngine:
    """Add human-like variations to MIDI notes."""
    
    def __init__(self, config: HumanizationConfig = None):
        self.config = config or HumanizationConfig()
    
    def humanize_notes(self, notes: List[Note], track_type: str) -> List[Note]:
        """Apply humanization to all notes."""
        
        if not notes:
            return notes
        
        # Apply different humanization strategies based on track type
        if track_type == "drums":
            notes = self._humanize_drums(notes)
        elif track_type in ["lead", "counter_melody"]:
            notes = self._humanize_melody(notes)
        elif track_type == "bass":
            notes = self._humanize_bass(notes)
        else:
            notes = self._humanize_generic(notes)
        
        return notes
    
    def _humanize_generic(self, notes: List[Note]) -> List[Note]:
        """Generic humanization for any track."""
        
        for i, note in enumerate(notes):
            # 1. Micro-timing variations (Gaussian distribution)
            timing_offset = random.gauss(0, self.config.timing_variance)
            note.start_time += timing_offset
            
            # 2. Velocity variations
            velocity_offset = int(random.gauss(0, self.config.velocity_variance))
            note.velocity = max(30, min(120, note.velocity + velocity_offset))
            
            # 3. Downbeat accents
            if note.start_time % 4.0 < 0.1:  # On downbeat
                note.velocity = min(127, int(note.velocity * self.config.accent_boost))
            
            # 4. Duration variations
            duration_offset = random.gauss(0, self.config.duration_variance)
            note.duration = max(0.1, note.duration + duration_offset)
        
        return notes
    
    def _humanize_melody(self, notes: List[Note]) -> List[Note]:
        """Humanization specific to melody tracks."""
        
        notes = self._humanize_generic(notes)
        
        # Add expressive velocity curves
        for i, note in enumerate(notes):
            progress = i / len(notes)
            
            # Crescendo in first quarter
            if progress < 0.25:
                note.velocity = int(note.velocity * (0.7 + 0.3 * (progress * 4)))
            
            # Decrescendo in last quarter
            elif progress > 0.75:
                note.velocity = int(note.velocity * (1.0 - 0.3 * ((progress - 0.75) * 4)))
        
        return notes
    
    def _humanize_drums(self, notes: List[Note]) -> List[Note]:
        """Humanization specific to drum tracks."""
        
        for note in notes:
            # Drums need tighter timing but more velocity variation
            timing_offset = random.gauss(0, self.config.timing_variance * 0.5)
            note.start_time += timing_offset
            
            # Hi-hats have more velocity variation
            if 42 <= note.pitch <= 46:  # Hi-hat range
                velocity_offset = int(random.gauss(0, self.config.velocity_variance * 1.5))
            else:
                velocity_offset = int(random.gauss(0, self.config.velocity_variance))
            
            note.velocity = max(30, min(120, note.velocity + velocity_offset))
            
            # Add swing to offbeats
            beat_position = note.start_time % 1.0
            if 0.45 < beat_position < 0.55:  # On the offbeat
                note.start_time += self.config.swing_amount
        
        return notes
    
    def _humanize_bass(self, notes: List[Note]) -> List[Note]:
        """Humanization specific to bass tracks."""
        
        notes = self._humanize_generic(notes)
        
        # Bass notes need groove (slight swing)
        for note in notes:
            beat_position = note.start_time % 1.0
            if 0.4 < beat_position < 0.6:  # Offbeat
                note.start_time += self.config.swing_amount * 0.5
        
        return notes
```

**Deliverable**:
- Humanization engine with track-type-specific logic
- Timing, velocity, duration variations
- Unit tests

**Time Estimate**: 2-3 hours

---

### Phase 7: Integration & Testing (P1)

**Goal**: Wire everything together and test with diverse prompts.

**Integration Steps**:

1. **Update `app.py`**:
   - Import new modules
   - Initialize `SectionStructureGenerator` and `HumanizationEngine`
   - Update `process_message()` to use enhanced parsing
   - Pass cultural context through generation pipeline

2. **Add debug logging**:
   - Track count at each step
   - Section generation
   - Per-track, per-section note counts
   - Final MIDI track count

3. **Test Cases**:

```python
# Test 1: Track count accuracy
"5 track pop music" → Should generate exactly 5 tracks

# Test 2: Cultural detection
"6 track Japanese music" → Should use koto, shamisen, taiko, etc.

# Test 3: Occasion detection
"party music" → Should be upbeat, high energy

# Test 4: Combined
"5 track Carnatic music for meditation 2 minutes" → 5 tracks, Indian classical instruments, calm, 2 min

# Test 5: Section variation
Generate 2-minute track, verify:
- Intro (bars 0-8) is quieter/simpler
- Chorus (bars 16-24) is louder/fuller
- Bridge (bars 24-28) uses different harmony
- Outro (bars 28-32) fades out
- ALL tracks participate in changes

# Test 6: Humanization
Examine MIDI file, verify:
- Note timings vary (not perfectly quantized)
- Velocities vary (not all 80)
- Downbeats are accented
```

**Deliverable**:
- Fully integrated system
- All test cases passing
- Documentation updated

**Time Estimate**: 3-4 hours

---

## Testing Strategy

### Unit Tests

```python
# tests/test_cultural_music.py
def test_japanese_detection():
    detector = CulturalMusicDetector()
    assert detector.detect("Japanese music").name == "Japanese Traditional"
    assert detector.detect("japan traditional").name == "Japanese Traditional"

def test_occasion_detection():
    detector = OccasionDetector()
    assert detector.detect("party music")["occasion"] == "party"
    assert detector.detect("meditation")["energy"] == "low"

# tests/test_intent_parser.py
def test_track_count_extraction():
    parser = IntentParser()
    assert parser._extract_track_count("5 track pop") == 5
    assert parser._extract_track_count("six tracks") == 6
    assert parser._extract_track_count("generate music") is None

# tests/test_section_structure.py
def test_standard_structure():
    generator = SectionStructureGenerator()
    sections = generator.generate_structure(32, "pop")
    assert len(sections) == 5
    assert sections[0].name == "intro"
    assert sections[2].name == "chorus"
    assert sections[2].energy_level > sections[0].energy_level

# tests/test_humanizer.py
def test_timing_variation():
    humanizer = HumanizationEngine()
    notes = [Note(60, 0.0, 1.0, 80) for _ in range(10)]
    humanized = humanizer.humanize_notes(notes, "lead")
    
    # Check that notes are no longer perfectly aligned
    timings = [n.start_time for n in humanized]
    assert len(set(timings)) > 1  # Not all the same
    
def test_velocity_variation():
    humanizer = HumanizationEngine()
    notes = [Note(60, i * 1.0, 1.0, 80) for i in range(10)]
    humanized = humanizer.humanize_notes(notes, "lead")
    
    # Check that velocities vary
    velocities = [n.velocity for n in humanized]
    assert len(set(velocities)) > 1  # Not all the same
```

### Integration Tests

```python
# tests/test_integration.py
def test_full_generation_track_count():
    app = MidiGenApp()
    _, midi_path, _, _ = app.process_message("5 track pop music", [])
    
    # Load MIDI and verify track count
    midi = mido.MidiFile(midi_path)
    # -1 for tempo track
    assert len(midi.tracks) - 1 == 5

def test_cultural_music_generation():
    app = MidiGenApp()
    _, midi_path, _, _ = app.process_message("Japanese traditional music", [])
    
    # Verify Japanese instruments were used (check track names)
    midi = mido.MidiFile(midi_path)
    track_names = [t.name for t in midi.tracks]
    assert any("koto" in name.lower() or "shamisen" in name.lower() for name in track_names)

def test_section_variation():
    app = MidiGenApp()
    _, midi_path, _, _ = app.process_message("2 minute pop music", [])
    
    # Load and analyze note density per section
    midi = mido.MidiFile(midi_path)
    # ... analyze note density in different time ranges
    # Verify intro has fewer notes than chorus
```

### Manual Testing Checklist

- [ ] "5 track pop" → 5 tracks generated
- [ ] "6 track Japan music" → 6 tracks with Japanese instruments
- [ ] "Japanese traditional music" → Uses koto, shamisen, taiko
- [ ] "Carnatic music" → Uses Indian classical elements
- [ ] "Sufi music" → Uses Middle Eastern scales/instruments
- [ ] "party music" → High energy, upbeat
- [ ] "meditation music" → Calm, ambient
- [ ] "cinema background" → Orchestral, dynamic
- [ ] "2 minute pop" → Has intro, verse, chorus, bridge, outro
- [ ] MIDI files sound natural (not robotic)
- [ ] All tracks participate in section changes

## Success Criteria

1. ✅ **Track count accuracy**: 100% match between requested and generated
2. ✅ **Cultural recognition**: Detects 50+ styles correctly
3. ✅ **Section variation**: Measurable energy/density differences
4. ✅ **Humanization**: Timing variance ±5-20ms, velocity variance ±5-15
5. ✅ **User satisfaction**: Music sounds professional and engaging

## Risks & Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| Groq API unavailable | High | Fallback to rule-based parsing |
| Cultural knowledge incomplete | Medium | Start with top 20 styles, expand over time |
| Humanization too subtle | Low | Make configurable, allow adjustment |
| Performance degradation | Medium | Profile and optimize section generation |
| GM instrument limitations | Low | Document limitations, suggest external soundfonts |

## Next Steps After Implementation

1. Create Gradio UI improvements (cultural style selector dropdown)
2. Add MIDI export with metadata (genre, culture, sections)
3. Create cultural music reference documentation
4. Consider adding audio preview (optional future enhancement)
5. Build example library of generated music from various cultures

---

**Total Estimated Time**: 18-26 hours

**Recommended Approach**: Implement in order (Phase 0 → Phase 7), testing after each phase.

**Critical Path**: Phase 0 (bug fix) → Phase 2 (intent parser) → Phase 3 (track planner) → Phase 5 (multi-track generation)
