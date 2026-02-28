# Plan-TUI: Fault Tolerance & Robustness for TUI Sidebar

**Status:** APPROVED  
**Date:** 2026-02-27  
**Scope:** Sidebar tree LLM interactions, error handling, retry logic, status display  

---

## Problem Statement

The TUI sidebar throws ugly errors whenever a user clicks on a child node expansion
or "More ideas" leaf. Exceptions from LLM provider calls propagate up as unhandled
errors, crashing the Textual event loop or rendering stack traces on screen. There is
no inline status indicator for LLM operations, no retry-with-cooldown logic, no
sidebar-level duplicate detection, and no concurrency guard against rapid repeated
clicks.

## Goals

1. **Zero visible errors** — the TUI must never display raw tracebacks or crash.
2. **Inline status feedback** — a small status label inside the sidebar shows
   progress ("Generating…") and errors (red text, auto-clears after 5 s).
3. **Retry with cooldown** — up to 2 retries (3 total attempts) with ≥ 2 s gaps
   when LLM calls fail; falls back gracefully to seed presets or empty state.
4. **Duplicate detection** — if the LLM returns a prompt already visible under
   that node, retry automatically (within the retry budget) instead of showing it.
5. **Concurrency guard** — prevent duplicate concurrent loads for the same genre
   (rapid clicks ignored while a load is in-flight).
6. **Rate limiting** — enforce a minimum 2 s gap between any two sidebar LLM calls
   to avoid hammering the API.
7. **Global safety net** — override `on_exception()` in the App so any stray
   unhandled exception produces a brief toast instead of a crash.
8. **Custom exceptions** — activate the existing `LLMProviderError` hierarchy in
   the preset service for better caller differentiation.

---

## Implementation Steps

### 1. Sidebar Status Label

**File:** `src/tui/widgets/sidebar.py`

- Add a `Label(id="sidebar-status")` above the `Tree` in `compose()`.
- Helper `_set_status(text, error=False)` — shows/hides label, toggles red class.
- Helper `_clear_status()` — clears text, hides label.
- Error auto-dismiss via `self.set_timer(5.0, self._clear_status)`.

### 2. CSS for Status Label

**File:** `src/tui/styles.tcss`

```css
#sidebar-status {
    height: auto;
    padding: 0 1;
    color: #6c7086;
    background: #181825;
    margin-bottom: 0;
    display: none;
}
#sidebar-status.visible { display: block; }
#sidebar-status.sidebar-error { color: #f38ba8; text-style: bold; }
```

### 3. Retry Logic with Cooldown

**File:** `src/tui/widgets/sidebar.py`

New method `_generate_with_retries(genre_id, bypass_cache=False) -> list[str]`:

- 1 initial attempt + 2 retries = 3 total.
- 2 s `time.sleep()` between attempts.
- Filters results against `self._generated_prompts[genre_id]` (sidebar-level dedup).
- If all retries produce duplicates or fail, falls back to seed presets (also deduped).
- Returns `[]` if absolutely nothing works.

### 4. Sidebar-Level Duplicate Detection

**File:** `src/tui/widgets/sidebar.py`

New instance var `_generated_prompts: dict[str, set[str]]` — maps genre_id → set of
normalized prompt strings already displayed as tree leaves.

- `_on_presets_loaded()` and `_on_more_loaded()` register new prompts.
- `_generate_with_retries()` filters against this set and retries on duplicates.

### 5. Concurrency Guard

**File:** `src/tui/widgets/sidebar.py`

New instance var `_loading_genres: set[str]`.

- Check before spawning a thread; silently return if already in-flight.
- Release in both success and failure `call_from_thread` callbacks.

### 6. Rate Limiting

**File:** `src/tui/widgets/sidebar.py`

New instance var `_last_llm_call: float = 0.0`.

- In `_generate_with_retries()`, enforce ≥ 2 s since last call via `time.sleep()`.
- Update timestamp after each call.

### 7. Harden Event Handlers

**File:** `src/tui/widgets/sidebar.py`

Wrap `on_tree_node_expanded()` and `on_tree_node_selected()` bodies in
`try/except Exception` — log + set error status, never propagate.

### 8. Harden `call_from_thread` Callbacks

**File:** `src/tui/widgets/sidebar.py`

Wrap `_on_presets_loaded()`, `_on_more_loaded()`, `_on_load_failed()` in
`try/except Exception` — if the node was removed while the thread ran, log silently.

### 9. Global Exception Handler

**File:** `main_tui.py`

```python
def on_exception(self, error: Exception) -> None:
    logger.exception("Unhandled TUI error: %s", error)
    self.notify(str(error)[:80], severity="error")
```

### 10. Custom Exception in Preset Service

**File:** `src/services/preset_service.py`

Replace bare `except Exception` in `generate_presets()` with raising
`LLMProviderError` from `src/app/errors.py` on LLM hard failures.

---

## Files Modified

| File | Changes |
|------|---------|
| `src/tui/widgets/sidebar.py` | Status label, retry, dedup, concurrency, rate limit, error wrapping |
| `src/tui/styles.tcss` | `#sidebar-status` normal + error styles |
| `main_tui.py` | Global `on_exception()` handler |
| `src/services/preset_service.py` | Use `LLMProviderError` |

## Verification

| Scenario | Expected |
|----------|----------|
| No LLM key configured | Seed presets shown, no crash |
| LLM rate-limited / network error | 3 attempts with 2 s gaps, then "(no ideas available)" + "🔄 Retry" |
| LLM returns duplicate | Auto-retry within budget, then "No new ideas" leaf |
| Rapid "More ideas" clicks | Concurrency guard ignores second click |
| Random unhandled exception | Toast notification, app continues |

## Decisions

- **Status label:** Inside sidebar, above tree
- **Retries:** 2 (3 total attempts, ≤ 6 s max)
- **Cooldown:** 2 s between retries
- **Error auto-dismiss:** 5 s
