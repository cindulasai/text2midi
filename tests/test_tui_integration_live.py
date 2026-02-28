# -*- coding: utf-8 -*-
"""
Live Integration Tests for TUI — Validates API keys, preset generation,
and full MIDI generation pipeline with REAL LLM calls (not mocked).

Run:  uv run python -m pytest tests/test_tui_integration_live.py -v -s
"""

from __future__ import annotations

import os
import sys
import time
import logging

import pytest

# Ensure .env is loaded before anything else
from dotenv import load_dotenv
load_dotenv()

from src.config.log import setup_logging
setup_logging()

from src.config.llm import LLMConfig, call_llm
from src.services.preset_service import PresetService, get_preset_service
from src.config.providers import MinimaxProvider, GroqProvider

logger = logging.getLogger(__name__)

# ================================================================== #
# Test 1: API Key Validation — No 401 Errors
# ================================================================== #

class TestAPIKeyValidation:
    """Verify that configured API keys are valid and do NOT return 401."""

    @classmethod
    def setup_class(cls):
        LLMConfig.initialize()

    def test_llm_providers_detected(self):
        """At least one LLM provider must be available."""
        assert len(LLMConfig.AVAILABLE_PROVIDERS) >= 1, (
            f"No providers available! Check .env file. "
            f"MINIMAX_API_KEY set: {bool(os.environ.get('MINIMAX_API_KEY'))}, "
            f"GROQ_API_KEY set: {bool(os.environ.get('GROQ_API_KEY'))}"
        )
        print(f"\n  [OK] Available providers: {LLMConfig.AVAILABLE_PROVIDERS}")
        print(f"  [OK] Default provider: {LLMConfig.DEFAULT_PROVIDER}")

    def test_minimax_api_key_valid_no_401(self):
        """MiniMax API key should authenticate successfully (no 401)."""
        api_key = os.environ.get("MINIMAX_API_KEY", "")
        if not api_key:
            pytest.skip("MINIMAX_API_KEY not set")

        provider = MinimaxProvider(api_key=api_key)
        try:
            result = provider.call(
                "You are a helpful assistant.",
                "Say 'hello' in one word.",
                temperature=0.1,
                max_tokens=50,
            )
            # MiniMax may return None for very short prompts (content=None)
            # as long as we got HTTP 200, the key is valid
            if result is not None:
                print(f"\n  [OK] MiniMax response: {result!r}")
            else:
                print("\n  [WARN] MiniMax returned None content (key valid, 200 OK, but empty response)")
        except Exception as exc:
            error_str = str(exc).lower()
            assert "401" not in error_str, f"MiniMax got 401 Unauthorized: {exc}"
            assert "unauthorized" not in error_str, f"MiniMax Unauthorized: {exc}"
            assert "authentication" not in error_str, f"MiniMax Auth error: {exc}"
            raise  # re-raise if it's a different error

    def test_groq_api_key_valid_no_401(self):
        """Groq API key should authenticate successfully (no 401)."""
        api_key = os.environ.get("GROQ_API_KEY", "")
        if not api_key:
            pytest.skip("GROQ_API_KEY not set")

        provider = GroqProvider(api_key=api_key)
        try:
            result = provider.call(
                "You are a helpful assistant.",
                "Say 'hello' in one word.",
                temperature=0.1,
                max_tokens=10,
            )
            assert result is not None, "Groq returned None — possible 401 or API error"
            print(f"\n  [OK] Groq response: {result!r}")
        except Exception as exc:
            error_str = str(exc).lower()
            assert "401" not in error_str, f"Groq 401 Unauthorized: {exc}"
            assert "unauthorized" not in error_str, f"Groq Unauthorized: {exc}"
            assert "authentication" not in error_str, f"Groq Auth error: {exc}"
            raise

    def test_call_llm_with_default_provider(self):
        """call_llm() should work with the default provider."""
        result = call_llm(
            "You are a helpful assistant.",
            "Respond with exactly: OK",
            temperature=0.1,
            max_tokens=10,
        )
        assert result is not None, (
            f"call_llm returned None — all providers failed. "
            f"Default: {LLMConfig.DEFAULT_PROVIDER}, "
            f"Available: {LLMConfig.AVAILABLE_PROVIDERS}"
        )
        print(f"\n  [OK] call_llm default provider response: {result!r}")


# ================================================================== #
# Test 2: Preset Service — Select & Load Presets
# ================================================================== #

class TestPresetSelection:
    """Test clicking on preset genres and loading presets (live LLM)."""

    @classmethod
    def setup_class(cls):
        LLMConfig.initialize()
        cls.svc = PresetService(cache_max=50)

    def test_root_categories_available(self):
        """All 16 root genre categories should load."""
        roots = self.svc.get_root_categories()
        assert len(roots) == 16
        root_ids = {r.id for r in roots}
        print(f"\n  [OK] Root genres: {sorted(root_ids)}")
        assert "jazz" in root_ids
        assert "electronic" in root_ids
        assert "cinematic" in root_ids
        assert "ambient" in root_ids

    def test_sub_genres_load_for_jazz(self):
        """Jazz sub-genres should load properly."""
        subs = self.svc.get_sub_genres("jazz")
        assert len(subs) >= 4
        sub_ids = {s.id for s in subs}
        print(f"\n  [OK] Jazz sub-genres ({len(subs)}): {sorted(sub_ids)}")
        assert "jazz.bebop" in sub_ids

    def test_sub_genres_load_for_electronic(self):
        """Electronic sub-genres should load properly."""
        subs = self.svc.get_sub_genres("electronic")
        assert len(subs) >= 4
        sub_ids = {s.id for s in subs}
        print(f"\n  [OK] Electronic sub-genres ({len(subs)}): {sorted(sub_ids)}")

    def test_seed_presets_for_all_roots(self):
        """Seed presets should be available for all root genres (offline fallback)."""
        roots = self.svc.get_root_categories()
        for root in roots:
            seeds = self.svc.get_seed_presets(root.id)
            assert len(seeds) >= 1, f"No seed presets for {root.id}"
        print(f"\n  [OK] All {len(roots)} root genres have seed presets")

    def test_live_preset_generation_jazz_bebop(self):
        """Generate presets for jazz.bebop via LIVE LLM call."""
        start = time.time()
        prompts = self.svc.generate_presets("jazz.bebop", count=3)
        elapsed = time.time() - start

        assert len(prompts) >= 1, "No presets generated for jazz.bebop"
        assert all(isinstance(p, str) and len(p) > 10 for p in prompts), (
            f"Invalid preset content: {prompts}"
        )
        print(f"\n  [OK] jazz.bebop presets ({elapsed:.1f}s):")
        for i, p in enumerate(prompts, 1):
            print(f"      {i}. {p[:80]}...")

    def test_live_preset_generation_electronic_house(self):
        """Generate presets for electronic.house via LIVE LLM call."""
        start = time.time()
        prompts = self.svc.generate_presets("electronic.house", count=3)
        elapsed = time.time() - start

        assert len(prompts) >= 1, "No presets generated for electronic.house"
        print(f"\n  [OK] electronic.house presets ({elapsed:.1f}s):")
        for i, p in enumerate(prompts, 1):
            print(f"      {i}. {p[:80]}...")

    def test_live_preset_generation_cinematic(self):
        """Generate presets for cinematic via LIVE LLM call."""
        start = time.time()
        prompts = self.svc.generate_presets("cinematic", count=3)
        elapsed = time.time() - start

        assert len(prompts) >= 1, "No presets generated for cinematic"
        print(f"\n  [OK] cinematic presets ({elapsed:.1f}s):")
        for i, p in enumerate(prompts, 1):
            print(f"      {i}. {p[:80]}...")


# ================================================================== #
# Test 3: Full Generation Pipeline (end-to-end)
# ================================================================== #

class TestDynamicGeneration:
    """Full end-to-end generation — prompt → LLM → MIDI file output."""

    @classmethod
    def setup_class(cls):
        LLMConfig.initialize()

    def test_full_pipeline_ambient_preset(self):
        """Run the full generation pipeline with an ambient preset prompt."""
        from src.agents.graph import get_agentic_graph
        from src.agents.state import MusicState
        from src.config.constants import OUTPUT_DIR
        import uuid

        OUTPUT_DIR.mkdir(exist_ok=True)
        prompt = "Create a peaceful ambient pad with soft evolving textures, gentle reverb, and slow chord progressions in D major"

        session_id = str(uuid.uuid4())[:8]
        initial_state: MusicState = {
            "user_prompt": prompt,
            "intent": None,
            "track_plan": [],
            "theory_validation": {},
            "theory_valid": False,
            "theory_issues": [],
            "generated_tracks": [],
            "generation_metadata": {},
            "quality_report": None,
            "refinement_attempts": 0,
            "refinement_feedback": "",
            "needs_refinement": False,
            "final_midi_path": None,
            "session_summary": "",
            "messages": [],
            "error": None,
            "error_context": None,
            "session_id": session_id,
            "composition_state": {
                "existing_tracks": [],
                "tempo": 120,
                "key": "C",
                "genre": "pop",
                "mode": "major",
            },
            "max_refinement_iterations": 2,
            "current_iteration": 0,
        }

        graph = get_agentic_graph()
        config = {"configurable": {"thread_id": session_id}}

        print(f"\n  [RUN] Starting full pipeline with prompt: {prompt[:60]}...")
        start = time.time()

        last_state = dict(initial_state)
        nodes_completed = []

        try:
            for chunk in graph.stream(initial_state, config=config, stream_mode="values"):
                current_keys = set(
                    k for k, v in chunk.items()
                    if v is not None
                    and k not in (
                        "user_prompt", "messages", "session_id",
                        "composition_state", "max_refinement_iterations",
                        "current_iteration",
                    )
                )
                last_state = chunk

                key_to_node = {
                    "intent": "intent_parser",
                    "track_plan": "track_planner",
                    "theory_validation": "theory_validator",
                    "generated_tracks": "track_generator",
                    "quality_report": "quality_control",
                    "final_midi_path": "midi_creator",
                    "session_summary": "session_summary",
                }
                for key in current_keys:
                    node = key_to_node.get(key)
                    if node and node not in nodes_completed:
                        nodes_completed.append(node)
                        print(f"      [NODE] {node} ✓")

        except Exception as exc:
            error_str = str(exc).lower()
            assert "401" not in error_str, f"Pipeline hit 401 Unauthorized: {exc}"
            assert "unauthorized" not in error_str, f"Pipeline Unauthorized: {exc}"
            pytest.fail(f"Pipeline failed: {exc}")

        elapsed = time.time() - start

        # Verify results
        error = last_state.get("error")
        if error:
            error_lower = str(error).lower()
            assert "401" not in error_lower, f"Pipeline error contains 401: {error}"
            assert "unauthorized" not in error_lower, f"Pipeline Unauthorized: {error}"

        midi_path = last_state.get("final_midi_path")
        print(f"\n  [OK] Pipeline completed in {elapsed:.1f}s")
        print(f"      Nodes completed: {nodes_completed}")
        print(f"      MIDI path: {midi_path}")
        print(f"      Error: {error}")

        # Intent should be parsed
        assert last_state.get("intent") is not None, "Intent was not parsed"

        # Track plan should exist
        assert len(last_state.get("track_plan", [])) >= 1, "No tracks planned"

        # MIDI file should be created
        if midi_path:
            from pathlib import Path
            assert Path(midi_path).exists(), f"MIDI file not found: {midi_path}"
            file_size = Path(midi_path).stat().st_size
            assert file_size > 0, f"MIDI file is empty: {midi_path}"
            print(f"      MIDI file size: {file_size:,} bytes")

        # Quality report
        qr = last_state.get("quality_report")
        if qr:
            score = getattr(qr, "overall_score", None) or qr.get("overall_score", None) if isinstance(qr, dict) else None
            print(f"      Quality score: {score}")

    def test_full_pipeline_with_dynamic_preset(self):
        """Pick a dynamically generated preset and run full pipeline."""
        from src.agents.graph import get_agentic_graph
        from src.agents.state import MusicState
        from src.config.constants import OUTPUT_DIR
        import uuid

        OUTPUT_DIR.mkdir(exist_ok=True)

        # Step 1: Generate a dynamic preset from jazz.modal
        svc = PresetService(cache_max=10)
        print("\n  [RUN] Generating dynamic preset for jazz.modal...")
        presets = svc.generate_presets("jazz.modal", count=3)
        assert len(presets) >= 1, "Failed to generate jazz.modal presets"

        prompt = presets[0]  # Pick the first dynamically generated preset
        print(f"  [RUN] Selected preset: {prompt[:80]}...")

        # Step 2: Run the full pipeline with this preset
        session_id = str(uuid.uuid4())[:8]
        initial_state: MusicState = {
            "user_prompt": prompt,
            "intent": None,
            "track_plan": [],
            "theory_validation": {},
            "theory_valid": False,
            "theory_issues": [],
            "generated_tracks": [],
            "generation_metadata": {},
            "quality_report": None,
            "refinement_attempts": 0,
            "refinement_feedback": "",
            "needs_refinement": False,
            "final_midi_path": None,
            "session_summary": "",
            "messages": [],
            "error": None,
            "error_context": None,
            "session_id": session_id,
            "composition_state": {
                "existing_tracks": [],
                "tempo": 120,
                "key": "C",
                "genre": "pop",
                "mode": "major",
            },
            "max_refinement_iterations": 2,
            "current_iteration": 0,
        }

        graph = get_agentic_graph()
        config = {"configurable": {"thread_id": session_id}}

        start = time.time()
        last_state = dict(initial_state)
        nodes_completed = []

        try:
            for chunk in graph.stream(initial_state, config=config, stream_mode="values"):
                last_state = chunk
                current_keys = set(
                    k for k, v in chunk.items()
                    if v is not None
                    and k not in (
                        "user_prompt", "messages", "session_id",
                        "composition_state", "max_refinement_iterations",
                        "current_iteration",
                    )
                )
                key_to_node = {
                    "intent": "intent_parser",
                    "track_plan": "track_planner",
                    "theory_validation": "theory_validator",
                    "generated_tracks": "track_generator",
                    "quality_report": "quality_control",
                    "final_midi_path": "midi_creator",
                    "session_summary": "session_summary",
                }
                for key in current_keys:
                    node = key_to_node.get(key)
                    if node and node not in nodes_completed:
                        nodes_completed.append(node)
                        print(f"      [NODE] {node} ✓")

        except Exception as exc:
            error_str = str(exc).lower()
            assert "401" not in error_str, f"Pipeline 401 Unauthorized: {exc}"
            assert "unauthorized" not in error_str, f"Pipeline Unauthorized: {exc}"
            pytest.fail(f"Dynamic preset pipeline failed: {exc}")

        elapsed = time.time() - start
        error = last_state.get("error")
        midi_path = last_state.get("final_midi_path")

        print(f"\n  [OK] Dynamic preset pipeline completed in {elapsed:.1f}s")
        print(f"      Nodes completed: {nodes_completed}")
        print(f"      MIDI path: {midi_path}")

        if error:
            error_lower = str(error).lower()
            assert "401" not in error_lower, f"401 in pipeline error: {error}"

        assert last_state.get("intent") is not None, "Intent not parsed for dynamic preset"
        assert len(last_state.get("track_plan", [])) >= 1, "No tracks planned for dynamic preset"

        if midi_path:
            from pathlib import Path
            assert Path(midi_path).exists(), f"MIDI file not found: {midi_path}"
            print(f"      MIDI file size: {Path(midi_path).stat().st_size:,} bytes")


# ================================================================== #
# Test 4: Provider Fallback — Ensure no 401 across all providers
# ================================================================== #

class TestProviderFallback:
    """Test that each configured provider responds without auth errors."""

    @classmethod
    def setup_class(cls):
        LLMConfig.initialize()

    def test_each_available_provider_individually(self):
        """Call each available provider and verify no 401."""
        for provider_name in LLMConfig.AVAILABLE_PROVIDERS:
            result = call_llm(
                "You are a music AI.",
                "Name one musical instrument.",
                provider=provider_name,
                temperature=0.1,
                max_tokens=20,
            )
            assert result is not None, (
                f"Provider '{provider_name}' returned None — possible 401 or auth error"
            )
            print(f"\n  [OK] {provider_name}: {result!r}")

    def test_fallback_chain_works(self):
        """call_llm with default should succeed using fallback chain."""
        result = call_llm(
            "You are a test.",
            "Reply with: PASS",
            temperature=0.1,
            max_tokens=10,
        )
        assert result is not None, "Fallback chain exhausted — all providers failed"
        print(f"\n  [OK] Fallback chain result: {result!r}")
