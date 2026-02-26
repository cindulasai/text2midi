"""
Duration validator and configuration.

Validates duration requests against system constraints and provides
user-friendly confirmation and warning messages.
"""

from typing import Optional
from .duration_models import DurationRequest, ValidationResult, DurationUnit


class DurationConfig:
    """Configuration for duration constraints and behavior."""
    
    # System constraints (in seconds)
    MIN_DURATION_SECONDS: float = 5.0
    MAX_DURATION_SECONDS: float = 600.0  # 10 minutes
    DEFAULT_DURATION_SECONDS: float = 60.0  # 1 minute
    
    # Maximum bars constraint (for MVP)
    MAX_BARS: int = 200  # Approximately 10 minutes at 120 BPM
    
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
                    warning=f"⚠️  Requested {request} is below minimum. Using {config.MIN_DURATION_SECONDS} seconds instead."
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
                    warning=f"⚠️  Requested {request} exceeds {config.MAX_DURATION_SECONDS/60:.0f}-minute limit. Using maximum duration instead."
                )
        
        # Duration is valid
        return ValidationResult(
            is_valid=True,
            message=f"✅ Duration validated: {request} ≈ {duration_seconds:.0f} seconds"
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
        "Generating 5-minute track (300 seconds, ~100 bars at 120 BPM)"
        
        Args:
            request: The duration request
            tempo: Tempo in BPM
            time_signature: Time signature
            
        Returns:
            Formatted confirmation string
        """
        seconds = request.to_seconds(tempo, time_signature)
        bars = request.to_bars(tempo, time_signature)
        
        # Format the primary duration nicely
        if request.unit == DurationUnit.MINUTES:
            if request.value == int(request.value):
                primary = f"{int(request.value)}-minute"
            else:
                primary = f"{request.value:.1f}-minute"
        elif request.unit == DurationUnit.SECONDS:
            primary = f"{int(request.value)}-second"
        elif request.unit == DurationUnit.BARS:
            primary = f"{int(request.value)}-bar"
        else:
            primary = f"{int(seconds)}-second"
        
        # Build confirmation with conversions
        parts = [f"🎵 Generating {primary} track"]
        
        # Add conversions
        conversions = []
        if request.unit != DurationUnit.SECONDS:
            conversions.append(f"{int(seconds)} seconds")
        if request.unit != DurationUnit.BARS:
            conversions.append(f"~{bars} bars")
        
        if conversions:
            parts.append(f"({', '.join(conversions)} at {tempo} BPM)")
        
        return " ".join(parts)
