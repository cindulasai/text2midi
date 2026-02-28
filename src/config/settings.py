# -*- coding: utf-8 -*-
"""
Application Settings Manager
Persistent configuration using platformdirs for cross-platform config storage.

Settings are stored as JSON at::

    <platform config dir>/text2midi/settings.json

New multi-provider format (v2)::

    {
      "providers": [
        {"id": "groq", "api_key": "gsk_...", "model": "llama-3.3-70b-versatile"},
        {"id": "anthropic", "api_key": "sk-ant-...", "model": "claude-sonnet-4-20250514"}
      ],
      "primary_provider": "groq",
      "theme": "dark",
      ...
    }

Legacy single-provider format (v1) is auto-migrated on first load.
"""

import json
import logging
import os
from pathlib import Path
from typing import Any, Optional

from platformdirs import user_config_dir, user_data_dir

from src.config.keyring_store import (
    KEYRING_SENTINEL,
    retrieve_key,
    restrict_file_permissions,
    store_key,
)

logger = logging.getLogger(__name__)

_CONFIG_DIR = Path(user_config_dir("text2midi", ensure_exists=True))
_DATA_DIR = Path(user_data_dir("text2midi", ensure_exists=True))
_SETTINGS_FILE = _CONFIG_DIR / "settings.json"

_DEFAULTS = {
    # ── New multi-provider format ──
    "providers": [],          # list of {"id", "api_key", "model", "endpoint"}
    "primary_provider": "",   # id of the default provider
    # ── Legacy single-provider (kept for migration) ──
    "provider": "",
    "api_key": "",
    "custom_endpoint": "",
    "custom_model": "",
    # ── App preferences ──
    "theme": "dark",
    "history_max": 50,
    "preset_cache_max": 100,
    # ── Internal ──
    "_settings_version": 2,
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
        """Load settings from disk (or create defaults).

        Automatically migrates legacy single-provider format to the
        new multi-provider list.
        """
        if _SETTINGS_FILE.exists():
            try:
                with open(_SETTINGS_FILE, "r", encoding="utf-8") as f:
                    cls._cache = {**_DEFAULTS, **json.load(f)}
            except (json.JSONDecodeError, OSError) as exc:
                logger.warning("Settings file corrupt, using defaults: %s", exc)
                cls._cache = dict(_DEFAULTS)
        else:
            cls._cache = dict(_DEFAULTS)

        # Restore API keys from OS keyring where sentinels are found
        cls._restore_keys_from_keyring()

        cls._migrate_v1_to_v2()
        return cls._cache

    @classmethod
    def save(cls) -> None:
        """Persist current settings to disk.

        API keys are moved to OS keyring when available.  The JSON file
        stores the sentinel ``__KEYRING__`` instead of the real secret.
        """
        data = cls._ensure_loaded()
        _SETTINGS_FILE.parent.mkdir(parents=True, exist_ok=True)

        # Deep-copy the data so we can strip keys for disk without
        # altering the in-memory cache.
        disk_data = json.loads(json.dumps(data))

        # Move provider API keys into the OS keyring
        for entry in disk_data.get("providers", []):
            pid = entry.get("id", "")
            key = entry.get("api_key", "")
            if key and key != KEYRING_SENTINEL:
                if store_key(pid, key):
                    entry["api_key"] = KEYRING_SENTINEL

        # Legacy single-provider field
        legacy_key = disk_data.get("api_key", "")
        if legacy_key and legacy_key != KEYRING_SENTINEL:
            legacy_pid = disk_data.get("provider", "legacy")
            if store_key(f"legacy_{legacy_pid}", legacy_key):
                disk_data["api_key"] = KEYRING_SENTINEL

        with open(_SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(disk_data, f, indent=2)

        restrict_file_permissions(_SETTINGS_FILE)
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
    # Keyring integration
    # ------------------------------------------------------------------ #

    @classmethod
    def _restore_keys_from_keyring(cls) -> None:
        """Replace ``__KEYRING__`` sentinels with real keys from OS keyring."""
        assert cls._cache is not None
        data = cls._cache

        for entry in data.get("providers", []):
            pid = entry.get("id", "")
            if entry.get("api_key") == KEYRING_SENTINEL:
                real = retrieve_key(pid)
                if real:
                    entry["api_key"] = real
                else:
                    logger.warning(
                        "Could not retrieve key for provider '%s' from keyring", pid
                    )
                    entry["api_key"] = ""

        # Legacy single-provider field
        if data.get("api_key") == KEYRING_SENTINEL:
            legacy_pid = data.get("provider", "legacy")
            real = retrieve_key(f"legacy_{legacy_pid}")
            if real:
                data["api_key"] = real
            else:
                data["api_key"] = ""

    # ------------------------------------------------------------------ #
    # Migration
    # ------------------------------------------------------------------ #

    @classmethod
    def _migrate_v1_to_v2(cls) -> None:
        """Migrate legacy single-provider settings to multi-provider list.

        If the old ``provider`` + ``api_key`` fields are set but the new
        ``providers`` list is empty, create a list entry and set
        ``primary_provider``.  This is a one-time silent migration.
        """
        assert cls._cache is not None
        data = cls._cache

        if data.get("_settings_version", 1) >= 2 and data.get("providers"):
            return  # already migrated

        old_provider = data.get("provider", "")
        old_key = data.get("api_key", "")

        if old_provider and old_key:
            entry: dict[str, str] = {"id": old_provider, "api_key": old_key}
            endpoint = data.get("custom_endpoint", "")
            model = data.get("custom_model", "")
            if endpoint:
                entry["endpoint"] = endpoint
            if model:
                entry["model"] = model

            existing = data.get("providers", [])
            if not any(e.get("id") == old_provider for e in existing):
                existing.append(entry)
                data["providers"] = existing

            if not data.get("primary_provider"):
                data["primary_provider"] = old_provider

            data["_settings_version"] = 2
            logger.info(
                "Migrated legacy settings to multi-provider (provider=%s)",
                old_provider,
            )

    # ------------------------------------------------------------------ #
    # Multi-provider helpers
    # ------------------------------------------------------------------ #

    @classmethod
    def add_provider(cls, provider_id: str, api_key: str = "",
                     model: str = "", endpoint: str = "",
                     set_primary: bool = False) -> None:
        """Add or update a provider in the multi-provider list.

        Also updates the legacy ``provider`` / ``api_key`` fields so
        ``is_configured()`` keeps working for all code paths.
        """
        data = cls._ensure_loaded()
        providers = data.get("providers", [])

        entry = {"id": provider_id, "api_key": api_key}
        if model:
            entry["model"] = model
        if endpoint:
            entry["endpoint"] = endpoint

        # Replace existing entry with same id, or append
        providers = [e for e in providers if e.get("id") != provider_id]
        providers.append(entry)
        data["providers"] = providers

        if set_primary or not data.get("primary_provider"):
            data["primary_provider"] = provider_id

        # Keep legacy fields in sync for backward compat
        if set_primary or not data.get("provider"):
            data["provider"] = provider_id
            data["api_key"] = api_key
            if endpoint:
                data["custom_endpoint"] = endpoint
            if model:
                data["custom_model"] = model

        data["_settings_version"] = 2

    @classmethod
    def remove_provider(cls, provider_id: str) -> None:
        """Remove a provider from the list."""
        data = cls._ensure_loaded()
        providers = data.get("providers", [])
        data["providers"] = [e for e in providers if e.get("id") != provider_id]

        # If removed provider was primary, pick the next one
        if data.get("primary_provider") == provider_id:
            remaining = data["providers"]
            data["primary_provider"] = remaining[0]["id"] if remaining else ""

    @classmethod
    def get_configured_providers(cls) -> list[dict]:
        """Return the list of configured provider entries."""
        return cls._ensure_loaded().get("providers", [])

    @classmethod
    def get_primary_provider_id(cls) -> str:
        """Return the id of the primary provider, or empty string."""
        return cls._ensure_loaded().get("primary_provider", "")

    # ------------------------------------------------------------------ #
    # Environment bridge
    # ------------------------------------------------------------------ #

    @classmethod
    def apply_to_environment(cls) -> None:
        """Push stored API keys into environment variables so that
        ``LLMConfig.initialize()`` picks them up.

        Handles both the new multi-provider list and the legacy
        single-provider fields.
        """
        data = cls._ensure_loaded()

        # ── New multi-provider list ──
        from src.config.provider_catalog import get_env_var_for_provider

        for entry in data.get("providers", []):
            pid = entry.get("id", "")
            api_key = entry.get("api_key", "")
            endpoint = entry.get("endpoint", "")
            model = entry.get("model", "")

            if api_key:
                env_var = get_env_var_for_provider(pid)
                if env_var:
                    os.environ[env_var] = api_key
                    logger.debug("Set %s from AppSettings providers list", env_var)

            # Custom endpoint vars
            if pid in ("custom", "openai_custom") and endpoint:
                os.environ["OPENAI_CUSTOM_API_KEY"] = api_key
                os.environ["OPENAI_CUSTOM_ENDPOINT"] = endpoint
                if model:
                    os.environ["OPENAI_CUSTOM_MODEL"] = model

        # ── Legacy single-provider fallback ──
        provider = data.get("provider", "")
        api_key = data.get("api_key", "")

        if api_key and provider:
            env_map = {
                "minimax": "MINIMAX_API_KEY",
                "groq": "GROQ_API_KEY",
                "openai_custom": "OPENAI_CUSTOM_API_KEY",
            }
            env_var = env_map.get(provider)
            if env_var:
                os.environ[env_var] = api_key
                logger.debug("Set %s from legacy AppSettings", env_var)

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
        """Return True when at least one provider with an API key is present.

        Checks both new multi-provider list and legacy single-provider fields.
        """
        data = cls._ensure_loaded()

        # New format
        providers = data.get("providers", [])
        for entry in providers:
            pid = entry.get("id", "")
            key = entry.get("api_key", "")
            # Ollama doesn't need an API key
            if pid == "ollama":
                return True
            if pid and key:
                return True

        # Legacy format
        return bool(data.get("provider")) and bool(data.get("api_key"))
