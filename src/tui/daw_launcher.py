# -*- coding: utf-8 -*-
"""
DAW Launcher Utility

Provides utilities to open MIDI files in the default application or a specific DAW.
"""

from __future__ import annotations

import glob
import logging
import os
import platform
import subprocess
from pathlib import Path
from typing import List

logger = logging.getLogger(__name__)


# ------------------------------------------------------------------ #
# Public API
# ------------------------------------------------------------------ #


def open_in_default_app(file_path: str) -> bool:
    """
    Open a file with the system's default application.

    Returns True on success, False on failure.
    """
    path = Path(file_path).resolve()
    if not path.exists():
        logger.error("File does not exist: %s", path)
        return False

    system = platform.system()
    try:
        if system == "Windows":
            os.startfile(str(path))
        elif system == "Darwin":
            subprocess.Popen(["open", str(path)])
        else:
            subprocess.Popen(["xdg-open", str(path)])
        logger.info("Opened in default app: %s", path)
        return True
    except Exception as exc:
        logger.error("Failed to open file: %s", exc)
        return False


def open_folder(file_path: str) -> bool:
    """
    Open the containing folder of a file, highlighting the file if possible.

    Returns True on success, False on failure.
    """
    path = Path(file_path).resolve()
    folder = path.parent if path.is_file() else path

    if not folder.exists():
        logger.error("Folder does not exist: %s", folder)
        return False

    system = platform.system()
    try:
        if system == "Windows":
            if path.is_file():
                # Highlight the file in Explorer
                subprocess.Popen(["explorer", "/select,", str(path)])
            else:
                os.startfile(str(folder))
        elif system == "Darwin":
            if path.is_file():
                subprocess.Popen(["open", "-R", str(path)])
            else:
                subprocess.Popen(["open", str(folder)])
        else:
            subprocess.Popen(["xdg-open", str(folder)])
        return True
    except Exception as exc:
        logger.error("Failed to open folder: %s", exc)
        return False


def detect_installed_daws() -> List[str]:
    """
    Detect commonly installed DAWs on the system.

    Returns a list of DAW names that are found.
    """
    system = platform.system()
    found: List[str] = []

    if system == "Windows":
        daw_patterns = {
            "Ableton Live": [
                r"C:\ProgramData\Ableton\Live *\Program\Ableton Live *.exe",
                r"C:\Program Files\Ableton\Live *\Program\Ableton Live *.exe",
            ],
            "FL Studio": [
                r"C:\Program Files\Image-Line\FL Studio *\FL64.exe",
                r"C:\Program Files (x86)\Image-Line\FL Studio *\FL.exe",
            ],
            "Reaper": [
                r"C:\Program Files\REAPER (x64)\reaper.exe",
                r"C:\Program Files\REAPER\reaper.exe",
            ],
            "Bitwig Studio": [
                r"C:\Program Files\Bitwig Studio\Bitwig Studio.exe",
            ],
            "Cubase": [
                r"C:\Program Files\Steinberg\Cubase *\Cubase*.exe",
            ],
        }
        for daw_name, patterns in daw_patterns.items():
            for pattern in patterns:
                if glob.glob(pattern):
                    found.append(daw_name)
                    break

    elif system == "Darwin":
        mac_apps = {
            "Logic Pro": "/Applications/Logic Pro.app",
            "Ableton Live": "/Applications/Ableton Live * Suite.app",
            "GarageBand": "/Applications/GarageBand.app",
            "Reaper": "/Applications/REAPER.app",
        }
        for daw_name, pattern in mac_apps.items():
            if glob.glob(pattern):
                found.append(daw_name)

    return found
