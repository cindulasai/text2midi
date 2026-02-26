#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Edge Cases and Bug Fixes
Tests vague input processing and null composition_structure handling
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.midigent.intelligent_quality_reviewer import IntelligentQualityReviewer
from src.midigent.advanced_intent_parser import AdvancedIntentParser, EnhancedMusicIntent
from src.agents.intent_parser_node import intent_parser_node
from src.agents.state import MusicState


def test_quality_reviewer_with_none_composition():
    """Test that quality reviewer handles None composition_structure gracefully."""
    print("\n" + "="*70)
    print("TEST 1: Quality Reviewer with None composition_structure")
    print("="*70)
    
    # Create mock track data
    class MockTrack:
        def __init__(self):
            self.track_type = "melody"
            self.notes = []
    
    tracks = [MockTrack(), MockTrack()]
    
    # Create intent but no composition structure
    intent = type('obj', (), {
        'duration_bars': 64,
        'genre': 'ambient',
        'mood': 'calm',
        'energy': 'low'
    })()
    
    try:
        # This should NOT crash even with composition_structure=None
        report = IntelligentQualityReviewer.review_composition(
            tracks=tracks,
            original_intent=intent,
            composition_structure=None,  # <- The edge case
            previous_reviews=[]
        )
        
        print("[OK] SUCCESS: Quality review completed with None composition_structure")
        print(f"   Overall Score: {report.overall_score:.2f}/1.00")
        print(f"   Reasoning steps: {len(report.reasoning_chain)}")
        print(f"   Issues identified: {len(report.issues)}")
        print(f"   Needs refinement: {report.needs_refinement}")
        return True
    except Exception as e:
        print(f"[FAIL] FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_vague_input_processing():
    """Test processing of vague user input (edge case)."""
    print("\n" + "="*70)
    print("TEST 2: Vague Input Processing (Intent Parser Fallback)")
    print("="*70)
    
    vague_inputs = [
        "generate epic one",
        "make some music",
        "apic",
        "audio",
    ]
    
    results = []
    for prompt in vague_inputs:
        print(f"\nTesting prompt: '{prompt}'")
        try:
            state = MusicState(user_prompt=prompt)
            state = intent_parser_node(state)
            
            if state.get("error"):
                print(f"   [FAIL] Error: {state['error']}")
                results.append(False)
            else:
                print(f"   [OK] Intent parsed")
                
                # Check that composition_structure exists
                comp_struct = state.get("composition_structure")
                if comp_struct:
                    print(f"   [OK] Composition structure created")
                    print(f"      Total bars: {getattr(comp_struct, 'total_bars', '?')}")
                    print(f"      Tempo: {getattr(comp_struct, 'tempo', '?')}")
                    results.append(True)
                else:
                    print(f"   [FAIL] Composition structure is None!")
                    results.append(False)
                    
        except Exception as e:
            print(f"   [FAIL] Exception: {str(e)}")
            results.append(False)
    
    success_rate = sum(results) / len(results) * 100
    print(f"\nResult: {success_rate:.0f}% ({sum(results)}/{len(results)})")
    return all(results)


def test_quality_with_missing_intent():
    """Test quality reviewer with None original_intent."""
    print("\n" + "="*70)
    print("TEST 3: Quality Reviewer with None original_intent")
    print("="*70)
    
    class MockTrack:
        def __init__(self):
            self.track_type = "melody"
            self.notes = []
    
    tracks = [MockTrack()]
    
    try:
        # Test with None intent
        report = IntelligentQualityReviewer.review_composition(
            tracks=tracks,
            original_intent=None,  # <- Edge case
            composition_structure=None,  # <- Edge case
            previous_reviews=[]
        )
        
        print("[OK] SUCCESS: Quality review completed with None intent and composition")
        print(f"   Overall Score: {report.overall_score:.2f}/1.00")
        return True
    except Exception as e:
        print(f"[FAIL] FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_advanced_intent_parser_creates_structure():
    """Test that advanced intent parser always creates composition_structure."""
    print("\n" + "="*70)
    print("TEST 4: Advanced Intent Parser Composition Structure")
    print("="*70)
    
    test_cases = [
        "4 minute ambient track",
        "generate pop music",
        "lofi beats",
        "fast tempo electronic",
    ]
    
    results = []
    for prompt in test_cases:
        print(f"\nTesting: '{prompt}'")
        try:
            intent = AdvancedIntentParser.parse_intent_deeply(prompt)
            
            if intent.composition_structure:
                print(f"   [OK] Composition structure created")
                print(f"      Total bars: {intent.composition_structure.total_bars}")
                print(f"      Complexity: {intent.complexity.value}")
                results.append(True)
            else:
                print(f"   [FAIL] Composition structure is None!")
                results.append(False)
                
        except Exception as e:
            print(f"   [FAIL] Exception: {str(e)}")
            results.append(False)
    
    success_rate = sum(results) / len(results) * 100
    print(f"\nResult: {success_rate:.0f}% ({sum(results)}/{len(results)})")
    return all(results)


def main():
    """Run all tests."""
    print("\n" + "="*70)
    print("        BUG FIX VERIFICATION TEST SUITE")
    print("="*70)
    
    tests = [
        ("None composition_structure", test_quality_reviewer_with_none_composition),
        ("Vague input processing", test_vague_input_processing),
        ("None original_intent", test_quality_with_missing_intent),
        ("Advanced parser structures", test_advanced_intent_parser_creates_structure),
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"\n[FAIL] Test '{test_name}' crashed: {str(e)}")
            results[test_name] = False
    
    print("\n" + "="*70)
    print("                    SUMMARY")
    print("="*70)
    
    for test_name, passed in results.items():
        status = "[OK]" if passed else "[FAIL]"
        print(f"{status}: {test_name}")
    
    total_passed = sum(results.values())
    total_tests = len(results)
    
    print(f"\nTotal: {total_passed}/{total_tests} tests passed")
    
    if total_passed == total_tests:
        print("\n[SUCCESS] ALL TESTS PASSED! Bug fixes verified successfully!")
        return 0
    else:
        print(f"\n[WARNING] {total_tests - total_passed} test(s) failed")
        return 1


if __name__ == "__main__":
    exit(main())
