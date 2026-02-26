"""
Simple MIDIgent Demo - Creates MIDI from natural language
This is a simplified MVP version that doesn't require LangGraph/Groq yet
"""

import mido
from dataclasses import dataclass
from typing import List
import random
from pathlib import Path

# === DATA STRUCTURES ===

@dataclass
class Note:
    pitch: int
    start_time: float
    duration: float
    velocity: int = 80
    channel: int = 0

@dataclass
class Track:
    name: str
    notes: List[Note]
    midi_program: int
    channel: int = 0

# === MUSIC THEORY ===

SCALES = {
    "major": [0, 2, 4, 5, 7, 9, 11],
    "minor": [0, 2, 3, 5, 7, 8, 10],
}

NOTE_TO_MIDI = {"C": 60, "D": 62, "E": 64, "F": 65, "G": 67, "A": 69, "B": 71}

DRUM_MAP = {
    "kick": 36,
    "snare": 38,
    "hihat": 42,
}

# === MIDI GENERATOR ===

class SimpleMIDIGen:
    def create_midi(self, tracks, tempo_bpm=120):
        midi = mido.MidiFile(ticks_per_beat=480)
        
        # Tempo track
        tempo_track = mido.MidiTrack()
        midi.tracks.append(tempo_track)
        tempo_track.append(mido.MetaMessage('set_tempo', tempo=mido.bpm2tempo(tempo_bpm)))
        
        # Convert each track
        for track in tracks:
            midi_track = mido.MidiTrack()
            midi.tracks.append(midi_track)
            
            # Track name
            midi_track.append(mido.MetaMessage('track_name', name=track.name))
            
            # Program change
            midi_track.append(mido.Message('program_change', program=track.midi_program, channel=track.channel))
            
            # Sort notes and add them
            events = []
            for note in track.notes:
                events.append(('on', note.start_time, note.pitch, note.velocity, note.channel))
                events.append(('off', note.start_time + note.duration, note.pitch, 0, note.channel))
            
            events.sort(key=lambda x: x[1])
            
            current_time = 0
            for event in events:
                delta = int((event[1] - current_time) * 480)
                if event[0] == 'on':
                    midi_track.append(mido.Message('note_on', note=event[2], velocity=event[3], 
                                                   channel=event[4], time=delta))
                else:
                    midi_track.append(mido.Message('note_off', note=event[2], velocity=event[3], 
                                                   channel=event[4], time=delta))
                current_time = event[1]
            
            midi_track.append(mido.MetaMessage('end_of_track'))
        
        return midi

def generate_melody(key="C", bars=8):
    """Generate a simple melody"""
    root = NOTE_TO_MIDI[key]
    scale = [root + i for i in SCALES["major"]]
    notes = []
    time = 0
    
    for _ in range(bars * 4):  # 4 beats per bar
        pitch = random.choice(scale) + 12  # Octave up
        duration = random.choice([0.5, 1.0, 1.0, 2.0])
        velocity = random.randint(70, 100)
        notes.append(Note(pitch, time, duration, velocity))
        time += duration
    
    return Track("Melody", notes, 0, 0)

def generate_chords(key="C", bars=8):
    """Generate simple chord progression"""
    root = NOTE_TO_MIDI[key]
    notes = []
    
    # I-V-vi-IV progression
    progression = [
        [root, root+4, root+7],          # I (C major)
        [root+7, root+11, root+14],      # V (G major)
        [root+9, root+12, root+16],      # vi (A minor)
        [root+5, root+9, root+12],       # IV (F major)
    ]
    
    time = 0
    for bar in range(bars):
        chord = progression[bar % 4]
        for note_pitch in chord:
            notes.append(Note(note_pitch, time, 4.0, 60, 1))
        time += 4
    
    return Track("Chords", notes, 4, 1)  # Electric piano

def generate_drums(bars=8):
    """Generate drum pattern"""
    notes = []
    
    for bar in range(bars):
        for beat in range(4):
            time = bar * 4 + beat
            # Kick on 1 and 3
            if beat in [0, 2]:
                notes.append(Note(DRUM_MAP["kick"], time, 0.1, 100, 9))
            # Snare on 2 and 4
            if beat in [1, 3]:
                notes.append(Note(DRUM_MAP["snare"], time, 0.1, 90, 9))
            # Hihat every beat
            notes.append(Note(DRUM_MAP["hihat"], time, 0.1, 70, 9))
    
    return Track("Drums", notes, 0, 9)

# === MAIN DEMO ===

def main():
    print("í¾µ MIDIgent Demo - Creating music...")
    
    # Generate tracks
    melody = generate_melody("C", 16)
    chords = generate_chords("C", 16)
    drums = generate_drums(16)
    
    # Create MIDI
    gen = SimpleMIDIGen()
    midi = gen.create_midi([melody, chords, drums], tempo_bpm=120)
    
    # Save
    Path("outputs").mkdir(exist_ok=True)
    filepath = Path("outputs/midigent_demo.mid")
    midi.save(filepath)
    
    print(f"âœ… Created MIDI file: {filepath}")
    print(f"âœ… Tracks: Melody, Chords, Drums")
    print(f"âœ… Duration: 16 bars (32 seconds at 120 BPM)")
    print("\ní¾§ Open the MIDI file in your DAW or media player to listen!")
    
    # Also create a simple version
    simple_melody = generate_melody("C", 8)
    simple_midi = gen.create_midi([simple_melody], tempo_bpm=100)
    simple_path = Path("outputs/simple_melody.mid")
    simple_midi.save(simple_path)
    print(f"\nâœ… Also created simple melody: {simple_path}")

if __name__ == "__main__":
    main()
