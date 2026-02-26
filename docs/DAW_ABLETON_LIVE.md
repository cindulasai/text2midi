# Using text2midi with Ableton Live Lite (Complete Guide)

Learn how to import MIDI from text2midi into Ableton Live Lite, assign instruments, and create professional tracks.

## Table of Contents

1. [Setup & Installation](#setup)
2. [Importing MIDI from Lyra](#importing)
3. [Assigning Instruments](#instruments)
4. [Workflow: From MIDI to Production](#workflow)
5. [Step-by-Step Tutorial](#tutorial)
6. [Troubleshooting](#troubleshooting)

---

## Setup & Installation

### What You Need

- **Lyra** (installed and running)
- **Ableton Live Lite** (free version available)
- A **MIDI keyboard** (optional but recommended)
- **VST instruments** (Ableton comes with several)

### Install Ableton Live Lite

1. Go to [ableton.com/live](https://www.ableton.com/en/live/)
2. Download **Live Lite** (free) or **Live Standard/Suite** (paid)
3. Install and open

### Recommended Additional Plugins (Free)

These work great with Lyra MIDI:
- **Serum** (paid) - Advanced synth
- **Vital** - Free advanced synth
- **Surge XT** - Free, powerful synth
- **Dexed** - Free FM synth
- **Helm** - Free synth
- **Kontakt Lite** - Free sampling engine from Native Instruments

---

## Importing MIDI from Lyra

### Method 1: Drag & Drop (Easiest)

1. **Generate MIDI in text2midi**
   - Create a composition in text2midi
   - Download the .mid file

2. **Open Ableton Live**
   - Create a new project: File → New Live Set

3. **Drag MIDI File to Ableton**
   - Locate your downloaded .mid file in File Explorer/Finder
   - Drag and drop onto the Ableton timeline
   - Ableton automatically creates tracks!

**Result:** Multiple tracks appear in Ableton, each with MIDI data and basic drum kit instruments.

### Method 2: Import via Menu

1. **File → Import Audio/MIDI**
2. **Select your Lyra MIDI file**
3. **Choose "Import to new tracks"**
4. **Click Import**

---

## Assigning Instruments

### Understanding MIDI Channels in text2midi

text2midi outputs MIDI on **Channels 1-8**, each with:
- A **program change** message (defines instrument type)
- **MIDI data** (notes, timing, velocity)
- **Channel info** visible in Ableton

```
Track 1 → Lead/Synth (Program 33 = Synth Lead)
Track 2 → Bass (Program 33 = Electric Bass)
Track 3 → Drums (Program 0 = Kick on note 36, etc.)
Track 4 → Harmony (Program 5 = Strings)
Track 5 → Counter Melody (Program 73 = Flute)
Track 6 → Arpeggio (Program 25 = Guitar)
Track 7 → Pad (Program 50 = Warm Synth)
Track 8 → Effects/Percussion (Program 0 or varies)
```

### Changing Instruments in Ableton Live

**For Musical Instruments:**

1. **Click on the track header** in the Session view
2. **Look at the instrument slot** (shows current instrument)
3. **Click the instrument** to open menu
4. **Choose a new instrument**:
   - Ableton Wavetable (synth sounds)
   - Operator (complex synthesis)
   - Sampler (load samples / loops)
   - Wavetable (subtractive synth)

**For Drums:**

1. **Track 3 (usually drums)** shows as a drum track
2. **Click on the drum rack** to adjust
3. **Choose drum sounds** for each MIDI note:
   - Note 36 = Kick
   - Note 38 = Snare
   - Note 42 = Hi-Hat
   - Note 43 = Pedal Hi-Hat
   - Note 46 = Open Hi-Hat
   - Note 49 = Crash
   - Note 51 = Ride

### Recommended Instrument Assignments

**Track 1 (Lead/Melody)**
```
Instrument: Ableton Wavetable or Serum
Sound Type: Bright lead, synth lead, or bell
Sound Preset: "Bright Synth Lead" or "Electric Piano"
```

**Track 2 (Bass)**
```
Instrument: Ableton Wavetable or Serum
Sound Type: Deep sub bass or electric bass
Sound Preset: "Sub Bass" or "Funky Bass"
```

**Track 3 (Drums)**
```
Instrument: Ableton Drum Rack (comes with Live Lite)
Sounds: Professional drum kit (Ableton Factory sounds)
File: Drums_and_Percussion > Acoustic Drums or Electronic Drums
```

**Track 4 (Harmony/Pad)**
```
Instrument: Ableton Wavetable
Sound Type: Lush pad or string pad
Sound Preset: "String Pad" or "Ambient Pad"
Add Reverb: Use Ableton Reverb plugin (add richness)
```

**Track 5 (Counter Melody)**
```
Instrument: Ableton Wavetable
Sound Type: Flute, bells, or soft lead
Sound Preset: "Flute" or "Bell"
```

---

## Workflow: From MIDI to Production

### The Classic 5-Step Workflow

```
1. GENERATE in Lyra
2. IMPORT into Ableton
3. ASSIGN INSTRUMENTS
4. ADJUST & ARRANGE
5. ADD EFFECTS & MIX
```

### Step-by-Step Workflow

#### Step 1: Generate in Lyra
```
Prompt: "Upbeat pop song in E major with synth lead, bass, drums, and strings"
Duration: 20-30 seconds
Output: 4-5 tracks in a MIDI file
```

#### Step 2: Import into Ableton
- Drag .mid file onto Ableton timeline
- All tracks appear with default drum sounds

#### Step 3: Assign Instruments
- Track 1 (Melody): Wavetable Synth Lead
- Track 2 (Bass): Wavetable Sub Bass
- Track 3 (Drums): Drum Rack
- Track 4 (Strings): Wavetable String Pad + Reverb

#### Step 4: Adjust & Arrange
- Adjust tempo: Cmd+T (Mac) or Ctrl+T (Windows)
- Swap sections: Copy/paste arrange tracks
- Extend intro/outro: Duplicate and rearrange bar sections

#### Step 5: Add Production
- **Reverb** on pads (Create → Reverb)
- **Delay** on lead (Create → Delay)
- **EQ** on drums (Create → EQ Eight)
- **Compression** for glue
- **Master Effects** on Master track

---

## Step-by-Step Tutorial

### Complete Example: Piano Pop to Produced Track

**Goal:** Take a text2midi pop piano MIDI and turn it into a polished track

### Phase 1: Generation (In text2midi)

```
Prompt: "Upbeat pop song in G major with warm piano, funky bass, tight drums, and soft strings"

Time to generate: ~25 seconds
Expected tracks:
1. Piano Melody
2. Bass
3. Drums (kick, snare, hi-hat)
4. String Pad
```

### Phase 2: Import (In Ableton)

**Step 1:** Open Ableton Live → New Live Set

**Step 2:** Drag downloaded MIDI file onto timeline

**Result:** 
```
Track 1: Piano [MIDI] (currently shows drum kit)
Track 2: Bass [MIDI] (currently shows drum kit)
Track 3: Drums [MIDI] (shows drum kit) ✓
Track 4: Strings [MIDI] (currently shows drum kit)
Master Track
```

### Phase 3: Assign Instruments

**Track 1 - Piano Melody:**
1. Click on "Instrument" in Track 1
2. Choose: Ableton → Wavetable
3. Look for preset: "Bright Piano" or "Electric Piano"
4. (Or: Operators → Electric Piano)

**Track 2 - Bass:**
1. Click on "Instrument" in Track 2
2. Choose: Ableton → Wavetable
3. Search: "Bass" or "Sub Bass"
4. Select: "Funk Bass" or "Deep Sub Bass"

**Track 3 - Drums:**
1. Already shows drum kit ✓
2. Check: Drums_and_Percussion → Acoustic Drums
3. Or: Electronic Drums (match your vibe)

**Track 4 - Strings:**
1. Click on "Instrument" in Track 4
2. Choose: Ableton → Wavetable
3. Search: "String" or "Pad"
4. Select: "String Pad" or "Analog String"

### Phase 4: Add Effects

**Add Reverb to String Pad (Track 4):**
1. **Right-click** below the Wavetable instrument
2. **Select: Audio Effects → Reverb**
3. Set: Room = 70%, Decay = 2.5s
4. **Listen:** String pad now has space

**Add Delay to Piano (Track 1):**
1. Right-click below Wavetable in Track 1
2. Select: Audio Effects → Delay
3. Set: Time = 1/4 beat, Feedback = 30%
4. Listen: Piano now has rhythmic echo

**Add EQ to Drums (Track 3):**
1. Right-click below drum rack
2. Select: Audio Effects → EQ Eight
3. Boost: 100Hz (add punch), 8kHz (add attack)
4. Listen: Drums cut through better

### Phase 5: Mixing

**Volume Levels** (typical starting point):
```
Piano:    -6dB (main focus)
Bass:     -8dB (supports)
Drums:    -4dB (drives groove)
Strings:  -12dB (background)
Master:   -3dB (headroom)
```

**Panning** (left-right stereo):
```
Piano:    Center (L: 50, R: 50)
Bass:     Center (L: 50, R: 50)
Drums:    Center (L: 50, R: 50)
Strings:  Slightly left & right (L: 35, R: 65) for width
```

**Final Check:**
1. Play the track end-to-end
2. Adjust levels so nothing clips (Master shows -6dB headroom)
3. Export: File → Export Audio → WAV or MP3

---

## Advanced Techniques

### Velocity Editing

Lyra sometimes has even velocities. **Make it humanize:**

1. **Select all MIDI notes** in a track (Cmd+A on Mac, Ctrl+A on Windows)
2. **Tools → Adjust → Randomize Velocity** (±10-15%)
3. **Listen:** Now sounds more human

### Humanization

To make perfect MIDI sound natural:

1. **Select all notes** (Cmd+A)
2. **Tools → Fold** (randomizes timing slightly)
3. **Set amount:** 5-20ms randomization
4. **Listen:** Sounds more organic

### Extending the Track

If your Lyra MIDI is 16 bars but you want 32:

1. **Select all MIDI notes** on a track
2. **Copy-Paste** at bar 16
3. **Optionally modify:** Change instruments/effects for second half
4. **Result:** 32-bar track

### Key Changes

Want to modulate to a different key?

1. **Select a track** of MIDI
2. **Edit → Transpose**
3. **Enter semitones** (12 = up one octave, 2 = up one whole step)
4. **Listen:** New key version ready

---

## Troubleshooting

### Problem: MIDI tracks show wrong sounds (all drums)

**Solution:** 
Make sure you select **Wavetable** or **Operators** for musical tracks, not the Drum Rack.

### Problem: Some MIDI notes are not playing

**Possible causes:**
1. **Note outside range** - Ableton can only play notes 0-127
2. **Channel muted** - Check track isn't muted (M button)
3. **Instrument needs notes** - Wavetable needs MIDI input

**Solution:** 
- Check note range in MIDI Editor (Notes should be roughly 36-84 for melody)
- Unmute tracks
- Reload instrument

### Problem: Tempo is wrong

**Solution:**
1. **Tempodrop:** Look at top of Ableton (shows BPM)
2. **Lyra created 120 BPM** but Ableton shows different
3. **Click on BPM** and match what Lyra created
4. Or manually set: **Double-click the number → edit**

### Problem: MIDI file doesn't import

**Possible causes:**
1. File is corrupted
2. File format is not .mid/.midi
3. Ableton doesn't have read permissions

**Solution:**
- Re-export from Lyra
- Ensure file ends in **.mid**
- Try importing via: Import Audio/MIDI menu (instead of drag-drop)

### Problem: Drums don't sound right

**Solution:**
Lyra outputs standard MIDI notes:
- Note 36 = Kick
- Note 38 = Snare
- Note 42 = Hi-Hat
- Note 43 = Open Hi-Hat

Make sure your drum rack uses a **standard General MIDI** drum kit, not a custom one.

### Problem: Effects make it sound worse

**Solution:**
- **Reduce effect amounts** (they're usually set too high by default)
- **Try different instruments** (one might respond better)
- **Remove effects** and listen to raw MIDI first
- **Less is more** - subtle effects sound more professional

### Problem: Too quiet or too loud

**Check levels:**
1. **Track levels** - Fader should be around 0dB
2. **Master level** - Should not clip (red light)
3. **Instrument outputs** - Wavetable/Operators have volume controls too
4. **Reverb/Effects** - Can boost level significantly

**Solution:**
- Drag track faders to comfortable level
- Reduce reverb/effect amounts if too loud
- Keep Master below -6dB for headroom

---

## Next Steps

1. **Join the Lyra Community** - Share your tracks
2. **Explore Ableton's Built-in instruments** - Many hidden gems
3. **Download Free Plugins** - Surge XT, Vital for more sounds
4. **Study Music Production** - YouTube channels: Ableton, In Depth Music
5. **Export & Share** - File → Export Audio (WAV 44.1kHz, 16-bit)

---

## Quick Reference

### Keyboard Shortcuts (macOS)

| Action | Shortcut |
|--------|----------|
| Play/Pause | Space |
| Undo | Cmd+Z |
| Select All MIDI | Cmd+A |
| Copy | Cmd+C |
| Paste | Cmd+V |
| Duplicate Track | Cmd+D |
| New Instrument | Cmd+8 |
| Toggle Editor | Cmd+E |

### Keyboard Shortcuts (Windows)

| Action | Shortcut |
|--------|----------|
| Play/Pause | Space |
| Undo | Ctrl+Z |
| Select All MIDI | Ctrl+A |
| Copy | Ctrl+C |
| Paste | Ctrl+V |
| Duplicate Track | Ctrl+D |
| New Instrument | Ctrl+8 |
| Toggle Editor | Ctrl+E |

---

**Happy producing!** 🎵
For more on specific instruments, see [Surge XT Guide](DAW_SURGE_XT.md)
