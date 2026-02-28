# -*- coding: utf-8 -*-
"""
Cultural Music Database
Comprehensive knowledge base of world music traditions, instruments, scales, and characteristics.
"""

import logging
from dataclasses import dataclass, field
from typing import List, Tuple, Optional, Dict, Any

logger = logging.getLogger(__name__)


@dataclass
class CulturalMusicStyle:
    """Definition of a cultural/regional music style."""
    name: str
    aliases: List[str]  # Alternative names/keywords
    scales: List[str]   # Musical scales/modes used
    instruments: List[str]  # Traditional instruments (GM MIDI approximations)
    typical_tempo_range: Tuple[int, int]  # BPM range
    rhythm_patterns: List[str]  # Characteristic rhythms
    characteristics: str  # Descriptive text
    energy_default: str = "medium"  # Default energy level
    
    def matches(self, text: str) -> bool:
        """Check if this style matches the given text."""
        text_lower = text.lower()
        return any(alias.lower() in text_lower for alias in self.aliases)


# ============== CULTURAL MUSIC DATABASE ==============

CULTURAL_MUSIC_DATABASE: Dict[str, CulturalMusicStyle] = {
    
    # ===== EAST ASIAN =====
    
    "japanese": CulturalMusicStyle(
        name="Japanese Traditional",
        aliases=["japanese", "japan", "nihon", "wagaku", "japanese traditional", "j-traditional"],
        scales=["pentatonic_minor", "hirajoshi"],  # Yo, In scales (using closest GM equivalents)
        instruments=["koto", "shamisen", "shakuhachi", "taiko"],
        typical_tempo_range=(60, 100),
        rhythm_patterns=["ma", "jo_ha_kyu"],
        characteristics="Emphasis on ma (silence/negative space), nature-inspired, pentatonic scales, gradual development (jo-ha-kyu)",
        energy_default="low"
    ),
    
    "chinese": CulturalMusicStyle(
        name="Chinese Traditional",
        aliases=["chinese", "china", "zhongguo", "chinese traditional", "c-traditional"],
        scales=["pentatonic_major", "pentatonic_minor"],
        instruments=["pipa", "erhu", "dizi", "guzheng"],
        typical_tempo_range=(70, 110),
        rhythm_patterns=["banyan_rhythm"],
        characteristics="Pentatonic scales, silk and bamboo instruments, lyrical melodies",
        energy_default="medium"
    ),
    
    "korean": CulturalMusicStyle(
        name="Korean Traditional",
        aliases=["korean", "korea", "hanguk", "korean traditional", "k-traditional"],
        scales=["pentatonic_minor"],
        instruments=["gayageum", "daegeum", "janggu"],
        typical_tempo_range=(60, 100),
        rhythm_patterns=["jangdan"],
        characteristics="Pentatonic scales, ornamentation, slow-fast-slow structure",
        energy_default="medium"
    ),
    
    # ===== SOUTH ASIAN =====
    
    "carnatic": CulturalMusicStyle(
        name="Carnatic (South Indian Classical)",
        aliases=["carnatic", "south indian classical", "south indian", "karnatic", "karnataka"],
        scales=["harmonic_minor"],  # Raga approximations
        instruments=["violin", "flute", "sitar"],  # Using GM approximations for veena, mridangam
        typical_tempo_range=(70, 120),
        rhythm_patterns=["adi_tala", "rupaka_tala"],
        characteristics="Complex rhythmic patterns (talas), improvisation, drone (tanpura), gamakas (ornamentations), 72 melakarta ragas",
        energy_default="medium"
    ),
    
    "hindustani": CulturalMusicStyle(
        name="Hindustani (North Indian Classical)",
        aliases=["hindustani", "north indian classical", "north indian", "hindusthani"],
        scales=["harmonic_minor", "dorian"],  # Raga approximations
        instruments=["sitar", "tabla", "flute"],  # GM approximations for tabla, tanpura
        typical_tempo_range=(60, 140),
        rhythm_patterns=["teental", "jhaptal"],
        characteristics="Raga-based, alap-jor-jhala structure, tabla rhythms, improvisation, spiritual depth",
        energy_default="medium"
    ),
    
    "bollywood": CulturalMusicStyle(
        name="Bollywood/Indian Film",
        aliases=["bollywood", "indian film", "indian cinema", "hindi film"],
        scales=["minor", "harmonic_minor"],
        instruments=["sitar", "tabla", "violin", "synth_strings"],
        typical_tempo_range=(90, 130),
        rhythm_patterns=["bhangra", "dandiya"],
        characteristics="Fusion of Indian classical with Western pop, dramatic, danceable, orchestral",
        energy_default="high"
    ),
    
    # ===== MIDDLE EASTERN =====
    
    "sufi": CulturalMusicStyle(
        name="Sufi/Islamic Mystical",
        aliases=["sufi", "qawwali", "dhikr", "sufi music"],
        scales=["harmonic_minor", "dorian"],  # Maqam approximations (Hijaz, Rast, Bayati)
        instruments=["oud", "ney", "qanun", "daf"],  # GM approximations
        typical_tempo_range=(70, 110),
        rhythm_patterns=["sama_rhythm", "dhikr_patterns"],
        characteristics="Spiritual devotion, repetitive phrases, trance-inducing, maqam-based scales, call-and-response",
        energy_default="medium"
    ),
    
    "arabic": CulturalMusicStyle(
        name="Arabic Traditional",
        aliases=["arabic", "arab", "middle eastern", "arabian"],
        scales=["harmonic_minor", "dorian"],  # Maqam approximations
        instruments=["oud", "qanun", "ney", "darbuka"],
        typical_tempo_range=(80, 120),
        rhythm_patterns=["maqsum", "baladi"],
        characteristics="Maqam scales (quarter tones approximated), improvisation (taqsim), complex rhythms",
        energy_default="medium"
    ),
    
    "persian": CulturalMusicStyle(
        name="Persian/Iranian",
        aliases=["persian", "iranian", "iran", "persia"],
        scales=["harmonic_minor"],  # Dastgah approximations
        instruments=["santur", "tar", "ney", "tombak"],
        typical_tempo_range=(70, 110),
        rhythm_patterns=["persian_rhythm"],
        characteristics="Dastgah modal system, poetic, melancholic, improvisational",
        energy_default="low"
    ),
    
    # ===== AFRICAN =====
    
    "west_african": CulturalMusicStyle(
        name="West African",
        aliases=["west african", "african", "ghana", "senegal", "mali", "west africa"],
        scales=["pentatonic_major", "blues"],
        instruments=["kalimba", "kora", "djembe"],  # GM approximations
        typical_tempo_range=(100, 140),
        rhythm_patterns=["afrobeat", "highlife"],
        characteristics="Polyrhythmic, call-and-response, percussion-heavy, pentatonic melodies",
        energy_default="high"
    ),
    
    "south_african": CulturalMusicStyle(
        name="South African",
        aliases=["south african", "south africa", "zulu", "xhosa", "mbube"],
        scales=["major", "pentatonic_major"],
        instruments=["marimba", "choir"],
        typical_tempo_range=(90, 120),
        rhythm_patterns=["marabi", "kwela"],
        characteristics="Vocal harmonies, choral traditions, isicathamiya, mbube, jazz influences",
        energy_default="medium"
    ),
    
    # ===== LATIN AMERICAN =====
    
    "brazilian": CulturalMusicStyle(
        name="Brazilian",
        aliases=["brazilian", "brazil", "samba", "bossa nova", "brazilian music"],
        scales=["major", "minor"],
        instruments=["acoustic_guitar", "synth_bass", "shaker"],  # Approximations for cavaquinho, pandeiro, surdo
        typical_tempo_range=(100, 140),
        rhythm_patterns=["samba", "bossa_nova"],
        characteristics="Syncopated rhythms, samba groove, bossa nova coolness, percussion-rich",
        energy_default="high"
    ),
    
    "cuban": CulturalMusicStyle(
        name="Cuban/Afro-Cuban",
        aliases=["cuban", "cuba", "afro-cuban", "son", "rumba", "salsa"],
        scales=["major", "mixolydian"],
        instruments=["trumpet", "piano", "bass", "clap"],  # Conga, bongo approximations
        typical_tempo_range=(110, 140),
        rhythm_patterns=["clave", "son_clave"],
        characteristics="Clave rhythm foundation, Afro-Cuban percussion, syncopation, dance-oriented",
        energy_default="high"
    ),
    
    "mexican": CulturalMusicStyle(
        name="Mexican Traditional",
        aliases=["mexican", "mexico", "mariachi", "ranchera"],
        scales=["major", "minor"],
        instruments=["trumpet", "acoustic_guitar", "violin"],
        typical_tempo_range=(90, 130),
        rhythm_patterns=["ranchera", "corrido"],
        characteristics="Mariachi ensemble, dramatic vocals, rhythmic guitar (vihuela), festive",
        energy_default="high"
    ),
    
    "tango": CulturalMusicStyle(
        name="Argentine Tango",
        aliases=["tango", "argentine tango", "argentina"],
        scales=["minor", "harmonic_minor"],
        instruments=["accordion", "violin", "bass"],  # Bandoneon approximation
        typical_tempo_range=(90, 130),
        rhythm_patterns=["tango_rhythm"],
        characteristics="Dramatic, passionate, staccato rhythms, melancholic, dance-oriented",
        energy_default="medium"
    ),
    
    # ===== EUROPEAN =====
    
    "flamenco": CulturalMusicStyle(
        name="Flamenco",
        aliases=["flamenco", "spanish traditional", "andalusian"],
        scales=["harmonic_minor", "dorian"],  # Phrygian mode approximation
        instruments=["acoustic_guitar", "clap"],
        typical_tempo_range=(100, 180),
        rhythm_patterns=["bulerias", "alegrias"],
        characteristics="Passionate, rhythmic complexity, palmas (handclaps), Phrygian mode, guitar rasgueo",
        energy_default="high"
    ),
    
    "irish": CulturalMusicStyle(
        name="Irish Folk",
        aliases=["irish", "ireland", "celtic", "irish folk"],
        scales=["dorian", "mixolydian"],
        instruments=["fiddle", "flute", "accordion"],  # Tin whistle, bodhrán approximations
        typical_tempo_range=(100, 140),
        rhythm_patterns=["jig", "reel"],
        characteristics="Modal scales, jigs (6/8), reels (4/4), ornamentation, dance tunes",
        energy_default="medium"
    ),
    
    "scottish": CulturalMusicStyle(
        name="Scottish Traditional",
        aliases=["scottish", "scotland", "bagpipe", "scottish folk"],
        scales=["mixolydian", "pentatonic_major"],
        instruments=["bagpipe", "fiddle", "flute"],
        typical_tempo_range=(100, 140),
        rhythm_patterns=["strathspey", "reel"],
        characteristics="Bagpipes, pentatonic scales, strathspeys, reels, marches",
        energy_default="medium"
    ),
    
    "greek": CulturalMusicStyle(
        name="Greek Traditional",
        aliases=["greek", "greece", "rebetiko", "greek folk"],
        scales=["harmonic_minor", "dorian"],
        instruments=["bouzouki", "violin", "accordion"],  # GM approximations
        typical_tempo_range=(90, 130),
        rhythm_patterns=["zeimbekiko", "hasapiko"],
        characteristics="Bouzouki, rebetiko style, modal scales, emotional expression",
        energy_default="medium"
    ),
    
    "russian": CulturalMusicStyle(
        name="Russian Folk",
        aliases=["russian", "russia", "russian folk"],
        scales=["minor", "harmonic_minor"],
        instruments=["accordion", "balalaika", "violin"],  # GM approximations
        typical_tempo_range=(80, 120),
        rhythm_patterns=["khorovod"],
        characteristics="Melancholic, minor keys, accordion, choral singing traditions",
        energy_default="medium"
    ),
    
    # ===== CARIBBEAN =====
    
    "reggae": CulturalMusicStyle(
        name="Reggae/Jamaican",
        aliases=["reggae", "jamaican", "jamaica", "ska", "dub"],
        scales=["minor", "pentatonic_minor"],
        instruments=["electric_bass", "organ", "guitar"],
        typical_tempo_range=(70, 110),
        rhythm_patterns=["one_drop", "steppers"],
        characteristics="Offbeat rhythm (skank), bass-heavy, one drop drums, social commentary",
        energy_default="medium"
    ),
    
    "calypso": CulturalMusicStyle(
        name="Calypso/Trinidad",
        aliases=["calypso", "trinidad", "soca", "trinidadian"],
        scales=["major", "mixolydian"],
        instruments=["steel_drum", "marimba", "bass"],
        typical_tempo_range=(110, 140),
        rhythm_patterns=["calypso_rhythm"],
        characteristics="Steel pan, upbeat, carnival spirit, syncopation, storytelling",
        energy_default="high"
    ),
    
    # ===== NORTH AMERICAN =====
    
    "blues": CulturalMusicStyle(
        name="American Blues",
        aliases=["blues", "delta blues", "chicago blues"],
        scales=["blues", "pentatonic_minor"],
        instruments=["guitar", "harmonica", "organ"],
        typical_tempo_range=(60, 120),
        rhythm_patterns=["shuffle", "swing"],
        characteristics="12-bar blues, blue notes, swing feel, call-and-response, emotional depth",
        energy_default="medium"
    ),
    
    "country": CulturalMusicStyle(
        name="American Country",
        aliases=["country", "country music", "nashville", "honky tonk"],
        scales=["major", "mixolydian"],
        instruments=["acoustic_guitar", "fiddle", "steel_guitar"],
        typical_tempo_range=(90, 140),
        rhythm_patterns=["two_step", "waltz"],
        characteristics="Storytelling lyrics, twang, fiddle, steel guitar, simple harmonies",
        energy_default="medium"
    ),
    
    "bluegrass": CulturalMusicStyle(
        name="Bluegrass",
        aliases=["bluegrass", "appalachian"],
        scales=["major", "mixolydian"],
        instruments=["banjo", "fiddle", "acoustic_guitar"],
        typical_tempo_range=(120, 180),
        rhythm_patterns=["shuffle"],
        characteristics="Fast tempos, banjo rolls, high harmonies, instrumental virtuosity",
        energy_default="high"
    ),
    
    "native_american": CulturalMusicStyle(
        name="Native American",
        aliases=["native american", "indigenous american", "powwow"],
        scales=["pentatonic_minor"],
        instruments=["flute", "drums"],  # Native American flute, powwow drums
        typical_tempo_range=(70, 120),
        rhythm_patterns=["powwow_rhythm"],
        characteristics="Spiritual, nature-inspired, drums and flutes, pentatonic, chanting",
        energy_default="low"
    ),
    
    # ===== ADDITIONAL STYLES =====
    
    "klezmer": CulturalMusicStyle(
        name="Klezmer (Jewish)",
        aliases=["klezmer", "jewish", "yiddish"],
        scales=["harmonic_minor", "dorian"],  # Freygish mode
        instruments=["clarinet", "violin", "accordion"],
        typical_tempo_range=(100, 160),
        rhythm_patterns=["hora", "freylekhs"],
        characteristics="Clarinet-led, emotional expressiveness, dance tunes, Eastern European influences",
        energy_default="high"
    ),
    
    "balkan": CulturalMusicStyle(
        name="Balkan",
        aliases=["balkan", "bulgarian", "romanian", "serbian"],
        scales=["harmonic_minor", "dorian"],
        instruments=["accordion", "clarinet", "violin"],
        typical_tempo_range=(100, 160),
        rhythm_patterns=["asymmetric_meters"],  # 7/8, 9/8, 11/8
        characteristics="Complex meters (5/8, 7/8, 9/8), brass bands, energetic, folk dances",
        energy_default="high"
    ),
    
    "gamelan": CulturalMusicStyle(
        name="Indonesian Gamelan",
        aliases=["gamelan", "indonesian", "javanese", "balinese"],
        scales=["pentatonic_major"],  # Slendro, pelog approximations
        instruments=["glockenspiel", "xylophone", "marimba"],  # Gamelan approximations
        typical_tempo_range=(60, 100),
        rhythm_patterns=["gongan"],
        characteristics="Metallic percussion ensemble, interlocking rhythms, cyclic structures, pentatonic",
        energy_default="medium"
    ),
    
    "polynesian": CulturalMusicStyle(
        name="Polynesian/Hawaiian",
        aliases=["polynesian", "hawaiian", "hawaii", "tahitian"],
        scales=["major", "pentatonic_major"],
        instruments=["ukulele", "steel_guitar", "marimba"],
        typical_tempo_range=(80, 120),
        rhythm_patterns=["hula_rhythm"],
        characteristics="Ukulele, slack-key guitar, relaxed vibe, ocean imagery, vocal harmonies",
        energy_default="low"
    ),
    
    "aboriginal": CulturalMusicStyle(
        name="Australian Aboriginal",
        aliases=["aboriginal", "australian aboriginal", "didgeridoo"],
        scales=["pentatonic_minor"],
        instruments=["didgeridoo", "clap"],  # GM approximations
        typical_tempo_range=(60, 100),
        rhythm_patterns=["dreamtime_rhythm"],
        characteristics="Didgeridoo, circular breathing, drone, ancient traditions, storytelling",
        energy_default="low"
    ),
}


# ============== OCCASION-BASED MUSIC MAPPING ==============

OCCASION_MUSIC_MAP = {
    # Social Events
    "party": {"energy": "high", "tempo_range": (120, 140), "genre": "electronic", "density": 0.9},
    "wedding": {"energy": "high", "tempo_range": (110, 130), "genre": "pop", "density": 0.8},
    "birthday": {"energy": "high", "tempo_range": (115, 135), "genre": "pop", "density": 0.8},
    "celebration": {"energy": "high", "tempo_range": (120, 140), "genre": "pop", "density": 0.9},
    "dance": {"energy": "high", "tempo_range": (120, 140), "genre": "electronic", "density": 0.9},
    "club": {"energy": "high", "tempo_range": (125, 135), "genre": "electronic", "density": 1.0},
    
    # Relaxation
    "meditation": {"energy": "low", "tempo_range": (60, 75), "genre": "ambient", "density": 0.3},
    "yoga": {"energy": "low", "tempo_range": (70, 90), "genre": "ambient", "density": 0.4},
    "sleep": {"energy": "low", "tempo_range": (50, 70), "genre": "ambient", "density": 0.2},
    "relaxation": {"energy": "low", "tempo_range": (60, 80), "genre": "ambient", "density": 0.3},
    "spa": {"energy": "low", "tempo_range": (65, 85), "genre": "ambient", "density": 0.3},
    "massage": {"energy": "low", "tempo_range": (60, 80), "genre": "ambient", "density": 0.3},
    
    # Activities
    "workout": {"energy": "high", "tempo_range": (130, 160), "genre": "electronic", "density": 0.9},
    "gym": {"energy": "high", "tempo_range": (130, 150), "genre": "electronic", "density": 0.9},
    "running": {"energy": "high", "tempo_range": (140, 170), "genre": "electronic", "density": 0.8},
    "exercise": {"energy": "high", "tempo_range": (130, 160), "genre": "electronic", "density": 0.9},
    "study": {"energy": "low", "tempo_range": (70, 100), "genre": "lofi", "density": 0.5},
    "focus": {"energy": "low", "tempo_range": (70, 100), "genre": "lofi", "density": 0.5},
    "concentration": {"energy": "medium", "tempo_range": (80, 110), "genre": "lofi", "density": 0.5},
    "work": {"energy": "medium", "tempo_range": (90, 120), "genre": "lofi", "density": 0.6},
    
    # Venues
    "restaurant": {"energy": "low", "tempo_range": (80, 110), "genre": "jazz", "density": 0.5},
    "cafe": {"energy": "low", "tempo_range": (70, 100), "genre": "lofi", "density": 0.5},
    "bar": {"energy": "medium", "tempo_range": (90, 120), "genre": "jazz", "density": 0.6},
    "lounge": {"energy": "low", "tempo_range": (75, 105), "genre": "jazz", "density": 0.5},
    "elevator": {"energy": "low", "tempo_range": (70, 90), "genre": "ambient", "density": 0.3},
    
    # Media/Content
    "cinema": {"energy": "medium", "tempo_range": (70, 110), "genre": "cinematic", "density": 0.7},
    "film": {"energy": "medium", "tempo_range": (70, 110), "genre": "cinematic", "density": 0.7},
    "movie": {"energy": "medium", "tempo_range": (70, 110), "genre": "cinematic", "density": 0.7},
    "video": {"energy": "medium", "tempo_range": (90, 120), "genre": "pop", "density": 0.7},
    "background": {"energy": "low", "tempo_range": (70, 100), "genre": "ambient", "density": 0.4},
    "vlog": {"energy": "medium", "tempo_range": (100, 130), "genre": "pop", "density": 0.7},
    "podcast": {"energy": "low", "tempo_range": (70, 100), "genre": "ambient", "density": 0.3},
    "game": {"energy": "medium", "tempo_range": (90, 140), "genre": "electronic", "density": 0.7},
    "gaming": {"energy": "high", "tempo_range": (100, 150), "genre": "electronic", "density": 0.8},
    
    # Emotions/Moods
    "dramatic": {"energy": "high", "tempo_range": (80, 120), "genre": "cinematic", "density": 0.8},
    "epic": {"energy": "high", "tempo_range": (90, 130), "genre": "cinematic", "density": 0.9},
    "emotional": {"energy": "medium", "tempo_range": (70, 100), "genre": "classical", "density": 0.6},
    "sad": {"energy": "low", "tempo_range": (60, 80), "genre": "classical", "density": 0.4},
    "happy": {"energy": "high", "tempo_range": (110, 140), "genre": "pop", "density": 0.8},
    "romantic": {"energy": "medium", "tempo_range": (70, 100), "genre": "jazz", "density": 0.6},
    "mysterious": {"energy": "low", "tempo_range": (60, 90), "genre": "ambient", "density": 0.5},
    "suspense": {"energy": "medium", "tempo_range": (70, 110), "genre": "cinematic", "density": 0.6},
    "tension": {"energy": "high", "tempo_range": (90, 130), "genre": "cinematic", "density": 0.7},
    "hopeful": {"energy": "medium", "tempo_range": (80, 110), "genre": "classical", "density": 0.6},
    "inspiring": {"energy": "medium", "tempo_range": (90, 120), "genre": "cinematic", "density": 0.7},
    "motivational": {"energy": "high", "tempo_range": (110, 140), "genre": "rock", "density": 0.8},
}


# ============== DETECTOR CLASSES ==============

class CulturalMusicDetector:
    """Detect cultural music style from user prompt."""
    
    def __init__(self):
        self.database = CULTURAL_MUSIC_DATABASE
    
    def detect(self, prompt: str) -> Optional[CulturalMusicStyle]:
        """Detect cultural music style from prompt."""
        prompt_lower = prompt.lower()
        
        # Check each style for matches
        for style_key, style in self.database.items():
            if style.matches(prompt):
                logger.info("🌍 Detected cultural style: %s", style.name)
                return style
        
        return None
    
    def get_all_styles(self) -> List[str]:
        """Get list of all available cultural styles."""
        return [style.name for style in self.database.values()]


class OccasionDetector:
    """Detect occasion/use-case from user prompt."""
    
    def __init__(self):
        self.occasion_map = OCCASION_MUSIC_MAP
    
    def detect(self, prompt: str) -> Optional[Dict[str, Any]]:
        """Detect occasion/use-case from prompt."""
        prompt_lower = prompt.lower()
        
        # Check for occasion keywords
        for occasion, config in self.occasion_map.items():
            if occasion in prompt_lower:
                logger.info("🎯 Detected occasion: %s", occasion)
                return {"occasion": occasion, **config}
        
        return None
    
    def get_all_occasions(self) -> List[str]:
        """Get list of all available occasions."""
        return list(self.occasion_map.keys())


# ============== HELPER FUNCTIONS ==============

def get_cultural_instruments(cultural_style: Optional[CulturalMusicStyle], 
                            track_type: str, 
                            genre: str) -> str:
    """Get appropriate instrument for track type, considering cultural context."""
    
    if not cultural_style or not cultural_style.instruments:
        # Fallback to genre-based defaults
        return _get_default_instrument(track_type, genre)
    
    # Map track types to cultural instruments
    if track_type == "lead" and len(cultural_style.instruments) > 0:
        return cultural_style.instruments[0]  # Primary melodic instrument
    
    elif track_type == "harmony" and len(cultural_style.instruments) > 1:
        return cultural_style.instruments[1 if len(cultural_style.instruments) > 1 else 0]
    
    elif track_type == "bass":
        # Look for bass-like instrument, otherwise fallback
        for inst in cultural_style.instruments:
            if any(bass_word in inst.lower() for bass_word in ["bass", "contrabass", "oud"]):
                return inst
        return "bass"  # Standard GM bass
    
    elif track_type == "drums":
        # Look for percussion
        for inst in cultural_style.instruments:
            if any(perc in inst.lower() for perc in ["drum", "percussion", "tabla", "taiko", "darbuka", "djembe"]):
                return inst
        return "drums"  # Standard GM drums
    
    elif track_type in ["arpeggio", "counter_melody"] and len(cultural_style.instruments) > 2:
        return cultural_style.instruments[2] if len(cultural_style.instruments) > 2 else cultural_style.instruments[0]
    
    elif track_type == "pad":
        # Use sustained instruments if available
        for inst in cultural_style.instruments:
            if any(sus in inst.lower() for sus in ["organ", "choir", "pad", "strings"]):
                return inst
        return "synth_pad"  # Fallback
    
    else:
        return cultural_style.instruments[0] if cultural_style.instruments else "piano"


def _get_default_instrument(track_type: str, genre: str) -> str:
    """Get default instrument for track type based on genre."""
    defaults = {
        "lead": "piano",
        "harmony": "electric_piano",
        "bass": "bass",
        "drums": "drums",
        "arpeggio": "synth_lead",
        "pad": "synth_pad",
        "counter_melody": "flute",
        "fx": "fx_atmosphere"
    }
    return defaults.get(track_type, "piano")


# ============== MODULE EXPORTS ==============

__all__ = [
    "CulturalMusicStyle",
    "CULTURAL_MUSIC_DATABASE",
    "OCCASION_MUSIC_MAP",
    "CulturalMusicDetector",
    "OccasionDetector",
    "get_cultural_instruments",
]
