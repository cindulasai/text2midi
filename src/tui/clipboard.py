# -*- coding: utf-8 -*-
"""
Platform-Aware Clipboard Module for MIDI File Transfer

Provides two clipboard operations:
1. copy_file_to_clipboard() — Places a file on the clipboard in native format
   (CF_HDROP on Windows) so DAWs can accept Ctrl+V paste.
2. copy_path_to_clipboard() — Copies the file path as plain text.

Windows CF_HDROP format allows direct paste into:
- Ableton Live
- FL Studio
- Reaper
- Logic Pro (macOS)
- Any DAW that accepts file drops
"""

from __future__ import annotations

import logging
import os
import platform
import struct
import subprocess
from pathlib import Path

logger = logging.getLogger(__name__)


# ------------------------------------------------------------------ #
# Public API
# ------------------------------------------------------------------ #


def copy_file_to_clipboard(file_path: str) -> bool:
    """
    Copy a file to the system clipboard in native file-drop format.

    On Windows, uses CF_HDROP format so the file can be pasted (Ctrl+V)
    directly into DAWs like Ableton Live, FL Studio, Reaper, etc.

    On macOS, uses AppleScript to set the clipboard to a file reference.
    On Linux, falls back to copying the file path as text.

    Returns True on success, False on failure.
    """
    path = Path(file_path).resolve()
    if not path.exists():
        logger.error("File does not exist: %s", path)
        return False

    system = platform.system()
    try:
        if system == "Windows":
            return _windows_copy_file_to_clipboard(str(path))
        elif system == "Darwin":
            return _macos_copy_file_to_clipboard(str(path))
        else:
            # Linux fallback: copy path as text
            return copy_path_to_clipboard(str(path))
    except Exception as exc:
        logger.error("Failed to copy file to clipboard: %s", exc)
        return False


def copy_path_to_clipboard(file_path: str) -> bool:
    """
    Copy the file path as plain text to the system clipboard.

    Cross-platform. Returns True on success, False on failure.
    """
    path = Path(file_path).resolve()
    path_str = str(path)

    system = platform.system()
    try:
        if system == "Windows":
            return _windows_copy_text(path_str)
        elif system == "Darwin":
            subprocess.run(
                ["pbcopy"],
                input=path_str.encode("utf-8"),
                check=True,
                timeout=5,
            )
            return True
        else:
            # Try xclip first, then xsel
            for cmd in [
                ["xclip", "-selection", "clipboard"],
                ["xsel", "--clipboard", "--input"],
            ]:
                try:
                    subprocess.run(
                        cmd,
                        input=path_str.encode("utf-8"),
                        check=True,
                        timeout=5,
                    )
                    return True
                except FileNotFoundError:
                    continue
            logger.error("No clipboard tool found (install xclip or xsel)")
            return False
    except Exception as exc:
        logger.error("Failed to copy path to clipboard: %s", exc)
        return False


# ------------------------------------------------------------------ #
# Windows Implementation — CF_HDROP
# ------------------------------------------------------------------ #


def _windows_copy_file_to_clipboard(file_path: str) -> bool:
    """
    Place a file on the Windows clipboard using CF_HDROP format.

    This uses the same format Windows Explorer uses when you Ctrl+C a file.
    DAWs and all applications that accept file drops will recognize it.

    DROPFILES structure (20 bytes):
        DWORD pFiles   = 20  (offset to file list)
        LONG  pt.x     = 0   (drop point x)
        LONG  pt.y     = 0   (drop point y)
        BOOL  fNC      = 0   (not non-client area)
        BOOL  fWide    = 1   (Unicode file names)
    Followed by:
        Wide-char null-terminated file path
        Extra null terminator (double-null ends the list)
    """
    import ctypes
    import ctypes.wintypes as wintypes

    CF_HDROP = 15
    GMEM_MOVEABLE = 0x0002
    GMEM_ZEROINIT = 0x0040
    GHND = GMEM_MOVEABLE | GMEM_ZEROINIT

    kernel32 = ctypes.windll.kernel32
    user32 = ctypes.windll.user32

    # Set proper function signatures for 64-bit compatibility
    kernel32.GlobalAlloc.argtypes = [wintypes.UINT, ctypes.c_size_t]
    kernel32.GlobalAlloc.restype = ctypes.c_void_p

    kernel32.GlobalLock.argtypes = [ctypes.c_void_p]
    kernel32.GlobalLock.restype = ctypes.c_void_p

    kernel32.GlobalUnlock.argtypes = [ctypes.c_void_p]
    kernel32.GlobalUnlock.restype = wintypes.BOOL

    kernel32.GlobalFree.argtypes = [ctypes.c_void_p]
    kernel32.GlobalFree.restype = ctypes.c_void_p

    user32.OpenClipboard.argtypes = [wintypes.HWND]
    user32.OpenClipboard.restype = wintypes.BOOL

    user32.EmptyClipboard.argtypes = []
    user32.EmptyClipboard.restype = wintypes.BOOL

    user32.SetClipboardData.argtypes = [wintypes.UINT, ctypes.c_void_p]
    user32.SetClipboardData.restype = ctypes.c_void_p

    user32.CloseClipboard.argtypes = []
    user32.CloseClipboard.restype = wintypes.BOOL

    # Build the DROPFILES data
    # Header: 20 bytes (pFiles=20, pt=(0,0), fNC=0, fWide=1)
    header = struct.pack("IiiII", 20, 0, 0, 0, 1)

    # File path as wide string (UTF-16LE) with null terminator
    file_path_wide = file_path.encode("utf-16-le") + b"\x00\x00"

    # Double null terminator to end the file list
    data = header + file_path_wide + b"\x00\x00"

    # Allocate global memory
    h_global = kernel32.GlobalAlloc(GHND, len(data))
    if not h_global:
        logger.error("GlobalAlloc failed")
        return False

    # Lock memory and copy data
    p_global = kernel32.GlobalLock(h_global)
    if not p_global:
        kernel32.GlobalFree(h_global)
        logger.error("GlobalLock failed")
        return False

    ctypes.memmove(p_global, data, len(data))
    kernel32.GlobalUnlock(h_global)

    # Open clipboard, empty it, set CF_HDROP data, close
    if not user32.OpenClipboard(None):
        kernel32.GlobalFree(h_global)
        logger.error("OpenClipboard failed")
        return False

    try:
        user32.EmptyClipboard()
        result = user32.SetClipboardData(CF_HDROP, h_global)
        if not result:
            kernel32.GlobalFree(h_global)
            logger.error("SetClipboardData failed")
            return False
    finally:
        user32.CloseClipboard()

    logger.info("File copied to clipboard (CF_HDROP): %s", file_path)
    return True


def _windows_copy_text(text: str) -> bool:
    """Copy plain text to Windows clipboard using CF_UNICODETEXT."""
    import ctypes
    import ctypes.wintypes as wintypes

    CF_UNICODETEXT = 13
    GMEM_MOVEABLE = 0x0002
    GMEM_ZEROINIT = 0x0040
    GHND = GMEM_MOVEABLE | GMEM_ZEROINIT

    kernel32 = ctypes.windll.kernel32
    user32 = ctypes.windll.user32

    # Set proper function signatures for 64-bit compatibility
    kernel32.GlobalAlloc.argtypes = [wintypes.UINT, ctypes.c_size_t]
    kernel32.GlobalAlloc.restype = ctypes.c_void_p

    kernel32.GlobalLock.argtypes = [ctypes.c_void_p]
    kernel32.GlobalLock.restype = ctypes.c_void_p

    kernel32.GlobalUnlock.argtypes = [ctypes.c_void_p]
    kernel32.GlobalUnlock.restype = wintypes.BOOL

    kernel32.GlobalFree.argtypes = [ctypes.c_void_p]
    kernel32.GlobalFree.restype = ctypes.c_void_p

    user32.OpenClipboard.argtypes = [wintypes.HWND]
    user32.OpenClipboard.restype = wintypes.BOOL

    user32.EmptyClipboard.argtypes = []
    user32.EmptyClipboard.restype = wintypes.BOOL

    user32.SetClipboardData.argtypes = [wintypes.UINT, ctypes.c_void_p]
    user32.SetClipboardData.restype = ctypes.c_void_p

    user32.CloseClipboard.argtypes = []
    user32.CloseClipboard.restype = wintypes.BOOL

    # Encode as UTF-16LE with null terminator
    text_wide = text.encode("utf-16-le") + b"\x00\x00"

    h_global = kernel32.GlobalAlloc(GHND, len(text_wide))
    if not h_global:
        return False

    p_global = kernel32.GlobalLock(h_global)
    if not p_global:
        kernel32.GlobalFree(h_global)
        return False

    ctypes.memmove(p_global, text_wide, len(text_wide))
    kernel32.GlobalUnlock(h_global)

    if not user32.OpenClipboard(None):
        kernel32.GlobalFree(h_global)
        return False

    try:
        user32.EmptyClipboard()
        result = user32.SetClipboardData(CF_UNICODETEXT, h_global)
        if not result:
            kernel32.GlobalFree(h_global)
            return False
    finally:
        user32.CloseClipboard()

    return True


# ------------------------------------------------------------------ #
# macOS Implementation
# ------------------------------------------------------------------ #


def _macos_copy_file_to_clipboard(file_path: str) -> bool:
    """
    Place a file on the macOS clipboard using AppleScript.

    This sets the clipboard to a file reference that Finder and other apps
    (including Logic Pro) can paste.
    """
    script = f'''
    set the clipboard to (POSIX file "{file_path}")
    '''
    result = subprocess.run(
        ["osascript", "-e", script],
        capture_output=True,
        text=True,
        timeout=10,
    )
    if result.returncode != 0:
        logger.error("AppleScript clipboard failed: %s", result.stderr)
        return False

    logger.info("File copied to clipboard (macOS): %s", file_path)
    return True
