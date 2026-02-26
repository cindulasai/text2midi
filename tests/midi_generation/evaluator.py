# -*- coding: utf-8 -*-
"""
MIDI Evaluation Engine
======================
Provides ``MidiEvaluator`` – a rule-based scorer that analyses a generated
MIDI file against a set of expected attributes derived from the generation
prompt.

Evaluation Dimensions
---------------------
1. **Structural validity** (binary gate)
   - File exists on disk
   - Non-zero file size
   - Parseable by ``mido``

2. **Tempo match** (0–1)
   - Checks that the detected BPM falls within ``expected_tempo_range``

3. **Track count match** (0–1)
   - Checks that the number of non-empty MIDI tracks falls within
     ``expected_track_count_range``

4. **Note density match** (0–1)
   - Total note count vs ``expected_note_count_range``

5. **Duration match** (0–1)
   - Estimated playback duration vs ``expected_duration_range`` (seconds)

6. **Pitch range match** (0–1)
   - Average MIDI pitch vs ``expected_pitch_range`` (MIDI note numbers)

7. **Velocity dynamics match** (0–1)
   - Checks that velocity spread (std-dev) exceeds a genre-appropriate
     minimum to avoid lifeless flat dynamics.

8. **Drum track presence** (0–1)
   - Confirms channel 9 (GM drums) is used when ``expected_has_drums=True``.

Scoring
-------
The final score is a weighted average of dimensions 2-8.  A test **passes**
when:
  - Structural gate passes (all three structural checks succeed), AND
  - Final weighted score ≥ ``pass_threshold`` (default 0.55)

This lenient threshold accounts for LLM non-determinism while still
catching clear mismatches (e.g. a 2-BPM file, empty output, wrong genre).
"""

from __future__ import annotations

import statistics
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Tuple

try:
    import mido
    _MIDO_AVAILABLE = True
except ImportError:
    _MIDO_AVAILABLE = False


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------


@dataclass
class MidiMetrics:
    """Raw metrics extracted from a MIDI file."""

    # File-level
    file_size_bytes: int = 0
    is_parseable: bool = False

    # Timing
    bpm: float = 120.0
    duration_seconds: float = 0.0
    ticks_per_beat: int = 480

    # Tracks
    track_count: int = 0
    non_empty_track_count: int = 0

    # Notes
    total_notes: int = 0
    pitch_values: list = field(default_factory=list)
    velocity_values: list = field(default_factory=list)

    # Channels
    channels_used: set = field(default_factory=set)

    # Computed properties (populated after extraction)
    avg_pitch: float = 0.0
    pitch_range: float = 0.0
    avg_velocity: float = 0.0
    velocity_stddev: float = 0.0
    has_drums: bool = False  # channel 9 present


@dataclass
class EvaluationResult:
    """Complete evaluation result for one test case."""

    test_id: str
    prompt: str
    midi_path: Optional[str]

    # Structural checks
    file_exists: bool = False
    file_nonempty: bool = False
    file_parseable: bool = False

    # Dimension scores (0.0 – 1.0 each, or None if not applicable)
    score_tempo: Optional[float] = None
    score_track_count: Optional[float] = None
    score_note_count: Optional[float] = None
    score_duration: Optional[float] = None
    score_pitch: Optional[float] = None
    score_velocity: Optional[float] = None
    score_drums: Optional[float] = None

    # Aggregated
    weighted_score: float = 0.0
    passed: bool = False
    pass_threshold: float = 0.55

    # Raw metrics snapshot
    metrics: Optional[MidiMetrics] = None

    # Human-readable notes
    notes: list = field(default_factory=list)
    failures: list = field(default_factory=list)

    @property
    def structural_ok(self) -> bool:
        return self.file_exists and self.file_nonempty and self.file_parseable

    def summary_line(self) -> str:
        status = "PASS" if self.passed else "FAIL"
        score_str = f"{self.weighted_score:.2f}" if self.structural_ok else "N/A"
        return (
            f"[{status}] {self.test_id:<30}  score={score_str:<6}  "
            f"{self.prompt[:60]}{'…' if len(self.prompt) > 60 else ''}"
        )


# ---------------------------------------------------------------------------
# Evaluator
# ---------------------------------------------------------------------------


class MidiEvaluator:
    """Assess a generated MIDI file against expected attributes.

    Usage
    -----
    >>> ev = MidiEvaluator()
    >>> result = ev.evaluate(
    ...     test_id="tc_001",
    ...     prompt="calm lo-fi hip-hop study music",
    ...     midi_path="/path/to/file.mid",
    ...     expected_tempo_range=(70, 90),
    ...     expected_track_count_range=(2, 4),
    ...     expected_note_count_range=(80, 400),
    ...     expected_duration_range=(50, 150),
    ...     expected_pitch_range=(45, 72),
    ...     expected_has_drums=True,
    ...     pass_threshold=0.55,
    ... )
    >>> print(result.summary_line())
    """

    # Dimension weights must sum to 1.0
    WEIGHTS = {
        "tempo":       0.20,
        "track_count": 0.15,
        "note_count":  0.20,
        "duration":    0.15,
        "pitch":       0.15,
        "velocity":    0.10,
        "drums":       0.05,
    }

    def evaluate(
        self,
        test_id: str,
        prompt: str,
        midi_path: Optional[str],
        *,
        expected_tempo_range: Optional[Tuple[float, float]] = None,
        expected_track_count_range: Optional[Tuple[int, int]] = None,
        expected_note_count_range: Optional[Tuple[int, int]] = None,
        expected_duration_range: Optional[Tuple[float, float]] = None,
        expected_pitch_range: Optional[Tuple[float, float]] = None,
        expected_has_drums: Optional[bool] = None,
        pass_threshold: float = 0.55,
    ) -> EvaluationResult:
        """Evaluate a MIDI file and return a structured result."""

        result = EvaluationResult(
            test_id=test_id,
            prompt=prompt,
            midi_path=midi_path,
            pass_threshold=pass_threshold,
        )

        # ── Structural gate ──────────────────────────────────────────────────
        if midi_path is None:
            result.failures.append("No MIDI path returned from generator")
            return result

        path = Path(midi_path)

        result.file_exists = path.exists()
        if not result.file_exists:
            result.failures.append(f"File not found: {midi_path}")
            return result

        result.file_nonempty = path.stat().st_size > 0
        if not result.file_nonempty:
            result.failures.append("File exists but is empty (0 bytes)")
            return result

        if not _MIDO_AVAILABLE:
            result.failures.append("mido not installed – cannot parse MIDI")
            return result

        metrics = self._extract_metrics(path)
        result.metrics = metrics

        result.file_parseable = metrics.is_parseable
        if not result.file_parseable:
            result.failures.append("File could not be parsed as valid MIDI")
            return result

        # ── Dimension scoring ────────────────────────────────────────────────
        scores: dict[str, float] = {}

        # 1. Tempo
        if expected_tempo_range is not None:
            scores["tempo"] = self._range_score(
                metrics.bpm, expected_tempo_range, label="BPM", result=result
            )

        # 2. Track count
        if expected_track_count_range is not None:
            scores["track_count"] = self._range_score(
                metrics.non_empty_track_count,
                expected_track_count_range,
                label="track_count",
                result=result,
                is_int=True,
            )

        # 3. Note count
        if expected_note_count_range is not None:
            scores["note_count"] = self._range_score(
                metrics.total_notes,
                expected_note_count_range,
                label="note_count",
                result=result,
                is_int=True,
            )

        # 4. Duration
        if expected_duration_range is not None:
            scores["duration"] = self._range_score(
                metrics.duration_seconds,
                expected_duration_range,
                label="duration_s",
                result=result,
            )

        # 5. Pitch range
        if expected_pitch_range is not None and metrics.total_notes > 0:
            scores["pitch"] = self._range_score(
                metrics.avg_pitch,
                expected_pitch_range,
                label="avg_pitch",
                result=result,
            )

        # 6. Velocity dynamics
        # We expect at least some dynamic variation (stddev > 5) for any real
        # piece.  Flat static velocity (stddev ≈ 0) is a quality failure.
        if metrics.total_notes >= 10:
            vel_stddev = metrics.velocity_stddev
            min_dynamic = 5.0  # acceptable minimum stddev
            if vel_stddev >= min_dynamic:
                scores["velocity"] = 1.0
            else:
                scores["velocity"] = vel_stddev / min_dynamic
                result.notes.append(
                    f"Low velocity dynamics: stddev={vel_stddev:.1f} (want ≥{min_dynamic})"
                )

        # 7. Drum presence
        if expected_has_drums is not None:
            has = metrics.has_drums
            if expected_has_drums:
                scores["drums"] = 1.0 if has else 0.0
                if not has:
                    result.notes.append("Drum track (ch9) expected but not found")
            else:
                # Drums not expected – penalise if present
                scores["drums"] = 0.0 if has else 1.0
                if has:
                    result.notes.append("Drum track (ch9) present but was not expected")

        # ── Aggregate ────────────────────────────────────────────────────────
        if scores:
            total_weight = sum(self.WEIGHTS[k] for k in scores)
            weighted_sum = sum(self.WEIGHTS[k] * v for k, v in scores.items())
            result.weighted_score = weighted_sum / total_weight if total_weight > 0 else 0.0
        else:
            # No dimension expectations set → structural pass is sufficient
            result.weighted_score = 1.0

        # Store individual dimension scores
        result.score_tempo       = scores.get("tempo")
        result.score_track_count = scores.get("track_count")
        result.score_note_count  = scores.get("note_count")
        result.score_duration    = scores.get("duration")
        result.score_pitch       = scores.get("pitch")
        result.score_velocity    = scores.get("velocity")
        result.score_drums       = scores.get("drums")

        result.passed = (
            result.structural_ok
            and result.weighted_score >= pass_threshold
        )

        if not result.passed and result.structural_ok:
            result.failures.append(
                f"Weighted score {result.weighted_score:.2f} < threshold {pass_threshold}"
            )

        # Annotate raw metrics summary
        result.notes.append(
            f"BPM={metrics.bpm:.0f}  tracks={metrics.non_empty_track_count}"
            f"  notes={metrics.total_notes}  dur={metrics.duration_seconds:.1f}s"
            f"  avg_pitch={metrics.avg_pitch:.0f}  vel_std={metrics.velocity_stddev:.1f}"
        )

        return result

    # ── Private helpers ──────────────────────────────────────────────────────

    def _extract_metrics(self, path: Path) -> MidiMetrics:
        """Parse a MIDI file and extract raw metrics."""
        m = MidiMetrics(file_size_bytes=path.stat().st_size)

        try:
            mid = mido.MidiFile(str(path))
            m.is_parseable = True
            m.ticks_per_beat = mid.ticks_per_beat

            # --- Tempo ---
            tempo_us = 500_000  # default 120 BPM
            for track in mid.tracks:
                for msg in track:
                    if msg.type == "set_tempo":
                        tempo_us = msg.tempo
                        break

            m.bpm = mido.tempo2bpm(tempo_us)

            # --- Track stats ---
            m.track_count = len(mid.tracks)

            total_ticks = 0
            for track in mid.tracks:
                abs_tick = 0
                track_has_notes = False
                for msg in track:
                    abs_tick += msg.time
                    total_ticks = max(total_ticks, abs_tick)
                    if msg.type == "note_on" and msg.velocity > 0:
                        track_has_notes = True
                        m.total_notes += 1
                        m.pitch_values.append(msg.note)
                        m.velocity_values.append(msg.velocity)
                        m.channels_used.add(msg.channel)
                if track_has_notes:
                    m.non_empty_track_count += 1

            # --- Duration ---
            if total_ticks > 0 and m.ticks_per_beat > 0:
                beats = total_ticks / m.ticks_per_beat
                m.duration_seconds = beats * (tempo_us / 1_000_000)

            # --- Aggregated pitch / velocity ---
            if m.pitch_values:
                m.avg_pitch = statistics.mean(m.pitch_values)
                m.pitch_range = max(m.pitch_values) - min(m.pitch_values)

            if m.velocity_values:
                m.avg_velocity = statistics.mean(m.velocity_values)
                if len(m.velocity_values) >= 2:
                    m.velocity_stddev = statistics.stdev(m.velocity_values)

            # --- Drums ---
            m.has_drums = 9 in m.channels_used

        except Exception:
            m.is_parseable = False

        return m

    @staticmethod
    def _range_score(
        value: float,
        expected_range: Tuple[float, float],
        *,
        label: str = "value",
        result: EvaluationResult,
        is_int: bool = False,
        tolerance_factor: float = 0.3,
    ) -> float:
        """Return a score in [0, 1] based on how close *value* is to *expected_range*.

        * 1.0  – value lies within the range
        * 0.5  – value is at most ``tolerance_factor`` outside the range
        * 0.0  – value is very far outside the range
        """
        lo, hi = expected_range
        if lo <= value <= hi:
            return 1.0

        # How far outside?
        if value < lo:
            gap = lo - value
            span = lo - lo * (1 - tolerance_factor) or 1
            margin = lo * tolerance_factor or tolerance_factor * 10
        else:
            gap = value - hi
            margin = hi * tolerance_factor or tolerance_factor * 10

        score = max(0.0, 1.0 - gap / margin)
        label_val = f"{value:.0f}" if is_int else f"{value:.1f}"
        result.notes.append(
            f"{label}={label_val} outside expected [{lo}, {hi}]  → dim_score={score:.2f}"
        )
        return score
