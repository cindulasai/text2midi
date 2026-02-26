# -*- coding: utf-8 -*-
"""
Advanced Music Theory Engine
Provides intelligent music composition rules, constraints, and generation patterns.
Based on music theory principles and contemporary composition practices.
"""

from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional
from enum import Enum
import random


class CompositionArc(Enum):
    """Musical structure templates."""
    TENSION_BUILD = "tension_build"  # Gradually increase energy
    RESOLUTION = "resolution"  # Build then resolve
    EXPLORATION = "exploration"  # Wander through ideas
    NARRATIVE = "narrative"  # Story-like progression
    MINIMALIST = "minimalist"  # Subtle evolution


@dataclass
class MusicalConstraints:
    """Rules for generating music in a specific context."""
    allowed_intervals: List[int]  # Semitones allowed in melodies
    harmonic_rhythm: int  # Beats per chord change
    max_contour_jump: int  # Max melodic leap (semitones)
    voice_leading_rules: List[str]  # Movement rules between notes
    density_curve: List[float]  # Expected note density over time (0-1)
    articulation_patterns: List[str]  # Short/long note patterns


class MusicTheoryEngine:
    """
    Advanced music theory engine for intelligent composition.
    Generates variations while maintaining musical coherence.
    """
    
    # Scales (intervallic patterns)
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
        "dorian": [0, 2, 3, 5, 7, 9, 10],
        "mixolydian": [0, 2, 4, 5, 7, 9, 10],
        "pentatonic_major": [0, 2, 4, 7, 9],
        "pentatonic_minor": [0, 3, 5, 7, 10],
        "blues": [0, 3, 5, 6, 7, 10],
        "harmonic_minor": [0, 2, 3, 5, 7, 8, 11],
    }
    
    # Consonant intervals (semitones from root)
    CONSONANT_INTERVALS = {
        0: "unison",      # Perfect
        3: "minor_third",  # Consonant
        4: "major_third",  # Consonant
        5: "perfect_fourth",  # Consonant
        7: "perfect_fifth",  # Consonant
        8: "minor_sixth",  # Consonant
        9: "major_sixth",  # Consonant
        12: "octave",     # Perfect
    }
    
    # Dissonant intervals (add tension)
    DISSONANT_INTERVALS = {
        1: "minor_second",
        2: "major_second",
        6: "tritone",
        10: "minor_seventh",
        11: "major_seventh",
    }
    
    # Interval tension values (0=consonant, 1=maximum dissonance)
    INTERVAL_TENSION = {
        0: 0.0,
        1: 0.95,   # Very tense
        2: 0.6,    # Moderately tense
        3: 0.1,
        4: 0.0,
        5: 0.0,
        6: 1.0,    # Maximum tension
        7: 0.0,
        8: 0.15,
        9: 0.0,
        10: 0.7,   # Tense
        11: 0.85,  # Very tense
        12: 0.0,
    }
    
    # Voice leading preferences (movement between consecutive notes)
    GOOD_VOICE_LEADING_INTERVALS = [
        0,      # Unison (sustain)
        1, 2,   # Small steps (stepwise motion)
        -1, -2,  # Down steps
    ]
    
    @staticmethod
    def get_scale_degrees(root: int, scale: List[int]) -> List[int]:
        """Get all playable notes in a scale across multiple octaves."""
        notes = []
        for octave in range(2, 7):  # 5 octaves
            for degree in scale:
                notes.append(root + (octave * 12) + degree)
        return notes
    
    @staticmethod
    def get_consonant_neighbors(note: int, scale: List[int]) -> List[int]:
        """
        Get notes that form consonant intervals with the given note.
        Useful for chord generation and melody harmonization.
        """
        consonant = []
        for neighbor in scale:
            interval = (neighbor - note) % 12
            if interval in MusicTheoryEngine.CONSONANT_INTERVALS:
                consonant.append(neighbor)
        return consonant
    
    @staticmethod
    def analyze_interval_tension(note1: int, note2: int) -> float:
        """
        Analyze the tension between two notes (0=consonant, 1=very dissonant).
        Used for evaluating harmonic quality.
        """
        interval = abs(note2 - note1) % 12
        return MusicTheoryEngine.INTERVAL_TENSION.get(interval, 0.5)
    
    @staticmethod
    def generate_melodic_contour(
        length: int,
        starting_note: int,
        scale: List[int],
        energy_target: float,
        arc_type: CompositionArc
    ) -> List[int]:
        """
        Generate a melodic contour with musical character.
        
        Args:
            length: Number of notes to generate
            starting_note: Starting MIDI note
            scale: Available scale degrees
            energy_target: Target energy level (0-1)
            arc_type: Musical structure type
        
        Returns:
            List of MIDI notes forming a melodic contour
        """
        contour = [starting_note]
        scale_notes = MusicTheoryEngine.get_scale_degrees(starting_note % 12, scale)
        
        for i in range(length - 1):
            # Calculate position in composition (0-1)
            position = i / (length - 1) if length > 1 else 0
            
            # Determine note based on arc type
            if arc_type == CompositionArc.TENSION_BUILD:
                # Gradually move higher
                target_range = int(energy_target * 12)  # Semitones higher
                current_note = contour[-1]
                candidates = [n for n in scale_notes 
                             if abs(n - current_note) <= 7  # Stay connected
                             and abs(n - (starting_note + target_range)) < abs(current_note - (starting_note + target_range))]
                if candidates:
                    contour.append(random.choice(candidates[:3]))  # Pick from top candidates
                else:
                    contour.append(random.choice(scale_notes))
                    
            elif arc_type == CompositionArc.RESOLUTION:
                # Build up then come back down
                if position < 0.5:
                    # First half: go up
                    current = contour[-1]
                    up_candidates = [n for n in scale_notes if n > current and abs(n - current) <= 5]
                    contour.append(random.choice(up_candidates) if up_candidates else current)
                else:
                    # Second half: come down
                    current = contour[-1]
                    down_candidates = [n for n in scale_notes if n < current and abs(n - current) <= 5]
                    contour.append(random.choice(down_candidates) if down_candidates else current)
                    
            elif arc_type == CompositionArc.EXPLORATION:
                # Wander through scale with occasional larger jumps
                current = contour[-1]
                # 70% small steps, 30% larger jumps
                if random.random() < 0.7:
                    neighbors = [n for n in scale_notes if abs(n - current) <= 3]
                else:
                    neighbors = [n for n in scale_notes if 5 <= abs(n - current) <= 12]
                if neighbors:
                    contour.append(random.choice(neighbors))
                else:
                    contour.append(random.choice(scale_notes))
                    
            elif arc_type == CompositionArc.MINIMALIST:
                # Subtle variations, mostly stepwise motion
                current = contour[-1]
                step_candidates = [n for n in scale_notes 
                                 if abs(n - current) in [0, 2, 3]]  # Steps only
                if step_candidates:
                    contour.append(random.choice(step_candidates))
                else:
                    contour.append(current)
            else:  # NARRATIVE
                # Tell a story: introduce new ideas, develop, resolve
                segment = (i / length) * 4  # 4 sections
                if segment < 1:
                    # Intro: establish
                    contour.append(random.choice(scale_notes))
                elif segment < 2:
                    # Build: explore higher
                    current = contour[-1]
                    higher = [n for n in scale_notes if n > current]
                    contour.append(random.choice(higher) if higher else current)
                elif segment < 3:
                    # Climax: move to extremes
                    contour.append(random.choice(scale_notes))
                else:
                    # Resolution: return to midpoint
                    contour.append(random.choice(scale_notes))
        
        return contour
    
    @staticmethod
    def generate_chord_progression(
        length: int,
        scale: List[int],
        root: int,
        energy_curve: List[float]
    ) -> List[List[int]]:
        """
        Generate harmonic progression based on energy curve.
        
        Args:
            length: Number of chords
            scale: Scale degrees available
            root: Root note
            energy_curve: Energy evolution (0-1) across progression
        
        Returns:
            List of chords (each chord is a list of notes)
        """
        progressions = []
        
        for i in range(length):
            energy = energy_curve[i] if i < len(energy_curve) else energy_curve[-1]
            
            # Select chord based on energy
            if energy < 0.3:
                # Low energy: simple, stable chords
                # Root position major or minor triads
                chord_types = [
                    [0, 4, 7],      # Major triad
                    [0, 3, 7],      # Minor triad
                ]
            elif energy < 0.6:
                # Medium energy: add extensions
                chord_types = [
                    [0, 4, 7, 11],  # Major 7
                    [0, 3, 7, 10],  # Minor 7
                    [0, 4, 7, 9],   # Major 6
                ]
            else:
                # High energy: extensions, alterations, suspended chords
                chord_types = [
                    [0, 2, 7],      # Sus4 (added second)
                    [0, 4, 7, 9],   # 6/9 chord
                    [0, 4, 7, 11],  # Major 7
                    [0, 3, 7, 10, 13],  # Min 7♭5
                ]
            
            chosen_chord = random.choice(chord_types)
            
            # Transpose to scale degree
            actual_chord = [(note + root) for note in chosen_chord]
            progressions.append(actual_chord)
        
        return progressions
    
    @staticmethod
    def create_variation_of_melody(
        original: List[int],
        variation_type: str,
        scale: List[int],
        percent_change: float = 0.5
    ) -> List[int]:
        """
        Create a musical variation of an existing melody.
        Common variation types: transposition, inversion, retrograde, augmentation.
        
        Args:
            original: Original melody
            variation_type: Type of variation to apply
            scale: Available scale
            percent_change: How much to change (0-1)
        
        Returns:
            Varied melody
        """
        if variation_type == "transposition":
            # Transpose by a scale degree
            degree_shift = random.randint(-3, 3) * 2  # Shift by interval
            return [note + degree_shift for note in original]
        
        elif variation_type == "inversion":
            # Mirror around center note
            if not original:
                return original
            center = original[len(original) // 2]
            return [center - (note - center) for note in original]
        
        elif variation_type == "retrograde":
            # Play backwards
            return list(reversed(original))
        
        elif variation_type == "augmentation":
            # Stretch durations (handled elsewhere, return melody unchanged)
            return original
        
        elif variation_type == "partial_mutation":
            # Change some notes while keeping structure
            varied = list(original)
            changes_to_make = int(len(original) * percent_change)
            
            for _ in range(changes_to_make):
                idx = random.randint(0, len(varied) - 1)
                scale_notes = MusicTheoryEngine.get_scale_degrees(varied[idx] % 12, scale)
                neighbors = [n for n in scale_notes if abs(n - varied[idx]) <= 7]
                if neighbors:
                    varied[idx] = random.choice(neighbors)
            
            return varied
        
        else:
            return original
    
    @staticmethod
    def analyze_phrase_quality(
        phrase: List[int],
        scale: List[int],
        target_energy: float
    ) -> Dict[str, float]:
        """
        Analyze quality metrics of a generated phrase.
        Returns scores for various musical qualities.
        """
        if not phrase or len(phrase) < 2:
            return {"score": 0.5, "contour": 0.5, "interval_quality": 0.5}
        
        # Contour analysis (does it move interestingly?)
        intervals = [phrase[i+1] - phrase[i] for i in range(len(phrase)-1)]
        interval_variety = len(set(abs(i) for i in intervals)) / (len(intervals) + 1)
        interval_range = (max(phrase) - min(phrase)) / 24  # Normalized to 2 octaves
        contour_score = (interval_variety + min(interval_range, 1.0)) / 2
        
        # Interval consonance
        consonance_total = 0
        for i in range(len(phrase) - 1):
            tension = MusicTheoryEngine.analyze_interval_tension(phrase[i], phrase[i+1])
            # Prefer some tension for energy, but not dissonant
            expected_tension = target_energy * 0.3
            difference = abs(tension - expected_tension)
            consonance_total += 1 - difference
        
        interval_quality = consonance_total / max(len(phrase) - 1, 1)
        
        # Range analysis
        phrase_range = max(phrase) - min(phrase)
        range_score = 1.0 if 5 <= phrase_range <= 24 else 0.5
        
        # Overall score
        overall = (contour_score + interval_quality + range_score) / 3
        
        return {
            "overall_score": overall,
            "contour_interest": contour_score,
            "interval_quality": interval_quality,
            "range_quality": range_score,
            "interval_variety": interval_variety,
        }
