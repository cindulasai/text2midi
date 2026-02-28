# -*- coding: utf-8 -*-
"""
Secure API Key Storage via OS Keyring
======================================

Uses the operating system's native credential store:

- **Windows** — Windows Credential Manager
- **macOS**  — Keychain
- **Linux**  — Secret Service (GNOME Keyring / KWallet)

Falls back gracefully to plaintext storage (with restricted file
permissions) when the keyring is unavailable — headless servers, CI,
containers, WSL without a desktop session, etc.

This module is intentionally defensive: every public function swallows
exceptions and returns a safe default so the application never crashes
due to a credential-storage issue.
"""

from __future__ import annotations

import logging
import os
import stat
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

SERVICE_NAME = "text2midi"

# Cached after the first probe so we only test the keyring once
_keyring_available: Optional[bool] = None


# ------------------------------------------------------------------ #
# Internal helpers
# ------------------------------------------------------------------ #

def _check_keyring() -> bool:
    """Return *True* if the OS keyring is usable.

    Performs a real write → read → delete cycle on first call and
    caches the result.  This catches Linux environments where the
    ``keyring`` package is installed but no D-Bus secret service is
    running.
    """
    global _keyring_available
    if _keyring_available is not None:
        return _keyring_available

    try:
        import keyring                        # type: ignore[import-untyped]
        from keyring.errors import (          # type: ignore[import-untyped]
            KeyringError,
            NoKeyringError,
        )
    except ImportError:
        _keyring_available = False
        logger.debug("keyring package not installed — using file storage.")
        return False

    test_key = "__text2midi_keyring_probe__"
    try:
        keyring.set_password(SERVICE_NAME, test_key, "probe")
        result = keyring.get_password(SERVICE_NAME, test_key)
        try:
            keyring.delete_password(SERVICE_NAME, test_key)
        except Exception:
            pass  # deletion failing is acceptable
        _keyring_available = (result == "probe")
    except (NoKeyringError, KeyringError, Exception):
        _keyring_available = False

    if _keyring_available:
        logger.debug("OS keyring is available and working.")
    else:
        logger.debug("OS keyring not available; falling back to file storage.")

    return _keyring_available


# ------------------------------------------------------------------ #
# Public API
# ------------------------------------------------------------------ #

def store_key(provider_id: str, api_key: str) -> bool:
    """Store an API key in the OS keyring.

    Returns **True** if the key was persisted in the keyring (meaning
    the caller should write the sentinel :data:`KEYRING_SENTINEL` to
    JSON instead of the real key).  Returns **False** when the caller
    must keep the key in the JSON file.
    """
    if not api_key or not provider_id:
        return False
    if not _check_keyring():
        return False

    try:
        import keyring  # type: ignore[import-untyped]
        keyring.set_password(SERVICE_NAME, provider_id, api_key)
        logger.debug("Stored key for '%s' in OS keyring.", provider_id)
        return True
    except Exception as exc:
        logger.warning("Keyring store failed for '%s': %s", provider_id, exc)
        return False


def retrieve_key(provider_id: str) -> Optional[str]:
    """Retrieve an API key from the OS keyring.

    Returns the key string, or ``None`` when the keyring is
    unavailable or has no entry for *provider_id*.
    """
    if not _check_keyring():
        return None
    try:
        import keyring  # type: ignore[import-untyped]
        return keyring.get_password(SERVICE_NAME, provider_id)
    except Exception as exc:
        logger.warning("Keyring retrieve failed for '%s': %s", provider_id, exc)
        return None


def delete_key(provider_id: str) -> None:
    """Remove an API key from the OS keyring (best-effort, never raises)."""
    if not _check_keyring():
        return
    try:
        import keyring  # type: ignore[import-untyped]
        keyring.delete_password(SERVICE_NAME, provider_id)
    except Exception:
        pass  # key may not exist — that's fine


def restrict_file_permissions(filepath: Path) -> None:
    """Lock a file down to owner-only read/write.

    - **Unix**  — ``chmod 600``
    - **Windows** — ``icacls`` to remove inherited ACLs and grant the
      current user Full Control only.

    Silently does nothing when the operation is unsupported or fails.
    """
    try:
        if os.name == "nt":
            username = os.environ.get("USERNAME", "")
            if username and filepath.exists():
                os.system(
                    f'icacls "{filepath}" /inheritance:r '
                    f'/grant:r "{username}:(R,W)" >nul 2>&1'
                )
        else:
            if filepath.exists():
                filepath.chmod(stat.S_IRUSR | stat.S_IWUSR)  # 0o600
    except Exception as exc:
        logger.debug("Could not restrict permissions on %s: %s", filepath, exc)


# Sentinel value written into the JSON file when the real key lives
# in the OS keyring.  The load() path recognises this and fetches the
# actual key from the keyring at runtime.
KEYRING_SENTINEL = "__KEYRING__"
