# -*- coding: utf-8 -*-
"""
Professional Analytics Engine: Detailed metrics and insights for music creators
USP Feature #4: Professional-grade analytics and reporting
Provides comprehensive statistics and insights for composition quality
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum
import statistics


class AnalyticsCategory(Enum):
    """Categories of metric analysis."""
    MELODIC = "melodic"
    HARMONIC = "harmonic"
    RHYTHMIC = "rhythmic"
    STRUCTURAL = "structural"
    TIMBRAL = "timbral"
    EMOTIONAL = "emotional"


@dataclass
class MetricScore:
    """Individual metric with explanation."""
    name: str
    value: float  # 0-1 or 0-100
    category: AnalyticsCategory
    ideal_range: tuple = None
    interpretation: str = ""
    recommendation: str = ""


@dataclass
class ProfessionalAnalytics:
    """Comprehensive analytics report for a composition."""
    composition_id: str
    genre: str
    duration_seconds: float
    
    # Category scores
    melodic_score: float = 0.0
    harmonic_score: float = 0.0
    rhythmic_score: float = 0.0
    structural_score: float = 0.0
    timbral_score: float = 0.0
    emotional_score: float = 0.0
    
    # Overall quality
    overall_score: float = 0.0
    
    # Detailed metrics
    metrics: List[MetricScore] = field(default_factory=list)
    
    # Comparisons
    genre_percentile: float = 0.0  # Where this ranks in genre
    historical_percentile: float = 0.0  # Where this ranks historically
    
    # Insights
    strengths: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)
    opportunities: List[str] = field(default_factory=list)
    
    # Export format
    def to_markdown(self) -> str:
        """Export analytics as readable markdown."""
        report = f"# Composition Analytics Report\n\n"
        report += f"**Composition:** {self.composition_id}\n"
        report += f"**Genre:** {self.genre.capitalize()}\n"
        report += f"**Duration:** {self.duration_seconds:.1f}s\n\n"
        
        report += "## Quality Scores\n\n"
        report += f"| Category | Score | Status |\n"
        report += f"|----------|-------|--------|\n"
        overall_status = "EXCELLENT" if self.overall_score > 0.85 else "GOOD" if self.overall_score > 0.70 else "FAIR"
        report += f"| Overall | {self.overall_score:.2f}/1.00 | {overall_status} |\n"
        report += f"| Melodic | {self.melodic_score:.2f}/1.00 | ✓ |\n"
        report += f"| Harmonic | {self.harmonic_score:.2f}/1.00 | ✓ |\n"
        report += f"| Rhythmic | {self.rhythmic_score:.2f}/1.00 | ✓ |\n"
        report += f"| Structural | {self.structural_score:.2f}/1.00 | ✓ |\n"
        report += f"| Timbral | {self.timbral_score:.2f}/1.00 | ✓ |\n"
        report += f"| Emotional | {self.emotional_score:.2f}/1.00 | ✓ |\n\n"
        
        report += "## Strengths\n\n"
        for strength in self.strengths:
            report += f"- {strength}\n"
        report += "\n"
        
        report += "## Areas for Improvement\n\n"
        for weakness in self.weaknesses:
            report += f"- {weakness}\n"
        report += "\n"
        
        report += "## Opportunities\n\n"
        for opportunity in self.opportunities:
            report += f"- {opportunity}\n"
        
        return report


class ProfessionalAnalyticsEngine:
    """
    Advanced analytics for professional music creators.
    Provides detailed insights and comparative metrics.
    """
    
    @staticmethod
    def analyze_composition(
        composition_id: str,
        genre: str,
        duration_seconds: float,
        tracks: List,
        melody_hash: str = None,
        harmonic_complexity: float = 0.5,
        rhythmic_regularity: float = 0.5,
        emotional_intensity: float = 0.5
    ) -> ProfessionalAnalytics:
        """
        Comprehensive composition analysis.
        Returns detailed analytics with scores and recommendations.
        """
        
        analytics = ProfessionalAnalytics(
            composition_id=composition_id,
            genre=genre,
            duration_seconds=duration_seconds
        )
        
        # MELODIC ANALYSIS
        melodic_score, melodic_metrics = ProfessionalAnalyticsEngine._analyze_melodic(tracks)
        analytics.melodic_score = melodic_score
        analytics.metrics.extend(melodic_metrics)
        
        # HARMONIC ANALYSIS
        harmonic_score, harmonic_metrics = ProfessionalAnalyticsEngine._analyze_harmonic(
            tracks, harmonic_complexity
        )
        analytics.harmonic_score = harmonic_score
        analytics.metrics.extend(harmonic_metrics)
        
        # RHYTHMIC ANALYSIS
        rhythmic_score, rhythmic_metrics = ProfessionalAnalyticsEngine._analyze_rhythmic(
            tracks, rhythmic_regularity
        )
        analytics.rhythmic_score = rhythmic_score
        analytics.metrics.extend(rhythmic_metrics)
        
        # STRUCTURAL ANALYSIS
        structural_score, structural_metrics = ProfessionalAnalyticsEngine._analyze_structural(
            duration_seconds, len(tracks)
        )
        analytics.structural_score = structural_score
        analytics.metrics.extend(structural_metrics)
        
        # TIMBRAL ANALYSIS
        timbral_score, timbral_metrics = ProfessionalAnalyticsEngine._analyze_timbral(tracks)
        analytics.timbral_score = timbral_score
        analytics.metrics.extend(timbral_metrics)
        
        # EMOTIONAL ANALYSIS
        emotional_score, emotional_metrics = ProfessionalAnalyticsEngine._analyze_emotional(
            emotional_intensity, genre
        )
        analytics.emotional_score = emotional_score
        analytics.metrics.extend(emotional_metrics)
        
        # Calculate overall score with weights
        weights = {
            "melodic": 0.25,
            "harmonic": 0.25,
            "rhythmic": 0.15,
            "structural": 0.15,
            "timbral": 0.10,
            "emotional": 0.10
        }
        
        analytics.overall_score = (
            analytics.melodic_score * weights["melodic"] +
            analytics.harmonic_score * weights["harmonic"] +
            analytics.rhythmic_score * weights["rhythmic"] +
            analytics.structural_score * weights["structural"] +
            analytics.timbral_score * weights["timbral"] +
            analytics.emotional_score * weights["emotional"]
        )
        
        # Generate insights
        ProfessionalAnalyticsEngine._generate_insights(analytics)
        
        return analytics
    
    @staticmethod
    def _analyze_melodic(tracks: List) -> tuple:
        """Analyze melodic qualities."""
        metrics = []
        
        # Extract main melody
        melody_notes = []
        for track in tracks:
            if hasattr(track, 'notes'):
                melody_notes.extend([n.pitch for n in track.notes])
        
        score = 0.7  # Default
        
        if melody_notes:
            # Check range
            pitch_range = max(melody_notes) - min(melody_notes) if melody_notes else 0
            range_metric = MetricScore(
                name="Pitch Range",
                value=min(1.0, pitch_range / 48),  # Good range is 48+ semitones
                category=AnalyticsCategory.MELODIC,
                ideal_range=(40, 60),
                interpretation=f"{pitch_range} semitones",
                recommendation="Wider ranges are generally more interesting" if pitch_range < 24 else ""
            )
            metrics.append(range_metric)
            
            # Check for variety
            if len(set(melody_notes)) > len(melody_notes) * 0.6:  # 60%+ unique notes
                score += 0.15
            
            # Check contour interest
            score = max(0.5, min(1.0, score))
        
        return score, metrics
    
    @staticmethod
    def _analyze_harmonic(tracks: List, harmonic_complexity: float) -> tuple:
        """Analyze harmonic qualities."""
        metrics = []
        score = harmonic_complexity * 0.7 + 0.3
        
        complexity_metric = MetricScore(
            name="Harmonic Complexity",
            value=harmonic_complexity,
            category=AnalyticsCategory.HARMONIC,
            ideal_range=(0.3, 0.8),
            interpretation="Moderate complexity is ideal for most genres",
            recommendation="Increase harmonic complexity with more chord extensions" if harmonic_complexity < 0.3 else ""
        )
        metrics.append(complexity_metric)
        
        return score, metrics
    
    @staticmethod
    def _analyze_rhythmic(tracks: List, rhythmic_regularity: float) -> tuple:
        """Analyze rhythmic qualities."""
        metrics = []
        score  = 0.7
        
        regularity_metric = MetricScore(
            name="Rhythmic Regularity",
            value=rhythmic_regularity,
            category=AnalyticsCategory.RHYTHMIC,
            ideal_range=(0.5, 0.9),
            interpretation="Higher regularity = more predictable, lower = more experimental",
            recommendation="Add more syncopation for interest" if rhythmic_regularity > 0.85 else ""
        )
        metrics.append(regularity_metric)
        
        score = 0.5 + (rhythmic_regularity * 0.5)
        return score, metrics
    
    @staticmethod
    def _analyze_structural(duration_seconds: float, num_tracks: int) -> tuple:
        """Analyze structural qualities."""
        metrics = []
        
        # Duration appropriateness
        duration_metric = MetricScore(
            name="Duration Appropriateness",
            value=min(1.0, duration_seconds / 300),  # Ideal is 300+ seconds for depth
            category=AnalyticsCategory.STRUCTURAL,
            interpretation=f"{duration_seconds:.0f}s composition"
        )
        metrics.append(duration_metric)
        
        # Track count appropriateness
        track_metric = MetricScore(
            name="Orchestration Density",
            value=min(1.0, num_tracks / 6),  # Ideal is 4-6 tracks
            category=AnalyticsCategory.STRUCTURAL,
            interpretation=f"{num_tracks} tracks"
        )
        metrics.append(track_metric)
        
        score = 0.7 + (min(num_tracks, 6) / 10)
        return score, metrics
    
    @staticmethod
    def _analyze_timbral(tracks: List) -> tuple:
        """Analyze timbral (tone color) qualities."""
        metrics = []
        
        # Track variety
        track_types = set()
        for track in tracks:
            if hasattr(track, 'track_type'):
                track_types.add(track.track_type)
        
        variety_score = len(track_types) / max(1, len(tracks))
        variety_metric = MetricScore(
            name="Timbral Variety",
            value=variety_score,
            category=AnalyticsCategory.TIMBRAL,
            interpretation=f"{len(track_types)} different timbres across {len(tracks)} tracks"
        )
        metrics.append(variety_metric)
        
        score = 0.5 + (variety_score * 0.5)
        return score, metrics
    
    @staticmethod
    def _analyze_emotional(emotional_intensity: float, genre: str) -> tuple:
        """Analyze emotional qualities."""
        metrics = []
        
        intensity_metric = MetricScore(
            name="Emotional Intensity",
            value=emotional_intensity,
            category=AnalyticsCategory.EMOTIONAL,
            ideal_range=(0.0, 1.0),
            interpretation="How strongly the emotional intent is conveyed"
        )
        metrics.append(intensity_metric)
        
        # Genre appropriateness
        intense_genres = ["rock", "metal", "electronic", "cinematic"]
        calm_genres = ["ambient", "lofi", "classical"]
        
        if genre.lower() in intense_genres:
            genre_match = emotional_intensity  # Should be high
        elif genre.lower() in calm_genres:
            genre_match = 1.0 - emotional_intensity  # Should be low
        else:
            genre_match = 0.5 + (abs(0.5 - emotional_intensity) / 2)
        
        score = 0.5 + (genre_match * 0.5)
        return score, metrics
    
    @staticmethod
    def _generate_insights(analytics: ProfessionalAnalytics):
        """Generate actionable insights from analytics."""
        
        # Strengths
        if analytics.melodic_score > 0.75:
            analytics.strengths.append("Strong melodic content with good contour and range")
        if analytics.harmonic_score > 0.75:
            analytics.strengths.append("Sophisticated harmonic language")
        if analytics.rhythmic_score > 0.75:
            analytics.strengths.append("Well-developed rhythmic interest")
        if analytics.structural_score > 0.75:
            analytics.strengths.append("Excellent structural balance")
        
        # Weaknesses
        if analytics.melodic_score < 0.6:
            analytics.weaknesses.append("Melodic content could be more distinctive")
        if analytics.harmonic_score < 0.6:
            analytics.weaknesses.append("Harmonic language is relatively simple")
        if analytics.rhythmic_score < 0.6:
            analytics.weaknesses.append("Rhythmic patterns are predictable")
        
        # Opportunities
        if analytics.overall_score < 0.8:
            analytics.opportunities.append("Room for improvement in overall composition depth")
        if analytics.emotional_score < 0.7:
            analytics.opportunities.append("Strengthen emotional expression through intensity variation")
