# -*- coding: utf-8 -*-
"""
MIDI File Creation Engine
Creates and manages MIDI files from track data.
"""

import mido
from typing import List
from src.app.models import Track, Note
from src.config.constants import TICKS_PER_BEAT


class MIDIGenerator:
    """Handles MIDI file creation."""

    def __init__(self, ticks_per_beat: int = TICKS_PER_BEAT):
        self.ticks_per_beat = ticks_per_beat

    def create_midi(self, tracks: List[Track], tempo: int = 120) -> mido.MidiFile:
        """Create a MIDI file from tracks.
        
        Args:
            tracks: List of Track objects with notes
            tempo: Tempo in BPM
            
        Returns:
            mido.MidiFile object
        """
        midi = mido.MidiFile(ticks_per_beat=self.ticks_per_beat)
        tempo_track = mido.MidiTrack()
        midi.tracks.append(tempo_track)
        tempo_track.append(mido.MetaMessage('set_tempo', tempo=mido.bpm2tempo(tempo)))

        for track in tracks:
            midi_track = mido.MidiTrack()
            midi.tracks.append(midi_track)
            midi_track.append(mido.MetaMessage('track_name', name=track.name))

            if track.channel != 9:
                midi_track.append(mido.Message('program_change',
                                               channel=track.channel,
                                               program=track.midi_program))

            sorted_notes = sorted(track.notes, key=lambda n: n.start_time)
            events = []
            for note in sorted_notes:
                start_tick = int(note.start_time * self.ticks_per_beat)
                duration_tick = int(note.duration * self.ticks_per_beat)
                events.append((start_tick, 'note_on', note.pitch, note.velocity, track.channel))
                events.append((start_tick + duration_tick, 'note_off', note.pitch, 0, track.channel))

            events.sort(key=lambda x: (x[0], x[1] == 'note_on'))

            current_tick = 0
            for tick, msg_type, pitch, velocity, channel in events:
                delta = tick - current_tick
                midi_track.append(mido.Message(msg_type, note=pitch, velocity=velocity,
                                               channel=channel, time=delta))
                current_tick = tick

        return midi

    def merge_midi(self, existing_tracks: List[Track], new_tracks: List[Track], 
                   offset_bars: int, tempo: int) -> List[Track]:
        """Merge new tracks into existing, with time offset.
        
        Args:
            existing_tracks: Current tracks
            new_tracks: New tracks to add
            offset_bars: Number of bars to offset
            tempo: Current tempo
            
        Returns:
            Merged track list
        """
        offset_beats = offset_bars * 4
        
        merged = list(existing_tracks)
        for new_track in new_tracks:
            # Offset all notes
            offset_notes = []
            for note in new_track.notes:
                offset_notes.append(Note(
                    pitch=note.pitch,
                    start_time=note.start_time + offset_beats,
                    duration=note.duration,
                    velocity=note.velocity,
                    channel=note.channel
                ))
            
            # Check if track type already exists
            existing = next((t for t in merged if t.track_type == new_track.track_type), None)
            if existing:
                existing.notes.extend(offset_notes)
            else:
                merged.append(Track(
                    name=new_track.name,
                    notes=offset_notes,
                    midi_program=new_track.midi_program,
                    channel=new_track.channel,
                    track_type=new_track.track_type
                ))
        
        return merged
