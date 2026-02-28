# Instrument Palettes by Genre

> Per-genre instrument palettes with GM MIDI program numbers, roles, and cultural instrument mappings.
> Expands GM_INSTRUMENTS from ~70 to 110+ entries with world music coverage.

---

## GM MIDI Instrument Additions

### New Entries for `GM_INSTRUMENTS` dict

These supplement the existing 70+ entries in `constants.py`:

```python
# === Additional World/Cultural Mappings ===
# These map cultural instrument names to the closest GM equivalent
GM_INSTRUMENTS_ADDITIONS = {
    # String instruments (cultural)
    "oud": 25,           # → Acoustic Guitar (steel) — Middle Eastern lute
    "pipa": 25,          # → Acoustic Guitar — Chinese lute
    "erhu": 40,          # → Violin — Chinese 2-string
    "guzheng": 107,      # → Koto — Chinese zither
    "gayageum": 107,     # → Koto — Korean zither
    "tar": 25,           # → Acoustic Guitar — Persian lute
    "santur": 15,        # → Dulcimer/Tubular Bells — Persian hammered dulcimer
    "bouzouki": 25,      # → Acoustic Guitar — Greek
    "balalaika": 25,     # → Acoustic Guitar — Russian triangle
    "ukulele": 25,       # → Acoustic Guitar — Hawaiian
    "mandolin": 25,      # → Acoustic Guitar — Italian/American
    "charango": 25,      # → Acoustic Guitar — Andean
    "steel_guitar": 25,  # → Steel-string Guitar
    "tres": 25,          # → Acoustic Guitar — Cuban
    "vihuela": 25,       # → Acoustic Guitar — Mexican
    "nyckelharpa": 110,  # → Fiddle — Swedish keyed fiddle
    "hardingfele": 110,  # → Fiddle — Norwegian Hardanger fiddle
    "morin_khuur": 110,  # → Fiddle — Mongolian horsehead
    "kora": 46,          # → Harp — West African 21-string
    "harp": 46,          # → Orchestral Harp
    
    # Wind instruments (cultural)
    "ney": 75,           # → Pan Flute — Middle Eastern flute
    "shakuhachi": 77,    # → Shakuhachi — Japanese bamboo flute (GM has it!)
    "dizi": 73,          # → Flute — Chinese transverse
    "daegeum": 73,       # → Flute — Korean transverse
    "bansuri": 73,       # → Flute — Indian bamboo
    "duduk": 68,         # → Oboe — Armenian double-reed
    "tin_whistle": 74,   # → Recorder — Irish/Celtic
    "zurna": 68,         # → Oboe — Turkish/Balkan
    "suona": 68,         # → Oboe — Chinese
    "didgeridoo": 58,    # → Tuba — Australian Aboriginal (deep drone)
    "harmonica": 22,     # → Harmonica
    "accordion": 21,     # → Accordion
    "harmonium": 20,     # → Reed Organ — Indian devotional
    "bandoneon": 21,     # → Accordion — Tango
    "melodica": 22,      # → Harmonica — Reggae
    "sheng": 20,         # → Reed Organ — Chinese mouth organ
    
    # Percussion (non-drum, pitched)
    "steel_drum": 114,   # → Steel Drums — Caribbean
    "hang_drum": 12,     # → Marimba — Modern handpan
    "tongue_drum": 12,   # → Marimba — Steel tongue drum
    "berimbau": 32,      # → Acoustic Bass — Brazilian (approx)
    "mbira": 108,        # → Kalimba — Zimbabwean thumb piano
    "balafon": 12,       # → Marimba — West African
    "angklung": 14,      # → Tubular Bells — Indonesian bamboo
    "rainstick": 96,     # → FX Rain
    
    # Percussion (drums — use channel 9)
    "tabla": -1,         # Drum channel → mapped via DRUM_MAP extensions
    "darbuka": -1,       # Drum channel (doumbek)
    "djembe": -1,        # Drum channel
    "cajon": -1,         # Drum channel
    "bodhran": -1,       # Drum channel — Irish
    "taiko": -1,         # Drum channel — Japanese
    "dhol": -1,          # Drum channel — Punjabi
    "surdo": -1,         # Drum channel — Brazilian
    "pandeiro": -1,      # Drum channel — Brazilian
    "janggu": -1,        # Drum channel — Korean
    "bongos": -1,        # Drum channel
    "congas": -1,        # Drum channel
    "timbales": -1,      # Drum channel
    
    # Synth (aliases)
    "supersaw": 81,      # → Sawtooth Lead
    "pluck": 80,         # → Synth Lead (Square)
    "wobble_bass": 87,   # → Lead 8 (bass + lead)
    "808_bass": 38,      # → Synth Bass 1
    "sub_bass": 38,      # → Synth Bass 1
    "acid_bass": 87,     # → Lead 8
    "reese_bass": 39,    # → Synth Bass 2
    "fm_bass": 38,       # → Synth Bass 1
    "pad_strings": 48,   # → String Ensemble
    "pad_choir": 52,     # → Choir Aahs
    "pad_atmosphere": 99, # → FX Atmosphere
    "bell_pad": 88,      # → New Age (Pad 1, also called Fantasy)
}
```

---

## Genre-Specific Instrument Palettes

### Classical & Orchestral

| Sub-genre | Lead | Harmony | Bass | Rhythm | Pad | Arpeggio | FX |
|-----------|------|---------|------|--------|-----|----------|-----|
| `classical.baroque` | harpsichord | violin | cello | - | strings | flute | - |
| `classical.classical_era` | piano | violin | cello | - | strings | flute | - |
| `classical.romantic` | piano | strings | cello | timpani | french_horn | harp | - |
| `classical.impressionist` | piano | flute | cello | - | harp | glockenspiel | fx_atmosphere |
| `classical.minimalist` | piano | marimba | bass | - | strings | vibraphone | - |
| `classical.symphonic` | violin | brass | contrabass | timpani | strings | flute | - |
| `classical.choral` | choir | organ | bass | - | strings | - | - |
| `classical.opera` | voice_oohs | strings | cello | timpani | piano | harp | brass |

### Jazz

| Sub-genre | Lead | Harmony | Bass | Rhythm | Pad | Arpeggio | FX |
|-----------|------|---------|------|--------|-----|----------|-----|
| `jazz.swing` | trumpet | piano | bass | drums | saxophone | - | - |
| `jazz.bebop` | saxophone | piano | bass | drums | trumpet | - | - |
| `jazz.cool` | trumpet | piano | bass | drums | - | flute | - |
| `jazz.modal` | saxophone | piano | bass | drums | - | trumpet | - |
| `jazz.fusion` | electric_guitar | piano | electric_bass | drums | synth_pad | saxophone | - |
| `jazz.smooth` | saxophone | electric_piano | bass | drums | synth_pad | - | - |
| `jazz.gypsy` | acoustic_guitar | violin | bass | - | accordion | acoustic_guitar | - |
| `jazz.bossa_nova` | acoustic_guitar | piano | bass | drums | flute | - | - |
| `jazz.ethio` | saxophone | organ | electric_bass | drums | - | electric_guitar | - |
| `jazz.latin` | trumpet | piano | bass | drums | saxophone | percussion | - |

### Blues & Soul

| Sub-genre | Lead | Harmony | Bass | Rhythm | Pad | Arpeggio | FX |
|-----------|------|---------|------|--------|-----|----------|-----|
| `blues.delta` | acoustic_guitar | harmonica | - | - | voice_oohs | - | - |
| `blues.chicago` | electric_guitar | piano | electric_bass | drums | harmonica | - | - |
| `blues.soul` | voice_oohs | organ | electric_bass | drums | strings | electric_guitar | - |
| `blues.motown` | voice_oohs | piano | electric_bass | drums | strings | - | - |
| `blues.neo_soul` | voice_oohs | electric_piano | synth_bass | drums | synth_pad | acoustic_guitar | - |
| `blues.gospel` | choir | organ | bass | drums | piano | - | - |

### Rock

| Sub-genre | Lead | Harmony | Bass | Rhythm | Pad | Arpeggio | FX |
|-----------|------|---------|------|--------|-----|----------|-----|
| `rock.classic` | electric_guitar | piano | bass | drums | organ | - | - |
| `rock.progressive` | synth_lead | piano | bass | drums | strings | electric_guitar | synth_pad |
| `rock.psychedelic` | electric_guitar | sitar | bass | drums | synth_pad | organ | fx_atmosphere |
| `rock.grunge` | distortion_guitar | - | bass | drums | voice_oohs | - | - |
| `rock.punk` | distortion_guitar | - | bass | drums | - | - | - |
| `rock.shoegaze` | electric_guitar | synth_pad | bass | drums | voice_oohs | - | fx_atmosphere |
| `rock.post_rock` | electric_guitar | piano | bass | drums | strings | synth_pad | fx_atmosphere |
| `rock.surf` | electric_guitar | organ | bass | drums | - | - | - |

### Metal

| Sub-genre | Lead | Harmony | Bass | Rhythm | Pad | Arpeggio | FX |
|-----------|------|---------|------|--------|-----|----------|-----|
| `metal.heavy` | distortion_guitar | - | bass | drums | - | synth_lead | - |
| `metal.symphonic` | distortion_guitar | strings | bass | drums | choir | piano | synth_pad |
| `metal.doom` | distortion_guitar | organ | bass | drums | - | - | fx_atmosphere |
| `metal.power` | distortion_guitar | choir | bass | drums | strings | synth_lead | - |
| `metal.djent` | distortion_guitar | piano | bass | drums | synth_pad | - | - |

### Electronic & Dance

| Sub-genre | Lead | Harmony | Bass | Rhythm | Pad | Arpeggio | FX |
|-----------|------|---------|------|--------|-----|----------|-----|
| `electronic.house` | synth_lead | piano | synth_bass | drums | synth_pad | - | - |
| `electronic.deep_house` | synth_lead | electric_piano | synth_bass | drums | synth_pad | organ | - |
| `electronic.techno` | synth_lead | - | synth_bass | drums | synth_pad | - | fx_atmosphere |
| `electronic.trance` | synth_lead | piano | synth_bass | drums | synth_pad | strings | - |
| `electronic.dubstep` | synth_lead | - | wobble_bass | drums | synth_pad | - | fx_atmosphere |
| `electronic.drum_and_bass` | synth_lead | - | synth_bass | drums | synth_pad | - | fx_atmosphere |
| `electronic.synthwave` | synth_lead | electric_guitar | synth_bass | drums | synth_pad | - | - |
| `electronic.vaporwave` | electric_piano | synth_pad | synth_bass | drums | - | - | fx_atmosphere |
| `electronic.future_bass` | synth_lead | piano | synth_bass | drums | voice_oohs | synth_pad | - |
| `electronic.downtempo` | synth_pad | acoustic_guitar | synth_bass | drums | flute | - | fx_atmosphere |

### Hip-Hop & Urban

| Sub-genre | Lead | Harmony | Bass | Rhythm | Pad | Arpeggio | FX |
|-----------|------|---------|------|--------|-----|----------|-----|
| `hiphop.boom_bap` | piano | saxophone | synth_bass | drums | - | - | - |
| `hiphop.trap` | synth_lead | piano | 808_bass | drums | synth_pad | - | - |
| `hiphop.lofi_hiphop` | electric_piano | acoustic_guitar | synth_bass | drums | - | - | fx_atmosphere |
| `hiphop.drill` | piano | - | 808_bass | drums | synth_lead | strings | - |
| `hiphop.g_funk` | synth_lead | piano | synth_bass | drums | voice_oohs | - | - |
| `hiphop.phonk` | piano | - | 808_bass | drums | voice_oohs | - | - |

### Pop

| Sub-genre | Lead | Harmony | Bass | Rhythm | Pad | Arpeggio | FX |
|-----------|------|---------|------|--------|-----|----------|-----|
| `pop.synth_pop` | synth_lead | piano | synth_bass | drums | synth_pad | - | - |
| `pop.kpop` | synth_lead | piano | synth_bass | drums | strings | synth_pad | - |
| `pop.jpop` | piano | synth_lead | bass | drums | strings | - | - |
| `pop.city_pop` | electric_piano | electric_guitar | synth_bass | drums | saxophone | - | - |
| `pop.dream_pop` | voice_oohs | synth_pad | bass | drums | electric_guitar | - | fx_atmosphere |
| `pop.tropical` | marimba | acoustic_guitar | synth_bass | drums | synth_pad | - | - |

### R&B & Funk

| Sub-genre | Lead | Harmony | Bass | Rhythm | Pad | Arpeggio | FX |
|-----------|------|---------|------|--------|-----|----------|-----|
| `rnb.funk` | electric_guitar | organ | slap_bass | drums | brass | - | - |
| `rnb.disco` | strings | piano | synth_bass | drums | electric_guitar | brass | - |
| `rnb.contemporary` | voice_oohs | electric_piano | synth_bass | drums | synth_pad | - | - |
| `rnb.neo_funk` | synth_lead | electric_guitar | synth_bass | drums | brass | - | - |

### Latin & Caribbean

| Sub-genre | Lead | Harmony | Bass | Rhythm | Pad | Arpeggio | FX |
|-----------|------|---------|------|--------|-----|----------|-----|
| `latin.salsa` | trumpet | piano | bass | drums | trombone | - | percussion |
| `latin.reggaeton` | synth_lead | - | synth_bass | drums | voice_oohs | - | - |
| `latin.bossa_nova` | acoustic_guitar | piano | bass | drums | flute | - | - |
| `latin.samba` | acoustic_guitar | piano | bass | drums | percussion | - | - |
| `latin.cumbia` | accordion | electric_guitar | bass | drums | - | percussion | - |
| `latin.reggae` | electric_guitar | organ | electric_bass | drums | piano | - | - |
| `latin.tango` | accordion | violin | bass | - | piano | - | - |
| `latin.ska` | electric_guitar | organ | bass | drums | brass | - | - |
| `latin.dancehall` | synth_lead | - | synth_bass | drums | voice_oohs | - | - |

### African

| Sub-genre | Lead | Harmony | Bass | Rhythm | Pad | Arpeggio | FX |
|-----------|------|---------|------|--------|-----|----------|-----|
| `african.afrobeat` | trumpet | organ | bass | drums | saxophone | electric_guitar | - |
| `african.amapiano` | piano | kalimba | synth_bass | drums | synth_pad | - | - |
| `african.highlife` | electric_guitar | trumpet | bass | drums | piano | - | - |
| `african.soukous` | electric_guitar | piano | bass | drums | brass | - | - |
| `african.desert_blues` | electric_guitar | - | bass | drums | percussion | - | - |
| `african.gnawa` | bass | kalimba | - | drums | voice_oohs | - | - |

### Asian & Middle Eastern

| Sub-genre | Lead | Harmony | Bass | Rhythm | Pad | Arpeggio | FX |
|-----------|------|---------|------|--------|-----|----------|-----|
| `asian.hindustani` | sitar | flute | bass | drums | - | - | - |
| `asian.carnatic` | violin | flute | bass | drums | - | - | - |
| `asian.bollywood` | sitar | violin | bass | drums | synth_strings | piano | - |
| `asian.gamelan` | glockenspiel | xylophone | - | marimba | - | - | - |
| `asian.maqam` | acoustic_guitar | flute | bass | drums | - | - | - |
| `asian.turkish` | acoustic_guitar | violin | bass | drums | flute | - | - |
| `asian.persian` | acoustic_guitar | flute | - | drums | - | - | - |
| `asian.japanese_traditional` | koto | shamisen | - | drums | flute | - | - |
| `asian.chinese_traditional` | koto | flute | - | glockenspiel | - | - | - |
| `asian.khaleeji` | voice_oohs | synth_pad | bass | drums | - | - | - |

### Cinematic & Ambient

| Sub-genre | Lead | Harmony | Bass | Rhythm | Pad | Arpeggio | FX |
|-----------|------|---------|------|--------|-----|----------|-----|
| `cinematic.film_score` | strings | brass | bass | drums | choir | harp | piano |
| `cinematic.epic` | brass | strings | bass | drums | choir | piano | synth_pad |
| `cinematic.dark_ambient` | - | - | bass | - | synth_pad | - | fx_atmosphere |
| `cinematic.ambient` | piano | strings | - | - | synth_pad | - | - |
| `cinematic.drone` | - | - | - | - | synth_pad | - | fx_atmosphere |
| `cinematic.meditation` | - | harp | - | - | synth_pad | bells | - |
| `cinematic.horror` | strings | synth_pad | bass | drums | - | piano | fx_atmosphere |
| `cinematic.video_game` | synth_lead | piano | bass | drums | strings | - | - |
| `cinematic.fantasy` | flute | strings | bass | drums | harp | piano | brass |
