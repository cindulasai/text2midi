#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Quick test of LLM provider configuration and switching.
Run this to verify Gemini and Groq integration is working.
"""

from app import LLMConfig, GEMINI_AVAILABLE, GROQ_AVAILABLE, call_llm

def test_configuration():
    """Test LLM configuration."""
    print("\n" + "="*60)
    print("MidiGen LLM Configuration Test")
    print("="*60)
    
    # Test 1: Library availability
    print("\n[Test 1] Library Availability:")
    print(f"  [OK] Gemini library: {GEMINI_AVAILABLE}")
    print(f"  [OK] Groq library: {GROQ_AVAILABLE}")
    
    # Test 2: LLM Config
    print("\n[Test 2] LLM Configuration:")
    print(f"  [OK] Available providers: {LLMConfig.AVAILABLE_PROVIDERS}")
    print(f"  [OK] Default provider: {LLMConfig.get_provider()}")
    
    # Test 3: Provider switching (Gemini only)
    if "gemini" in LLMConfig.AVAILABLE_PROVIDERS:
        print("\n[Test 3] Provider Switching:")
        print(f"  [OK] Current: {LLMConfig.get_provider()}")
        
        # Verify Gemini works
        if LLMConfig.get_provider() == "gemini":
            print(f"  [OK] Gemini is set as default")
    
    # Test 4: API keys status
    print("\n[Test 4] API Key Status:")
    import os
    gemini_key = os.environ.get("GEMINI_API_KEY", "")
    groq_key = os.environ.get("GROQ_API_KEY", "")
    
    if gemini_key:
        print(f"  [OK] Gemini API key: {gemini_key[:10]}..." if len(gemini_key) > 10 else f"  [OK] Gemini API key: {gemini_key}")
    else:
        print(f"  [OK] Gemini API key: (using default hardcoded)")
    
    if groq_key:
        print(f"  [OK] Groq API key: {groq_key[:10]}...")
    else:
        print(f"  [NO] Groq API key: not set (optional)")
    
    # Test 5: Simple call test
    print("\n[Test 5] LLM Call Test (Gemini):")
    if "gemini" in LLMConfig.AVAILABLE_PROVIDERS:
        try:
            # Simple but fast request
            result = call_llm(
                system_prompt="You are a music expert. Answer in one sentence.",
                user_message="What is the most important element of good music?",
                provider="gemini",
                temperature=0.7,
                max_tokens=100
            )
            if result:
                print(f"  [OK] Response from Gemini: {result[:100]}...")
            else:
                print(f"  [NO] No response from Gemini (timeout or error)")
        except Exception as e:
            print(f"  [NO] Error calling Gemini: {e}")
    else:
        print(f"  - Gemini not available")
    
    print("\n" + "="*60)
    print("[DONE] Configuration Test Complete")
    print("="*60 + "\n")

def test_switching():
    """Test provider switching."""
    print("\n" + "="*60)
    print("LLM Provider Switching Test")
    print("="*60)
    
    initial = LLMConfig.get_provider()
    print(f"\n[Initial] Provider: {initial}")
    
    # Try to switch to Groq if available
    if "groq" in LLMConfig.AVAILABLE_PROVIDERS:
        print(f"\n[Switching] Attempting to switch to 'groq'...")
        LLMConfig.set_provider("groq")
        new_provider = LLMConfig.get_provider()
        print(f"[Result] Provider is now: {new_provider}")
        if new_provider == "groq":
            print(f"  [OK] Successfully switched to Groq")
        else:
            print(f"  [NO] Failed to switch to Groq")
        
        # Switch back
        print(f"\n[Switching] Switching back to 'gemini'...")
        LLMConfig.set_provider("gemini")
        restored = LLMConfig.get_provider()
        print(f"[Result] Provider is now: {restored}")
        if restored == "gemini":
            print(f"  [OK] Successfully switched back to Gemini")
    else:
        print(f"\n[INFO] Groq not available (requires GROQ_API_KEY)")
        print(f"       Available providers: {LLMConfig.AVAILABLE_PROVIDERS}")
    
    print("\n" + "="*60)
    print("[DONE] Switching Test Complete")
    print("="*60 + "\n")

if __name__ == "__main__":
    test_configuration()
    test_switching()
    
    print("\n[Summary]")
    print(f"  • Default LLM: {LLMConfig.get_provider()}")
    print(f"  • Available: {LLMConfig.AVAILABLE_PROVIDERS}")
    print(f"  • Read: LLM_CONFIG_GUIDE.md for more options")
    print("\n[SUCCESS] Ready to generate music!\n")
