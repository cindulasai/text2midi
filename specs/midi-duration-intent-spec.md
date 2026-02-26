# Feature Specification: MIDI Track Duration Intent Understanding

**Feature Name**: Intelligent MIDI Duration Parsing  
**Created**: 2026-01-31  
**Status**: Draft  
**Priority**: High  

## Problem Statement

### Current Issue
When users request MIDI tracks with specific durations (e.g., "generate 5 minutes length tracks"), the system does not correctly interpret or honor the requested duration. This leads to:
- User frustration due to unmet expectations
- Unclear whether this is a technical constraint or a parsing failure
- Missed opportunity to understand and fulfill user intent

### Example Failure Scenario
**User Input**: "Can you generate 5 minutes length tracks"  
**Expected Behavior**: Generate MIDI file with approximately 5 minutes (300 seconds) of music  
**Actual Behavior**: System ignores duration request and generates default-length track

## Root Cause Analysis

The issue stems from one or more of the following:

1. **Natural Language Parsing Gap**: The system may not extract duration information from conversational requests
2. **Parameter Mapping Issue**: Duration from user input is not being mapped to the generation parameters
3. **Hard-Coded Constraints**: There may be maximum duration limits preventing 5-minute generation
4. **Default Override**: User-specified duration is being overridden by default values

## Proposed Solution

### Solution Overview
Implement an intelligent duration extraction and validation system that:
1. Parses natural language duration requests
2. Converts them to appropriate technical parameters (bars, beats, or seconds)
3. Validates against system constraints
4. Provides clear feedback when requests exceed limits

### Technical Approach

#### 1. Duration Extraction Module
```python
def extract_duration_from_text(user_input: str) -> Optional[DurationRequest]:
    """
    Extract duration information from natural language input.
    
    Supported formats:
    - "5 minutes" → 300 seconds
    - "2 min" → 120 seconds
    - "30 seconds" → 30 seconds
    - "1:30" → 90 seconds (mm:ss format)
    - "16 bars" → calculated based on tempo
    """
    # Implementation details below
```

#### 2. Duration Validation & Conversion
```python
class DurationRequest:
    value: float
    unit: str  # 'seconds', 'minutes', 'bars'
    
    def to_seconds(self, tempo: int = 120, time_signature: tuple = (4, 4)) -> float:
        """Convert any duration format to seconds"""
        
    def to_bars(self, tempo: int = 120, time_signature: tuple = (4, 4)) -> int:
        """Convert any duration format to bars"""
        
    def validate(self, max_duration_seconds: float = 600) -> ValidationResult:
        """Check if duration is within system limits"""
```

#### 3. User Feedback System
When duration requests are processed, provide clear feedback:
- ✅ "Generating 5-minute track (300 seconds, ~100 bars at 120 BPM)"
- ⚠️ "Requested 10 minutes, but system limit is 5 minutes. Generating 5-minute track."
- ❌ "Invalid duration format. Please specify duration like: '5 minutes', '30 seconds', or '16 bars'"

### Implementation Details

#### Regex Patterns for Duration Extraction
```python
import re
from typing import Optional, Tuple

DURATION_PATTERNS = [
    # Minutes: "5 minutes", "5 min", "5mins"
    (r'(\d+(?:\.\d+)?)\s*(?:minutes?|mins?)', 'minutes'),
    
    # Seconds: "30 seconds", "30 sec", "30s"
    (r'(\d+(?:\.\d+)?)\s*(?:seconds?|secs?|s)', 'seconds'),
    
    # MM:SS format: "1:30", "2:45"
    (r'(\d+):(\d+)', 'mm:ss'),
    
    # Bars: "16 bars", "32 bars"
    (r'(\d+)\s*bars?', 'bars'),
]

def parse_duration(text: str) -> Optional[DurationRequest]:
    text = text.lower()
    
    for pattern, unit_type in DURATION_PATTERNS:
        match = re.search(pattern, text)
        if match:
            if unit_type == 'mm:ss':
                minutes = int(match.group(1))
                seconds = int(match.group(2))
                return DurationRequest(
                    value=minutes * 60 + seconds,
                    unit='seconds'
                )
            else:
                value = float(match.group(1))
                return DurationRequest(value=value, unit=unit_type)
    
    return None
```

#### Integration with Generation Pipeline
```python
def generate_midi_with_intent(
    user_prompt: str,
    style: Optional[str] = None,
    tempo: int = 120,
    **kwargs
) -> GeneratedMIDI:
    """
    Enhanced MIDI generation that respects user intent for duration.
    """
    # Extract duration from natural language
    duration_request = parse_duration(user_prompt)
    
    # Convert to appropriate parameters
    if duration_request:
        duration_seconds = duration_request.to_seconds(tempo)
        duration_bars = duration_request.to_bars(tempo)
        
        # Validate against constraints
        validation = duration_request.validate(max_duration_seconds=600)
        
        if not validation.is_valid:
            # Provide clear feedback and use maximum allowed
            duration_seconds = min(duration_seconds, 600)
            duration_bars = calculate_bars_for_seconds(duration_seconds, tempo)
            
        # Override kwargs with extracted duration
        kwargs['duration_seconds'] = duration_seconds
        kwargs['duration_bars'] = duration_bars
    
    # Proceed with generation using updated parameters
    return generate_midi(**kwargs)
```

### Configuration Options

Add system configuration for duration handling:

```python
class DurationConfig:
    # System constraints
    min_duration_seconds: float = 5.0
    max_duration_seconds: float = 600.0  # 10 minutes max
    default_duration_seconds: float = 60.0  # 1 minute default
    
    # Parsing options
    enable_natural_language_parsing: bool = True
    strict_validation: bool = False  # If True, reject out-of-bounds; if False, clamp to limits
    
    # Feedback options
    show_duration_confirmation: bool = True
    show_technical_details: bool = True  # Show bars, beats, etc.
```

## User Stories

### Story 1: Explicit Duration Request
**As a** user creating background music  
**I want to** specify "generate a 5-minute ambient track"  
**So that** the output fits my video length exactly

**Acceptance Criteria**:
- System extracts "5 minutes" from the request
- Generates MIDI file with 300 seconds (±5 seconds) of content
- Confirms to user: "Generating 5-minute track"

### Story 2: Duration in Different Units
**As a** musician familiar with music notation  
**I want to** request "create a 32-bar progression"  
**So that** I get the structure I need for my composition

**Acceptance Criteria**:
- System recognizes "32 bars" and calculates duration based on tempo
- At 120 BPM in 4/4 time, generates 64 seconds of music
- Shows conversion: "Generating 32-bar track (approximately 64 seconds at 120 BPM)"

### Story 3: Exceeding System Limits
**As a** user requesting a long composition  
**I want to** be notified if my request exceeds limits  
**So that** I understand why I'm getting a shorter track

**Acceptance Criteria**:
- User requests "15-minute epic composition"
- System detects 15 minutes exceeds 10-minute limit
- Responds: "Your request exceeds the 10-minute limit. Generating maximum 10-minute track."
- Generates 10-minute (600 second) track

### Story 4: Ambiguous or Missing Duration
**As a** user making a general request  
**I want to** get reasonable default duration  
**So that** I can quickly iterate without specifying every detail

**Acceptance Criteria**:
- User requests "generate a jazz track" (no duration specified)
- System uses default duration (60 seconds)
- Optionally shows: "No duration specified, generating 1-minute track (use '5 minutes' to specify)"

## Technical Constraints

### Current System Limitations
- **Memory/Processing**: Very long MIDI files may consume excessive memory during generation
- **Model Context**: AI model may have difficulty maintaining musical coherence over extended durations
- **Export Size**: MIDI files grow with duration, affecting download/upload times

### Recommended Limits
- **Minimum**: 5 seconds (shorter would be musically incoherent)
- **Maximum**: 600 seconds (10 minutes - balances quality with resource usage)
- **Default**: 60 seconds (1 minute - good for previews and quick iterations)

## Implementation Plan Summary

### Phase 1: Duration Parsing (Priority: High)
- Implement regex-based duration extraction
- Add unit tests for various input formats
- Integrate into main generation pipeline

### Phase 2: Validation & Feedback (Priority: High)
- Add duration validation logic
- Implement user-friendly error messages
- Add duration confirmation in UI/responses

### Phase 3: Configuration & Optimization (Priority: Medium)
- Add configurable duration limits
- Optimize generation for longer durations
- Add progress indicators for long generations

### Phase 4: Advanced Features (Priority: Low)
- Support for section-based duration ("intro: 30 sec, chorus: 45 sec")
- Auto-adjustment based on style (epic styles get longer defaults)
- Learning from user preferences

## Success Metrics

1. **Intent Recognition Rate**: >95% of duration requests correctly parsed
2. **User Satisfaction**: Reduction in duration-related user complaints
3. **Accuracy**: Generated duration within ±5% of requested duration
4. **Error Handling**: 100% of out-of-bounds requests handled gracefully with clear feedback

## Testing Strategy

### Unit Tests
```python
def test_duration_extraction():
    assert parse_duration("5 minutes") == DurationRequest(5, 'minutes')
    assert parse_duration("generate a 2:30 track") == DurationRequest(150, 'seconds')
    assert parse_duration("32 bars") == DurationRequest(32, 'bars')
    assert parse_duration("no duration here") is None

def test_duration_conversion():
    req = DurationRequest(5, 'minutes')
    assert req.to_seconds() == 300
    assert req.to_bars(tempo=120) == 100  # 5 min = 300 sec = 100 bars at 120 BPM
```

### Integration Tests
- Test full generation pipeline with various duration inputs
- Verify actual MIDI file duration matches requested duration
- Test edge cases (very short, very long, invalid formats)

### User Acceptance Tests
- Real-world prompts from users
- Comparison of before/after behavior
- User feedback collection

## Future Enhancements

1. **Smart Duration Suggestions**: Based on style/genre (epic → longer, jingle → shorter)
2. **Multi-Section Support**: "verse: 30s, chorus: 45s, verse: 30s"
3. **BPM-Aware Defaults**: Slower tempo → longer default duration
4. **User Preferences**: Remember user's typical duration preferences
5. **Streaming Generation**: For very long tracks, generate in chunks

## References

- MIDI time calculation formulas
- Music theory: bars, beats, tempo relationships
- Natural language processing for numeric extraction
- User experience best practices for error handling

---

**Next Steps**:
1. Review and approve this specification
2. Create implementation plan with detailed tasks
3. Set up development environment for testing
4. Begin Phase 1 implementation
