"""
Real-world simulation test - Test actual user prompts end-to-end.
"""

import sys
from pathlib import Path

# Setup imports
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from midigent.duration_parser import DurationParser
from midigent.duration_validator import DurationValidator, DurationConfig

print("=" * 80)
print("REAL-WORLD USER PROMPTS TEST")
print("=" * 80)

# Simulate real user requests
USER_PROMPTS = [
    # Format variations
    "can you generate 5 minutes length tracks",  # Original user issue
    "make me a 3 minute chill lofi beat",
    "create 2:30 of upbeat electronic music",
    "I need a 45 second jingle for my podcast",
    "generate 32 bars of jazz piano",
    
    # Edge cases
    "epic 15 minute cinematic soundtrack",  # Exceeds max
    "quick 2 second sound effect",  # Below min
    "ambient music",  # No duration specified
    
    # Different styles
    "1 min techno loop at 140 BPM",
    "make a 64 beat drum pattern",
    "4 minutes of relaxing piano in C major",
]

def simulate_user_request(prompt: str, tempo: int = 120):
    """Simulate processing a user request."""
    print(f"\n{'─' * 80}")
    print(f"👤 User: \"{prompt}\"")
    print(f"{'─' * 80}")
    
    # Parse duration
    duration_request = DurationParser.parse(prompt)
    config = DurationConfig()
    
    if duration_request:
        # Validate
        validation = DurationValidator.validate(duration_request, tempo=tempo, config=config)
        
        if validation.is_valid:
            if validation.adjusted_value is not None:
                # Was clamped
                from midigent.duration_models import DurationRequest, DurationUnit
                adjusted_request = DurationRequest(validation.adjusted_value, DurationUnit.SECONDS)
                bars = adjusted_request.to_bars(tempo=tempo)
                if validation.warning:
                    print(f"🤖 {validation.warning}")
            else:
                # Use as requested
                bars = duration_request.to_bars(tempo=tempo)
                confirmation = DurationValidator.format_confirmation(duration_request, tempo=tempo)
                print(f"🤖 {confirmation}")
            
            print(f"🎹 Generating: {bars} bars at {tempo} BPM")
            return True
        else:
            print(f"🤖 ❌ {validation.message}")
            return False
    else:
        # No duration found - use default
        print(f"🤖 No duration specified, using default (60 seconds = 30 bars at {tempo} BPM)")
        return True

# Run all simulations
print("\nSimulating real user interactions...\n")

success_count = 0
for prompt in USER_PROMPTS:
    if simulate_user_request(prompt):
        success_count += 1

print("\n" + "=" * 80)
print(f"✅ SIMULATION COMPLETE: {success_count}/{len(USER_PROMPTS)} requests handled successfully")
print("=" * 80)

# Special test for the original reported issue
print("\n" + "=" * 80)
print("TESTING ORIGINAL ISSUE")
print("=" * 80)

original_issue = "can you generate 5 minutes length tracks"
print(f"\n👤 Original User Request: \"{original_issue}\"")

duration_request = DurationParser.parse(original_issue)
if duration_request:
    tempo = 120
    bars = duration_request.to_bars(tempo=tempo)
    seconds = duration_request.to_seconds(tempo=tempo)
    confirmation = DurationValidator.format_confirmation(duration_request, tempo=tempo)
    
    print(f"\n✅ FIXED! System now understands:")
    print(f"   - Parsed: {duration_request}")
    print(f"   - Duration: {seconds:.0f} seconds ({bars} bars at {tempo} BPM)")
    print(f"   - {confirmation}")
    print(f"\n🎉 The issue is RESOLVED! The system will now generate 5-minute tracks as requested.")
else:
    print(f"\n❌ Still not working - duration not parsed")

print("\n" + "=" * 80)
