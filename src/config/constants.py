# -*- coding: utf-8 -*-
"""
Shared constants for the MidiGen application.

Single source of truth for values that are used across multiple modules.
Import from here instead of hardcoding magic numbers.
"""

from pathlib import Path

# MIDI timing
TICKS_PER_BEAT: int = 480

# Composition defaults
DEFAULT_BARS: int = 64
DEFAULT_TEMPO: int = 120

# Output
OUTPUT_DIR: Path = Path("outputs")

# Pipeline
MAX_REFINEMENT_ITERATIONS: int = 2
