# -*- coding: utf-8 -*-
"""
Quality Control Node: Assess quality of generated tracks with intelligent reasoning.
Uses chain-of-thought quality analysis and recommendation generation.
"""

from src.agents.state import MusicState, GenerationQualityReport, TrackQualityIssue

try:
    from src.midigent.intelligent_quality_reviewer import (
        IntelligentQualityReviewer, 
        QualityReport,
        SeverityLevel
    )
    INTELLIGENT_REVIEWER_AVAILABLE = True
except ImportError:
    INTELLIGENT_REVIEWER_AVAILABLE = False


def quality_control_agent_node(state: MusicState) -> MusicState:
    """
    Agent Node: Assess quality of generated tracks with intelligent reasoning.
    Uses chain-of-thought analysis to evaluate musical quality.
    """
    print("\n[🔍 QUALITY AGENT] Comprehensive quality assessment...")
    
    if state.get("error"):
        print("[⚠️  ERROR] Skipping quality review due to upstream error")
        return state
    
    generated_tracks = state.get("generated_tracks", [])
    
    if not generated_tracks:
        print("[⚠️  ] No tracks to review")
        state["needs_refinement"] = False
        state["quality_report"] = GenerationQualityReport(overall_score=0.0)
        return state
    
    try:
        # Use intelligent reviewer if available
        if INTELLIGENT_REVIEWER_AVAILABLE:
            original_intent = state.get("enhanced_intent")
            composition_structure = state.get("composition_structure")
            previous_reviews = state.get("previous_quality_reviews", [])
            
            quality_report = IntelligentQualityReviewer.review_composition(
                tracks=generated_tracks,
                original_intent=original_intent,
                composition_structure=composition_structure,
                previous_reviews=previous_reviews if isinstance(previous_reviews, list) else []
            )
            
            # Display the reasoning chain
            print("\n" + "=" * 70)
            for line in quality_report.reasoning_chain:
                print(line)
            print("=" * 70)
            
            # Display recommendations
            if quality_report.recommendations:
                print("\n📋 RECOMMENDATIONS:")
                for rec in quality_report.recommendations:
                    print(f"   • {rec}")
            
            # Convert to legacy format for compatibility
            legacy_report = GenerationQualityReport(
                overall_score=quality_report.overall_score,
                issues=[
                    TrackQualityIssue(
                        track_index=issue.category.value.count("_"),
                        issue_type=issue.category.value,
                        severity=issue.severity.value,
                        description=issue.description,
                        suggestion=issue.suggestion
                    )
                    for issue in quality_report.issues
                ],
                needs_refinement=quality_report.needs_refinement,
                refinement_suggestions=quality_report.recommendations,
                positive_aspects=quality_report.positive_aspects
            )
            
            state["quality_report"] = legacy_report
            state["intelligent_quality_report"] = quality_report
            state["needs_refinement"] = quality_report.needs_refinement
            
            # Track previous reviews for consistency checking
            if "previous_quality_reviews" not in state:
                state["previous_quality_reviews"] = []
            state["previous_quality_reviews"].append(quality_report)
            
            print(f"\n✅ [ASSESSMENT COMPLETE] Score: {quality_report.overall_score:.2f}/1.00")
            print(f"   Refinement needed: {'YES' if quality_report.needs_refinement else 'NO'}")
            print(f"   Priority: {quality_report.refinement_priority}")
            
        else:
            # Fallback to basic quality checks
            print("[ℹ️  ] Using basic quality checks (intelligent reviewer unavailable)")
            issues = []
            positive_aspects = []
            
            # Check 1: Track diversity
            track_types = {t.track_type for t in generated_tracks if hasattr(t, 'track_type')}
            if len(track_types) >= 3:
                positive_aspects.append("Good track type diversity")
            else:
                issues.append(TrackQualityIssue(
                    track_index=0,
                    issue_type="instrumentation",
                    severity="medium",
                    description="Limited track type diversity",
                    suggestion="Add more varied track types"
                ))
            
            # Check 2: Density analysis
            total_notes = sum(len(t.notes) if hasattr(t, 'notes') else 0 for t in generated_tracks)
            avg_notes_per_track = total_notes / len(generated_tracks) if generated_tracks else 0
            
            if 10 < avg_notes_per_track < 100:
                positive_aspects.append("Good note density")
            elif avg_notes_per_track <= 10:
                issues.append(TrackQualityIssue(
                    track_index=0,
                    issue_type="density",
                    severity="medium",
                    description="Tracks too sparse",
                    suggestion="Increase note density"
                ))
            
            issue_penalty = min(len(issues) * 0.15, 0.7)
            overall_score = max(0.3, 1.0 - issue_penalty)
            
            needs_refinement = (
                any(issue.severity == "high" for issue in issues) or
                overall_score < 0.6
            ) and state.get("current_iteration", 0) < state.get("max_refinement_iterations", 2)
            
            report = GenerationQualityReport(
                overall_score=overall_score,
                issues=issues,
                needs_refinement=needs_refinement,
                refinement_suggestions=[issue.suggestion for issue in issues if issue.severity in ["high", "medium"]],
                positive_aspects=positive_aspects
            )
            
            state["quality_report"] = report
            state["needs_refinement"] = needs_refinement
            
            print(f"   Score: {overall_score:.2f}/1.0 | Issues: {len(issues)}")
        
    except Exception as e:
        state["error"] = f"Quality assessment failed: {str(e)}"
        state["needs_refinement"] = False
        state["quality_report"] = GenerationQualityReport(overall_score=0.5)
        print(f"[❌ ERROR] {state['error']}")
        import traceback
        traceback.print_exc()
    
    return state


def quality_control_router(state: MusicState) -> str:
    """
    Router to determine next step based on quality assessment.
    Routes to refinement if issues found, otherwise to finalization.
    """
    if state.get("needs_refinement", False):
        current_iter = state.get("current_iteration", 0)
        max_iter = state.get("max_refinement_iterations", 2)
        if current_iter < max_iter:
            print(f"\n[🔄 ROUTING] Quality check denies refinement (iter {current_iter}/{max_iter})")
            return "refine"
    
    print("\n[✅ ROUTING] Quality check passed - proceeding to finalization")
    return "finalize"
