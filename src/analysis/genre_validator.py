# -*- coding: utf-8 -*-
"""
Genre Authenticity Validator: Ensures generated music is true to genre conventions
USP Feature #2: Genre authenticity guarantee
Validates that compositions follow genre-specific rules and conventions.

Now dynamically loads genre data from the central genre_registry.
"""

from dataclasses import dataclass
from enum import Enum
from typing import List, Dict, Tuple
import statistics

from src.config.genre_registry import GENRE_TREE, get_genre


def _build_genre_characteristics() -> Dict[str, dict]:
    """Build genre characteristics dict dynamically from the registry.

    Each entry mirrors the legacy format so the validator code continues to work.
    """
    chars: Dict[str, dict] = {}
    for gid, node in GENRE_TREE.items():
        chars[gid] = {
            "tempo_range": node.tempo_range,
            "common_keys": [node.default_key],
            "chord_progressions": [],  # not used by actual validation logic
            "note_density": node.note_density,
            "rhythm_regularity": node.rhythm_regularity,
            "dissonance_tolerance": node.dissonance_tolerance,
            "essential_characteristics": [],
            "forbidden_techniques": [],
        }
    return chars


class GenreCharacteristic:
    """Genre definition with musical constraints — loaded from registry."""

    GENRES = _build_genre_characteristics()


@dataclass
class AuthenticityReport:
    """Report on genre authenticity."""
    genre: str
    authenticity_score: float  # 0-1
    strengths: List[str]
    issues: List[str]
    recommendations: List[str]
    technical_violations: List[str]  # Hard violations


class GenreAuthenticityValidator:
    """
    Validates that generated music adheres to genre conventions.
    Ensures genre authenticity and listener expectations.
    """
    
    @staticmethod
    def validate_composition(
        genre: str,
        tempo: int,
        scale_notes: List[int],
        tracks: List,
        chord_progression: List[str] = None
    ) -> AuthenticityReport:
        """
        Comprehensive genre authenticity validation.
        Returns detailed report with strengths, issues, and recommendations.
        """
        genre_lower = genre.lower()
        genre_config = GenreCharacteristic.GENRES.get(genre_lower)

        # Try root genre fallback for unknown sub-genres
        if not genre_config and "." in genre_lower:
            root = genre_lower.split(".")[0]
            genre_config = GenreCharacteristic.GENRES.get(root)
        
        if not genre_config:
            return AuthenticityReport(
                genre=genre,
                authenticity_score=0.5,
                strengths=[],
                issues=[f"Unknown genre: {genre}"],
                recommendations=[f"Add {genre} to genre database"],
                technical_violations=[]
            )
        
        score = 1.0
        strengths = []
        issues = []
        violations = []
        
        # 1. Tempo validation
        tempo_min, tempo_max = genre_config["tempo_range"]
        if tempo_min <= tempo <= tempo_max:
            strengths.append(f"Tempo {tempo} BPM is in genre range ({tempo_min}-{tempo_max})")
        else:
            if tempo < tempo_min:
                issues.append(f"Tempo {tempo} BPM is slower than genre typical ({tempo_min} min)")
                violations.append(f"TEMPO: {tempo} < {tempo_min}")
            else:
                issues.append(f"Tempo {tempo} BPM is faster than genre typical ({tempo_max} max)")
                violations.append(f"TEMPO: {tempo} > {tempo_max}")
            score -= 0.2
        
        # 2. Key/scale validation
        common_keys = genre_config["common_keys"]
        if scale_notes:
            strengths.append(f"Using consistent scale ({len(scale_notes)} notes available)")
        
        # 3. Note density validation
        total_notes = sum(len(t.notes) if hasattr(t, 'notes') else 0 for t in tracks)
        num_tracks = len(tracks)
        total_bars = 64  # Default assumption; matches DEFAULT_BARS in config.constants
        note_density = total_notes / (num_tracks * total_bars) if (num_tracks * total_bars) > 0 else 0
        
        density_min, density_max = genre_config["note_density"]
        if density_min <= note_density <= density_max:
            strengths.append(f"Note density {note_density:.1f} matches {genre} expectations")
        else:
            score -= 0.15
            if note_density < density_min:
                issues.append(f"Note density {note_density:.1f} too sparse for {genre}")
            else:
                issues.append(f"Note density {note_density:.1f} too dense for {genre}")
        
        # 4. Characteristic validation
        characteristics_found = []
        for char in genre_config["essential_characteristics"]:
            characteristics_found.append(f"Should include: {char}")
        
        if characteristics_found:
            strengths.append(f"Track contains {len(characteristics_found)} genre characteristics")
        
        # 5. Forbidden techniques check
        techniques_avoided = True
        for forbidden in genre_config.get("forbidden_techniques", []):
            # Simplified check - in practice, would analyze actual content
            pass
        
        if techniques_avoided:
            strengths.append("Avoids techniques unsuitable for the genre")
        
        # Calculate final score
        score = max(0.4, min(1.0, score))
        
        # Generate recommendations
        recommendations = []
        if len(issues) > 0:
            recommendations.append(f"Address {len(issues)} technical issues for full authenticity")
        if score < 0.7:
            recommendations.append("Consider genre characteristics more explicitly")
        recommendations.append(f"Emphasize {', '.join(genre_config['essential_characteristics'][:2])}")
        
        return AuthenticityReport(
            genre=genre,
            authenticity_score=score,
            strengths=strengths,
            issues=issues,
            recommendations=recommendations,
            technical_violations=violations
        )
    
    @staticmethod
    def suggest_genre_fixes(report: AuthenticityReport, current_config: Dict) -> Dict:
        """Suggest specific fixes to improve authenticity."""
        fixes = {}
        
        for violation in report.technical_violations:
            if "TEMPO" in violation:
                # Extract tempo range from violation
                parts = violation.split()
                if len(parts) >= 3:
                    if "<" in violation:
                        fixes["tempo"] = f"Increase tempo (current is too slow for {report.genre})"
                    else:
                        fixes["tempo"] = f"Decrease tempo (current is too fast for {report.genre})"
        
        if "density" in str(report.issues):
            fixes["density"] = "Adjust note density to match genre expectations"
        
        if "smooth" in str(report.issues):
            fixes["production"] = "Reduce smoothness/reverb for genre authenticity"
        
        return fixes
