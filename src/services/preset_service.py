# -*- coding: utf-8 -*-
"""
Preset Service — Dynamic LLM-Powered Preset Generation

Provides genre-aware preset prompts for the TUI sidebar:
  - Builds the genre tree from ``genre_registry.GENRE_TREE``
  - Generates creative prompt ideas on-demand via LLM
  - Falls back to curated seed presets when offline
  - Caches results in-memory (LRU, configurable max)

See SPEC-005-DYNAMIC-PRESETS for full specification.
"""

from __future__ import annotations

import json
import logging
import re
from collections import OrderedDict
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from src.config.genre_registry import (
    GenreNode,
    get_children,
    get_genre,
    get_root_genres,
)
from src.config.llm import call_llm

logger = logging.getLogger(__name__)


# =====================================================================
# Genre Emoji Mapping
# =====================================================================

GENRE_EMOJI: Dict[str, str] = {
    "classical": "🎻",
    "jazz": "🎷",
    "blues": "🎵",
    "rock": "🎸",
    "metal": "🤘",
    "electronic": "🎧",
    "hiphop": "🎤",
    "pop": "🎹",
    "rnb": "💜",
    "folk": "🪕",
    "latin": "💃",
    "african": "🌍",
    "asian": "🌏",
    "cinematic": "🎬",
    "lofi": "📻",
    "ambient": "🎹",
}


# =====================================================================
# Seed Presets — Curated fallback prompts (from PRESET_PROMPTS_LIBRARY.md)
# =====================================================================

_SEED_PRESETS: Dict[str, List[str]] = {
    # ── Classical ───────────────────────────────────────────────
    "classical": [
        "Write a classical chamber piece with elegant piano and sweeping cello",
        "Compose a baroque-inspired harpsichord and strings arrangement",
        "Create a romantic-era piano sonata in D minor with dramatic dynamics",
    ],
    "classical.baroque": [
        "Baroque concerto with harpsichord, strings, and ornamental flute",
        "Bach-inspired fugue with interweaving contrapuntal voices",
    ],
    "classical.romantic": [
        "Romantic orchestral piece with sweeping strings and dramatic crescendos",
        "Chopin-style nocturne with expressive rubato piano",
    ],
    "classical.minimalist": [
        "Minimalist piano piece with slowly shifting repetitive patterns",
        "Philip Glass style composition with arpeggiated piano and strings",
    ],
    "classical.symphonic": [
        "Sweeping orchestral symphony with strings, brass, and timpani",
        "Dramatic symphonic movement with building intensity and full orchestra",
    ],
    "classical.impressionist": [
        "Impressionist piano piece with whole-tone textures and soft dynamics",
        "Debussy-style atmospheric piece with harp and flute",
    ],
    "classical.chamber": [
        "String quartet with elegant interplay between violin, viola, and cello",
        "Chamber music for piano trio with lyrical melodies",
    ],

    # ── Jazz ────────────────────────────────────────────────────
    "jazz": [
        "Write a smooth jazz improvisation with sultry saxophone and piano comping",
        "Create a bebop jazz piece with fast piano runs and walking bass line",
        "Generate a cool jazz trio piece with brushed drums and muted trumpet",
    ],
    "jazz.swing": [
        "Swing era big band with brass section and walking bass",
        "Uptempo swing with ride cymbal and piano comping",
    ],
    "jazz.bebop": [
        "Fast bebop with saxophone runs and intricate piano voicings",
        "Charlie Parker style bebop with complex harmony and quick tempo",
    ],
    "jazz.cool": [
        "Cool jazz with muted trumpet, brushes, and laid-back feel",
        "West Coast cool jazz with flute and vibraphone",
    ],
    "jazz.modal": [
        "Modal jazz exploration in Dorian mode with sparse piano",
        "So What style modal jazz with bass ostinato and trumpet",
    ],
    "jazz.fusion": [
        "Jazz fusion with electric guitar, synth, and funk groove",
        "70s jazz fusion with Rhodes, wah guitar, and complex drums",
    ],
    "jazz.smooth": [
        "Smooth jazz with soprano sax and R&B groove",
        "Late-night smooth jazz with electric piano and soft drums",
    ],
    "jazz.gypsy": [
        "Django Reinhardt style gypsy jazz with fast acoustic guitar",
        "Gypsy jazz manouche with violin and rhythm guitar",
    ],
    "jazz.bossa_nova": [
        "Gentle bossa nova with nylon guitar and brushed drums",
        "Tom Jobim style bossa nova with warm guitar",
    ],
    "jazz.ethio": [
        "Ethiopian jazz with modal scales, organ, and brass",
        "Ethio-jazz groove with minor pentatonic and funky rhythm",
    ],
    "jazz.latin": [
        "Latin jazz with piano montuno, trumpet, and Afro-Cuban drums",
        "Salsa-jazz fusion with clave rhythm and saxophone",
    ],

    # ── Blues & Soul ────────────────────────────────────────────
    "blues": [
        "Generate a 12-bar Chicago blues with harmonica, electric guitar, and shuffle beat",
        "Create a Delta blues piece with acoustic slide guitar and foot stomps",
    ],
    "blues.delta": [
        "Raw Delta blues with slide guitar and stomping rhythm",
        "Acoustic Delta blues, solo guitar fingerpicking",
    ],
    "blues.chicago": [
        "Chicago electric blues with howling guitar and driving bass",
        "Chicago blues band with piano, harmonica, and shuffling drums",
    ],
    "blues.soul": [
        "Deep soul ballad with strings and passionate organ",
        "Old school soul with warm Wurlitzer and horns",
    ],
    "blues.neo_soul": [
        "Neo-soul with Fender Rhodes, warm bass, and gentle drums",
        "Modern neo-soul with lush harmonies and soft beats",
    ],
    "blues.gospel": [
        "Powerful gospel with choir, organ, and uplifting energy",
        "Gospel praise track with piano and clapping rhythm",
    ],

    # ── Rock ────────────────────────────────────────────────────
    "rock": [
        "Generate an indie rock song with jangly guitars and steady drumbeat",
        "Compose a power ballad with emotional piano intro building to full band",
    ],
    "rock.classic": [
        "70s classic rock with distorted guitar solo and steady beat",
        "Classic rock anthem with piano intro and big chorus",
    ],
    "rock.progressive": [
        "Progressive rock in 7/8 time with synth pads and complex drums",
        "Epic prog rock with alternating time signatures and Mellotron",
    ],
    "rock.psychedelic": [
        "Psychedelic rock with sitar drones and swirling organ",
        "60s psychedelic jam with wah-wah guitar and tabla",
    ],
    "rock.punk": [
        "Fast punk rock at 180 BPM with power chords and pure energy",
        "Ska-punk fusion with brass stabs and upstrokes",
    ],
    "rock.shoegaze": [
        "Shoegaze wall of sound with layers of tremolo guitar and ethereal pads",
        "Dreamy shoegaze with buried vocals and thick distortion",
    ],
    "rock.post_rock": [
        "Cinematic post-rock building from quiet piano to massive crescendo",
        "Post-rock with tremolo-picked guitar, delayed layers, and no drums",
    ],
    "rock.grunge": [
        "Raw grunge track with heavy distortion and angst",
        "90s Seattle grunge with quiet verse and explosive chorus",
    ],

    # ── Metal ───────────────────────────────────────────────────
    "metal": [
        "Create a heavy metal riff-driven track with double kick drums and distorted guitars",
        "Compose a symphonic metal piece with orchestral strings over aggressive drums",
    ],
    "metal.heavy": [
        "Heavy metal with galloping bass and shredding guitar solo",
        "Classic heavy metal with dual guitar harmony",
    ],
    "metal.symphonic": [
        "Symphonic metal with full orchestra, choir, and heavy riffs",
        "Epic symphonic metal battle theme with brass and strings",
    ],
    "metal.doom": [
        "Slow doom metal with crushing riffs and dark organ",
        "Funeral doom with glacial tempo and suffocating atmosphere",
    ],
    "metal.power": [
        "Triumphant power metal with soaring melodies and double bass drums",
        "Fantasy power metal with choir and fast arpeggios",
    ],
    "metal.djent": [
        "Djent with polyrhythmic guitar chugs and atmospheric clean sections",
        "Progressive djent with 8-string guitar and complex rhythms",
    ],
    "metal.thrash": [
        "Thrash metal with breakneck tempo, aggressive riffs, and shredding solo",
        "Old school thrash with palm-muted riffs and raw energy",
    ],

    # ── Electronic ──────────────────────────────────────────────
    "electronic": [
        "Generate a funky electronic groove with synth leads and syncopated bass",
        "Create a deep house track with warm bass, hi-hats, and smooth pads",
    ],
    "electronic.house": [
        "Deep house with warm pads, rolling bassline, and smooth groove",
        "Classic house track with piano chords and soulful vibes",
    ],
    "electronic.techno": [
        "Dark Berlin techno with pounding kick and industrial textures",
        "Acid techno with TB-303 bassline and relentless energy",
    ],
    "electronic.trance": [
        "Euphoric uplifting trance with soaring lead and emotional breakdown",
        "Progressive trance with lush pads and building arpeggios",
    ],
    "electronic.dubstep": [
        "Heavy dubstep with massive wobble bass and halfstep drums",
        "Melodic dubstep with emotional chords and powerful drops",
    ],
    "electronic.drum_and_bass": [
        "Liquid drum and bass with jazzy piano and fast breaks at 174 BPM",
        "Neurofunk DnB with aggressive bass design and tight drums",
    ],
    "electronic.synthwave": [
        "80s synthwave with retro arpeggios and neon vibes",
        "Dark synthwave with analog bass and cinematic atmosphere",
    ],
    "electronic.vaporwave": [
        "Vaporwave with slowed jazz samples and dreamy atmosphere",
        "Late night mall vaporwave with smooth electric piano",
    ],
    "electronic.future_bass": [
        "Future bass with lush chords, vocal chops, and heavy drops",
        "Colorful future bass with supersaw leads and bouncy rhythm",
    ],
    "electronic.downtempo": [
        "Cinematic downtempo with organic textures and slow groove",
        "Downtempo electronica with trip-hop drums and ambient pads",
    ],
    "electronic.idm": [
        "Glitchy IDM with fractured beats and evolving textures",
        "Ambient IDM with crystalline pads and generative rhythms",
    ],

    # ── Hip-Hop ─────────────────────────────────────────────────
    "hiphop": [
        "Create a hard-hitting trap beat with 808 bass, hi-hat rolls, and dark synths",
        "Generate a boom-bap hip hop beat with vinyl scratch and jazzy piano samples",
    ],
    "hiphop.boom_bap": [
        "90s boom bap with dusty vinyl drums and saxophone",
        "Classic New York boom bap with heavy kick and scratches",
    ],
    "hiphop.trap": [
        "Hard trap beat with 808 bass, rapid hi-hats, and dark piano",
        "Melodic trap with atmospheric pads and rolling 808s",
    ],
    "hiphop.lofi_hiphop": [
        "Lo-fi chill beats to study to with warm piano and vinyl crackle",
        "Rainy day lo-fi hip-hop with mellow guitar and soft drums",
        "Late night lo-fi with jazzy Rhodes and tape wobble",
    ],
    "hiphop.drill": [
        "UK drill with sliding 808s, dark piano, and aggressive drums",
        "Chicago drill with ominous strings and rapid hi-hats",
    ],
    "hiphop.phonk": [
        "Dark phonk with cowbell, distorted 808, and Memphis vocals",
        "Drift phonk with aggressive bass and lo-fi samples",
    ],
    "hiphop.g_funk": [
        "West Coast G-funk with smooth synth lead and funky bass",
        "90s G-funk cruising beat with talk box and whistles",
    ],

    # ── Pop ─────────────────────────────────────────────────────
    "pop": [
        "Create a catchy pop track with bright synths, driving drums, and vocal melody",
        "Compose a dreamy synth-pop ballad with lush pads and arpeggiated leads",
    ],
    "pop.synth_pop": [
        "80s-inspired synthpop with arpeggiated synths and punchy drums",
        "Retro synth pop with analog lead and driving bassline",
    ],
    "pop.kpop": [
        "High-energy K-pop track with dynamic drops and synth leads",
        "K-pop dance track with layered synths and powerful beats",
    ],
    "pop.jpop": [
        "Energetic J-pop with bright piano and uplifting melody",
        "Anime opening style track with fast tempo and orchestral hits",
    ],
    "pop.dream_pop": [
        "Ethereal dream pop with shimmering reverb guitars and soft vocals",
        "Hazy dream pop with warm pads and gentle rhythms",
    ],
    "pop.city_pop": [
        "Japanese city pop with funky electric piano and smooth saxophone",
        "1980s city pop groove with slap bass and bright guitar",
    ],
    "pop.tropical": [
        "Tropical pop with marimba, steel drums, and upbeat groove",
        "Island vibes pop track with acoustic guitar and light percussion",
    ],

    # ── R&B & Funk ──────────────────────────────────────────────
    "rnb": [
        "Create a silky neo-soul R&B track with warm Rhodes piano and soft drums",
        "Compose a 90s R&B slow jam with lush pads, finger snaps, and bass groove",
    ],
    "rnb.funk": [
        "Funky groove with slap bass, wah guitar, and tight drums",
        "Classic funk jam with brass stabs and clavinet",
    ],
    "rnb.disco": [
        "Disco anthem with strings, four-on-the-floor, and funky bass",
        "70s disco with orchestral hits and driving groove",
    ],
    "rnb.contemporary": [
        "Modern R&B with atmospheric pads and trap-influenced drums",
        "Sultry contemporary R&B with soft synths and slow groove",
    ],
    "rnb.neo_funk": [
        "Modern funk with synth bass and retro drum machine",
        "Lo-fi funk with minimalist arrangement and groovy bass",
    ],

    # ── Folk & Acoustic ─────────────────────────────────────────
    "folk": [
        "Generate a country song with acoustic guitar, pedal steel, and fiddle",
        "Create a Celtic folk tune with tin whistle, bodhrán drum, and fiddle",
    ],
    "folk.celtic": [
        "Irish jig in 6/8 with tin whistle and bodhrán",
        "Lively Celtic reel with fiddle and bouzouki",
    ],
    "folk.country": [
        "Classic country with steel guitar and train beat",
        "Modern country-pop with bright guitar and sing-along chorus",
    ],
    "folk.bluegrass": [
        "Fast bluegrass with banjo, mandolin, and flatpick guitar",
        "Bluegrass jam session with fiddle breakdown",
    ],
    "folk.americana": [
        "Americana roots rock with slide guitar and organ",
        "Heartland Americana with piano and pedal steel",
    ],
    "folk.balkan": [
        "Balkan brass band in 7/8 time with trumpet and tuba",
        "Bulgarian wedding music with clarinet and accordion",
    ],
    "folk.nordic": [
        "Scandinavian folk with nyckelharpa and gentle drone",
        "Nordic ambient folk with hardingfele and nature sounds",
    ],

    # ── Latin & Caribbean ───────────────────────────────────────
    "latin": [
        "Generate a salsa track with timbales, congas, piano montuno, and brass",
        "Create a reggaeton beat with dembow rhythm, 808 bass, and catchy melody",
    ],
    "latin.salsa": [
        "Hot salsa with brass, piano montuno, and driving percussion",
        "Romantic salsa with smooth trumpet and piano",
    ],
    "latin.reggaeton": [
        "Reggaeton with dembow beat, synth lead, and heavy bass",
        "Modern reggaeton perreo track at 92 BPM",
    ],
    "latin.bossa_nova": [
        "Bossa nova sunset with nylon guitar and soft percussion",
        "Modern bossa nova with piano, bass, and brushed drums",
    ],
    "latin.samba": [
        "Carnival samba with batucada percussion and brass",
        "Samba de roda with acoustic guitar and pandeiro",
    ],
    "latin.cumbia": [
        "Cumbia with accordion, güira, and bouncy bassline",
        "Colombian cumbia with gaita flute and drums",
    ],
    "latin.reggae": [
        "Roots reggae with skank guitar, organ bass, and one-drop drums",
        "Dub reggae with heavy delay and reverb on everything",
    ],
    "latin.tango": [
        "Argentine tango with bandoneon and dramatic violin",
        "Nuevo tango with piano and electronic elements",
    ],
    "latin.dancehall": [
        "Dancehall riddim with heavy bass and digital drums",
        "Modern dancehall with synth stabs and bouncy beat",
    ],

    # ── African ─────────────────────────────────────────────────
    "african": [
        "Create an Afrobeat groove with polyrhythmic drums, horns, and funky guitar",
        "Generate an Afro-pop track with bright guitars, shakers, and danceable beat",
    ],
    "african.afrobeat": [
        "Fela Kuti style Afrobeat with polyrhythmic drums and brass",
        "Afrobeat jam with organ, guitar, and Tony Allen drums",
    ],
    "african.amapiano": [
        "Amapiano with log bass, piano stabs, and shaker groove",
        "Deep amapiano with warm pads and gentle keys",
    ],
    "african.highlife": [
        "Ghanaian highlife with sweet guitar, trumpets, and steady groove",
        "Modern highlife fusion with electronic and traditional elements",
    ],
    "african.soukous": [
        "Congolese soukous with fast guitar sebene and dancing bass",
        "Soukous rumba with rhythm guitar and brass",
    ],
    "african.desert_blues": [
        "Saharan desert blues with hypnotic guitar and minimal percussion",
        "Tinariwen style desert rock with electric guitar and calabash",
    ],
    "african.gnawa": [
        "Moroccan Gnawa trance with guembri bass and metal castanets",
        "Gnawa spiritual music with hypnotic repetition and chanting",
    ],

    # ── Asian & Middle Eastern ──────────────────────────────────
    "asian": [
        "Create a Hindustani raga piece with sitar, tabla, and tanpura drone",
        "Generate a Chinese guzheng piece with pentatonic melody and bamboo flute",
    ],
    "asian.hindustani": [
        "Hindustani classical raga in Yaman with sitar and tabla",
        "Evening raga with slow alap building to rhythmic gat",
    ],
    "asian.carnatic": [
        "Carnatic classical with violin and mridangam in Adi tala",
        "Carnatic composition with veena and rhythmic patterns",
    ],
    "asian.bollywood": [
        "Bollywood dance number with tabla, strings, and synths",
        "Romantic Bollywood ballad with piano, sitar, and strings",
    ],
    "asian.gamelan": [
        "Javanese gamelan with interlocking metallophones and gongs",
        "Balinese gamelan kecak with rhythmic vocal patterns",
    ],
    "asian.maqam": [
        "Arabic maqam Bayati with oud, ney, and frame drum",
        "Lebanese pop with maqam Nahawand and modern production",
    ],
    "asian.turkish": [
        "Turkish classical with oud, ney, and kanun in 9/8",
        "Sufi music with ney flute and whirling rhythm",
    ],
    "asian.persian": [
        "Persian classical with tar, santoor, and tombak",
        "Iranian pop with Western and Persian fusion",
    ],
    "asian.qawwali": [
        "Qawwali devotional with harmonium, tabla, and handclaps",
        "Nusrat style Qawwali with building intensity and vocal power",
    ],
    "asian.japanese_traditional": [
        "Japanese koto and shakuhachi duet in pentatonic mode",
        "Festival matsuri music with taiko drums and fue",
    ],
    "asian.chinese_traditional": [
        "Chinese guzheng solo in pentatonic with gentle pipa",
        "Chinese silk and bamboo ensemble with erhu and dizi",
    ],

    # ── Cinematic & Ambient ─────────────────────────────────────
    "cinematic": [
        "Compose an epic cinematic orchestral piece with sweeping strings and brass",
        "Create a tense sci-fi cinematic score with staccato strings and building percussion",
    ],
    "cinematic.film_score": [
        "Sweeping orchestral film score with strings and brass",
        "Mystery film score with piano and suspended strings",
    ],
    "cinematic.epic": [
        "Epic cinematic trailer with massive drums and choir",
        "Triumphant victory theme with full orchestra",
    ],
    "cinematic.ambient": [
        "Peaceful ambient with soft pads and gentle piano",
        "Warm ambient meditation with slowly shifting harmonies",
        "Brian Eno style ambient with generative piano loops",
    ],
    "cinematic.dark_ambient": [
        "Dark ambient drone with unsettling textures and deep bass",
        "Haunting dark ambient with metallic resonance and whispers",
    ],
    "cinematic.horror": [
        "Horror soundtrack with dissonant strings and tension",
        "Psychological horror with unsettling piano and creeping bass",
    ],
    "cinematic.video_game": [
        "Retro 8-bit video game music with chiptune lead",
        "RPG adventure town theme with harp and flute",
        "Boss battle theme with heavy drums and aggressive synth",
    ],
    "cinematic.fantasy": [
        "Fantasy adventure with Celtic harp and mystical flute",
        "Medieval tavern music with lute and recorder",
    ],
    "cinematic.meditation": [
        "Tibetan singing bowl meditation with gentle bell sounds",
        "Zen meditation ambient with bamboo flute and silence",
    ],
    "cinematic.drone": [
        "Deep drone with layered synthesizers and long sustains",
        "Earth drone with rich harmonics and sub-bass vibrations",
    ],

    # ── Backward-compat alias roots ─────────────────────────────
    "lofi": [
        "Lo-fi chill beats to study to with warm piano and vinyl crackle",
        "Rainy day lo-fi hip-hop with mellow guitar and soft drums",
        "Late night lo-fi with jazzy Rhodes and tape wobble",
    ],
    "ambient": [
        "Peaceful ambient soundscape with floating pads and soft bells",
        "Dark mysterious ambient piece with dissonant textures and drones",
        "Warm ambient wash with gentle evolving synthesizer textures",
    ],
}


# =====================================================================
# PresetService
# =====================================================================

# Default persistence path (next to outputs/)
_DEFAULT_PERSIST_PATH = Path(__file__).resolve().parent.parent.parent / "preset_cache.json"


class PresetService:
    """Dynamic LLM-powered preset generation with registry-backed genre tree.

    Usage::

        svc = PresetService()
        roots = svc.get_root_categories()         # 14 root GenreNodes
        subs = svc.get_sub_genres("jazz")          # 14 jazz sub-genres
        prompts = svc.generate_presets("jazz.bebop")  # LLM-generated prompts
    """

    def __init__(self, cache_max: int = 100, persist_path: Optional[Path] = None) -> None:
        self._cache: OrderedDict[str, List[str]] = OrderedDict()
        self._cache_max = cache_max
        self._persist_path: Path = persist_path or _DEFAULT_PERSIST_PATH
        self._load_from_disk()

    # ------------------------------------------------------------------ #
    # Genre hierarchy
    # ------------------------------------------------------------------ #

    def get_root_categories(self) -> List[GenreNode]:
        """Return all 14 root-level genre nodes."""
        return get_root_genres()

    def get_sub_genres(self, root_id: str) -> List[GenreNode]:
        """Return direct children of a root genre."""
        return get_children(root_id)

    @staticmethod
    def get_emoji(genre_id: str) -> str:
        """Return the emoji for a root genre ID."""
        root = genre_id.split(".")[0]
        return GENRE_EMOJI.get(root, "🎵")

    @staticmethod
    def get_display_name(node: GenreNode) -> str:
        """Return a display-friendly name for a genre node."""
        if node.depth == 0:
            emoji = GENRE_EMOJI.get(node.id, "🎵")
            children = get_children(node.id)
            count = len(children)
            return f"{emoji} {node.name} ({count})" if count > 0 else f"{emoji} {node.name}"
        return node.name

    # ------------------------------------------------------------------ #
    # Preset generation
    # ------------------------------------------------------------------ #

    _MAX_DEDUP_RETRIES: int = 3  # max LLM retries to avoid duplicates

    def generate_presets(
        self,
        genre_id: str,
        count: int = 5,
        bypass_cache: bool = False,
    ) -> List[str]:
        """Generate creative prompt ideas for a genre via LLM.

        Args:
            genre_id: Dot-notation genre ID (e.g. ``"jazz.bebop"``).
            count: Number of prompts to generate.
            bypass_cache: If True, skip cache and generate fresh prompts.

        Returns:
            List of prompt strings. Falls back to seed presets on error.
        """
        # Check cache first
        if not bypass_cache and genre_id in self._cache:
            logger.debug("Cache hit for %s", genre_id)
            return self._cache[genre_id]

        # Look up genre node
        node = get_genre(genre_id)
        if node is None:
            logger.warning("Genre %s not found, returning seeds", genre_id)
            return self.get_seed_presets(genre_id)[:count]

        # Existing prompts to check duplicates against
        existing = set(self._normalize(p) for p in self._cache.get(genre_id, []))

        # Build and call LLM (with retry on duplicates)
        for attempt in range(self._MAX_DEDUP_RETRIES):
            system_prompt, user_message = self._build_generation_prompt(node, count)
            try:
                response = call_llm(
                    system_prompt=system_prompt,
                    user_message=user_message,
                    temperature=min(0.9 + attempt * 0.05, 1.0),  # slightly raise temp on retry
                    max_tokens=800,
                )
                if response:
                    parsed = self._parse_response(response)[:count]  # strict limit
                    # Filter out duplicates
                    unique = [p for p in parsed if self._normalize(p) not in existing]
                    if unique:
                        if bypass_cache and genre_id in self._cache:
                            combined = self._cache[genre_id] + unique
                            self._cache_put(genre_id, combined)
                        else:
                            self._cache_put(genre_id, unique)
                        return unique
                    logger.debug("Attempt %d: all prompts were duplicates, retrying", attempt + 1)
            except Exception as exc:
                logger.warning("LLM preset generation failed for %s: %s", genre_id, exc)
                break  # don't retry on hard errors — fall through to seeds

        # Fallback to seeds (also respect count limit, filter duplicates)
        seeds = [s for s in self.get_seed_presets(genre_id) if self._normalize(s) not in existing][:count]
        if seeds:
            if bypass_cache and genre_id in self._cache:
                combined = self._cache[genre_id] + seeds
                self._cache_put(genre_id, combined)
            else:
                self._cache_put(genre_id, seeds)
        return seeds

    @staticmethod
    def _normalize(text: str) -> str:
        """Normalize a prompt for duplicate comparison (lowercase, stripped)."""
        return text.strip().lower()

    def get_seed_presets(self, genre_id: str) -> List[str]:
        """Return curated seed presets for a genre (offline fallback).

        Falls back to parent genre if no seeds for the specific ID.
        """
        seeds = _SEED_PRESETS.get(genre_id, [])
        if seeds:
            return list(seeds)

        # Try parent
        node = get_genre(genre_id)
        if node and node.parent:
            parent_seeds = _SEED_PRESETS.get(node.parent, [])
            if parent_seeds:
                return list(parent_seeds)

        # Try root
        root = genre_id.split(".")[0]
        root_seeds = _SEED_PRESETS.get(root, [])
        if root_seeds:
            return list(root_seeds)

        return [f"Create a {genre_id.replace('.', ' ')} composition with authentic instruments and feel"]

    def clear_cache(self) -> None:
        """Clear the entire preset cache (memory and disk)."""
        self._cache.clear()
        try:
            if self._persist_path.exists():
                self._persist_path.unlink()
        except Exception as exc:
            logger.warning("Failed to remove cache file: %s", exc)

    # ------------------------------------------------------------------ #
    # LLM prompt construction
    # ------------------------------------------------------------------ #

    @staticmethod
    def _build_generation_prompt(
        node: GenreNode, count: int
    ) -> Tuple[str, str]:
        """Build system + user prompts grounded in GenreNode metadata."""
        instruments_str = ", ".join(
            inst[0].replace("_", " ") for inst in node.instruments[:6]
        ) if node.instruments else "various instruments"

        system_prompt = (
            "You are a world-class music production expert and creative prompt writer. "
            "Generate unique, vivid, and diverse text prompts that a user would type to "
            "generate MIDI music. Each prompt should be 1-2 sentences, specific about "
            "instruments, mood, tempo feel, and style. Return ONLY a JSON array of strings. "
            "No markdown, no explanation — just the JSON array."
        )

        user_message = (
            f"Generate {count} unique and creative MIDI generation prompts for the genre: "
            f"{node.name}.\n\n"
            f"Genre context:\n"
            f"- Style: {node.name} ({node.id})\n"
            f"- Tempo range: {node.tempo_range[0]}-{node.tempo_range[1]} BPM\n"
            f"- Default key: {node.default_key} {node.default_scale}\n"
            f"- Energy level: {node.energy}\n"
            f"- Typical instruments: {instruments_str}\n"
            f"- Chord feel: {node.chord_feel}\n\n"
            f"Make each prompt unique with different moods, tempos, and instrument combinations. "
            f"Be specific and evocative. Return a JSON array of {count} strings."
        )

        return system_prompt, user_message

    # ------------------------------------------------------------------ #
    # Response parsing
    # ------------------------------------------------------------------ #

    @staticmethod
    def _parse_response(response: str) -> List[str]:
        """Parse LLM response into a list of prompt strings."""
        text = response.strip()

        # Strip markdown fences
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()

        # Try JSON parse
        try:
            data = json.loads(text)
            if isinstance(data, list):
                prompts = [
                    str(p).strip() for p in data
                    if isinstance(p, str) and 15 <= len(str(p).strip()) <= 250
                ]
                if prompts:
                    return prompts
        except json.JSONDecodeError:
            pass

        # Fallback: extract quoted strings
        pattern = r'"([^"]{15,250})"'
        matches = re.findall(pattern, text)
        if matches:
            return matches

        return []

    # ------------------------------------------------------------------ #
    # Cache management
    # ------------------------------------------------------------------ #

    def _cache_put(self, genre_id: str, prompts: List[str]) -> None:
        """Add to cache with LRU eviction and persist to disk."""
        if genre_id in self._cache:
            self._cache.move_to_end(genre_id)
        self._cache[genre_id] = prompts
        while len(self._cache) > self._cache_max:
            self._cache.popitem(last=False)
        self._save_to_disk()

    # ------------------------------------------------------------------ #
    # Disk persistence
    # ------------------------------------------------------------------ #

    def _load_from_disk(self) -> None:
        """Load cached presets from the JSON file on disk."""
        if not self._persist_path.exists():
            return
        try:
            data = json.loads(self._persist_path.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                for genre_id, prompts in data.items():
                    if isinstance(prompts, list):
                        self._cache[genre_id] = prompts
            logger.debug("Loaded %d cached preset groups from disk", len(self._cache))
        except Exception as exc:
            logger.warning("Failed to load preset cache from %s: %s", self._persist_path, exc)

    def _save_to_disk(self) -> None:
        """Persist the current cache to a JSON file."""
        try:
            self._persist_path.write_text(
                json.dumps(dict(self._cache), indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
        except Exception as exc:
            logger.warning("Failed to save preset cache to %s: %s", self._persist_path, exc)


# =====================================================================
# Module-level singleton
# =====================================================================

_service: Optional[PresetService] = None


def get_preset_service(cache_max: int = 100) -> PresetService:
    """Get or create the module-level PresetService singleton."""
    global _service
    if _service is None:
        _service = PresetService(cache_max=cache_max)
    return _service
