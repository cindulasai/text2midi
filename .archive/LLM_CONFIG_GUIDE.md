# LLM Configuration - Quick Guide

## What's New

✅ **Groq is now the default provider**  
✅ **llama-4-maverick is the default model** (most intelligent)  
✅ **Fallback to llama-3.3-70b-versatile** if maverick unavailable  

---

## Usage Examples

### Python Code

```python
from src.config.llm import LLMConfig

# Initialize (sets Groq as default)
LLMConfig.initialize()
# Prints: "Default provider: groq"
# Prints: "Current model: llama-4-maverick"

# Switch to llama-3.3-70b-versatile
LLMConfig.set_groq_model("llama-3.3-70b-versatile")

# Switch back to llama-4-maverick
LLMConfig.set_groq_model("llama-4-maverick")

# View available models
print(LLMConfig.GROQ_MODELS)
# Output: ["llama-4-maverick", "llama-3.3-70b-versatile"]

# View current model
print(LLMConfig.CURRENT_GROQ_MODEL)
# Output: "llama-4-maverick"
```

### In UI/CLI

The system will automatically use **Groq** with **llama-4-maverick** - no changes needed!

---

## Configuration Details

### Default Settings

```python
DEFAULT_PROVIDER = "groq"           # ✓ Set automatically if available
CURRENT_GROQ_MODEL = "llama-4-maverick"  # ✓ Most intelligent
GROQ_MODELS = [
    "llama-4-maverick",
    "llama-3.3-70b-versatile"
]
```

### How It Works

1. **Initialize**: Sets Groq as default if GROQ_API_KEY is available
2. **Primary Model**: Tries llama-4-maverick first
3. **Fallback**: Falls back to llama-3.3-70b-versatile if maverick fails
4. **Toggleable**: Call `LLMConfig.set_groq_model()` to switch anytime

---

## To Test

### Option 1: Run main.py
```bash
poetry run python main.py
# Will use Groq + llama-4-maverick automatically
```

### Option 2: Run UI
```bash
poetry run python ui.py
# Will use Groq + llama-4-maverick automatically
```

### Option 3: Quick Test Script
```python
from src.config.llm import LLMConfig
from src.config.llm import call_llm

LLMConfig.initialize()

# Use default (llama-4-maverick)
response = call_llm(
    "You are a helpful assistant",
    "What are the benefits of music?",
    temperature=0.7
)
print(response)

# Switch to other model and try again
LLMConfig.set_groq_model("llama-3.3-70b-versatile")
response = call_llm(
    "You are a helpful assistant",
    "What are the benefits of music?",
    temperature=0.7
)
print(response)

# Switch back
LLMConfig.set_groq_model("llama-4-maverick")
```

---

## Files Modified

✅ `src/config/llm.py`
- Added `GROQ_MODELS` list
- Added `CURRENT_GROQ_MODEL` variable (default: llama-4-maverick)
- Added `set_groq_model()` method
- Updated `initialize()` to set Groq as default
- Updated `_call_groq()` to use configurable model

---

## Key Methods

### `LLMConfig.initialize()`
Sets up providers and models. Call once at startup.

### `LLMConfig.set_groq_model(model: str)`
Switch between available Groq models.
- `"llama-4-maverick"` - Most intelligent
- `"llama-3.3-70b-versatile"` - Fallback

### `LLMConfig.set_provider(provider: str)`
Switch between providers.
- `"groq"` - Default
- `"gemini"` - If available

### `call_llm(...)`
Makes LLM calls using current configuration.

---

## Summary

- ✅ Groq is default provider
- ✅ llama-4-maverick is default model  
- ✅ Simple toggle method: `LLMConfig.set_groq_model()`
- ✅ Automatic fallback on errors
- ✅ No existing code changes needed
- ✅ Ready to test!
