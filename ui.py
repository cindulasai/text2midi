# -*- coding: utf-8 -*-
"""
MidiGen Web UI Entry Point
Launch the Gradio-based web interface.
"""

from src.app import MidiGenApp
from src.config import LLMConfig


def main():
    """Launch the web UI."""
    print("=" * 70)
    print("[MUSIC] MidiGen v2.0 - AI Music Generator (Web UI)")
    print("=" * 70)
    
    # Initialize LLM configuration
    LLMConfig.initialize()
    print(f"\n📡 Available LLM Providers: {LLMConfig.AVAILABLE_PROVIDERS}")
    print(f"📡 Current LLM Provider: {LLMConfig.get_provider()}")
    print("\n[INFO] To switch LLM providers: LLMConfig.set_provider('groq')")
    print("[INFO] Launching web interface...\n")
    
    app = MidiGenApp()
    interface = app.create_ui()
    
    interface.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True,
    )


if __name__ == "__main__":
    main()
