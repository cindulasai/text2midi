# Chord Progressions Library

> **100+ chord progressions** organized by genre family with named patterns, interval arrays, and usage notes.
> Each genre gets 3–5 characteristic progressions.

---

## Format Convention

Each progression is given as:
- **Name**: Human-readable name (e.g., "Andalusian cadence")
- **Roman numerals**: Functional harmony notation
- **Intervals**: Arrays of intervals from root for MIDI generation (compatible with current `CHORD_PROGRESSIONS` format)
- **Bars**: Typical length in bars

---

## 1. Classical & Orchestral

### Baroque / Classical Era
| Name | Roman | Intervals | Notes |
|------|-------|-----------|-------|
| Classical Cadence | I → IV → V → I | `[[0,4,7], [5,9,12], [7,11,14], [0,4,7]]` | Standard resolution |
| Circle of Fifths | I → IV → vii° → iii → vi → ii → V → I | `[[0,4,7], [5,9,12], [11,14,17], [4,7,11], [9,12,16], [2,5,9], [7,11,14], [0,4,7]]` | Baroque sequences |
| Romanesca | I → V → vi → iii | `[[0,4,7], [7,11,14], [9,12,16], [4,7,11]]` | Renaissance/Baroque |

### Romantic / Impressionist
| Name | Roman | Intervals | Notes |
|------|-------|-----------|-------|
| Romantic Yearning | I → vi → IV → V | `[[0,4,7], [9,12,16], [5,9,12], [7,11,14]]` | Emotional, unresolved |
| Plagal Drift | I → IV → iv → I | `[[0,4,7], [5,9,12], [5,8,12], [0,4,7]]` | Impressionist color |
| Chromatic Descent | I → V/vi → vi → V | `[[0,4,7], [4,8,11], [9,12,16], [7,11,14]]` | Dramatic |

### Minimalist
| Name | Roman | Intervals | Notes |
|------|-------|-----------|-------|
| Two-Chord Oscillation | I → V | `[[0,4,7], [7,11,14]]` | Repetitive, hypnotic |
| Modal Static | i → VII | `[[0,3,7], [10,14,17]]` | Glass/Reich style |
| Phasing Pattern | I → IV → I → IV | `[[0,4,7], [5,9,12], [0,4,7], [5,9,12]]` | Phase music |

---

## 2. Jazz

### Swing / Bebop
| Name | Roman | Intervals | Notes |
|------|-------|-----------|-------|
| ii-V-I Major | ii7 → V7 → Imaj7 | `[[2,5,9,12], [7,11,14,17], [0,4,7,11]]` | **The** jazz progression |
| ii-V-I Minor | iiø7 → V7b9 → i7 | `[[2,5,8,12], [7,11,14,17], [0,3,7,10]]` | Minor key jazz |
| Rhythm Changes (A) | Imaj7 → vi7 → ii7 → V7 | `[[0,4,7,11], [9,12,16,19], [2,5,9,12], [7,11,14,17]]` | Gershwin-derived |
| Blues Turnaround | I7 → IV7 → I7 → V7 | `[[0,4,7,10], [5,9,12,15], [0,4,7,10], [7,11,14,17]]` | 12-bar feel |
| Tritone Substitution | ii7 → bII7 → Imaj7 | `[[2,5,9,12], [1,5,8,11], [0,4,7,11]]` | Harmonic sophistication |

### Modal / Cool
| Name | Roman | Intervals | Notes |
|------|-------|-----------|-------|
| So What Vamp | Dm7 → Ebm7 (half-step) | `[[2,5,9,12], [3,6,10,13]]` | Miles Davis modal |
| Dorian Vamp | i7 → IV7 | `[[0,3,7,10], [5,9,12,15]]` | Modal jazz standard |
| Quartal Voicings | sus4 stack | `[[0,5,10], [7,12,17]]` | McCoy Tyner style |

### Bossa Nova / Latin Jazz
| Name | Roman | Intervals | Notes |
|------|-------|-----------|-------|
| Bossa Classic | Imaj7 → ii7 → V7 → Imaj7 | `[[0,4,7,11], [2,5,9,12], [7,11,14,17], [0,4,7,11]]` | Jobim-style |
| Corcovado | Imaj9 → vi9 → ii9 → V13 | `[[0,4,7,11,14], [9,12,16,19,23], [2,5,9,12,16], [7,11,14,17,21]]` | Rich voicings |
| Girl from Ipanema | Imaj7 → ii7 → bII7 → I | `[[0,4,7,11], [2,5,9,12], [1,5,8,11], [0,4,7]]` | Chromatic movement |

### Smooth Jazz
| Name | Roman | Intervals | Notes |
|------|-------|-----------|-------|
| Smooth Groove | Imaj7 → iii7 → vi7 → V7 | `[[0,4,7,11], [4,7,11,14], [9,12,16,19], [7,11,14,17]]` | Gentle, polished |
| Silky | iii7 → vi7 → ii7 → V7 | `[[4,7,11,14], [9,12,16,19], [2,5,9,12], [7,11,14,17]]` | Sophisticated |

---

## 3. Blues & Soul

| Name | Roman | Intervals | Notes |
|------|-------|-----------|-------|
| 12-Bar Blues (basic) | I7 → I7 → I7 → I7 → IV7 → IV7 → I7 → I7 → V7 → IV7 → I7 → V7 | See below... | **The** blues form |
| Quick-Change Blues | I7 → IV7 → I7 → I7 → IV7 → ... | Quick IV in bar 2 | More movement |
| Minor Blues | i7 → iv7 → i7 → V7 | `[[0,3,7,10], [5,8,12,15], [0,3,7,10], [7,11,14,17]]` | Dark blues |
| Gospel Progression | I → I7 → IV → iv → I → V → I | `[[0,4,7], [0,4,7,10], [5,9,12], [5,8,12], [0,4,7], [7,11,14], [0,4,7]]` | Church feel |
| Soul Cadence | I → iii → IV → iv → I | `[[0,4,7], [4,7,11], [5,9,12], [5,8,12], [0,4,7]]` | Emotional resolution |

### 12-Bar Blues (4-bar progressions for our system)
| Bars | Roman | Intervals |
|------|-------|-----------|
| 1-4 | I7 → IV7 → I7 → I7 | `[[0,4,7,10], [5,9,12,15], [0,4,7,10], [0,4,7,10]]` |
| 5-8 | IV7 → IV7 → I7 → I7 | `[[5,9,12,15], [5,9,12,15], [0,4,7,10], [0,4,7,10]]` |
| 9-12 | V7 → IV7 → I7 → V7 | `[[7,11,14,17], [5,9,12,15], [0,4,7,10], [7,11,14,17]]` |

---

## 4. Rock

| Name | Roman | Intervals | Notes |
|------|-------|-----------|-------|
| Classic Rock I-IV-V | I → IV → V → IV | `[[0,4,7], [5,9,12], [7,11,14], [5,9,12]]` | Universally used |
| Power Chord Riff | I5 → bVII5 → IV5 | `[[0,7], [10,17], [5,12]]` | Nirvana, Foo Fighters |
| Grunge Drop | i → bVI → bIII → bVII | `[[0,3,7], [8,12,15], [3,7,10], [10,14,17]]` | Seattle sound |
| Classic Punk | I → V → vi → IV | `[[0,4,7], [7,11,14], [9,12,16], [5,9,12]]` | Three chords + truth |
| Post-Rock Build | i → III → VII → iv | `[[0,3,7], [3,7,10], [10,14,17], [5,8,12]]` | Crescendo structure |
| Shoegaze Drone | I → bVII → IV → I | `[[0,4,7], [10,14,17], [5,9,12], [0,4,7]]` | Wall of sound |
| Surf Reverb | i → bVII → bVI → V | `[[0,3,7], [10,14,17], [8,12,15], [7,11,14]]` | Dick Dale style |
| Southern Boogie | I → IV → I → V | `[[0,4,7], [5,9,12], [0,4,7], [7,11,14]]` | Lynyrd Skynyrd |

---

## 5. Metal

| Name | Roman | Intervals | Notes |
|------|-------|-----------|-------|
| Metal Power Descent | i → bVII → bVI → V | `[[0,3,7], [10,14,17], [8,12,15], [7,11,14]]` | Phrygian cadence |
| Doom Crawl | i → bII → i → bII | `[[0,3,7], [1,5,8], [0,3,7], [1,5,8]]` | Crushing slow |
| Thrash Riff Sequence | i → bII → i → bVII | `[[0,7], [1,8], [0,7], [10,17]]` | Power chord movement |
| Symphonic Drama | i → iv → V → i | `[[0,3,7], [5,8,12], [7,11,14], [0,3,7]]` | Harmonic minor feel |
| Djent Groove | i → bII → bVII → i | `[[0,7,12], [1,8,13], [10,17,22], [0,7,12]]` | Polyrhythmic |

---

## 6. Electronic & Dance

| Name | Roman | Intervals | Notes |
|------|-------|-----------|-------|
| Four-on-Floor House | i → bVII → bVI → V | `[[0,3,7], [10,14,17], [8,12,15], [7,11,14]]` | Classic house |
| Deep House Groove | i7 → IV7 → bVII7 → bIII7 | `[[0,3,7,10], [5,9,12,15], [10,14,17,20], [3,7,10,13]]` | Soulful deep |
| Trance Anthem | vi → IV → I → V | `[[9,12,16], [5,9,12], [0,4,7], [7,11,14]]` | Euphoric builds |
| Dubstep Half-Time | i → bVI → bIII → bVII | `[[0,3,7], [8,12,15], [3,7,10], [10,14,17]]` | Dark, heavy |
| Synthwave Drive | vi → IV → I → V | `[[9,12,16], [5,9,12], [0,4,7], [7,11,14]]` | 80s nostalgia |
| DnB Roller | i → bVI | `[[0,3,7], [8,12,15]]` | Two-chord tension |
| Techno Minimal | i → i → bII → i | `[[0,3,7], [0,3,7], [1,5,8], [0,3,7]]` | Hypnotic |
| Ambient Wash | Imaj7 → IVmaj7 | `[[0,4,7,11], [5,9,12,16]]` | Floating, no resolution |
| Future Bass Saws | I → vi → IV → V | `[[0,4,7], [9,12,16], [5,9,12], [7,11,14]]` | Big supersaw stacks |

---

## 7. Hip-Hop & Urban

| Name | Roman | Intervals | Notes |
|------|-------|-----------|-------|
| Boom Bap Sample | i7 → iv7 → V7 → i7 | `[[0,3,7,10], [5,8,12,15], [7,11,14,17], [0,3,7,10]]` | Jazzy, sampled |
| Trap Dark | i → bVI → bVII → i | `[[0,3,7], [8,12,15], [10,14,17], [0,3,7]]` | Menacing minor |
| Lo-fi Jazzy | Imaj7 → vi7 → ii7 → V7 | `[[0,4,7,11], [9,12,16,19], [2,5,9,12], [7,11,14,17]]` | Chill, nostalgic |
| Drill Slide | i → bVII → bVI → V | `[[0,3,7], [10,14,17], [8,12,15], [7,11,14]]` | Dark, 808 slides |
| Cloud Rap Ethereal | Imaj7 → iii7 → vi7 | `[[0,4,7,11], [4,7,11,14], [9,12,16,19]]` | Dreamy, spacey |
| Phonk Memphis | i → bVII → i → bVI | `[[0,3,7], [10,14,17], [0,3,7], [8,12,15]]` | Dark, cowbell |

---

## 8. Pop

| Name | Roman | Intervals | Notes |
|------|-------|-----------|-------|
| Pop Canon (Axis) | I → V → vi → IV | `[[0,4,7], [7,11,14], [9,12,16], [5,9,12]]` | **Most used pop progression** |
| Millennial Whoop | I → V → vi → IV | Same as above | With vocal pattern vi→V |
| Sensitive | vi → IV → I → V | `[[9,12,16], [5,9,12], [0,4,7], [7,11,14]]` | Emotional pop |
| Doo-Wop | I → vi → IV → V | `[[0,4,7], [9,12,16], [5,9,12], [7,11,14]]` | 50s classic |
| K-Pop Dramatic | vi → V → IV → V | `[[9,12,16], [7,11,14], [5,9,12], [7,11,14]]` | Build-drop-build |
| Tropical Pop | I → iii → vi → IV | `[[0,4,7], [4,7,11], [9,12,16], [5,9,12]]` | Island vibe |

---

## 9. R&B & Funk

| Name | Roman | Intervals | Notes |
|------|-------|-----------|-------|
| Funk Groove | I7 → IV7 → I7 → V7 | `[[0,4,7,10], [5,9,12,15], [0,4,7,10], [7,11,14,17]]` | Dominant 7th groove |
| P-Funk Vamp | I7 → I7 → IV7 → I7 | `[[0,4,7,10], [0,4,7,10], [5,9,12,15], [0,4,7,10]]` | Funky one-chord |
| Neo-Soul Cycle | i9 → IV9 → bVII9 → bIII9 | `[[0,3,7,10,14], [5,9,12,15,19], [10,14,17,20,24], [3,7,10,13,17]]` | Rich extensions |
| Disco Four | I → ii → iii → IV | `[[0,4,7], [2,5,9], [4,7,11], [5,9,12]]` | Ascending disco |
| R&B Smooth | Imaj7 → iii7 → vi7 → ii7 → V7 | `[[0,4,7,11], [4,7,11,14], [9,12,16,19], [2,5,9,12], [7,11,14,17]]` | Silky R&B |

---

## 10. Folk & Acoustic

| Name | Roman | Intervals | Notes |
|------|-------|-----------|-------|
| Folk Standard | I → IV → V → I | `[[0,4,7], [5,9,12], [7,11,14], [0,4,7]]` | Simple, timeless |
| Celtic Modal | i → bVII → i → bVI | `[[0,3,7], [10,14,17], [0,3,7], [8,12,15]]` | Dorian feel |
| Country Train | I → IV → I → V | `[[0,4,7], [5,9,12], [0,4,7], [7,11,14]]` | Nashville |
| Bluegrass Drive | I → IV → V → V | `[[0,4,7], [5,9,12], [7,11,14], [7,11,14]]` | Driving pickup |
| Nordic Haunting | i → bIII → bVII → iv | `[[0,3,7], [3,7,10], [10,14,17], [5,8,12]]` | Minor modal |

---

## 11. Latin & Caribbean

| Name | Roman | Intervals | Notes |
|------|-------|-----------|-------|
| Salsa Monte | I → IV → V → I | `[[0,4,7], [5,9,12], [7,11,14], [0,4,7]]` | With clave rhythm |
| Reggaeton Loop | i → bVI → bVII → i | `[[0,3,7], [8,12,15], [10,14,17], [0,3,7]]` | Dembow rhythm |
| Bossa ii-V | ii7 → V7 → Imaj7 → Imaj7 | `[[2,5,9,12], [7,11,14,17], [0,4,7,11], [0,4,7,11]]` | Gentle Brazilian |
| Cumbia Cycle | I → IV → V → IV | `[[0,4,7], [5,9,12], [7,11,14], [5,9,12]]` | Steady cumbia |
| Reggae One-Drop | i → bVII → bVI → V | `[[0,3,7], [10,14,17], [8,12,15], [7,11,14]]` | Roots reggae |
| Tango Dramático | i → iv → V → i | `[[0,3,7], [5,8,12], [7,11,14], [0,3,7]]` | Harmonic minor feel |
| Ska Upstroke | I → IV → V → IV | `[[0,4,7], [5,9,12], [7,11,14], [5,9,12]]` | Upbeat offbeat |
| Samba Partido Alto | I → ii → V → I | `[[0,4,7], [2,5,9], [7,11,14], [0,4,7]]` | Syncopated |

---

## 12. African

| Name | Roman | Intervals | Notes |
|------|-------|-----------|-------|
| Afrobeat Cycle | I → IV → I → V | `[[0,4,7], [5,9,12], [0,4,7], [7,11,14]]` | Hypnotic loop |
| Highlife Guitar | I → IV → V → IV | `[[0,4,7], [5,9,12], [7,11,14], [5,9,12]]` | Palm-wine guitar |
| Soukous Sebene | I → V → IV → V | `[[0,4,7], [7,11,14], [5,9,12], [7,11,14]]` | Fast guitar solo section |
| Amapiano Keys | i → bVI → bVII → i | `[[0,3,7], [8,12,15], [10,14,17], [0,3,7]]` | Piano-driven |
| Desert Blues Hypnotic | I → I → IV → I | `[[0,4,7], [0,4,7], [5,9,12], [0,4,7]]` | Repetitive loop |

---

## 13. Asian & Middle Eastern

| Name | Roman | Intervals | Notes |
|------|-------|-----------|-------|
| Andalusian Cadence | i → bVII → bVI → V | `[[0,3,7], [10,14,17], [8,12,15], [7,11,14]]` | Flamenco / Arabic |
| Maqam Hijaz | Based on Phrygian dominant | `[[0,1,4,5,7,8,10]]` scale-based | Arabic classical |
| Raga Drone | I → I → I → I (pedal) | `[[0,7], [0,7], [0,7], [0,7]]` | Indian drone (Sa) |
| Bollywood Drama | i → bVI → bIII → V | `[[0,3,7], [8,12,15], [3,7,10], [7,11,14]]` | Film score tension |
| Japanese Ma | I → (silence) → IV → (silence) | `[[0,4,7], [], [5,9,12], []]` | Negative space |
| Turkish Seyir | i → iv → bII → i | `[[0,3,7], [5,8,12], [1,5,8], [0,3,7]]` | Makam descent |
| Gamelan Cycle | I → V → I → V | `[[0,4,7], [7,11,14], [0,4,7], [7,11,14]]` | Cyclic interlocking |
| K-Pop Power | vi → IV → I → V | `[[9,12,16], [5,9,12], [0,4,7], [7,11,14]]` | Dynamic build |

---

## 14. Cinematic & Ambient

| Name | Roman | Intervals | Notes |
|------|-------|-----------|-------|
| Epic Rise | i → bVI → bIII → bVII | `[[0,3,7], [8,12,15], [3,7,10], [10,14,17]]` | Trailer music |
| Dark Tension | i → bII → i → V | `[[0,3,7], [1,5,8], [0,3,7], [7,11,14]]` | Horror/suspense |
| Ambient Float | Imaj7 → IVmaj7 → Imaj7 → IVmaj7 | `[[0,4,7,11], [5,9,12,16], [0,4,7,11], [5,9,12,16]]` | Peaceful wash |
| Heroic Theme | I → V → vi → IV → I → V → I | `[[0,4,7], [7,11,14], [9,12,16], [5,9,12], [0,4,7], [7,11,14], [0,4,7]]` | Fantasy, John Williams |
| Meditation Drone | I → I → I → I | `[[0,7,12], [0,7,12], [0,7,12], [0,7,12]]` | Open fifths, static |
| Documentary Hope | I → iii → IV → V | `[[0,4,7], [4,7,11], [5,9,12], [7,11,14]]` | Gentle rising |

---

## Progression Count Summary

| Genre Family | Progressions |
|-------------|-------------|
| Classical & Orchestral | 9 |
| Jazz | 12 |
| Blues & Soul | 8 |
| Rock | 8 |
| Metal | 5 |
| Electronic & Dance | 9 |
| Hip-Hop & Urban | 6 |
| Pop | 6 |
| R&B & Funk | 5 |
| Folk & Acoustic | 5 |
| Latin & Caribbean | 8 |
| African | 5 |
| Asian & Middle Eastern | 8 |
| Cinematic & Ambient | 6 |
| **TOTAL** | **100** |
