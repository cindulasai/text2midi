# text2midi VST3 Plugin

Generate multi-track MIDI compositions using AI — directly inside your DAW.

**Type a text prompt → AI generates music → Drag the MIDI file into your arrangement.**

![Plugin Screenshot](assets/screenshot.png)

---

## Features

- **Text-to-MIDI in your DAW** — Describe the music you want, get a multi-track MIDI file
- **Drag & Drop** — Drag the generated MIDI file from the plugin directly onto your DAW's arrangement view
- **Multi-track** — Type 1 MIDI files auto-create separate tracks per channel in Ableton Live and other DAWs
- **Multiple AI Providers** — MiniMax M2.5, Groq (Llama 4 Maverick), or any OpenAI-compatible endpoint
- **One-time setup** — Enter your API key once, it's saved with your DAW project
- **8-node AI pipeline** — Intent parsing, track planning, theory validation, quality control, and more
- **Dark theme** — Catppuccin Mocha colour scheme that fits right in with modern DAWs

## System Requirements

- **OS:** Windows 10/11 (64-bit)
- **DAW:** Any VST3-compatible host (Ableton Live 10+, FL Studio, Bitwig, Reaper, etc.)
- **Internet:** Required for AI generation (LLM API calls)
- **API Key:** One of: MiniMax, Groq, or any OpenAI-compatible provider

## Installation

### Option A: Installer (Recommended)

1. Download `text2midi_setup.exe` from the releases page
2. Run the installer — it will:
   - Install the VST3 plugin to `C:\Program Files\Common Files\VST3\`
   - Install the backend server to `C:\Program Files\text2midi\`
   - Optionally add the server to Windows startup
3. Rescan plugins in your DAW
4. Add "text2midi" as an instrument on a MIDI track

### Option B: Manual Installation

1. Copy `text2midi.vst3` folder to `C:\Program Files\Common Files\VST3\`
2. Copy `text2midi-backend\` folder somewhere accessible
3. Rescan plugins in your DAW

## First-Time Setup

1. Load the text2midi plugin on an instrument track in your DAW
2. The backend server will auto-launch (or start it manually)
3. Select your AI provider and enter your API key
4. Click "Save & Connect"
5. The green indicator shows when backed is connected

## Usage

1. **Type a prompt** — e.g., "dreamy jazz with piano and soft drums"
2. **Click Generate** — Watch the 8-step AI pipeline progress
3. **Drag the MIDI file** — Grab the generated MIDI clip and drop it on your DAW arrangement
4. **Multi-track creation** — Ableton Live automatically creates separate tracks per MIDI channel

## Supported DAWs

| DAW | Status | Multi-track on Drop |
|-----|--------|-------------------|
| Ableton Live 10+ | ✅ Tested | ✅ Auto-creates tracks |
| FL Studio 20+ | ✅ Expected | ⚠️ Manual channel routing |
| Bitwig Studio | ✅ Expected | ✅ Auto-creates tracks |
| Reaper | ✅ Expected | ✅ Auto-creates tracks |
| Logic Pro | ❌ macOS only (v2) | N/A |

## Troubleshooting

### "Server offline" indicator

The plugin couldn't connect to the backend server.

1. Check if `text2midi-backend.exe` is running (Task Manager → Details)
2. Try starting it manually from `C:\Program Files\text2midi\text2midi-backend.exe`
3. Check if port 18323 is available: `netstat -an | findstr 18323`
4. Firewall: Allow `text2midi-backend.exe` through Windows Firewall

### Windows SmartScreen Warning

If Windows SmartScreen blocks the server executable:

1. Click "More info"
2. Click "Run anyway"
3. This only happens once — the .exe is safe but unsigned (code signing planned for v1.0)

### Generation takes too long

- Generation typically takes 5-30 seconds depending on the AI provider
- The progress panel shows which step is currently running
- If stuck, check your internet connection and API key validity

### No tracks created when dropping MIDI

- Make sure you're dropping onto the arrangement view (not the session view in Ableton)
- The MIDI file uses Type 1 format — each channel becomes a separate track
- In FL Studio, you may need to manually assign channels after import

## Known Limitations

- Windows only (macOS planned for v2)
- Requires internet connection for generation
- Maximum 8 MIDI tracks per generation (Ableton Live Lite limit)
- Backend server must be running during generation
- No real-time audio output (silence pass-through — this is a MIDI generation tool)

## License

MIT — See [LICENSE](../LICENSE) for details.
