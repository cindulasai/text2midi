# PLAN-004: TUI Modernization & DAW Integration

**Spec:** SPEC-004-TUI-MODERNIZATION  
**Estimated Effort:** 2–3 days  
**Prerequisites:** Existing TUI (PLAN-001 completed), Python 3.11+, Windows 10+  

---

## Problem Statement

The current TUI generates MIDI files but requires the user to manually navigate
to the output folder in Windows Explorer and drag files into their DAW (Ableton
Live, FL Studio, etc.). This breaks the creative flow and makes the TUI feel
incomplete. Additionally, the interface lacks several modern UX patterns that would
make it feel premium and polished.

## Solution Overview

1. **Clipboard File-Drop (CF_HDROP)** — Place the generated MIDI file on the
   Windows clipboard in CF_HDROP format, allowing the user to simply press
   `Ctrl+V` in their DAW to paste the file directly.
2. **Copy Path to Clipboard** — Cross-platform fallback that copies the full file
   path as text.
3. **Open in Default App** — Launch the MIDI file in the system's default
   application (or a detected DAW).
4. **Quick Actions Toolbar** — Modern action bar in the output panel with
   clipboard/open/folder buttons and keyboard shortcuts.
5. **MIDI File Info Badge** — Show file size, track count, and duration at a glance.
6. **Enhanced Visual Polish** — Animated progress steps, better color coding,
   improved spacing, and micro-interactions.

---

## Phase 1: Clipboard File-Drop Engine (Core Feature)

### Step 1: Create Platform-Aware Clipboard Module

Create `src/tui/clipboard.py`:
- `copy_file_to_clipboard(file_path: str) -> bool` — Main API
- **Windows (CF_HDROP):** Use `ctypes` to call Win32 APIs:
  - `OpenClipboard`, `EmptyClipboard`, `SetClipboardData`, `CloseClipboard`
  - Build `DROPFILES` struct: 20-byte header + null-terminated wide-char path + double null
  - `GlobalAlloc` / `GlobalLock` / `GlobalUnlock` for memory management
  - CF_HDROP format constant = 15
  - After this, the user can `Ctrl+V` in Ableton Live, FL Studio, Reaper, etc.
- **macOS fallback:** Use `subprocess.run(["osascript", "-e", ...])` with AppleScript
  to set clipboard to POSIX file
- **Linux fallback:** Use `xclip -selection clipboard` with file path as text
- `copy_path_to_clipboard(file_path: str) -> bool` — Text-only path copy via `pyperclip`
- All functions return `True` on success, `False` on failure with logged error

### Step 2: Create DAW Launcher Utility

Create `src/tui/daw_launcher.py`:
- `open_in_default_app(file_path: str) -> bool` — Uses `os.startfile` (Windows),
  `open` (macOS), `xdg-open` (Linux)
- `detect_installed_daws() -> List[str]` — Check common DAW install paths on Windows:
  - Ableton Live: `C:\ProgramData\Ableton\Live *\Program\Ableton Live *.exe`
  - FL Studio: `C:\Program Files\Image-Line\FL Studio *\FL64.exe`
  - Reaper: `C:\Program Files\REAPER (x64)\reaper.exe`
  - Logic Pro: `/Applications/Logic Pro.app` (macOS)
- `open_in_daw(file_path: str, daw_name: str) -> bool` — Launch specific DAW with file

---

## Phase 2: Output Panel Quick Actions

### Step 3: Add Quick Action Buttons to OutputPanel

Modify `src/tui/widgets/output_panel.py`:
- Replace existing button row with a modern quick-actions toolbar:
  - `📋 Copy to DAW (Ctrl+C)` — Calls `copy_file_to_clipboard()` (CF_HDROP)
  - `📁 Open Folder` — Opens containing folder (existing)
  - `🎹 Open in App` — Opens MIDI in default app
  - `📝 Copy Path` — Copies file path as text
  - `🔑 Change API Key` — Existing
- Each button shows a toast notification on success
- Keyboard shortcuts active when output panel is visible

### Step 4: Add MIDI File Info Badge

In `OutputPanel.show_results()`:
- Calculate and display file info badge:
  - File size (e.g., "12.4 KB")
  - Track count (e.g., "5 tracks")
  - Total duration (e.g., "2m 30s")
  - Genre tag (from intent)
- Display as a compact horizontal info bar above the track table
- Use color-coded labels matching Catppuccin theme

---

## Phase 3: Enhanced Visual Polish

### Step 5: Improve Progress Panel Animations

Modify `src/tui/widgets/progress_panel.py`:
- Add checkmark (✓) for completed steps, spinner (⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏) for active step
- Color-code steps: completed = green (#a6e3a1), active = blue (#89b4fa),
  pending = dim (#6c7086)
- Show elapsed time per step
- Add completion celebration: brief "🎉 Done!" animation

### Step 6: Add Keyboard Shortcut Hints

Modify `src/tui/styles.tcss`:
- Add subtle keyboard shortcut indicators on buttons
- Improve button hover states with smooth color transitions
- Add focus ring styles for better keyboard navigation visibility
- Ensure consistent spacing and alignment across all panels

### Step 7: Update Main App Keybindings

Modify `main_tui.py`:
- Add `Ctrl+C` binding → Copy MIDI to clipboard (when output visible)
- Add `Ctrl+D` binding → Open in default app (when output visible)
- Update Footer to show context-aware bindings

---

## Phase 4: Testing & Integration

### Step 8: Test Clipboard File-Drop

Manual testing checklist:
- [ ] Generate a MIDI file via TUI
- [ ] Press "Copy to DAW" button
- [ ] Open Ableton Live → Ctrl+V → MIDI file appears on track
- [ ] Open FL Studio → Ctrl+V → MIDI file appears
- [ ] Verify toast notification shows success/failure
- [ ] Test "Copy Path" copies correct path
- [ ] Test "Open in App" launches default program
- [ ] Test "Open Folder" still works

### Step 9: Unit Tests

Create `tests/test_tui/test_clipboard.py`:
- Test CF_HDROP struct building (Windows)
- Test path copy fallback
- Test error handling for missing files
- Test cross-platform detection

---

## Technical Notes

### Windows CF_HDROP Clipboard Format

The CF_HDROP format uses a `DROPFILES` structure:
```
struct DROPFILES {
    DWORD pFiles;    // Offset to file list (always 20 for wide chars)
    POINT pt;        // Drop point (0,0 for clipboard)
    BOOL  fNC;       // Non-client area flag (FALSE)
    BOOL  fWide;     // Wide char flag (TRUE for Unicode)
};
// Followed by: null-terminated wide-char file path + extra null terminator
```

This is the same format Windows Explorer uses when you Ctrl+C a file. DAWs that
accept file drops (virtually all of them) will recognize this format on Ctrl+V.

### No Additional Dependencies Required

The implementation uses only:
- `ctypes` (stdlib) — Win32 API calls for CF_HDROP
- `struct` (stdlib) — Binary data packing
- `subprocess` (stdlib) — macOS/Linux fallbacks
- `pyperclip` (already available) — Text clipboard fallback

---

## Dependency Chain

```
Phase 1 (Clipboard Engine)
  └── Phase 2 (Quick Actions UI)
        └── Phase 3 (Visual Polish)
              └── Phase 4 (Testing)
```

All phases are sequential. Phase 1 provides the core clipboard API. Phase 2
integrates it into the UI. Phase 3 adds visual improvements. Phase 4 validates
everything works end-to-end.
