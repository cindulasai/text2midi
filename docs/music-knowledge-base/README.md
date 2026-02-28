# Music Knowledge Base

> **Purpose:** This folder is the single source of musical knowledge for the spec-kit (text2midi) platform. Every document here is designed to be consumed by both human developers and LLM agents implementing the world-class music preset system.

## How to Use These Docs

1. **LLM Implementers:** Read `IMPLEMENTATION_PLAN.md` first — it tells you exactly which files to change, in what order, and references every other doc.
2. **Music Researchers:** Browse by topic — each doc is self-contained.
3. **Preset Authors:** See `PRESET_PROMPTS_LIBRARY.md` for sample prompts and `GENRE_TAXONOMY.md` for the full hierarchy.

## Document Index

| Document | Purpose |
|----------|---------|
| [GENRE_TAXONOMY.md](GENRE_TAXONOMY.md) | Master hierarchical genre tree — 14 root categories → 80+ sub-genres → 200+ presets |
| [WORLD_MUSIC_BY_COUNTRY.md](WORLD_MUSIC_BY_COUNTRY.md) | Country-by-country music styles for 100+ nations with scales, instruments, rhythms |
| [SCALES_AND_MODES.md](SCALES_AND_MODES.md) | 30+ scales/modes with intervals, cultural origins, and genre associations |
| [CHORD_PROGRESSIONS_LIBRARY.md](CHORD_PROGRESSIONS_LIBRARY.md) | 100+ chord progressions organized by genre family |
| [RHYTHM_PATTERNS_LIBRARY.md](RHYTHM_PATTERNS_LIBRARY.md) | Rhythm patterns, time signatures, drum kits, and groove definitions |
| [INSTRUMENT_PALETTES.md](INSTRUMENT_PALETTES.md) | Per-genre instrument palettes with GM MIDI mappings for 100+ instruments |
| [PRESET_PROMPTS_LIBRARY.md](PRESET_PROMPTS_LIBRARY.md) | 500+ curated prompt examples organized by genre hierarchy |
| [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md) | Step-by-step code change guide for building the genre registry system |

## Architecture Principle

**Single Source of Truth:** All genre data flows from `src/config/genre_registry.py` which is the programmatic manifestation of `GENRE_TAXONOMY.md`. No more keeping 6+ files in manual sync.

```
GENRE_TAXONOMY.md (knowledge) → genre_registry.py (code) → all consumers auto-import
```

## Genre Hierarchy Design

```
Root Category (Level 0)     e.g., "Electronic & Dance"
  └─ Sub-Genre (Level 1)    e.g., "house"
       └─ Variant (Level 2)  e.g., "deep_house"
```

**ID Format:** Dot-notation — `electronic.house.deep_house`
**Backward Compat:** Original 10 genres (`pop`, `rock`, etc.) remain valid as aliases.

## Key Design Decisions

1. **3-level hierarchy** — Root → Sub-genre → Variant. Deep enough for specificity, shallow enough for usability.
2. **Dot-notation IDs** — `latin.salsa`, `asian.bollywood` — human-readable, parseable, sortable.
3. **Python registry over JSON** — Supports inheritance, computed properties, type checking with no extra deps.
4. **Cultural music merger** — The parallel `cultural_music.py` gets absorbed into the unified registry.
5. **Scale expansion** — From 8 to 30+ scales. Generators already handle arbitrary interval lists.
6. **Additive, not breaking** — All 10 original genres keep working identically.
