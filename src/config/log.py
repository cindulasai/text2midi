# -*- coding: utf-8 -*-
"""
Centralized logging configuration.

Call :func:`setup_logging` once from each entry-point (``main.py``)
or  :func:`setup_logging_for_tui` from the TUI entry-point
(``main_tui.py``) before any other imports to ensure consistent output.

The TUI variant routes all logs to a file so nothing corrupts the
Textual rendering — this is the primary fix for 401 / HTTP errors
showing up as ugly text in the terminal UI.
"""

import logging
import os
import re
import sys
from pathlib import Path

_CONFIGURED = False


# ── API-key redaction filter ────────────────────────────────────────
# Catches common key prefixes: gsk_, sk-ant-, sk-, key-, AIza, xai-
_KEY_PATTERN = re.compile(
    r"(gsk_|sk-ant-|sk-|key-|AIza|xai-)[A-Za-z0-9_\-]{8,}",
)


class ApiKeyRedactionFilter(logging.Filter):
    """Replace anything that looks like an API key with '***REDACTED***'."""

    def filter(self, record: logging.LogRecord) -> bool:
        if isinstance(record.msg, str):
            record.msg = _KEY_PATTERN.sub("***REDACTED***", record.msg)
        if record.args:
            if isinstance(record.args, dict):
                record.args = {
                    k: _KEY_PATTERN.sub("***REDACTED***", str(v))
                    if isinstance(v, str) else v
                    for k, v in record.args.items()
                }
            elif isinstance(record.args, tuple):
                record.args = tuple(
                    _KEY_PATTERN.sub("***REDACTED***", str(a))
                    if isinstance(a, str) else a
                    for a in record.args
                )
        return True

# ── Noisy third-party loggers to silence ───────────────────────────
_NOISY_LOGGERS = (
    "httpx",
    "httpcore",
    "openai",
    "groq",
    "urllib3",
    "requests",
    "openai._base_client",
    "httpcore.http11",
    "httpcore.connection",
)


def _suppress_noisy_loggers() -> None:
    """Set third-party HTTP / LLM library loggers to ERROR-only."""
    for name in _NOISY_LOGGERS:
        logging.getLogger(name).setLevel(logging.ERROR)


def setup_logging(level: int = logging.INFO) -> None:
    """Configure the root logger with a clean console format.

    Uses ``%(message)s`` so existing output (``[OK]``, ``[ERROR]``, etc.)
    appears unchanged on the console.
    """
    global _CONFIGURED
    if _CONFIGURED:
        return

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("%(message)s"))
    handler.addFilter(ApiKeyRedactionFilter())

    root = logging.getLogger()
    root.setLevel(level)
    root.addHandler(handler)

    _suppress_noisy_loggers()
    _CONFIGURED = True


def setup_logging_for_tui(level: int = logging.INFO) -> None:
    """Configure logging for the Textual TUI — route to file, NOT stdout.

    Writing log messages to stdout/stderr while Textual owns the terminal
    corrupts the rendering and causes users to see raw HTTP errors (e.g. 401)
    on screen. This routes everything to ``logs/tui.log`` instead.
    """
    global _CONFIGURED
    if _CONFIGURED:
        return

    # Ensure log directory exists
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / "tui.log"

    handler = logging.FileHandler(str(log_file), encoding="utf-8")
    handler.setFormatter(
        logging.Formatter(
            "%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
            datefmt="%H:%M:%S",
        )
    )
    handler.addFilter(ApiKeyRedactionFilter())

    root = logging.getLogger()
    # Remove any existing handlers (e.g. if something imported setup_logging first)
    root.handlers.clear()
    root.setLevel(level)
    root.addHandler(handler)

    _suppress_noisy_loggers()
    _CONFIGURED = True
