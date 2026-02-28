# -*- coding: utf-8 -*-
"""
Creative Variation Engine
Generates unique, non-repetitive musical compositions.
Implements principles of musical creativity and surprise.
"""

import random
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import math


class VariationStrategy(Enum):
    """Musical variation techniques."""
    TRANSPOSITION = "transposition"  # Move melody up/down
    INVERSION = "inversion"  # Mirror the melody
    RETROGRADE = "retrograde"  # Play backwards
    AUGMENTATION = "augmentation"  # Lengthen durations
    DIMINUTION = "diminution"  # Shorten durations
    RHYTHM_VARIATION = "rhythm_variation"  # Change rhythmic pattern
    COUNTERPOINT = "counterpoint"  # Add complementary melody
    ORCHESTRATION = "orchestration"  # Change instruments/timbre
    HARMONIC_ENRICHMENT = "harmonic_enrichment"  # Add harmonies
    PARTIAL_MUTATION = "partial_mutation"  # Change some notes
    ACCENT_VARIATION = "accent_variation"  # Change dynamics/velocity


@dataclass
class CreativeContext:
    """Context for creative generation."""
    composition_history: List[str] = None  # Previously used variations
    tension_level: float = 0.5  # Current musical tension
    bar_position: int = 0  # Current position in composition
    total_bars: int = 16  # Total length
    last_melody: Optional[List[int]] = None  # Previously generated melody
    
    def __post_init__(self):
        if self.composition_history is None:
            self.composition_history = []


class CreativeVariationEngine:
    """
    Generates creative musical variations to avoid repetition.
    Implements multiple variation strategies and intelligently combines them.
    """
    
    @staticmethod
    def generate_unique_melody(
        scale_notes: List[int],
        length: int,
        context: CreativeContext,
        energy_target: float,
        previous_melodies: List[List[int]] = None
    ) -> List[int]:
        """
        Generate a unique melody that differs from previously generated ones.
        Uses intelligently randomized variation techniques.
        """
        if previous_melodies is None:
            previous_melodies = []
        
        # Try multiple generations to find one that's sufficiently different
        best_melody = None
        best_uniqueness = 0
        
        for attempt in range(3):  # Give it multiple tries
            candidate = CreativeVariationEngine._generate_raw_melody(
                scale_notes, length, energy_target, context
            )
            
            # Check uniqueness against previous melodies
            uniqueness = CreativeVariationEngine._calculate_uniqueness(
                candidate, previous_melodies
            )
            
            if uniqueness > best_uniqueness:
                best_uniqueness = uniqueness
                best_melody = candidate
            
            # If unique enough, use it
            if uniqueness > 0.6:
                break
        
        return best_melody or scale_notes[:length]
    
    @staticmethod
    def _generate_raw_melody(
        scale_notes: List[int],
        length: int,
        energy_target: float,
        context: CreativeContext
    ) -> List[int]:
        """Generate a raw melody with creative variation."""
        melody = []
        
        # Start with a random note from the scale
        current = random.choice(scale_notes)
        melody.append(current)
        
        for i in range(length - 1):
            progress = i / length  # 0-1 position in melody
            
            # Vary the generation strategy to create unpredictability
            strategy = random.choice([
                "stepwise",
                "random_scale",
                "leap",
                "return",
                "target_jump"
            ])
            
            if strategy == "stepwise":
                # Small stepwise motion (most common)
                candidates = [n for n in scale_notes 
                            if abs(n - current) <= 4]
                
            elif strategy == "random_scale":
                # Pick any note from scale (adds surprise)
                candidates = [n for n in scale_notes]
                
            elif strategy == "leap":
                # Larger leap (adds interest)
                candidates = [n for n in scale_notes 
                            if 5 <= abs(n - current) <= 12]
                
            elif strategy == "return":
                # Go back to start (creates tension/resolution)
                candidates = [n for n in scale_notes 
                            if abs(n - melody[0]) <= 3]
                
            else:  # target_jump
                # Jump toward target energy
                if energy_target > 0.5:
                    candidates = [n for n in scale_notes if n > current]
                else:
                    candidates = [n for n in scale_notes if n < current]
            
            # Make selection
            if candidates:
                current = random.choice(candidates)
            else:
                current = random.choice(scale_notes)
            
            melody.append(current)
        
        return melody
    
    @staticmethod
    def _calculate_uniqueness(
        melody: List[int],
        previous_melodies: List[List[int]]
    ) -> float:
        """
        Calculate how unique this melody is compared to previous ones.
        Returns 0-1 score (1 = completely unique).
        """
        if not previous_melodies:
            return 1.0
        
        uniqueness_scores = []
        
        for prev in previous_melodies:
            # Compare at same length
            compare_length = min(len(melody), len(prev))
            if compare_length == 0:
                continue
            
            # Calculate note-by-note differences
            differences = 0
            for i in range(compare_length):
                if melody[i] != prev[i]:
                    differences += 1
            
            # Also check interval patterns
            if len(melody) > 2 and len(prev) > 2:
                melody_intervals = [melody[i+1] - melody[i] for i in range(len(melody)-1)]
                prev_intervals = [prev[i+1] - prev[i] for i in range(len(prev)-1)]
                
                interval_diffs = sum(1 for a, b in zip(melody_intervals, prev_intervals) if a != b)
                interval_uniqueness = interval_diffs / max(len(melody_intervals), 1)
            else:
                interval_uniqueness = 0.5
            
            note_uniqueness = differences / compare_length
            combined = (note_uniqueness * 0.6) + (interval_uniqueness * 0.4)
            uniqueness_scores.append(combined)
        
        # Return minimum uniqueness (worst case against all melodies)
        return min(uniqueness_scores) if uniqueness_scores else 1.0
    
    @staticmethod
    def apply_variation(
        original: List[int],
        variation_type: VariationStrategy,
        intensity: float = 0.5  # 0-1, how intense the variation
    ) -> List[int]:
        """
        Apply a specific variation technique to a melody.
        """
        if variation_type == VariationStrategy.TRANSPOSITION:
            # Transpose by random intervalsemitones
            semitones = random.randint(-5, 5)
            return [n + semitones for n in original]
        
        elif variation_type == VariationStrategy.INVERSION:
            # Mirror around center
            if not original:
                return original
            center = sum(original) / len(original)
            return [int(2 * center - n) for n in original]
        
        elif variation_type == VariationStrategy.RETROGRADE:
            # Play backwards
            return list(reversed(original))
        
        elif variation_type == VariationStrategy.AUGMENTATION:
            # Lengthen durations (conceptual - actual durations handled elsewhere)
            # For now, just return with "slow" characteristic
            return original
        
        elif variation_type == VariationStrategy.DIMINUTION:
            # Shorten durations
            return original
        
        elif variation_type == VariationStrategy.RHYTHM_VARIATION:
            # Shuffle rhythm while keeping notes
            indices = list(range(len(original)))
            random.shuffle(indices)
            partially_shuffled = list(original)
            
            # Only shuffle a portion (intensity controls how much)
            shuffle_count = int(len(original) * intensity)
            for i in range(shuffle_count):
                idx1, idx2 = random.sample(range(len(partially_shuffled)), 2)
                partially_shuffled[idx1], partially_shuffled[idx2] = partially_shuffled[idx2], partially_shuffled[idx1]
            
            return partially_shuffled
        
        elif variation_type == VariationStrategy.PARTIAL_MUTATION:
            # Change some notes
            mutated = list(original)
            mutation_count = int(len(original) * intensity)
            
            for _ in range(mutation_count):
                idx = random.randint(0, len(mutated) - 1)
                # Slightly alter the note (semitone up or down)
                mutated[idx] += random.choice([-2, -1, 1, 2])
            
            return mutated
        
        elif variation_type == VariationStrategy.ACCENT_VARIATION:
            # Handled at velocity/dynamics level
            return original
        
        elif variation_type == VariationStrategy.COUNTERPOINT:
            # Generate complementary melody
            # Move in opposite direction to original mostly
            counter = []
            for i, note in enumerate(original[:-1]):
                next_note = original[i + 1]
                interval = next_note - note
                
                if interval > 0:  # Original goes up
                    counter_move = random.choice([-1, 0, -1, 0])  # Mostly down
                else:  # Original goes down
                    counter_move = random.choice([1, 0, 1, 0])  # Mostly up
                
                counter.append(note + counter_move)
            
            counter.append(original[-1])
            return counter
        
        else:
            return original
    
    @staticmethod
    def compose_with_variety(
        structure: 'CompositionStructure',  # From intent parser
        scale_notes: List[int],
        complexity_level: str,
        previous_sections: List[Dict] = None
    ) -> Dict[str, List]:
        """
        Compose a section with built-in variety to avoid repetition.
        Returns dictionary with different musical elements.
        """
        if previous_sections is None:
            previous_sections = []
        
        section = {
            "melody": None,
            "harmony": None,
            "bass_line": None,
            "rhythm_pattern": None,
            "variations": []
        }
        
        # Generate unique melody
        previous_melodies = [s.get("melody") for s in previous_sections if s.get("melody")]
        melody = CreativeVariationEngine.generate_unique_melody(
            scale_notes, 8, CreativeContext(), 0.6, previous_melodies
        )
        section["melody"] = melody
        
        # If we have complexity, add variations
        if complexity_level in ["rich", "very_complex"]:
            variation_techniques = random.sample(
                list(VariationStrategy),
                min(3, len(VariationStrategy))
            )
            
            for technique in variation_techniques:
                varied = CreativeVariationEngine.apply_variation(melody, technique, 0.5)
                section["variations"].append({
                    "type": technique.value,
                    "melody": varied
                })
        
        return section
    
    @staticmethod
    def generate_rhythmic_variation(
        base_rhythm: List[float],  # Durations in beats
        intensity: float = 0.5
    ) -> List[float]:
        """
        Create rhythmic variation without completely changing pattern.
        Useful for adding interest to repeated sections.
        """
        varied_rhythm = list(base_rhythm)
        
        # Introduce syncopation
        changes = int(len(varied_rhythm) * intensity)
        
        for _ in range(changes):
            idx = random.randint(0, len(varied_rhythm) - 1)
            
            # Shorten or lengthen notes
            if varied_rhythm[idx] > 0.25:
                varied_rhythm[idx] *= random.choice([0.5, 0.75, 1.25, 1.5])
        
        return varied_rhythm
    
    @staticmethod
    def create_tension_arc(
        total_bars: int,
        energy_profile: str = "build"
    ) -> List[float]:
        """
        Generate a tension/energy arc for the composition.
        Used to guide how music evolves over time.
        
        Args:
            total_bars: Total duration
            energy_profile: "build", "decay", "dynamic", "smooth"
        
        Returns:
            List of tension values (0-1) for each bar
        """
        arc = []
        
        for bar in range(total_bars):
            progress = bar / max(total_bars - 1, 1)
            
            if energy_profile == "build":
                # Gradually increase
                tension = progress
                
            elif energy_profile == "decay":
                # Gradually decrease
                tension = 1.0 - progress
                
            elif energy_profile == "dynamic":
                # Wave pattern with multiple peaks
                tension = 0.5 + 0.4 * math.sin(progress * math.pi * 4)
                
            elif energy_profile == "smooth":
                # Gentle S-curve
                tension = 0.5 + 0.5 * math.sin((progress - 0.5) * math.pi)
                
            else:  # "static"
                tension = 0.5
            
            # Add small random variations
            tension += random.uniform(-0.05, 0.05)
            arc.append(max(0, min(1, tension)))  # Clamp to 0-1
        
        return arc
    
    @staticmethod
    def generate_accompaniment_pattern(
        root_note: int,
        scale: List[int],
        pattern_type: str,
        bars: int,
        tension: float
    ) -> Dict[str, List]:
        """
        Generate accompaniment patterns (arpeggios, broken chords, etc).
        Adds richness without repetition.
        """
        pattern = {
            "notes": [],
            "durations": [],
            "pattern_type": pattern_type
        }
        
        scale_notes = [root_note + degree for degree in scale]
        
        notes_per_bar = max(3, int(4 + tension * 4))  # More notes with higher tension
        
        for bar in range(bars):
            

            if pattern_type == "arpeggio":
                # Play scale in ascending order
                bar_notes = scale_notes[:notes_per_bar]
                if tension > 0.6:
                    # Add variation: skip notes
                    bar_notes = bar_notes[::2]
            
            elif pattern_type == "broken_chord":
                # Cycle through chord tones
                chord_root = random.choice(scale_notes)
                bar_notes = [chord_root, chord_root + 4, chord_root + 7]  # Major triad
                random.shuffle(bar_notes)
                bar_notes = bar_notes[:notes_per_bar]
            
            elif pattern_type == "pedal_point":
                # Repeat one note mostly
                pedal = scale_notes[0]
                bar_notes = [pedal] * notes_per_bar
                if random.random() < 0.3:
                    # Variation: insert another note occasionally
                    idx = random.randint(0, len(bar_notes) - 1)
                    bar_notes[idx] = random.choice(scale_notes)
            
            elif pattern_type == "descending":
                # Play downward
                bar_notes = list(reversed(scale_notes[:notes_per_bar]))
            
            else:  # "random"
                # Random notes from scale
                bar_notes = [random.choice(scale_notes) for _ in range(notes_per_bar)]
            
            pattern["notes"].extend(bar_notes)
            
            # Add durations
            note_duration = 1.0 / len(bar_notes) if bar_notes else 1.0
            pattern["durations"].extend([note_duration] * len(bar_notes))
        
        return pattern
