# Duration Feature - User Guide

## Overview

The MIDI generator now intelligently understands duration requests in natural language! Simply tell it how long you want your track, and it will generate accordingly.

## Supported Formats

### ✅ Minutes
```
"Generate 5 minutes of ambient music"
"Create a 3 min lofi track"
"Make 2 minutes of jazz"
```

### ✅ Seconds  
```
"Create a 30 second intro"
"Generate 90 seconds of music"
"Make a 45 sec jingle"
```

### ✅ MM:SS Format
```
"Generate a 2:30 track"
"Create a 1:45 song"
"Make a 3:00 composition"
```

### ✅ Bars
```
"Create 32 bars of jazz"
"Generate 16 bars"
"Make a 64 bar progression"
```

### ✅ Beats
```
"Generate 64 beats"
"Create 128 beats of drums"
```

## System Limits

| Limit | Value | Notes |
|-------|-------|-------|
| **Minimum** | 5 seconds | Shorter tracks lack musical coherence |
| **Maximum** | 10 minutes (600 seconds) | Ensures quality and performance |
| **Default** | 1 minute (60 seconds) | Used when no duration specified |

## Examples

### ✅ Good Requests

```
"5 minute lofi hip hop track"
→ Generates 300 seconds (150 bars at 120 BPM)

"Create a 16-bar blues progression"  
→ Generates 64 seconds at 120 BPM

"2:30 upbeat pop song"
→ Generates 150 seconds (75 bars at 120 BPM)

"Quick 30 second intro"
→ Generates 30 seconds (15 bars at 120 BPM)
```

### ⚠️ Out of Bounds (Automatically Adjusted)

```
"15 minute symphony"
→ ⚠️  Exceeds 10-minute limit. Generates 10 minutes instead.

"2 second blip"  
→ ⚠️  Below 5-second minimum. Generates 5 seconds instead.
```

## How It Works

1. **Parse**: The system extracts duration from your request
2. **Validate**: Checks against min/max limits  
3. **Convert**: Converts to bars based on tempo
4. **Confirm**: Shows what will be generated
5. **Generate**: Creates MIDI with exact duration

## Confirmation Messages

When you request a duration, you'll see a confirmation like:

```
🎵 Generating 5-minute track (300 seconds, ~150 bars at 120 BPM)
```

This helps you verify the system understood your intent correctly.

## Tips

- **Longer durations** work best with ambient/atmospheric styles
- **For complex compositions**, 2-3 minutes is optimal  
- **Use bars** when you need specific musical structure
- **Use MM:SS** for precise timing (e.g., matching video length)

## Default Behavior

If you don't specify a duration, the system uses:
- **1 minute** (60 seconds) as default
- **8 bars** for "short" tracks
- **32 bars** for "long" tracks

## Troubleshooting

### Duration not recognized?
- Make sure to include the unit: "5 minutes" not just "5"
- Use supported formats (minutes, seconds, MM:SS, bars, beats)

### Track shorter/longer than expected?
- Check the confirmation message for what was actually generated
- System may have adjusted duration to fit within limits

### Want very long tracks?
- Maximum is 10 minutes for quality and performance
- Consider generating multiple sections and combining them

---

**Feature Status**: ✅ Fully Implemented and Tested

Last Updated: January 31, 2026
