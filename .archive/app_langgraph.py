# -*- coding: utf-8 -*-
"""
MidiGen v2.0 - AI-Powered MIDI Generator with LangGraph Agentic Architecture
Uses LangGraph for multi-agent orchestration with self-reflection and refinement.
"""

import gradio as gr
import mido
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
import random
import re
from pathlib import Path
from datetime import datetime
import os
import json
import uuid
import traceback

# LangGraph imports
from langgraph.checkpoint.memory import MemorySaver

# Agentic architecture imports
from src.agents.graph import get_agentic_graph, describe_graph
from src.agents.state import MusicState, MusicIntent

# V2: Import variation engine for true randomization
try:
    from src.midigent.variation_engine import VariationEngine
    VARIATION_ENGINE_AVAILABLE = True
except ImportError:
    VARIATION_ENGINE_AVAILABLE = False
    print("Warning: Variation engine not available")

# Duration parsing modules
try:
    from src.midigent.duration_parser import DurationParser
    from src.midigent.duration_validator import DurationValidator, DurationConfig
    DURATION_PARSER_AVAILABLE = True
except ImportError:
    DURATION_PARSER_AVAILABLE = False
    print("Warning: Duration parser modules not available. Using basic parsing.")

# Groq integration
try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False
    print("Warning: Groq not installed. Using simple keyword-based parsing.")

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")


# ============== DATA STRUCTURES ==============

@dataclass
class Note:
    """Represents a MIDI note."""
    pitch: int
    start_time: float
    duration: float
    velocity: int = 80
    channel: int = 0

@dataclass
class Track:
    """Represents a MIDI track with notes."""
    name: str
    notes: List[Note]
    midi_program: int
    channel: int = 0
    track_type: str = "melody"

@dataclass
class GenerationSnapshot:
    """Snapshot of a generation for history."""
    timestamp: datetime
    prompt: str
    tracks: List[Track]
    tempo: int
    key: str
    mode: str
    bars: int

@dataclass
class CompositionSession:
    """Session state for multi-turn composition."""
    session_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    created_at: datetime = field(default_factory=datetime.now)
    
    # Current composition state
    tracks: List[Track] = field(default_factory=list)
    tempo: int = 120
    key: str = "C"
    mode: str = "major"
    genre: str = "pop"
    total_bars: int = 0
    
    # Conversation context
    messages: List[Dict[str, str]] = field(default_factory=list)
    generations: List[GenerationSnapshot] = field(default_factory=list)
    preferences: Dict[str, Any] = field(default_factory=dict)


# ============== MUSIC THEORY ==============

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

NOTE_TO_MIDI = {
    "C": 60, "C#": 61, "Db": 61,
    "D": 62, "D#": 63, "Eb": 63,
    "E": 64, "F": 65, "F#": 66, "Gb": 66,
    "G": 67, "G#": 68, "Ab": 68,
    "A": 69, "A#": 70, "Bb": 70, "B": 71,
}

DRUM_MAP = {
    "kick": 36, "bass_drum": 35, "snare": 38,
    "closed_hihat": 42, "open_hihat": 46,
    "crash": 49, "ride": 51,
    "tom_low": 45, "tom_mid": 47, "tom_high": 50,
    "clap": 39, "rimshot": 37, "shaker": 70,
}

GM_INSTRUMENTS = {
    "piano": 0, "bright_piano": 1, "electric_grand": 2,
    "electric_piano": 4, "rhodes": 4, "harpsichord": 6,
    "clavinet": 7, "celesta": 8, "glockenspiel": 9,
    "music_box": 10, "vibraphone": 11, "marimba": 12,
    "xylophone": 13, "tubular_bells": 14,
    "organ": 19, "church_organ": 19, "rock_organ": 18,
    "guitar": 24, "acoustic_guitar": 25, "electric_guitar": 27,
    "clean_guitar": 27, "distortion_guitar": 30,
    "bass": 32, "electric_bass": 33, "finger_bass": 33,
    "pick_bass": 34, "fretless_bass": 35, "slap_bass": 36,
    "synth_bass": 38, "synth_bass_2": 39,
    "violin": 40, "viola": 41, "cello": 42, "contrabass": 43,
    "strings": 48, "synth_strings": 50, "slow_strings": 49,
    "choir": 52, "voice_oohs": 53, "synth_voice": 54,
    "trumpet": 56, "trombone": 57, "tuba": 58, "brass": 61,
    "saxophone": 64, "alto_sax": 65, "tenor_sax": 66,
    "clarinet": 71, "oboe": 68, "bassoon": 70,
    "flute": 73, "recorder": 74, "pan_flute": 75,
    "synth_lead": 80, "square_lead": 80, "sawtooth": 81,
    "synth_pad": 88, "warm_pad": 89, "polysynth": 90,
    "space_voice": 91, "bowed_pad": 92, "metallic_pad": 93,
    "halo_pad": 94, "sweep_pad": 95,
    "fx_rain": 96, "fx_soundtrack": 97, "fx_crystal": 98,
    "fx_atmosphere": 99, "fx_brightness": 100,
    "sitar": 104, "banjo": 105, "shamisen": 106, "koto": 107,
    "kalimba": 108, "bagpipe": 109, "fiddle": 110,
    "drums": 128,
}

GENRE_CONFIG = {
    "pop": {"tempo_range": (100, 130), "key": "C", "mode": "major", "energy": "medium", "typical_tracks": 4},
    "rock": {"tempo_range": (110, 140), "key": "E", "mode": "minor", "energy": "high", "typical_tracks": 5},
    "electronic": {"tempo_range": (120, 135), "key": "A", "mode": "minor", "energy": "high", "typical_tracks": 6},
    "lofi": {"tempo_range": (70, 90), "key": "D", "mode": "minor", "energy": "low", "typical_tracks": 4},
    "jazz": {"tempo_range": (80, 140), "key": "F", "mode": "dorian", "energy": "medium", "typical_tracks": 5},
    "classical": {"tempo_range": (60, 120), "key": "G", "mode": "major", "energy": "medium", "typical_tracks": 4},
    "ambient": {"tempo_range": (60, 80), "key": "C", "mode": "major", "energy": "low", "typical_tracks": 3},
    "cinematic": {"tempo_range": (70, 100), "key": "D", "mode": "minor", "energy": "high", "typical_tracks": 7},
    "funk": {"tempo_range": (95, 115), "key": "E", "mode": "mixolydian", "energy": "high", "typical_tracks": 5},
    "rnb": {"tempo_range": (70, 100), "key": "Ab", "mode": "minor", "energy": "medium", "typical_tracks": 5},
}

CHORD_PROGRESSIONS = {
    "pop": [[0, 4, 7], [5, 9, 12], [7, 11, 14], [5, 9, 12]],
    "rock": [[0, 4, 7], [7, 11, 14], [5, 9, 12], [0, 4, 7]],
    "jazz": [[0, 4, 7, 11], [5, 9, 12, 16], [2, 5, 9, 12], [7, 11, 14, 17]],
    "lofi": [[0, 4, 7, 11], [2, 5, 9], [5, 9, 12], [7, 11, 14]],
    "electronic": [[0, 4, 7], [0, 4, 7], [5, 9, 12], [7, 11, 14]],
    "classical": [[0, 4, 7], [5, 9, 12], [4, 7, 11], [0, 4, 7]],
    "ambient": [[0, 4, 7, 11], [0, 4, 7, 11], [5, 9, 12, 16], [5, 9, 12, 16]],
    "cinematic": [[0, 3, 7], [5, 8, 12], [7, 10, 14], [3, 7, 10]],
    "funk": [[0, 4, 7, 10], [5, 9, 12], [0, 4, 7, 10], [7, 11, 14]],
    "rnb": [[0, 4, 7, 11], [2, 5, 9, 12], [5, 9, 12, 16], [7, 11, 14, 17]],
}


# ============== MIDI GENERATOR ==============

class MIDIGenerator:
    """Handles MIDI file creation."""

    def __init__(self, ticks_per_beat: int = 480):
        self.ticks_per_beat = ticks_per_beat

    def create_midi(self, tracks: List[Track], tempo: int = 120) -> mido.MidiFile:
        """Create a MIDI file from tracks."""
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
        """Merge new tracks into existing, with time offset."""
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


# ============== MUSIC GENERATOR ==============

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
            if random.random() < 0.4:
                scale_degree = random.choice(scale[2:5])
                pitch = root + scale_degree + random.choice([-12, 0])
                duration = random.choice([1.0, 1.5, 2.0])
                velocity = random.randint(55, 75)
                notes.append(Note(pitch=pitch, start_time=beat, duration=duration, velocity=velocity, channel=1))
                beat += duration
            else:
                beat += 1.0
        return notes

    def generate_harmony(self, root: int, mode: str, bars: int, energy: str) -> List[Note]:
        """Generate harmonic chords."""
        notes = []
        scale = SCALES.get(mode, SCALES["major"])
        beats = bars * 4
        
        beat = 0.0
        while beat < beats:
            # Build simple triad from scale
            for degree in [0, 2, 4]:
                if degree < len(scale):
                    pitch = root + scale[degree] - 12
                    notes.append(Note(
                        pitch=pitch,
                        start_time=beat,
                        duration=4.0,
                        velocity=random.randint(50, 70),
                        channel=1
                    ))
            beat += 4.0
        return notes

    def generate_bass(self, root: int, mode: str, bars: int, energy: str) -> List[Note]:
        """Generate bass line."""
        notes = []
        scale = SCALES.get(mode, SCALES["major"])
        beats = bars * 4
        
        beat = 0.0
        while beat < beats:
            bass_pitch = root + scale[0] - 24
            for i in range(4):
                notes.append(Note(
                    pitch=bass_pitch,
                    start_time=beat + i,
                    duration=0.9,
                    velocity=random.randint(75, 95),
                    channel=2
                ))
            beat += 4.0
        return notes

    def generate_arpeggio(self, root: int, mode: str, bars: int, energy: str) -> List[Note]:
        """Generate arpeggiated pattern."""
        notes = []
        scale = SCALES.get(mode, SCALES["major"])
        beats = bars * 4
        
        beat = 0.0
        arp_speed = {"low": 1.0, "medium": 0.5, "high": 0.25}.get(energy, 0.5)
        
        while beat < beats:
            for degree in [0, 2, 4]:
                if degree < len(scale):
                    pitch = root + scale[degree]
                    notes.append(Note(
                        pitch=pitch,
                        start_time=beat,
                        duration=arp_speed * 0.8,
                        velocity=random.randint(60, 80),
                        channel=2
                    ))
                    beat += arp_speed
        
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

    def generate_drums(self, bars: int, energy: str, genre: str) -> List[Note]:
        """Generate drum pattern."""
        notes = []
        total_beats = bars * 4

        if genre == "electronic":
            kick_pattern = [0, 1, 2, 3]
            snare_pattern = [1, 3]
            hihat_pattern = [i * 0.25 for i in range(16)]
        elif genre == "jazz":
            kick_pattern = [0, 2.5]
            snare_pattern = []
            hihat_pattern = [i * (1/3) for i in range(12)]
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

        return notes

    def generate_fx(self, root: int, bars: int) -> List[Note]:
        """Generate ambient FX/texture notes."""
        notes = []
        total_beats = bars * 4
        
        beat = 0.0
        while beat < total_beats:
            if random.random() < 0.15:
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


# ============== MAIN APPLICATION ==============

class MidiGenAgenticApp:
    """Main application using LangGraph agentic architecture."""

    def __init__(self):
        self.graph = get_agentic_graph()
        self.midi_gen = MIDIGenerator()
        self.session: Optional[CompositionSession] = None
        self.variation_engine: Optional[VariationEngine] = None
        Path("outputs").mkdir(exist_ok=True)
        
        print("\n" + "="*70)
        print("🎵 MidiGen v2.0 - Agentic Architecture (LangGraph)")
        print("="*70)
        print(describe_graph())
        print("="*70 + "\n")

    def _get_session_summary(self) -> str:
        """Get current session state as string."""
        if not self.session or self.session.total_bars == 0:
            return "**No active composition**\n\nStart by describing the music you want!"
        
        track_list = "\n".join([f"  - {t.name} ({t.track_type})" for t in self.session.tracks])
        return f"""**Current Composition:**
- Genre: {self.session.genre}
- Key: {self.session.key} {self.session.mode}
- Tempo: {self.session.tempo} BPM
- Duration: {self.session.total_bars} bars
- Tracks ({len(self.session.tracks)}):
{track_list}"""

    def process_message(self, message: str, history: List[Dict[str, str]]) -> tuple:
        """Process user message through agentic workflow."""
        if not message.strip():
            return "", None, history, self._get_session_summary()

        try:
            # Initialize session if needed
            if not self.session:
                self.session = CompositionSession()
                if VARIATION_ENGINE_AVAILABLE:
                    self.variation_engine = VariationEngine(self.session.session_id)
                print(f"\n🎯 New session: {self.session.session_id}")

            print(f"\n{'='*70}")
            print(f"📨 User: {message[:60]}...")
            print(f"{'='*70}\n")

            # Prepare initial state for graph
            initial_state: MusicState = {
                "user_prompt": message,
                "intent": None,
                "track_plan": [],
                "theory_validation": {},
                "theory_valid": False,
                "theory_issues": [],
                "generated_tracks": [],
                "generation_metadata": {},
                "quality_report": None,
                "refinement_attempts": 0,
                "refinement_feedback": "",
                "needs_refinement": False,
                "final_midi_path": None,
                "session_summary": "",
                "messages": self.session.messages,
                "error": None,
                "error_context": None,
                "session_id": self.session.session_id,
                "composition_state": {
                    "existing_tracks": self.session.tracks,
                    "tempo": self.session.tempo,
                    "key": self.session.key,
                    "genre": self.session.genre,
                    "mode": self.session.mode,
                },
                "max_refinement_iterations": 2,
                "current_iteration": 0,
            }

            # Run through agentic graph
            config = {"configurable": {"thread_id": self.session.session_id}}
            result_state = self.graph.invoke(initial_state, config=config)

            # Handle errors
            if result_state.get("error"):
                error_msg = f"❌ Error: {result_state['error']}"
                history.append({"role": "user", "content": message})
                history.append({"role": "assistant", "content": error_msg})
                return "", None, history, self._get_session_summary()

            # Extract results
            generated_tracks = result_state.get("generated_tracks", [])
            final_midi_path = result_state.get("final_midi_path")
            session_summary = result_state.get("session_summary", "Composition complete!")
            quality_report = result_state.get("quality_report")

            # Update session if we have tracks
            if generated_tracks:
                self.session.tracks = generated_tracks
                intent = result_state.get("intent")
                
                if intent:
                    self.session.genre = intent.genre
                    self.session.key = intent.key_preference or self.session.key
                    self.session.tempo = intent.tempo_preference or self.session.tempo
                    self.session.total_bars = intent.duration_requested or 16
                
                # Save snapshot
                self.session.generations.append(GenerationSnapshot(
                    timestamp=datetime.now(),
                    prompt=message,
                    tracks=list(self.session.tracks),
                    tempo=self.session.tempo,
                    key=self.session.key,
                    mode=self.session.mode,
                    bars=self.session.total_bars
                ))

            # Build response
            response_parts = [session_summary]
            
            if quality_report:
                response_parts.append(f"\n📊 **Quality Score:** {quality_report.overall_score:.2f}/1.0")
                if quality_report.positive_aspects:
                    response_parts.append(f"✨ **Strengths:** {', '.join(quality_report.positive_aspects[:2])}")
                if quality_report.refinement_suggestions:
                    response_parts.append(f"💡 **Tips:** {', '.join(quality_report.refinement_suggestions[:2])}")

            if final_midi_path:
                response_parts.append("\n✅ **Your MIDI file is ready to download!**")
                response_parts.append("\n**Continue building:**")
                response_parts.append("- \"Add some strings\"")
                response_parts.append("- \"Make it more energetic\"")
                response_parts.append("- \"Add 8 more bars\"")
                response_parts.append("- \"New song\" to start fresh")

            response = "\n".join(response_parts)
            
            history.append({"role": "user", "content": message})
            history.append({"role": "assistant", "content": response})

            return "", final_midi_path, history, self._get_session_summary()

        except Exception as e:
            error_msg = f"❌ Error: {str(e)}\n\nDebug: {traceback.format_exc()[:200]}"
            print(f"ERROR: {error_msg}")
            history.append({"role": "user", "content": message})
            history.append({"role": "assistant", "content": error_msg})
            return "", None, history, self._get_session_summary()

    def create_ui(self) -> gr.Blocks:
        """Create Gradio interface."""
        
        with gr.Blocks(title="MidiGen v2.0 - Agentic AI Music Creator") as app:
            
            gr.Markdown("""
            # 🎵 MidiGen v2.0 - AI Music Creator (Agentic)
            
            **Create MIDI music through conversation with LangGraph!**
            
            ✨ **Features:**
            - 🤖 **Agentic Architecture**: Multiple specialized agents orchestrating music generation
            - 🎼 **Intelligent Planning**: AI-guided track arrangement and composition
            - 🔍 **Self-Reflection**: Quality assessment and automatic refinement
            - 💬 **Multi-turn Support**: Build compositions across multiple messages
            - 🎛️ **1-8 Dynamic Tracks**: Scales from simple to orchestral arrangements
            """)

            with gr.Row():
                with gr.Column(scale=2):
                    chatbot = gr.Chatbot(
                        height=350,
                        label="Chat with MidiGen Agent",
                    )
                    msg = gr.Textbox(
                        placeholder="Describe music (e.g., 'Epic orchestral piece' or 'Simple piano melody')...",
                        label="Your Message",
                        lines=2,
                    )
                    with gr.Row():
                        send_btn = gr.Button("Generate", variant="primary")
                        clear_btn = gr.Button("Clear Chat")
                        reset_btn = gr.Button("New Song", variant="secondary")

                with gr.Column(scale=1):
                    session_display = gr.Markdown(
                        value="**No active composition**\n\nStart by describing the music you want!",
                        label="Session State"
                    )
                    audio_output = gr.File(label="Download MIDI", type="filepath")
                    
                    gr.Markdown("""
                    ### Examples
                    
                    **Simple (1-2 tracks):**
                    - "Solo piano ballad"
                    - "Just acoustic guitar"
                    
                    **Standard (4-5 tracks):**
                    - "Upbeat pop song"
                    - "Chill lo-fi beat"
                    
                    **Rich (6-8 tracks):**
                    - "Epic cinematic orchestra"
                    - "Full electronic production"
                    
                    **Multi-turn:**
                    - "Add strings"
                    - "Make it more energetic"
                    - "New song"
                    """)

            def respond(message, history):
                return self.process_message(message, history)

            def reset_session():
                self.session = CompositionSession()
                if VARIATION_ENGINE_AVAILABLE:
                    self.variation_engine = VariationEngine(self.session.session_id)
                return [], None, "**No active composition**\n\nStart by describing the music you want!"

            send_btn.click(respond, [msg, chatbot], [msg, audio_output, chatbot, session_display])
            msg.submit(respond, [msg, chatbot], [msg, audio_output, chatbot, session_display])
            clear_btn.click(reset_session, outputs=[chatbot, audio_output, session_display])
            reset_btn.click(reset_session, outputs=[chatbot, audio_output, session_display])

            gr.Examples(
                examples=[
                    "Create a peaceful ambient soundscape",
                    "Epic cinematic orchestra with full arrangement",
                    "Simple solo piano piece",
                    "Funky electronic beat at 125 BPM",
                    "Sad lo-fi hip hop in D minor",
                ],
                inputs=msg,
            )

        return app


def main():
    """Main entry point."""
    print("\n🚀 Starting MidiGen v2.0 with LangGraph Agentic Architecture...")
    print(f"   Groq API available: {GROQ_AVAILABLE}")
    print(f"   Variation Engine available: {VARIATION_ENGINE_AVAILABLE}")
    print(f"   Duration Parser available: {DURATION_PARSER_AVAILABLE}\n")
    
    app = MidiGenAgenticApp()
    interface = app.create_ui()
    
    interface.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True,
    )


if __name__ == "__main__":
    main()
