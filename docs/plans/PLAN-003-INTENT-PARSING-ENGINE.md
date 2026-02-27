# PLAN-003: High-Accuracy LLM Intent Parsing Engine

**Spec:** SPEC-003-INTENT-PARSING  
**Estimated Effort:** 4–5 days  
**Prerequisites:** Python 3.11+, Pydantic v2, existing LLM providers configured  
**Target Accuracy:** 99–100% on structured musical intent extraction  
**Status:** DRAFT  

---

## Problem Statement

The current intent parsing system has three separate, disconnected parsers with critical weaknesses:

| Parser | Location | Method | Fatal Flaw |
|--------|----------|--------|------------|
| `AdvancedIntentParser` | `src/midigent/advanced_intent_parser.py` | Pure regex/keyword (519 lines, **zero LLM**) | Cannot handle compound phrases, references, implicit genre, production vocabulary, or structural requests |
| `IntentParser._parse_with_ai` | `src/app/intent_parser.py` | Weak 15-line LLM prompt, 8-field JSON | No chain-of-thought, no few-shot examples, no disambiguation, no confidence scoring, no validation loop |
| `_parse_intent_basic` | `src/agents/intent_parser_node.py` | 10-genre keyword scan | Last-resort fallback; false positives on "bass"→funk, "power"→rock, "chill"→lofi |

**Result:** Complex, vague, or reference-based prompts fail 50–70% of the time. There is no output validation — musically incoherent combinations (e.g., `genre: "ambient"` + `tempo: 180`) pass through unchecked.

---

## Research Foundation

This plan is grounded in peer-reviewed research and official prompt engineering guidance from major LLM providers:

### Academic References
1. **Chain-of-Thought Prompting** (Wei et al., 2022, arXiv:2201.11903) — Demonstrates that providing intermediate reasoning steps as exemplars dramatically improves accuracy on complex reasoning tasks. Applied here: force the LLM to reason step-by-step about genre, mood, instruments, tempo, structure BEFORE emitting JSON.
2. **Prompt Pattern Catalog** (White et al., 2023, arXiv:2302.11382) — Catalogs reusable prompt patterns: Persona, Template, Few-Shot, Output Automater, Fact Check List, Cognitive Verifier. Applied here: system prompt combines Persona + Template + Few-Shot + Cognitive Verifier patterns.

### Industry Guidance Applied
3. **OpenAI Structured Outputs** (developers.openai.com) — Use Pydantic models to enforce JSON schema adherence. All fields required, `additionalProperties: false`, use `anyOf` with null for optional fields. Chain-of-thought works inside structured output schemas (steps → final_answer pattern).
4. **Anthropic Prompt Engineering Best Practices** (platform.claude.com) — Give Claude a role; use XML tags `<instructions>`, `<examples>`, `<context>`; include 3–5 diverse examples covering edge cases; be explicit about output format and constraints; leverage chain-of-thought with `<thinking>` tags in few-shot examples.
5. **Microsoft Prompt Engineering** (microsoft.github.io/prompt-engineering) — Tell It (high-level task description) + Show It (few-shot examples) + Describe It (API/context description) + Remind It (conversation history). Applied here: system prompt follows this exact 4-layer structure.

### Key Design Principles Derived from Research
- **LLM-first, regex-fallback**: The LLM handles ALL interpretation; regex only runs when no LLM provider is available.
- **Chain-of-thought before output**: The LLM must reason in a `reasoning` field before committing to parameter values. This is proven to increase accuracy by 15–30% on complex tasks (Wei et al.).
- **Few-shot with diverse edge cases**: 8–10 examples covering simple, complex, vague, reference-based, conflicting, and modification prompts. Per Anthropic's guidance, examples should be "relevant, diverse, and structured."
- **Structured output with Pydantic validation**: Guarantees type safety and musical coherence post-extraction. Per OpenAI's guidance, all fields must be required (use null union for optional).
- **Confidence scoring per field**: Each extracted parameter carries a 0.0–1.0 confidence score so downstream nodes can decide whether to trust or override.
- **Self-correction loop**: If the LLM output fails validation, re-query once with the specific error. Per Anthropic's guidance, the "generate → review → refine" chaining pattern is the most common and effective.

---

## Architecture

```
User Prompt (raw text)
    │
    ▼
┌─────────────────────────────────────┐
│  STAGE 1: PRE-PROCESSOR             │  Deterministic text normalization
│  src/intent/preprocessor.py         │  + hard-number extraction (tempo,
│                                     │    duration, bars) via regex
│  Output: PreprocessedInput          │  + abbreviation expansion
└───────────────┬─────────────────────┘
                │
                ▼
┌─────────────────────────────────────┐
│  STAGE 2: LLM INTENT ENGINE        │  Chain-of-thought system prompt
│  src/intent/engine.py               │  + 10 few-shot examples
│                                     │  + structured JSON schema
│  Calls: call_llm() from            │  Temperature: 0.1 (near-deterministic)
│  src/config/llm.py                  │  Max tokens: 1500
│                                     │
│  Output: raw JSON string            │
└───────────────┬─────────────────────┘
                │
                ▼
┌─────────────────────────────────────┐
│  STAGE 3: SCHEMA VALIDATION         │  Pydantic v2 model validates:
│  src/intent/schema.py               │  - Type correctness
│                                     │  - Enum membership
│                                     │  - Range constraints
│                                     │  - Musical coherence rules
│  Output: validated ParsedIntent     │
│          or ValidationError         │
└───────────────┬─────────────────────┘
                │
           ┌────┴────┐
           │ Valid?   │
           └────┬────┘
          yes   │   no
           │    │    │
           │    ▼    ▼
           │  ┌───────────────────────┐
           │  │ STAGE 4: CORRECTION   │  Auto-fix clampable errors OR
           │  │ src/intent/engine.py  │  re-query LLM with error context
           │  │ _retry_with_feedback  │  (max 1 retry)
           │  └──────┬────────────────┘
           │         │
           ▼         ▼
┌─────────────────────────────────────┐
│  STAGE 5: INTENT ENRICHMENT         │  Fill defaults for low-confidence
│  src/intent/engine.py               │  fields using genre config.
│  _enrich_intent()                   │  Map to EnhancedMusicIntent for
│                                     │  downstream compatibility.
│  Output: EnhancedMusicIntent        │
└─────────────────────────────────────┘
                │
                ▼
        [Consumed by track_planner_node,
         theory_validator_node, etc.]
```

---

## Phase 1: Pydantic Schema & Data Models (Day 1 — Morning)

### Step 1: Create `src/intent/__init__.py`
Empty init file for the new package.

### Step 2: Create `src/intent/schema.py` — Pydantic Validation Models

Define the complete output schema as Pydantic v2 `BaseModel` classes. This is the single source of truth for what the LLM must produce.

**Musical coherence validators** (as Pydantic `@model_validator` methods):

1. `validate_tempo_genre_coherence`: If genre is "ambient" and tempo > 100, flag warning; if genre is "electronic" and tempo < 80, flag warning. Use `GENRE_CONFIG` tempo ranges from `src/app/constants.py`.
2. `validate_key_scale_coherence`: Ensure scale value exists in `SCALES` dict.
3. `validate_duration_seconds_match`: Verify `duration.seconds` approximately matches `(duration.bars * 4 / tempo.bpm) * 60`.
4. `validate_instrument_role_uniqueness`: No two instruments should share the same role unless role is "harmony" or "pad".
5. `validate_energy_dynamics_alignment`: If energy is "very_low"/"low", dynamics intensity should not be "powerful" (warn, don't fail).

---

## Phase 2: System Prompt & Few-Shot Examples (Day 1 — Afternoon)

### Step 3: Create `src/intent/prompt_templates.py`

This is the **highest-impact file** in the entire plan. The system prompt follows proven patterns from research:

**Structure (following Microsoft's Tell It + Show It + Describe It + Remind It):**
- Role establishment (Grammy-winning producer persona)
- Task description (extract every musical parameter)
- Context (supported genres, scales, instruments, time signatures)
- Disambiguation rules (10 explicit rules for conflict resolution)
- Output schema (full JSON template with descriptions)
- 8 diverse few-shot examples covering: simple genre, complex multi-parameter, vague contextual, reference-based, conflicting parameters, modification request, instrument-heavy, structural request
- Final instructions (reasoning first, confidence scoring rules, no markdown)

### Step 4: Design the LLM call parameters

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| `temperature` | 0.1 | Near-deterministic for classification accuracy |
| `max_tokens` | 1500 | Schema with reasoning needs ~800-1200 tokens |

---

## Phase 3: Pre-Processor (Day 2 — Morning)

### Step 5: Create `src/intent/preprocessor.py`

Deterministic text normalization layer:
1. `normalize_text()` — Strip whitespace, collapse spaces, normalize unicode
2. `expand_abbreviations()` — bpm→beats per minute, lofi→lo-fi, etc.
3. `extract_hard_numbers()` — Regex for tempo, duration, bars, track count
4. `build_enriched_prompt()` — Combine original text + extracted numbers as context

---

## Phase 4: Core Engine (Day 2 — Afternoon)

### Step 6: Create `src/intent/engine.py` — The Unified Intent Engine

Single entry point replacing all three current parsers.

**Methods:**
1. `parse()` — Main entry. Orchestrates all stages.
2. `_preprocess()` — Stage 1
3. `_build_system_prompt()` — Stage 2
4. `_call_llm_for_intent()` — LLM call with temp=0.1
5. `_parse_and_validate()` — JSON parse + Pydantic validation
6. `_retry_with_feedback()` — Correction loop (max 1 retry)
7. `_enrich_intent()` — Convert to EnhancedMusicIntent
8. `_fallback_keyword_parse()` — Enhanced keyword fallback (no LLM)

---

## Phase 5: Enhanced Keyword Fallback (Day 3 — Morning)

### Step 7: Create `src/intent/fallback_parser.py`

Consolidate best parts of all three existing parsers. Used ONLY when no LLM provider is configured.

---

## Phase 6: Integration (Day 3 — Afternoon)

### Step 8: Modify `src/agents/intent_parser_node.py`
Replace multi-fallback logic with single `LLMIntentEngine.parse()` call.

### Step 9: Modify `src/app/intent_parser.py`
Replace old AI parsing with `LLMIntentEngine.parse()`.

### Step 10: Modify `src/agents/track_planner_node.py`
Pass richer intent data; only override instruments when confidence < 0.5.

---

## Phase 7: Test Suite (Day 4)

### Step 11-13: Create comprehensive test files
- `tests/test_intent_engine.py` — 50+ test cases across 9 categories
- `tests/test_intent_schema.py` — Pydantic validator tests
- `tests/test_preprocessor.py` — Normalization tests

---

## Phase 8: Documentation & Cleanup (Day 5)

### Step 14-16: Update architecture docs, deprecate old parsers, update roadmap

---

## File Summary

| File | Action | Lines (est.) | Priority |
|------|--------|-------------|----------|
| `src/intent/__init__.py` | CREATE | 5 | P0 |
| `src/intent/schema.py` | CREATE | ~250 | P0 |
| `src/intent/prompt_templates.py` | CREATE | ~350 | P0 |
| `src/intent/preprocessor.py` | CREATE | ~120 | P1 |
| `src/intent/engine.py` | CREATE | ~300 | P0 |
| `src/intent/fallback_parser.py` | CREATE | ~200 | P1 |
| `src/agents/intent_parser_node.py` | MODIFY | ~-80 / +30 | P0 |
| `src/app/intent_parser.py` | MODIFY | ~-60 / +20 | P1 |
| `src/agents/track_planner_node.py` | MODIFY | ~+15 | P2 |
| `tests/test_intent_engine.py` | CREATE | ~400 | P0 |
| `tests/test_intent_schema.py` | CREATE | ~150 | P1 |
| `tests/test_preprocessor.py` | CREATE | ~80 | P2 |

---

## Decisions Log

| Decision | Choice | Rationale |
|----------|--------|-----------|
| LLM temperature | 0.1 | Near-deterministic for structured extraction |
| Few-shot count | 8 examples | Covers the full edge-case taxonomy |
| Retry count | 1 max | Balance between accuracy and latency |
| Confidence threshold | 0.4 | Below this, genre defaults replace inference |
| Pydantic v2 vs v1 | v2 | Better performance, native JSON schema export |
| Single engine vs separate | Single `LLMIntentEngine` | Eliminates duplication |
| Structured Output API vs JSON mode | JSON mode + Pydantic | Provider-agnostic |
| Keep old parsers | Deprecate, don't delete | Backward compatibility |

---

## Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| LLM returns malformed JSON | Parse with `json.loads`, catch exception, retry once |
| LLM hallucinates unsupported genre | Pydantic `Literal` enum rejects; correction loop re-queries |
| Provider outage | Enhanced keyword fallback produces reasonable defaults |
| System prompt too large | Total ~4K tokens; within all provider limits |
| Latency increase from CoT | +200-400ms; acceptable for non-realtime MIDI generation |
| Few-shot examples bias | Diverse examples across all genres; tested for patterns |
