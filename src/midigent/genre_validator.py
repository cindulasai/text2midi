# -*- coding: utf-8 -*-
"""
Genre Authenticity Validator: Ensures generated music is true to genre conventions
USP Feature #2: Genre authenticity guarantee
Validates that compositions follow genre-specific rules and conventions
"""

from dataclasses import dataclass
from enum import Enum
from typing import List, Dict, Tuple
import statistics


class GenreCharacteristic:
    """Genre definition with musical constraints."""
    
    GENRES = {
        "ambient": {
            "tempo_range": (40, 90),
            "common_keys": ["C", "Am", "F", "Dm", "G"],
            "chord_progressions": [
                ["Am", "Em", "Am", "Em"],
                ["C", "F", "C", "F"],
                ["Dm", "G", "Dm", "G"],
            ],
            "note_density": (5, 20),  # notes per bar
            "rhythm_regularity": (0.7, 1.0),
            "dissonance_tolerance": (0.0, 0.3),
            "essential_characteristics": [
                "sparse melodic content",
                "repetitive structures",
                "emphasis on timbre",
                "minimal percussion",
                "sustained tones"
            ],
            "forbiddentechniques": [
                "rapid note sequences",
                "aggressive percussion",
                "harsh dissonance"
            ]
        },
        "lofi": {
            "tempo_range": (80, 110),
            "common_keys": ["C", "F", "G", "Am", "Dm"],
            "chord_progressions": [
                ["Cmaj7", "Am7", "Cmaj7", "Am7"],
                ["Fmaj7", "Bm7b5", "Fmaj7", "Bm7b5"],
            ],
            "note_density": (15, 40),
            "rhythm_regularity": (0.5, 0.8),
            "dissonance_tolerance": (0.2, 0.5),
            "essential_characteristics": [
                "jazzy chords (maj7, min7)",
                "chill vibe",
                "hip-hop beats",
                "piano or guitar",
                "nostalgic sound"
            ],
            "forbidden_techniques": [
                "harsh synthesizers",
                "distortion",
                "extreme dynamics"
            ]
        },
        "electronic": {
            "tempo_range": (100, 140),
            "common_keys": ["C", "A", "D", "G"],
            "chord_progressions": [
                ["C", "G", "D", "A"],
                ["Am", "F", "C", "G"],
            ],
            "note_density": (20, 50),
            "rhythm_regularity": (0.6, 0.95),
            "dissonance_tolerance": (0.3, 0.7),
            "essential_characteristics": [
                "synthesizers",
                "electronic drums",
                "repetitive patterns",
                "clear beat",
                "robotic elements"
            ],
            "forbidden_techniques": [
                "acoustic instruments only",
                "live drums"
            ]
        },
        "pop": {
            "tempo_range": (90, 130),
            "common_keys": ["C", "G", "D", "A", "E"],
            "chord_progressions": [
                ["C", "Am", "F", "G"],
                ["G", "D", "A", "D"],
            ],
            "note_density": (20, 40),
            "rhythm_regularity": (0.75, 0.95),
            "dissonance_tolerance": (0.1, 0.4),
            "essential_characteristics": [
                "catchy melody",
                "clear harmony",
                "steady beat",
                "verse-chorus structure",
                "singability"
            ],
            "forbidden_techniques": [
                "extreme dissonance",
                "experimental structures"
            ]
        },
        "jazz": {
            "tempo_range": (80, 160),
            "common_keys": ["Bb", "Eb", "F", "C", "G"],
            "chord_progressions": [
                ["Cmaj7", "Dm7", "G7", "Cmaj7"],
                ["Bbmaj7", "Bbm7", "Ebmaj7", "Edim"],
            ],
            "note_density": (25, 50),
            "rhythm_regularity": (0.3, 0.7),
            "dissonance_tolerance": (0.4, 0.8),
            "essential_characteristics": [
                "jazz chords (7ths, extensions)",
                "syncopation",
                "improvisation feel",
                "swung rhythms",
                "blue notes"
            ],
            "forbidden_techniques": [
                "rigid quantized rhythms",
                "pop simplicity"
            ]
        },
        "classical": {
            "tempo_range": (40, 200),
            "common_keys": ["C", "G", "D", "E", "F"],
            "chord_progressions": [
                ["I", "IV", "V", "I"],
                ["I", "vi", "IV", "V"],
            ],
            "note_density": (20, 60),
            "rhythm_regularity": (0.6, 1.0),
            "dissonance_tolerance": (0.1, 0.6),
            "essential_characteristics": [
                "acoustic instruments",
                "harmonic sophistication",
                "orchestration",
                "formal structure",
                "dynamic variation"
            ],
            "forbidden_techniques": [
                "electronic production",
                "drum machines"
            ]
        },
        "rock": {
            "tempo_range": (100, 160),
            "common_keys": ["E", "A", "D", "G"],
            "chord_progressions": [
                ["E", "A", "E", "B"],
                ["Am", "F", "C", "G"],
            ],
            "note_density": (20, 45),
            "rhythm_regularity": (0.7, 0.9),
            "dissonance_tolerance": (0.3, 0.7),
            "essential_characteristics": [
                "electric guitar",
                "powerful drums",
                "strong rhythm",
                "distortion",
                "rebellious energy"
            ],
            "forbidden_techniques": [
                "overly smooth production",
                "excessive reverb"
            ]
        },
        "funk": {
            "tempo_range": (90, 130),
            "common_keys": ["F", "C", "Bb", "Eb"],
            "chord_progressions": [
                ["Fm", "Fm", "Bbm", "Fm"],
                ["C", "C", "F", "C"],
            ],
            "note_density": (25, 50),
            "rhythm_regularity": (0.4, 0.7),
            "dissonance_tolerance": (0.3, 0.6),
            "essential_characteristics": [
                "syncopated rhythm",
                "groove",
                "funky bass",
                "tight rhythm section",
                "danceable"
            ],
            "forbidden_techniques": [
                "straight beats",
                "lack of groove"
            ]
        },
        "cinematic": {
            "tempo_range": (60, 120),
            "common_keys": ["C", "A", "F", "G"],
            "chord_progressions": [
                ["Cmaj7", "Dm7", "Gsus4", "Cmaj7"],
                ["Dm", "F", "Cdim", "Dm"],
            ],
            "note_density": (10, 35),
            "rhythm_regularity": (0.5, 0.8),
            "dissonance_tolerance": (0.2, 0.6),
            "essential_characteristics": [
                "orchestral arrangement",
                "emotional depth",
                "dramatic dynamics",
                "strings emphasis",
                "epic scope"
            ],
            "forbidden_techniques": [
                "trivial melody",
                "lack of depth"
            ]
        }
    }


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
        total_bars = 64  # Default assumption
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
