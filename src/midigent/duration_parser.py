"""
Duration parser for extracting duration information from natural language.

Supports multiple formats:
- Minutes: "5 minutes", "5 min", "5m"
- Seconds: "30 seconds", "30 sec", "30s"
- MM:SS format: "2:30", "1:45"
- Bars: "32 bars", "16 bar"
- Beats: "64 beats"
"""

import re
from typing import Optional
from .duration_models import DurationRequest, DurationUnit


class DurationParser:
    """Parse duration information from natural language text."""
    
    # Regex patterns for different duration formats
    # Order matters - more specific patterns first
    PATTERNS = [
        # MM:SS format: "1:30", "2:45" (must come before minutes pattern)
        (r'(\d+):(\d{2})', 'mm:ss'),
        
        # Minutes: "5 minutes", "5 min", "5mins", "5 m" (but not 5:30)
        (r'(\d+(?:\.\d+)?)\s*(?:minutes?|mins?)\b', DurationUnit.MINUTES),
        
        # Bars: "16 bars", "32 bar", "16-bar"
        (r'(\d+)(?:\s*-?\s*)?bars?\b', DurationUnit.BARS),
        
        # Seconds: "30 seconds", "30 sec", "30s"
        (r'(\d+(?:\.\d+)?)\s*(?:seconds?|secs?|s)\b', DurationUnit.SECONDS),
        
        # Beats: "64 beats", "128 beat"
        (r'(\d+)\s*beats?\b', DurationUnit.BEATS),
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
