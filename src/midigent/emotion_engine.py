# -*- coding: utf-8 -*-
"""
Emotion Engine: Sophisticated emotion detection and generation
Maps user intent to rich emotional and musical parameters.
USP Feature #1: Emotional depth and authenticity
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Optional
import math


class EmotionType(Enum):
    """Recognized emotions in music."""
    JOY = "joy"
    SADNESS = "sadness"
    CALMNESS = "calmness"
    ENERGY = "energy"
    MYSTERY = "mystery"
    TENSION = "tension"
    TRIUMPH = "triumph"
    NOSTALGIA = "nostalgia"
    ANXIETY = "anxiety"
    PEACE = "peace"
    MELANCHOLY = "melancholy"
    EUPHORIA = "euphoria"


@dataclass
class EmotionalProfile:
    """Rich emotional profile for a composition."""
    primary_emotion: EmotionType
    secondary_emotions: List[EmotionType] = field(default_factory=list)
    emotional_arc: str = "steady"  # "build", "decay", "wave", "steady"
    intensity: float = 0.5  # 0-1
    openness: float = 0.5  # 0-1, how open vs introspective
    complexity_emotional: float = 0.5  # 0-1, emotional sophistication
    instrumentation_suggestion: List[str] = field(default_factory=list)
    harmonic_approach: str = "functional"  # functional, modal, atonal, etc.
    
    def describe(self) -> str:
        """Generate human-readable emotional description."""
        main = self.primary_emotion.value.capitalize()
        secondary = ", ".join([e.value for e in self.secondary_emotions]) if self.secondary_emotions else "none"
        intensity_desc = ["delicate", "subtle", "moderate", "strong", "intense"][int(self.intensity * 4)]
        arc_desc = {
            "build": "building intensity",
            "decay": "waning intensity",
            "wave": "dynamic fluctuation",
            "steady": "steady presence"
        }.get(self.emotional_arc, self.emotional_arc)
        
        return f"{main} ({intensity_desc}, {secondary}) with {arc_desc}"


class EmotionEngine:
    """
    Sophisticated emotion detection and generation engine.
    Maps text descriptions to rich emotional and musical parameters.
    """
    
    # Emotion keyword mappings
    EMOTION_KEYWORDS = {
        EmotionType.JOY: [
            "happy", "joyful", "cheerful", "bright", "uplifting", "celebratory",
            "festive", "playful", "gleeful", "exuberant", "delightful"
        ],
        EmotionType.SADNESS: [
            "sad", "sorrowful", "gloomy", "melancholic", "mournful", "doleful",
            "forlorn", "despondent", "heartbroken", "tearful", "wistful"
        ],
        EmotionType.CALMNESS: [
            "calm", "peaceful", "serene", "tranquil", "meditative", "relaxing",
            "soothing", "gentle", "quiet", "still", "restful"
        ],
        EmotionType.ENERGY: [
            "energetic", "vigorous", "dynamic", "powerful", "intense", "driving",
            "propulsive", "forceful", "aggressive", "explosive"
        ],
        EmotionType.MYSTERY: [
            "mysterious", "enigmatic", "cryptic", "secretive", "hidden", "unclear",
            "ambiguous", "puzzling", "intriguing", "suspicious"
        ],
        EmotionType.TENSION: [
            "tense", "anxious", "suspenseful", "uneasy", "unsettling", "ominous",
            "ominous", "dramatic", "thrilling", "nerve-wracking"
        ],
        EmotionType.TRIUMPH: [
            "triumphant", "victorious", "heroic", "majestic", "grandiose", "epic",
            "conquering", "glorious", "magnificent", "dominant"
        ],
        EmotionType.NOSTALGIA: [
            "nostalgic", "bittersweet", "wistful", "retro", "vintage", "memory",
            "reminiscent", "longing", "sentimental", "throwback"
        ],
        EmotionType.ANXIETY: [
            "anxious", "nervous", "worried", "panicked", "frantic", "stressed",
            "agitated", "restless", "unsettled", "jittery"
        ],
        EmotionType.PEACE: [
            "peaceful", "harmonious", "balanced", "integrated", "whole", "complete",
            "at ease", "content", "satisfied", "fulfilled"
        ],
        EmotionType.MELANCHOLY: [
            "melancholy", "introspective", "pensive", "contemplative", "thoughtful",
            "reflective", "somber", "dark", "brooding"
        ],
        EmotionType.EUPHORIA: [
            "euphoric", "blissful", "transcendent", "ecstatic", "rapturous", "divine",
            "heavenly", "exalted", "sublime"
        ]
    }
    
    # Emotional characteristics per emotion
    EMOTION_CHARACTERISTICS = {
        EmotionType.JOY: {
            "tempo_multiplier": 1.3,
            "mode": "major",
            "key_brightness": "bright",
            "orchestration": "full, bright",
            "rhythm_regularity": 0.8,
            "dissonance_tolerance": 0.2,
            "suggested_instruments": ["trumpet", "flute", "bells", "violin", "piano"]
        },
        EmotionType.SADNESS: {
            "tempo_multiplier": 0.6,
            "mode": "minor",
            "key_brightness": "dark",
            "orchestration": "sparse, mournful",
            "rhythm_regularity": 0.5,
            "dissonance_tolerance": 0.6,
            "suggested_instruments": ["cello", "french horn", "oboe", "violin", "piano"]
        },
        EmotionType.CALMNESS: {
            "tempo_multiplier": 0.5,
            "mode": "major",
            "key_brightness": "neutral",
            "orchestration": "sparse, gentle",
            "rhythm_regularity": 0.9,
            "dissonance_tolerance": 0.1,
            "suggested_instruments": ["pad", "strings", "flute", "harp", "bells"]
        },
        EmotionType.ENERGY: {
            "tempo_multiplier": 1.5,
            "mode": "major",
            "key_brightness": "bright",
            "orchestration": "full, dense",
            "rhythm_regularity": 0.7,
            "dissonance_tolerance": 0.5,
            "suggested_instruments": ["drums", "guitar", "synth", "trumpet", "bass"]
        },
        EmotionType.MYSTERY: {
            "tempo_multiplier": 0.8,
            "mode": "minor",
            "key_brightness": "dark",
            "orchestration": "sparse, atmospheric",
            "rhythm_regularity": 0.4,
            "dissonance_tolerance": 0.7,
            "suggested_instruments": ["string pad", "pizzicato strings", "synth", "harp", "wind"]
        },
        EmotionType.TENSION: {
            "tempo_multiplier": 1.2,
            "mode": "minor",
            "key_brightness": "dark",
            "orchestration": "dramatic, layered",
            "rhythm_regularity": 0.6,
            "dissonance_tolerance": 0.8,
            "suggested_instruments": ["timpani", "strings", "horn", "synth bass", "orchestra"]
        },
        EmotionType.TRIUMPH: {
            "tempo_multiplier": 1.2,
            "mode": "major",
            "key_brightness": "bright",
            "orchestration": "full, grand",
            "rhythm_regularity": 0.8,
            "dissonance_tolerance": 0.3,
            "suggested_instruments": ["trumpet", "trombone", "timpani", "full orchestra", "organ"]
        },
        EmotionType.NOSTALGIA: {
            "tempo_multiplier": 0.75,
            "mode": "major",
            "key_brightness": "warm",
            "orchestration": "vintage, organic",
            "rhythm_regularity": 0.7,
            "dissonance_tolerance": 0.4,
            "suggested_instruments": ["piano", "strings", "guitar", "horn", "woodwinds"]
        },
        EmotionType.ANXIETY: {
            "tempo_multiplier": 1.4,
            "mode": "minor",
            "key_brightness": "dark",
            "orchestration": "active, unsettling",
            "rhythm_regularity": 0.3,
            "dissonance_tolerance": 0.8,
            "suggested_instruments": ["strings", "synth", "timpani", "bass", "percussion"]
        },
        EmotionType.PEACE: {
            "tempo_multiplier": 0.4,
            "mode": "major",
            "key_brightness": "neutral",
            "orchestration": "open, breathing",
            "rhythm_regularity": 0.9,
            "dissonance_tolerance": 0.05,
            "suggested_instruments": ["pad", "harp", "piano", "flute", "strings"]
        },
        EmotionType.MELANCHOLY: {
            "tempo_multiplier": 0.7,
            "mode": "minor",
            "key_brightness": "neutral",
            "orchestration": "introspective, sparse",
            "rhythm_regularity": 0.6,
            "dissonance_tolerance": 0.5,
            "suggested_instruments": ["piano", "cello", "guitar", "voice", "oboe"]
        },
        EmotionType.EUPHORIA: {
            "tempo_multiplier": 1.4,
            "mode": "major",
            "key_brightness": "bright",
            "orchestration": "ecstatic, layered",
            "rhythm_regularity": 0.8,
            "dissonance_tolerance": 0.3,
            "suggested_instruments": ["synth", "pad", "strings", "bells", "uplifting sounds"]
        }
    }
    
    @staticmethod
    def detect_emotion_from_text(text: str) -> EmotionalProfile:
        """
        Detect predominant emotion(s) from text description.
        Analyzes keyword presence and intensity indicators.
        """
        text_lower = text.lower()
        emotion_scores: Dict[EmotionType, int] = {e: 0 for e in EmotionType}
        
        # Score each emotion based on keyword matches
        for emotion, keywords in EmotionEngine.EMOTION_KEYWORDS.items():
            for keyword in keywords:
                if keyword in text_lower:
                    emotion_scores[emotion] += 1
        
        # Find primary and secondary emotions
        sorted_emotions = sorted(emotion_scores.items(), key=lambda x: x[1], reverse=True)
        primary = sorted_emotions[0][0] if sorted_emotions[0][1] > 0 else EmotionType.CALMNESS
        
        secondary = []
        for emotion, score in sorted_emotions[1:3]:
            if score > 0:
                secondary.append(emotion)
        
        # Determine intensity
        intensity = min(1.0, (sorted_emotions[0][1] + sum(s for _, s in sorted_emotions[1:3])) / 10.0)
        
        # Determine emotional arc
        emotional_arc = "steady"
        if "build" in text_lower or "growing" in text_lower:
            emotional_arc = "build"
        elif "fade" in text_lower or "decay" in text_lower:
            emotional_arc = "decay"
        elif "dynamic" in text_lower or "fluctuat" in text_lower:
            emotional_arc = "wave"
        
        # Openness: introspective vs expansive
        openness = 0.5
        if any(w in text_lower for w in ["open", "expansive", "grand", "full"]):
            openness = 0.8
        elif any(w in text_lower for w in ["intimate", "private", "introspect", "personal"]):
            openness = 0.2
        
        # Get instrumentation suggestions
        chars = EmotionEngine.EMOTION_CHARACTERISTICS.get(primary, {})
        instruments = chars.get("suggested_instruments", [])
        
        return EmotionalProfile(
            primary_emotion=primary,
            secondary_emotions=secondary,
            emotional_arc=emotional_arc,
            intensity=intensity,
            openness=openness,
            complexity_emotional=intensity * 0.7,
            instrumentation_suggestion=instruments[:3],
            harmonic_approach=chars.get("mode", "functional")
        )
    
    @staticmethod
    def get_harmonic_parameters(emotion: EmotionalProfile) -> Dict:
        """Get harmonic/musical parameters for an emotional profile."""
        chars = EmotionEngine.EMOTION_CHARACTERISTICS.get(emotion.primary_emotion, {})
        
        return {
            "tempo_multiplier": chars.get("tempo_multiplier", 1.0),
            "mode": chars.get("mode", "major"),
            "key_brightness": chars.get("key_brightness", "neutral"),
            "rhythm_regularity": chars.get("rhythm_regularity", 0.5),
            "dissonance_tolerance": chars.get("dissonance_tolerance", 0.5),
            "suggested_instruments": chars.get("suggested_instruments", []),
            "orchestration": chars.get("orchestration", "balanced")
        }
    
    @staticmethod
    def calculate_emotional_coherence(
        emotional_profile: EmotionalProfile,
        tempo: int,
        scale_mode: str,
        instruments: List[str]
    ) -> Dict:
        """Calculate how well the composition matches emotional intent."""
        score = 1.0
        issues = []
        strengths = []
        
        chars = EmotionEngine.EMOTION_CHARACTERISTICS.get(emotional_profile.primary_emotion, {})
        
        # Check tempo alignment
        ideal_tempo = int(120 * chars.get("tempo_multiplier", 1.0))
        tempo_diff = abs(tempo - ideal_tempo) / ideal_tempo
        if tempo_diff > 0.3:
            score -= 0.15
            issues.append(f"Tempo {tempo} BPM differs from emotional ideal {ideal_tempo} BPM")
        else:
            strengths.append(f"Tempo {tempo} BPM aligns with {emotional_profile.primary_emotion.value}")
        
        # Check mode alignment
        ideal_mode = chars.get("mode", "major")
        if scale_mode.lower() == ideal_mode.lower():
            strengths.append(f"Scale mode matches emotional character")
        else:
            score -= 0.1
            issues.append(f"Scale mode {scale_mode} may not suit {emotional_profile.primary_emotion.value}")
        
        # Check instrumentation alignment
        suggested = set(chars.get("suggested_instruments", []))
        actual = set([i.lower() for i in instruments])
        overlap = len(suggested & actual)
        if overlap > 0:
            strengths.append(f"Instrumentation includes {overlap} emotionally appropriate choices")
        
        score = max(0.4, min(1.0, score))
        
        return {
            "coherence_score": score,
            "strengths": strengths,
            "issues": issues
        }
