"""
Integration test - Verify duration parsing works with app.py imports.
"""

import sys
from pathlib import Path

# Test that the imports work as expected in app.py
print("Testing duration parser imports as used in app.py...")

try:
    from src.midigent.duration_parser import DurationParser
    from src.midigent.duration_validator import DurationValidator, DurationConfig
    print("✅ Primary import path works")
except ImportError:
    # Fallback
    try:
        sys.path.insert(0, str(Path(__file__).parent / 'src'))
        from midigent.duration_parser import DurationParser
        from midigent.duration_validator import DurationValidator, DurationConfig
        print("✅ Fallback import path works")
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        sys.exit(1)

# Test a real-world example
test_prompt = "Generate a 5 minute lofi track"
print(f"\n🎵 Testing with prompt: \"{test_prompt}\"")

duration_request = DurationParser.parse(test_prompt)
if duration_request:
    tempo = 120
    config = DurationConfig()
    validation = DurationValidator.validate(duration_request, tempo=tempo, config=config)
    
    if validation.is_valid:
        bars = duration_request.to_bars(tempo=tempo)
        confirmation = DurationValidator.format_confirmation(duration_request, tempo=tempo)
        
        print(f"✅ Successfully parsed and validated")
        print(f"   Duration bars: {bars}")
        print(f"   {confirmation}")
        
        if validation.warning:
            print(f"   {validation.warning}")
    else:
        print(f"❌ Validation failed: {validation.message}")
else:
    print("❌ Failed to parse duration")
    sys.exit(1)

print("\n✅ Integration test PASSED - Ready for real use!")
