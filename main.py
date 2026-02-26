# -*- coding: utf-8 -*-
"""
MidiGen v2.0 - Main Entry Point
Command-line interface for AI-powered MIDI generation with LangGraph agentic architecture.
"""

import sys
import os
from pathlib import Path
from datetime import datetime
import uuid

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from src.agents.graph import get_agentic_graph, describe_graph
from src.agents.state import MusicState
from src.config.llm import call_llm, LLMConfig
import json
import random


def initialize_system():
    """Initialize LLM configuration and required systems."""
    print("\n[INIT] Starting MidiGen v2.0...")
    LLMConfig.initialize()
    print("[INIT] System ready.\n")


def print_header():
    """Print application header."""
    print("\n" + "="*70)
    print("[MUSIC]  MidiGen v2.0 - AI Music Generator (LangGraph Agentic)")
    print("="*70)
    try:
        print(describe_graph())
    except Exception:
        # Fallback if unicode issues on Windows
        print("[Graph] Advanced multi-node agentic system ready")
    print("="*70 + "\n")


def generate_dynamic_prompts() -> dict:
    """Generate 5 unique, creative music prompts dynamically using LLM with track details."""
    system_prompt = """You are an expert MIDI music generator strategist. Generate 5 COMPLETELY DIFFERENT and highly detailed music compositions.

Each must include:
1. **Title**: Creative style name (3-5 words)
2. **Prompt**: Detailed 3-5 sentence description with:
   - Specific emotions and atmospheres
   - Instrument choices and their roles
   - Genre, tempo, and musical style
   - Unique characteristics that set it apart
3. **Tracks**: Array of track descriptions (2-4 tracks), each with:
   - name: Track name (string)
   - description: What this track does (string)
4. **Duration**: Expected length in seconds
5. **Key_Mood**: Overall emotional descriptor (string)

Make each completely unique with different genres, emotions, and instrumentation. Different Request IDs will generate different prompts.

Format as valid JSON:
{
    "1": {
        "title": "Title Here",
        "prompt": "Detailed description here...",
        "tracks": [
            {"name": "Track 1", "description": "What it does"},
            {"name": "Track 2", "description": "What it does"}
        ],
        "duration": 120,
        "key_mood": "Emotional descriptor"
    },
    "2": { ... }
}

Return ONLY valid JSON, 5 completely different styles."""

    request_id = f"req_{random.randint(100000, 999999)}"
    user_message = f"Generate 5 UNIQUE and DIVERSE music prompts. Each must be completely different from the others. Include different genres, emotions, and styles. ID: {request_id}"
    
    try:
        response = call_llm(system_prompt, user_message, temperature=0.95, max_tokens=3000)
        
        if response:
            # Clean response
            response_clean = response.strip()
            if "```json" in response_clean:
                response_clean = response_clean.split("```json")[1].split("```")[0].strip()
            elif "```" in response_clean:
                response_clean = response_clean.split("```")[1].split("```")[0].strip()
            
            data = json.loads(response_clean)
            return data
    except Exception as e:
        print(f"[LLM] Dynamic prompt generation failed: {e}")
    
    # Fallback if LLM fails
    return None


def get_preset_prompts() -> dict:
    """Get dynamic prompts from LLM, fallback to static if needed."""
    # Try to generate dynamic prompts first
    dynamic_prompts = generate_dynamic_prompts()
    if dynamic_prompts:
        return dynamic_prompts
    
    # Fallback to static prompts if LLM fails
    return {
        "1": {
            "title": "Peaceful Meditation",
            "prompt": "Create a peaceful, meditative, and ethereal ambient soundscape with serene and tranquil vibes. Use sustained floating pads, soft bell tones, and nature-like whispers. The mood should be calming, spiritual, minimalist, and deeply relaxing with gentle wind instruments and natural decay.",
            "tracks": [
                {"name": "Ambient Pads", "description": "Floating, sustained harmonic background"},
                {"name": "Bell Textures", "description": "Soft chiming and ethereal tones"},
                {"name": "Wind & Nature", "description": "Gentle breezes and natural elements"}
            ],
            "duration": 120,
            "key_mood": "Tranquil, Spiritual, Calming"
        },
        "2": {
            "title": "Epic Cinematic Orchestra",
            "prompt": "Compose an epic, grandiose, and cinematic orchestral masterpiece with dramatic, uplifting, and emotionally powerful builds. Use full orchestration with strings, brass, timpani, and choir. Create sweeping violin melodies and thunderous drum patterns.",
            "tracks": [
                {"name": "Strings Section", "description": "Sweeping violins and lush orchestral strings"},
                {"name": "Brass & Percussion", "description": "Powerful horns, trumpets, and timpani"},
                {"name": "Choir & Atmosphere", "description": "Emotional vocal textures and epic builds"}
            ],
            "duration": 180,
            "key_mood": "Epic, Triumphant, Inspirational"
        },
        "3": {
            "title": "Funky Electronic Groove",
            "prompt": "Generate a funky, energetic, groovy, and rhythmic electronic track with syncopated and driving patterns. Use synth leads with attitude, syncopated synth bass with complex patterns, and progressive polyrhythmic drums.",
            "tracks": [
                {"name": "Synth Lead", "description": "Funky synth melody with attitude"},
                {"name": "Bass Groove", "description": "Complex syncopated bass with driving rhythms"},
                {"name": "Drums & Rhythm", "description": "Progressive polyrhythmic drums and percussion"}
            ],
            "duration": 150,
            "key_mood": "Energetic, Funky, Upbeat"
        },
        "4": {
            "title": "Dark Mysterious Ambient",
            "prompt": "Create a dark, mysterious, eerie, and unsettling ambient composition with experimental and chaotic textures. Use dissonant pads, wandering melodies with strange intervals, and sparse percussion.",
            "tracks": [
                {"name": "Dissonant Pads", "description": "Unsettling harmonic textures and drones"},
                {"name": "Experimental Melody", "description": "Strange intervals and wandering melodic lines"},
                {"name": "Sparse Percussion", "description": "Minimal, mysterious rhythmic elements"}
            ],
            "duration": 140,
            "key_mood": "Dark, Mysterious, Eerie"
        },
        "5": {
            "title": "Smooth Jazz Improvisation",
            "prompt": "Generate a smooth, sophisticated, cool, and expressive jazz composition with improvisation vibes. Use saxophone with sultry tones, piano comping with jazz harmonies, and swinging drums with brush work.",
            "tracks": [
                {"name": "Saxophone Solo", "description": "Sultry, expressive jazz saxophone"},
                {"name": "Jazz Piano", "description": "Sophisticated comping and jazz harmonies"},
                {"name": "Swinging Drums", "description": "Brush work and swinging jazz rhythm"}
            ],
            "duration": 160,
            "key_mood": "Smooth, Cool, Sophisticated"
        }
    }


def show_preset_menu():
    """Display detailed preset prompt menu with track information."""
    prompts = get_preset_prompts()
    
    print("\n" + "="*70)
    print("[PRESET SELECTION] Choose from AI-generated music styles")
    print("="*70)
    
    for key in ["1", "2", "3", "4", "5"]:
        if key in prompts:
            data = prompts[key]
            print(f"\n[OPTION {key}] {data['title'].upper()}")
            print("-" * 70)
            print(f"  Description: {data['prompt'][:150]}..." if len(data['prompt']) > 150 else f"  Description: {data['prompt']}")
            
            # Show track information if available
            if 'tracks' in data and data['tracks']:
                print(f"\n  [COMPOSITION DETAILS]")
                print(f"     * Tracks: {len(data['tracks'])} parts")
                for i, track in enumerate(data['tracks'], 1):
                    print(f"     * Track {i}: {track.get('name', 'Unknown')} - {track.get('description', '')}")
            
            if 'duration' in data:
                print(f"     * Duration: ~{data['duration']}s")
            if 'key_mood' in data:
                print(f"     * Mood: {data['key_mood']}")
    
    print("\n" + "="*70)
    print("[OPTION 0] >> CREATE CUSTOM PROMPT")
    print("-" * 70)
    print("  Want something unique? Create your own detailed music description.")
    print("  Include: style, mood, instruments, tempo, special effects, etc.")
    print("="*70)
    
    choice = input("\n[SELECTION] Enter 0-5 (or 0 for custom): ").strip()
    
    if choice in ["1", "2", "3", "4", "5"] and choice in prompts:
        prompt = prompts[choice]["prompt"]
        print(f"\n[SELECTED] {prompts[choice]['title']}")
        
        if 'tracks' in prompts[choice]:
            print(f"   Generating {len(prompts[choice]['tracks'])} tracks...")
        
        return prompt
    elif choice == "0":
        return get_user_prompt()
    else:
        print("\n[ERROR] Invalid choice. Please enter 0-5.")
        return show_preset_menu()


def get_user_prompt() -> str:
    """Get custom music generation prompt from user."""
    print("\n[INFO] Describe the music you want to generate:")
    print("   Examples:")
    print("   - 'Create a peaceful ambient soundscape'")
    print("   - 'Epic cinematic orchestra with full arrangement'")
    print("   - 'Simple solo piano piece in D minor'")
    print("   - 'Funky electronic beat at 125 BPM'")
    print("   - 'Sad lo-fi hip hop in D minor'")
    print()
    
    prompt = input("[TARGET] Your prompt: ").strip()
    
    if not prompt:
        print("[ERROR] Empty prompt. Please try again.")
        return get_user_prompt()
    
    return prompt


def run_generation_workflow(prompt: str):
    """Run the music generation workflow."""
    print(f"\n{'='*70}")
    print(f"[MESSAGE] Processing: {prompt[:60]}...")
    print(f"{'='*70}\n")
    
    try:
        # Get the compiled graph
        graph = get_agentic_graph()
        
        # Create initial state
        session_id = str(uuid.uuid4())[:8]
        initial_state: MusicState = {
            "user_prompt": prompt,
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
            "messages": [],
            "error": None,
            "error_context": None,
            "session_id": session_id,
            "composition_state": {
                "existing_tracks": [],
                "tempo": 120,
                "key": "C",
                "genre": "pop",
                "mode": "major",
            },
            "max_refinement_iterations": 2,
            "current_iteration": 0,
        }
        
        # Run through the graph
        config = {"configurable": {"thread_id": session_id}}
        result_state = graph.invoke(initial_state, config=config)
        
        # Print results
        print(f"\n{'='*70}")
        print("[OK] GENERATION COMPLETE")
        print(f"{'='*70}\n")
        
        if result_state.get("error"):
            print(f"[ERROR] Error: {result_state['error']}")
            return
        
        # Print session summary
        summary = result_state.get("session_summary", "")
        if summary:
            print(summary)
            print()
        
        # Print quality report if available
        quality_report = result_state.get("quality_report")
        if quality_report:
            print(f"[STATS] Quality Score: {quality_report.overall_score:.2f}/1.0")
            if quality_report.positive_aspects:
                print(f"✨ Strengths: {', '.join(quality_report.positive_aspects[:2])}")
            if quality_report.refinement_suggestions:
                print(f"💡 Tips: {', '.join(quality_report.refinement_suggestions[:2])}")
            print()
        
        # Print file path if available
        final_path = result_state.get("final_midi_path")
        if final_path:
            print(f"[SAVE] MIDI File: {final_path}")
            print(f"📂 You can find it in the 'outputs' directory")
            print()
            
            # Show file info
            if Path(final_path).exists():
                file_size = Path(final_path).stat().st_size
                print(f"   File size: {file_size:,} bytes")
        
        print()
        
    except Exception as e:
        import traceback
        print(f"[ERROR] Error during generation: {str(e)}")
        print(f"\nDebug info:\n{traceback.format_exc()}")


def main():
    """Main entry point."""
    # Initialize LLM first
    initialize_system()
    print_header()
    
    # Ensure outputs directory exists
    Path("outputs").mkdir(exist_ok=True)
    
    # Interactive mode
    while True:
        try:
            prompt = show_preset_menu()
            
            if prompt.lower() in ["quit", "exit", "q"]:
                print("\n[WAVE] Goodbye!")
                break
            
            if prompt.lower() == "help":
                print(describe_graph())
                continue
            
            # Run the workflow
            run_generation_workflow(prompt)
            
            # Ask if user wants to continue
            print("\n" + "-"*70)
            cont = input("[MUSIC] Generate another? (yes/no): ").strip().lower()
            if cont not in ["yes", "y"]:
                print("\n[WAVE] Goodbye!")
                break
            
        except KeyboardInterrupt:
            print("\n\n[WAVE] Interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"[ERROR] Unexpected error: {e}")
            import traceback
            traceback.print_exc()
            break


if __name__ == "__main__":
    main()
