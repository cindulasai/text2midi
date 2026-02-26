# Implementation Plan: MIDI Track Duration Intent Understanding

**Feature**: Intelligent MIDI Duration Parsing  
**Created**: 2026-01-31  
**Estimated Effort**: 8-12 hours  
**Complexity**: Medium  

## Overview

This plan implements a system to correctly understand and honor user requests for specific MIDI track durations (e.g., "5 minutes length tracks"). The solution involves natural language parsing, parameter validation, and clear user feedback.

## Architecture Changes

### New Components

1. **`duration_parser.py`** - Duration extraction and parsing module
2. **`duration_models.py`** - Data models for duration handling
3. **`duration_validator.py`** - Validation and constraint checking
4. **`duration_config.py`** - Configuration for duration limits and behavior

### Modified Components

1. **Main generation function** - Integrate duration parsing
2. **User interface/prompt handler** - Extract and display duration information
3. **MIDI generation pipeline** - Use extracted duration parameters

## Detailed Implementation Steps

### Phase 1: Core Duration Parsing (3-4 hours)

#### Step 1.1: Create Duration Models
**File**: `src/duration_models.py`

```python
from dataclasses import dataclass
from typing import Literal, Optional
from enum import Enum

class DurationUnit(Enum):
    SECONDS = "seconds"
    MINUTES = "minutes"
    BARS = "bars"
    BEATS = "beats"

@dataclass
class DurationRequest:
    """Represents a parsed duration request from user input."""
    value: float
    unit: DurationUnit
    
    def to_seconds(self, tempo: int = 120, time_signature: tuple = (4, 4)) -> float:
        """Convert duration to seconds based on tempo and time signature."""
        if self.unit == DurationUnit.SECONDS:
            return self.value
        elif self.unit == DurationUnit.MINUTES:
            return self.value * 60
        elif self.unit == DurationUnit.BARS:
            # Calculate beats per bar from time signature
            beats_per_bar = time_signature[0]
            total_beats = self.value * beats_per_bar
            # Calculate seconds from beats and tempo
            seconds_per_beat = 60.0 / tempo
            return total_beats * seconds_per_beat
        elif self.unit == DurationUnit.BEATS:
            seconds_per_beat = 60.0 / tempo
            return self.value * seconds_per_beat
        return self.value
    
    def to_bars(self, tempo: int = 120, time_signature: tuple = (4, 4)) -> int:
        """Convert duration to number of bars."""
        if self.unit == DurationUnit.BARS:
            return int(self.value)
        
        # First convert to seconds
        seconds = self.to_seconds(tempo, time_signature)
        
        # Then convert seconds to bars
        beats_per_bar = time_signature[0]
        seconds_per_beat = 60.0 / tempo
        seconds_per_bar = seconds_per_beat * beats_per_bar
        bars = seconds / seconds_per_bar
        
        return max(1, int(round(bars)))
    
    def __str__(self) -> str:
        return f"{self.value} {self.unit.value}"

@dataclass
class ValidationResult:
    """Result of duration validation."""
    is_valid: bool
    adjusted_value: Optional[float] = None
    message: Optional[str] = None
    warning: Optional[str] = None
```

**Tests to write**:
- Test conversion from minutes to seconds
- Test conversion from bars to seconds at various tempos
- Test conversion to bars at various tempos
- Test edge cases (0, negative, very large values)

#### Step 1.2: Create Duration Parser
**File**: `src/duration_parser.py`

```python
import re
from typing import Optional
from duration_models import DurationRequest, DurationUnit

class DurationParser:
    """Parse duration information from natural language text."""
    
    # Regex patterns for different duration formats
    PATTERNS = [
        # Minutes: "5 minutes", "5 min", "5mins", "5m"
        (r'(\d+(?:\.\d+)?)\s*(?:minutes?|mins?|m)(?:\s|$)', DurationUnit.MINUTES),
        
        # Seconds: "30 seconds", "30 sec", "30s"
        (r'(\d+(?:\.\d+)?)\s*(?:seconds?|secs?|s)(?:\s|$)', DurationUnit.SECONDS),
        
        # MM:SS format: "1:30", "2:45"
        (r'(\d+):(\d{2})', 'mm:ss'),
        
        # Bars: "16 bars", "32 bar", "16-bar"
        (r'(\d+)(?:\s*-?\s*)bars?(?:\s|$)', DurationUnit.BARS),
        
        # Beats: "64 beats", "128 beat"
        (r'(\d+)(?:\s*)beats?(?:\s|$)', DurationUnit.BEATS),
    ]
    
    @classmethod
    def parse(cls, text: str) -> Optional[DurationRequest]:
        """
        Extract duration information from text.
        
        Args:
            text: Natural language input from user
            
        Returns:
            DurationRequest if duration found, None otherwise
            
        Examples:
            >>> DurationParser.parse("generate 5 minutes of music")
            DurationRequest(value=5, unit=DurationUnit.MINUTES)
            
            >>> DurationParser.parse("create a 2:30 track")
            DurationRequest(value=150, unit=DurationUnit.SECONDS)
            
            >>> DurationParser.parse("32 bar progression")
            DurationRequest(value=32, unit=DurationUnit.BARS)
        """
        if not text:
            return None
            
        text = text.lower()
        
        for pattern, unit_type in cls.PATTERNS:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                if unit_type == 'mm:ss':
                    # Special handling for MM:SS format
                    minutes = int(match.group(1))
                    seconds = int(match.group(2))
                    total_seconds = minutes * 60 + seconds
                    return DurationRequest(
                        value=total_seconds,
                        unit=DurationUnit.SECONDS
                    )
                else:
                    # Standard numeric value with unit
                    value = float(match.group(1))
                    return DurationRequest(value=value, unit=unit_type)
        
        return None
    
    @classmethod
    def parse_with_fallback(cls, text: str, default_seconds: float = 60.0) -> DurationRequest:
        """
        Parse duration with fallback to default if not found.
        
        Args:
            text: Natural language input
            default_seconds: Default duration in seconds if none specified
            
        Returns:
            DurationRequest (either parsed or default)
        """
        parsed = cls.parse(text)
        if parsed:
            return parsed
        return DurationRequest(value=default_seconds, unit=DurationUnit.SECONDS)
```

**Tests to write**:
- Test parsing various formats ("5 minutes", "5 min", "5m")
- Test MM:SS format edge cases
- Test case insensitivity
- Test multiple durations in same text (should return first)
- Test no duration found returns None

#### Step 1.3: Create Duration Validator
**File**: `src/duration_validator.py`

```python
from typing import Optional
from duration_models import DurationRequest, ValidationResult

class DurationConfig:
    """Configuration for duration constraints and behavior."""
    
    # System constraints (in seconds)
    MIN_DURATION_SECONDS: float = 5.0
    MAX_DURATION_SECONDS: float = 600.0  # 10 minutes
    DEFAULT_DURATION_SECONDS: float = 60.0  # 1 minute
    
    # Validation behavior
    STRICT_VALIDATION: bool = False  # If True, reject; if False, clamp
    SHOW_WARNINGS: bool = True
    SHOW_CONFIRMATION: bool = True

class DurationValidator:
    """Validate and constrain duration requests."""
    
    @staticmethod
    def validate(
        request: DurationRequest,
        tempo: int = 120,
        time_signature: tuple = (4, 4),
        config: Optional[DurationConfig] = None
    ) -> ValidationResult:
        """
        Validate a duration request against system constraints.
        
        Args:
            request: The duration request to validate
            tempo: Current tempo in BPM
            time_signature: Time signature as (numerator, denominator)
            config: Configuration for validation behavior
            
        Returns:
            ValidationResult with validation status and any adjustments
        """
        if config is None:
            config = DurationConfig()
        
        # Convert to seconds for validation
        duration_seconds = request.to_seconds(tempo, time_signature)
        
        # Check minimum
        if duration_seconds < config.MIN_DURATION_SECONDS:
            if config.STRICT_VALIDATION:
                return ValidationResult(
                    is_valid=False,
                    message=f"Duration {request} is too short. Minimum is {config.MIN_DURATION_SECONDS} seconds."
                )
            else:
                return ValidationResult(
                    is_valid=True,
                    adjusted_value=config.MIN_DURATION_SECONDS,
                    warning=f"Requested duration {request} is below minimum. Using {config.MIN_DURATION_SECONDS} seconds."
                )
        
        # Check maximum
        if duration_seconds > config.MAX_DURATION_SECONDS:
            if config.STRICT_VALIDATION:
                return ValidationResult(
                    is_valid=False,
                    message=f"Duration {request} exceeds maximum of {config.MAX_DURATION_SECONDS} seconds ({config.MAX_DURATION_SECONDS/60:.1f} minutes)."
                )
            else:
                return ValidationResult(
                    is_valid=True,
                    adjusted_value=config.MAX_DURATION_SECONDS,
                    warning=f"Requested duration {request} exceeds maximum. Using {config.MAX_DURATION_SECONDS} seconds ({config.MAX_DURATION_SECONDS/60:.1f} minutes)."
                )
        
        # Duration is valid
        return ValidationResult(
            is_valid=True,
            message=f"Duration validated: {request} = {duration_seconds:.1f} seconds"
        )
    
    @staticmethod
    def format_confirmation(
        request: DurationRequest,
        tempo: int = 120,
        time_signature: tuple = (4, 4)
    ) -> str:
        """
        Create user-friendly confirmation message for duration.
        
        Returns a message like:
        "Generating 5-minute track (300 seconds, approximately 100 bars at 120 BPM)"
        """
        seconds = request.to_seconds(tempo, time_signature)
        bars = request.to_bars(tempo, time_signature)
        
        # Format the primary duration nicely
        if request.unit == DurationUnit.MINUTES:
            primary = f"{request.value:.0f}-minute"
        elif request.unit == DurationUnit.SECONDS:
            primary = f"{request.value:.0f}-second"
        elif request.unit == DurationUnit.BARS:
            primary = f"{request.value:.0f}-bar"
        else:
            primary = f"{seconds:.0f}-second"
        
        # Build confirmation with conversions
        parts = [f"Generating {primary} track"]
        
        # Add conversions
        conversions = []
        if request.unit != DurationUnit.SECONDS:
            conversions.append(f"{seconds:.0f} seconds")
        if request.unit != DurationUnit.BARS:
            conversions.append(f"~{bars} bars at {tempo} BPM")
        
        if conversions:
            parts.append(f"({', '.join(conversions)})")
        
        return " ".join(parts)
```

**Tests to write**:
- Test validation with values below minimum
- Test validation with values above maximum
- Test validation with valid values
- Test strict vs non-strict mode
- Test confirmation message formatting

### Phase 2: Integration (2-3 hours)

#### Step 2.1: Integrate into Generation Pipeline
**File**: `src/midi_generator.py` (or equivalent)

```python
from duration_parser import DurationParser
from duration_validator import DurationValidator, DurationConfig
from typing import Optional

def generate_midi_with_intent(
    user_prompt: str,
    style: Optional[str] = None,
    tempo: int = 120,
    time_signature: tuple = (4, 4),
    duration_seconds: Optional[float] = None,
    duration_bars: Optional[int] = None,
    **kwargs
):
    """
    Enhanced MIDI generation that extracts and respects duration from user intent.
    
    Args:
        user_prompt: Natural language request from user
        style: Musical style/genre
        tempo: Tempo in BPM
        time_signature: Time signature as (numerator, denominator)
        duration_seconds: Explicit duration in seconds (overrides prompt)
        duration_bars: Explicit duration in bars (overrides prompt)
        **kwargs: Additional generation parameters
        
    Returns:
        Generated MIDI data with metadata
    """
    config = DurationConfig()
    
    # Step 1: Determine duration source
    if duration_seconds is not None or duration_bars is not None:
        # Explicit parameters take precedence
        if duration_seconds is not None:
            duration_request = DurationRequest(duration_seconds, DurationUnit.SECONDS)
        else:
            duration_request = DurationRequest(duration_bars, DurationUnit.BARS)
    else:
        # Extract from natural language prompt
        duration_request = DurationParser.parse_with_fallback(
            user_prompt,
            default_seconds=config.DEFAULT_DURATION_SECONDS
        )
    
    # Step 2: Validate duration
    validation = DurationValidator.validate(
        duration_request,
        tempo=tempo,
        time_signature=time_signature,
        config=config
    )
    
    # Step 3: Apply validation results
    if not validation.is_valid:
        raise ValueError(validation.message)
    
    if validation.adjusted_value is not None:
        # Duration was clamped to limits
        if validation.warning and config.SHOW_WARNINGS:
            print(f"⚠️  {validation.warning}")
        final_seconds = validation.adjusted_value
    else:
        final_seconds = duration_request.to_seconds(tempo, time_signature)
    
    # Step 4: Show confirmation
    if config.SHOW_CONFIRMATION:
        confirmation = DurationValidator.format_confirmation(
            duration_request,
            tempo=tempo,
            time_signature=time_signature
        )
        print(f"✅ {confirmation}")
    
    # Step 5: Convert to bars for generation
    final_bars = duration_request.to_bars(tempo, time_signature)
    
    # Step 6: Call actual generation function with calculated parameters
    return _generate_midi_internal(
        prompt=user_prompt,
        style=style,
        tempo=tempo,
        time_signature=time_signature,
        duration_seconds=final_seconds,
        duration_bars=final_bars,
        **kwargs
    )
```

#### Step 2.2: Update UI/CLI Integration
**File**: `src/ui_handler.py` or CLI entry point

```python
# If using Gradio or similar UI framework
def create_ui():
    with gr.Blocks() as demo:
        with gr.Row():
            prompt_input = gr.Textbox(
                label="Describe your music",
                placeholder="E.g., 'Generate a 5-minute ambient track' or 'Create a 32-bar jazz progression'",
                lines=3
            )
        
        # Duration can still be manually specified
        with gr.Row():
            duration_input = gr.Slider(
                minimum=5,
                maximum=600,
                value=None,  # None means "extract from prompt"
                label="Duration (seconds) - Leave empty to extract from prompt",
                info="Or specify duration in your prompt (e.g., '5 minutes', '32 bars')"
            )
        
        # ... rest of UI
        
        generate_button.click(
            fn=generate_midi_with_intent,
            inputs=[prompt_input, style_input, tempo_input, duration_input],
            outputs=[audio_output, midi_file, status_text]
        )
```

### Phase 3: Testing & Refinement (2-3 hours)

#### Step 3.1: Unit Tests
**File**: `tests/test_duration_parser.py`

```python
import pytest
from duration_parser import DurationParser
from duration_models import DurationRequest, DurationUnit

class TestDurationParser:
    
    def test_parse_minutes_full_word(self):
        result = DurationParser.parse("generate 5 minutes of music")
        assert result is not None
        assert result.value == 5
        assert result.unit == DurationUnit.MINUTES
    
    def test_parse_minutes_abbreviated(self):
        result = DurationParser.parse("create 2 min track")
        assert result.value == 2
        assert result.unit == DurationUnit.MINUTES
    
    def test_parse_seconds(self):
        result = DurationParser.parse("30 seconds long")
        assert result.value == 30
        assert result.unit == DurationUnit.SECONDS
    
    def test_parse_mmss_format(self):
        result = DurationParser.parse("make it 2:30")
        assert result.value == 150  # 2*60 + 30
        assert result.unit == DurationUnit.SECONDS
    
    def test_parse_bars(self):
        result = DurationParser.parse("32 bars please")
        assert result.value == 32
        assert result.unit == DurationUnit.BARS
    
    def test_parse_no_duration(self):
        result = DurationParser.parse("jazz music")
        assert result is None
    
    def test_parse_with_fallback(self):
        result = DurationParser.parse_with_fallback("jazz music", default_seconds=90)
        assert result.value == 90
        assert result.unit == DurationUnit.SECONDS
    
    def test_case_insensitive(self):
        result = DurationParser.parse("Generate 5 MINUTES")
        assert result.value == 5
        assert result.unit == DurationUnit.MINUTES
```

**File**: `tests/test_duration_models.py`

```python
import pytest
from duration_models import DurationRequest, DurationUnit

class TestDurationRequest:
    
    def test_minutes_to_seconds(self):
        req = DurationRequest(5, DurationUnit.MINUTES)
        assert req.to_seconds() == 300
    
    def test_bars_to_seconds_120bpm(self):
        req = DurationRequest(32, DurationUnit.BARS)
        # At 120 BPM, 4/4 time: 32 bars = 128 beats = 64 seconds
        assert req.to_seconds(tempo=120, time_signature=(4, 4)) == 64
    
    def test_bars_to_seconds_60bpm(self):
        req = DurationRequest(16, DurationUnit.BARS)
        # At 60 BPM, 4/4 time: 16 bars = 64 beats = 64 seconds
        assert req.to_seconds(tempo=60, time_signature=(4, 4)) == 64
    
    def test_seconds_to_bars(self):
        req = DurationRequest(300, DurationUnit.SECONDS)
        # At 120 BPM, 4/4 time: 300 seconds = 600 beats = 150 bars
        assert req.to_bars(tempo=120, time_signature=(4, 4)) == 150
```

**File**: `tests/test_duration_validator.py`

```python
import pytest
from duration_validator import DurationValidator, DurationConfig
from duration_models import DurationRequest, DurationUnit

class TestDurationValidator:
    
    def test_valid_duration(self):
        req = DurationRequest(60, DurationUnit.SECONDS)
        result = DurationValidator.validate(req)
        assert result.is_valid
        assert result.adjusted_value is None
    
    def test_too_short_non_strict(self):
        config = DurationConfig()
        config.STRICT_VALIDATION = False
        req = DurationRequest(2, DurationUnit.SECONDS)
        result = DurationValidator.validate(req, config=config)
        assert result.is_valid
        assert result.adjusted_value == config.MIN_DURATION_SECONDS
        assert result.warning is not None
    
    def test_too_long_non_strict(self):
        config = DurationConfig()
        config.STRICT_VALIDATION = False
        req = DurationRequest(15, DurationUnit.MINUTES)
        result = DurationValidator.validate(req, config=config)
        assert result.is_valid
        assert result.adjusted_value == config.MAX_DURATION_SECONDS
    
    def test_confirmation_message_format(self):
        req = DurationRequest(5, DurationUnit.MINUTES)
        msg = DurationValidator.format_confirmation(req, tempo=120)
        assert "5-minute" in msg
        assert "300 seconds" in msg
        assert "100 bars" in msg
```

#### Step 3.2: Integration Tests
**File**: `tests/test_integration.py`

```python
import pytest
from midi_generator import generate_midi_with_intent

class TestMIDIGenerationIntegration:
    
    def test_generate_with_minute_request(self):
        result = generate_midi_with_intent(
            user_prompt="Create a 5-minute ambient track",
            style="ambient",
            tempo=90
        )
        # Verify duration is approximately 300 seconds
        assert 295 <= result.duration_seconds <= 305
    
    def test_generate_with_bar_request(self):
        result = generate_midi_with_intent(
            user_prompt="32 bar jazz progression",
            style="jazz",
            tempo=120
        )
        # Verify bar count
        assert result.duration_bars == 32
    
    def test_generate_exceeds_max(self):
        result = generate_midi_with_intent(
            user_prompt="15 minute epic",
            tempo=120
        )
        # Should be clamped to max (600 seconds)
        assert result.duration_seconds == 600
    
    def test_generate_no_duration_uses_default(self):
        result = generate_midi_with_intent(
            user_prompt="jazz music",
            tempo=120
        )
        # Should use default (60 seconds)
        assert result.duration_seconds == 60
```

#### Step 3.3: Manual Testing Checklist
Create a test script or checklist:

```python
# Manual test cases
TEST_PROMPTS = [
    ("Generate 5 minutes of ambient music", 300),
    ("Create a 2:30 track", 150),
    ("Make 32 bars of jazz", 64),  # at 120 BPM
    ("Epic 10 minute composition", 600),  # max limit
    ("15 minute symphony", 600),  # should clamp to max
    ("Quick jingle", 60),  # should use default
    ("30 second intro", 30),
    ("1 min loop", 60),
]

for prompt, expected_seconds in TEST_PROMPTS:
    print(f"\nTesting: {prompt}")
    result = generate_midi_with_intent(prompt, tempo=120)
    print(f"Expected: {expected_seconds}s, Got: {result.duration_seconds}s")
    assert abs(result.duration_seconds - expected_seconds) < 5
```

### Phase 4: Documentation (1-2 hours)

#### Step 4.1: User Documentation
**File**: `docs/duration-feature.md`

```markdown
# Specifying Track Duration

You can specify the duration of generated MIDI tracks in several ways:

## Natural Language (Recommended)

Simply include the duration in your request:

- "Generate a **5-minute** ambient track"
- "Create **2:30** of jazz music"  
- "Make a **32-bar** progression"
- "Quick **30 second** jingle"

## Supported Formats

| Format | Example | Result |
|--------|---------|--------|
| Minutes | "5 minutes", "5 min", "5m" | 300 seconds |
| Seconds | "30 seconds", "30 sec", "30s" | 30 seconds |
| MM:SS | "2:30", "1:45" | 150, 105 seconds |
| Bars | "32 bars", "16 bar" | Depends on tempo |

## System Limits

- **Minimum**: 5 seconds
- **Maximum**: 10 minutes (600 seconds)
- **Default**: 1 minute (when not specified)

If you request a duration outside these limits, the system will automatically adjust and notify you.

## Examples

✅ **Good requests:**
- "5 minute lo-fi hip hop track"
- "Create a 16-bar blues progression"
- "2:30 upbeat pop song"

⚠️ **Out of bounds:**
- "15 minute symphony" → Generates 10 minutes (max limit)
- "2 second blip" → Generates 5 seconds (min limit)

## Tips

- Longer durations work best with ambient/atmospheric styles
- For complex compositions, 2-3 minutes is optimal
- Use bars when you need specific musical structure
```

#### Step 4.2: Developer Documentation
Add docstrings and inline comments throughout the code (already included above).

#### Step 4.3: Update Changelog
**File**: `CHANGELOG.md`

```markdown
## [Unreleased]

### Added
- **Duration Intent Understanding**: System now parses and honors duration requests from natural language
  - Supports minutes, seconds, MM:SS format, and bars
  - Automatic validation with configurable min/max limits
  - Clear feedback when duration adjusted or out of bounds
  - Improved user experience with confirmation messages

### Changed
- MIDI generation pipeline now extracts duration from user prompts automatically
- Default duration handling now more intelligent and user-friendly

### Fixed
- Issue where requested track durations (e.g., "5 minutes") were ignored
```

## Risk Analysis & Mitigation

### Risk 1: Parsing False Positives
**Impact**: Medium  
**Probability**: Low  
**Mitigation**: 
- Use specific regex patterns with word boundaries
- Test with large set of real user prompts
- Allow manual duration override

### Risk 2: Performance with Long Durations
**Impact**: Medium  
**Probability**: Medium  
**Mitigation**:
- Set reasonable maximum (10 minutes)
- Add progress indicators for long generations
- Consider chunked generation for very long tracks

### Risk 3: User Confusion About Limits
**Impact**: Low  
**Probability**: Medium  
**Mitigation**:
- Clear messaging when limits reached
- Show conversions (e.g., "5 min = 300 sec = ~100 bars")
- Document limits in user-facing documentation

## Rollout Strategy

1. **Development**: Implement core parsing and validation
2. **Internal Testing**: Test with variety of prompts
3. **Beta Release**: Deploy to subset of users, collect feedback
4. **Full Release**: Roll out to all users with documentation
5. **Monitor**: Track usage patterns and error rates

## Success Criteria

- [ ] 95%+ of duration requests correctly parsed
- [ ] All out-of-bounds requests handled gracefully
- [ ] User satisfaction scores improve
- [ ] Zero crashes related to duration handling
- [ ] Documentation complete and clear

## Timeline

| Phase | Duration | Dependencies |
|-------|----------|--------------|
| Phase 1: Core Parsing | 3-4 hours | None |
| Phase 2: Integration | 2-3 hours | Phase 1 complete |
| Phase 3: Testing | 2-3 hours | Phase 2 complete |
| Phase 4: Documentation | 1-2 hours | Phase 3 complete |
| **Total** | **8-12 hours** | |

## Next Steps

1. ✅ Review and approve this implementation plan
2. Set up development environment
3. Create git branch: `feature/duration-intent-parsing`
4. Begin Phase 1 implementation
5. Write tests alongside implementation
6. Code review before merge
7. Deploy to staging environment
8. User acceptance testing
9. Production deployment

---

**Questions or Concerns?**
Contact the development team before beginning implementation.
