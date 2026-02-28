# text2midi — One-Touch Installer Guide

Welcome! This guide will help you install **text2midi**, the AI-powered MIDI composer that turns your words into music.

**No programming knowledge required.** The installer does everything for you.

---

## Quick Start

### Windows

1. Download or clone this project.
2. Open the `installer` folder.
3. **Double-click `install.bat`**.
4. Follow the on-screen prompts.
5. When done, double-click **text2midi.exe** (or **text2midi.bat**) in the project folder.

### macOS

1. Download or clone this project.
2. Open **Terminal** (search for it in Spotlight).
3. Run:
   ```
   cd /path/to/text2midi
   bash installer/install.sh
   ```
4. When done, double-click **text2midi.command** in Finder, or run `./text2midi` from Terminal.

### Linux

1. Download or clone this project.
2. Open a terminal.
3. Run:
   ```
   cd /path/to/text2midi
   bash installer/install.sh
   ```
4. When done, run `./text2midi` from the project folder, or find **text2midi** in your application menu.

---

## Getting a Free AI API Key

text2midi needs an AI provider to turn your text into music. Here are some **completely free** options:

### Groq (Recommended — Fastest)

1. Go to [console.groq.com](https://console.groq.com/keys)
2. Sign up with email or Google/GitHub
3. Click **Create API Key**
4. Copy the key (starts with `gsk_`)

### Google Gemini (Free Tier)

1. Go to [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
2. Sign in with your Google account
3. Click **Create API Key**
4. Copy the key

### OpenRouter (Multiple Models)

1. Go to [openrouter.ai/keys](https://openrouter.ai/keys)
2. Sign up and navigate to API Keys
3. Create a key and copy it

### Ollama (Run AI Locally — No Key Needed)

1. Go to [ollama.com](https://ollama.com) and download
2. Install and run Ollama
3. In your terminal run: `ollama pull llama3.2`
4. Select **Ollama** when setting up text2midi — no API key required!

> **Tip:** You can skip the API key during installation and set it up later by pressing **Ctrl+S** inside the app, or by running `uv run python main.py --setup`.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| **"Python not found"** | Download from [python.org/downloads](https://python.org/downloads) and re-run the installer. |
| **"uv not found"** | Run `pip install uv` then re-run the installer. |
| **Dependencies fail to install** | Check your internet connection and re-run. |
| **API key not working** | Make sure you copied the full key. Run `uv run python main.py --setup` to try again. |
| **Exe not created** | That is fine — use **text2midi.bat** (Windows) or `./text2midi` (macOS/Linux) instead. |
| **"Permission denied" on macOS/Linux** | Run `chmod +x installer/install.sh` then try again. |
| **App launches but shows errors** | Make sure you completed a `uv sync` (the installer does this automatically). |

---

## What Gets Installed

| Component | What It Is | Where |
|-----------|-----------|-------|
| **Python 3.12** | Programming runtime | System-level (only if not already installed) |
| **uv** | Fast package manager | `~/.local/bin/` |
| **App dependencies** | Libraries the app uses | Project `.venv/` folder |
| **Launcher** | The app shortcut | Project root |

> Your personal files are **never** modified. All app data goes into the project folder or standard config directories.

---

## Uninstalling

1. Delete the project folder — that removes the app and all dependencies.
2. (Optional) Uninstall uv: `pip uninstall uv` or delete `~/.local/bin/uv`.
3. (Optional) Uninstall Python if you installed it just for this.

---

## Need Help?

- Open an issue on GitHub
- Check `docs/GETTING_STARTED.md` for detailed usage instructions
- Run `uv run python main.py --help` for command-line options
