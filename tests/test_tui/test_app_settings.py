# -*- coding: utf-8 -*-
"""Tests for AppSettings."""

import json
import os
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from src.config.settings import AppSettings


@pytest.fixture(autouse=True)
def _clean_settings(tmp_path):
    """Use a temp directory for settings during tests."""
    settings_file = tmp_path / "settings.json"
    with patch("src.config.settings._SETTINGS_FILE", settings_file), \
         patch("src.config.settings._CONFIG_DIR", tmp_path):
        AppSettings._cache = None
        yield
        AppSettings._cache = None


class TestAppSettingsBasic:
    def test_load_defaults_when_no_file(self):
        data = AppSettings.load()
        assert data["provider"] == ""
        assert data["api_key"] == ""
        assert data["theme"] == "dark"
        assert data["history_max"] == 50

    def test_set_and_get(self):
        AppSettings.set("provider", "minimax")
        assert AppSettings.get("provider") == "minimax"

    def test_get_default(self):
        assert AppSettings.get("nonexistent", "fallback") == "fallback"

    def test_save_and_reload(self, tmp_path):
        AppSettings.set("provider", "groq")
        AppSettings.set("api_key", "test-key-123")
        AppSettings.save()

        # Force reload
        AppSettings._cache = None
        data = AppSettings.load()
        assert data["provider"] == "groq"
        assert data["api_key"] == "test-key-123"

    def test_update_bulk(self):
        AppSettings.update(provider="minimax", api_key="sk-test")
        assert AppSettings.get("provider") == "minimax"
        assert AppSettings.get("api_key") == "sk-test"

    def test_reset(self):
        AppSettings.set("provider", "groq")
        AppSettings.reset()
        assert AppSettings.get("provider") == ""

    def test_is_configured(self):
        assert not AppSettings.is_configured()
        AppSettings.update(provider="groq", api_key="sk-test")
        assert AppSettings.is_configured()


class TestAppSettingsEnvironment:
    def test_apply_minimax_key(self):
        AppSettings.update(provider="minimax", api_key="sk-minimax-test")
        AppSettings.apply_to_environment()
        assert os.environ.get("MINIMAX_API_KEY") == "sk-minimax-test"
        # Cleanup
        os.environ.pop("MINIMAX_API_KEY", None)

    def test_apply_groq_key(self):
        AppSettings.update(provider="groq", api_key="gsk-test")
        AppSettings.apply_to_environment()
        assert os.environ.get("GROQ_API_KEY") == "gsk-test"
        os.environ.pop("GROQ_API_KEY", None)

    def test_apply_custom_endpoint(self):
        AppSettings.update(
            provider="openai_custom",
            api_key="custom-key",
            custom_endpoint="http://localhost:1234/v1",
            custom_model="llama3",
        )
        AppSettings.apply_to_environment()
        assert os.environ.get("OPENAI_CUSTOM_API_KEY") == "custom-key"
        assert os.environ.get("OPENAI_CUSTOM_ENDPOINT") == "http://localhost:1234/v1"
        assert os.environ.get("OPENAI_CUSTOM_MODEL") == "llama3"
        os.environ.pop("OPENAI_CUSTOM_API_KEY", None)
        os.environ.pop("OPENAI_CUSTOM_ENDPOINT", None)
        os.environ.pop("OPENAI_CUSTOM_MODEL", None)


class TestAppSettingsEdgeCases:
    def test_corrupt_json(self, tmp_path):
        """Loading a corrupt file should fall back to defaults."""
        settings_file = tmp_path / "settings.json"
        settings_file.write_text("{invalid json!!", encoding="utf-8")
        with patch("src.config.settings._SETTINGS_FILE", settings_file):
            AppSettings._cache = None
            data = AppSettings.load()
            assert data["provider"] == ""
