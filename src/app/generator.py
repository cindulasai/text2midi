# -*- coding: utf-8 -*-
"""
Music Generation Engine
Generates melodies, bass lines, drum patterns, and other musical elements.
"""

import random
from typing import List
from src.app.models import Note
from src.app.constants import SCALES, CHORD_PROGRESSIONS, DRUM_MAP


class MusicGenerator:
    """Generates musical content for different track types."""

    def generate_melody(self, root: int, mode: str, bars: int, energy: str, genre: str) -> List[Note]:
        """Generate a lead melody."""
        notes = []
        scale = SCALES.get(mode, SCALES["major"])
        beats = bars * 4
        density = {"low": 0.3, "medium": 0.5, "high": 0.7}.get(energy, 0.5)

        beat = 0.0
        while beat < beats:
            if random.random() < density:
                octave = random.choice([0, 0, 12, 12, -12])
                scale_degree = random.choice(scale)
                pitch = root + scale_degree + octave
                durations = [0.5, 1.0, 1.5, 2.0] if energy == "low" else [0.25, 0.5, 0.75, 1.0]
                duration = random.choice(durations)
                velocity = random.randint(60, 90) if energy == "low" else random.randint(70, 110)
                notes.append(Note(pitch=pitch, start_time=beat, duration=duration, velocity=velocity))
                beat += duration
            else:
                beat += 0.5
        return notes

    def generate_counter_melody(self, root: int, mode: str, bars: int, energy: str) -> List[Note]:
        """Generate a counter-melody that complements the main melody."""
        notes = []
        scale = SCALES.get(mode, SCALES["major"])
        beats = bars * 4
        
        beat = 0.0
        while beat < beats:
            if random.random() < 0.4:  # Sparser than main melody
                scale_degree = random.choice(scale[2:5])  # 3rd, 4th, 5th
                pitch = root + scale_degree + random.choice([-12, 0])
                duration = random.choice([1.0, 1.5, 2.0])
                velocity = random.randint(55, 75)
                notes.append(Note(pitch=pitch, start_time=beat, duration=duration, velocity=velocity, channel=1))
                beat += duration
            else:
                beat += 1.0
        return notes

    def generate_chords(self, root: int, genre: str, bars: int) -> List[Note]:
        """Generate chord progression."""
        notes = []
        progression = CHORD_PROGRESSIONS.get(genre, CHORD_PROGRESSIONS["pop"])
        beats_per_chord = 4
        total_beats = bars * 4

        beat = 0.0
        chord_idx = 0
        while beat < total_beats:
            chord = progression[chord_idx % len(progression)]
            for interval in chord:
                pitch = root + interval - 12
                notes.append(Note(pitch=pitch, start_time=beat, duration=beats_per_chord - 0.5,
                                  velocity=70, channel=1))
            beat += beats_per_chord
            chord_idx += 1
        return notes

    def generate_arpeggio(self, root: int, genre: str, bars: int, energy: str) -> List[Note]:
        """Generate arpeggiated pattern."""
        notes = []
        progression = CHORD_PROGRESSIONS.get(genre, CHORD_PROGRESSIONS["pop"])
        beats_per_chord = 4
        total_beats = bars * 4
        
        arp_speed = {"low": 1.0, "medium": 0.5, "high": 0.25}.get(energy, 0.5)

        beat = 0.0
        chord_idx = 0
        while beat < total_beats:
            chord = progression[chord_idx % len(progression)]
            chord_beat = beat
            
            while chord_beat < beat + beats_per_chord:
                for i, interval in enumerate(chord):
                    if chord_beat + i * arp_speed < beat + beats_per_chord:
                        pitch = root + interval
                        notes.append(Note(
                            pitch=pitch, 
                            start_time=chord_beat + i * arp_speed,
                            duration=arp_speed * 0.8,
                            velocity=random.randint(60, 80),
                            channel=2
                        ))
                chord_beat += len(chord) * arp_speed
            
            beat += beats_per_chord
            chord_idx += 1
        return notes

    def generate_bass(self, root: int, genre: str, bars: int, energy: str = "medium") -> List[Note]:
        """Generate bass line."""
        notes = []
        progression = CHORD_PROGRESSIONS.get(genre, CHORD_PROGRESSIONS["pop"])
        beats_per_chord = 4
        total_beats = bars * 4

        beat = 0.0
        chord_idx = 0
        while beat < total_beats:
            chord = progression[chord_idx % len(progression)]
            bass_note = root + chord[0] - 24

            if genre in ["electronic", "rock", "funk"]:
                for i in range(8):
                    vel = 95 if i % 2 == 0 else 75
                    notes.append(Note(pitch=bass_note, start_time=beat + i * 0.5,
                                      duration=0.4, velocity=vel, channel=2))
            elif genre == "jazz":
                for i in range(4):
                    walk_note = bass_note + random.choice([0, 2, 4, 7])
                    notes.append(Note(pitch=walk_note, start_time=beat + i,
                                      duration=0.9, velocity=75, channel=2))
            else:
                for i in range(4):
                    notes.append(Note(pitch=bass_note, start_time=beat + i,
                                      duration=0.9, velocity=80, channel=2))

            beat += beats_per_chord
            chord_idx += 1
        return notes

    def generate_pad(self, root: int, mode: str, bars: int) -> List[Note]:
        """Generate sustained pad/atmosphere."""
        notes = []
        scale = SCALES.get(mode, SCALES["major"])
        total_beats = bars * 4
        
        beat = 0.0
        while beat < total_beats:
            duration = random.choice([4.0, 8.0])
            
            for degree in [0, 2, 4]:
                if degree < len(scale):
                    pitch = root + scale[degree] - 12
                    notes.append(Note(
                        pitch=pitch,
                        start_time=beat,
                        duration=duration - 0.5,
                        velocity=random.randint(40, 60),
                        channel=3
                    ))
            
            beat += duration
        return notes

    def generate_drums(self, genre: str, bars: int, energy: str) -> List[Note]:
        """Generate drum pattern."""
        notes = []

        if genre == "electronic":
            kick_pattern = [0, 1, 2, 3]
            snare_pattern = [1, 3]
            hihat_pattern = [i * 0.25 for i in range(16)]
        elif genre == "jazz":
            kick_pattern = [0, 2.5]
            snare_pattern = []
            hihat_pattern = [i * (1/3) for i in range(12)]  # Swing
        elif genre == "rock":
            kick_pattern = [0, 2]
            snare_pattern = [1, 3]
            hihat_pattern = [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5]
        else:
            kick_pattern = [0, 2]
            snare_pattern = [1, 3]
            hihat_pattern = [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5] if energy != "low" else [0, 1, 2, 3]

        for bar in range(bars):
            bar_start = bar * 4

            for beat in kick_pattern:
                notes.append(Note(pitch=DRUM_MAP["kick"], start_time=bar_start + beat,
                                  duration=0.5, velocity=100, channel=9))

            for beat in snare_pattern:
                notes.append(Note(pitch=DRUM_MAP["snare"], start_time=bar_start + beat,
                                  duration=0.5, velocity=90, channel=9))

            for beat in hihat_pattern:
                if bar_start + beat < (bar + 1) * 4:
                    vel = 60 if beat % 1 != 0 else 75
                    notes.append(Note(pitch=DRUM_MAP["closed_hihat"], start_time=bar_start + beat,
                                      duration=0.25, velocity=vel, channel=9))

            if bar % 4 == 0:
                notes.append(Note(pitch=DRUM_MAP["crash"], start_time=bar_start,
                                  duration=2.0, velocity=85, channel=9))

        return notes

    def generate_fx(self, root: int, bars: int) -> List[Note]:
        """Generate ambient FX/texture notes."""
        notes = []
        total_beats = bars * 4
        
        beat = 0.0
        while beat < total_beats:
            if random.random() < 0.15:  # Sparse
                pitch = root + random.choice([0, 7, 12, 19, 24])
                duration = random.choice([2.0, 4.0, 8.0])
                notes.append(Note(
                    pitch=pitch,
                    start_time=beat,
                    duration=duration,
                    velocity=random.randint(30, 50),
                    channel=4
                ))
            beat += random.choice([2.0, 4.0])
        return notes
