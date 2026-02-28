"""
installer/build_launcher.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Builds a tiny native launcher executable using PyInstaller.

The exe is just a ~5MB wrapper that calls  uv run python main_tui.py.
It is NOT a monolithic bundle of the entire application.
If PyInstaller is unavailable or fails, the script creates a plain .bat or .sh
fallback launcher instead — so the user is never left without a way to run the app.
"""

from __future__ import annotations

import os
import platform
import subprocess
import sys
import textwrap
import time
from pathlib import Path

# ── Paths ────────────────────────────────────────────────────────
INSTALLER_DIR = Path(__file__).resolve().parent
PROJECT_DIR = INSTALLER_DIR.parent
STUB_PATH = INSTALLER_DIR / "_launcher_stub.py"

LAUNCHER_NAME = "text2midi"

# ── Stub source embedded here (written to disk before PyInstaller) ──
STUB_CODE = textwrap.dedent(r'''
    """
    text2midi launcher stub — compiled into a tiny native executable.
    Finds uv, then runs  uv run python main_tui.py.
    """
    import os
    import sys
    import shutil
    import subprocess

    def find_uv() -> str | None:
        """Locate the uv binary, searching common locations."""
        found = shutil.which("uv")
        if found:
            return found
        # Check common install locations
        home = os.path.expanduser("~")
        candidates = [
            os.path.join(home, ".local", "bin", "uv"),
            os.path.join(home, ".cargo", "bin", "uv"),
            r"C:\Users\{}\\.local\\bin\\uv.exe".format(os.getenv("USERNAME", "")),
            "/opt/homebrew/bin/uv",
            "/usr/local/bin/uv",
        ]
        for c in candidates:
            if os.path.isfile(c):
                return c
        return None

    def main() -> None:
        # Determine the project directory (exe lives inside it)
        if getattr(sys, "frozen", False):
            project_dir = os.path.dirname(os.path.abspath(sys.executable))
        else:
            project_dir = os.path.dirname(os.path.abspath(__file__))

        uv_path = find_uv()
        if not uv_path:
            print()
            print("  ERROR:  Could not find 'uv' (fast Python package manager).")
            print("          Please run the installer first, or install uv manually:")
            print("            curl -LsSf https://astral.sh/uv/install.sh | sh")
            print("            (or: pip install uv)")
            print()
            input("  Press ENTER to close...")
            sys.exit(1)

        # Launch the TUI
        cmd = [uv_path, "run", "python", "main_tui.py"] + sys.argv[1:]
        try:
            result = subprocess.run(cmd, cwd=project_dir)
            sys.exit(result.returncode)
        except KeyboardInterrupt:
            sys.exit(0)
        except Exception as exc:
            print(f"\n  ERROR:  Failed to start text2midi — {exc}")
            print(f"          Command: {' '.join(cmd)}")
            print(f"          Working dir: {project_dir}")
            print()
            input("  Press ENTER to close...")
            sys.exit(1)

    if __name__ == "__main__":
        main()
''').lstrip()


def write_stub() -> Path:
    """Write the launcher stub source to disk."""
    STUB_PATH.write_text(STUB_CODE, encoding="utf-8")
    return STUB_PATH


def ensure_pyinstaller() -> bool:
    """Make sure PyInstaller is available, attempt install if not."""
    try:
        import PyInstaller  # noqa: F401
        return True
    except ImportError:
        pass

    print("  [..] PyInstaller not found — installing...")
    for _ in range(2):
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "pyinstaller", "--quiet"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            return True
        except subprocess.CalledProcessError:
            time.sleep(3)
    return False


def build_exe() -> Path | None:
    """Build the launcher exe.  Returns the path on success, None on failure."""
    write_stub()

    if not ensure_pyinstaller():
        print("  [WARNING] Could not install PyInstaller — will create a script launcher instead.")
        return None

    print("  [..] Building launcher executable (this takes about a minute)...")

    exe_name = LAUNCHER_NAME
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--console",
        "--name", exe_name,
        "--distpath", str(PROJECT_DIR),
        "--workpath", str(INSTALLER_DIR / "build"),
        "--specpath", str(INSTALLER_DIR),
        "--clean",
        "--noconfirm",
        str(STUB_PATH),
    ]

    for attempt in range(1, 4):
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=600,
            )
            if result.returncode == 0:
                suffix = ".exe" if platform.system() == "Windows" else ""
                exe_path = PROJECT_DIR / f"{exe_name}{suffix}"
                if exe_path.exists():
                    print(f"  [OK] Launcher built: {exe_path.name}")
                    _cleanup_build_artifacts()
                    return exe_path
                else:
                    print(f"  [WARNING] Build completed but exe not found — attempt {attempt}/3")
            else:
                print(f"  [WARNING] Build attempt {attempt}/3 failed:")
                # Print last 5 lines of stderr for debugging
                for line in result.stderr.strip().splitlines()[-5:]:
                    print(f"           {line}")
        except subprocess.TimeoutExpired:
            print(f"  [WARNING] Build attempt {attempt}/3 timed out.")
        except Exception as exc:
            print(f"  [WARNING] Build attempt {attempt}/3 error: {exc}")

        if attempt < 3:
            print("           Retrying in 5 seconds...")
            time.sleep(5)

    return None


def create_fallback_launcher() -> Path:
    """Create a plain script launcher as fallback when PyInstaller fails."""
    system = platform.system()

    if system == "Windows":
        launcher = PROJECT_DIR / "text2midi.bat"
        launcher.write_text(
            '@echo off\r\n'
            'cd /d "%~dp0"\r\n'
            'uv run python main_tui.py %*\r\n',
            encoding="utf-8",
        )
        print(f"  [OK] Created fallback launcher: {launcher.name}")
        return launcher
    else:
        launcher = PROJECT_DIR / "text2midi"
        launcher.write_text(
            '#!/usr/bin/env bash\n'
            'cd "$(dirname "${BASH_SOURCE[0]}")"\n'
            'exec uv run python main_tui.py "$@"\n',
            encoding="utf-8",
        )
        launcher.chmod(0o755)
        print(f"  [OK] Created fallback launcher: {launcher.name}")
        return launcher


def _cleanup_build_artifacts() -> None:
    """Remove PyInstaller temp directories."""
    import shutil
    build_dir = INSTALLER_DIR / "build"
    if build_dir.exists():
        shutil.rmtree(build_dir, ignore_errors=True)
    # __pycache__ that PyInstaller sometimes creates
    pycache = INSTALLER_DIR / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache, ignore_errors=True)


def main() -> None:
    print()
    print("  ══════════════════════════════════════════════════════════════")
    print("    text2midi — Building Launcher")
    print("  ══════════════════════════════════════════════════════════════")
    print()

    exe_path = build_exe()
    if exe_path is None:
        print("  [..] Falling back to script-based launcher...")
        create_fallback_launcher()

    # Cleanup stub source (it was only needed during build)
    if STUB_PATH.exists():
        STUB_PATH.unlink(missing_ok=True)

    print()
    print("  Done!")
    print()


if __name__ == "__main__":
    main()
