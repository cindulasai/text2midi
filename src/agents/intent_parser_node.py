# -*- coding: utf-8 -*-
"""
Intent Parser Node: Extract musical intent from user prompts.

Uses the unified LLM Intent Engine (src/intent/engine.py) for high-accuracy
chain-of-thought parsing with Pydantic validation, replacing the legacy
multi-parser fallback chain.
"""

import logging

from src.agents.state import MusicState, MusicIntent
from src.intent.engine import LLMIntentEngine

logger = logging.getLogger(__name__)

# Singleton engine — initialised once, reused across graph invocations
_engine = LLMIntentEngine()


def intent_parser_node(state: MusicState) -> MusicState:
    """
    Agent Node: Parse user prompt and extract musical intent.

    Pipeline:
      1. Preprocess (normalize, extract hard numbers)
      2. LLM call with chain-of-thought system prompt + 8 few-shot examples
      3. Pydantic v2 schema validation + musical coherence checks
      4. Auto-correction retry (max 1) on validation failure
      5. Enrichment + conversion to legacy types for downstream compatibility
      6. Keyword fallback when no LLM provider is configured
    """
    print("\n[INTENT AGENT] Analyzing user request with LLM Intent Engine...")

    user_prompt = state.get("user_prompt", "")

    if not user_prompt:
        state["error"] = "No user prompt provided"
        return state

    try:
        parsed_intent, enhanced_intent, music_intent = _engine.parse(user_prompt)

        # Display chain-of-thought reasoning
        if parsed_intent.reasoning:
            print("\nPARSING REASONING (chain-of-thought):")
            # Reasoning is a single string; show first ~500 chars
            reasoning_preview = parsed_intent.reasoning[:500]
            for line in reasoning_preview.split(". "):
                print(f"   {line.strip()}")

        # Store in state
        state["intent"] = music_intent
        state["enhanced_intent"] = enhanced_intent
        state["parsed_intent"] = parsed_intent  # Rich Pydantic model for downstream nodes
        state["composition_structure"] = enhanced_intent.composition_structure

        # Summary
        print(f"\n[OK] INTENT PARSED: Genre={music_intent.genre} | Energy={music_intent.energy}")
        print(f"   Tempo: {enhanced_intent.tempo_preference} BPM")
        print(f"   Duration: {enhanced_intent.duration_bars} bars ({enhanced_intent.duration_seconds}s)")
        print(f"   Complexity: {enhanced_intent.complexity.value}")
        print(f"   Instruments: {', '.join(enhanced_intent.specific_instruments) or 'auto'}")
        print(f"   Confidence: {parsed_intent.overall_confidence:.0%}")

        cs = enhanced_intent.composition_structure
        print(f"   Structure: I:{cs.intro_bars} V:{cs.verse_bars} C:{cs.chorus_bars} B:{cs.bridge_bars} O:{cs.outro_bars}")

    except Exception as e:
        logger.exception("[INTENT AGENT] Parsing failed")
        state["error"] = f"Intent parsing failed: {str(e)}"
        print(f"[ERROR] Error: {state['error']}")

    return state
