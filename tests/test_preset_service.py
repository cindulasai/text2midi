# -*- coding: utf-8 -*-
"""Tests for src.services.preset_service — Dynamic LLM-Powered Preset System."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.services.preset_service import (
    GENRE_EMOJI,
    PresetService,
    _SEED_PRESETS,
    get_preset_service,
)


# ------------------------------------------------------------------ #
# Fixtures
# ------------------------------------------------------------------ #

@pytest.fixture
def svc(tmp_path: Path) -> PresetService:
    """Fresh PresetService with small cache and isolated temp persistence."""
    return PresetService(cache_max=10, persist_path=tmp_path / "test_cache.json")


# ------------------------------------------------------------------ #
# Genre hierarchy tests
# ------------------------------------------------------------------ #

class TestGenreHierarchy:
    """Test that PresetService correctly surfaces the genre registry."""

    def test_get_root_categories_returns_16(self, svc: PresetService) -> None:
        roots = svc.get_root_categories()
        assert len(roots) == 16

    def test_root_ids_match_expected(self, svc: PresetService) -> None:
        expected = {
            "classical", "jazz", "blues", "rock", "metal",
            "electronic", "hiphop", "pop", "rnb", "folk",
            "latin", "african", "asian", "cinematic",
            "lofi", "ambient",
        }
        root_ids = {r.id for r in svc.get_root_categories()}
        assert root_ids == expected

    def test_get_sub_genres_jazz(self, svc: PresetService) -> None:
        subs = svc.get_sub_genres("jazz")
        assert len(subs) >= 10  # Jazz has 14 sub-genres
        sub_ids = {s.id for s in subs}
        assert "jazz.bebop" in sub_ids
        assert "jazz.swing" in sub_ids

    def test_get_sub_genres_electronic(self, svc: PresetService) -> None:
        subs = svc.get_sub_genres("electronic")
        assert len(subs) >= 10  # Electronic has many sub-genres

    def test_get_sub_genres_nonexistent(self, svc: PresetService) -> None:
        subs = svc.get_sub_genres("nonexistent_genre")
        assert subs == []

    def test_get_emoji_known(self) -> None:
        assert PresetService.get_emoji("jazz") == "🎷"
        assert PresetService.get_emoji("jazz.bebop") == "🎷"
        assert PresetService.get_emoji("rock") == "🎸"
        assert PresetService.get_emoji("cinematic") == "🎬"

    def test_get_emoji_unknown_defaults(self) -> None:
        assert PresetService.get_emoji("unknown") == "🎵"

    def test_display_name_root_has_count(self, svc: PresetService) -> None:
        roots = svc.get_root_categories()
        jazz = next(r for r in roots if r.id == "jazz")
        display = svc.get_display_name(jazz)
        assert "🎷" in display
        assert "Jazz" in display
        assert "(" in display  # has count


# ------------------------------------------------------------------ #
# Seed presets tests
# ------------------------------------------------------------------ #

class TestSeedPresets:
    """Test the curated seed preset fallback system."""

    def test_all_root_genres_have_seeds(self) -> None:
        root_ids = {
            "classical", "jazz", "blues", "rock", "metal",
            "electronic", "hiphop", "pop", "rnb", "folk",
            "latin", "african", "asian", "cinematic",
            "lofi", "ambient",
        }
        for gid in root_ids:
            # lofi and ambient may fall back to parent seeds
            seeds = PresetService().get_seed_presets(gid)
            assert len(seeds) >= 1, f"No seeds available for root genre: {gid}"

    def test_seed_presets_are_nonempty_strings(self) -> None:
        for gid, prompts in _SEED_PRESETS.items():
            for p in prompts:
                assert isinstance(p, str), f"Non-string seed in {gid}"
                assert len(p) >= 15, f"Seed too short in {gid}: {p!r}"

    def test_get_seed_presets_direct(self, svc: PresetService) -> None:
        seeds = svc.get_seed_presets("jazz.bebop")
        assert len(seeds) >= 2
        assert all("bebop" in s.lower() or "jazz" in s.lower() for s in seeds)

    def test_get_seed_presets_falls_back_to_root(self, svc: PresetService) -> None:
        # A sub-genre without direct seeds should fall back to root
        seeds = svc.get_seed_presets("jazz.acid")
        assert len(seeds) >= 1  # Falls back to "jazz" seeds

    def test_get_seed_presets_generates_default(self, svc: PresetService) -> None:
        seeds = svc.get_seed_presets("completely_unknown_genre")
        assert len(seeds) >= 1


# ------------------------------------------------------------------ #
# LLM generation tests (mocked)
# ------------------------------------------------------------------ #

class TestGeneratePresets:
    """Test LLM-based preset generation with mocked call_llm."""

    @patch("src.services.preset_service.call_llm")
    def test_generate_presets_parses_json(self, mock_llm: MagicMock, svc: PresetService) -> None:
        mock_llm.return_value = '["Create a cool jazz piece with muted trumpet", "Write a smooth jazz ballad with piano and bass", "Compose bebop with fast saxophone runs"]'
        prompts = svc.generate_presets("jazz.cool")
        assert len(prompts) == 3
        assert "cool jazz" in prompts[0].lower()
        mock_llm.assert_called_once()

    @patch("src.services.preset_service.call_llm")
    def test_generate_presets_handles_markdown_fences(self, mock_llm: MagicMock, svc: PresetService) -> None:
        mock_llm.return_value = '```json\n["Create a dark ambient drone with deep bass", "Generate an eerie soundscape with metallic textures"]\n```'
        prompts = svc.generate_presets("cinematic.dark_ambient")
        assert len(prompts) == 2

    @patch("src.services.preset_service.call_llm")
    def test_generate_presets_falls_back_on_llm_failure(self, mock_llm: MagicMock, svc: PresetService) -> None:
        mock_llm.return_value = None
        prompts = svc.generate_presets("jazz.bebop")
        # Should fall back to seed presets
        assert len(prompts) >= 2

    @patch("src.services.preset_service.call_llm")
    def test_generate_presets_falls_back_on_bad_json(self, mock_llm: MagicMock, svc: PresetService) -> None:
        mock_llm.return_value = "This is not JSON at all"
        prompts = svc.generate_presets("rock.punk")
        # Should fall back to seed presets
        assert len(prompts) >= 1

    @patch("src.services.preset_service.call_llm")
    def test_generate_presets_filters_short_prompts(self, mock_llm: MagicMock, svc: PresetService) -> None:
        mock_llm.return_value = '["Good prompt with enough detail here", "too short", "Another great detailed prompt for testing"]'
        prompts = svc.generate_presets("pop.synth_pop")
        # "too short" should be filtered out (< 15 chars)
        assert len(prompts) == 2

    @patch("src.services.preset_service.call_llm")
    def test_generate_presets_extracts_quoted_strings_fallback(self, mock_llm: MagicMock, svc: PresetService) -> None:
        mock_llm.return_value = 'Here are some ideas: "Create a lush electronic track with deep bass" and "Compose ambient music with floating pads"'
        prompts = svc.generate_presets("electronic.house")
        assert len(prompts) == 2


# ------------------------------------------------------------------ #
# Cache tests
# ------------------------------------------------------------------ #

class TestCache:
    """Test the LRU caching behavior."""

    @patch("src.services.preset_service.call_llm")
    def test_cache_hit_avoids_llm_call(self, mock_llm: MagicMock, svc: PresetService) -> None:
        mock_llm.return_value = '["First call prompt number one here", "First call prompt number two here"]'
        # First call
        prompts1 = svc.generate_presets("jazz.bebop")
        assert mock_llm.call_count == 1
        # Second call — should hit cache
        prompts2 = svc.generate_presets("jazz.bebop")
        assert mock_llm.call_count == 1  # No additional LLM call
        assert prompts1 == prompts2

    @patch("src.services.preset_service.call_llm")
    def test_bypass_cache_makes_new_call(self, mock_llm: MagicMock, svc: PresetService) -> None:
        mock_llm.return_value = '["First call prompt detailing jazz", "Another first call prompt for jazz"]'
        svc.generate_presets("jazz.bebop")
        assert mock_llm.call_count == 1

        mock_llm.return_value = '["Second call new fresh prompt here", "Another fresh prompt for second call"]'
        prompts = svc.generate_presets("jazz.bebop", bypass_cache=True)
        assert mock_llm.call_count == 2
        assert "Second call" in prompts[0] or "fresh" in prompts[0].lower()

    def test_cache_eviction(self, tmp_path: Path) -> None:
        svc = PresetService(cache_max=3, persist_path=tmp_path / "evict_cache.json")
        # Manually populate cache
        svc._cache_put("a", ["prompt a"])
        svc._cache_put("b", ["prompt b"])
        svc._cache_put("c", ["prompt c"])
        assert len(svc._cache) == 3

        # Adding a 4th should evict the oldest (a)
        svc._cache_put("d", ["prompt d"])
        assert len(svc._cache) == 3
        assert "a" not in svc._cache
        assert "d" in svc._cache

    def test_clear_cache(self, svc: PresetService) -> None:
        svc._cache_put("test", ["prompt"])
        assert len(svc._cache) == 1
        svc.clear_cache()
        assert len(svc._cache) == 0


# ------------------------------------------------------------------ #
# Singleton test
# ------------------------------------------------------------------ #

class TestSingleton:
    """Test the module-level singleton."""

    def test_get_preset_service_returns_same_instance(self) -> None:
        # Reset singleton for test
        import src.services.preset_service as mod
        mod._service = None
        svc1 = get_preset_service()
        svc2 = get_preset_service()
        assert svc1 is svc2


# ------------------------------------------------------------------ #
# Emoji mapping completeness
# ------------------------------------------------------------------ #

class TestEmojiMapping:
    """Ensure all root genres have emoji mappings."""

    def test_all_roots_have_emoji(self, svc: PresetService) -> None:
        for root in svc.get_root_categories():
            assert root.id in GENRE_EMOJI, f"Missing emoji for {root.id}"
