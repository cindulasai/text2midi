# -*- coding: utf-8 -*-
"""
Emotion & Style-Aware Instrument Mapper
Intelligently selects instruments based on mood, emotion, and genre.
"""

from typing import List, Dict, Optional
from dataclasses import dataclass


@dataclass
class InstrumentProfile:
    """Profile of an instrument for specific emotions/styles."""
    name: str
    midi_program: int
    channel: int
    best_for_genres: List[str]
    best_for_emotions: List[str]
    best_for_styles: List[str]
    versatility: int  # 1-10, higher = works in more contexts
    priority: int  # 1-10, higher = prefer this


class EmotionAwareInstrumentMapper:
    """
    Maps user intent (emotions, styles, genres) to appropriate instruments.
    Creates diverse, emotion-aligned orchestrations.
    """

    # Comprehensive instrument database
    INSTRUMENTS = {
        # LEAD INSTRUMENTS
        "acoustic_guitar": InstrumentProfile(
            name="Acoustic Guitar",
            midi_program=24,
            channel=0,
            best_for_genres=["folk", "acoustic", "indie", "singer-songwriter"],
            best_for_emotions=["warm", "intimate", "nostalgic", "melancholic"],
            best_for_styles=["fingerpicking", "strumming", "minimalist"],
            versatility=8,
            priority=9
        ),
        "electric_guitar": InstrumentProfile(
            name="Electric Guitar",
            midi_program=29,
            channel=0,
            best_for_genres=["rock", "metal", "blues", "funk"],
            best_for_emotions=["energetic", "aggressive", "bold", "rebellious"],
            best_for_styles=["distorted", "lead", "rhythmic"],
            versatility=7,
            priority=8
        ),
        "piano": InstrumentProfile(
            name="Piano",
            midi_program=0,
            channel=0,
            best_for_genres=["classical", "jazz", "pop", "ballad"],
            best_for_emotions=["emotional", "sophisticated", "tender", "dramatic"],
            best_for_styles=["structured", "flowing", "expressive"],
            versatility=10,  # Most versatile
            priority=10
        ),
        "strings_ensemble": InstrumentProfile(
            name="Strings Ensemble",
            midi_program=48,
            channel=0,
            best_for_genres=["classical", "cinematic", "orchestral", "ambient"],
            best_for_emotions=["uplifting", "epic", "grand", "emotional"],
            best_for_styles=["lush", "flowing", "cinematic"],
            versatility=9,
            priority=9
        ),
        "violin": InstrumentProfile(
            name="Violin",
            midi_program=40,
            channel=0,
            best_for_genres=["classical", "jazz", "folk"],
            best_for_emotions=["soaring", "tender", "passionate"],
            best_for_styles=["melodic", "ornate", "expressive"],
            versatility=8,
            priority=8
        ),
        "flute": InstrumentProfile(
            name="Flute",
            midi_program=73,
            channel=0,
            best_for_genres=["classical", "folk", "ambient", "world"],
            best_for_emotions=["ethereal", "peaceful", "light", "whimsical"],
            best_for_styles=["flowing", "ornate", "minimal"],
            versatility=7,
            priority=8
        ),
        "trumpet": InstrumentProfile(
            name="Trumpet",
            midi_program=56,
            channel=0,
            best_for_genres=["jazz", "funk", "orchestral", "big band"],
            best_for_emotions=["bright", "energetic", "triumphant", "jubilant"],
            best_for_styles=["rhythmic", "bold", "call-and-response"],
            versatility=6,
            priority=7
        ),
        "saxophone": InstrumentProfile(
            name="Saxophone",
            midi_program=65,
            channel=0,
            best_for_genres=["jazz", "funk", "soul", "blues"],
            best_for_emotions=["sultry", "cool", "emotional", "expressive"],
            best_for_styles=["smooth", "ornate", "rhythmic"],
            versatility=8,
            priority=8
        ),
        "lead_synth": InstrumentProfile(
            name="Lead Synth",
            midi_program=80,
            channel=0,
            best_for_genres=["electronic", "ambient", "synth-pop", "industrial"],
            best_for_emotions=["futuristic", "mysterious", "energetic", "ethereal"],
            best_for_styles=["experimental", "rhythmic", "atmospheric"],
            versatility=9,
            priority=9
        ),
        "electric_bass": InstrumentProfile(
            name="Electric Bass",
            midi_program=33,
            channel=1,
            best_for_genres=["funk", "rock", "jazz", "electronic"],
            best_for_emotions=["energetic", "groovy", "solid", "driving"],
            best_for_styles=["funky", "rhythmic", "active"],
            versatility=8,
            priority=9
        ),
        "synth_bass": InstrumentProfile(
            name="Synth Bass",
            midi_program=38,
            channel=1,
            best_for_genres=["electronic", "funk", "synth-pop", "industrial"],
            best_for_emotions=["powerful", "modern", "energetic", "dark"],
            best_for_styles=["electronic", "rhythmic", "modern"],
            versatility=7,
            priority=8
        ),
        "pad_synth": InstrumentProfile(
            name="Pad Synth",
            midi_program=88,
            channel=2,
            best_for_genres=["ambient", "electronic", "cinematic", "new age"],
            best_for_emotions=["peaceful", "mysterious", "ethereal", "vast"],
            best_for_styles=["atmospheric", "minimal", "lush"],
            versatility=9,
            priority=8
        ),
        "arpeggio_synth": InstrumentProfile(
            name="Arpeggio Synth",
            midi_program=85,
            channel=1,
            best_for_genres=["electronic", "ambient", "progressive", "trance"],
            best_for_emotions=["hypnotic", "ethereal", "dreamy", "modern"],
            best_for_styles=["rhythmic", "electronic", "flowing"],
            versatility=8,
            priority=7
        ),
        "bells": InstrumentProfile(
            name="Bells/Glockenspiel",
            midi_program=9,
            channel=0,
            best_for_genres=["ambient", "classical", "world", "meditation"],
            best_for_emotions=["ethereal", "peaceful", "magical", "light"],
            best_for_styles=["sparse", "minimal", "tonal"],
            versatility=6,
            priority=7
        ),
        "harpsichord": InstrumentProfile(
            name="Harpsichord",
            midi_program=6,
            channel=0,
            best_for_genres=["baroque", "classical", "world"],
            best_for_emotions=["historical", "ornate", "formal"],
            best_for_styles=["ornate", "structured", "classical"],
            versatility=4,
            priority=6
        ),
        "ocarina": InstrumentProfile(
            name="Ocarina",
            midi_program=79,
            channel=0,
            best_for_genres=["world", "ambient", "folk"],
            best_for_emotions=["whimsical", "mysterious", "nostalgic"],
            best_for_styles=["minimal", "organic", "world"],
            versatility=5,
            priority=6
        ),
    }

    @classmethod
    def select_instruments_for_intent(
        cls,
        genre: str,
        emotions: List[str],
        style_descriptors: List[str],
        track_count: int = 4,
        specific_instruments: List[str] = None
    ) -> List[Dict]:
        """
        Select instruments based on comprehensive understanding of user intent.
        
        Returns:
            List of instrument configs with track type and priority
        """
        if specific_instruments:
            # User explicitly requested instruments
            selected = []
            for inst_name in specific_instruments:
                inst = cls._find_instrument(inst_name)
                if inst:
                    selected.append({
                        "instrument": inst_name,
                        "track_type": cls._infer_track_type(inst_name),
                        "midi_program": inst.midi_program,
                        "channel": inst.channel,
                        "priority": inst.priority
                    })
            return selected[:track_count]
        
        # Automatic selection based on emotion/genre/style
        candidates = cls._find_best_instruments(genre, emotions, style_descriptors)
        
        # Select top instruments for lead, harmony, bass, etc.
        selected = []
        used_names = set()
        
        # Priority order
        track_types_needed = ["lead", "harmony", "bass"]
        if track_count >= 4:
            track_types_needed.insert(2, "arpeggio")
        
        for track_type in track_types_needed:
            if len(selected) >= track_count:
                break
            
            # Find best instrument for this track type
            for inst_name, score in candidates:
                if inst_name in used_names:
                    continue
                
                inst = cls.INSTRUMENTS[inst_name]
                if cls._is_suitable_for_track_type(track_type, inst):
                    selected.append({
                        "instrument": inst_name,
                        "track_type": track_type,
                        "midi_program": inst.midi_program,
                        "channel": inst.channel,
                        "priority": inst.priority,
                        "score": score
                    })
                    used_names.add(inst_name)
                    break
        
        # Fill remaining slots with any suitable instruments
        for inst_name, score in candidates:
            if len(selected) >= track_count:
                break
            if inst_name not in used_names:
                selected.append({
                    "instrument": inst_name,
                    "track_type": "harmony",
                    "midi_program": cls.INSTRUMENTS[inst_name].midi_program,
                    "channel": cls.INSTRUMENTS[inst_name].channel,
                    "priority": cls.INSTRUMENTS[inst_name].priority,
                    "score": score
                })
                used_names.add(inst_name)
        
        return selected

    @classmethod
    def _find_best_instruments(
        cls,
        genre: str,
        emotions: List[str],
        style_descriptors: List[str]
    ) -> List[tuple]:
        """
        Score all instruments based on how well they match the intent.
        Returns sorted list of (instrument_name, score) tuples.
        """
        scores = {}
        
        for inst_name, inst in cls.INSTRUMENTS.items():
            score = 0
            
            # Genre matching
            if genre in inst.best_for_genres:
                score += 30
            elif any(g in inst.best_for_genres for g in [genre.lower(), genre.split()[0].lower()]):
                score += 20
            
            # Emotion matching
            matching_emotions = sum(1 for e in emotions if e in inst.best_for_emotions)
            score += matching_emotions * 20
            
            # Style matching
            matching_styles = sum(1 for s in style_descriptors if s in inst.best_for_styles)
            score += matching_styles * 15
            
            # Versatility bonus
            score += inst.versatility * 2
            
            # Priority bonus
            score += inst.priority
            
            scores[inst_name] = score
        
        # Return sorted by score (descending)
        return sorted(scores.items(), key=lambda x: x[1], reverse=True)

    @classmethod
    def _find_instrument(cls, name: str) -> Optional[InstrumentProfile]:
        """Find instrument by name (case-insensitive)."""
        name_lower = name.lower().replace(" ", "_")
        
        for key, inst in cls.INSTRUMENTS.items():
            if key == name_lower or inst.name.lower() == name_lower:
                return inst
        
        return None

    @classmethod
    def _infer_track_type(cls, instrument_name: str) -> str:
        """Infer track type from instrument."""
        if any(x in instrument_name.lower() for x in ["bass", "low"]):
            return "bass"
        elif any(x in instrument_name.lower() for x in ["pad", "synth", "strings", "ensemble"]):
            return "harmony"
        elif any(x in instrument_name.lower() for x in ["arpeggio", "arp"]):
            return "arpeggio"
        else:
            return "lead"

    @classmethod
    def _is_suitable_for_track_type(cls, track_type: str, instrument: InstrumentProfile) -> bool:
        """Check if instrument is suitable for track type."""
        if track_type == "bass":
            return "bass" in instrument.name.lower() or instrument.midi_program in [33, 38]
        elif track_type == "harmony":
            return any(x in instrument.name.lower() for x in ["pad", "strings", "ensemble", "synth"])
        elif track_type == "arpeggio":
            return "synth" in instrument.name.lower()
        elif track_type == "lead":
            return "pad" not in instrument.name.lower()
        return True
