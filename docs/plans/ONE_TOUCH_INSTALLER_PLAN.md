# One-Touch Installer — Implementation Plan

> Saved reference plan for the text2midi one-touch installer system.

---

## Architecture

**Two-stage bootstrap** — a platform-native script (.bat / .sh) handles
environment setup, then optionally builds a tiny native launcher via PyInstaller.

The launcher exe is **not** a monolithic bundle. It is a ~5 MB wrapper that
runs `uv run python main_tui.py`. The app already needs internet for LLM
calls, so bundling 150 MB of langchain/litellm has zero benefit and makes
packaging fragile.

## Files Created

| File | Purpose |
|------|---------|
| `installer/install.bat` | Windows one-touch bootstrap (5-step) |
| `installer/install.sh` | macOS / Linux one-touch bootstrap (5-step) |
| `installer/build_launcher.py` | PyInstaller exe wrapper builder with fallback |
| `installer/checksums.json` | SHA-256 hashes for download verification |
| `installer/README.md` | Plain-English user installation guide |
| `src/config/keyring_store.py` | OS Keyring integration for API key storage |

## Files Modified

| File | Change |
|------|--------|
| `src/config/settings.py` | Keyring sentinel in save(), restore in load() |
| `src/config/log.py` | ApiKeyRedactionFilter on all log handlers |
| `pyproject.toml` | Added `keyring>=25.0.0` dependency |
| `.gitignore` | Added installer build artifacts |

## Installation Flow (5 Steps)

1. **Python Runtime** — Detect existing Python 3.11+; if missing, install via
   winget / Homebrew / apt / dnf / pacman / zypper / apk with 3-tier fallback.

2. **uv Package Manager** — Detect existing uv; if missing, install via
   official installer (download-then-verify, NOT pipe-to-exec) → pip fallback.

3. **Dependencies** — `uv sync` with 3× retry and 5-second backoff.

4. **AI Provider Setup** (optional, skippable) — Launches existing
   `setup_wizard.py`. Shows free-tier guidance (Groq, Gemini, OpenRouter,
   Ollama). User can press S to skip; can configure later via `--setup` or
   Ctrl+S in the app.

5. **Launcher Creation** — Attempts PyInstaller exe build with 3× retry.
   Falls back to `.bat` (Windows) or shell script + `.command` / `.desktop`
   (macOS / Linux) if PyInstaller unavailable.

## Security Model

- **API Key Storage**: OS Keyring (Windows Credential Manager / macOS Keychain /
  Linux Secret Service) via `keyring>=25.0.0`. JSON file stores `__KEYRING__`
  sentinel instead of real secret. Fallback: plaintext with restricted file
  permissions (icacls / chmod 600).

- **Log Redaction**: Regex filter catches `gsk_`, `sk-ant-`, `sk-`, `key-`,
  `AIza`, `xai-` prefixed strings and replaces with `***REDACTED***`.

- **Download Security**: All downloads go to temp file first, content verified,
  then executed. No pipe-to-exec patterns.

- **User Consent**: Explicit Y/n prompt before any system modifications.

## Reliability Design

- Every step has retry logic (typically 3 attempts with backoff)
- Every step has a fallback if the primary method fails
- Network check at startup with graceful continue-anyway option
- API key setup is fully skippable — never blocks installation
- If PyInstaller fails, a script launcher is always created
- Clear, jargon-free error messages at every failure point
- Temp files cleaned up regardless of success or failure
