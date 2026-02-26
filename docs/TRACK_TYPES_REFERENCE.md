# Track Types & Instruments Reference - text2midi

Complete reference for understanding text2midi's track types, MIDI channels, and instrument assignments.

## Quick Reference Table

| Track | Channel | Typical Instrument | MIDI Program | Best Use | MIDI Range |
|-------|---------|-------------------|--------------|----------|-----------|
| **Melody/Lead** | 1 | Synth Lead, Piano | 33, 5 | Main musical line | 60-84 (C4-C6) |
| **Bass** | 2 | Electric Bass, Sub Synth | 33, 32 | Harmonic foundation | 36-48 (C2-C4) |
| **Drums** | 3 | Drum Kit | 0, 128 | Rhythm foundation | 36-81 (drum map) |
| **Harmony/Pad** | 4 | String Pad, Synth Pad | 5, 50 | Rich texture | 48-72 (C3-C5) |
| **Counter Melody** | 5 | Flute, Bell, Synth | 73, 33 | Interesting secondary | 60-84 (C4-C6) |
| **Arpeggio** | 6 | Guitar, Harp, Bells | 24, 25 | Rhythmic movement | 48-84 (C3-C6) |
| **Pad/Effects** | 7 | Pad, Strings, Choir | 50, 5 | Atmosphere | 36-84 (varies) |
| **Additional** | 8 | Special/Percussion | varies | Texture/interest | varies |

---

## 1. Lead/Melody Track

### Purpose
The main melodic line - what listeners sing along with.

### Characteristics
- **Pitch Range:** C4 to C6 (MIDI 60-84)
- **Density:** Medium-High (1 note every ~0.5-1 beat)
- **Sustain:** Held notes (200ms - 2sec per note)
- **Velocity:** Variable (60-110) for expression

### Best Instruments (VST/DAW)

**Bright & Present:**
```
Ableton:        Wavetable (select "Bright Synth Lead")
Surge XT:       "Fast Decay Lead" or "Bright Arpeggio"
Stock:          Operator → Electric Piano
Best Preset:    "Synth Lead Bright" in any synth
```

**Warm & Musical:**
```
Ableton:        Sampler or Wavetable ("Electric Piano")
Surge XT:       "Warm Keys" or "Ivory Grand"
Stock:          Built-in Piano
Best Preset:    "Warm Piano" or "Mellow Keys"
```

**Orchestral:**
```
Ableton:        Wavetable → Strings or Flute
Surge XT:       "Legato Flute" or "Soprano Sax"
Stock:          Kontakt (if available) → Orchestral Library
Best Preset:    "Solo Violin" or "Flute"
```

### Processing Tips
- **Reverb:** 15-25% (adds space)
- **Delay:** Optional, 1/8 note 20% feedback
- **EQ:** Slight boost at 3-5kHz (presence)
- **Compression:** Subtle (10:1 ratio, 4ms attack)

### Example Prompts
- "Bright piano melody"
- "Solo synth lead with movement"
- "Ethereal flute line"
- "Emotional violin melody"

---

## 2. Bass Track

### Purpose
Foundation and harmonic support - feels the groove.

### Characteristics
- **Pitch Range:** C2 to G3 (MIDI 36-48)
- **Density:** Low-Medium (1 note per 1-2 beats)
- **Sustain:** Longer notes (1-4 beats each)
- **Velocity:** Consistent (70-90)
- **Role:** Supports harmony, drives groove

### Best Instruments

**Deep & Punchy:**
```
Ableton:        Wavetable ("Sub Bass" or "Synth Bass")
Surge XT:       "Analog Saw Bass" or "Retro Sub Bass"
Stock:          Operator → FM Bass
Best Preset:    "Deep Sub" or "Punch Bass"
Settings:       Cutoff 40-60%, Resonance 30-50%
```

**Funky & Present:**
```
Ableton:        Wavetable → "Funky Bass"
Surge XT:       "Funk Bass" or "Bright Bass"
Stock:          Electric Bass sampler
Best Preset:    "Funky Electric Bass"
Settings:       Cutoff 50-70%, Resonance 40-60%
```

**Orchestral/Bowed:**
```
Ableton:        Sampler → Contrabass
Surge XT:       "Deep Strings" (with processing)
Stock:          Kontakt → Orchestral Strings
Best Preset:    "Cello" or "Contrabass"
```

### Processing Tips
- **Reverb:** 10-15% (keep tight)
- **EQ:** Boost 50-100Hz (depth), cut 300Hz (mud)
- **Compression:** Heavy (4:1 ratio, 5ms attack, 30ms release)
- **Saturation:** 5-15% for warmth

### Example Prompts
- "Deep punchy bass"
- "Funky electric bass line"
- "Steady foundational bass"
- "Groove-heavy bass"

---

## 3. Drums Track

### Purpose
Rhythm foundation and drive - the pulse.

### Characteristics
- **Notes Used:** Standard General MIDI Drum Map
- **Density:** High (8-16 notes per 4 bars)
- **Sustain:** Short (50-200ms decay)
- **Velocity:** Variable (60-110)

### MIDI Note Mapping (General MIDI Standard)

```
35   | Acoustic Bass Drum (very deep kick)
36   | Bass Drum 1 (standard kick)
37   | Side Stick (cowbell-like click)
38   | Acoustic Snare (standard snare)
39   | Hand Clap (clap sound)
40   | Electric Snare (snappy snare)
41   | Low Floor Tom (tom)
42   | Closed Hi-Hat (crisp hat)
43   | High Floor Tom (tom)
44   | Pedal Hi-Hat (controlled hat)
45   | Low Tom (tom)
46   | Open Hi-Hat (shimmering hat)
47   | Low-Mid Tom (tom)
48   | High Mid Tom (tom)
49   | Crash Cymbal 1 (crash)
50   | High Tom (tom)
51   | Ride Cymbal 1 (ride)
52   | Chinese Cymbal (textured crash)
53   | Ride Bell (bright ride)
54   | Tambourine (loose, bright)
55   | Splash Cymbal (short crash)
56   | Cowbell (metallic)
```

### Best Instruments

**Acoustic Drums:**
```
Ableton:        Drum Rack + Acoustic Drums (Factory)
Surge XT:       N/A (better in DAW drum plugin)
Stock:          Native drum kits
Best:           Ableton Acoustic Drums kit
```

**Electronic Drums:**
```
Ableton:        Drum Rack + Electronic Drums (Factory)
Surge XT:       "Drums" preset (if available)
Stock:          Electronic drum kits
Best:           Classic 808/909 style kits
```

### Processing Tips
- **Kick:** Compression 6:1, EQ boost at 100Hz
- **Snare:** EQ boost at 5kHz, light reverb 5%
- **Hi-Hat:** EQ boost at 8-12kHz, dry (no reverb)
- **Overall:** Sidechain to kick for pump effect

### Example Prompts
- "Tight electronic drums"
- "Acoustic jazz drums"
- "4-on-the-floor kick with busy hi-hats"
- "Minimal drums: kick and snare"

---

## 4. Harmony/Pad Track

### Purpose
Rich harmonic background - emotional depth and texture.

### Characteristics
- **Pitch Range:** C3 to C5 (MIDI 48-72)
- **Density:** Very Low (1 chord per 4-8 bars)
- **Sustain:** Very Long (4-16 bars per note)
- **Velocity:** Consistent (70-85)
- **Role:** Emotional foundation, warm texture

### Best Instruments

**Lush String Pad:**
```
Ableton:        Wavetable ("String Pad" or "Analog String")
Surge XT:       "Warm Strings" or "Evolving Ambient"
Stock:          String sampler or Kontakt Strings
Best Preset:    "Lush Strings" or "Warm Pad"
```

**Synth Pad:**
```
Ableton:        Wavetable ("Evolving Pad")
Surge XT:       "Ambient Pad" or "Swelling Waves"
Stock:          Any synth pad preset
Best Preset:    "Atmospheric Pad"
```

**Choir/Orchestral:**
```
Ableton:        Sampler (choir sample)
Surge XT:       "Warm Choir" if available
Stock:          Choir samples or Kontakt Choir
Best Preset:    "Ethereal Choir"
```

### Processing Tips
- **Reverb:** 40-60% (crucial for pad texture)
- **Delay:** Optional, 1/4 note, 15-20% feedback
- **Chorus:** 20-30% for width
- **EQ:** Keep warm (boost 1-2kHz, cut 8kHz)
- **Attack:** Slow (500-1000ms fade in)

### Example Prompts
- "Warm lush pad underneath"
- "Ethereal string pad"
- "Ambient evolving pad"
- "Swelling choir pad"

---

## 5. Counter Melody Track

### Purpose
Interesting secondary line - adds sophistication without competing.

### Characteristics
- **Pitch Range:** C4 to C6 (MIDI 60-84)
- **Density:** Low (1 note every 1-2 beats, sparse)
- **Sustain:** Medium (500ms-1sec)
- **Velocity:** Consistent (65-80)
- **Role:** Weave in and out of main melody

### Best Instruments

**Flute/Woodwind:**
```
Ableton:        Sampler or Wavetable ("Flute")
Surge XT:       "Legato Flute" or "Bright Flute"
Stock:          Woodwind sampler
Best Preset:    "Solo Flute" or "Recorder"
```

**Bells/Chimes:**
```
Ableton:        Sampler (bell samples)
Surge XT:       "Bell" or "Bright Bells"
Stock:          Bell samples
Best Preset:    "Vibraphone" or "Bells"
```

**Secondary Synth:**
```
Ableton:        Wavetable ("Soft Lead" or "Bright Pad")
Surge XT:       "Soft Pluck" or "Ethereal Synth"
Stock:          Any bright synth
Best Preset:    "Sparkling Synth"
```

### Processing Tips
- **Reverb:** 20-30% (some space, not too much)
- **EQ:** Keep bright, slight boost at 3kHz
- **Volume:** -3 to -6dB below main melody
- **Pan:** Optional left/right for width

### Example Prompts
- "Gentle flute counter melody"
- "Sparkling bell response"
- "Weaving counter synth"
- "Complementary violin line"

---

## 6. Arpeggio Track

### Purpose
Rhythmic harmonic movement - adds energy and motion.

### Characteristics
- **Pitch Range:** C3 to C6 (MIDI 48-84, varies)
- **Density:** High (continuous or regular pattern)
- **Sustain:** Short (1/4 to 1 beat per note)
- **Velocity:** May vary for expression
- **Role:** Driving groove, rhythmic interest

### Best Instruments

**Guitar Arpeggio:**
```
Ableton:        Sampler (acoustic or electric guitar)
Surge XT:       "Strummed Guitar" or "Clean Nylon"
Stock:          Guitar samples
Best Preset:    "Fingerpicked Guitar"
```

**Harp:**
```
Ableton:        Sampler (harp samples)
Surge XT:       "Ethereal Harp"
Stock:          Harp samples
Best Preset:    "Cascading Harp"
```

**Digital/Synth:**
```
Ableton:        Wavetable ("Bright Arpeggio")
Surge XT:       "Digital Arpeggio" or "Sparkle"
Stock:          Any bright synth
Best Preset:    "Crystalline Arpeggio"
```

### Processing Tips
- **Reverb:** 15-25% (some space)
- **EQ:** Bright, boost 5-8kHz
- **Panning:** Can pan left/right on different notes for width
- **Saturation:** Light (3-5%) for warmth

### Example Prompts
- "Cascading guitar arpeggio"
- "Digital sparkling synth arpeggio"
- "Fingerpicked acoustic guitar"
- "Ethereal harp glissando"

---

## 7. FX/Special Track

### Purpose
Texture and novelty - ear candy and transitions.

### Characteristics
- **Sparse usage** (1-5 notes per 16 bars)
- **Strategic placement** (builds, transitions, fills)
- **Unusual sounds** (reversed, processed, textured)
- **High impact** with minimal presence

### Best Instruments

**Reverse Strings:**
```
Technique: Take a string sample, reverse it in your DAW
Effect: Swelling build-up before chorus drop
Sound: Ethereal, unnatural, attention-grabbing
```

**Impact Hits:**
```
Ableton:        Sampler (impact/whoosh samples)
Sound: Low-pass filtered noise burst
Uses: Transition points, builds
```

**Reverse Cymbal:**
```
Technique: Take a cymbal crash, reverse it and lower pitch
Effect: Creeping, building sensation
Perfect for: Before chorus, before breakdown
```

**Granular/Glitch:**
```
Ableton:        Granulator (advanced)
Surge XT:       Effect processor chain with reverb/delay
Sound: Ethereal, deconstructed, modern
Uses: Avant-garde production, texture fills
```

### Processing Tips
- **Heavy effects:** Reverb 70%+, Delay 30%+
- **EQ:** Shape creatively
- **Automation:** Volume swells, panning moves
- **Timing:** Hit at exact moments (usually beat 1 of new section)

### Example Prompts
- "Add a reverse cymbal swell before the chorus"
- "Impact hit on beat 1"
- "Synth whoosh transition"
- "Ethereal string reverse"

---

## Instrument Selection by Genre

### Pop

**Lead:** Bright synth or piano
**Bass:** Deep sub bass
**Drums:** 4-on-the-floor electronic
**Harmony:** Warm pad (synth or strings)
**Counter:** Optional bell or synth
**Arpeggio:** Not typically
**Result:** DAW Example:
```
Track 1: Piano/Synth Lead (Wavetable)
Track 2: Sub Bass (Wavetable)
Track 3: Drums (Drum Rack)
Track 4: String Pad (Wavetable + Reverb)
```

### Rock/Indie

**Lead:** Electric guitar or edgy synth
**Bass:** Present, groovy bass
**Drums:** Live-feel drums with dynamics
**Harmony:** Guitar chords or pad
**Counter:** Doesn't apply
**Arpeggio:** Strummed guitar pattern
**Result:**
```
Track 1: Electric Guitar Lead (Sampler)
Track 2: Bass (Synth Bass or Sampler)
Track 3: Drums (Live kit)
Track 4: Rhythm Guitar (Sampler, panned)
```

### Electronic/EDM

**Lead:** Digital synth, bright and cutting
**Bass:** Sub bass, heavily processed
**Drums:** Programmed, precise timing
**Harmony:** Synth pad, evolving
**Counter:** Digital FX, sweeps
**Arpeggio:** Synth arpeggio, fast
**Result:**
```
Track 1: Digital Synth Lead (Wavetable/Surge)
Track 2: Sub Bass (Wavetable + Sidechain)
Track 3: Drums (Electronic, tight)
Track 4: Evolving Pad (Surge XT + FX)
Track 5: Synth Arpeggio (Wavetable, fast)
```

### Classical/Orchestral

**Lead:** Violin, flute, or trumpet
**Bass:** Cello or contrabass
**Drums:** Timpani, not electronic
**Harmony:** Full string section
**Counter:** Woodwind counterpoint
**Arpeggio:** Harp arpeggios
**Result:**
```
Track 1: Violin Solo (Sampler/Kontakt)
Track 2: Cello Bass (Sampler)
Track 3: Timpani & Perc (Sampler)
Track 4: String Pad (Sampler)
Track 5: Flute Counter (Sampler)
Track 6: Harp Arpeggio (Sampler)
```

### Lo-Fi

**Lead:** Soft piano or flute
**Bass:** Warm, jazz bass
**Drums:** Jazz-influenced, relaxed
**Harmony:** Warm pad
**Counter:** Vinyl crackle (FX track)
**Arpeggio:** Not typical
**Result:**
```
Track 1: Lo-Fi Piano (Sampler, slight compression)
Track 2: Walking Bass (Sampler)
Track 3: Drums (Swung, relaxed)
Track 4: Warm Pad (Synth)
Track 5: Vinyl Noise (FX - low level)
```

---

## Common Issues & Solutions

### Issue: Track 3 (Drums) not playing drum sounds

**Problem:** Default instrument is generic synth, not drum kit

**Solution:**
1. Click Track 3 and locate instrument slot
2. Change to **Drum Rack** (Ableton) or **Drum Kit** (other DAW)
3. Select **General MIDI drum kit**
4. Notes should now map correctly:
   - 36 = Kick
   - 38 = Snare
   - 42 = Hi-Hat

### Issue: Some tracks too loud/quiet relative to others

**Problem:** Lyra velocities may vary by track type

**Solution:**
```
Expected levels:
- Lead:     -6 to -3dB
- Bass:     -8 to -6dB
- Drums:    -4 to -2dB
- Pad:      -15 to -12dB
- Counter:  -10 to -8dB
```

Adjust faders to these approximate levels.

### Issue: Sound is muddy or unclear

**Problem:** Too many mid-frequency instruments playing simultaneously

**Solution:**
1. **EQ each track:**
   - Cut 300Hz (mud frequency)
   - Boost unique frequencies for each
2. **Pan:** Spread instruments left/right
3. **Volume:** Make quieter to create space
4. **Mute optional tracks** (counter-melody, arpeggio)
5. **Add reverb differently**: Varying amounts create depth

### Issue: Can't find good sound for bass track

**Problem:** Wrong instrument type selected

**Solution:**
- Use **subtractive synth** (Wavetable, Serum, Surge XT)
- Search for presets with "bass" in name
- Set Filter Cutoff to 40-60% (darker sound)
- Boost Resonance 30-50% for punch
- See [Surge XT Guide](DAW_SURGE_XT.md) for detailed recipes

---

## Detailed Audio Example Levels

**Properly mixed track with Lyra:**

```
Master Level: -3dB (headroom)
├─ Lead/Melody:     0dB (reference)
├─ Bass:            -6dB
├─ Drums:           -4dB
├─ Pad/Harmony:     -12dB
├─ Counter Melody:  -9dB
├─ Arpeggio:        -8dB
└─ FX:              -15dB (very subtle)
```

**What each level achieves:**
- Lead at 0dB = Clear, upfront, present
- Bass -6dB = Supports without overwhelming
- Drums -4dB = Drives rhythm, sits well
- Pad -12dB = Background texture, not distracting
- Others: Various levels depending on role

---

**Next:** [Getting Started](GETTING_STARTED.md) | [DAW Guides](DAW_ABLETON_LIVE.md) | [Advanced Synthesis](DAW_SURGE_XT.md)

Happy producing! 🎵
