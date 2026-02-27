# -*- coding: utf-8 -*-
"""
History Manager
Persistent JSON-based history of generation sessions.
"""

from __future__ import annotations

import json
import logging
import threading
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from platformdirs import user_data_dir

logger = logging.getLogger(__name__)

_DATA_DIR = Path(user_data_dir("text2midi", ensure_exists=True))
_HISTORY_FILE = _DATA_DIR / "history.json"
_LOCK = threading.Lock()
_DEFAULT_MAX = 50


class HistoryManager:
    """Thread-safe JSON file history store."""

    @classmethod
    def _load(cls) -> List[Dict[str, Any]]:
        if not _HISTORY_FILE.exists():
            return []
        try:
            with open(_HISTORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list):
                return data
        except (json.JSONDecodeError, OSError) as exc:
            logger.warning("History file corrupt, returning empty: %s", exc)
        return []

    @classmethod
    def _save(cls, entries: List[Dict[str, Any]]) -> None:
        _HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(_HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(entries, f, indent=2, default=str)

    # ------------------------------------------------------------------ #
    # Public API
    # ------------------------------------------------------------------ #

    @classmethod
    def add_entry(
        cls,
        prompt: str,
        genre: str = "",
        quality: float = 0.0,
        midi_path: str = "",
    ) -> None:
        """Add a new entry at the top and prune to max size."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "prompt": prompt,
            "genre": genre,
            "quality": quality,
            "midi_path": midi_path,
        }
        with _LOCK:
            entries = cls._load()
            entries.insert(0, entry)
            entries = entries[:_DEFAULT_MAX]
            cls._save(entries)

    @classmethod
    def get_entries(cls, limit: int = 50) -> List[Dict[str, Any]]:
        """Return the most recent entries."""
        with _LOCK:
            entries = cls._load()
        return entries[:limit]

    @classmethod
    def remove_entry(cls, timestamp: str) -> None:
        """Remove an entry by its timestamp."""
        with _LOCK:
            entries = cls._load()
            entries = [e for e in entries if e.get("timestamp") != timestamp]
            cls._save(entries)

    @classmethod
    def clear(cls) -> None:
        """Delete all history."""
        with _LOCK:
            cls._save([])
