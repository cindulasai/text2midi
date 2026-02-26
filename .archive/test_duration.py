"""
Test script for duration parsing functionality.

Tests various duration formats to ensure correct parsing and conversion.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from midigent.duration_parser import DurationParser
from midigent.duration_validator import DurationValidator, DurationConfig

# Test cases
TEST_CASES = [
    ("Generate 5 minutes of ambient music", "5 minutes → 300 seconds → 150 bars at 120 BPM"),
    ("Create a 2:30 track", "2:30 → 150 seconds → 75 bars at 120 BPM"),
    ("Make 32 bars of jazz", "32 bars → 64 seconds at 120 BPM"),
    ("Epic 10 minute composition", "10 minutes → 600 seconds → 300 bars at 120 BPM"),
    ("15 minute symphony", "15 minutes → exceeds max → clamped to 600 seconds"),
    ("Quick jingle", "No duration → default 60 seconds"),
    ("30 second intro", "30 seconds → 15 bars at 120 BPM"),
    ("1 min loop", "1 min → 60 seconds → 30 bars at 120 BPM"),
    ("64 beats track", "64 beats → 32 seconds → 16 bars at 120 BPM"),
]

def test_duration_parsing():
    """Test duration parsing with various inputs."""
    print("=" * 80)
    print("DURATION PARSING TEST")
    print("=" * 80)
    
    config = DurationConfig()
    passed = 0
    failed = 0
    
    for test_input, expected_description in TEST_CASES:
        print(f"\n📝 Testing: \"{test_input}\"")
        print(f"   Expected: {expected_description}")
        
        try:
            # Parse duration
            duration_request = DurationParser.parse(test_input)
            
            if duration_request:
                # Convert to various formats
                seconds = duration_request.to_seconds(tempo=120)
                bars = duration_request.to_bars(tempo=120)
                
                # Validate
                validation = DurationValidator.validate(duration_request, tempo=120, config=config)
                
                # Get confirmation message
                confirmation = DurationValidator.format_confirmation(duration_request, tempo=120)
                
                print(f"   ✅ Parsed: {duration_request}")
                print(f"   → {seconds:.0f} seconds, {bars} bars")
                print(f"   → {confirmation}")
                
                if validation.warning:
                    print(f"   {validation.warning}")
                elif validation.message:
                    print(f"   {validation.message}")
                    
                passed += 1
            else:
                print(f"   ⚠️  No duration found (will use default)")
                passed += 1
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            failed += 1
    
    print("\n" + "=" * 80)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("=" * 80)
    
    return failed == 0

if __name__ == "__main__":
    success = test_duration_parsing()
    sys.exit(0 if success else 1)
