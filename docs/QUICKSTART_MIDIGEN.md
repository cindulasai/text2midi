# MidiGen v2.0 - Quick Start Guide

Professional AI-powered MIDI music generator. Create complex musical compositions through simple natural language descriptions.

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <repo-url>
cd spec-kit

# Install dependencies with Poetry
poetry install
```

### 2. Run Web UI (Recommended)

```bash
python ui.py
```

Visit `http://localhost:7860` and start creating music!

### 3. Example Prompts

**Simple (1-2 tracks):**
- "Solo piano ballad"
- "Just acoustic guitar"

**Standard (4-5 tracks):**
- "Upbeat pop song"
- "Chill lo-fi beat in D minor"

**Rich/Epic (6-8 tracks):**
- "Epic cinematic orchestra with full arrangement"
- "Complex electronic production with multiple layers"

## 📋 Features

- **Dynamic Track Generation**: 1-8 tracks based on your description
- **Multi-turn Support**: Build on previous compositions
- **AI-Powered**: LLM-based intent understanding
- **Genre Support**: Pop, rock, electronic, lo-fi, jazz, classical, ambient, cinematic, funk, R&B
- **Real-time MIDI**: Download your creations instantly

## 🎛️ Configuration

### LLM Providers

Default: Google Gemini

```python
from src.config import LLMConfig
LLMConfig.set_provider('groq')  # Switch to Groq
```

## 📊 Output Files

Saved to `outputs/` as MIDI files ready for:
- Music Production DAWs
- MIDI synthesizers
- Audio conversion tools

## 📚 Full Documentation

- [Architecture](/docs/ARCHITECTURE.md) - System design
- [Main Docs](/docs/README.md) - Complete reference

---

See Also: [Spec-Kit QuickStart](QUICKSTART.md) for Spec-Driven Development setup.
