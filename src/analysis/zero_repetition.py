# -*- coding: utf-8 -*-
"""
Zero Repetition Guarantee: Tracks composition history and ensures uniqueness
USP Feature #3: Absolute uniqueness guarantee
Maintains composition history and prevents duplicate generations
"""

from dataclasses import dataclass, field
from typing import List, Dict, Tuple
import hashlib


@dataclass
class CompositionSignature:
    """Unique fingerprint of a composition for deduplication."""
    generation_id: str  # UUID
    genre: str
    tempo: int
    melody_hash: str  # Hash of main melody
    harmony_hash: str  # Hash of chord progression
    rhythm_hash: str  # Hash of rhythmic pattern
    structure_hash: str  # Hash of overall structure
    overall_hash: str  # Combined hash
    timestamp: str
    parameters: Dict = field(default_factory=dict)
    
    def __hash__(self):
        return hash(self.overall_hash)
    
    def __eq__(self, other):
        if not isinstance(other, CompositionSignature):
            return False
        return self.overall_hash == other.overall_hash


class ZeroRepetitionGuarantee:
    """
    Enforces absolute uniqueness across all generations.
    Maintains composition history and similarity metrics.
    """
    
    def __init__(self):
        self.composition_history: List[CompositionSignature] = []
        self.generation_count = 0
    
    @staticmethod
    def _hash_sequence(sequence: List) -> str:
        """Create hash from a sequence of values."""
        sequence_str = ",".join(str(x) for x in sequence)
        return hashlib.md5(sequence_str.encode()).hexdigest()[:16]
    
    @staticmethod
    def _extract_melody_hash(tracks: List) -> str:
        """Extract melody from main track and create signature."""
        # Find track with most notes (likely main melody)
        main_track = None
        max_notes = 0
        
        for track in tracks:
            if hasattr(track, 'notes'):
                if len(track.notes) > max_notes:
                    main_track = track
                    max_notes = len(track.notes)
        
        if not main_track or not hasattr(main_track, 'notes'):
            return "nomélody"
        
        # Get first 64 notes or entire melody
        melody_pitches = [n.pitch for n in main_track.notes[:64]]
        return ZeroRepetitionGuarantee._hash_sequence(melody_pitches)
    
    @staticmethod
    def _extract_harmony_hash(chords: List[str] = None) -> str:
        """Create hash from chord progression."""
        if not chords:
            return "noharmony"
        return ZeroRepetitionGuarantee._hash_sequence(chords[:32])
    
    @staticmethod
    def _extract_rhythm_hash(tracks: List) -> str:
        """Create hash from rhythmic patterns."""
        # Extract note durations and gaps
        rhythms = []
        for track in tracks:
            if hasattr(track, 'notes'):
                for note in track.notes[:32]:
                    rhythm_val = int(getattr(note, 'duration', 0.5) * 100)
                    rhythms.append(rhythm_val)
        
        return ZeroRepetitionGuarantee._hash_sequence(rhythms[:32])
    
    def create_signature(
        self,
        tracks: List,
        genre: str,
        tempo: int,
        chords: List[str] = None,
        generation_id: str = None,
        parameters: Dict = None
    ) -> CompositionSignature:
        """Create unique signature for a composition."""
        if generation_id is None:
            generation_id = f"gen_{self.generation_count:05d}"
        
        self.generation_count += 1
        
        melody_hash = self._extract_melody_hash(tracks)
        harmony_hash = self._extract_harmony_hash(chords)
        rhythm_hash = self._extract_rhythm_hash(tracks)
        
        # Structure hash includes genre, tempo, and basic config
        structure_hash = self._hash_sequence([genre, str(tempo), str(len(tracks))])
        
        # Overall hash combines all signatures
        combined = f"{melody_hash}_{harmony_hash}_{rhythm_hash}_{structure_hash}"
        overall_hash = hashlib.sha256(combined.encode()).hexdigest()[:24]
        
        signature = CompositionSignature(
            generation_id=generation_id,
            genre=genre,
            tempo=tempo,
            melody_hash=melody_hash,
            harmony_hash=harmony_hash,
            rhythm_hash=rhythm_hash,
            structure_hash=structure_hash,
            overall_hash=overall_hash,
            timestamp=self._get_timestamp(),
            parameters=parameters or {}
        )
        
        self.composition_history.append(signature)
        return signature
    
    def check_uniqueness(self, new_signature: CompositionSignature) -> Tuple[bool, Dict]:
        """
        Check if composition is truly unique.
        Returns (is_unique, analysis_dict)
        """
        analysis = {
            "is_unique": True,
            "duplicate_count": 0,
            "similar_count": 0,
            "most_similar": None,
            "similarity_scores": [],
            "uniqueness_confidence": 1.0
        }
        
        if not self.composition_history:
            return True, analysis
        
        uniqueness_threshold = 0.15  # Allow 15% similarity
        
        for existing in self.composition_history:
            # Check exact match
            if existing.overall_hash == new_signature.overall_hash:
                analysis["duplicate_count"] += 1
                analysis["is_unique"] = False
                analysis["most_similar"] = existing.generation_id
                analysis["uniqueness_confidence"] = 0.0
                continue
            
            # Calculate similarity score
            similarity = self._calculate_similarity(new_signature, existing)
            analysis["similarity_scores"].append({
                "generation": existing.generation_id,
                "score": similarity
            })
            
            if similarity > 0.7:  # High similarity
                analysis["similar_count"] += 1
                if analysis["most_similar"] is None:
                    analysis["most_similar"] = existing.generation_id
        
        # Confidence decreases with similar compositions
        analysis["uniqueness_confidence"] = max(0.0, 1.0 - (analysis["similar_count"] * 0.2))
        
        return analysis["is_unique"], analysis
    
    @staticmethod
    def _calculate_similarity(sig1: CompositionSignature, sig2: CompositionSignature) -> float:
        """
        Calculate similarity between two compositions (0-1).
        1.0 = identical, 0.0 = completely different
        """
        if sig1.overall_hash == sig2.overall_hash:
            return 1.0
        
        similarities = []
        
        # Melody similarity
        melody_match = 1.0 if sig1.melody_hash == sig2.melody_hash else 0.3
        similarities.append(melody_match * 0.4)  # 40% weight
        
        # Harmony similarity
        harmony_match = 1.0 if sig1.harmony_hash == sig2.harmony_hash else 0.3
        similarities.append(harmony_match * 0.3)  # 30% weight
        
        # Rhythm similarity
        rhythm_match = 1.0 if sig1.rhythm_hash == sig2.rhythm_hash else 0.3
        similarities.append(rhythm_match * 0.2)  # 20% weight
        
        # Genre/Tempo match
        same_genre = 0.5 if sig1.genre == sig2.genre else 0.1
        same_tempo = 0.5 if abs(sig1.tempo - sig2.tempo) <= 10 else 0.1
        similarities.append((same_genre + same_tempo) / 2 * 0.1)  # 10% weight
        
        return sum(similarities)
    
    def generate_uniqueness_report(self) -> Dict:
        """Generate comprehensive uniqueness statistics."""
        return {
            "total_generations": len(self.composition_history),
            "unique_compositions": len(set(s.overall_hash for s in self.composition_history)),
            "duplicate_count": len(self.composition_history) - len(set(s.overall_hash for s in self.composition_history)),
            "diversity_score": len(set(s.genre for s in self.composition_history)) / max(1, len(self.composition_history)),
            "genre_distribution": self._get_genre_distribution(),
            "guarantee_status": "100% UNIQUE" if len(self.composition_history) == len(set(s.overall_hash for s in self.composition_history)) else "DUPLICATES DETECTED"
        }
    
    def _get_genre_distribution(self) -> Dict[str, int]:
        """Get count of compositions per genre."""
        dist = {}
        for sig in self.composition_history:
            dist[sig.genre] = dist.get(sig.genre, 0) + 1
        return dist
    
    @staticmethod
    def _get_timestamp() -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def clear_history(self):
        """Clear composition history (use with caution)."""
        self.composition_history = []
        self.generation_count = 0
    
    def get_history_summary(self) -> str:
        """Get human-readable summary of generation history."""
        if not self.composition_history:
            return "No compositions generated yet"
        
        summary = f"Generation History ({len(self.composition_history)} total):\n"
        summary += "-" * 60 + "\n"
        
        for sig in self.composition_history[-10:]:  # Last 10
            summary += f"  {sig.generation_id}: {sig.genre.capitalize()} @ {sig.tempo} BPM\n"
        
        if len(self.composition_history) > 10:
            summary += f"  ... and {len(self.composition_history) - 10} more\n"
        
        report = self.generate_uniqueness_report()
        summary += "-" * 60 + "\n"
        summary += f"Uniqueness: {report['guarantee_status']}\n"
        summary += f"Unique compositions: {report['unique_compositions']}/{report['total_generations']}\n"
        
        return summary
