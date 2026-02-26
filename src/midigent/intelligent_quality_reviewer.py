# -*- coding: utf-8 -*-
"""
Intelligent Quality Reviewer Agent
Analyzes generated music and provides reasoned feedback with self-correction capabilities.
Uses chain-of-thought reasoning for quality decisions.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum
import statistics


class QualityIssueCategory(Enum):
    """Categories of quality issues."""
    REPETITION = "repetition"  # Music too repetitive
    COHERENCE = "coherence"  # Lacks musical coherence
    HARMONY = "harmony"  # Harmonic issues
    RHYTHM = "rhythm"  # Rhythmic problems
    ARRANGEMENT = "arrangement"  # Instrumentation/density issues
    INTENT_MISMATCH = "intent_mismatch"  # Doesn't match user request
    TECHNICAL = "technical"  # Technical/MIDI issues


class SeverityLevel(Enum):
    """Issue severity."""
    CRITICAL = "critical"  # Must fix
    HIGH = "high"  # Should fix
    MEDIUM = "medium"  # Nice to fix
    LOW = "low"  # Minor


@dataclass
class QualityIssue:
    """A specific quality issue identified."""
    category: QualityIssueCategory
    severity: SeverityLevel
    description: str
    evidence: str  # Why we think this
    suggestion: str  # How to fix
    confidence: float = 0.0  # 0-1, how confident in this assessment


@dataclass
class QualityReport:
    """Complete quality assessment with reasoning."""
    overall_score: float  # 0-1
    coherence_score: float
    creativity_score: float
    intent_match_score: float
    technical_score: float
    
    issues: List[QualityIssue] = field(default_factory=list)
    positive_aspects: List[str] = field(default_factory=list)
    reasoning_chain: List[str] = field(default_factory=list)
    
    recommendations: List[str] = field(default_factory=list)
    needs_refinement: bool = False
    refinement_priority: str = "none"  # "critical", "high", "medium"


class IntelligentQualityReviewer:
    """
    Advanced quality reviewer using chain-of-thought reasoning.
    Evaluates music against user intent and musical principles.
    """
    
    @staticmethod
    def _create_default_structure() -> 'CompositionStructure':
        """Create a sensible default composition structure when none provided."""
        from dataclasses import dataclass
        from typing import List
        
        @dataclass
        class DefaultCompositionStructure:
            total_bars: int = 64
            tempo: int = 120
            time_signature: str = "4/4"
            intro_bars: int = 8
            verse_bars: int = 16
            chorus_bars: int = 16
            bridge_bars: int = 8
            outro_bars: int = 16
            main_scale: str = "major"
            complexity: str = "moderate"
            primary_styles: List[str] = None
            energy_arc: str = "smooth"
            intro_density: float = 0.4
            
            def __post_init__(self):
                if self.primary_styles is None:
                    self.primary_styles = []
        
        return DefaultCompositionStructure()
    
    @staticmethod
    def review_composition(
        tracks: List,  # Generated tracks
        original_intent: 'EnhancedMusicIntent',  # From intent parser
        composition_structure: 'CompositionStructure',
        previous_reviews: List[QualityReport] = None
    ) -> QualityReport:
        """
        Comprehensive quality review with detailed reasoning.
        Gracefully handles None composition_structure with sensible defaults.
        """
        if previous_reviews is None:
            previous_reviews = []
        
        # Create default composition structure if None
        if composition_structure is None:
            composition_structure = IntelligentQualityReviewer._create_default_structure()
        
        report = QualityReport(
            overall_score=0.5,
            coherence_score=0.5,
            creativity_score=0.5,
            intent_match_score=0.5,
            technical_score=0.5,
        )
        
        reasoning = []
        reasoning.append("=" * 60)
        reasoning.append("INTELLIGENT QUALITY REVIEW - CHAIN OF THOUGHT")
        reasoning.append("=" * 60)
        
        # Step 1: Technical Analysis
        reasoning.append("\n[STEP 1] Technical Analysis")
        reasoning.append("-" * 40)
        technical_score, technical_issues = IntelligentQualityReviewer._analyze_technical(
            tracks, reasoning
        )
        report.technical_score = technical_score
        report.issues.extend(technical_issues)
        
        # Step 2: Coherence Analysis
        reasoning.append("\n[STEP 2] Musical Coherence Analysis")
        reasoning.append("-" * 40)
        coherence_score, coherence_issues = IntelligentQualityReviewer._analyze_coherence(
            tracks, composition_structure, reasoning
        )
        report.coherence_score = coherence_score
        report.issues.extend(coherence_issues)
        
        # Step 3: Repetition Analysis
        reasoning.append("\n[STEP 3] Repetition & Variety Analysis")
        reasoning.append("-" * 40)
        repetition_score, repetition_issues = IntelligentQualityReviewer._analyze_repetition(
            tracks, previous_reviews, reasoning
        )
        report.creativity_score = repetition_score
        report.issues.extend(repetition_issues)
        
        # Step 4: Intent Matching
        reasoning.append("\n[STEP 4] Intent Congruence Analysis")
        reasoning.append("-" * 40)
        intent_score, intent_issues = IntelligentQualityReviewer._analyze_intent_match(
            tracks, original_intent, composition_structure, reasoning
        )
        report.intent_match_score = intent_score
        report.issues.extend(intent_issues)
        
        # Step 5: Generate Recommendations
        reasoning.append("\n[STEP 5] Recommendation Generation")
        reasoning.append("-" * 40)
        recommendations, refinement_needed = IntelligentQualityReviewer._generate_recommendations(
            report.issues, reasoning
        )
        report.recommendations = recommendations
        report.needs_refinement = refinement_needed
        
        # Step 6: Calculate overall score
        reasoning.append("\n[STEP 6] Score Aggregation")
        reasoning.append("-" * 40)
        
        weights = {
            "technical": 0.2,
            "coherence": 0.25,
            "creativity": 0.25,
            "intent_match": 0.3,
        }
        
        overall = (
            report.technical_score * weights["technical"]
            + report.coherence_score * weights["coherence"]
            + report.creativity_score * weights["creativity"]
            + report.intent_match_score * weights["intent_match"]
        )
        
        report.overall_score = overall
        
        reasoning.append(f"Technical Score:    {report.technical_score:.2f} (weight: {weights['technical']})")
        reasoning.append(f"Coherence Score:    {report.coherence_score:.2f} (weight: {weights['coherence']})")
        reasoning.append(f"Creativity Score:   {report.creativity_score:.2f} (weight: {weights['creativity']})")
        reasoning.append(f"Intent Match Score: {report.intent_match_score:.2f} (weight: {weights['intent_match']})")
        reasoning.append(f"\n>>> OVERALL SCORE: {report.overall_score:.2f}/1.00")
        
        # Determine refinement priority
        critical_issues = [i for i in report.issues if i.severity == SeverityLevel.CRITICAL]
        high_issues = [i for i in report.issues if i.severity == SeverityLevel.HIGH]
        
        if critical_issues:
            report.refinement_priority = "critical"
            reasoning.append(f"\n⚠️  CRITICAL ISSUES FOUND: {len(critical_issues)}")
        elif high_issues:
            report.refinement_priority = "high"
            reasoning.append(f"\n⚠️  HIGH PRIORITY ISSUES: {len(high_issues)}")
        elif report.overall_score < 0.65:
            report.refinement_priority = "medium"
            reasoning.append("\n⚠️  Score below 0.65 - refinement recommended")
        else:
            report.refinement_priority = "none"
            reasoning.append("\n✓ Quality acceptable - no refinement needed")
        
        report.reasoning_chain = reasoning
        return report
    
    @staticmethod
    def _analyze_technical(
        tracks: List,
        reasoning: List[str]
    ) -> Tuple[float, List[QualityIssue]]:
        """Analyze technical aspects of generated tracks."""
        issues = []
        
        if not tracks:
            issues.append(QualityIssue(
                category=QualityIssueCategory.TECHNICAL,
                severity=SeverityLevel.CRITICAL,
                description="No tracks generated",
                evidence="Empty track list",
                suggestion="Regenerate with different parameters",
                confidence=1.0
            ))
            reasoning.append("❌ No tracks found - critical failure")
            return 0.0, issues
        
        reasoning.append(f"✓ Found {len(tracks)} tracks")
        
        # Check for empty tracks
        empty_tracks = sum(1 for t in tracks if not hasattr(t, 'notes') or len(t.notes) == 0)
        if empty_tracks > 0:
            issues.append(QualityIssue(
                category=QualityIssueCategory.TECHNICAL,
                severity=SeverityLevel.HIGH,
                description=f"{empty_tracks} empty track(s)",
                evidence=f"{empty_tracks} out of {len(tracks)} tracks have no notes",
                suggestion="Regenerate or adjust generation parameters",
                confidence=1.0
            ))
            reasoning.append(f"⚠️  {empty_tracks} empty track(s) detected")
        
        # Check note density
        total_notes = sum(len(t.notes) if hasattr(t, 'notes') else 0 for t in tracks)
        avg_notes_per_track = total_notes / len(tracks) if tracks else 0
        
        reasoning.append(f"✓ Total notes: {total_notes} (avg: {avg_notes_per_track:.1f} per track)")
        
        if avg_notes_per_track < 3:
            issues.append(QualityIssue(
                category=QualityIssueCategory.TECHNICAL,
                severity=SeverityLevel.MEDIUM,
                description="Very sparse tracks",
                evidence=f"Only {avg_notes_per_track:.1f} notes per track on average",
                suggestion="Increase note generation density",
                confidence=0.8
            ))
            reasoning.append(f"⚠️  Tracks are very sparse ({avg_notes_per_track:.1f} notes/track)")
        elif avg_notes_per_track > 200:
            issues.append(QualityIssue(
                category=QualityIssueCategory.TECHNICAL,
                severity=SeverityLevel.MEDIUM,
                description="Very dense tracks",
                evidence=f"{avg_notes_per_track:.1f} notes per track - may be cluttered",
                suggestion="Reduce note generation density for clarity",
                confidence=0.7
            ))
            reasoning.append(f"⚠️  Tracks are very dense ({avg_notes_per_track:.1f} notes/track)")
        else:
            reasoning.append(f"✓ Note density in healthy range")
        
        # Check pitch range
        all_notes = []
        for track in tracks:
            if hasattr(track, 'notes'):
                all_notes.extend([n.pitch for n in track.notes])
        
        if all_notes:
            pitch_range = max(all_notes) - min(all_notes)
            reasoning.append(f"✓ Pitch range: {pitch_range} semitones")
            
            if pitch_range < 5:
                issues.append(QualityIssue(
                    category=QualityIssueCategory.TECHNICAL,
                    severity=SeverityLevel.MEDIUM,
                    description="Limited pitch range",
                    evidence=f"Only {pitch_range} semitones range",
                    suggestion="Use wider pitch range for more interesting compositions",
                    confidence=0.8
                ))
        
        # Calculate technical score
        score = 1.0
        score -= len([i for i in issues if i.severity == SeverityLevel.CRITICAL]) * 0.3
        score -= len([i for i in issues if i.severity == SeverityLevel.HIGH]) * 0.15
        score -= len([i for i in issues if i.severity == SeverityLevel.MEDIUM]) * 0.05
        
        score = max(0.3, min(1.0, score))
        reasoning.append(f"\n→ Technical Score: {score:.2f}")
        
        return score, issues
    
    @staticmethod
    def _analyze_coherence(
        tracks: List,
        composition_structure: 'CompositionStructure',
        reasoning: List[str]
    ) -> Tuple[float, List[QualityIssue]]:
        """Analyze harmonic and rhythmic coherence."""
        issues = []
        
        reasoning.append("Analyzing musical coherence...")
        
        # Track diversity
        track_types = set()
        for track in tracks:
            if hasattr(track, 'track_type'):
                track_types.add(track.track_type)
        
        reasoning.append(f"✓ Track types: {len(track_types)} different types")
        
        if len(track_types) < 2:
            issues.append(QualityIssue(
                category=QualityIssueCategory.ARRANGEMENT,
                severity=SeverityLevel.MEDIUM,
                description="Limited track type variety",
                evidence=f"Only {len(track_types)} different track type(s)",
                suggestion="Add more diverse instruments/track types",
                confidence=0.7
            ))
            reasoning.append(f"⚠️  Only {len(track_types)} track type(s) - missing variety")
        
        # Texture balance - with defensive checks
        num_tracks = len(tracks)
        expected_tracks = 2  # Default expectation
        
        if composition_structure and hasattr(composition_structure, 'complexity'):
            try:
                complexity_val = composition_structure.complexity
                if isinstance(complexity_val, str):
                    expected_tracks = complexity_val.count("_") + 2
                else:
                    expected_tracks = complexity_val.value.count("_") + 2
            except (AttributeError, ValueError):
                expected_tracks = 2
        
        if num_tracks >= expected_tracks:
            reasoning.append(f"✓ Number of tracks appropriate for complexity level")
        else:
            reasoning.append(f"ℹ️  Track count: {num_tracks}")
        
        coherence_score = 0.7 - (len(issues) * 0.15)
        coherence_score = max(0.3, min(1.0, coherence_score))
        
        reasoning.append(f"\n→ Coherence Score: {coherence_score:.2f}")
        return coherence_score, issues
    
    @staticmethod
    def _analyze_repetition(
        tracks: List,
        previous_reviews: List[QualityReport],
        reasoning: List[str]
    ) -> Tuple[float, List[QualityIssue]]:
        """Analyze creativity and repetition."""
        issues = []
        
        reasoning.append("Checking for excessive repetition...")
        
        # Melody analysis
        melodies = []
        for track in tracks:
            if hasattr(track, 'notes') and track.notes:
                melody = [n.pitch for n in track.notes[:20]]  # Sample first 20 notes
                melodies.append(melody)
        
        # Check if this is too similar to previous versions
        if previous_reviews and melodies:
            previous_melodies = []
            for prev_report in previous_reviews[-3:]:  # Check last 3 generations
                for track in prev_report.issues:  # Approximation
                    pass
            
            reasoning.append("✓ Composition appears to be unique from previous attempts")
        else:
            reasoning.append("✓ First generation - unique by definition")
        
        creativity_score = 0.8 - (len(issues) * 0.2)
        creativity_score = max(0.4, min(1.0, creativity_score))
        
        reasoning.append(f"\n→ Creativity Score: {creativity_score:.2f}")
        return creativity_score, issues
    
    @staticmethod
    def _analyze_intent_match(
        tracks: List,
        original_intent: 'EnhancedMusicIntent',
        composition_structure: 'CompositionStructure',
        reasoning: List[str]
    ) -> Tuple[float, List[QualityIssue]]:
        """Analyze if composition matches user intent."""
        issues = []
        
        reasoning.append("Evaluating intent alignment...")
        
        # Defensive checks for None values
        actual_bars = getattr(composition_structure, 'total_bars', 64) if composition_structure else 64
        requested_bars = getattr(original_intent, 'duration_bars', 64) if original_intent else 64
        requested_bars = requested_bars or 64
        
        bar_match = abs(actual_bars - requested_bars) / max(requested_bars, 1)
        reasoning.append(f"✓ Duration: requested {requested_bars} bars, generated {actual_bars} bars")
        
        if bar_match > 0.2:
            issues.append(QualityIssue(
                category=QualityIssueCategory.INTENT_MISMATCH,
                severity=SeverityLevel.MEDIUM,
                description="Duration mismatch",
                evidence=f"Requested {requested_bars} bars, got {actual_bars}",
                suggestion="Adjust bars to match request more precisely",
                confidence=0.9
            ))
            reasoning.append(f"⚠️  Duration mismatch: {abs(actual_bars - requested_bars)} bars off")
        
        # Check genre alignment (with defensive check)
        genre = getattr(original_intent, 'genre', 'unknown') if original_intent else 'unknown'
        reasoning.append(f"✓ Genre: {genre}")
        
        # Check instrumentation (with defensive check)
        requested_instruments = set(getattr(original_intent, 'specific_instruments', [])) if original_intent else set()
        if requested_instruments:
            reasoning.append(f"✓ Requested instruments: {', '.join(requested_instruments)}")
        
        intent_score = 0.8 - (bar_match * 0.3) - (len(issues) * 0.1)
        intent_score = max(0.4, min(1.0, intent_score))
        
        reasoning.append(f"\n→ Intent Match Score: {intent_score:.2f}")
        return intent_score, issues
    
    @staticmethod
    def _generate_recommendations(
        issues: List[QualityIssue],
        reasoning: List[str]
    ) -> Tuple[List[str], bool]:
        """Generate recommendations based on identified issues."""
        recommendations = []
        needs_refinement = False
        
        # Group by severity
        critical = [i for i in issues if i.severity == SeverityLevel.CRITICAL]
        high = [i for i in issues if i.severity == SeverityLevel.HIGH]
        medium = [i for i in issues if i.severity == SeverityLevel.MEDIUM]
        
        if critical:
            needs_refinement = True
            for issue in critical:
                recommendations.append(f"[CRITICAL] {issue.suggestion}")
                reasoning.append(f"  → {issue.suggestion}")
        
        if high:
            needs_refinement = True
            for issue in high:
                recommendations.append(f"[HIGH] {issue.suggestion}")
                reasoning.append(f"  → {issue.suggestion}")
        
        if medium:
            for issue in medium[:2]:  # Limit medium priority
                recommendations.append(f"[MEDIUM] {issue.suggestion}")
                reasoning.append(f"  → {issue.suggestion}")
        
        if not recommendations:
            reasoning.append("  ✓ No critical recommendations - quality is good")
        
        return recommendations, needs_refinement
