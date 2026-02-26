# -*- coding: utf-8 -*-
"""
Test script to verify the workflow works end-to-end.
"""

import sys
import os
from pathlib import Path

# Set environment variable to handle Unicode
os.environ['PYTHONIOENCODING'] = 'utf-8'

sys.path.insert(0, str(Path(__file__).parent))

from src.agents.graph import get_agentic_graph
from src.agents.state import MusicState
import uuid


def test_workflow():
    """Test a simple workflow."""
    print("\nTesting MidiGen Workflow...\n")
    
    try:
        # Get the compiled graph
        print("1. Loading graph...")
        graph = get_agentic_graph()
        print("   [OK] Graph loaded")
        
        # Create initial state
        print("\n2. Creating initial state...")
        session_id = str(uuid.uuid4())[:8]
        initial_state: MusicState = {
            "user_prompt": "Create a simple lo-fi beat",
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
            "max_refinement_iterations": 1,
            "current_iteration": 0,
        }
        print(f"   [OK] State created (session: {session_id})")
        
        # Run through the graph
        print("\n3. Running workflow...")
        config = {"configurable": {"thread_id": session_id}}
        result_state = graph.invoke(initial_state, config=config)
        
        print("\n4. Checking results...")
        
        if result_state.get("error"):
            print(f"   [ERROR] Workflow error: {result_state['error']}")
            return False
        
        print(f"   [OK] No errors")
        print(f"   [OK] Generated tracks: {len(result_state.get('generated_tracks', []))}")
        print(f"   [OK] MIDI path: {result_state.get('final_midi_path', 'N/A')}")
        print(f"   [OK] Session summary: {bool(result_state.get('session_summary'))}")
        
        # Verify MIDI file was created
        final_path = result_state.get("final_midi_path")
        if final_path:
            midi_file = Path(final_path)
            if midi_file.exists():
                size = midi_file.stat().st_size
                print(f"\n[SUCCESS] MIDI file created successfully!")
                print(f"   Path: {final_path}")
                print(f"   Size: {size:,} bytes")
                return True
            else:
                print(f"\n[FAILED] MIDI file path set but file not found: {final_path}")
                return False
        else:
            print(f"\n[WARNING] No MIDI path returned")
            return False
        
    except Exception as e:
        print(f"\n[FAILED] Test failed with error:")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_workflow()
    sys.exit(0 if success else 1)
