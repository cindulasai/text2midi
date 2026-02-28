# -*- coding: utf-8 -*-
"""
Deterministic pre-processor for user prompts.

Runs BEFORE the LLM call to:
  1. Normalize text (whitespace, unicode, casing for numbers)
  2. Expand common abbreviations
  3. Extract hard numbers (tempo, duration, bars) that regex can catch reliably
  4. Build an enriched prompt that gives the LLM explicit numeric context

This stage is 100% deterministic — no LLM calls.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field
from typing import Optional


# ---- Abbreviation map ----------------------------------------------------

_ABBREVIATIONS: dict[str, str] = {
    r"\bbpm\b": "beats per minute",
    r"\blofi\b": "lo-fi",
    r"\blo fi\b": "lo-fi",
    r"\brnb\b": "r&b",
    r"\br&b\b": "r&b",
    r"\bedm\b": "electronic dance music",
    r"\bdnb\b": "drum and bass",
    r"\bd&b\b": "drum and bass",
    r"\bsfx\b": "sound effects",
    r"\bsynth\b": "synthesizer",
    r"\bsax\b": "saxophone",
    r"\bkeys\b": "keyboard",
    r"\bacoustic gtr\b": "acoustic guitar",
    r"\belec gtr\b": "electric guitar",
    r"\bmin\b(?=\s|$|,)": "minutes",
    r"\bsec\b(?=\s|$|,)": "seconds",
    r"\bmins\b": "minutes",
    r"\bsecs\b": "seconds",
    # World music abbreviations
    r"\bkpop\b": "k-pop",
    r"\bjpop\b": "j-pop",
    r"\bafrobeat\b": "afrobeat",
    r"\bbossa\b": "bossa nova",
    r"\bcumbia\b": "cumbia",
    r"\breggae\b": "reggae",
    r"\btrap\b": "trap",
    r"\bdrill\b": "drill",
    r"\bphonk\b": "phonk",
    r"\bgtr\b": "guitar",
    r"\bvox\b": "vocals",
    r"\bstrgs\b": "strings",
    r"\bhh\b": "hi-hat",
    r"\bperc\b": "percussion",
}


# ---- Extracted hard numbers dataclass ------------------------------------

@dataclass
class ExtractedNumbers:
    """Numbers extracted deterministically from the prompt."""
    tempo_bpm: Optional[int] = None
    duration_seconds: Optional[int] = None
    duration_bars: Optional[int] = None
    track_count: Optional[int] = None
    channel_count: Optional[int] = None
    time_signature: Optional[str] = None

    def summary(self) -> str:
        """Human-readable summary for appending to the LLM prompt."""
        parts: list[str] = []
        if self.tempo_bpm:
            parts.append(f"Tempo: {self.tempo_bpm} BPM (explicitly stated)")
        if self.duration_seconds:
            parts.append(f"Duration: {self.duration_seconds} seconds (explicitly stated)")
        if self.duration_bars:
            parts.append(f"Duration: {self.duration_bars} bars (explicitly stated)")
        if self.track_count:
            parts.append(f"Track count: {self.track_count} (explicitly stated)")
        if self.channel_count:
            parts.append(f"Channel count: {self.channel_count} (explicitly stated)")
        if self.time_signature:
            parts.append(f"Time signature: {self.time_signature} (explicitly stated)")
        return "; ".join(parts) if parts else ""


@dataclass
class PreprocessedInput:
    """Result of the preprocessing stage."""
    original: str
    normalized: str
    extracted: ExtractedNumbers = field(default_factory=ExtractedNumbers)
    enriched_prompt: str = ""


# ---- Core functions ------------------------------------------------------

def normalize_text(text: str) -> str:
    """Normalize whitespace, unicode, and strip outer whitespace."""
    # Normalize unicode (NFC)
    text = unicodedata.normalize("NFC", text)
    # Collapse multiple spaces / tabs / newlines
    text = re.sub(r"\s+", " ", text).strip()
    return text


def expand_abbreviations(text: str) -> str:
    """Expand known music abbreviations for clarity."""
    result = text
    for pattern, replacement in _ABBREVIATIONS.items():
        result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
    return result


def extract_hard_numbers(text: str) -> ExtractedNumbers:
    """Extract explicit numeric values that regex can catch reliably.

    Handles:
      - "120 BPM", "120 beats per minute"
      - "2 minutes", "90 seconds", "1:30", "2m30s"
      - "32 bars", "16 measures"
      - "5 tracks", "4 instruments"
      - "3/4", "6/8" (time signature)
    """
    nums = ExtractedNumbers()
    text_lower = text.lower()

    # Tempo: "120 bpm", "120 beats per minute", "tempo 120", "at 120"
    tempo_patterns = [
        r"(\d{2,3})\s*(?:bpm|beats?\s*per\s*min(?:ute)?)",
        r"(?:tempo|at)\s+(\d{2,3})\b",
    ]
    for pat in tempo_patterns:
        m = re.search(pat, text_lower)
        if m:
            val = int(m.group(1))
            if 30 <= val <= 300:
                nums.tempo_bpm = val
            break

    # Duration in MM:SS or Xm Ys format
    mm_ss = re.search(r"(\d{1,2}):(\d{2})\b", text_lower)
    if mm_ss:
        mins, secs = int(mm_ss.group(1)), int(mm_ss.group(2))
        nums.duration_seconds = mins * 60 + secs
    else:
        # "2m30s", "2m 30s"
        ms_match = re.search(r"(\d{1,2})\s*m\s*(\d{1,2})\s*s", text_lower)
        if ms_match:
            nums.duration_seconds = int(ms_match.group(1)) * 60 + int(ms_match.group(2))
        else:
            # "X minutes"
            min_match = re.search(r"(\d{1,3})\s*(?:minutes?|mins?)\b", text_lower)
            if min_match:
                nums.duration_seconds = int(min_match.group(1)) * 60

            # "X seconds"  (only if no minutes found above)
            if nums.duration_seconds is None:
                sec_match = re.search(r"(\d{1,4})\s*(?:seconds?|secs?)\b", text_lower)
                if sec_match:
                    nums.duration_seconds = int(sec_match.group(1))

    # Bars/measures
    bar_match = re.search(r"(\d{1,3})\s*(?:bars?|measures?)\b", text_lower)
    if bar_match:
        nums.duration_bars = int(bar_match.group(1))

    # Track count: "5 tracks", "create 5 track", "5-track"
    track_match = re.search(r"(\d{1,2})\s*[-\s]?(?:tracks?|instruments?)\b", text_lower)
    if track_match:
        val = int(track_match.group(1))
        if 1 <= val <= 16:
            nums.track_count = val

    # Channel count: "8 channels", "8 channel", "8-channel"
    channel_match = re.search(r"(\d{1,2})\s*[-\s]?(?:channels?)\b", text_lower)
    if channel_match:
        val = int(channel_match.group(1))
        if 1 <= val <= 16:
            nums.channel_count = val

    # Infer duration from "N minutes length" or "of N minutes" if not already found
    # Handles: "5 minutes length", "of 3 minutes", "N minute long"
    if nums.duration_seconds is None:
        alt_min_patterns = [
            r"(\d{1,3})\s*(?:minutes?|mins?)\s*(?:length|long)\b",
            r"(?:of|about|around|approximately)\s+(\d{1,3})\s*(?:minutes?|mins?)",
        ]
        for pat in alt_min_patterns:
            m = re.search(pat, text_lower)
            if m:
                nums.duration_seconds = int(m.group(1)) * 60
                break

    # Cross-reference: "N track...of minutes" — if track_count was extracted
    # and nearby text says "minutes" without a number, try to use track_count
    # value as the minute count (common phrasing: "5 track...5 minutes")
    # Only if we still don't have duration and the phrasing strongly suggests it.
    if nums.duration_seconds is None:
        # "X ... of minutes length" or "X ... minutes length" where X is nearby
        min_length_match = re.search(
            r"(\d{1,3})\s+.*?(?:of\s+)?(?:minutes?|mins?)\s*(?:length|long|duration)?",
            text_lower,
        )
        if min_length_match:
            candidate = int(min_length_match.group(1))
            # Only use if it's a plausible minute count (1-60) and not already
            # consumed as track/channel count, or if it IS the track count
            # and there's explicit "minutes" nearby
            if 1 <= candidate <= 60:
                # Check that "minutes" appears after this number's context
                after_num = text_lower[min_length_match.start():]
                if re.search(r"minutes?\s*(?:length|long|duration)", after_num):
                    nums.duration_seconds = candidate * 60

    # Time signature: "3/4", "6/8", "4/4"
    ts_match = re.search(r"\b(\d{1,2}/\d{1,2})\b", text)
    if ts_match:
        nums.time_signature = ts_match.group(1)

    return nums


def build_enriched_prompt(original: str, extracted: ExtractedNumbers) -> str:
    """Combine original text with extracted context for the LLM.

    If hard numbers were found, append them as an explicit context block
    so the LLM doesn't need to re-parse them and can trust the values.
    """
    summary = extracted.summary()
    if not summary:
        return original

    return f"{original}\n\n[Extracted parameters: {summary}]"


def preprocess(text: str) -> PreprocessedInput:
    """Full preprocessing pipeline.

    Returns a PreprocessedInput with the normalized text, extracted numbers,
    and an enriched prompt ready for the LLM.
    """
    normalized = normalize_text(text)
    expanded = expand_abbreviations(normalized)
    extracted = extract_hard_numbers(expanded)
    enriched = build_enriched_prompt(expanded, extracted)

    return PreprocessedInput(
        original=text,
        normalized=expanded,
        extracted=extracted,
        enriched_prompt=enriched,
    )
