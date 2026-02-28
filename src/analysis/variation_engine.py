"""
Variation Engine for MidiGent V2

CRITICAL FIX: This module solves the V1 bug where all generations were identical.
V1 used random.choice() etc. without seeding, resulting in deterministic output.
V2 seeds the RNG with high-resolution timestamp + session ID for uniqueness.
"""

import logging
import time
import random
import hashlib
from typing import List, Any, Optional

logger = logging.getLogger(__name__)


class VariationEngine:
    """
    Ensures every music generation is unique by properly managing randomization.
    
    Key Features:
    - Unique seed per generation (time_ns + session_id + counter)
    - Controlled variation methods
    - Seed tracking for reproducibility
    """
    
    def __init__(self, session_id: str):
        """
        Initialize variation engine for a session.
        
        Args:
            session_id: Unique identifier for this session
        """
        self.session_id = session_id
        self.generation_count = 0
        self.previous_seeds = []
        self.current_seed = None
    
    def initialize_generation(self) -> int:
        """
        Create and apply a unique seed for this generation.
        
        Combines multiple entropy sources to guarantee uniqueness:
        - Nanosecond timestamp (changes every call)
        - Session ID hash (unique per session)
        - Generation counter (unique per generation in session)
        
        Returns:
            The seed value used
        """
        self.generation_count += 1
        
        # Create seed from multiple entropy sources
        timestamp_ns = time.time_ns()  # Nanosecond precision
        session_hash = int(hashlib.md5(self.session_id.encode()).hexdigest()[:8], 16)
        
        # Combine: timestamp + session + counter
        seed = timestamp_ns + session_hash + (self.generation_count * 1000000)
        
        # Apply seed to Python's random module
        random.seed(seed)
        
        # Store for reproducibility (debug mode)
        self.previous_seeds.append(seed)
        self.current_seed = seed
        
        logger.info("🎲 Generation #%d | Seed: %s", self.generation_count, seed)
        
        return seed
    
    def get_variation_factor(self, base_value: float, variance: float = 0.2) -> float:
        """
        Apply controlled randomization to a base value.
        
        Args:
            base_value: Starting value
            variance: Max variation as percentage (0.2 = ±20%)
        
        Returns:
            Randomized value within variance range
            
        Example:
            >>> get_variation_factor(100, 0.1)  # ±10%
            105.3  # Somewhere between 90-110
        """
        variation = random.uniform(-variance, variance)
        return base_value * (1.0 + variation)
    
    def choose_weighted(self, options: List[Any], weights: Optional[List[float]] = None) -> Any:
        """
        Weighted random choice with better distribution than random.choice().
        
        Args:
            options: List of choices
            weights: Optional probability weights (default: equal probability)
        
        Returns:
            One randomly selected option
        
        Example:
            >>> choose_weighted(['a', 'b', 'c'], [0.5, 0.3, 0.2])
            'a'  # 50% chance, 'b' 30% chance, 'c' 20% chance
        """
        if weights is None:
            weights = [1.0] * len(options)
        
        if len(options) != len(weights):
            raise ValueError(f"Options ({len(options)}) and weights ({len(weights)}) must have same length")
        
        return random.choices(options, weights=weights, k=1)[0]
    
    def should_trigger(self, probability: float) -> bool:
        """
        Random boolean decision with specified probability.
        
        Args:
            probability: Chance of returning True (0.0 to 1.0)
        
        Returns:
            True with given probability, False otherwise
        
        Example:
            >>> should_trigger(0.7)  # 70% chance of True
            True
        """
        if not 0.0 <= probability <= 1.0:
            raise ValueError(f"Probability must be 0.0-1.0, got {probability}")
        
        return random.random() < probability
    
    def random_int(self, min_val: int, max_val: int) -> int:
        """Random integer in range [min_val, max_val] inclusive."""
        return random.randint(min_val, max_val)
    
    def random_float(self, min_val: float, max_val: float) -> float:
        """Random float in range [min_val, max_val]."""
        return random.uniform(min_val, max_val)
    
    def random_choice(self, options: List[Any]) -> Any:
        """Random choice from list (uniform distribution)."""
        return random.choice(options)
    
    def shuffle(self, items: List[Any]) -> List[Any]:
        """Return shuffled copy of list."""
        shuffled = items.copy()
        random.shuffle(shuffled)
        return shuffled
    
    def get_seed_info(self) -> dict:
        """
        Get information about current and previous seeds.
        Useful for debugging and reproducibility.
        
        Returns:
            Dict with seed information
        """
        return {
            "current_seed": self.current_seed,
            "generation_count": self.generation_count,
            "previous_seeds": self.previous_seeds[-10:],  # Last 10 seeds
            "session_id": self.session_id
        }
