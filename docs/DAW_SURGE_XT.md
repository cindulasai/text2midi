# Using text2midi with Surge XT (Advanced Synthesis Guide)

Learn advanced synthesis techniques to transform text2midi MIDI into stunning soundscapes using Surge XT - the professional free synthesizer.

## Table of Contents

1. [Surge XT Basics](#basics)
2. [Installation & Setup](#setup)
3. [Using Surge XT with Lyra MIDI](#workflow)
4. [Sound Design Recipes](#recipes)
5. [Advanced Synthesis](#advanced)
6. [Performance Tips](#tips)

---

## Basics

### What is Surge XT?

**Surge XT** is a professional-grade FREE synthesizer:
- **Wavetable synthesis** - Create custom tones
- **FM synthesis** - Complex, evolving sounds
- **Subtractive synthesis** - Classic sound design
- **Effects** - Distortion, reverb, delay, chorus
- **Modulation systems** - LFOs, envelopes, sequencers
- **Preset library** - 3000+ presets included

## Why Surge XT + text2midi?

**text2midi provides:**
- Melodies and musical ideas
- Timing and structure
- Multiple tracks

**Surge XT provides:**
- Professional instruments
- Deep sound customization
- Effects and processing
- Much better than stock DAW sounds

**Result:** Professional-sounding tracks in minutes!

---

## Installation & Setup

### Download Surge XT

1. Go to [surge-synthesizer.github.io](https://surge-synthesizer.github.io)
2. Click **Download**
3. Choose your OS (Windows, Mac, Linux)
4. **Select VST3 plugin version** (most compatible)
5. Install and restart your DAW

### Add Surge XT to Your DAW

**In Ableton Live:**
1. **Right-click** in track's instrument slot
2. **Select Audio Effects → Max for Live → Plug-in Device**
3. Choose **Surge XT** from the list
4. **Done!** It's ready to use

**In FL Studio:**
1. **Insert → More Plugins → Surge XT**
2. Done!

**In Logic Pro:**
1. **Smart Controls → Plug-in → Surge XT**
2. Done!

---

## Using Surge XT with text2midi

### Basic Workflow

```
Generate MIDI in text2midi
    ↓
Import into your DAW
    ↓
Replace track instrument with Surge XT
    ↓
Choose a preset matching the track type
    ↓
Tweak for your taste
    ↓
Add effects (reverb, delay, etc.)
    ↓
Export as audio
```

### Quick Start: 3 Steps to Great Sound

**Step 1: Load Surge XT**
- Drag your text2midi MIDI to a track
- Double-click the instrument slot
- Select **Surge XT** from VST list
- Click **Load**

**Step 2: Choose a Preset**
- Surge opens with a random preset
- Click **← → arrows** to browse presets
- Look for presets named:
  - **Lead**: Bright, sharp, focused
  - **Bass**: Deep, punchy, focused
  - **Pad**: Lush, evolving, atmospheric
  - **Strings**: Orchestral, warm
  - **Synth**: Modern, electronic

**Step 3: Tweak to Taste**
- **Volume:** Slider on right side
- **Resonance Filter:** Makes lead sounds pop
- **Release Time:** How long sound lasts after note ends
- **Listen and adjust**

### Detailed Walkthrough

#### For Lead/Melody Tracks

**Goal:** Bright, cutting sound that sits on top of mix

**Step 1: Open Surge XT on your melody track**

**Step 2: Find a good Lead preset**
- Browse: **Pluck** → **Fast Decay Lead**
- Or: **Synth** → **Bright Arpeggio**
- Or: **Keys** → **Electric Piano**

**Step 3: Customize**
```
Filter Cutoff:    70-80% (keeps it bright)
Filter Resonance: 20-40% (adds character/edge)
Amp Envelope:
  - Attack:  0-20ms (fast, punchy)
  - Release: 100-300ms (quick decay)
```

**Step 4: Add effects**
- Right-click on FX Aux area
- Add: **Reverb** (20-30%)
- Add: **EQ** (boost 3kHz for presence)

**Result:** Punchy, cutting lead that shines

#### For Bass Tracks

**Goal:** Deep, solid foundation with movement

**Step 1: Open Surge XT on bass track**

**Step 2: Find a Bass preset**
- Browse: **Bass** → **Analog Saw Bass**
- Or: **Synth** → **Retro Sub Bass**
- Or: **Sub** → **Deep Sub**

**Step 3: Customize**
```
Filter Cutoff:    40-60% (keeps it deep/dark)
Filter Resonance: 30-60% (adds punch and movement)
Amp Envelope:
  - Attack:  5-10ms (tight)
  - Sustain: 100% (held throughout note)
  - Release: 50-100ms (quick)
Octave:           -2 (down 2 octaves, really deep)
```

**Step 4: Add effects**
- Add: **Distortion** (10-20% subtle crunch)
- Add: Compression (not shown but implied)

**Result:** Professional, deep bass that drives the song

#### For Pad/Harmony Tracks

**Goal:** Lush, evolving, atmospheric

**Step 1: Open Surge XT on pad track**

**Step 2: Find a Pad preset**
- Browse: **Pad** → **Evolving Ambient**
- Or: **Pad** → **Swelling Waves**
- Or: **Wavetable** → **Evolving Pad**

**Step 3: Customize**
```
Filter Cutoff:    100% (let all harmonics through)
Filter Resonance: 10-30% (subtle movement)
Amp Envelope:
  - Attack:  500-1000ms (slow fade in)
  - Sustain: 100% (held throughout)
  - Release: 2000-3000ms (long, luscious tail)
Unison Voices:    5-7 (adds thickness)
Unison Detune:    20-40% (adds movement)
```

**Step 4: Add effects**
- Add: **Reverb** (50-70% for space)
- Add: **Delay** (1/4 note, 25% feedback for texture)
- Add: **Chorus** (10-20% for width)

**Result:** Lush, modern, professional-sounding pad

#### For String/Orchestral Tracks

**Goal:** Warmth, humanity, emotive

**Step 1: Open Surge XT**

**Step 2: Choose a String preset**
- Browse: **Strings** → **Warm Strings**
- Or: **Orchestral** → **Legato Strings**
- Or: **Keys** → **Orchestra**

**Step 3: Customize**
```
Filter Cutoff:    80-100% (open, warm)
Filter Resonance: 20% (subtle!)
Amp Envelope:
  - Attack:  300-500ms (slower, more orchestral)
  - Release: 1000-1500ms (long sustain)
Unison Voices:    7 (natural orchestral thickness)
Unison Detune:    30-50%
```

**Step 4: Add effects**
- Add: **Reverb** (40-60% for hall/church)
- Maybe: **EQ** (slight boost at 1kHz for warmth)

**Result:** Orchestral, emotive, beautiful

---

## Sound Design Recipes

### Recipe 1: Funky Disco Bass

```
Synth: "Analog Saw Bass" preset

Adjustments:
- Octave:         -1 (one octave lower)
- Filter Cutoff:  45%
- Filter Res:     50% (movement)
- Attack:         5ms
- Sustain:        100%
- Release:        75ms
- Overdrive:      25% (warm distortion)
- LFO Rate:       2 Hz (slow wobble)
- LFO Amount:     30% (to filter cutoff)

Result: Funky, vintage disco bass that moves and grooves
Extra: Add **Sidechain** for pumping effect in DAW
```

### Recipe 2: Atmospheric Pad with Movement

```
Synth: "Evolving Ambient Pad" preset

Adjustments:
- Filter Cutoff:  100%
- Filter Res:     15%
- Unison Voices:  7
- Unison Detune:  35%
- Attack:         800ms (slow fade in)
- Release:        3000ms (6 second tail)
- LFO1 Rate:      0.3 Hz (very slow evolution)
- LFO1 Amount:    25% (to filter cutoff and pan)

Effects:
- Reverb:         60% (spacy)
- Delay:          1/4 note, 20% feedback (ethereal)
- Width:          Add **Chorus** for stereo movement

Result: Lush, evolving, professional ambient sound
```

### Recipe 3: Punchy Synth Lead

```
Synth: "Retro Lead Square" preset

Adjustments:
- Filter Cutoff:  75%
- Filter Res:     35%
- Attack:         10ms
- Sustain:        80%
- Release:        150ms
- Pulse Width:    We'll use envelope, 40-60% range
- LFO Rate:       6 Hz (moderate modulation)
- LFO Amount:     20% (to filter for wobble)

Effects:
- Distortion:     8% (slight grit)
- **Resonator**:  Adds metallic sheen
- Reverb:         20% (just enough space)

Result: 80s-style synth lead, punchy and present
```

### Recipe 4: Warm Electric Piano

```
Synth: "FM Piano" or "Vintage Electric" preset

Adjustments:
- Transpose:      +12 (one octave up for brightness)
- Amp Release:    500ms (natural decay)
- Filter Cutoff:  80% (warm)
- Filter Res:     10%

Effects:
- Distortion:     3% (vintage warmth)
- Phaser:         25% rate, 30% amount
- Reverb:         30% (room ambience)

Result: Warm, vintage electric piano perfect for soul/funk
```

### Recipe 5: Atmospheric Strings

```
Synth: "Orchestral Strings" or "Warm Strings" preset

Adjustments:
- Filter Cutoff:  90%
- Filter Res:     20% (natural variation)
- Attack:         400ms (slow articulation)
- Release:        2000ms (long tail)
- Unison Voices:  7
- Unison Detune:  40%

Step Modulation (if available):
- Pitch Envelope: Slight pitch rise on attack (humanizes)

Effects:
- Reverb:         50% (orchestral hall)
- EQ:             +2dB at 2kHz (midrange warmth)
- Delay:          Optional: 1/8 note, 15% for texture

Result: Lush orchestral strings that sound Hollywood-grade
```

---

## Advanced Synthesis

### Understanding Surge XT Sections

#### 1. Oscillators (Creating the raw sound)

**Waveshapes available:**
- **Sine** - Pure, clean (mathematical)
- **Triangle** - Soft, mellow
- **Square** - Bright, harsh
- **Saw** - Rich, complex (most harmonics)
- **Pulse** - Between sine and square (variable)
- **Noise** - All frequencies at once

**For Lyra MIDI:**
- Lead tracks: Use **Saw** or **Pulse** (bright)
- Bass tracks: Use **Saw** (rich) or **Square** (tight)
- Pads: **Triangle** or **Sine** (smooth)
- Effects: **Noise** oscillators

#### 2. Filters (Shaping the sound)

**Filter Types:**
- **12dB Lowpass** - Warm, soft (removes highs)
- **24dB Lowpass** - Darker, smoother
- **Highpass** - Removes lows (thins out)
- **Bandpass** - Band-limited (special character)

**Key Parameters:**
- **Cutoff:** How much harmonics pass (0-100%)
- **Resonance:** Peak at cutoff frequency (0-100%)
  - 0% = Smooth
  - 30% = Musical
  - 60%+ = Self-oscillating (very bright)

**For Lyra MIDI:**
- Leads: High cutoff (70-90%), medium resonance (20-40%)
- Bass: Low cutoff (30-60%), high resonance (40-70%)
- Pads: Very high cutoff (80-100%), low resonance (5-20%)

#### 3. Envelopes (Time-based shaping)

**ADSR Envelope:**
```
Attack    → How fast sound reaches peak (0-1000ms)
Decay     → How fast it drops from peak
Sustain   → Level held while note is pressed (0-100%)
Release   → How long after key release (0-5000ms)

Visualized:
  ↗ (Attack)
 ╱ ↘ (Decay)
╱   ↘ (Sustain)_____ (Release) ╲╲╲
```

**For Lyra MIDI:**
- Plucked sounds: Fast Attack, Fast Decay, Low Sustain
  - Attack: 0-20ms
  - Decay: 100-200ms
  - Sustain: 0-20%
  - Release: 50-100ms

- Held sounds (pads, leads): Slow Attack, No Decay, Full Sustain
  - Attack: 300-1000ms
  - Decay: 0ms (skip)
  - Sustain: 100%
  - Release: 1000-3000ms

- Percussive (drums): Very Fast
  - Attack: 0ms
  - Decay: 50ms
  - Sustain: 0%
  - Release: 100ms

#### 4. LFOs (Modulation - Wobble/Movement)

**LFO = Low Frequency Oscillator**
- Creates movement in sound
- Modulates parameters over time
- Creates pitch wobble, panning, filter movement

**Parameters:**
- **Rate:** Speed of wobble (0.01-20 Hz)
  - 0.5 Hz = Slow, dreamy
  - 2 Hz = Moderate, musical
  - 6+ Hz = Fast, intricate
- **Amount:** How much modulation (0-100%)
  - 5-15% = Subtle
  - 30-50% = Obvious, musical
  - 70%+ = Extreme

**Common routing for Lyra:**
```
LFO → Filter Cutoff (wobbles the tone)
LFO → Pitch (subtle pitch modulation)
LFO → Pan (stereo movement)
```

#### 5. Effects (Processing and texture)

**Essential Surge XT Effects:**

| Effect | Use | Settings |
|--------|-----|----------|
| **Reverb** | Space & ambience | 30-60% for natural, 60%+ for ethereal |
| **Delay** | Echo & groove | 1/4, 1/8, or 1/16 note timing |
| **Chorus** | Width & movement | 15-25% for subtle, 40%+ for obvious |
| **Distortion** | Warmth or aggression | 5-20% warm, 40%+ aggressive |
| **Resonator** | Metallic/bell tones | Frequency: 1-4kHz |
| **Vocoder** | Formant shaping | Natural humanizing |
| **Phaser** | Classic modulation | 20-40% for texture |

---

## Performance Tips

### Making Surge XT Efficient

**CPU Usage:**
- Use **fewer unison voices** (3-5 instead of 7)
- Disable **reverb if not needed**
- Use **simpler presets** if running low on CPU

### Mixing Multiple Surge XT Instances

**Levels:**
```
Track 1 (Lead):    0dB (reference)
Track 2 (Bass):    -6dB (support)
Track 3 (Drums):   -4dB (groove)
Track 4 (Pad):     -12dB (background)
Master:            -3dB (headroom)
```

### Quick Favorite-Finding

**Search by sound type:**
- Type in search box top-left
- Keywords: "bass", "lead", "pad", "string", "warm", "bright"
- **Use tags:** Filter by category for faster browsing

### Exporting Settings

**Save your tweaks:**
1. Once you nail a sound
2. **Save As** (button at top)
3. Name it (e.g., "Lyra Lead Bright")
4. Use in future tracks!

---

## Troubleshooting

### Surge XT not showing MIDI input

**Solution:**
1. Check track has Surge XT as instrument
2. Check MIDI is actually going to the track (meter shows activity)
3. Reload Surge XT instance

### Sound is too quiet

**Solution:**
1. Increase **Master Volume** slider (right side of Surge XT)
2. Check **DAW track fader** (Ableton, etc.)
3. Increase **Amp Envelope Sustain** to full

### Sound is too harsh/bright

**Solution:**
1. Lower **Filter Cutoff** (move left)
2. Reduce **Filter Resonance**
3. Try a different preset (search "warm" or "smooth")

### Presets sound thin/weak

**Solution:**
1. Add **Unison Voices** (right side panel, increase to 5-7)
2. Add **Unison Detune** (30-50% for richness)
3. Add **Reverb effect** (lends space/professionalism)

---

## Next Steps

1. **Explore presets** - Click → until you find sounds you like
2. **Watch tutorials** - YouTube: "Surge XT Synthesis Tutorial"
3. **Read the manual** - surge-synthesizer.github.io/manual
4. **Experiment** - Tweak every parameter and listen
5. **Share tracks** - Post your Lyra + Surge XT productions!

---

**Happy synthesizing!** 🎵
For DAW-specific setup, see [Ableton Live Guide](DAW_ABLETON_LIVE.md)
