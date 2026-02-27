# -*- coding: utf-8 -*-
"""Tests for HistoryManager."""

from unittest.mock import patch

import pytest

from src.tui.history import HistoryManager


@pytest.fixture(autouse=True)
def _clean_history(tmp_path):
    """Use a temp directory for history during tests."""
    history_file = tmp_path / "history.json"
    with patch("src.tui.history._HISTORY_FILE", history_file):
        yield


class TestHistoryManager:
    def test_empty_initially(self):
        entries = HistoryManager.get_entries()
        assert entries == []

    def test_add_and_retrieve(self):
        HistoryManager.add_entry("jazz prompt", genre="jazz", quality=0.85)
        entries = HistoryManager.get_entries()
        assert len(entries) == 1
        assert entries[0]["prompt"] == "jazz prompt"
        assert entries[0]["genre"] == "jazz"
        assert entries[0]["quality"] == 0.85

    def test_most_recent_first(self):
        HistoryManager.add_entry("first")
        HistoryManager.add_entry("second")
        HistoryManager.add_entry("third")
        entries = HistoryManager.get_entries()
        assert entries[0]["prompt"] == "third"
        assert entries[2]["prompt"] == "first"

    def test_limit(self):
        for i in range(10):
            HistoryManager.add_entry(f"prompt {i}")
        entries = HistoryManager.get_entries(limit=3)
        assert len(entries) == 3

    def test_prune_to_max(self):
        with patch("src.tui.history._DEFAULT_MAX", 5):
            for i in range(10):
                HistoryManager.add_entry(f"prompt {i}")
            entries = HistoryManager.get_entries()
            assert len(entries) == 5
            # Most recent should be last added
            assert entries[0]["prompt"] == "prompt 9"

    def test_remove_entry(self):
        HistoryManager.add_entry("to-keep")
        HistoryManager.add_entry("to-remove")
        entries = HistoryManager.get_entries()
        ts = entries[0]["timestamp"]  # to-remove is first (most recent)
        HistoryManager.remove_entry(ts)
        remaining = HistoryManager.get_entries()
        assert len(remaining) == 1
        assert remaining[0]["prompt"] == "to-keep"

    def test_clear(self):
        HistoryManager.add_entry("a")
        HistoryManager.add_entry("b")
        HistoryManager.clear()
        assert HistoryManager.get_entries() == []
