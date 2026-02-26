# -*- coding: utf-8 -*-
"""
conftest.py – shared pytest fixtures for MIDI generation tests.
"""

from __future__ import annotations

import os
import sys
import uuid
import pytest
from pathlib import Path

# ── Bootstrap ────────────────────────────────────────────────────────────────
_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_REPO_ROOT))

try:
    from dotenv import load_dotenv
    load_dotenv(_REPO_ROOT / ".env")
except ImportError:
    pass  # dotenv not installed in CI; rely on real env vars

from src.config.llm import LLMConfig
from src.agents.graph import get_agentic_graph


# ── Session-scoped fixtures ──────────────────────────────────────────────────


@pytest.fixture(scope="session", autouse=True)
def init_llm():
    """Initialize LLM configuration once per test session."""
    LLMConfig.initialize()
    yield


@pytest.fixture(scope="session")
def agentic_graph():
    """Compile and return the LangGraph once per session."""
    return get_agentic_graph()


@pytest.fixture(scope="session")
def output_dir() -> Path:
    """Directory where test-generated MIDI files are stored."""
    p = _REPO_ROOT / "tests" / "midi_generation" / "outputs"
    p.mkdir(parents=True, exist_ok=True)
    return p
