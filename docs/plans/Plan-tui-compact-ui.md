# Plan: Compact Right Panel Redesign

**Status:** APPROVED  
**Date:** 2026-02-27  
**Scope:** Right panel (main-content) — output, progress, prompt, styles  

---

## Problem Statement

The right panel is cluttered with redundant information, oversized widgets, and
excessive padding/margins that force too much scrolling. It lacks the sleek,
professional appearance expected of a polished product.

## Goals

1. **Minimal vertical footprint** — every widget earns its space.
2. **No redundancy** — remove duplicate information and buttons available via keybindings.
3. **Compact data** — use terse labels, inline badges, and short separators.
4. **Professional appearance** — tight spacing, consistent rhythm, no visual noise.

---

## Changes

### Output Panel (`src/tui/widgets/output_panel.py`)

| Before | After |
|--------|-------|
| Title "🎶 Generation Results" | Removed — context is obvious |
| Markdown summary block (max 8 lines) | Removed — biggest vertical offender |
| Quality: `0.85/1.0  ■■■■■■■■□□` | `Quality █████████░ 85%` |
| Badge: `💾 2.1 KB  │  🎵 4 tracks  │  🎹 120 notes` | `2.1KB · 4trk · 120n · 45s · ambient` |
| File path: full absolute path | Filename only |
| 5 action buttons (Copy to DAW, Open in App, Open Folder, Copy Path, Change API Key) | 3 buttons (Copy to DAW, Folder, Path) |

Removed buttons rationale:
- "Change API Key" → already Ctrl+S
- "Open in App" → "Open Folder" suffices; double-click in folder is standard

### Progress Panel (`src/tui/widgets/progress_panel.py`)

| Before | After |
|--------|-------|
| Title "⏳ Generating…" / "✅ Generation Complete" | Removed |
| Icons per step (🧠📋🎼…) | Removed |
| Long labels: "Intent Parser", "Track Planner" | Short: "Parse", "Plan", "QC" |
| Status: `🧠 Step 1/8: Intent Parser…` | `1/8 Parse…` |
| Complete: `🎉 Complete — Quality: 0.85/1.0` | `✓ Done · 85%` |
| Step indicators use `short[:3]` | Full short label |

### Prompt Input (`src/tui/widgets/prompt_input.py`)

| Before | After |
|--------|-------|
| TextArea height: 4 | Height: 3 |
| "🎵 Generate" button | "Generate" |
| "🎲 Surprise Me" button | "🎲 Surprise" |

### Styles (`src/tui/styles.tcss`)

| Area | Before | After |
|------|--------|-------|
| `#main-content` padding | `1 2` | `1 2 0 2` |
| `#prompt-panel` padding | `1 2` | `1 2 0 2` |
| `#prompt-input` height | 4 | 3 |
| `#prompt-panel .title` margin-bottom | 1 | 0 |
| `#progress-panel` padding | `1 2` | `0 2` |
| Progress title/label/steps margin | various | all `0` |
| `#output-panel` padding | `1 2` | `0 2 1 2` |
| `#track-table` max-height | 12 | 8 |
| `#output-summary` | exists | removed |
| `#quality-display` margin | 1 | `1 0 0 0` |
| `#file-info-badge` | padded, bg color | minimal, no bg |
| Quick actions | `height: auto` | `height: 3` |
| `.action-btn` min-width | 16 | 10 |

## Files Modified

| File | Changes |
|------|---------|
| `src/tui/widgets/output_panel.py` | Remove title, summary, 2 buttons; compact quality/badge/path |
| `src/tui/widgets/progress_panel.py` | Remove title; short labels; compact steps |
| `src/tui/widgets/prompt_input.py` | Shorter button labels |
| `src/tui/styles.tcss` | Tighten all padding/margins/heights |

## Verification

- TUI launches without errors
- All panels visible without excessive scrolling
- Generation pipeline still works end-to-end
- Quick action buttons functional
