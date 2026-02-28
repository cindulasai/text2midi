# Scales and Modes — Comprehensive Reference

> **30+ scales/modes** with interval definitions, cultural origins, genre associations, and implementation-ready interval arrays.
> Expands the current 8 scales to cover all musical traditions worldwide.

---

## Currently Supported (8 scales)

These exist in `src/app/constants.py` today:

| Scale | Intervals | Notes (from C) |
|-------|-----------|----------------|
| major (Ionian) | `[0, 2, 4, 5, 7, 9, 11]` | C D E F G A B |
| minor (Aeolian) | `[0, 2, 3, 5, 7, 8, 10]` | C D Eb F G Ab Bb |
| dorian | `[0, 2, 3, 5, 7, 9, 10]` | C D Eb F G A Bb |
| mixolydian | `[0, 2, 4, 5, 7, 9, 10]` | C D E F G A Bb |
| pentatonic_major | `[0, 2, 4, 7, 9]` | C D E G A |
| pentatonic_minor | `[0, 3, 5, 7, 10]` | C Eb F G Bb |
| blues | `[0, 3, 5, 6, 7, 10]` | C Eb F F# G Bb |
| harmonic_minor | `[0, 2, 3, 5, 7, 8, 11]` | C D Eb F G Ab B |

---

## New Scales to Add (22 scales)

### Western Church Modes (3 missing)

| Scale | Intervals | Notes (from C) | Character | Genre Use |
|-------|-----------|----------------|-----------|-----------|
| phrygian | `[0, 1, 3, 5, 7, 8, 10]` | C Db Eb F G Ab Bb | Dark, Spanish, exotic | Flamenco, metal, Middle Eastern |
| lydian | `[0, 2, 4, 6, 7, 9, 11]` | C D E F# G A B | Dreamy, floating, bright | Film scores, jazz, prog rock |
| locrian | `[0, 1, 3, 5, 6, 8, 10]` | C Db Eb F Gb Ab Bb | Unstable, diminished feel | Metal, experimental, avant-garde |

### Minor Variants (1 missing)

| Scale | Intervals | Notes (from C) | Character | Genre Use |
|-------|-----------|----------------|-----------|-----------|
| melodic_minor | `[0, 2, 3, 5, 7, 9, 11]` | C D Eb F G A B | Jazzy, sophisticated | Jazz, classical, fusion |

### Ethnic/Regional Scales (14 new)

| Scale | Intervals | Notes (from C) | Character | Origin | Genre Use |
|-------|-----------|----------------|-----------|--------|-----------|
| phrygian_dominant | `[0, 1, 4, 5, 7, 8, 10]` | C Db E F G Ab Bb | Exotic, intense, Middle Eastern | Spain, Middle East, Balkans | Flamenco, Arabic maqam (Hijaz), Klezmer (Freygish), belly dance |
| hungarian_minor | `[0, 2, 3, 6, 7, 8, 11]` | C D Eb F# G Ab B | Dramatic, mystical | Hungary, Roma | Csárdás, Hungarian folk, Liszt |
| hungarian_major | `[0, 3, 4, 5, 7, 9, 10]` | C D# E F G A Bb | Exotic major, unexpected | Hungary | Bartók, folk |
| double_harmonic | `[0, 1, 4, 5, 7, 8, 11]` | C Db E F G Ab B | Byzantine, Arabic, dramatic | Middle East, Greece, India | Arabic classical, Byzantine chant, Bhairav raga |
| whole_tone | `[0, 2, 4, 6, 8, 10]` | C D E F# G# A# | Dreamlike, ambiguous, floating | France | Debussy, impressionist, film scores |
| diminished | `[0, 2, 3, 5, 6, 8, 9, 11]` | C D Eb F Gb Ab A B | Tense, symmetric, jazz | International | Jazz, film scores, suspense |
| chromatic | `[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]` | All 12 notes | Atonal, all notes | International | Avant-garde, 12-tone, free jazz |
| hirajoshi | `[0, 2, 3, 7, 8]` | C D Eb G Ab | Japanese, meditative, haunting | Japan | Japanese traditional, ambient, new age |
| in_scale | `[0, 1, 5, 7, 8]` | C Db F G Ab | Melancholic, Japanese minor | Japan | Japanese folk, min'yō, enka |
| yo_scale | `[0, 2, 5, 7, 9]` | C D F G A | Bright, Japanese major | Japan | Japanese folk, matsuri |
| bhairav | `[0, 1, 4, 5, 7, 8, 11]` | C Db E F G Ab B | Morning devotion, Indian | India (= double_harmonic) | Hindustani classical |
| kafi | `[0, 2, 3, 5, 7, 9, 10]` | C D Eb F G A Bb | Romantic, Indian Dorian | India (≈ Dorian) | Hindustani light classical |
| bayati | `[0, 1, 3, 5, 7, 8, 10]` | C Db Eb F G Ab Bb | Tender, Arabic | Arabic (≈ Phrygian) | Arabic classical, Turkish |
| rast | `[0, 2, 4, 5, 7, 9, 10]` | C D E F G A Bb | Majestic, Arabic major | Arabic (≈ Mixolydian) | Arabic classical, Turkish, Egyptian |

### Synthetic/Modern Scales (4 new)

| Scale | Intervals | Notes (from C) | Character | Genre Use |
|-------|-----------|----------------|-----------|-----------|
| prometheus | `[0, 2, 4, 6, 9, 10]` | C D E F# A Bb | Mystical, Scriabin | Avant-garde, experimental |
| enigmatic | `[0, 1, 4, 6, 8, 10, 11]` | C Db E F# G# A# B | Mysterious, tense | Film scores, dark ambient |
| super_locrian | `[0, 1, 3, 4, 6, 8, 10]` | C Db Eb Fb Gb Ab Bb | Altered dominant, tense | Jazz (altered scale), fusion |
| iwato | `[0, 1, 5, 6, 10]` | C Db F Gb Bb | Dark Japanese, eerie | Horror, Japanese-inspired |

---

## Scale Categories Quick Reference

### By Mood/Character

| Mood | Recommended Scales |
|------|--------------------|
| Happy, bright | major, lydian, pentatonic_major, yo_scale |
| Sad, melancholic | minor, harmonic_minor, in_scale, hirajoshi |
| Dark, ominous | phrygian, locrian, diminished, iwato |
| Exotic, Middle Eastern | phrygian_dominant, double_harmonic, bayati, rast |
| Mystic, floating | whole_tone, lydian, prometheus, enigmatic |
| Jazzy, sophisticated | dorian, melodic_minor, diminished, super_locrian |
| Bluesy, soulful | blues, pentatonic_minor, mixolydian, dorian |
| Meditative, peaceful | pentatonic_major, major, whole_tone, hirajoshi |
| Aggressive, intense | phrygian, locrian, chromatic, hungarian_minor |
| Romantic, warm | major, harmonic_minor, kafi, melodic_minor |

### By Cultural Region

| Region | Primary Scales |
|--------|---------------|
| Western Classical | major, minor, harmonic_minor, melodic_minor |
| Jazz | dorian, mixolydian, melodic_minor, blues, diminished |
| Blues/Soul | blues, pentatonic_minor, mixolydian |
| Middle Eastern | phrygian_dominant, double_harmonic, bayati, rast |
| Indian | harmonic_minor, dorian, double_harmonic (Bhairav), pentatonic_minor |
| Japanese | hirajoshi, in_scale, yo_scale, pentatonic_minor |
| Chinese | pentatonic_major, pentatonic_minor |
| Indonesian | pentatonic_major (slendro approximation) |
| Celtic/Irish | dorian, mixolydian, pentatonic_major |
| Flamenco/Spanish | phrygian_dominant, harmonic_minor, phrygian |
| Balkan/Eastern European | harmonic_minor, phrygian_dominant, hungarian_minor |
| African | pentatonic_major, pentatonic_minor, blues |
| Latin American | major, minor, mixolydian |

---

## Implementation: Python Dict for `constants.py`

```python
SCALES = {
    # === Western Modes (7) ===
    "major": [0, 2, 4, 5, 7, 9, 11],
    "minor": [0, 2, 3, 5, 7, 8, 10],
    "dorian": [0, 2, 3, 5, 7, 9, 10],
    "phrygian": [0, 1, 3, 5, 7, 8, 10],
    "lydian": [0, 2, 4, 6, 7, 9, 11],
    "mixolydian": [0, 2, 4, 5, 7, 9, 10],
    "locrian": [0, 1, 3, 5, 6, 8, 10],
    
    # === Minor Variants (3) ===
    "harmonic_minor": [0, 2, 3, 5, 7, 8, 11],
    "melodic_minor": [0, 2, 3, 5, 7, 9, 11],
    
    # === Pentatonic & Blues (4) ===
    "pentatonic_major": [0, 2, 4, 7, 9],
    "pentatonic_minor": [0, 3, 5, 7, 10],
    "blues": [0, 3, 5, 6, 7, 10],
    
    # === Ethnic/Regional (14) ===
    "phrygian_dominant": [0, 1, 4, 5, 7, 8, 10],
    "hungarian_minor": [0, 2, 3, 6, 7, 8, 11],
    "hungarian_major": [0, 3, 4, 5, 7, 9, 10],
    "double_harmonic": [0, 1, 4, 5, 7, 8, 11],
    "whole_tone": [0, 2, 4, 6, 8, 10],
    "diminished": [0, 2, 3, 5, 6, 8, 9, 11],
    "chromatic": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
    "hirajoshi": [0, 2, 3, 7, 8],
    "in_scale": [0, 1, 5, 7, 8],
    "yo_scale": [0, 2, 5, 7, 9],
    "bhairav": [0, 1, 4, 5, 7, 8, 11],
    "kafi": [0, 2, 3, 5, 7, 9, 10],
    "bayati": [0, 1, 3, 5, 7, 8, 10],
    "rast": [0, 2, 4, 5, 7, 9, 10],
    
    # === Synthetic/Modern (4) ===
    "prometheus": [0, 2, 4, 6, 9, 10],
    "enigmatic": [0, 1, 4, 6, 8, 10, 11],
    "super_locrian": [0, 1, 3, 4, 6, 8, 10],
    "iwato": [0, 1, 5, 6, 10],
}
```

**Total: 30 scales** (8 existing + 22 new)

---

## Scale Aliases (for intent matching)

```python
SCALE_ALIASES = {
    # Existing
    "ionian": "major",
    "aeolian": "minor",
    "natural_minor": "minor",
    
    # New
    "freygish": "phrygian_dominant",
    "hijaz": "phrygian_dominant",
    "spanish": "phrygian_dominant",
    "jewish": "phrygian_dominant",
    "gypsy": "hungarian_minor",
    "romani": "hungarian_minor",
    "byzantine": "double_harmonic",
    "arabic": "double_harmonic",
    "japanese": "hirajoshi",
    "indian": "harmonic_minor",
    "chinese": "pentatonic_major",
    "celtic": "dorian",
    "altered": "super_locrian",
    "octatonic": "diminished",
    "flamenco": "phrygian_dominant",
    "middle_eastern": "phrygian_dominant",
    "egyptian": "phrygian_dominant",
    "turkish": "phrygian_dominant",
    "klezmer": "phrygian_dominant",
    "balinese": "pentatonic_major",
    "gamelan": "pentatonic_major",
}
```
