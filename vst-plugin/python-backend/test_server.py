# -*- coding: utf-8 -*-
"""Tests for the text2midi VST3 Python Backend Server."""

import importlib
import json
import os
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

# ── Ensure project root importable ────────────────────────────────────────────
_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_REPO_ROOT))
sys.path.insert(0, str(_REPO_ROOT / "vst-plugin" / "python-backend"))


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture(autouse=True)
def _reset_settings(tmp_path, monkeypatch):
    """Run each test with isolated settings & history."""
    monkeypatch.setenv("TEXT2MIDI_CONFIG_DIR", str(tmp_path / "cfg"))
    monkeypatch.setenv("TEXT2MIDI_DATA_DIR", str(tmp_path / "data"))

    from src.config.settings import AppSettings
    AppSettings._cache = {}
    AppSettings._path = tmp_path / "cfg" / "settings.json"
    yield


@pytest.fixture
def client():
    from server import app
    return TestClient(app)


# ── Health ────────────────────────────────────────────────────────────────────

class TestHealth:
    def test_health_returns_ok(self, client):
        resp = client.get("/health")
        assert resp.status_code == 200
        body = resp.json()
        assert body["status"] == "ok"
        assert body["version"] == "0.1.0"
        assert "provider" in body
        assert "available_providers" in body

    def test_health_provider_is_string(self, client):
        resp = client.get("/health")
        assert isinstance(resp.json()["provider"], str)


# ── Configure ─────────────────────────────────────────────────────────────────

class TestConfigure:
    def test_configure_sets_provider(self, client):
        resp = client.post("/configure", json={
            "provider": "groq",
            "api_key": "fake-key-123",
        })
        assert resp.status_code == 200
        body = resp.json()
        assert body["status"] == "configured"

    def test_configure_custom_provider(self, client):
        resp = client.post("/configure", json={
            "provider": "openai_custom",
            "api_key": "sk-test",
            "endpoint": "https://api.example.com/v1",
            "model": "gpt-4o",
        })
        assert resp.status_code == 200

    def test_configure_missing_fields(self, client):
        resp = client.post("/configure", json={"provider": "groq"})
        assert resp.status_code == 422  # Pydantic validation error


# ── Generate ──────────────────────────────────────────────────────────────────

class TestGenerate:
    @patch("server.LLMConfig")
    @patch("server._run_pipeline")
    def test_generate_success(self, mock_pipeline, mock_llm, client):
        mock_llm.DEFAULT_PROVIDER = "groq"
        mock_pipeline.return_value = {
            "user_prompt": "test",
            "generated_tracks": [],
            "quality_report": None,
            "intent": None,
            "composition_state": {"tempo": 120},
            "final_midi_path": "outputs/test.mid",
            "session_summary": "Generated OK",
            "error": None,
        }

        resp = client.post("/generate", json={"prompt": "ambient pads"})
        assert resp.status_code == 200
        body = resp.json()
        assert body["status"] == "completed"
        assert body["midi_path"] == "outputs/test.mid"

    @patch("server.LLMConfig")
    def test_generate_no_provider(self, mock_llm, client):
        mock_llm.DEFAULT_PROVIDER = None

        resp = client.post("/generate", json={"prompt": "hi"})
        assert resp.status_code == 503

    @patch("server.LLMConfig")
    @patch("server._run_pipeline")
    def test_generate_pipeline_error(self, mock_pipeline, mock_llm, client):
        mock_llm.DEFAULT_PROVIDER = "groq"
        mock_pipeline.side_effect = RuntimeError("LLM timeout")

        resp = client.post("/generate", json={"prompt": "funky bass"})
        assert resp.status_code == 500


# ── Generate Stream ───────────────────────────────────────────────────────────

class TestGenerateStream:
    @patch("server.LLMConfig")
    def test_stream_no_provider(self, mock_llm, client):
        mock_llm.DEFAULT_PROVIDER = None
        resp = client.get("/generate/stream", params={"session_id": "x", "prompt": "test"})
        assert resp.status_code == 503

    @patch("server.LLMConfig")
    def test_stream_missing_prompt(self, mock_llm, client):
        mock_llm.DEFAULT_PROVIDER = "groq"
        resp = client.get("/generate/stream", params={"session_id": "new-session"})
        assert resp.status_code == 400


# ── Response Formatting ──────────────────────────────────────────────────────

class TestFormatResponse:
    def test_format_empty_state(self):
        from server import _format_response
        resp = _format_response({
            "generated_tracks": [],
            "quality_report": None,
            "intent": None,
            "composition_state": {"tempo": 140},
            "final_midi_path": "",
            "session_summary": "Nothing",
            "error": None,
        })
        assert resp.status == "completed"
        assert resp.tracks == []
        assert resp.tempo == 140

    def test_format_error_state(self):
        from server import _format_response
        resp = _format_response({
            "generated_tracks": [],
            "quality_report": None,
            "intent": None,
            "composition_state": {},
            "final_midi_path": "",
            "session_summary": "",
            "error": "Something went wrong",
        })
        assert resp.status == "error"
