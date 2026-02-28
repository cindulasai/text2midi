# Genre Taxonomy — Master Hierarchical Tree

> **200+ genres** organized in a 3-level hierarchy: Root Category → Sub-Genre → Variant.
> This is the canonical reference. `src/config/genre_registry.py` is the code manifestation.

---

## Hierarchy Overview

| # | Root Category | Sub-genres | Description |
|---|--------------|-----------|-------------|
| 1 | Classical & Orchestral | 12 | Western art music from Baroque to Contemporary |
| 2 | Jazz | 14 | America's classical music and its global offshoots |
| 3 | Blues & Soul | 10 | The roots of modern popular music |
| 4 | Rock | 16 | Guitar-driven music from the 1950s onward |
| 5 | Metal | 10 | Heavy, distorted, aggressive rock offshoots |
| 6 | Electronic & Dance | 20 | Synthesizer/computer-based music |
| 7 | Hip-Hop & Urban | 12 | Beat-driven vocal/instrumental music |
| 8 | Pop | 12 | Broadly appealing melodic music |
| 9 | R&B & Funk | 10 | Groove-based African-American music |
| 10 | Folk & Acoustic | 10 | Traditional and acoustic-based music |
| 11 | Latin & Caribbean | 16 | Music from Latin America and Caribbean islands |
| 12 | African | 14 | Music from the African continent |
| 13 | Asian & Middle Eastern | 18 | Music from Asia and the Middle East |
| 14 | Cinematic & Ambient | 12 | Atmospheric, functional, and film music |

**Total: ~200 uniquely defined presets**

---

## ID Convention

```
{root}.{sub_genre}.{variant}   (3 levels)
{root}.{sub_genre}             (2 levels — when no further breakdown)
{root}                         (1 level — root category only)
```

Examples: `electronic.house.deep_house`, `jazz.bebop`, `classical`

---

## 1. Classical & Orchestral

**Root ID:** `classical`
**Default:** tempo 60–120, key G major, energy medium, 4 tracks

| Sub-genre ID | Display Name | Tempo | Key | Scale | Energy | Tracks | Chord Feel | Instruments |
|-------------|-------------|-------|-----|-------|--------|--------|------------|-------------|
| `classical.baroque` | Baroque | 70–130 | D | major | medium | 4 | I-V-vi-IV, sequences | harpsichord, violin, cello, flute |
| `classical.classical_era` | Classical Era | 60–130 | C | major | medium | 4 | I-IV-V-I, Alberti bass | piano, violin, cello, flute |
| `classical.romantic` | Romantic | 50–120 | Eb | minor | high | 6 | Rich chromatic, I-vi-IV-V | piano, strings, french_horn, cello |
| `classical.impressionist` | Impressionist | 50–90 | Db | whole_tone | low | 4 | Parallel chords, whole-tone | piano, flute, harp, strings |
| `classical.contemporary` | Contemporary/20th Century | 40–140 | C | chromatic | medium | 5 | Atonal, clusters, serial | piano, strings, percussion, winds |
| `classical.minimalist` | Minimalist | 60–120 | C | major | low | 3 | Repetitive, phasing | piano, marimba, strings |
| `classical.chamber` | Chamber Music | 60–120 | G | major | medium | 4 | Classical harmony | violin, viola, cello, piano |
| `classical.symphonic` | Symphonic | 50–140 | Bb | minor | high | 7 | Full orchestral palette | strings, brass, woodwinds, timpani |
| `classical.choral` | Choral | 50–100 | F | major | medium | 4 | Hymn-like, SATB | choir, organ, strings |
| `classical.opera` | Opera | 50–140 | C | minor | high | 6 | Dramatic, recitative+aria | voice_oohs, strings, piano, brass |
| `classical.neoclassical` | Neo-classical | 60–120 | A | minor | medium | 4 | Modern classical fusion | piano, strings, synth_pad |
| `classical.avant_garde` | Avant-garde | 40–160 | C | chromatic | medium | 5 | Experimental, prepared | piano, percussion, strings, fx_atmosphere |

---

## 2. Jazz

**Root ID:** `jazz`
**Default:** tempo 80–140, key F dorian, energy medium, 5 tracks

| Sub-genre ID | Display Name | Tempo | Key | Scale | Energy | Tracks | Chord Feel | Instruments |
|-------------|-------------|-------|-----|-------|--------|--------|------------|-------------|
| `jazz.swing` | Swing | 120–180 | Bb | mixolydian | high | 5 | ii-V-I, swing rhythm | saxophone, trumpet, piano, bass, drums |
| `jazz.bebop` | Bebop | 140–280 | F | dorian | high | 5 | ii-V-I, rapid changes | saxophone, trumpet, piano, bass, drums |
| `jazz.cool` | Cool Jazz | 80–130 | C | dorian | low | 4 | Sparse, modal | trumpet, saxophone, piano, bass |
| `jazz.hard_bop` | Hard Bop | 120–200 | Bb | blues | high | 5 | Blues-inflected ii-V-I | saxophone, trumpet, piano, bass, drums |
| `jazz.free` | Free Jazz | 80–200 | C | chromatic | high | 5 | Atonal, free-form | saxophone, trumpet, bass, drums, piano |
| `jazz.modal` | Modal Jazz | 80–140 | D | dorian | medium | 5 | Modal vamps, So What | piano, saxophone, trumpet, bass, drums |
| `jazz.fusion` | Jazz Fusion | 100–160 | E | mixolydian | high | 6 | Complex harmony + rock | electric_guitar, synth_lead, bass, drums, saxophone, piano |
| `jazz.smooth` | Smooth Jazz | 80–120 | Eb | major | low | 4 | Gentle, polished | saxophone, electric_piano, bass, drums |
| `jazz.gypsy` | Gypsy Jazz | 130–220 | D | minor | high | 4 | Django-style, minor swing | acoustic_guitar, violin, bass, accordion |
| `jazz.acid` | Acid Jazz | 90–120 | Am | dorian | medium | 5 | Groove + jazz harmony | organ, electric_guitar, bass, drums, saxophone |
| `jazz.nu_jazz` | Nu-Jazz | 90–130 | C | dorian | medium | 5 | Electronic + jazz | synth_pad, saxophone, electric_bass, drums, piano |
| `jazz.ethio` | Ethio-Jazz | 90–130 | C | harmonic_minor | medium | 5 | Ethiopian scales + jazz | saxophone, organ, electric_guitar, bass, drums |
| `jazz.latin` | Latin Jazz | 100–150 | C | mixolydian | high | 6 | Clave + jazz harmony | piano, trumpet, saxophone, bass, drums, percussion |
| `jazz.bossa_nova` | Bossa Nova Jazz | 100–140 | F | major | low | 4 | ii-V-I bossa groove | acoustic_guitar, piano, bass, flute |

---

## 3. Blues & Soul

**Root ID:** `blues`
**Default:** tempo 60–120, key E blues, energy medium, 4 tracks

| Sub-genre ID | Display Name | Tempo | Key | Scale | Energy | Tracks | Chord Feel | Instruments |
|-------------|-------------|-------|-----|-------|--------|--------|------------|-------------|
| `blues.delta` | Delta Blues | 60–90 | E | blues | low | 3 | 12-bar blues | acoustic_guitar, harmonica, voice_oohs |
| `blues.chicago` | Chicago Blues | 80–120 | A | blues | medium | 5 | 12-bar electric | electric_guitar, harmonica, piano, bass, drums |
| `blues.electric` | Electric Blues | 90–130 | E | blues | high | 5 | 12-bar with band | electric_guitar, organ, bass, drums, saxophone |
| `blues.texas` | Texas Blues | 90–130 | G | blues | high | 5 | Shuffle, SRV style | electric_guitar, organ, bass, drums, saxophone |
| `blues.soul` | Soul | 70–110 | Ab | minor | medium | 5 | Gospel-flavored R&B | voice_oohs, organ, electric_guitar, bass, drums |
| `blues.motown` | Motown | 100–130 | C | major | high | 5 | Upbeat, hook-driven | electric_bass, drums, piano, strings, voice_oohs |
| `blues.neo_soul` | Neo-Soul | 70–100 | Db | dorian | low | 5 | J Dilla-influenced | electric_piano, synth_bass, drums, guitar, voice_oohs |
| `blues.gospel` | Gospel | 70–130 | C | major | high | 5 | Praise, choral | organ, piano, choir, bass, drums |
| `blues.boogie_woogie` | Boogie Woogie | 120–160 | C | blues | high | 4 | Walking bass piano | piano, bass, drums, guitar |
| `blues.rhythm_and_blues` | Classic R&B | 80–120 | F | blues | medium | 5 | Jump blues era | saxophone, piano, electric_guitar, bass, drums |

---

## 4. Rock

**Root ID:** `rock`
**Default:** tempo 110–140, key E minor, energy high, 5 tracks

| Sub-genre ID | Display Name | Tempo | Key | Scale | Energy | Tracks | Chord Feel | Instruments |
|-------------|-------------|-------|-----|-------|--------|--------|------------|-------------|
| `rock.classic` | Classic Rock | 110–140 | A | pentatonic_minor | high | 5 | I-IV-V, blues-rock | electric_guitar, bass, drums, organ, piano |
| `rock.hard` | Hard Rock | 120–150 | E | minor | high | 5 | Power chords, riffs | distortion_guitar, bass, drums, organ |
| `rock.progressive` | Progressive Rock | 70–160 | C | mixolydian | medium | 6 | Complex, odd meters | synth_lead, electric_guitar, bass, drums, piano, strings |
| `rock.psychedelic` | Psychedelic Rock | 80–130 | D | mixolydian | medium | 6 | Spacey, phased | electric_guitar, synth_pad, bass, drums, organ, sitar |
| `rock.alternative` | Alternative Rock | 100–140 | C | minor | medium | 5 | Indie-influenced | electric_guitar, bass, drums, piano, synth_pad |
| `rock.indie` | Indie Rock | 100–140 | G | major | medium | 5 | Jangly, lo-fi | acoustic_guitar, electric_guitar, bass, drums, synth_pad |
| `rock.grunge` | Grunge | 100–130 | D | minor | high | 4 | Drop-D, heavy/quiet | distortion_guitar, bass, drums, voice_oohs |
| `rock.punk` | Punk Rock | 150–200 | E | minor | very_high | 4 | Fast, 3-chord | distortion_guitar, bass, drums, voice_oohs |
| `rock.post_punk` | Post-Punk | 110–140 | Bb | minor | medium | 5 | Angular, atmospheric | electric_guitar, synth_lead, bass, drums, synth_pad |
| `rock.shoegaze` | Shoegaze | 80–120 | D | major | low | 5 | Wall of sound, reverb | electric_guitar, synth_pad, bass, drums, voice_oohs |
| `rock.garage` | Garage Rock | 130–170 | E | pentatonic_minor | high | 4 | Raw, lo-fi | electric_guitar, bass, drums, organ |
| `rock.surf` | Surf Rock | 130–170 | Am | minor | high | 4 | Reverb guitar, twang | electric_guitar, bass, drums, organ |
| `rock.southern` | Southern Rock | 100–140 | G | mixolydian | high | 5 | Twin guitar, boogie | electric_guitar, acoustic_guitar, bass, drums, piano |
| `rock.stoner` | Stoner Rock | 60–100 | D | pentatonic_minor | medium | 4 | Slow, heavy, fuzzy | distortion_guitar, bass, drums, organ |
| `rock.math` | Math Rock | 120–180 | C | major | high | 4 | Complex meters, tapping | electric_guitar, bass, drums, piano |
| `rock.post_rock` | Post-Rock | 60–140 | C | major | medium | 6 | Build-ups, cinematic | electric_guitar, synth_pad, bass, drums, piano, strings |

---

## 5. Metal

**Root ID:** `metal`
**Default:** tempo 120–180, key E minor, energy very_high, 5 tracks

| Sub-genre ID | Display Name | Tempo | Key | Scale | Energy | Tracks | Chord Feel | Instruments |
|-------------|-------------|-------|-----|-------|--------|--------|------------|-------------|
| `metal.heavy` | Heavy Metal | 120–160 | E | minor | very_high | 5 | Power chords, gallops | distortion_guitar, bass, drums, synth_lead |
| `metal.thrash` | Thrash Metal | 160–220 | E | minor | very_high | 4 | Fast riffs, tremolo | distortion_guitar, bass, drums |
| `metal.death` | Death Metal | 140–220 | D | phrygian | very_high | 4 | Blast beats, chromatic | distortion_guitar, bass, drums |
| `metal.black` | Black Metal | 140–200 | C | harmonic_minor | very_high | 4 | Tremolo, atmospheric | distortion_guitar, bass, drums, synth_pad |
| `metal.doom` | Doom Metal | 50–80 | D | minor | high | 4 | Ultra-slow, crushing | distortion_guitar, bass, drums, organ |
| `metal.power` | Power Metal | 130–180 | E | major | very_high | 6 | Uplifting, double-bass | distortion_guitar, bass, drums, synth_lead, choir, strings |
| `metal.symphonic` | Symphonic Metal | 120–160 | Cm | harmonic_minor | very_high | 7 | Orchestral + metal | distortion_guitar, bass, drums, strings, choir, piano, synth_pad |
| `metal.progressive` | Progressive Metal | 100–180 | C | mixolydian | high | 6 | Complex, polyrhythmic | distortion_guitar, bass, drums, piano, synth_lead, strings |
| `metal.nu` | Nu-Metal | 90–130 | D | minor | high | 5 | Down-tuned, groove | distortion_guitar, synth_bass, drums, synth_lead, voice_oohs |
| `metal.djent` | Djent | 100–140 | F# | phrygian | high | 5 | Polyrhythmic, 8-string | distortion_guitar, bass, drums, synth_pad, piano |

---

## 6. Electronic & Dance

**Root ID:** `electronic`
**Default:** tempo 120–135, key A minor, energy high, 6 tracks

| Sub-genre ID | Display Name | Tempo | Key | Scale | Energy | Tracks | Chord Feel | Instruments |
|-------------|-------------|-------|-----|-------|--------|--------|------------|-------------|
| `electronic.house` | House | 120–130 | C | minor | high | 6 | 4-on-floor, chord stabs | synth_pad, synth_bass, drums, piano, synth_lead |
| `electronic.deep_house` | Deep House | 118–125 | Am | minor | medium | 5 | Soulful pads, groovy | synth_pad, synth_bass, drums, electric_piano, organ |
| `electronic.tech_house` | Tech House | 122–130 | Am | minor | high | 5 | Minimal + groovy | synth_bass, drums, synth_lead, synth_pad, percussion |
| `electronic.techno` | Techno | 125–145 | Am | minor | high | 5 | Industrial, hypnotic | synth_bass, drums, synth_lead, synth_pad, fx_atmosphere |
| `electronic.trance` | Trance | 128–142 | Am | minor | high | 6 | Uplifting, anthemic | synth_lead, synth_pad, synth_bass, drums, piano, strings |
| `electronic.psytrance` | Psytrance | 140–150 | Am | phrygian | very_high | 5 | Rolling bassline, acid | synth_bass, drums, synth_lead, fx_atmosphere, synth_pad |
| `electronic.dubstep` | Dubstep | 138–142 | D | minor | very_high | 5 | Half-time, wobble | synth_bass, drums, synth_lead, synth_pad, fx_atmosphere |
| `electronic.drum_and_bass` | Drum & Bass | 160–180 | Am | minor | very_high | 5 | Fast breaks, deep bass | synth_bass, drums, synth_pad, synth_lead, fx_atmosphere |
| `electronic.jungle` | Jungle | 160–170 | Cm | minor | very_high | 5 | Breakbeats, reggae bass | synth_bass, drums, synth_pad, organ, fx_atmosphere |
| `electronic.uk_garage` | UK Garage | 130–140 | Cm | minor | high | 5 | Skippy 2-step rhythm | synth_bass, drums, synth_pad, piano, voice_oohs |
| `electronic.idm` | IDM | 80–160 | C | chromatic | medium | 5 | Glitchy, experimental | synth_lead, synth_pad, drums, synth_bass, fx_crystal |
| `electronic.synthwave` | Synthwave/Retrowave | 80–118 | Am | minor | medium | 5 | 80s nostalgia, arps | synth_lead, synth_pad, synth_bass, drums, electric_guitar |
| `electronic.vaporwave` | Vaporwave | 60–100 | C | major | low | 4 | Slowed, chopped samples | synth_pad, electric_piano, synth_bass, drums |
| `electronic.electro` | Electro | 125–135 | Am | minor | high | 5 | 808-driven, robotic | synth_bass, drums, synth_lead, synth_pad, voice_oohs |
| `electronic.breakbeat` | Breakbeat | 120–140 | Am | minor | high | 5 | Broken beat patterns | synth_bass, drums, synth_lead, synth_pad, electric_guitar |
| `electronic.downtempo` | Downtempo | 70–100 | Dm | minor | low | 5 | Chill, atmospheric | synth_pad, acoustic_guitar, synth_bass, drums, flute |
| `electronic.chillwave` | Chillwave | 80–110 | C | major | low | 4 | Dreamy, lo-fi synths | synth_pad, synth_lead, drums, synth_bass |
| `electronic.future_bass` | Future Bass | 130–150 | C | major | high | 6 | Supersaws, chopped vox | synth_lead, synth_pad, synth_bass, drums, voice_oohs, piano |
| `electronic.ambient_electronic` | Ambient Electronic | 60–90 | C | major | low | 3 | Textures, drones | synth_pad, fx_atmosphere, synth_lead |
| `electronic.gabber` | Gabber/Hardcore | 160–200 | Am | minor | very_high | 4 | Distorted kick, fast | synth_bass, drums, synth_lead, fx_atmosphere |

---

## 7. Hip-Hop & Urban

**Root ID:** `hiphop`
**Default:** tempo 80–100, key C minor, energy medium, 5 tracks

| Sub-genre ID | Display Name | Tempo | Key | Scale | Energy | Tracks | Chord Feel | Instruments |
|-------------|-------------|-------|-----|-------|--------|--------|------------|-------------|
| `hiphop.boom_bap` | Boom Bap | 85–100 | Am | minor | medium | 4 | Sampled jazz, soulful | piano, synth_bass, drums, saxophone |
| `hiphop.trap` | Trap | 130–170 | Cm | minor | high | 5 | 808 bass, hi-hat rolls | synth_bass, drums, synth_lead, synth_pad, piano |
| `hiphop.lofi_hiphop` | Lo-fi Hip-Hop | 70–90 | D | minor | low | 4 | Jazzy, dusty beats | electric_piano, synth_bass, drums, acoustic_guitar |
| `hiphop.drill` | Drill | 135–145 | Cm | minor | high | 4 | Dark, sliding 808s | synth_bass, drums, synth_lead, piano |
| `hiphop.grime` | Grime | 138–142 | Dm | minor | very_high | 4 | UK, aggressive | synth_bass, drums, synth_lead, synth_pad |
| `hiphop.crunk` | Crunk | 75–85 | Eb | minor | very_high | 4 | Southern, chant-heavy | synth_bass, drums, synth_lead, brass |
| `hiphop.g_funk` | G-Funk | 90–100 | Ab | minor | medium | 5 | West Coast, P-Funk | synth_lead, synth_bass, drums, piano, voice_oohs |
| `hiphop.conscious` | Conscious Hip-Hop | 85–100 | C | minor | medium | 5 | Jazzy, lyrical | piano, bass, drums, strings, saxophone |
| `hiphop.cloud_rap` | Cloud Rap | 60–80 | Db | minor | low | 4 | Ethereal, spacey | synth_pad, synth_bass, drums, synth_lead |
| `hiphop.phonk` | Phonk | 130–140 | Cm | minor | high | 4 | Memphis-style, cowbell | synth_bass, drums, piano, voice_oohs |
| `hiphop.afrobeats_fusion` | Afrobeats-Hip-Hop | 95–110 | Am | minor | high | 5 | Log drum, afro-swing | synth_bass, drums, synth_lead, kalimba, piano |
| `hiphop.uk_drill` | UK Drill | 138–143 | Cm | minor | high | 4 | Sliding 808, darker | synth_bass, drums, piano, strings |

---

## 8. Pop

**Root ID:** `pop`
**Default:** tempo 100–130, key C major, energy medium, 4 tracks

| Sub-genre ID | Display Name | Tempo | Key | Scale | Energy | Tracks | Chord Feel | Instruments |
|-------------|-------------|-------|-----|-------|--------|--------|------------|-------------|
| `pop.synth_pop` | Synth-Pop | 110–130 | C | major | medium | 5 | Synth-driven, catchy | synth_lead, synth_pad, synth_bass, drums, piano |
| `pop.indie_pop` | Indie Pop | 100–130 | G | major | medium | 5 | Jangly, charming | acoustic_guitar, synth_pad, bass, drums, piano |
| `pop.electropop` | Electropop | 118–130 | Am | minor | high | 5 | Electronic, danceable | synth_lead, synth_bass, drums, synth_pad, voice_oohs |
| `pop.dream_pop` | Dream Pop | 80–110 | C | major | low | 5 | Ethereal, reverb | synth_pad, electric_guitar, bass, drums, voice_oohs |
| `pop.art_pop` | Art Pop | 90–130 | C | major | medium | 6 | Experimental, eclectic | piano, synth_lead, strings, bass, drums, synth_pad |
| `pop.kpop` | K-Pop | 100–140 | C | major | high | 6 | Dynamic, polished | synth_lead, synth_bass, drums, piano, strings, synth_pad |
| `pop.jpop` | J-Pop | 110–140 | C | major | high | 5 | Melodic, bright | piano, synth_lead, bass, drums, strings |
| `pop.city_pop` | City Pop | 100–120 | Bb | major | medium | 5 | 80s Japanese, funkish | electric_piano, electric_guitar, synth_bass, drums, saxophone |
| `pop.bubblegum` | Bubblegum Pop | 110–140 | C | major | high | 4 | Simple, sugar-sweet | synth_lead, piano, bass, drums |
| `pop.power_pop` | Power Pop | 120–150 | G | major | high | 5 | Crunchy guitars + hooks | electric_guitar, bass, drums, piano, voice_oohs |
| `pop.tropical` | Tropical Pop | 100–120 | C | major | high | 5 | Island vibes, marimba | marimba, synth_bass, drums, acoustic_guitar, synth_pad |
| `pop.bedroom_pop` | Bedroom Pop | 80–110 | D | major | low | 4 | Lo-fi, intimate | acoustic_guitar, synth_pad, bass, drums |

---

## 9. R&B & Funk

**Root ID:** `rnb`
**Default:** tempo 70–100, key Ab minor, energy medium, 5 tracks

| Sub-genre ID | Display Name | Tempo | Key | Scale | Energy | Tracks | Chord Feel | Instruments |
|-------------|-------------|-------|-----|-------|--------|--------|------------|-------------|
| `rnb.classic` | Classic R&B | 80–110 | F | minor | medium | 5 | Smooth, groove | electric_piano, electric_bass, drums, guitar, strings |
| `rnb.contemporary` | Contemporary R&B | 70–100 | Ab | minor | medium | 5 | Modern production | synth_pad, synth_bass, drums, electric_piano, voice_oohs |
| `rnb.funk` | Funk | 95–115 | E | mixolydian | high | 5 | Syncopated, groove | electric_guitar, slap_bass, drums, organ, brass |
| `rnb.p_funk` | P-Funk | 90–110 | E | mixolydian | high | 6 | Space-funk, wah | synth_lead, electric_bass, drums, electric_guitar, organ, brass |
| `rnb.disco` | Disco | 110–130 | C | major | high | 6 | Four-on-floor, strings | strings, synth_bass, drums, electric_guitar, piano, brass |
| `rnb.new_jack_swing` | New Jack Swing | 100–120 | Ab | minor | high | 5 | Swing + hip-hop | synth_bass, drums, electric_piano, synth_lead, brass |
| `rnb.afroswing` | Afroswing | 95–110 | Am | minor | high | 5 | UK Afro-fusion | synth_bass, drums, synth_lead, kalimba, voice_oohs |
| `rnb.neo_funk` | Neo-Funk | 100–120 | E | mixolydian | high | 5 | Modern retro funk | synth_lead, synth_bass, drums, electric_guitar, brass |
| `rnb.quiet_storm` | Quiet Storm | 65–85 | Db | minor | low | 4 | Intimate, smooth | electric_piano, bass, drums, synth_pad |
| `rnb.alternative_rnb` | Alternative R&B | 70–100 | Cm | minor | medium | 5 | Experimental, moody | synth_pad, synth_bass, drums, electric_guitar, voice_oohs |

---

## 10. Folk & Acoustic

**Root ID:** `folk`
**Default:** tempo 90–130, key G major, energy medium, 4 tracks

| Sub-genre ID | Display Name | Tempo | Key | Scale | Energy | Tracks | Chord Feel | Instruments |
|-------------|-------------|-------|-----|-------|--------|--------|------------|-------------|
| `folk.americana` | Americana | 90–130 | G | major | medium | 4 | I-IV-V, country-folk | acoustic_guitar, banjo, fiddle, bass |
| `folk.country` | Country | 90–140 | G | mixolydian | medium | 5 | Nashville, twang | acoustic_guitar, fiddle, piano, bass, drums |
| `folk.bluegrass` | Bluegrass | 120–180 | G | major | high | 4 | Fast picking, drive | banjo, fiddle, acoustic_guitar, bass |
| `folk.singer_songwriter` | Singer-Songwriter | 70–120 | C | major | low | 3 | Simple, intimate | acoustic_guitar, piano, bass |
| `folk.celtic` | Celtic Folk | 100–140 | D | dorian | medium | 4 | Modal, dance tunes | fiddle, flute, accordion, acoustic_guitar |
| `folk.nordic` | Nordic Folk | 70–120 | Am | dorian | low | 4 | Haunting, minimal | fiddle, flute, harp, bass |
| `folk.balkan` | Balkan Folk | 100–160 | D | harmonic_minor | high | 5 | Odd meters, brass | accordion, clarinet, violin, bass, drums |
| `folk.contemporary` | Contemporary Folk | 80–120 | C | major | medium | 4 | Modern, storytelling | acoustic_guitar, piano, bass, drums |
| `folk.protest` | Protest/Political Folk | 80–120 | Am | minor | medium | 3 | Lyric-driven | acoustic_guitar, harmonica, bass |
| `folk.neofolk` | Neofolk | 70–110 | Am | minor | low | 4 | Dark, acoustic | acoustic_guitar, violin, drums, voice_oohs |

---

## 11. Latin & Caribbean

**Root ID:** `latin`
**Default:** tempo 100–140, key C major, energy high, 5 tracks

| Sub-genre ID | Display Name | Tempo | Key | Scale | Energy | Tracks | Chord Feel | Instruments |
|-------------|-------------|-------|-----|-------|--------|--------|------------|-------------|
| `latin.salsa` | Salsa | 150–200 | C | major | very_high | 6 | Clave-based, ii-V-I | trumpet, piano, bass, drums, percussion, trombone |
| `latin.reggaeton` | Reggaeton | 85–100 | Cm | minor | high | 4 | Dembow rhythm | synth_bass, drums, synth_lead, voice_oohs |
| `latin.bossa_nova` | Bossa Nova | 100–140 | F | major | low | 4 | ii-V-I, gentle groove | acoustic_guitar, piano, bass, drums |
| `latin.samba` | Samba | 120–160 | C | major | very_high | 5 | Batucada groove | acoustic_guitar, bass, drums, percussion, piano |
| `latin.cumbia` | Cumbia | 80–110 | C | major | high | 5 | Cumbia rhythm | accordion, electric_guitar, bass, drums, percussion |
| `latin.bachata` | Bachata | 120–140 | Dm | minor | medium | 4 | Romantic, guitar-led | acoustic_guitar, bass, drums, bongos |
| `latin.merengue` | Merengue | 140–180 | C | major | very_high | 5 | Fast 2-beat | accordion, saxophone, bass, drums, piano |
| `latin.son_cubano` | Son Cubano | 110–140 | G | major | high | 5 | Clave, tres guitar | acoustic_guitar, trumpet, bass, drums, piano |
| `latin.mambo` | Mambo | 140–180 | Bb | major | very_high | 6 | Big band Latin | trumpet, saxophone, piano, bass, drums, percussion |
| `latin.tango` | Tango | 90–130 | Dm | harmonic_minor | medium | 4 | Bandoneon + strings | accordion, violin, bass, piano |
| `latin.forro` | Forró | 100–130 | G | mixolydian | high | 4 | Northeast Brazilian | accordion, acoustic_guitar, drums, bass |
| `latin.ska` | Ska | 110–140 | C | major | high | 5 | Upbeat offbeat | electric_guitar, brass, bass, drums, organ |
| `latin.reggae` | Reggae | 70–110 | Am | minor | medium | 5 | One-drop, offbeat | electric_guitar, organ, electric_bass, drums, piano |
| `latin.dancehall` | Dancehall | 90–110 | Cm | minor | high | 4 | Riddim, digital | synth_bass, drums, synth_lead, voice_oohs |
| `latin.calypso` | Calypso/Soca | 110–140 | C | mixolydian | high | 5 | Carnival groove | marimba, brass, bass, drums, acoustic_guitar |
| `latin.dembow` | Dembow | 115–125 | Cm | minor | high | 4 | Dominican bounce | synth_bass, drums, synth_lead, voice_oohs |

---

## 12. African

**Root ID:** `african`
**Default:** tempo 100–130, key C major, energy high, 5 tracks

| Sub-genre ID | Display Name | Tempo | Key | Scale | Energy | Tracks | Chord Feel | Instruments |
|-------------|-------------|-------|-----|-------|--------|--------|------------|-------------|
| `african.afrobeat` | Afrobeat | 100–130 | Am | dorian | high | 6 | Fela-style, cyclic | electric_guitar, organ, trumpet, bass, drums, saxophone |
| `african.afropop` | Afropop | 100–120 | C | major | high | 5 | Melodic, danceable | electric_guitar, synth_bass, drums, synth_lead, piano |
| `african.highlife` | Highlife | 100–130 | C | major | high | 5 | Ghana/Nigeria, jazzy | electric_guitar, trumpet, bass, drums, piano |
| `african.amapiano` | Amapiano | 110–120 | Am | minor | medium | 5 | SA log drums, bass | synth_bass, drums, piano, kalimba, synth_pad |
| `african.kwaito` | Kwaito | 100–115 | Am | minor | medium | 4 | SA house, slow | synth_bass, drums, synth_pad, voice_oohs |
| `african.mbalax` | Mbalax | 110–140 | C | pentatonic_major | high | 5 | Senegal, sabar drums | electric_guitar, drums, bass, percussion, organ |
| `african.soukous` | Soukous | 120–150 | C | major | very_high | 5 | Congo rumba, guitar | electric_guitar, bass, drums, piano, brass |
| `african.gnawa` | Gnawa | 80–120 | D | pentatonic_minor | medium | 4 | Morocco, trance | bass, drums, kalimba, voice_oohs |
| `african.ethio_groove` | Ethio-Groove | 90–120 | C | harmonic_minor | medium | 5 | Ethiopian funk | organ, electric_guitar, bass, drums, saxophone |
| `african.chimurenga` | Chimurenga | 100–130 | C | pentatonic_major | high | 4 | Zimbabwe, mbira | kalimba, electric_guitar, bass, drums |
| `african.benga` | Benga | 120–140 | G | pentatonic_major | high | 4 | Kenya, fast guitar | electric_guitar, bass, drums, percussion |
| `african.desert_blues` | Desert Blues | 80–110 | Am | pentatonic_minor | medium | 4 | Tuareg, hypnotic | electric_guitar, bass, drums, percussion |
| `african.juju` | Jùjú | 100–120 | C | major | medium | 5 | Yoruba, talking drum | electric_guitar, bass, drums, percussion, organ |
| `african.makossa` | Makossa | 110–130 | C | major | high | 5 | Cameroon, danceable | electric_bass, electric_guitar, drums, saxophone, piano |

---

## 13. Asian & Middle Eastern

**Root ID:** `asian`
**Default:** tempo 70–110, key Am minor, energy medium, 4 tracks

| Sub-genre ID | Display Name | Tempo | Key | Scale | Energy | Tracks | Chord Feel | Instruments |
|-------------|-------------|-------|-----|-------|--------|--------|------------|-------------|
| `asian.hindustani` | Hindustani Classical | 60–140 | C | harmonic_minor | medium | 4 | Raga-based, drone | sitar, flute, tabla, bass |
| `asian.carnatic` | Carnatic Classical | 70–120 | C | harmonic_minor | medium | 4 | Raga + tala | violin, flute, bass, drums |
| `asian.bollywood` | Bollywood | 90–130 | Am | harmonic_minor | high | 6 | Dramatic, film | sitar, violin, synth_strings, drums, bass, piano |
| `asian.bhangra` | Bhangra | 100–130 | G | major | very_high | 5 | Punjabi, dhol-driven | drums, synth_lead, bass, synth_pad, electric_guitar |
| `asian.qawwali` | Qawwali | 70–120 | Dm | harmonic_minor | high | 4 | Sufi devotional | harmonium, drums, bass, voice_oohs |
| `asian.enka` | Enka | 60–90 | Am | pentatonic_minor | low | 3 | Japanese ballad | piano, strings, bass |
| `asian.gagaku` | Gagaku | 40–70 | C | pentatonic_major | low | 3 | Imperial court | flute, organ, glockenspiel |
| `asian.gamelan` | Gamelan | 60–100 | C | pentatonic_major | medium | 4 | Indonesian ensemble | glockenspiel, xylophone, marimba, bass |
| `asian.dangdut` | Dangdut | 100–130 | Am | harmonic_minor | high | 5 | Indonesian pop | flute, electric_guitar, drums, bass, synth_lead |
| `asian.pansori` | Pansori | 50–100 | Am | pentatonic_minor | medium | 2 | Korean narrative | voice_oohs, drums |
| `asian.kpop_traditional` | K-Traditional | 60–100 | Am | pentatonic_minor | low | 3 | Korean court music | koto, flute, drums |
| `asian.maqam` | Maqam/Arabic | 80–120 | D | phrygian_dominant | medium | 4 | Quarter-tone approximation | acoustic_guitar, flute, drums, bass |
| `asian.persian` | Persian Classical | 70–110 | D | harmonic_minor | low | 3 | Dastgah modal | acoustic_guitar, flute, drums |
| `asian.turkish` | Turkish Classical | 80–130 | D | phrygian_dominant | medium | 4 | Makam system | acoustic_guitar, flute, violin, drums |
| `asian.khaleeji` | Khaleeji/Gulf | 90–120 | Am | harmonic_minor | medium | 4 | Arabian Gulf | drums, bass, synth_pad, voice_oohs |
| `asian.throat_singing` | Throat Singing | 60–90 | C | pentatonic_minor | low | 2 | Mongolian overtone | voice_oohs, drums |
| `asian.chinese_traditional` | Chinese Traditional | 70–110 | C | pentatonic_major | medium | 3 | Silk & bamboo | koto, flute, glockenspiel |
| `asian.japanese_traditional` | Japanese Traditional | 60–100 | Am | pentatonic_minor | low | 3 | Ma (silence), wabi-sabi | koto, shamisen, flute |

---

## 14. Cinematic & Ambient

**Root ID:** `cinematic`
**Default:** tempo 70–100, key D minor, energy high, 7 tracks

| Sub-genre ID | Display Name | Tempo | Key | Scale | Energy | Tracks | Chord Feel | Instruments |
|-------------|-------------|-------|-----|-------|--------|--------|------------|-------------|
| `cinematic.film_score` | Film Score | 60–120 | Dm | minor | high | 7 | Orchestral, thematic | strings, brass, piano, drums, choir, flute, harp |
| `cinematic.epic` | Epic/Trailer | 80–130 | Cm | minor | very_high | 7 | Massive, building | strings, brass, choir, drums, piano, synth_pad, percussion |
| `cinematic.dark_ambient` | Dark Ambient | 40–70 | Cm | minor | low | 3 | Drones, tension | synth_pad, fx_atmosphere, bass |
| `cinematic.ambient` | Ambient | 60–80 | C | major | low | 3 | Floating, spacious | synth_pad, piano, strings |
| `cinematic.drone` | Drone | 30–60 | C | major | very_low | 2 | Sustained, evolving | synth_pad, fx_atmosphere |
| `cinematic.new_age` | New Age | 60–90 | C | major | low | 4 | Peaceful, nature | piano, flute, harp, synth_pad |
| `cinematic.meditation` | Meditation | 50–70 | C | major | very_low | 3 | Minimal, calm | synth_pad, bells, harp |
| `cinematic.lofi_ambient` | Lo-fi Ambient | 60–80 | D | minor | low | 3 | Textured, warm | synth_pad, piano, fx_atmosphere |
| `cinematic.video_game` | Video Game | 80–140 | C | major | medium | 5 | 8-bit to orchestral | synth_lead, piano, strings, drums, bass |
| `cinematic.documentary` | Documentary | 70–100 | G | major | medium | 4 | Understated, emotive | piano, strings, acoustic_guitar, bass |
| `cinematic.horror` | Horror | 50–90 | Cm | phrygian | high | 5 | Dissonant, unsettling | strings, synth_pad, fx_atmosphere, piano, drums |
| `cinematic.fantasy` | Fantasy/Adventure | 80–130 | D | major | high | 6 | Heroic, pastoral | flute, strings, brass, piano, drums, harp |

---

## Backward Compatibility Map

These original 10 genre IDs remain valid and map to sensible defaults:

| Legacy ID | Maps To | Behavior |
|-----------|---------|----------|
| `pop` | `pop` (root) | Uses root pop defaults |
| `rock` | `rock` (root) | Uses root rock defaults |
| `electronic` | `electronic` (root) | Uses root electronic defaults |
| `lofi` | `hiphop.lofi_hiphop` | Redirects to lo-fi hip-hop |
| `jazz` | `jazz` (root) | Uses root jazz defaults |
| `classical` | `classical` (root) | Uses root classical defaults |
| `ambient` | `cinematic.ambient` | Redirects to ambient under cinematic |
| `cinematic` | `cinematic` (root) | Uses root cinematic defaults |
| `funk` | `rnb.funk` | Redirects to funk under R&B |
| `rnb` | `rnb` (root) | Uses root R&B defaults |

---

## Genre Count Summary

| Root Category | Sub-genres |
|--------------|-----------|
| Classical & Orchestral | 12 |
| Jazz | 14 |
| Blues & Soul | 10 |
| Rock | 16 |
| Metal | 10 |
| Electronic & Dance | 20 |
| Hip-Hop & Urban | 12 |
| Pop | 12 |
| R&B & Funk | 10 |
| Folk & Acoustic | 10 |
| Latin & Caribbean | 16 |
| African | 14 |
| Asian & Middle Eastern | 18 |
| Cinematic & Ambient | 12 |
| **TOTAL** | **196** |

Plus 14 root categories = **210 total genre nodes** in the tree.
