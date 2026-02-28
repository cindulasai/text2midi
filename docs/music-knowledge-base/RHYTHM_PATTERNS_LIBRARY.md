# Rhythm Patterns Library

> Rhythm patterns, time signatures, drum kits, groove definitions, and swing ratios for every genre family.
> Expands the current 7 drum strategies to comprehensive genre-specific rhythm templates.

---

## Time Signatures by Genre

### Beyond 4/4

| Time Sig | Feel | Genres Using It |
|----------|------|-----------------|
| 4/4 | Standard | Pop, rock, electronic, hip-hop, funk, R&B, most genres |
| 3/4 | Waltz | Viennese waltz, country waltz, mazurka, musette |
| 6/8 | Compound | Irish jigs, Afro-Cuban, West African, tarantella, blues shuffle, Afrobeats |
| 2/4 | March | Polka, merengue, march, pasodoble, samba |
| 5/4 | Lopsided | Progressive rock, Dave Brubeck jazz, Balkan |
| 7/8 | Balkan odd | Bulgarian, Turkish, Macedonian (2+2+3 or 3+2+2) |
| 9/8 | Turkish | Zeimbekiko, Turkish 9/8 (2+2+2+3), Romani |
| 11/8 | Complex | Balkan kopanitsa (2+2+3+2+2) |
| 12/8 | Slow blues | Blues shuffle, gospel, West African 12/8 |
| Free | Rubato | Fado, alap (Indian), taqsim (Arabic), Gagaku, ambient |

---

## Drum Kit Definitions

### Standard Rock/Pop Kit
| Element | MIDI Note | Role |
|---------|-----------|------|
| Kick | 36 | Foundation beat |
| Snare | 38 | Backbeat |
| Closed Hi-hat | 42 | Time-keeping |
| Open Hi-hat | 46 | Accents |
| Crash | 49 | Section markers |
| Ride | 51 | Sustained rhythm |
| Tom Low | 45 | Fills |
| Tom Mid | 47 | Fills |
| Tom High | 50 | Fills |

### 808 Trap Kit
| Element | MIDI Note | Role | Character |
|---------|-----------|------|-----------|
| 808 Kick | 36 | Sub-bass foundation | Long sustained, pitched |
| Clap | 39 | Backbeat (replaces snare) | Layered, reverb |
| Closed Hi-hat | 42 | Rolls, rapid patterns | Tight, triplet rolls |
| Open Hi-hat | 46 | Accents every 4–8 beats | Sparse |
| Snare | 38 | Ghost hits | Layered with clap |
| Rimshot | 37 | Variation | Occasional accent |

### Jazz Brush Kit
| Element | MIDI Note | Role | Character |
|---------|-----------|------|-----------|
| Kick | 36 | Feathered, subtle | Quiet, felt not heard |
| Snare (brush) | 38 | Comping, ghost notes | Swish, light |
| Ride | 51 | Swing pattern | Main timekeeping |
| Hi-hat (foot) | 44 | 2 and 4 | Chick sound |
| Crash | 49 | Punctuation | Sparse |

### Orchestral Percussion
| Element | MIDI Note | Role |
|---------|-----------|------|
| Timpani | 47 | Dramatic accents |
| Snare (concert) | 38 | Rolls, marches |
| Bass Drum (concert) | 36 | Deep thuds |
| Crash Cymbal | 49 | Climax |
| Tam-tam/Gong | 52 | Epic moments |
| Triangle | 81 | Gentle accent |
| Tubular Bells | 14 (inst) | Ceremonial |

### Latin Percussion Kit
| Element | MIDI Note | Role | Pattern |
|---------|-----------|------|---------|
| Conga High | 62 | Lead pattern | Open/slap |
| Conga Low | 63 | Foundation | Bass tone |
| Bongo High | 60 | Martillo | Alternating |
| Bongo Low | 61 | Anchor | Steady |
| Timbale High | 65 | Cascara | Shell pattern |
| Timbale Low | 66 | Accents | Fill |
| Cowbell | 56 | Clave guide | Steady 8ths |
| Claves | 75 | Clave pattern | 3-2 or 2-3 |
| Guiro | 73 | Scrape | Continuous |
| Shaker | 70 | 16th notes | Steady motion |

### African Percussion Kit
| Element | MIDI Note | Role |
|---------|-----------|------|
| Djembe Bass | 36 | Deep center hit |
| Djembe Tone | 47 | Edge hit |
| Djembe Slap | 38 | Sharp edge |
| Talking Drum | 50 | Pitch-bending |
| Shekere | 70 | Shaker pattern |
| Bell (Gankogui) | 56 | Timeline |

### Tabla Kit (Indian)
| Element | MIDI Note | Role | Bol |
|---------|-----------|------|-----|
| Tabla Na | 38 | Open ring | Na/Ta |
| Tabla Tin | 42 | Closed tip | Tin/Ti |
| Tabla Tun | 47 | Modulated | Tun |
| Bayan Ge | 36 | Bass open | Ge/Ga |
| Bayan Ka | 45 | Bass closed | Ka/Ke |

### Taiko Kit (Japanese)
| Element | MIDI Note | Role |
|---------|-----------|------|
| O-daiko (big) | 36 | Thunder bass |
| Chu-daiko (medium) | 47 | Lead pattern |
| Shime-daiko (small) | 38 | Sharp accents |
| Kane (bell) | 56 | Timekeeper |

---

## Rhythm Pattern Definitions

### Pop/Rock Standard
```
Kick:    [X . . . X . . . X . . . X . . .]  (1 and 3)
Snare:   [. . . . X . . . . . . . X . . .]  (2 and 4)
Hi-hat:  [X . X . X . X . X . X . X . X .]  (8th notes)
```

### Rock Driving
```
Kick:    [X . . . X . X . X . . . X . X .]  (1, and of 2, 3, and of 4)
Snare:   [. . . . X . . . . . . . X . . .]  (2 and 4)
Hi-hat:  [X X X X X X X X X X X X X X X X]  (16th notes)
```

### Four-on-Floor (House/Techno)
```
Kick:    [X . . . X . . . X . . . X . . .]  (every beat)
Clap:    [. . . . X . . . . . . . X . . .]  (2 and 4)
Hi-hat:  [. . X . . . X . . . X . . . X .]  (offbeats)
Open HH: [. . . . . . . X . . . . . . . X]  (upbeats of 2 and 4)
```

### Trap (half-time feel)
```
Kick:    [X . . . . . . . . . X . . . . .]  (1 and "and of 3")
Clap:    [. . . . . . . . X . . . . . . .]  (3, half-time)
Hi-hat:  [X.X.X.XXX.X.X.X.X.X.XXX.X.X.X.]  (rolls, varying velocity)
```

### Boom Bap
```
Kick:    [X . . . . . X . . . . . X . . .]  (1, and-of-2, 3-ish)
Snare:   [. . . . X . . . . . . . X . . .]  (2 and 4)
Hi-hat:  [X . X . X . X . X . X . X . X .]  (8th notes, varying velocity)
```

### Reggae One-Drop
```
Kick:    [. . . . . . . . X . . . . . . .]  (3 only!)
Snare:   [. . . . . . . . X . . . . . . .]  (3, with kick)
Hi-hat:  [X . X . X . X . X . X . X . X .]  (8th notes)
Rimshot: [. . . . . . X . . . . . . . X .]  (offbeats of 2 and 4)
```

### Bossa Nova
```
Kick:    [X . . X . . X . . . X . . X . .]  (syncopated)
Snare:   [. . X . . X . . X . . X . . X .]  (cross-stick, syncopated)
Hi-hat:  [X . X . X . X . X . X . X . X .]  (steady 8ths)
```

### Son Clave 3-2
```
Clave:   [X . . X . . X . . . X . X . . .]
```

### Son Clave 2-3
```
Clave:   [. . X . X . . . X . . X . . X .]
```

### Rumba Clave 3-2
```
Clave:   [X . . X . . . X . . X . X . . .]
```

### Bossa Nova Clave
```
Clave:   [X . . X . . X . . . X . . X . .]
```

### Samba (Partido Alto)
```
Surdo:   [X . . . . . . . X . . . . . X .]
Tamborim:[. X . X X . X . . X . X X . X .]
Shaker:  [X X X X X X X X X X X X X X X X]
```

### Dembow (Reggaeton)
```
Kick:    [X . . X . . X . X . . X . . X .]
Snare:   [. . . X . . . . . . . X . . . .]
Hi-hat:  [X . X . X . X . X . X . X . X .]
```

### Afrobeat (Tony Allen)
```
Kick:    [X . . . . . X . . . . X . . . .]  (syncopated)
Snare:   [. . . . X . . . . . . . X . . .]  (2 and 4)
Hi-hat:  [X X X X X X X X X X X X X X X X]  (16ths, ghost notes)
Open HH: [. . . . . . . X . . . . . . . X]
Bell:    [X . X . X . X . X . X . X . X .]  (constant 8ths)
```

### Irish Jig (6/8)
```
Bodhrán: [X . X . X . X . . X . .]  (6/8 compound)
```

### Jazz Swing
```
Ride:    [X . . X X . X . . X X .]  (swing triplet: ding-a-ding)
Hi-hat:  [. . . . . . X . . . . X]  (2 and 4 foot chick)
Kick:    [X . . . . . . . . . . .]  (feathered on 1)
```

### Waltz (3/4)
```
Bass:    [X . . . . .]
Chord:   [. . X . X .]
```

### Polka (2/4)
```
Kick:    [X . . .]
Snare:   [. . X .]
```

### Balkan 7/8 (2+2+3)
```
Kick:    [X . X . X . .]
Snare:   [. X . X . . X]
```

### Turkish 9/8 (2+2+2+3)
```
Kick:    [X . X . X . X . .]
Darbuka: [. X . X . X . . X]
```

---

## Swing Ratios

| Genre | Swing Ratio | Description |
|-------|------------|-------------|
| Straight (default) | 50/50 | No swing — pop, rock, electronic |
| Light Swing | 55/45 | Subtle groove — lo-fi, neo-soul |
| Medium Swing | 60/40 | Jazz, funk |
| Hard Swing | 66/34 | Triplet feel — classic jazz, shuffle blues |
| Dotted Swing | 75/25 | Extreme — New Orleans, Dixieland |

---

## Genre → Rhythm Pattern Mapping

| Genre ID | Time Sig | Pattern | Swing | Kit |
|----------|----------|---------|-------|-----|
| `pop.*` | 4/4 | Pop Standard | Straight | Standard |
| `rock.*` | 4/4 | Rock Driving | Straight | Standard |
| `rock.punk` | 4/4 | Fast Driving | Straight | Standard (hard) |
| `rock.progressive` | 5/4, 7/8 | Complex | Straight | Standard |
| `metal.*` | 4/4 | Double-bass | Straight | Standard (heavy) |
| `electronic.house` | 4/4 | Four-on-Floor | Straight | 808 / Electronic |
| `electronic.techno` | 4/4 | Four-on-Floor | Straight | Electronic |
| `electronic.trance` | 4/4 | Four-on-Floor | Straight | Electronic |
| `electronic.dubstep` | 4/4 | Half-time | Straight | 808 |
| `electronic.drum_and_bass` | 4/4 | Fast Breakbeat | Straight | Electronic |
| `electronic.uk_garage` | 4/4 | 2-Step Skippy | Straight | Electronic |
| `hiphop.boom_bap` | 4/4 | Boom Bap | Light swing | Standard |
| `hiphop.trap` | 4/4 | Trap Half-time | Straight | 808 |
| `hiphop.lofi_hiphop` | 4/4 | Boom Bap (slow) | Light swing | Vinyl/Lo-fi |
| `hiphop.drill` | 4/4 | Drill | Straight | 808 |
| `jazz.swing` | 4/4 | Jazz Swing | Hard swing | Jazz Brush |
| `jazz.bebop` | 4/4 | Jazz Swing (fast) | Hard swing | Jazz Brush |
| `jazz.bossa_nova` | 4/4 | Bossa Nova | Straight | Bossa |
| `jazz.latin` | 4/4 | Son Clave 3-2 | Straight | Latin Percussion |
| `blues.*` | 12/8 | Shuffle | Hard swing | Standard |
| `blues.gospel` | 4/4 | Gospel Groove | Medium swing | Standard + Tambourine |
| `rnb.funk` | 4/4 | Funk Syncopated | Light swing | Standard |
| `rnb.disco` | 4/4 | Four-on-Floor | Straight | Disco (open HH) |
| `folk.celtic` | 6/8 | Irish Jig | Straight | Bodhrán |
| `folk.country` | 4/4 | Country Train | Light swing | Country (brushes) |
| `folk.bluegrass` | 4/4 | Bluegrass Drive | Straight | Minimal |
| `folk.balkan` | 7/8, 9/8, 11/8 | Odd-meter | Straight | Balkan Brass |
| `latin.salsa` | 4/4 | Son Clave 3-2 | Straight | Latin Percussion |
| `latin.samba` | 2/4 | Samba Partido | Straight | Samba Batucada |
| `latin.reggae` | 4/4 | One-Drop | Straight | Reggae |
| `latin.reggaeton` | 4/4 | Dembow | Straight | 808 |
| `latin.tango` | 4/4 | Tango | Straight | Tango (bandoneon) |
| `latin.cumbia` | 4/4 | Cumbia | Straight | Latin + Accordion |
| `african.afrobeat` | 4/4 | Afrobeat | Straight | African Percussion |
| `african.amapiano` | 4/4 | Amapiano Log | Straight | 808 + Log drums |
| `african.soukous` | 4/4 | Sebene | Straight | Standard + Congas |
| `asian.hindustani` | Various | Teental (16 beat) | Straight | Tabla |
| `asian.bollywood` | 4/4 | Bollywood Mix | Straight | Tabla + Standard |
| `asian.gamelan` | 4/4 | Gongan Cycle | Straight | Gamelan Metalophone |
| `asian.japanese_traditional` | Free | Ma (silence) | Straight | Taiko |
| `asian.maqam` | 4/4, 10/8 | Maqsum | Straight | Darbuka |
| `asian.turkish` | 9/8 | Turkish 9/8 | Straight | Darbuka |
| `cinematic.epic` | 4/4 | Epic March | Straight | Orchestral |
| `cinematic.ambient` | 4/4 | Minimal/None | Straight | None/Sparse |
| `cinematic.horror` | 4/4 | Tension | Straight | Orchestral |

---

## Velocity Curves by Genre

| Genre Family | Kick | Snare | Hi-hat | Ghost Notes | Variation |
|-------------|------|-------|--------|------------|-----------|
| Pop | 90–100 | 85–95 | 60–70 | 40–50 | ±10 |
| Rock | 95–110 | 90–105 | 65–80 | 45–55 | ±15 |
| Metal | 100–120 | 95–115 | 70–90 | 50–60 | ±10 |
| Electronic | 100–127 | 85–100 | 50–80 | N/A | ±5 (precise) |
| Hip-Hop | 100–127 | 80–100 | 40–70 | 30–45 | ±20 (humanized) |
| Jazz | 50–75 | 40–65 | 30–55 | 25–40 | ±25 (very dynamic) |
| Folk | 70–90 | 65–85 | 50–65 | 35–50 | ±15 |
| Latin | 80–100 | 75–95 | 55–75 | 40–55 | ±15 |
| African | 85–105 | 80–100 | 60–80 | 45–60 | ±20 |
| Ambient | 40–60 | 35–55 | 25–45 | 20–35 | ±10 |
| Cinematic | 80–127 | 75–110 | 50–70 | 30–50 | ±20 |
