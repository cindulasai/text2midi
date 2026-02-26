"""
Duration models for MIDI generation.

Handles duration requests in various formats (minutes, seconds, bars, beats)
with conversion and validation capabilities.
"""

from dataclasses import dataclass
from typing import Optional
from enum import Enum


class DurationUnit(Enum):
    """Units for specifying duration."""
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
        """
        Convert duration to seconds based on tempo and time signature.
        
        Args:
            tempo: Tempo in BPM (beats per minute)
            time_signature: Time signature as (numerator, denominator)
            
        Returns:
            Duration in seconds
        """
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
        """
        Convert duration to number of bars.
        
        Args:
            tempo: Tempo in BPM
            time_signature: Time signature as (numerator, denominator)
            
        Returns:
            Number of bars (rounded to nearest integer, minimum 1)
        """
        if self.unit == DurationUnit.BARS:
            return max(1, int(self.value))
        
        # First convert to seconds
        seconds = self.to_seconds(tempo, time_signature)
        
        # Then convert seconds to bars
        beats_per_bar = time_signature[0]
        seconds_per_beat = 60.0 / tempo
        seconds_per_bar = seconds_per_beat * beats_per_bar
        bars = seconds / seconds_per_bar
        
        return max(1, int(round(bars)))
    
    def __str__(self) -> str:
        """String representation for display."""
        return f"{self.value} {self.unit.value}"


@dataclass
class ValidationResult:
    """Result of duration validation."""
    is_valid: bool
    adjusted_value: Optional[float] = None
    message: Optional[str] = None
    warning: Optional[str] = None
