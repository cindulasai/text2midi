# -*- coding: utf-8 -*-
"""
Advanced Intent Parser with Semantic Understanding
Uses chain-of-thought reasoning to deeply understand user requests.
Maps duration requests to composition structure, complexity, and pacing.

.. deprecated::
    This module is superseded by ``src.intent.engine.LLMIntentEngine``
    (PLAN-003). The dataclasses ``EnhancedMusicIntent``, ``CompositionStructure``,
    and ``CompositionComplexity`` are still imported by the compatibility bridge
    in ``src.intent.engine`` — do NOT delete this file until all downstream
    consumers have migrated to ``ParsedIntent``.
"""

import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import math


class MusicalStyle(Enum):
    """Detected musical style from prompt."""
    AMBIENT = "ambient"
    CINEMATIC = "cinematic"
    RHYTHMIC = "rhythmic"
    MELODIC = "melodic"
    HARMONIC = "harmonic"
    PERCUSSIVE = "percussive"
    MINIMALIST = "minimalist"
    COMPLEX = "complex"


class CompositionComplexity(Enum):
    """How complex the composition should be."""
    SIMPLE = "simple"          # Few instruments, clear structure
    MODERATE = "moderate"      # Balanced complexity
    RICH = "rich"             # Many layers, intricate details
    VERY_COMPLEX = "very_complex"  # Advanced composition techniques


@dataclass
class CompositionStructure:
    """Detailed composition structure inferred from duration and intent."""
    total_bars: int
    tempo: int
    time_signature: str = "4/4"
    
    # Structure sections (bars each)
    intro_bars: int = 0
    verse_bars: int = 0
    chorus_bars: int = 0
    bridge_bars: int = 0
    outro_bars: int = 0
    
    # Musical characteristics
    main_scale: str = "major"
    complexity: CompositionComplexity = CompositionComplexity.MODERATE
    primary_styles: List[MusicalStyle] = field(default_factory=list)
    
    # Pacing
    energy_arc: str = "build"  # "build", "smooth", "dynamic", "decay"
    intro_density: float = 0.3  # 0-1, how full the intro is
    
    def total_seconds(self) -> float:
        """Calculate total duration in seconds."""
        beats = self.total_bars * 4  # Assuming 4/4
        return (beats / self.tempo) * 60


@dataclass
class EnhancedMusicIntent:
    """Enhanced music intent with deep semantic understanding."""
    action: str
    genre: str
    mood: str
    energy: str
    
    # Duration details
    duration_seconds: Optional[int] = None
    duration_bars: Optional[int] = None
    
    # Instruments
    specific_instruments: List[str] = field(default_factory=list)
    instrument_priorities: Dict[str, int] = field(default_factory=dict)  # priority 1-10
    
    # Style
    style_descriptors: List[str] = field(default_factory=list)
    emotions: List[str] = field(default_factory=list)
    dynamics: str = "moderate"  # "minimal", "moderate", "dramatic"
    
    # Preferences
    tempo_preference: Optional[int] = None
    key_preference: Optional[str] = None
    complexity: CompositionComplexity = CompositionComplexity.MODERATE
    
    # Composition structure
    composition_structure: Optional[CompositionStructure] = None
    
    # Reasoning
    reasoning: List[str] = field(default_factory=list)
    
    # Original prompt
    raw_prompt: str = ""


class AdvancedIntentParser:
    """
    Advanced intent parser with multi-step reasoning.
    Understands duration, complexity, and mu...
    """
    
    # Emotion to MIDI parameter mappings
    EMOTION_MAPPING = {
        "happy": {"energy": "high", "mode": "major", "tempo_factor": 1.1},
        "sad": {"energy": "low", "mode": "minor", "tempo_factor": 0.8},
        "dark": {"energy": "medium", "mode": "harmonic_minor", "tempo_factor": 0.9},
        "bright": {"energy": "high", "mode": "major", "tempo_factor": 1.0},
        "melancholic": {"energy": "low", "mode": "minor", "tempo_factor": 0.85},
        "epic": {"energy": "high", "mode": "major", "tempo_factor": 1.0},
        "mysterious": {"energy": "medium", "mode": "minor", "tempo_factor": 0.95},
        "calm": {"energy": "low", "mode": "major", "tempo_factor": 0.7},
        "energetic": {"energy": "high", "mode": "major", "tempo_factor": 1.2},
        "ethereal": {"energy": "low", "mode": "major", "tempo_factor": 0.75},
        "dramatic": {"energy": "high", "mode": "minor", "tempo_factor": 1.05},
        "peaceful": {"energy": "low", "mode": "major", "tempo_factor": 0.65},
    }
    
    STYLE_TO_COMPLEXITY = {
        "ambient": CompositionComplexity.SIMPLE,
        "minimalist": CompositionComplexity.SIMPLE,
        "simple": CompositionComplexity.SIMPLE,
        "basic": CompositionComplexity.SIMPLE,
        
        "lofi": CompositionComplexity.MODERATE,
        "pop": CompositionComplexity.MODERATE,
        "standard": CompositionComplexity.MODERATE,
        
        "jazz": CompositionComplexity.RICH,
        "cinematic": CompositionComplexity.RICH,
        "orchestral": CompositionComplexity.RICH,
        "complex": CompositionComplexity.RICH,
        
        "avant_garde": CompositionComplexity.VERY_COMPLEX,
        "experimental": CompositionComplexity.VERY_COMPLEX,
        "innovative": CompositionComplexity.VERY_COMPLEX,
    }
    
    @staticmethod
    def parse_intent_deeply(prompt: str) -> EnhancedMusicIntent:
        """
        Parse user intent with multi-step reasoning.
        """
        parser = AdvancedIntentParser()
        intent = EnhancedMusicIntent(
            action="new",
            genre="pop",
            mood=prompt,
            energy="medium",
            raw_prompt=prompt
        )
        reasoning = []
        
        # Step 1: Extract duration
        reasoning.append("Step 1: Extracting duration information...")
        duration_info = parser._extract_duration(prompt)
        if duration_info:
            intent.duration_seconds = duration_info["seconds"]
            intent.duration_bars = duration_info["bars"]
            intent.tempo_preference = duration_info.get("tempo")
            reasoning.append(f"  ✓ Found duration: {intent.duration_seconds}s ({intent.duration_bars} bars @ {intent.tempo_preference} BPM)")
        
        # Step 2: Extract genre and style
        reasoning.append("Step 2: Analyzing genre and musical style...")
        genre, styles = parser._detect_genre_and_styles(prompt)
        intent.genre = genre
        intent.style_descriptors = styles.get("descriptors", [])
        intent.primary_styles = styles.get("styles", [])
        reasoning.append(f"  ✓ Genre: {genre} | Styles: {', '.join(str(s.value) for s in intent.primary_styles)}")

        # Apply genre-aware tempo when no explicit tempo was embedded in the prompt
        # (duration extraction defaults to 120 BPM; override with genre-appropriate value)
        GENRE_TEMPO_DEFAULTS = {
            "ambient": 65, "lofi": 80, "rnb": 88, "cinematic": 75,
            "classical": 90, "jazz": 110, "funk": 100,
            "pop": 110, "rock": 120, "electronic": 126,
        }
        genre_tempo = GENRE_TEMPO_DEFAULTS.get(genre, 120)
        if intent.tempo_preference == 120 and genre_tempo != 120:
            prev_tempo = intent.tempo_preference
            intent.tempo_preference = genre_tempo
            # Recalculate bars so duration in seconds stays consistent
            if intent.duration_seconds:
                beats = intent.duration_seconds * genre_tempo / 60
                intent.duration_bars = max(4, int(beats / 4))
            reasoning.append(f"  -> Tempo adjusted for genre '{genre}': {prev_tempo} -> {genre_tempo} BPM")

        # Apply tempo modifiers based on descriptive style keywords
        prompt_lower_tempo = prompt.lower()
        fast_boost = 1.0
        if any(kw in prompt_lower_tempo for kw in ("bebop", "presto", "vivace", "very fast", "blazing")):
            fast_boost = 1.6
        elif any(kw in prompt_lower_tempo for kw in ("upbeat", "fast", "uptempo", "rapid")):
            fast_boost = 1.3
        elif any(kw in prompt_lower_tempo for kw in ("slow", "ballad", "adagio", "largo", "meditative")):
            fast_boost = 0.8
        if fast_boost != 1.0:
            intent.tempo_preference = max(40, int(intent.tempo_preference * fast_boost))
            if intent.duration_seconds:
                beats = intent.duration_seconds * intent.tempo_preference / 60
                intent.duration_bars = max(4, int(beats / 4))
            reasoning.append(f"  -> Tempo modified by style keywords: {intent.tempo_preference} BPM")
        
        # Step 3: Extract emotional content
        reasoning.append("Step 3: Extracting emotional intent...")
        emotions, dynamics = parser._extract_emotions(prompt)
        intent.emotions = emotions
        intent.dynamics = dynamics
        reasoning.append(f"  ✓ Emotions: {', '.join(emotions)} | Dynamics: {dynamics}")
        
        # Step 4: Detect complexity level
        reasoning.append("Step 4: Determining composition complexity...")
        complexity = parser._determine_complexity(prompt, styles, intent.duration_bars or 16)
        intent.complexity = complexity
        reasoning.append(f"  ✓ Complexity level: {complexity.value}")
        
        # Step 5: Extract instruments
        reasoning.append("Step 5: Identifying instruments...")
        instruments = parser._extract_instruments(prompt)
        intent.specific_instruments = list(instruments.keys())
        intent.instrument_priorities = instruments
        reasoning.append(f"  ✓ Instruments: {', '.join(f'{name}({priority})' for name, priority in instruments.items())}")
        
        # Step 6: Build composition structure
        reasoning.append("Step 6: Planning composition structure...")
        structure = parser._build_composition_structure(
            duration_bars=intent.duration_bars or 16,
            complexity=complexity,
            tempo=intent.tempo_preference or 120,
            style_descriptors=intent.style_descriptors
        )
        intent.composition_structure = structure
        reasoning.append(f"  ✓ Structure: Intro({structure.intro_bars}) → Verse({structure.verse_bars}) → Chorus({structure.chorus_bars}) → Bridge({structure.bridge_bars}) → Outro({structure.outro_bars})")
        reasoning.append(f"  ✓ Total: {structure.total_bars} bars ({structure.total_seconds():.1f}s @ {structure.tempo} BPM)")
        
        # Step 7: Final energy inference
        reasoning.append("Step 7: Finalizing energy level...")
        energy_mapped = parser._determine_energy(emotions, intent.style_descriptors)
        intent.energy = energy_mapped
        reasoning.append(f"  ✓ Final energy: {energy_mapped}")
        
        intent.reasoning = reasoning
        return intent
    
    @staticmethod
    def _extract_duration(prompt: str) -> Optional[Dict]:
        """Extract duration and map to bars/tempo."""
        prompt_lower = prompt.lower()
        
        # Look for explicit duration markers
        patterns = [
            (r'(\d+)\s*:\s*(\d{2})', lambda m: {
                "seconds": int(m.group(1)) * 60 + int(m.group(2)),
                "format": "mm:ss"
            }),
            (r'(\d+(?:\.\d+)?)\s*(?:minutes?|mins?|m\b)', lambda m: {
                "seconds": int(float(m.group(1)) * 60),
                "format": "minutes"
            }),
            (r'(\d+(?:\.\d+)?)\s*(?:seconds?|secs?|s\b)', lambda m: {
                "seconds": int(float(m.group(1))),
                "format": "seconds"
            }),
            (r'(\d+)\s*bars?\b', lambda m: {
                "bars": int(m.group(1)),
                "format": "bars"
            }),
        ]
        
        for pattern, handler in patterns:
            match = re.search(pattern, prompt_lower)
            if match:
                result = handler(match)
                
                # Convert to standard units if needed
                if "seconds" in result:
                    duration_info = AdvancedIntentParser._convert_duration(result["seconds"])
                else:
                    duration_info = AdvancedIntentParser._bars_to_duration(result.get("bars", 16))
                
                return duration_info
        
        # If no explicit duration, infer from context
        if "short" in prompt_lower or "quick" in prompt_lower or "snippet" in prompt_lower:
            return AdvancedIntentParser._convert_duration(30)  # 30 seconds
        elif "medium" in prompt_lower or "standard" in prompt_lower:
            return AdvancedIntentParser._convert_duration(120)  # 2 minutes
        elif "extended" in prompt_lower or "suite" in prompt_lower:
            return AdvancedIntentParser._convert_duration(300)  # 5 minutes
        elif re.search(r'\blong\b(?!\s+(?:reverb|tail|tails|note|notes|sustain|decay|delay))', prompt_lower):
            # Only treat 'long' as duration when it's not describing a sound characteristic
            return AdvancedIntentParser._convert_duration(300)  # 5 minutes
        elif "epic" in prompt_lower or "cinematic" in prompt_lower:
            return AdvancedIntentParser._convert_duration(180)  # 3 minutes
        else:
            # Default: 2 minutes
            return AdvancedIntentParser._convert_duration(120)
    
    @staticmethod
    def _convert_duration(seconds: int, default_tempo: int = 120) -> Dict:
        """Convert seconds to bars and tempo information."""
        beats = (seconds * default_tempo) / 60
        bars = int(beats / 4)  # 4/4 time
        return {
            "seconds": seconds,
            "bars": max(4, bars),  # Minimum 4 bars
            "tempo": default_tempo,
            "beats": beats
        }
    
    @staticmethod
    def _bars_to_duration(bars: int, tempo: int = 120) -> Dict:
        """Convert bars to duration in seconds."""
        beats = bars * 4  # 4/4 time
        seconds = int((beats / tempo) * 60)
        return {
            "bars": bars,
            "seconds": seconds,
            "tempo": tempo,
            "beats": beats
        }
    
    @staticmethod
    def _detect_genre_and_styles(prompt: str) -> Tuple[str, Dict]:
        """Detect genre and associated musical styles."""
        prompt_lower = prompt.lower()
        
        genres = {
            "ambient": ["ambient", "pad", "drone", "atmospheric"],
            "electronic": ["electronic", "synth", "digital", "beep"],
            "jazz": ["jazz", "bebop", "swing", "improvise"],
            "classical": ["classical", "symphony", "orchestral", "baroque"],
            "lofi": ["lofi", "lo-fi", "chill", "studying", "relaxing"],
            "rock": ["rock", "metal", "power"],
            "cinematic": ["cinematic", "movie", "film", "dramatic", "epic"],
            "funk": ["funk", "groove", "funky", "bass"],
            "rnb": ["rnb", "r&b", "soul", "smooth"],
            "pop": ["pop", "catchy", "upbeat", "mainstream"],
        }
        
        detected_genre = "pop"
        detected_styles = []
        
        for genre, keywords in genres.items():
            if any(kw in prompt_lower for kw in keywords):
                detected_genre = genre
                detected_styles = keywords
                break
        
        return detected_genre, {
            "descriptors": detected_styles,
            "styles": [MusicalStyle[s.upper().replace("-", "_")] 
                      for s in detected_styles if hasattr(MusicalStyle, s.upper().replace("-", "_"))]
        }
    
    @staticmethod
    def _extract_emotions(prompt: str) -> Tuple[List[str], str]:
        """Extract emotional descriptors."""
        emotions = []
        prompt_lower = prompt.lower()
        
        # Check all emotion keywords
        for emotion in AdvancedIntentParser.EMOTION_MAPPING.keys():
            if emotion in prompt_lower:
                emotions.append(emotion)
        
        # Also check for direct descriptors not in mapping
        extra_emotions = [
            ("chill", "calm"),
            ("chilling", "calm"),
            ("studying", "calm"),
            ("focus", "calm"),
            ("tense", "dramatic"),
            ("awesome", "energetic"),
            ("awesome", "epic"),
            ("uplifting", "bright"),
            ("groovy", "energetic"),
            ("laid-back", "calm"),
        ]
        
        for keyword, emotion_replacement in extra_emotions:
            if keyword in prompt_lower and emotion_replacement not in emotions:
                emotions.append(emotion_replacement)
        
        # Determine dynamics
        dynamics = "moderate"
        if "intense" in prompt_lower or "dramatic" in prompt_lower:
            dynamics = "dramatic"
        elif "minimal" in prompt_lower or "subtle" in prompt_lower:
            dynamics = "minimal"
        
        return emotions or ["neutral"], dynamics
    
    @staticmethod
    def _determine_complexity(
        prompt: str,
        styles: Dict,
        duration_bars: int
    ) -> CompositionComplexity:
        """Determine appropriate complexity level."""
        prompt_lower = prompt.lower()
        
        # Check explicit complexity markers
        for style_kw, complexity in AdvancedIntentParser.STYLE_TO_COMPLEXITY.items():
            if style_kw in prompt_lower:
                return complexity
        
        # Infer from duration and style
        if duration_bars < 8:
            return CompositionComplexity.SIMPLE
        elif duration_bars < 32:
            return CompositionComplexity.MODERATE
        elif duration_bars < 64:
            return CompositionComplexity.RICH
        else:
            return CompositionComplexity.VERY_COMPLEX
    
    @staticmethod
    def _extract_instruments(prompt: str) -> Dict[str, int]:
        """Extract specific instrument requests with priority."""
        instruments = {}
        prompt_lower = prompt.lower()
        
        instrument_keywords = {
            "piano": ["piano", "keys"],
            "guitar": ["guitar"],
            "bass": ["bass"],
            "drums": ["drums", "percussion", "beat"],
            "strings": ["strings", "violin", "cello"],
            "saxophone": ["sax", "saxophone"],
            "trumpet": ["trumpet"],
            "flute": ["flute"],
            "synthesizer": ["synth", "synthesizer"],
            "pad": ["pad", "ambient pad"],
        }
        
        for instrument, keywords in instrument_keywords.items():
            for kw in keywords:
                if kw in prompt_lower:
                    instruments[instrument] = 5  # Default priority
        
        return instruments
    
    @staticmethod
    def _determine_energy(emotions: List[str], style_descriptors: List[str]) -> str:
        """Determine energy level from emotions and style."""
        high_energy_emotions = {"energetic", "epic", "dramatic"}
        low_energy_emotions = {"calm", "peaceful", "ambient", "melancholic"}
        
        emotion_set = set(emotions)
        
        if emotion_set & high_energy_emotions or "intense" in style_descriptors:
            return "high"
        elif emotion_set & low_energy_emotions:
            return "low"
        else:
            return "medium"
    
    @staticmethod
    def _build_composition_structure(
        duration_bars: int,
        complexity: CompositionComplexity,
        tempo: int,
        style_descriptors: List[str]
    ) -> CompositionStructure:
        """Build a composition structure based on all parameters."""
        structure = CompositionStructure(
            total_bars=duration_bars,
            tempo=tempo,
            complexity=complexity
        )
        
        # Determine intro density
        if "ambient" in style_descriptors or "minimalist" in style_descriptors:
            structure.intro_density = 0.2
        elif "epic" in style_descriptors or "cinematic" in style_descriptors:
            structure.intro_density = 0.5
        else:
            structure.intro_density = 0.3
        
        # Allocate bars to sections based on total duration
        if duration_bars <= 16:
            structure.intro_bars = 4
            structure.verse_bars = 4
            structure.chorus_bars = 4
            structure.outro_bars = 4
        elif duration_bars <= 32:
            structure.intro_bars = 4
            structure.verse_bars = 8
            structure.chorus_bars = 8
            structure.bridge_bars = 4
            structure.outro_bars = 4
        elif duration_bars <= 64:
            structure.intro_bars = 8
            structure.verse_bars = 12
            structure.chorus_bars = 12
            structure.bridge_bars = 16
            structure.outro_bars = 8
        else:
            # Longer pieces
            structure.intro_bars = 12
            structure.verse_bars = 16
            structure.chorus_bars = 16
            structure.bridge_bars = 16
            structure.outro_bars = int(duration_bars - 60)
        
        # Adjust energy arc based on style
        if "ambient" in style_descriptors:
            structure.energy_arc = "decay"
        elif "epic" in style_descriptors or "cinematic" in style_descriptors:
            structure.energy_arc = "build"
        else:
            structure.energy_arc = "dynamic"
        
        return structure
