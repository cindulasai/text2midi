# MIDI Generation Guide - text2midi

Master the art of AI-powered music composition with practical examples and techniques.

## Table of Contents

1. [How MIDI Generation Works](#how-it-works)
2. [Music Theory Basics](#music-theory-basics)
3. [Track Types Explained](#track-types)
4. [Genre Guide](#genres)
5. [Advanced Prompting](#advanced-prompting)
6. [Multi-Turn Composition Workflow](#workflow)

---

## How MIDI Generation Works

### The Generation Pipeline

```
Your Description
       ↓
AI Intent Parser (understands genre, mood, tempo, key)
       ↓
Track Planner (decides how many tracks and types)
       ↓
Music Generator (creates notes for each track)
       ↓
MIDI Creator (converts to standard MIDI format)
       ↓
MIDI File (.mid)
```

### What Happens Behind the Scenes

1. **Intent Parsing**: AI analyzes your description for:
   - **Genre**: pop, rock, electronic, classical, etc.
   - **Tempo**: BPM (beats per minute)
   - **Mood**: energetic, calm, dark, happy
   - **Key**: C, G, D, A, E, B, F#, Db, Ab, Eb, Bb, F
   - **Track Count**: 1-8 depending on complexity

2. **Track Planning**: AI decides:
   - How many tracks to create
   - What instrument for each track
   - Which track type (melody, bass, drums, etc.)
   - Intensity levels for each

3. **Music Generation**: AI creates:
   - Melodies following music theory rules
   - Bass lines with proper progression
   - Drum patterns matching the genre/tempo
   - Harmonies and pads for texture

4. **MIDI Output**: Saved as `.mid` file ready for any DAW

---

## Music Theory Basics

### Keys & Modes

**Major Keys (Happy, Bright)**
```
C major  | 60 MIDI pitch
G major  | 67 MIDI pitch
D major  | 62 MIDI pitch
A major  | 69 MIDI pitch
E major  | 64 MIDI pitch
B major  | 71 MIDI pitch
F# major | 66 MIDI pitch
Db major | 61 MIDI pitch
Ab major | 68 MIDI pitch
Eb major | 63 MIDI pitch
Bb major | 70 MIDI pitch
F major  | 65 MIDI pitch
```

**Minor Keys (Dark, Sad, Introspective)**
```
A minor  | 57 MIDI pitch (relative to C major)
E minor  | 64 MIDI pitch
B minor  | 71 MIDI pitch
F# minor | 66 MIDI pitch
```

**Example Prompt with Key:**
```
Sad classical piece in A minor with piano and strings
```

### Tempo (BPM)

- **Slow (60-100 BPM)**: Ballads, ambient, funeral marches
- **Medium (100-120 BPM)**: Pop, indie, standard listening
- **Fast (120-140 BPM)**: Dance, upbeat pop, electronic
- **Very Fast (140+ BPM)**: Extreme electronic, drum & bass

**In Lyra:**
```
"120 BPM pop song"        → Exactly 120 tempo
"Fast paced electronic"   → ~130-140 BPM
"Slow piano ballad"       → ~70 BPM
```

### Song Structure

**Standard Pop/Rock (16-32 bars)**
```
Intro (4-8 bars)
  ↓
Verse 1 (8-16 bars)
  ↓
Pre-Chorus (4 bars)
  ↓
Chorus (8 bars)
  ↓
Verse 2 (8-16 bars)
  ↓
Chorus (8 bars)
  ↓
Bridge (4-8 bars)
  ↓
Final Chorus (8 bars)
  ↓
Outro (4 bars)
```

**Electronic/Ambient (32-64 bars)**
```
Intro: Minimal (8-16 bars)
  ↓
Build: Layers added (16-32 bars)
  ↓
Peak: Full arrangement (8-16 bars)
  ↓
Outro: Strips down (8-16 bars)
```

---

## Track Types

### Lead/Melody
- **Purpose**: Main melodic line
- **Instruments**: Piano, Synth Lead, Violin, Saxophone
- **MIDI Range**: 60-84 (comfortable vocal range)
- **Density**: Medium-High
- **Use Case**: Melody that listeners sing along to

**Example:**
```
"Piano melody line with emotional phrasing"
Solo: C4-C5 (MIDI 60-72)
```

### Bass
- **Purpose**: Foundation and harmonic support
- **Instruments**: Electric Bass, Bass Synth, Sub Bass
- **MIDI Range**: 36-48 (low frequencies)
- **Density**: Low (1 note every 2 beats)
- **Use Case**: Rhythmic support, groove

**Example:**
```
"Funky electric bass line"
Solo: C2-G2 (MIDI 36-43)
```

### Drums
- **Purpose**: Rhythm and percussion
- **Uses**: Kick, Snare, Hi-Hat, Tom, Cymbal, Perc
- **MIDI Range**: 36-81 (drum kit range)
- **Density**: High
- **Use Case**: Driving the rhythm

**Example:**
```
"Four-on-the-floor kick with tight snare"
Pattern: Kick (36) on 1,3 | Snare (38) on 2,4 | Hi-hat (42) 8th notes
```

### Harmony/Pad
- **Purpose**: Rich harmonic background
- **Instruments**: String Pad, Synth Pad, Warm Piano
- **MIDI Range**: 48-72 (mid-range chords)
- **Density**: Low (sustained notes)
- **Use Case**: Emotional depth, texture

**Example:**
```
"Lush string pad underneath"
Sustained chord: C3-E3-G3 (MIDI 48-52-55) held for 4 bars
```

### Counter-Melody
- **Purpose**: Interesting secondary line
- **Instruments**: Flute, Bells, Synth, Guitar
- **MIDI Range**: 60-84
- **Density**: Low-Medium
- **Use Case**: Interest without competing with main melody

**Example:**
```
"Gentle flute counter melody weaving around the piano"
Complementary notes: 3rd, 4th, 5th scale degrees
```

### Arpeggio
- **Purpose**: Rhythmic harmonic movement
- **Instruments**: Guitar, Harp, Electric Piano
- **MIDI Range**: 48-84
- **Density**: High (broken chord)
- **Use Case**: Adding movement and energy

**Example:**
```
"Cascading guitar arpeggio"
Pattern: C3-E3-G3-C4 repeating at 16th note intervals
```

### FX/Special
- **Purpose**: Texture and novelty
- **Instruments**: Bell Hits, Synth Effects, Reversed Strings
- **Usage**: Sparse, strategic placement
- **Use Case**: Transitions, builds, ear candy

**Example:**
```
"Reverse cymbal swell before the chorus drop"
1-2 notes per section, maximum impact
```

---

## Genres

### Pop
**Characteristics:**
- Tempo: 100-130 BPM
- Structure: Verse-Pre-Chorus-Chorus
- Lead: Catchy melody, often synth or vocal-like
- Bass: Simple, steady pattern
- Drums: 4-on-the-floor kick, snappy snare

**Best Prompt:**
```
"Catchy pop song in E major with upbeat drums, floating synth melody, and walking bass"
```

### Rock/Indie
**Characteristics:**
- Tempo: 110-140 BPM
- Lead: Electric guitar
- Bass: Present and groovy
- Drums: Live-feel, dynamic fills
- Harmony: Guitar chords

**Best Prompt:**
```
"Indie rock with jangly guitar chords, tight rhythm section, and melodic bass line"
```

### Electronic/EDM
**Characteristics:**
- Tempo: 120-180 BPM
- Lead: Digital Synths
- Bass: Sub bass, often side-chained
- Drums: Programmed, tight grid
- Effects: Heavy processing

**Best Prompt:**
```
"Progressive electronic with building layers, deep sub bass, and pulsing synth pad"
```

### Classical/Orchestral
**Characteristics:**
- Tempo: 60-120 BPM (varies)
- Instruments: Strings, Woodwinds, Brass, Timpani
- Structure: Theme and variations
- Dynamics: Crescendos and diminuendos
- Harmony: Complex chord progressions

**Best Prompt:**
```
"Baroque-style orchestral piece in D minor with strings, harpsichord, and subtle brass"
```

### Lo-Fi
**Characteristics:**
- Tempo: 80-100 BPM
- Vibe: Relaxed, nostalgic
- Instruments: Soft piano, warm pads, vinyl crackle
- Drums: Mellow, jazz-influenced
- Key: Often minor keys (A minor, E minor)

**Best Prompt:**
```
"Chill lo-fi beat with vinyl warmth, sleepy piano, and relaxed jazz drums"
```

### Jazz
**Characteristics:**
- Tempo: 90-140 BPM (varies)
- Lead: Saxophone, Piano, or Trumpet
- Bass: Walking bass (jazz standard)
- Drums: Swing feel, dynamic
- Harmony: Interesting chord progressions

**Best Prompt:**
```
"Cool jazz with walking bass, swinging drums, and warm saxophone over piano"
```

### Ambient
**Characteristics:**
- Tempo: 60-90 BPM
- Vibe: Atmospheric, meditative
- Instruments: Pads, Drones, Minimal melody
- Dynamics: Subtle changes
- Structure: No traditional form

**Best Prompt:**
```
"Ambient soundscape with layered pads, subtle bass movement, and sparse strings"
```

### Cinematic
**Characteristics:**
- Tempo: 80-120 BPM
- Instruments: Full Orchestra, Choir
- Dynamics: Dramatic crescendos
- Structure: Narrative arc
- Emotion: Epic, emotional, grand

**Best Prompt:**
```
"Epic cinematic with soaring strings, powerful brass, and thunderous drums"
```

---

## Advanced Prompting

### Technique 1: Emotion + Genre + Key + Tempo

```
Format:
[Emotion] [Genre] in [Key] at [Tempo] BPM with [instrumentation]

Examples:
- "Melancholic indie rock in E minor at 110 BPM with jangly guitars and warm bass"
- "Joyful pop in D major at 128 BPM with synth lead, tight drums, and funky bass"
- "Dark cinematic in F# minor at 90 BPM with strings, choir, and storm drums"
```

### Technique 2: Reference + Modification

```
Format:
[Reference sound] influenced by [artist/style] but with [modification]

Examples:
- "Piano ballad inspired by Elton John but more modern and electronic"
- "Funk track inspired by Jamiroquai but with more soulful strings"
- "Ambient piece inspired by Brian Eno but with ethnic instruments and vocals"
```

### Technique 3: Scene/Context Painting

```
Format:
[Musical scene] for [context/mood]

Examples:
- "Uplifting music for a sunrise scene with warm guitars and swelling pads"
- "Dark mysterious music for a heist scene with twisted synths and pulsing bass"
- "Peaceful music for meditation with ethereal vocals, sitar, and gongs"
```

### Technique 4: Layer Instructions

```
Format:
Start with [base] then add [layer 2], then add [layer 3]

Examples:
- "Start with warm piano, then add walking bass, then add swinging drums"
- "Start with sub bass drone, then add synth lead, then add ambient pads"
(Can be done in multiple turns for more control)
```

### Technique 5: Specific Bar Breakdown

```
Format:
[Bars 1-4]: [section description]
[Bars 5-8]: [section description]
etc.

Examples:
- "Bars 1-4: Minimal bass and drums, Bars 5-8: Add piano, Bars 9-12: Full arrangement"
- "Bars 1-2: Intro with just strings, Bars 3-6: Main verse with bass, Bars 7-8: Chorus with full section"
```

---

## Multi-Turn Composition Workflow

### The Iterative Process

**Turn 1: Generate Foundation**
```
Prompt: "Upbeat pop song in G major"
Result: 5-8 tracks with basic arrangement
Duration: ~20 seconds
```

**Turn 2: Add Detail**
```
Prompt: "Make the drums more interesting with more fills"
Result: Enhanced drum patterns
Duration: ~15 seconds
```

**Turn 3: Adjust Energy**
```
Prompt: "Reduce the tempo by 10 BPM and make it more groovy"
Result: Slower, funkier version
Duration: ~15 seconds
```

**Turn 4: Add Instrumentation**
```
Prompt: "Add a warm string pad underneath everything"
Result: Same tracks + new pad layer
Duration: ~15 seconds
```

**Turn 5: Final Polish**
```
Prompt: "Add a 2-bar string swell before the final chorus"
Result: Production touch added
Duration: ~10 seconds
```

### Example: Building a Complete Track

**Goal:** Create an uplifting pop anthem over 5 turns

**Turn 1 - Basic Structure**
```
Prompt: "Upbeat pop song in D major with bright energy, 4 tracks"
Generated:
- Synth lead melody
- Electric bass
- Drum kit (kick, snare, hi-hat)
- String pad (harmony)
```

**Turn 2 - Better Drums**
```
Prompt: "Make the drums pop more with more snare presence and open hats"
Generated:
- Same as above but with snappier drum sound
```

**Turn 3 - Add Interest**
```
Prompt: "Add a counter-melody on flute that plays between the main synth"
Generated:
- Original 4 tracks +
- Flute counter-melody
```

**Turn 4 - Build Section**
```
Prompt: "Create a 4-bar build section with just bass and drums getting more intense"
Generated:
- New track with isolated build section
- Can be spliced in at bar 32
```

**Turn 5 - Final Chorus**
```
Prompt: "Full arrangement for final chorus with all instruments and a brass hit on beat 1"
Generated:
- Dense, explosive final chorus
```

**Result:** Complete 48-64 bar pop song perfect for further production

---

## Exporting for Your DAW

### Format Details

Lyra exports **Standard MIDI Files (SMF)**:
- **Format**: .mid (Type 0 or Type 1)
- **Resolution**: 480 PPQ (ticks per quarter note)
- **Format**: Compatible with ALL DAWs

### What Gets Exported

Each MIDI file contains:
- **Tempo track** with BPM information
- **Time signature** (usually 4/4)
- **MIDI channel assignments** (Channel 1-8 per track)
- **Program changes** for instrument selection
- **Note data** with pitch, velocity, duration

### Import into Your DAW

See specific guides:
- [Ableton Live Lite](DAW_ABLETON_LIVE.md)
- [Surge XT](DAW_SURGE_XT.md)
- [FL Studio](DAW_FL_STUDIO.md)
- [Logic Pro / GarageBand](DAW_LOGIC.md)

---

**Next:** Learn how to import and enhance your creations in [DAW Integration Guides](DAW_ABLETON_LIVE.md)

Happy composing! 🎵
