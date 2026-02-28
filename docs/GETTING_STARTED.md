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
- Stores API keys securely in OS Keyring (never plain text)

## 🚀 Quick Start: Two Installation Options

### Option 1: One-Touch Installer (Easiest - Recommended! ⭐)

If you're new to coding, use the installer:

**Windows:**
```bash
installer/install.bat
```

**macOS/Linux:**
```bash
bash installer/install.sh
```

The installer will:
- ✅ Detect/install Python 3.11+ automatically
- ✅ Install uv and all dependencies
- ✅ Help you get a **free API key** (Groq, Gemini, or OpenRouter)
- ✅ Create a desktop launcher and shortcuts
- ✅ Secure your API key in OS Keyring

[📖 Full Installer Details](../installer/README.md)

### Option 2: Manual Setup (For Developers)

If you know Python/terminal:

```bash
# Step 1: Clone and enter directory
cd text2midi

# Step 2: Install dependencies with uv
uv sync          # or: pip install -r requirements.txt

# Step 3: Run and setup
python main_tui.py     # Terminal UI (recommended)
# or
python main.py         # CLI
```

On first run, the app auto-launches an interactive setup wizard that:
1. Shows you the available AI providers (free and paid)
2. Gives you direct URLs to get free API keys
3. Lets you paste your key
4. Tests the connection instantly
5. **Securely stores your key in OS Keyring** — you never edit `.env` files!

> **Security**: Your API keys are stored securely in your OS's credential manager (Windows Credential Manager, macOS Keychain, Linux Secret Service) — never as plain text in files.

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
# Run the Terminal UI and press Ctrl+S
python main_tui.py

# Or re-run setup wizard from CLI
python main.py --setup
```

Your keys are stored securely in OS Keyring, not in files.

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
python main_tui.py
```

The setup wizard will detect Ollama automatically and offer it as an option. No API key needed!

---

## (Optional) Manual `.env` Configuration

The setup wizard is the easiest way to configure providers. However, if you prefer to use a `.env` file for development or scripting:

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

> **Security Note**: On first run, text2midi automatically moves your keys from `.env` to secure OS Keyring storage. The `.env` file is only read if keyring is unavailable as a fallback.
>
> **Provider priority:** text2midi tries each configured provider until one works. We recommend Groq as the default.


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
