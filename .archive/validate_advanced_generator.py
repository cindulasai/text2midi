#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Quick validation of new advanced generation modules."""

import sys
from pathlib import Path

# Add to path
sys.path.insert(0, str(Path(__file__).parent))

print("Testing imports...")

try:
    from src.midigent.advanced_generator import AdvancedMusicGenerator
    print("[OK] AdvancedMusicGenerator imported successfully")
except Exception as e:
    print(f"[ERROR] Failed to import AdvancedMusicGenerator: {e}")
    sys.exit(1)

try:
    from src.midigent.emotion_instruments import EmotionAwareInstrumentMapper
    print("[OK] EmotionAwareInstrumentMapper imported successfully")
except Exception as e:
    print(f"[ERROR] Failed to import EmotionAwareInstrumentMapper: {e}")
    sys.exit(1)

# Test instantiation
try:
    gen = AdvancedMusicGenerator(session_id="test123")
    print(f"[OK] AdvancedMusicGenerator instantiated: {gen}")
except Exception as e:
    print(f"[ERROR] Failed to instantiate: {e}")
    sys.exit(1)

# Test instrument mapper
try:
    instruments = EmotionAwareInstrumentMapper.select_instruments_for_intent(
        genre="ambient",
        emotions=["peaceful", "tranquil"],
        style_descriptors=["minimal"],
        track_count=3
    )
    print(f"[OK] Emotion instrument mapper works: {len(instruments)} instruments selected")
    for inst in instruments:
        print(f"  - {inst['instrument']}: {inst['track_type']}")
except Exception as e:
    print(f"[ERROR] Failed emotion mapping: {e}")
    sys.exit(1)

print("\n[SUCCESS] All validations passed! System is ready.")
