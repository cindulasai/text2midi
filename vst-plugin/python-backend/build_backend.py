# -*- coding: utf-8 -*-
"""
PyInstaller build script for the text2midi backend server.
Produces a self-contained executable that the VST3 plugin can launch.

Usage:
    cd vst-plugin/python-backend
    pyinstaller build_backend.spec          # after generating .spec
    # OR simply run:
    python build_backend.py                 # wraps PyInstaller API
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
BACKEND_DIR = Path(__file__).resolve().parent
DIST_DIR = BACKEND_DIR / "dist"
BUILD_DIR = BACKEND_DIR / "build"


def build():
    print("=== text2midi Backend Builder ===")

    # Ensure PyInstaller is available
    try:
        import PyInstaller  # noqa: F401
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

    # Clean previous build artefacts
    for d in (DIST_DIR, BUILD_DIR):
        if d.exists():
            shutil.rmtree(d)

    # Collect hidden imports the pipeline needs
    hidden_imports = [
        "src.agents.graph",
        "src.agents.state",
        "src.config.llm",
        "src.config.settings",
        "src.midigent",
        "src.app",
        "dotenv",
        "langchain_core",
        "langchain_groq",
        "langchain_openai",
        "langgraph",
        "midiutil",
        "platformdirs",
        "pydantic",
        "fastapi",
        "uvicorn",
        "starlette",
        "httptools",
        "uvloop" if sys.platform != "win32" else "asyncio",
    ]

    hidden_flags = []
    for hi in hidden_imports:
        hidden_flags.extend(["--hidden-import", hi])

    # Data files to bundle: the entire src/ tree
    data_flags = [
        "--add-data", f"{REPO_ROOT / 'src'}{os.pathsep}src",
    ]

    # Also bring in the .env if it exists
    env_path = REPO_ROOT / ".env"
    if env_path.exists():
        data_flags.extend(["--add-data", f"{env_path}{os.pathsep}."])

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onedir",
        "--name", "text2midi-backend",
        "--noconfirm",
        "--clean",
        "--distpath", str(DIST_DIR),
        "--workpath", str(BUILD_DIR),
        *hidden_flags,
        *data_flags,
        str(BACKEND_DIR / "server.py"),
    ]

    print(f"Running: {' '.join(cmd)}")
    subprocess.check_call(cmd)

    output_dir = DIST_DIR / "text2midi-backend"
    print(f"\n✅ Build complete: {output_dir}")
    print(f"   Executable: {output_dir / 'text2midi-backend.exe' if sys.platform == 'win32' else output_dir / 'text2midi-backend'}")
    return output_dir


if __name__ == "__main__":
    build()
