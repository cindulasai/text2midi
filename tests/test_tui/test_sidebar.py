# -*- coding: utf-8 -*-
"""Tests for the dynamic sidebar tree structure."""

from __future__ import annotations

from unittest.mock import patch

import pytest

from src.services.preset_service import PresetService, get_preset_service


class TestSidebarTree:
    """Test that the sidebar tree structure matches the spec."""

    def test_root_categories_count(self) -> None:
        """16 root genre categories should be available (14 + lofi, ambient aliases)."""
        svc = PresetService()
        roots = svc.get_root_categories()
        assert len(roots) == 16

    def test_each_root_has_sub_genres(self) -> None:
        """Each root genre (except aliases) should have sub-genres."""
        svc = PresetService()
        alias_roots = {"lofi", "ambient"}  # backward-compat aliases have no children
        for root in svc.get_root_categories():
            if root.id in alias_roots:
                continue
            subs = svc.get_sub_genres(root.id)
            assert len(subs) >= 4, f"{root.id} has only {len(subs)} sub-genres"

    def test_display_names_include_emoji(self) -> None:
        """Root genre display names should include emojis."""
        svc = PresetService()
        for root in svc.get_root_categories():
            display = svc.get_display_name(root)
            # Should contain at least one emoji character (non-ASCII)
            assert any(ord(c) > 255 for c in display), f"No emoji in: {display}"

    def test_display_names_include_count(self) -> None:
        """Root genre display names with children should include child count."""
        svc = PresetService()
        alias_roots = {"lofi", "ambient"}
        for root in svc.get_root_categories():
            display = svc.get_display_name(root)
            if root.id in alias_roots:
                continue  # aliases have no children, so no count
            assert "(" in display and ")" in display, f"No count in: {display}"

    def test_sub_genre_display_names_are_clean(self) -> None:
        """Sub-genre display names should be plain text (no emoji prefix)."""
        svc = PresetService()
        subs = svc.get_sub_genres("jazz")
        for sub in subs:
            display = svc.get_display_name(sub)
            # Should be just the name like "Bebop", "Swing"
            assert display == sub.name

    @patch("src.services.preset_service.call_llm")
    def test_preset_generation_for_sub_genre(self, mock_llm) -> None:
        """Expanding a sub-genre should generate prompts."""
        mock_llm.return_value = '["Create a fast bebop piece with sax", "Write a bebop tune with piano runs", "Compose an uptempo bebop jam session"]'
        svc = PresetService()
        prompts = svc.generate_presets("jazz.bebop")
        assert len(prompts) == 3
        assert all(isinstance(p, str) for p in prompts)

    def test_seed_presets_available_offline(self) -> None:
        """Seed presets should be available for all root genres without LLM."""
        svc = PresetService()
        for root in svc.get_root_categories():
            seeds = svc.get_seed_presets(root.id)
            assert len(seeds) >= 2, f"Too few seeds for {root.id}: {seeds}"
