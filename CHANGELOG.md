# Changelog

All notable changes to text2midi are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-02-26

### Added

- Initial release of **text2midi** — AI-powered text-to-MIDI music generation
- LangGraph multi-agent architecture with 8 specialized nodes:
  - Intent Parser, Track Planner, Music Theory Validator
  - Track Generator, Quality Control, Refinement
  - MIDI Creator, Session Summary
- Multi-provider LLM support: MiniMax M2.5 (default), Groq llama-4-maverick, Google Gemini 2.0 Flash
- Automatic provider detection via environment variables
- Support for 8 genres: ambient, cinematic, classical, electronic, funk, jazz, lofi, pop
- Up to 8 simultaneous MIDI tracks with instrument assignment
- Standard MIDI Type 0/1 output at 480 PPQ
- Multi-turn conversation for iterative composition refinement
- Comprehensive music theory engine (scales, chord progressions, emotion mapping)
- Creative variation engine to avoid repetition
- Session management for generating multiple pieces
- CLI entry point: `python main.py`

### Technical

- Python 3.11+ with uv package management
- LangGraph agentic state machine
- mido library for MIDI file creation
- Outputs saved to `outputs/` with timestamped filenames
