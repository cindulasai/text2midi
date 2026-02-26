# -*- coding: utf-8 -*-
"""
Advanced Music Generator with Prompt Awareness
Generates diverse, genre-specific, emotion-aware musical content.
"""

import random
import math
from typing import List, Dict, Optional, Tuple
from enum import Enum
from src.app.models import Note
from src.app.constants import SCALES, CHORD_PROGRESSIONS, DRUM_MAP


class MusicPhrase(Enum):
    """Musical phrase patterns."""
    ASCENDING = "ascending"
    DESCENDING = "descending"
    ARCH = "arch"  # Up then down
    VALLEY = "valley"  # Down then up
    REPETITIVE = "repetitive"
    WANDERING = "wandering"
    CALL_RESPONSE = "call_response"


class GenerationStyle(Enum):
    """Generation style based on user intent."""
    MINIMAL = "minimal"
    FLOWING = "flowing"
    RHYTHMIC = "rhythmic"
    CHAOTIC = "chaotic"
    STRUCTURED = "structured"
    ORGANIC = "organic"


class AdvancedMusicGenerator:
    """
    Generates diverse musical content with deep prompt awareness.
    Creates different patterns for different emotions, styles, and genres.
    """

    def __init__(self, session_id: str = "default"):
        """Initialize with session ID for reproducibility."""
        self.session_id = session_id
        self.call_counter = 0

    def generate_aware_melody(
        self,
        root: int,
        mode: str,
        bars: int,
        energy: str,
        genre: str,
        style_descriptors: List[str] = None,
        emotions: List[str] = None,
        complexity: str = "moderate"
    ) -> List[Note]:
        """Generate melody that's aware of style and emotions."""
        style_descriptors = style_descriptors or []
        emotions = emotions or []
        
        # Determine generation strategy
        strategy = self._determine_strategy(genre, style_descriptors, emotions, energy)
        
        if strategy == GenerationStyle.MINIMAL:
            return self._generate_minimal_melody(root, mode, bars, energy)
        elif strategy == GenerationStyle.FLOWING:
            return self._generate_flowing_melody(root, mode, bars, energy)
        elif strategy == GenerationStyle.RHYTHMIC:
            return self._generate_rhythmic_melody(root, mode, bars, energy, genre)
        elif strategy == GenerationStyle.CHAOTIC:
            return self._generate_chaotic_melody(root, mode, bars, energy)
        elif strategy == GenerationStyle.STRUCTURED:
            return self._generate_structured_melody(root, mode, bars, energy, genre)
        else:  # ORGANIC
            return self._generate_organic_melody(root, mode, bars, energy)

    def generate_smart_bass(
        self,
        root: int,
        genre: str,
        bars: int,
        energy: str,
        style_descriptors: List[str] = None
    ) -> List[Note]:
        """Generate bass line that responds to genre and energy."""
        style_descriptors = style_descriptors or []
        progression = CHORD_PROGRESSIONS.get(genre, CHORD_PROGRESSIONS["pop"])
        beats_per_chord = 4
        total_beats = bars * 4
        notes = []
        beat = 0.0
        chord_idx = 0

        # Determine bass style
        if "funky" in style_descriptors + [genre] or genre == "funk":
            return self._generate_funky_bass(root, progression, bars, beats_per_chord)
        elif genre == "ambient" or "peaceful" in style_descriptors:
            return self._generate_ambient_bass(root, progression, bars, beats_per_chord)
        elif genre == "jazz":
            return self._generate_walking_bass(root, progression, bars)
        elif genre in ["rock", "metal"]:
            return self._generate_power_bass(root, progression, bars, beats_per_chord, energy)
        elif genre == "electronic":
            return self._generate_synth_bass(root, progression, bars, beats_per_chord, energy)
        else:
            return self._generate_standard_bass(root, progression, bars, beats_per_chord, energy)

    def generate_smart_drums(
        self,
        genre: str,
        bars: int,
        energy: str,
        style_descriptors: List[str] = None,
        emotions: List[str] = None
    ) -> List[Note]:
        """Generate drum pattern with deep genre and emotion awareness."""
        style_descriptors = style_descriptors or []
        emotions = emotions or []
        
        # Vary drum patterns based on style
        if "minimal" in style_descriptors or genre == "ambient":
            return self._generate_minimal_drums(genre, bars, energy)
        elif "jazzy" in style_descriptors or genre == "jazz":
            return self._generate_jazz_drums(bars)
        elif "hip hop" in style_descriptors + [genre] or genre == "lofi":
            return self._generate_hiphop_drums(bars, energy)
        elif "progressive" in style_descriptors or genre in ["progressive", "metal"]:
            return self._generate_progressive_drums(genre, bars, energy)
        elif "uplifting" in emotions or "epic" in style_descriptors:
            return self._generate_epic_drums(bars, energy)
        else:
            return self._generate_standard_drums(genre, bars, energy)

    def generate_smart_pad(
        self,
        root: int,
        mode: str,
        bars: int,
        style_descriptors: List[str] = None,
        emotions: List[str] = None
    ) -> List[Note]:
        """Generate pad with emotion awareness."""
        style_descriptors = style_descriptors or []
        emotions = emotions or []
        notes = []
        scale = SCALES.get(mode, SCALES["major"])
        total_beats = bars * 4
        
        if "minimal" in style_descriptors:
            # Single sustained note
            notes.append(Note(
                pitch=root,
                start_time=0,
                duration=total_beats - 0.5,
                velocity=35,
                channel=3
            ))
        elif "dark" in emotions or "melancholic" in emotions:
            # Dark, minor pad
            for degree in [0, 3, 7]:  # Minor intervals
                pitch = root + scale[degree % len(scale)] - 12
                notes.append(Note(
                    pitch=pitch,
                    start_time=0,
                    duration=total_beats - 0.5,
                    velocity=random.randint(30, 50),
                    channel=3
                ))
        elif "bright" in emotions or "happy" in emotions:
            # Bright, major pad
            for degree in [0, 2, 4, 7]:  # Major intervals
                pitch = root + scale[degree % len(scale)]
                notes.append(Note(
                    pitch=pitch,
                    start_time=0,
                    duration=total_beats - 0.5,
                    velocity=random.randint(40, 60),
                    channel=3
                ))
        else:
            # Standard pad: generate evolving chord blocks across the full piece
            # so that even long/sparse ambient pieces have enough notes
            bars_per_block = max(4, bars // max(2, bars // 8))
            block_beats = bars_per_block * 4
            num_blocks = max(2, math.ceil(total_beats / block_beats))
            chord_rotation = [
                [0, 2, 4],   # I
                [2, 4, 6],   # ii
                [4, 6, 8],   # IV
                [0, 2, 4],   # I
            ]
            for block_idx in range(num_blocks):
                start = block_idx * block_beats
                if start >= total_beats:
                    break
                duration = min(block_beats - 0.5, total_beats - start - 0.5)
                degrees = chord_rotation[block_idx % len(chord_rotation)]
                for degree in degrees:
                    pitch = root + scale[degree % len(scale)] - 12
                    notes.append(Note(
                        pitch=max(0, min(127, pitch)),
                        start_time=start,
                        duration=duration,
                        velocity=random.randint(38, 58),
                        channel=3
                    ))

        return notes

    # ===== INTERNAL MELODY STRATEGIES =====

    def _determine_strategy(
        self,
        genre: str,
        style_descriptors: List[str],
        emotions: List[str],
        energy: str
    ) -> GenerationStyle:
        """Determine which melody generation strategy to use."""
        # Check for specific indicators
        if "ambient" in style_descriptors + [genre] or "peaceful" in emotions:
            return GenerationStyle.MINIMAL
        if "chaotic" in style_descriptors or genre in ["metal", "industrial"]:
            return GenerationStyle.CHAOTIC
        if "rhythmic" in style_descriptors or genre in ["funk", "electronic"]:
            return GenerationStyle.RHYTHMIC
        if genre in ["jazz", "classical"]:
            return GenerationStyle.ORGANIC
        if energy == "high" and genre not in ["ambient", "lofi"]:
            return GenerationStyle.FLOWING
        if "structured" in style_descriptors or genre == "classical":
            return GenerationStyle.STRUCTURED
        
        return GenerationStyle.ORGANIC

    def _generate_minimal_melody(self, root: int, mode: str, bars: int, energy: str) -> List[Note]:
        """Generate sparse, minimal melody."""
        notes = []
        scale = SCALES.get(mode, SCALES["major"])
        beats = bars * 4
        
        beat = 0.0
        while beat < beats:
            # Very sparse: 20% chance of a note
            if random.random() < 0.2:
                scale_degree = random.choice(scale)
                pitch = root + scale_degree
                duration = random.choice([2.0, 4.0, 8.0])
                velocity = random.randint(40, 60)
                notes.append(Note(pitch=pitch, start_time=beat, duration=duration, velocity=velocity))
                beat += duration
            else:
                beat += 2.0
        
        return notes

    def _generate_flowing_melody(self, root: int, mode: str, bars: int, energy: str) -> List[Note]:
        """Generate smooth, flowing melody with connected phrases."""
        notes = []
        scale = SCALES.get(mode, SCALES["major"])
        beats = bars * 4
        beat = 0.0
        
        # Create phrases with direction (ascending/descending/arch)
        while beat < beats:
            phrase_length = random.choice([4, 8])
            phrase_type = random.choice([
                MusicPhrase.ASCENDING,
                MusicPhrase.DESCENDING,
                MusicPhrase.ARCH
            ])
            
            phrase_notes = self._create_directional_phrase(
                root, scale, phrase_type, phrase_length
            )
            
            for note in phrase_notes:
                if beat + note.start_time < beats:
                    note.start_time += beat
                    notes.append(note)
            
            beat += phrase_length
        
        return notes

    def _generate_rhythmic_melody(self, root: int, mode: str, bars: int, energy: str, genre: str) -> List[Note]:
        """Generate melody with strong rhythmic patterns."""
        notes = []
        scale = SCALES.get(mode, SCALES["major"])
        beats = bars * 4
        
        # Use repeating rhythm patterns
        rhythm_patterns = [
            [0.5, 0.5, 1.0],  # Short-short-long
            [1.0, 1.0, 2.0],  # Long pattern
            [0.25, 0.25, 0.25, 0.25],  # Fast
        ]
        
        beat = 0.0
        pattern_idx = 0
        while beat < beats:
            pattern = rhythm_patterns[pattern_idx % len(rhythm_patterns)]
            
            for duration in pattern:
                if beat < beats:
                    scale_degree = random.choice(scale)
                    pitch = root + scale_degree + random.choice([-12, 0, 12])
                    velocity = random.randint(65, 100)
                    notes.append(Note(
                        pitch=pitch,
                        start_time=beat,
                        duration=duration,
                        velocity=velocity
                    ))
                    beat += duration
            
            pattern_idx += 1
        
        return notes

    def _generate_chaotic_melody(self, root: int, mode: str, bars: int, energy: str) -> List[Note]:
        """Generate unpredictable, chaotic melody."""
        notes = []
        scale = SCALES.get(mode, SCALES["major"])
        beats = bars * 4
        
        beat = 0.0
        while beat < beats:
            # Random octave jumps and erratic rhythms
            scale_degree = random.choice(scale)
            octave = random.choice([-24, -12, 0, 12, 24])
            pitch = root + scale_degree + octave
            duration = random.choice([0.125, 0.25, 0.5, 2.0, 3.0])
            velocity = random.randint(30, 110)
            
            notes.append(Note(
                pitch=pitch,
                start_time=beat,
                duration=duration,
                velocity=velocity
            ))
            beat += duration
        
        return notes

    def _generate_structured_melody(self, root: int, mode: str, bars: int, energy: str, genre: str) -> List[Note]:
        """Generate classical, highly structured melody."""
        notes = []
        scale = SCALES.get(mode, SCALES["major"])
        beats = bars * 4
        
        # Create 8-bar phrases with clear structure
        phrase_length = 8
        beat = 0.0
        
        while beat < beats:
            # First half: ascending, second half: descending (or vice versa)
            if int(beat / phrase_length) % 2 == 0:
                # Ascending
                for i in range(8):
                    if beat < beats:
                        scale_degree = i % len(scale)
                        pitch = root + scale[scale_degree]
                        notes.append(Note(
                            pitch=pitch,
                            start_time=beat,
                            duration=1.0,
                            velocity=75
                        ))
                        beat += 1.0
            else:
                # Descending
                for i in range(7, -1, -1):
                    if beat < beats:
                        scale_degree = i % len(scale)
                        pitch = root + scale[scale_degree]
                        notes.append(Note(
                            pitch=pitch,
                            start_time=beat,
                            duration=1.0,
                            velocity=75
                        ))
                        beat += 1.0
        
        return notes

    def _generate_organic_melody(self, root: int, mode: str, bars: int, energy: str) -> List[Note]:
        """Generate natural, organic melody with variation."""
        notes = []
        scale = SCALES.get(mode, SCALES["major"])
        beats = bars * 4
        
        beat = 0.0
        last_pitch = root
        
        while beat < beats:
            # Choose nearby scale degrees (within 2-3 steps)
            current_scale_idx = (last_pitch - root) % len(scale)
            nearby_degrees = [
                scale[(current_scale_idx - 2) % len(scale)],
                scale[(current_scale_idx - 1) % len(scale)],
                scale[current_scale_idx],
                scale[(current_scale_idx + 1) % len(scale)],
                scale[(current_scale_idx + 2) % len(scale)],
            ]
            
            scale_degree = random.choice(nearby_degrees)
            pitch = root + scale_degree + random.choice([-12, 0, 12]) * random.choice([0, 1])
            
            # Vary duration based on energy
            if energy == "low":
                duration = random.choice([1.0, 1.5, 2.0])
            elif energy == "high":
                duration = random.choice([0.25, 0.5, 0.75])
            else:
                duration = random.choice([0.5, 1.0, 1.5])
            
            velocity = random.randint(60, 90)
            notes.append(Note(pitch=pitch, start_time=beat, duration=duration, velocity=velocity))
            last_pitch = pitch
            beat += duration
        
        return notes

    # ===== INTERNAL BASS STRATEGIES =====

    def _generate_funky_bass(self, root: int, progression, bars: int, beats_per_chord: int) -> List[Note]:
        """Generate syncopated funky bass."""
        notes = []
        beat = 0.0
        chord_idx = 0
        
        for bar in range(bars):
            chord = progression[chord_idx % len(progression)]
            bass_note = root + chord[0] - 24
            
            # Funky syncopated pattern
            syncopated_times = [0, 0.5, 1.5, 2.0, 2.5, 3.0, 3.5]
            for t in syncopated_times:
                vel = 100 if t % 1 == 0 else 70
                notes.append(Note(
                    pitch=bass_note,
                    start_time=beat + t,
                    duration=0.4,
                    velocity=vel,
                    channel=2
                ))
            
            beat += beats_per_chord
            chord_idx += 1
        
        return notes

    def _generate_ambient_bass(self, root: int, progression, bars: int, beats_per_chord: int) -> List[Note]:
        """Generate sustained, minimal bass."""
        notes = []
        beat = 0.0
        chord_idx = 0
        
        for bar in range(bars):
            chord = progression[chord_idx % len(progression)]
            bass_note = root + chord[0] - 24
            
            notes.append(Note(
                pitch=bass_note,
                start_time=beat,
                duration=beats_per_chord - 0.5,
                velocity=55,
                channel=2
            ))
            
            beat += beats_per_chord
            chord_idx += 1
        
        return notes

    def _generate_walking_bass(self, root: int, progression, bars: int) -> List[Note]:
        """Generate jazz walking bass."""
        notes = []
        beat = 0.0
        chord_idx = 0
        
        for bar in range(bars):
            chord = progression[chord_idx % len(progression)]
            
            for i in range(4):
                walk_note = root + chord[i % len(chord)] - 24
                notes.append(Note(
                    pitch=walk_note,
                    start_time=beat + i,
                    duration=0.9,
                    velocity=75,
                    channel=2
                ))
            
            beat += 4
            chord_idx += 1
        
        return notes

    def _generate_power_bass(self, root: int, progression, bars: int, beats_per_chord: int, energy: str) -> List[Note]:
        """Generate power-driven bass for rock."""
        notes = []
        beat = 0.0
        chord_idx = 0
        
        for bar in range(bars):
            chord = progression[chord_idx % len(progression)]
            bass_note = root + chord[0] - 24
            
            # Power pattern: down-up with strong accent
            num_notes = 8 if energy == "high" else 4
            for i in range(num_notes):
                vel = 105 if i % 2 == 0 else 75
                notes.append(Note(
                    pitch=bass_note,
                    start_time=beat + i * 0.5,
                    duration=0.4,
                    velocity=vel,
                    channel=2
                ))
            
            beat += beats_per_chord
            chord_idx += 1
        
        return notes

    def _generate_synth_bass(self, root: int, progression, bars: int, beats_per_chord: int, energy: str) -> List[Note]:
        """Generate synth bass for electronic."""
        notes = []
        beat = 0.0
        chord_idx = 0
        
        for bar in range(bars):
            chord = progression[chord_idx % len(progression)]
            bass_notes = [root + chord[0] - 24, root + chord[0] - 12]
            
            if energy == "high":
                for t in [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5]:
                    pitch = bass_notes[int(t) % len(bass_notes)]
                    notes.append(Note(
                        pitch=pitch,
                        start_time=beat + t,
                        duration=0.4,
                        velocity=random.randint(80, 100),
                        channel=2
                    ))
            else:
                notes.append(Note(
                    pitch=bass_notes[0],
                    start_time=beat,
                    duration=beats_per_chord - 0.5,
                    velocity=75,
                    channel=2
                ))
            
            beat += beats_per_chord
            chord_idx += 1
        
        return notes

    def _generate_standard_bass(self, root: int, progression, bars: int, beats_per_chord: int, energy: str) -> List[Note]:
        """Generate standard bass line."""
        notes = []
        beat = 0.0
        chord_idx = 0
        
        for bar in range(bars):
            chord = progression[chord_idx % len(progression)]
            bass_note = root + chord[0] - 24
            
            for i in range(4):
                notes.append(Note(
                    pitch=bass_note,
                    start_time=beat + i,
                    duration=0.9,
                    velocity=80,
                    channel=2
                ))
            
            beat += beats_per_chord
            chord_idx += 1
        
        return notes

    # ===== INTERNAL DRUMS STRATEGIES =====

    def _generate_minimal_drums(self, genre: str, bars: int, energy: str) -> List[Note]:
        """Generate minimal drum pattern."""
        notes = []
        
        for bar in range(bars):
            bar_start = bar * 4
            
            # Kick on beats 1 and 3
            notes.append(Note(pitch=DRUM_MAP["kick"], start_time=bar_start,
                            duration=0.5, velocity=100, channel=9))
            notes.append(Note(pitch=DRUM_MAP["kick"], start_time=bar_start + 2,
                            duration=0.5, velocity=100, channel=9))
        
        return notes

    def _generate_jazz_drums(self, bars: int) -> List[Note]:
        """Generate swing jazz drums."""
        notes = []
        
        for bar in range(bars):
            bar_start = bar * 4
            
            # Kick
            notes.append(Note(pitch=DRUM_MAP["kick"], start_time=bar_start,
                            duration=0.5, velocity=90, channel=9))
            notes.append(Note(pitch=DRUM_MAP["kick"], start_time=bar_start + 2.5,
                            duration=0.5, velocity=80, channel=9))
            
            # Snare (swung)
            notes.append(Note(pitch=DRUM_MAP["snare"], start_time=bar_start + 1.5,
                            duration=0.5, velocity=85, channel=9))
            
            # Hihat swing
            for t in [0, 2/3, 1.33, 2, 2.67, 3.33]:
                notes.append(Note(pitch=DRUM_MAP["closed_hihat"], start_time=bar_start + t,
                                duration=0.2, velocity=70, channel=9))
        
        return notes

    def _generate_hiphop_drums(self, bars: int, energy: str) -> List[Note]:
        """Generate hip-hop/lo-fi drums."""
        notes = []
        
        for bar in range(bars):
            bar_start = bar * 4
            
            # Kick pattern
            notes.append(Note(pitch=DRUM_MAP["kick"], start_time=bar_start,
                            duration=0.5, velocity=105, channel=9))
            notes.append(Note(pitch=DRUM_MAP["kick"], start_time=bar_start + 2.5,
                            duration=0.5, velocity=95, channel=9))
            
            # Snare
            notes.append(Note(pitch=DRUM_MAP["snare"], start_time=bar_start + 1.5,
                            duration=0.5, velocity=95, channel=9))
            notes.append(Note(pitch=DRUM_MAP["snare"], start_time=bar_start + 3.5,
                            duration=0.5, velocity=85, channel=9))
            
            # Closed hihat (sparse, laid-back)
            for t in [0, 1, 2, 3]:
                notes.append(Note(pitch=DRUM_MAP["closed_hihat"], start_time=bar_start + t,
                                duration=0.25, velocity=50, channel=9))
        
        return notes

    def _generate_progressive_drums(self, genre: str, bars: int, energy: str) -> List[Note]:
        """Generate progressive/complex drums."""
        notes = []
        
        for bar in range(bars):
            bar_start = bar * 4
            
            # Syncopated kick
            kick_times = [0, 0.75, 1.5, 2.25, 3, 3.75] if energy == "high" else [0, 1.5, 2.5, 3.5]
            for t in kick_times:
                notes.append(Note(pitch=DRUM_MAP["kick"], start_time=bar_start + t,
                                duration=0.35, velocity=100, channel=9))
            
            # Syncopated snare
            for t in [1, 3, 1.75, 3.25]:
                notes.append(Note(pitch=DRUM_MAP["snare"], start_time=bar_start + t,
                                duration=0.4, velocity=90, channel=9))
            
            # Open and closed hihat
            for t in [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5]:
                hat = DRUM_MAP["open_hihat"] if t % 1 == 0.5 else DRUM_MAP["closed_hihat"]
                notes.append(Note(pitch=hat, start_time=bar_start + t,
                                duration=0.2, velocity=random.randint(60, 80), channel=9))
        
        return notes

    def _generate_epic_drums(self, bars: int, energy: str) -> List[Note]:
        """Generate epic, cinematic drums."""
        notes = []
        
        for bar in range(bars):
            bar_start = bar * 4
            
            # Strong kick pattern
            notes.append(Note(pitch=DRUM_MAP["kick"], start_time=bar_start,
                            duration=0.6, velocity=110, channel=9))
            notes.append(Note(pitch=DRUM_MAP["kick"], start_time=bar_start + 2,
                            duration=0.6, velocity=105, channel=9))
            notes.append(Note(pitch=DRUM_MAP["kick"], start_time=bar_start + 3.5,
                            duration=0.5, velocity=95, channel=9))
            
            # Snare rolls
            notes.append(Note(pitch=DRUM_MAP["snare"], start_time=bar_start + 1,
                            duration=0.5, velocity=100, channel=9))
            notes.append(Note(pitch=DRUM_MAP["snare"], start_time=bar_start + 3,
                            duration=0.5, velocity=95, channel=9))
            
            # Dramatic tom fills (optional)
            if bar % 4 == 3:  # Every 4th bar
                for t in [0, 0.25, 0.5, 0.75]:
                    notes.append(Note(pitch=DRUM_MAP.get("tom_mid", 48), 
                                    start_time=bar_start + 3 + t,
                                    duration=0.2, velocity=85, channel=9))
        
        return notes

    def _generate_standard_drums(self, genre: str, bars: int, energy: str) -> List[Note]:
        """Generate standard drum pattern."""
        notes = []
        
        for bar in range(bars):
            bar_start = bar * 4
            
            # Kick
            notes.append(Note(pitch=DRUM_MAP["kick"], start_time=bar_start,
                            duration=0.5, velocity=100, channel=9))
            notes.append(Note(pitch=DRUM_MAP["kick"], start_time=bar_start + 2,
                            duration=0.5, velocity=100, channel=9))
            
            # Snare
            notes.append(Note(pitch=DRUM_MAP["snare"], start_time=bar_start + 1,
                            duration=0.5, velocity=90, channel=9))
            notes.append(Note(pitch=DRUM_MAP["snare"], start_time=bar_start + 3,
                            duration=0.5, velocity=90, channel=9))
            
            # Hihat
            for t in [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5]:
                vel = 75 if t % 1 == 0 else 60
                notes.append(Note(pitch=DRUM_MAP["closed_hihat"], start_time=bar_start + t,
                                duration=0.25, velocity=vel, channel=9))
        
        return notes

    # ===== HELPER METHODS =====

    def _create_directional_phrase(self, root: int, scale: List[int], phrase_type: MusicPhrase, length: float) -> List[Note]:
        """Create a musical phrase with direction."""
        notes = []
        beat = 0.0
        note_count = int(length / 0.5)  # Half-beat resolution
        
        scale_idx_range = len(scale) - 1
        
        if phrase_type == MusicPhrase.ASCENDING:
            for i in range(note_count):
                scale_idx = (i * scale_idx_range) // note_count
                pitch = root + scale[scale_idx]
                duration = length / note_count
                notes.append(Note(pitch=pitch, start_time=beat, duration=duration, velocity=75))
                beat += duration
        
        elif phrase_type == MusicPhrase.DESCENDING:
            for i in range(note_count):
                scale_idx = scale_idx_range - (i * scale_idx_range) // note_count
                pitch = root + scale[scale_idx]
                duration = length / note_count
                notes.append(Note(pitch=pitch, start_time=beat, duration=duration, velocity=75))
                beat += duration
        
        elif phrase_type == MusicPhrase.ARCH:
            # Up to middle, then down
            for i in range(note_count):
                if i < note_count / 2:
                    scale_idx = (i * scale_idx_range) // (note_count / 2)
                else:
                    scale_idx = scale_idx_range - ((i - note_count/2) * scale_idx_range) // (note_count / 2)
                pitch = root + scale[int(scale_idx) % len(scale)]
                duration = length / note_count
                notes.append(Note(pitch=pitch, start_time=beat, duration=duration, velocity=75))
                beat += duration
        
        return notes
