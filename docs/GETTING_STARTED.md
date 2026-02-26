# Getting Started with text2midi

Welcome to **text2midi** - Your AI Music Composer! Generate professional MIDI compositions with a simple text description.

## What is text2midi?

text2midi is an AI-powered music composition engine that:
- Generates full musical arrangements from text descriptions
- Creates 1-8 multi-instrument tracks automatically
- Supports 10+ music genres (pop, rock, classical, electronic, lo-fi, jazz, etc.)
- Outputs standard MIDI files compatible with any DAW
- Evolves compositions through multi-turn conversations

## 🚀 Quick Start (5 minutes)

### Step 1: Installation

```bash
# Clone or navigate to the project
cd text2midi

# Install dependencies with Poetry
poetry install

# Or with pip
pip install -r requirements.txt
```

### Step 2: Set Up Your API Key

text2midi uses **MiniMax M2.5** as its default AI model. Copy `.env.example` to `.env` and add your key:

```bash
cp .env.example .env
```

Then open `.env` and fill in at least one key:

```
MINIMAX_API_KEY=your-key-here    # ⭐ Default (recommended) — platform.minimaxi.com
GROQ_API_KEY=your-key-here       # Fallback — console.groq.com (free tier available)
GEMINI_API_KEY=your-key-here     # Fallback — aistudio.google.com (free tier available)
```

> **Provider priority:** MiniMax M2.5 → Groq → Gemini. text2midi auto-selects the first key you provide.

### Step 3: Run text2midi

```bash
python main.py
```

You'll see the active model displayed at startup:
```
[INIT] Active LLM: MINIMAX
[INIT] Model: MiniMax-M2.5 (default)
```

### Step 3: Create Your First Composition

1. **Enter a music description** when prompted:
   ```
   Upbeat pop song with drums, bass, and bright piano
   ```

2. **Wait 10-30 seconds** for generation

3. **Find your MIDI file** in the `outputs/` folder and import into your DAW

That's it! You've created your first AI composition.

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
