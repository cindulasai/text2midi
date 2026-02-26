# -*- coding: utf-8 -*-
"""
Web UI Module - Gradio Interface for MidiGen
Provides the interactive music generation interface.
"""

import gradio as gr
import random
from pathlib import Path
from datetime import datetime
from typing import List, Dict

from src.app.models import CompositionSession, GenerationSnapshot, Track
from src.app.constants import GENRE_CONFIG, NOTE_TO_MIDI, GM_INSTRUMENTS
from src.app.generator import MusicGenerator
from src.app.midi_creator import MIDIGenerator
from src.app.intent_parser import IntentParser
from src.app.session import get_session_summary, ensure_output_directory

try:
    from src.midigent.variation_engine import VariationEngine
    VARIATION_ENGINE_AVAILABLE = True
except ImportError:
    VARIATION_ENGINE_AVAILABLE = False


class MidiGenApp:
    """Main application with session support."""

    def __init__(self):
        self.parser = IntentParser()
        self.generator = MusicGenerator()
        self.midi_gen = MIDIGenerator()
        self.session: CompositionSession = None
        self.variation_engine = None
        ensure_output_directory()

    def _generate_tracks_from_plan(self, track_plan, root: int, 
                                   mode: str, bars: int, energy: str, genre: str) -> List[Track]:
        """Generate tracks based on plan."""
        print(f"\n🎼 Generating tracks from plan with {len(track_plan)} configs...")
        
        tracks = []
        channel_map = {}
        next_channel = 0
        
        for i, config in enumerate(track_plan):
            print(f"  Track {i+1}/{len(track_plan)}: {config.track_type} - {config.instrument}")
            
            # Assign channels
            if config.track_type == "drums":
                channel = 9
            else:
                if config.track_type not in channel_map:
                    channel_map[config.track_type] = next_channel
                    next_channel = (next_channel + 1) % 9
                    if next_channel == 9:
                        next_channel = 0
                channel = channel_map[config.track_type]
            
            # Get instrument program
            instrument = config.instrument.lower().replace(" ", "_")
            program = GM_INSTRUMENTS.get(instrument, 0)
            
            # Generate notes based on track type
            if config.track_type == "lead":
                notes = self.generator.generate_melody(root, mode, bars, energy, genre)
            elif config.track_type == "counter_melody":
                notes = self.generator.generate_counter_melody(root, mode, bars, energy)
            elif config.track_type == "harmony":
                notes = self.generator.generate_chords(root, genre, bars)
            elif config.track_type == "bass":
                notes = self.generator.generate_bass(root, genre, bars, energy)
            elif config.track_type == "drums":
                notes = self.generator.generate_drums(genre, bars, energy)
            elif config.track_type == "arpeggio":
                notes = self.generator.generate_arpeggio(root, genre, bars, energy)
            elif config.track_type == "pad":
                notes = self.generator.generate_pad(root, mode, bars)
            elif config.track_type == "fx":
                notes = self.generator.generate_fx(root, bars)
            else:
                notes = self.generator.generate_melody(root, mode, bars, energy, genre)
            
            # Update channel for notes
            for note in notes:
                note.channel = channel
            
            track_name = f"{config.instrument.title()} ({config.track_type})"
            track = Track(track_name, notes, program, channel, config.track_type)
            tracks.append(track)
            print(f"    ✓ Created track with {len(notes)} notes, channel {channel}")
        
        print(f"✅ Total tracks generated: {len(tracks)}\n")
        return tracks

    def process_message(self, message: str, history: List[Dict[str, str]]) -> tuple:
        """Process user message with session support.
        
        Args:
            message: User's message
            history: Chat history
            
        Returns:
            Tuple of (empty_message, file_path, updated_history, session_summary)
        """
        if not message.strip():
            return "", None, history, self._get_session_summary()

        try:
            # Initialize session if needed
            if not self.session:
                self.session = CompositionSession()
                if VARIATION_ENGINE_AVAILABLE:
                    self.variation_engine = VariationEngine(self.session.session_id)
                print(f"🎯 New session: {self.session.session_id}")

            # Parse intent with session context
            intent = self.parser.parse(message, self.session)
            action = intent.get("action", "new")
            
            # Handle reset
            if action == "reset":
                self.session = CompositionSession()
                if VARIATION_ENGINE_AVAILABLE:
                    self.variation_engine = VariationEngine(self.session.session_id)
                print(f"🎯 New session (reset): {self.session.session_id}")
                history.append({"role": "user", "content": message})
                history.append({"role": "assistant", "content": "Started fresh! What would you like to create?"})
                return "", None, history, self._get_session_summary()

            # Get parameters
            if action in ["new", "reset"]:
                genre = intent.get("genre", "pop")
                config = GENRE_CONFIG.get(genre, GENRE_CONFIG["pop"])
                tempo = intent.get("tempo") or random.randint(*config["tempo_range"])
                key = intent.get("key") or config["key"]
            else:
                genre = intent.get("genre", self.session.genre)
                config = GENRE_CONFIG.get(genre, GENRE_CONFIG["pop"])
                tempo = intent.get("tempo") or self.session.tempo
                key = intent.get("key") or self.session.key
            
            mode = config["mode"]
            if "m" in key.lower():
                mode = "minor"
                key = key.replace("m", "").replace("M", "")
            
            energy = intent.get("energy", config["energy"])
            bars = intent.get("duration_bars", 16)
            
            root_key = key.replace("m", "").replace("M", "")
            root = NOTE_TO_MIDI.get(root_key, 60)

            # Get track plan
            track_plan = intent.get("track_plan", [])
            if not track_plan:
                track_plan = self.parser.track_planner.plan_tracks(message, genre)
            
            print(f"\n📋 Track plan has {len(track_plan)} configurations")

            # Initialize generation with seed
            if self.variation_engine:
                seed = self.variation_engine.initialize_generation()
            else:
                import time
                seed = int(time.time() * 1000000)
                random.seed(seed)

            # Generate new tracks
            new_tracks = self._generate_tracks_from_plan(track_plan, root, mode, bars, energy, genre)
            print(f"📦 Generated {len(new_tracks)} new tracks")
            
            # Validate track count
            if len(new_tracks) != len(track_plan):
                raise ValueError(f"Track count mismatch! Planned: {len(track_plan)}, Generated: {len(new_tracks)}")

            # Handle action
            if action == "extend" and self.session.total_bars > 0:
                self.session.tracks = self.midi_gen.merge_midi(
                    self.session.tracks, new_tracks, self.session.total_bars, tempo
                )
                self.session.total_bars += bars
            else:
                self.session.tracks = new_tracks
                self.session.total_bars = bars
            
            # Update session state
            self.session.tempo = tempo
            self.session.key = key
            self.session.mode = mode
            self.session.genre = genre

            # Create and save MIDI
            print(f"\n💾 Creating MIDI file with {len(self.session.tracks)} tracks...")
            midi = self.midi_gen.create_midi(self.session.tracks, tempo)
            print(f"   MIDI object has {len(midi.tracks)} tracks (including tempo track)")
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"midigen_{genre}_{self.session.session_id}_{timestamp}.mid"
            filepath = Path("outputs") / filename
            midi.save(filepath)
            print(f"✅ Saved: {filepath}\n")

            # Save snapshot
            self.session.generations.append(GenerationSnapshot(
                timestamp=datetime.now(),
                prompt=message,
                tracks=list(self.session.tracks),
                tempo=tempo,
                key=key,
                mode=mode,
                bars=self.session.total_bars
            ))

            # Create response
            response = self._create_response(intent, action, len(new_tracks), filepath)
            
            history.append({"role": "user", "content": message})
            history.append({"role": "assistant", "content": response})
            
            return "", str(filepath), history, self._get_session_summary()

        except Exception as e:
            error_msg = f"Sorry, I encountered an error: {str(e)}"
            history.append({"role": "user", "content": message})
            history.append({"role": "assistant", "content": error_msg})
            return "", None, history, self._get_session_summary()

    def _create_response(self, intent: Dict, action: str, new_tracks: int, filepath: Path) -> str:
        """Create response message."""
        genre = intent.get("genre", "pop")
        mood = intent.get("mood", "")
        
        action_text = {
            "new": "Created",
            "extend": "Extended with",
            "modify": "Modified",
        }.get(action, "Generated")

        duration_info = intent.get('duration_confirmation', '')
        if duration_info:
            duration_display = f"\n{duration_info}\n"
        else:
            duration_display = ""

        response = f"""{action_text} {mood + ' ' if mood else ''}{genre} composition!
{duration_display}

**Total Composition:**
- Duration: {self.session.total_bars} bars
- Total tracks: {len(self.session.tracks)}
- Tempo: {self.session.tempo} BPM
- Key: {self.session.key} {self.session.mode}

Your MIDI file is ready to download!

**Continue building:**
- "Add some strings"
- "Make it more energetic"
- "Add 16 more bars"
- "Change to minor key"
- Or say "new song" to start fresh"""

        return response

    def _get_session_summary(self) -> str:
        """Get current session state."""
        if not self.session or self.session.total_bars == 0:
            return "No active composition"
        return get_session_summary(self.session)

    def create_ui(self) -> gr.Blocks:
        """Create Gradio interface."""
        
        with gr.Blocks(title="MidiGen v2.0 - AI Music Creator") as app:
            
            gr.Markdown("""
            # MidiGen v2.0 - AI Music Creator
            
            Create MIDI music through conversation! **Dynamic tracks** (1-8) based on your description.
            **Multi-turn** support - keep building on your composition!
            """)

            with gr.Row():
                with gr.Column(scale=2):
                    chatbot = gr.Chatbot(
                        height=350,
                        label="Chat with MidiGen",
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
                    - "Make drums louder"
                    - "16 more bars"
                    """)

            def respond(message, history):
                return self.process_message(message, history)

            def reset_session():
                self.session = CompositionSession()
                return [], None, "**No active composition**\n\nStart by describing the music you want!"

            send_btn.click(respond, [msg, chatbot], [msg, audio_output, chatbot, session_display])
            msg.submit(respond, [msg, chatbot], [msg, audio_output, chatbot, session_display])
            
            def clear_and_reset():
                self.session = CompositionSession()
                return [], None, "**No active composition**\n\nStart by describing the music you want!"
            
            clear_btn.click(clear_and_reset, outputs=[chatbot, audio_output, session_display])
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
