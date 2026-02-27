# -*- coding: utf-8 -*-
"""
Application Settings Manager
Persistent configuration using platformdirs for cross-platform config storage.
"""

import json
import logging
import os
from pathlib import Path
from typing import Any, Optional

from platformdirs import user_config_dir, user_data_dir

logger = logging.getLogger(__name__)

_CONFIG_DIR = Path(user_config_dir("text2midi", ensure_exists=True))
_DATA_DIR = Path(user_data_dir("text2midi", ensure_exists=True))
_SETTINGS_FILE = _CONFIG_DIR / "settings.json"

_DEFAULTS = {
    "provider": "",
    "api_key": "",
    "custom_endpoint": "",
    "custom_model": "",
    "theme": "dark",
    "history_max": 50,
}


class AppSettings:
    """Singleton-style persistent application settings.

    Stores configuration as JSON in the platform-specific config directory.
    Settings are loaded lazily on first access and cached in memory.
    """

    _cache: Optional[dict] = None

    # ------------------------------------------------------------------ #
    # Core API
    # ------------------------------------------------------------------ #

    @classmethod
    def _ensure_loaded(cls) -> dict:
        if cls._cache is None:
            cls.load()
        assert cls._cache is not None
        return cls._cache

    @classmethod
    def load(cls) -> dict:
        """Load settings from disk (or create defaults)."""
        if _SETTINGS_FILE.exists():
            try:
                with open(_SETTINGS_FILE, "r", encoding="utf-8") as f:
                    cls._cache = {**_DEFAULTS, **json.load(f)}
            except (json.JSONDecodeError, OSError) as exc:
                logger.warning("Settings file corrupt, using defaults: %s", exc)
                cls._cache = dict(_DEFAULTS)
        else:
            cls._cache = dict(_DEFAULTS)
        return cls._cache

    @classmethod
    def save(cls) -> None:
        """Persist current settings to disk."""
        data = cls._ensure_loaded()
        _SETTINGS_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(_SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        logger.info("Settings saved to %s", _SETTINGS_FILE)

    @classmethod
    def get(cls, key: str, default: Any = None) -> Any:
        """Return a single setting value."""
        return cls._ensure_loaded().get(key, default)

    @classmethod
    def set(cls, key: str, value: Any) -> None:
        """Set a single setting value (does NOT auto-save)."""
        cls._ensure_loaded()[key] = value

    @classmethod
    def update(cls, **kwargs: Any) -> None:
        """Bulk-update settings (does NOT auto-save)."""
        cls._ensure_loaded().update(kwargs)

    @classmethod
    def reset(cls) -> None:
        """Reset all settings to defaults."""
        cls._cache = dict(_DEFAULTS)

    # ------------------------------------------------------------------ #
    # Environment bridge
    # ------------------------------------------------------------------ #

    @classmethod
    def apply_to_environment(cls) -> None:
        """Push the stored API key into the correct environment variable
        so that ``LLMConfig.initialize()`` picks it up."""
        data = cls._ensure_loaded()
        provider = data.get("provider", "")
        api_key = data.get("api_key", "")

        if not api_key:
            return

        env_map = {
            "minimax": "MINIMAX_API_KEY",
            "groq": "GROQ_API_KEY",
            "openai_custom": "OPENAI_CUSTOM_API_KEY",
        }
        env_var = env_map.get(provider)
        if env_var:
            os.environ[env_var] = api_key
            logger.info("Set %s from AppSettings", env_var)

        # For openai_custom, also set endpoint / model
        if provider == "openai_custom":
            endpoint = data.get("custom_endpoint", "")
            model = data.get("custom_model", "")
            if endpoint:
                os.environ["OPENAI_CUSTOM_ENDPOINT"] = endpoint
            if model:
                os.environ["OPENAI_CUSTOM_MODEL"] = model

    # ------------------------------------------------------------------ #
    # Convenience helpers
    # ------------------------------------------------------------------ #

    @classmethod
    def config_dir(cls) -> Path:
        return _CONFIG_DIR

    @classmethod
    def data_dir(cls) -> Path:
        return _DATA_DIR

    @classmethod
    def settings_path(cls) -> Path:
        return _SETTINGS_FILE

    @classmethod
    def is_configured(cls) -> bool:
        """Return True when a provider and API key are present."""
        data = cls._ensure_loaded()
        return bool(data.get("provider")) and bool(data.get("api_key"))
