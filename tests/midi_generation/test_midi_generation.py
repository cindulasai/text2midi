# -*- coding: utf-8 -*-
"""
test_midi_generation.py
========================
Pytest-compatible test suite for MIDI generation.

Each ``TestCase`` in ``TEST_CASES`` is parametrized as a separate pytest test,
which means you can run any subset with standard pytest selection flags:

    # Run all 110 tests
    uv run pytest tests/midi_generation/test_midi_generation.py -v

    # Run a single test by ID
    uv run pytest tests/midi_generation/test_midi_generation.py -k "tc_001" -v

    # Run first 10 tests
    uv run pytest tests/midi_generation/test_midi_generation.py -k "tc_00" -v

    # Run tests matching a genre keyword in the prompt
    uv run pytest tests/midi_generation/test_midi_generation.py -k "jazz" -v

NOTE: These tests call the live LLM API and generate real MIDI.  Each test
can take several seconds.  Running all 110 sequentially may take 20-30 minutes
depending on the LLM provider's latency.

Set environment variable ``MIDI_TEST_DRY_RUN=1`` to skip generation and only
evaluate pre-existing MIDI files in ``tests/midi_generation/outputs/``.
"""

from __future__ import annotations

import os
import shutil
import sys
import time
import traceback
import uuid
from pathlib import Path
from typing import Optional

import pytest

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent

from tests.midi_generation.evaluator import MidiEvaluator
from tests.midi_generation.test_cases import TEST_CASES, TestCase

_DRY_RUN = os.environ.get("MIDI_TEST_DRY_RUN", "0") == "1"
_OUTPUTS_DIR = _REPO_ROOT / "tests" / "midi_generation" / "outputs"
_OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

_evaluator = MidiEvaluator()


# ============================================================================
# Generation helper (reused per test)
# ============================================================================


def _generate(tc: TestCase, agentic_graph, output_dir: Path) -> Optional[str]:
    """Run the graph for *tc* and return the path of the saved MIDI file."""
    from src.agents.state import MusicState

    session_id = str(uuid.uuid4())[:8]

    initial_state: MusicState = {
        "user_prompt": tc.prompt,
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
            "genre": "auto",
            "mode": "major",
        },
        "max_refinement_iterations": 1,
        "current_iteration": 0,
    }

    config = {"configurable": {"thread_id": session_id}}
    result = agentic_graph.invoke(initial_state, config=config)

    if result.get("error"):
        pytest.fail(
            f"Generator error for {tc.test_id}: {result['error'][:300]}",
            pytrace=False,
        )

    raw_path = result.get("final_midi_path")
    if raw_path is None:
        pytest.fail(f"No final_midi_path returned for {tc.test_id}", pytrace=False)

    src = Path(raw_path)
    if not src.exists():
        pytest.fail(f"Expected MIDI at {raw_path} but file missing", pytrace=False)

    dest = output_dir / f"{tc.test_id}_{src.name}"
    shutil.move(str(src), str(dest))
    return str(dest)


def _find_existing(tc: TestCase) -> Optional[str]:
    """Return path of an existing MIDI file for *tc* (dry-run mode)."""
    hits = list(_OUTPUTS_DIR.glob(f"{tc.test_id}_*.mid"))
    return str(hits[0]) if hits else None


# ============================================================================
# Parametrized tests
# ============================================================================

# Build human-readable IDs for each parametrized case so pytest -v shows them
_TC_IDS = [tc.test_id for tc in TEST_CASES]


@pytest.mark.parametrize("tc", TEST_CASES, ids=_TC_IDS)
def test_midi_file_generated_and_valid(tc: TestCase, agentic_graph, output_dir):
    """
    Structural test: verify that generation completes and produces a
    non-empty, parseable MIDI file.

    This test always runs, even in dry-run mode.
    """
    if _DRY_RUN:
        midi_path = _find_existing(tc)
        if midi_path is None:
            pytest.skip(f"dry-run: no pre-existing file for {tc.test_id}")
    else:
        midi_path = _generate(tc, agentic_graph, output_dir)

    result = _evaluator.evaluate(
        test_id=tc.test_id,
        prompt=tc.prompt,
        midi_path=midi_path,
        pass_threshold=tc.pass_threshold,
    )

    assert result.file_exists,    f"[{tc.test_id}] MIDI file not found at {midi_path}"
    assert result.file_nonempty,  f"[{tc.test_id}] MIDI file is empty (0 bytes)"
    assert result.file_parseable, f"[{tc.test_id}] MIDI file is not a valid/parseable MIDI"


@pytest.mark.parametrize("tc", TEST_CASES, ids=_TC_IDS)
def test_midi_content_matches_prompt(tc: TestCase, agentic_graph, output_dir):
    """
    Semantic / content evaluation test: verify that the generated MIDI
    satisfies the expected musical attributes derived from the prompt.

    This test is skipped when no expected constraints are defined for a case.

    Comment for each test case explains the specific trait being evaluated.
    """
    # Skip if test defines no specific constraints
    has_constraints = any([
        tc.expected_tempo_range,
        tc.expected_track_count_range,
        tc.expected_note_count_range,
        tc.expected_duration_range,
        tc.expected_pitch_range,
        tc.expected_has_drums is not None,
    ])
    if not has_constraints:
        pytest.skip(f"[{tc.test_id}] No content constraints defined – structural test only")

    # Find MIDI (may already exist from test_midi_file_generated_and_valid run
    # in the same session; pytest-xdist workers may not share files, so we
    # regenerate if necessary – that is fine for content evaluation).
    existing = _find_existing(tc)
    if _DRY_RUN or existing:
        midi_path = existing
        if midi_path is None:
            pytest.skip(f"dry-run: no pre-existing file for {tc.test_id}")
    else:
        midi_path = _generate(tc, agentic_graph, output_dir)

    result = _evaluator.evaluate(
        test_id=tc.test_id,
        prompt=tc.prompt,
        midi_path=midi_path,
        expected_tempo_range=tc.expected_tempo_range,
        expected_track_count_range=tc.expected_track_count_range,
        expected_note_count_range=tc.expected_note_count_range,
        expected_duration_range=tc.expected_duration_range,
        expected_pitch_range=tc.expected_pitch_range,
        expected_has_drums=tc.expected_has_drums,
        pass_threshold=tc.pass_threshold,
    )

    failure_detail = "\n  ".join(result.failures + result.notes)
    assert result.passed, (
        f"\n[{tc.test_id}] CONTENT EVALUATION FAILED\n"
        f"  Prompt    : {tc.prompt}\n"
        f"  Comment   : {tc.comment}\n"
        f"  Score     : {result.weighted_score:.2f} (threshold {tc.pass_threshold})\n"
        f"  Details   :\n  {failure_detail}"
    )
