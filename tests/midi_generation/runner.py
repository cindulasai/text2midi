# -*- coding: utf-8 -*-
"""
MIDI Generation Test Runner
============================
Runs all (or a subset of) ``TEST_CASES`` against the live agentic MIDI
generation pipeline, evaluates each output, and writes a machine-readable
JSON report plus a human-readable Markdown summary.

Usage
-----
Run all 110 tests (generates real MIDI files, requires API keys):

    uv run python tests/midi_generation/runner.py

Run only the first 10 tests:

    uv run python tests/midi_generation/runner.py --limit 10

Run a specific test by ID:

    uv run python tests/midi_generation/runner.py --filter tc_001

Dry-run mode (evaluate already-generated files, skip LLM):

    uv run python tests/midi_generation/runner.py --dry-run

Output files are written to:
  tests/midi_generation/outputs/     – generated MIDI files
  tests/midi_generation/reports/     – JSON + Markdown reports
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import traceback
import uuid
from datetime import datetime
from pathlib import Path

# ── Bootstrap path so we can import src.* from anywhere ─────────────────────
_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_REPO_ROOT))

# Load .env before importing anything that reads env vars
from dotenv import load_dotenv
load_dotenv(_REPO_ROOT / ".env")

from src.config.llm import LLMConfig, call_llm   # noqa: E402 (after path setup)
from src.agents.graph import get_agentic_graph     # noqa: E402
from src.agents.state import MusicState            # noqa: E402
from tests.midi_generation.evaluator import MidiEvaluator  # noqa: E402
from tests.midi_generation.test_cases import TEST_CASES, TestCase  # noqa: E402

# ── Constants ────────────────────────────────────────────────────────────────
OUTPUTS_DIR = _REPO_ROOT / "tests" / "midi_generation" / "outputs"
REPORTS_DIR = _REPO_ROOT / "tests" / "midi_generation" / "reports"
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# Delay between test cases to avoid hammering the API rate-limit
INTER_TEST_DELAY_SECONDS = 1.5


# ============================================================================
# Generation helper
# ============================================================================


def _build_initial_state(test_case: TestCase, session_id: str) -> MusicState:
    """Create the initial ``MusicState`` dict for a test case."""
    return {
        "user_prompt": test_case.prompt,
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


def generate_midi_for_test(
    test_case: TestCase,
    graph,
    output_dir: Path,
) -> tuple[str | None, str | None, float]:
    """Run the agentic graph for one test case.

    Returns
    -------
    (midi_path, error_message, elapsed_seconds)
    """
    session_id = str(uuid.uuid4())[:8]
    initial_state = _build_initial_state(test_case, session_id)
    config = {"configurable": {"thread_id": session_id}}

    t0 = time.monotonic()
    try:
        result = graph.invoke(initial_state, config=config)
        elapsed = time.monotonic() - t0

        if result.get("error"):
            return None, result["error"], elapsed

        raw_path = result.get("final_midi_path")
        if raw_path is None:
            return None, "Graph returned no final_midi_path", elapsed

        # Move/copy to test output dir so each run is archived
        src = Path(raw_path)
        if src.exists():
            dest = output_dir / f"{test_case.test_id}_{src.name}"
            src.rename(dest)
            return str(dest), None, elapsed
        else:
            return None, f"Expected MIDI file not found at {raw_path}", elapsed

    except Exception as exc:
        elapsed = time.monotonic() - t0
        return None, f"{type(exc).__name__}: {exc}\n{traceback.format_exc()}", elapsed


# ============================================================================
# Runner
# ============================================================================


class TestRunner:
    """Orchestrates generation, evaluation and reporting."""

    def __init__(
        self,
        test_cases: list[TestCase],
        dry_run: bool = False,
        verbose: bool = False,
    ) -> None:
        self.test_cases = test_cases
        self.dry_run = dry_run
        self.verbose = verbose
        self.evaluator = MidiEvaluator()
        self.graph = None
        self._results: list[dict] = []

    def run(self) -> dict:
        """Run all test cases and return a summary dict."""
        print(f"\n{'='*70}")
        print(f"  MIDI Generation Test Runner")
        print(f"  Running {len(self.test_cases)} test cases")
        print(f"  Dry-run: {self.dry_run}")
        print(f"  Provider: {LLMConfig.DEFAULT_PROVIDER}  "
              f"Available: {LLMConfig.AVAILABLE_PROVIDERS}")
        print(f"{'='*70}\n")

        if not self.dry_run:
            print("[INIT] Loading agentic graph…")
            self.graph = get_agentic_graph()
            print("[INIT] Graph ready.\n")

        start_time = time.monotonic()
        passed = 0
        failed = 0

        for idx, tc in enumerate(self.test_cases, start=1):
            print(f"[{idx:>3}/{len(self.test_cases)}] {tc.test_id}  – {tc.prompt[:55]}…")

            # ── Generation step ──────────────────────────────────────────────
            midi_path: str | None = None
            gen_error: str | None = None
            elapsed: float = 0.0

            if self.dry_run:
                # Look for existing file in output dir matching test_id prefix
                existing = list(OUTPUTS_DIR.glob(f"{tc.test_id}_*.mid"))
                if existing:
                    midi_path = str(existing[0])
                    print(f"         [dry-run] Using existing: {existing[0].name}")
                else:
                    gen_error = "dry-run: no pre-existing file found"
            else:
                midi_path, gen_error, elapsed = generate_midi_for_test(
                    tc, self.graph, OUTPUTS_DIR
                )
                if gen_error:
                    print(f"         [GEN FAIL] {gen_error[:120]}")

            # ── Evaluation step ──────────────────────────────────────────────
            eval_result = self.evaluator.evaluate(
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

            status_icon = "✓" if eval_result.passed else "✗"
            score_str = f"{eval_result.weighted_score:.2f}" if eval_result.structural_ok else "N/A"
            print(
                f"         [{status_icon}] score={score_str:<5}  "
                f"gen={elapsed:.1f}s  "
                + (f"bpm={eval_result.metrics.bpm:.0f}" if eval_result.metrics else "no-metrics")
            )

            if self.verbose and (eval_result.failures or eval_result.notes):
                for msg in eval_result.failures:
                    print(f"              FAIL: {msg}")
                for msg in eval_result.notes:
                    print(f"              note: {msg}")

            if eval_result.passed:
                passed += 1
            else:
                failed += 1

            # ── Collect structured result ────────────────────────────────────
            self._results.append({
                "test_id":        tc.test_id,
                "comment":        tc.comment,
                "prompt":         tc.prompt,
                "passed":         eval_result.passed,
                "weighted_score": round(eval_result.weighted_score, 4),
                "pass_threshold": tc.pass_threshold,
                "midi_path":      midi_path or "",
                "gen_error":      gen_error or "",
                "elapsed_s":      round(elapsed, 2),
                "structural": {
                    "file_exists":    eval_result.file_exists,
                    "file_nonempty":  eval_result.file_nonempty,
                    "file_parseable": eval_result.file_parseable,
                },
                "dimension_scores": {
                    "tempo":       eval_result.score_tempo,
                    "track_count": eval_result.score_track_count,
                    "note_count":  eval_result.score_note_count,
                    "duration":    eval_result.score_duration,
                    "pitch":       eval_result.score_pitch,
                    "velocity":    eval_result.score_velocity,
                    "drums":       eval_result.score_drums,
                },
                "expected": {
                    "tempo_range":       tc.expected_tempo_range,
                    "track_count_range": tc.expected_track_count_range,
                    "note_count_range":  tc.expected_note_count_range,
                    "duration_range":    tc.expected_duration_range,
                    "pitch_range":       tc.expected_pitch_range,
                    "has_drums":         tc.expected_has_drums,
                },
                "metrics": {
                    "bpm":             round(eval_result.metrics.bpm, 1) if eval_result.metrics else None,
                    "tracks":          eval_result.metrics.non_empty_track_count if eval_result.metrics else None,
                    "notes":           eval_result.metrics.total_notes if eval_result.metrics else None,
                    "duration_s":      round(eval_result.metrics.duration_seconds, 1) if eval_result.metrics else None,
                    "avg_pitch":       round(eval_result.metrics.avg_pitch, 1) if eval_result.metrics else None,
                    "vel_stddev":      round(eval_result.metrics.velocity_stddev, 1) if eval_result.metrics else None,
                    "has_drums":       eval_result.metrics.has_drums if eval_result.metrics else None,
                    "file_size_bytes": eval_result.metrics.file_size_bytes if eval_result.metrics else None,
                },
                "notes":    eval_result.notes,
                "failures": eval_result.failures,
            })

            # Rate-limit guard
            if not self.dry_run and idx < len(self.test_cases):
                time.sleep(INTER_TEST_DELAY_SECONDS)

        total_elapsed = time.monotonic() - start_time

        summary = {
            "run_timestamp": datetime.utcnow().isoformat() + "Z",
            "provider": LLMConfig.DEFAULT_PROVIDER,
            "total_tests":  len(self.test_cases),
            "passed":       passed,
            "failed":       failed,
            "pass_rate":    round(passed / len(self.test_cases) * 100, 1) if self.test_cases else 0,
            "total_elapsed_s": round(total_elapsed, 1),
            "results": self._results,
        }

        self._print_summary(summary)
        self._write_json_report(summary)
        self._write_markdown_report(summary)

        return summary

    # ── Reporting helpers ────────────────────────────────────────────────────

    @staticmethod
    def _print_summary(summary: dict) -> None:
        passed = summary["passed"]
        failed = summary["failed"]
        total  = summary["total_tests"]
        rate   = summary["pass_rate"]

        print(f"\n{'='*70}")
        print(f"  TEST SUMMARY")
        print(f"  Passed : {passed}/{total}  ({rate}%)")
        print(f"  Failed : {failed}/{total}")
        print(f"  Time   : {summary['total_elapsed_s']}s")
        print(f"{'='*70}")

        if failed:
            print("\n  Failed tests:")
            for r in summary["results"]:
                if not r["passed"]:
                    score = f"{r['weighted_score']:.2f}" if r["structural"]["file_parseable"] else "N/A"
                    print(f"    ✗ {r['test_id']:<12} score={score}  {r['prompt'][:50]}")
                    for f in r["failures"]:
                        print(f"        → {f}")

    def _write_json_report(self, summary: dict) -> None:
        ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        path = REPORTS_DIR / f"report_{ts}.json"
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(summary, fh, indent=2, default=str)
        print(f"\n[REPORT] JSON  → {path}")

    def _write_markdown_report(self, summary: dict) -> None:
        ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        path = REPORTS_DIR / f"report_{ts}.md"

        lines = [
            "# MIDI Generation Test Report",
            "",
            f"**Date**: {summary['run_timestamp']}  ",
            f"**Provider**: `{summary['provider']}`  ",
            f"**Pass rate**: {summary['pass_rate']}% ({summary['passed']}/{summary['total_tests']})  ",
            f"**Total time**: {summary['total_elapsed_s']}s",
            "",
            "## Results",
            "",
            "| # | ID | Status | Score | BPM | Tracks | Notes | Dur(s) | Comment |",
            "|---|-----|--------|-------|-----|--------|-------|--------|---------|",
        ]

        for r in summary["results"]:
            status = "✓ PASS" if r["passed"] else "✗ FAIL"
            score  = f"{r['weighted_score']:.2f}" if r["structural"]["file_parseable"] else "N/A"
            m = r["metrics"]
            bpm     = f"{m['bpm']:.0f}" if m.get("bpm") else "—"
            tracks  = str(m.get("tracks") or "—")
            notes   = str(m.get("notes") or "—")
            dur     = f"{m['duration_s']:.0f}" if m.get("duration_s") else "—"
            comment = r["comment"].replace("|", "╎")
            lines.append(
                f"| {r['test_id'].replace('tc_', '')} | `{r['test_id']}` | {status} "
                f"| {score} | {bpm} | {tracks} | {notes} | {dur} | {comment} |"
            )

        lines += [
            "",
            "## Failed Tests (detail)",
            "",
        ]
        for r in summary["results"]:
            if not r["passed"]:
                lines.append(f"### `{r['test_id']}`")
                lines.append(f"**Prompt**: {r['prompt']}  ")
                lines.append(f"**Comment**: {r['comment']}  ")
                lines.append(f"**Score**: {r['weighted_score']:.2f}  ")
                if r["gen_error"]:
                    lines.append(f"**Generation error**: `{r['gen_error'][:200]}`")
                for failure in r["failures"]:
                    lines.append(f"- {failure}")
                for note in r["notes"]:
                    lines.append(f"  - *{note}*")
                lines.append("")

        with open(path, "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines))
        print(f"[REPORT] MD    → {path}")


# ============================================================================
# CLI entry-point
# ============================================================================


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run MIDI generation tests and evaluate outputs."
    )
    parser.add_argument(
        "--limit", type=int, default=None,
        help="Only run the first N test cases.",
    )
    parser.add_argument(
        "--filter", type=str, default=None,
        help="Only run test cases whose ID contains this substring (e.g. tc_001).",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Skip generation; evaluate pre-existing MIDI files in outputs/.",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true",
        help="Print per-test notes and failure details inline.",
    )
    args = parser.parse_args()

    # Initialise LLM
    LLMConfig.initialize()

    # Filter test cases
    cases = TEST_CASES
    if args.filter:
        cases = [tc for tc in cases if args.filter.lower() in tc.test_id.lower()]
        print(f"[INFO] Filtered to {len(cases)} test cases matching '{args.filter}'")
    if args.limit:
        cases = cases[: args.limit]
        print(f"[INFO] Limited to first {args.limit} test cases")

    if not cases:
        print("[ERROR] No test cases to run.")
        sys.exit(1)

    runner = TestRunner(cases, dry_run=args.dry_run, verbose=args.verbose)
    summary = runner.run()

    sys.exit(0 if summary["failed"] == 0 else 1)


if __name__ == "__main__":
    main()
