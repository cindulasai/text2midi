#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Quick test of main.py in non-interactive mode.
"""

import sys
import subprocess
from pathlib import Path

def test_via_echo():
    """Test main.py using echo piping."""
    print("Testing main.py with piped input...\n")
    
    try:
        # Use echo to pipe input to main.py
        cmd = 'echo "Create a simple pop melody" | poetry run python main.py'
        
        print(f"Running: {cmd}\n")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        
        print("STDOUT:")
        print(result.stdout[:2000] if result.stdout else "(empty)")
        
        if result.stderr:
            print("\nSTDERR:")
            print(result.stderr[:1000])
        
        print(f"\nReturn code: {result.returncode}")
        
        # Check if MIDI was created
        midi_files = list(Path("outputs").glob("*.mid"))
        if midi_files:
            print(f"\n[SUCCESS] {len(midi_files)} MIDI files generated:")
            for f in midi_files[-3:]:  # Show last 3
                size = f.stat().st_size
                print(f"  - {f.name} ({size} bytes)")
            return True
        else:
            print("\n[WARNING] No MIDI files found in outputs/")
            return False
            
    except subprocess.TimeoutExpired:
        print("[ERROR] Test timed out after 30 seconds")
        return False
    except Exception as e:
        print(f"[ERROR] Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_via_echo()
    sys.exit(0 if success else 1)
