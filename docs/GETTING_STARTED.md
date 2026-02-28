# Getting Started with text2midi

Welcome to **text2midi** - Your AI Music Composer! Generate professional MIDI compositions with a simple text description.

## What is text2midi?

text2midi is an AI-powered music composition engine that:
- Generates full musical arrangements from text descriptions
- Creates 1-8 multi-instrument tracks automatically
- Supports 10+ music genres (pop, rock, classical, electronic, lo-fi, jazz, etc.)
- Outputs standard MIDI files compatible with any DAW
- Evolves compositions through multi-turn conversations
- Works with **15+ AI providers** — use whichever you already have

## 🚀 Quick Start (30 seconds)

### Step 1: Install

```bash
cd text2midi
uv sync          # or: pip install -r requirements.txt
```

### Step 2: Run & Setup

```bash
python main.py
```

**That's it!** On first run, the app auto-launches an interactive setup wizard that:
1. Shows you the available AI providers (free and paid)
2. Gives you the direct URL to get an API key
3. Lets you paste your key
4. Tests the connection instantly
5. Saves everything — you never have to do this again

> **No `.env` file editing required.** The wizard handles everything.

### Step 3: Create Music

Enter a description when prompted:
```
Upbeat pop song with drums, bass, and bright piano
```

Wait 10-30 seconds → find your MIDI file in `outputs/` → import into your DAW!

---

## 🔑 Choosing an AI Provider

You only need **ONE** provider. Here's a comparison:

### Free Options (No Credit Card)

| Provider | Speed | Quality | Best For |
|----------|-------|---------|----------|
| **Groq** ⭐ | Ultra-fast | Excellent | Best free option for most users |
| **Ollama** | Depends on PC | Good | Privacy, offline use, no internet |
| **Google Gemini** | Fast | Very Good | If you have a Google account |

### Paid Options

| Provider | Speed | Quality | Best For |
|----------|-------|---------|----------|
| **OpenAI** | Fast | Excellent | GPT-4o, industry leader |
| **Anthropic** | Fast | Excellent | Claude, great reasoning |
| **MiniMax** | Fast | Very Good | Strong structured output |
| **Mistral** | Fast | Very Good | European, multilingual |
| **DeepSeek** | Fast | Very Good | Affordable, coding strength |

### Meta-Providers
| Provider | Description |
|----------|-------------|
| **OpenRouter** | One API key → access 100+ models |

> **Our recommendation:** Start with **Groq** (free, fast, excellent quality).

---

## 🔧 Re-configure Anytime

```bash
# Re-run the setup wizard
python main.py --setup

# Or for the TUI version
python main_tui.py     # Use the Settings panel (Ctrl+S)
```

---

## 🖥️ Using Ollama (Free, Local, Offline)

Run AI models on your own computer — no API key, no internet, no cost:

```bash
# 1. Install Ollama
#    Windows: Download from https://ollama.com
#    Mac/Linux: curl -fsSL https://ollama.com/install.sh | sh

# 2. Download a model
ollama pull llama3.2

# 3. Run text2midi — it auto-detects Ollama!
python main.py
```

The setup wizard will detect Ollama automatically and offer it as an option.

---

## 📋 Alternative: Manual .env Configuration

If you prefer, you can configure providers via a `.env` file instead of the wizard:

```bash
cp .env.example .env
```

Then open `.env` and add your key(s):
```bash
# You only need ONE of these:
GROQ_API_KEY=gsk_your_key_here          # Free — console.groq.com
OPENAI_API_KEY=sk-your_key_here         # Paid — platform.openai.com
ANTHROPIC_API_KEY=sk-ant-your_key_here  # Paid — console.anthropic.com
GEMINI_API_KEY=your_key_here            # Free tier — aistudio.google.com
MINIMAX_API_KEY=your_key_here           # Paid — platform.minimaxi.com
```

> **Provider priority:** text2midi uses the first available key it finds. Configure multiple providers for automatic fallback.


---

## 📝 Example Prompts

### Simple (1-2 Tracks)
- `Solo piano ballad in F minor`
- `Melancholic acoustic guitar`
- `Ambient pad with reverb`

### Medium (3-5 Tracks)
- `Upbeat pop song with drums, bass, and piano`
- `Chill lo-fi beat with vinyl crackle`
- `Indie rock with guitars and drums`

### Complex (6-8 Tracks)
- `Epic cinematic orchestra with strings, brass, and woodwinds`
- `Layered electronic production with synths, bass, and drums`
- `Jazz ensemble with piano, bass, drums, and saxophone`

### Iterative Refinement
After generating a composition, refine it:
- `Make it faster` (increase tempo)
- `Add more strings` (thicken arrangement)
- `Use D major instead` (change key)
- `Make the drums less busy` (reduce density)
- `Add a 4-bar intro with just bass` (restructure)

---

## 🎯 Next Steps

1. **[MIDI Generation Guide](MIDI_GENERATION_GUIDE.md)** - Learn advanced composition techniques
2. **[DAW Integration: Ableton Live](DAW_ABLETON_LIVE.md)** - Import MIDI & add instruments
3. **[DAW Integration: Surge XT](DAW_SURGE_XT.md)** - Advanced synthesis & effects
4. **[Track Types Reference](TRACK_TYPES_REFERENCE.md)** - Understanding each track type
5. **[Troubleshooting](TROUBLESHOOTING.md)** - Common issues & solutions

---

## 💡 Pro Tips

✨ **Be Specific**
- Instead of: "Make a song"
- Try: "Upbeat 120 BPM pop track in G major with energetic drums and funky bass"

🎵 **Describe the Vibe**
- Include emotions: "Happy", "Dark", "Melancholic", "Energetic"
- Use context: "Soundtrack for a car chase" or "Background for studying"

🔄 **Iterate & Evolve**
- First generation is rarely perfect
- Build on previous generations with feedback
- Ask for specific changes in follow-up prompts

⚡ **Use Multiple Turns**
- Generate a basic structure first
- Then ask for layers to be added
- Finally, refine specific instruments

---

## 🆘 Having Trouble?

- **Installation Issues?** → See [Troubleshooting](TROUBLESHOOTING.md)
- **MIDI not importing?** → Check [DAW Integration Guides](DAW_ABLETON_LIVE.md)
- **Generating bad quality music?** → Review [MIDI Generation Guide](MIDI_GENERATION_GUIDE.md)

---

**Happy composing!** 🎶
