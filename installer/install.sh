#!/usr/bin/env bash
# ================================================================
#  text2midi  —  AI-Powered MIDI Composer
#  One-Touch Installer for macOS / Linux
#
#  Designed for people with ZERO technical background.
#  Every step has fallbacks.  If something fails the user always
#  gets a friendly message and an option to retry, skip, or quit.
# ================================================================

# We do NOT use "set -e" because we handle every error individually.
# "set -u" catches unset variable typos.  "pipefail" catches pipe errors.
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

# ── Colours (degrade gracefully on dumb terminals) ───────────────
if [[ -t 1 ]] && command -v tput &>/dev/null && [[ "$(tput colors 2>/dev/null || echo 0)" -ge 8 ]]; then
    RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[0;33m'
    CYAN='\033[0;36m'; BOLD='\033[1m'; NC='\033[0m'
else
    RED=''; GREEN=''; YELLOW=''; CYAN=''; BOLD=''; NC=''
fi

ok()   { printf "  ${GREEN}[OK]${NC} %s\n" "$1"; }
info() { printf "  ${CYAN}[..]${NC} %s\n" "$1"; }
warn() { printf "  ${YELLOW}[WARNING]${NC} %s\n" "$1"; }
err()  { printf "  ${RED}[ERROR]${NC} %s\n" "$1"; }

prompt_yn() {
    local msg="$1" default="${2:-Y}" yn
    if [[ "$default" == "Y" ]]; then
        read -rp "  $msg [Y/n]: " yn
        [[ -z "$yn" || "$yn" =~ ^[Yy] ]]
    else
        read -rp "  $msg [y/N]: " yn
        [[ "$yn" =~ ^[Yy] ]]
    fi
}

echo ""
printf "${BOLD}${CYAN}"
echo "  ================================================================"
echo "    text2midi — AI-Powered MIDI Composer"
echo "    One-Touch Installer"
echo "  ================================================================"
printf "${NC}\n"

# ── Consent ──────────────────────────────────────────────────────
echo "  This installer will set up everything you need:"
echo ""
echo "    1. Python 3.12   (programming runtime  — if not installed)"
echo "    2. uv            (fast package manager — if not installed)"
echo "    3. App libraries  (downloaded into a local folder)"
echo "    4. AI provider    (optional — you can skip and set up later)"
echo "    5. Launcher       (a script you can run or double-click)"
echo "    6. VST3 Plugin    (optional — for use inside DAWs)"
echo ""
echo "  Your personal files are NEVER touched."
echo ""
if ! prompt_yn "Continue?"; then
    echo "  No problem — run this script whenever you are ready."
    exit 0
fi
echo ""

OS="$(uname -s)"
ARCH="$(uname -m)"

# ── Network check ────────────────────────────────────────────────
info "Checking internet connection..."
NET_OK=0
# macOS (BSD) ping -W is milliseconds; Linux (iputils) ping -W is seconds
if [[ "$OS" == "Darwin" ]]; then _PW=4000; else _PW=4; fi
if ping -c 1 -W "$_PW" dns.google &>/dev/null; then NET_OK=1
elif ping -c 1 -W "$_PW" 8.8.8.8 &>/dev/null; then NET_OK=1
elif ping -c 1 -W "$_PW" 1.1.1.1 &>/dev/null; then NET_OK=1
fi

if [[ "$NET_OK" == "1" ]]; then
    ok "Internet connection verified."
else
    warn "No internet connection detected."
    echo "         The installer needs internet to download components."
    echo ""
    if ! prompt_yn "Continue anyway?"; then
        exit 0
    fi
fi
echo ""

# ================================================================
#  STEP 1 / 6  —  Python Runtime
# ================================================================
echo "  ──────────────────────────────────────────────────────────────"
echo "   Step 1 of 6 : Python Runtime"
echo "  ──────────────────────────────────────────────────────────────"

find_python() {
    for cmd in python3.13 python3.12 python3.11 python3 python; do
        if command -v "$cmd" &>/dev/null; then
            local ver
            ver="$("$cmd" -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")' 2>/dev/null)" || continue
            local major="${ver%%.*}"
            local minor="${ver#*.}"
            if [[ "$major" -ge 3 && "$minor" -ge 11 ]]; then
                echo "$cmd"
                return 0
            fi
        fi
    done
    return 1
}

PYTHON_CMD=""
if PYTHON_CMD=$(find_python); then
    ok "Found Python ($($PYTHON_CMD --version 2>&1))"
else
    info "Python 3.11+ not found. Installing..."
    echo ""

    install_ok=0

    if [[ "$OS" == "Darwin" ]]; then
        # ── macOS ── Homebrew ──────────────────────────────────
        if ! command -v brew &>/dev/null; then
            info "Installing Homebrew first (macOS package manager)..."
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)" && {
                # Add to PATH — Apple Silicon vs Intel
                if [[ "$ARCH" == "arm64" ]]; then
                    eval "$(/opt/homebrew/bin/brew shellenv 2>/dev/null)" || true
                else
                    eval "$(/usr/local/bin/brew shellenv 2>/dev/null)" || true
                fi
            }
        fi
        if command -v brew &>/dev/null; then
            info "Installing Python 3.12 via Homebrew..."
            if brew install python@3.12 2>/dev/null || brew install python3 2>/dev/null; then
                install_ok=1
            fi
        fi
    else
        # ── Linux ── try the distro package manager ────────────
        if command -v apt-get &>/dev/null; then
            info "Installing Python via apt..."
            sudo apt-get update -qq 2>/dev/null || true
            if sudo apt-get install -y -qq python3.12 python3.12-venv python3-pip 2>/dev/null \
               || sudo apt-get install -y -qq python3 python3-venv python3-pip 2>/dev/null; then
                install_ok=1
            fi
        elif command -v dnf &>/dev/null; then
            info "Installing Python via dnf..."
            if sudo dnf install -y python3.12 python3.12-pip 2>/dev/null \
               || sudo dnf install -y python3 python3-pip 2>/dev/null; then
                install_ok=1
            fi
        elif command -v pacman &>/dev/null; then
            info "Installing Python via pacman..."
            if sudo pacman -S --noconfirm python python-pip 2>/dev/null; then
                install_ok=1
            fi
        elif command -v zypper &>/dev/null; then
            info "Installing Python via zypper..."
            if sudo zypper install -y python312 python312-pip 2>/dev/null \
               || sudo zypper install -y python3 python3-pip 2>/dev/null; then
                install_ok=1
            fi
        elif command -v apk &>/dev/null; then
            info "Installing Python via apk..."
            if sudo apk add python3 py3-pip 2>/dev/null; then
                install_ok=1
            fi
        fi
    fi

    if [[ "$install_ok" == "0" ]]; then
        err "Could not auto-install Python on this system."
        err "Please install Python 3.11+ manually:"
        echo "         https://www.python.org/downloads/"
        err "Then re-run this script."
        exit 1
    fi

    PYTHON_CMD=$(find_python) || {
        err "Python was installed but 3.11+ still not found in PATH."
        err "Try opening a new terminal window and running this script again."
        exit 1
    }
    ok "Python installed ($($PYTHON_CMD --version 2>&1))"
fi
echo ""

# ================================================================
#  STEP 2 / 6  —  uv Package Manager
# ================================================================
echo "  ──────────────────────────────────────────────────────────────"
echo "   Step 2 of 6 : Package Manager (uv)"
echo "  ──────────────────────────────────────────────────────────────"

if command -v uv &>/dev/null; then
    ok "uv is already installed."
else
    info "Installing uv (fast Python package manager)..."

    # Security: download to a temp file, verify, then execute
    UV_INSTALLER="$(mktemp /tmp/text2midi_uv_XXXXXX.sh)"
    uv_install_ok=0

    if curl -LsSf https://astral.sh/uv/install.sh -o "$UV_INSTALLER" 2>/dev/null; then
        # Basic content check — should mention 'astral'
        if grep -qi "astral" "$UV_INSTALLER" 2>/dev/null; then
            if bash "$UV_INSTALLER" 2>/dev/null; then
                uv_install_ok=1
            fi
        else
            warn "uv installer content did not pass verification."
        fi
    fi
    rm -f "$UV_INSTALLER" 2>/dev/null

    # Add common locations to PATH
    export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"

    if ! command -v uv &>/dev/null && [[ "$uv_install_ok" == "0" ]]; then
        # Fallback: pip
        info "Trying pip fallback..."
        "$PYTHON_CMD" -m pip install uv --quiet 2>/dev/null \
            || "$PYTHON_CMD" -m pip install uv 2>/dev/null \
            || true
    fi

    if command -v uv &>/dev/null; then
        ok "uv installed."
    else
        err "Could not install uv."
        err "Please try manually:  curl -LsSf https://astral.sh/uv/install.sh | sh"
        err "Then re-run this script."
        exit 1
    fi
fi
echo ""

# ================================================================
#  STEP 3 / 6  —  Dependencies
# ================================================================
echo "  ──────────────────────────────────────────────────────────────"
echo "   Step 3 of 6 : Installing App Dependencies"
echo "  ──────────────────────────────────────────────────────────────"
info "This may take 2-3 minutes on first run..."
cd "$PROJECT_DIR"

dep_ok=0
for attempt in 1 2 3; do
    if [[ "$attempt" -gt 1 ]]; then
        info "Attempt $attempt of 3 — retrying after a short pause..."
        sleep 5
    fi
    if uv sync 2>/dev/null; then
        dep_ok=1
        break
    fi
done

if [[ "$dep_ok" == "1" ]]; then
    ok "All dependencies installed."
else
    warn "Dependency installation failed after 3 attempts."
    echo "         This is usually caused by a flaky internet connection."
    echo "         You can retry later by running:  cd '$PROJECT_DIR' && uv sync"
    echo "         The installer will keep going so the launcher is still created."
fi
echo ""

# ================================================================
#  STEP 4 / 6  —  AI Provider Setup  (OPTIONAL)
# ================================================================
echo "  ──────────────────────────────────────────────────────────────"
echo "   Step 4 of 6 : AI Provider Setup  (optional)"
echo "  ──────────────────────────────────────────────────────────────"
echo ""
echo "  text2midi uses an AI model to turn your words into music."
echo "  You need a free API key from one of these providers:"
echo ""
echo "    Groq        (recommended)  https://console.groq.com/keys"
echo "    Google       Gemini        https://aistudio.google.com/apikey"
echo "    OpenRouter                 https://openrouter.ai/keys"
echo ""
echo "  Groq is the easiest — sign up, create a key, paste it."
echo "  No credit card required."
echo ""
read -rp "  Press ENTER to set up now, or S to skip for later: " setup_choice

if [[ "$setup_choice" == [sS] ]]; then
    echo ""
    ok "Skipped — no problem!  You can set up anytime:"
    echo "       uv run python main.py --setup"
    echo "       Or press Ctrl+S inside the app"
else
    echo ""
    uv run python -c "
from src.config.setup_wizard import run_setup_wizard
run_setup_wizard()
" 2>/dev/null || {
        echo ""
        warn "The setup wizard had a hiccup, but do not worry!"
        echo "         You can configure your AI provider any time:"
        echo "           uv run python main.py --setup"
        echo "           Or press Ctrl+S inside the app"
    }
fi
echo ""

# ================================================================
#  STEP 5 / 6  —  Create Launcher
# ================================================================
echo "  ──────────────────────────────────────────────────────────────"
echo "   Step 5 of 6 : Creating Launcher"
echo "  ──────────────────────────────────────────────────────────────"

# Shell launcher (always works)
LAUNCHER="$PROJECT_DIR/text2midi"
cat > "$LAUNCHER" << 'LAUNCHER_SCRIPT'
#!/usr/bin/env bash
# text2midi — AI-Powered MIDI Composer launcher
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"
export PATH="$HOME/.local/bin:$HOME/.cargo/bin:/opt/homebrew/bin:/usr/local/bin:$PATH"
exec uv run python main_tui.py "$@"
LAUNCHER_SCRIPT
chmod +x "$LAUNCHER"
ok "Created: ./text2midi"

if [[ "$OS" == "Darwin" ]]; then
    # macOS: .command file is double-clickable in Finder
    COMMAND_FILE="$PROJECT_DIR/text2midi.command"
    cat > "$COMMAND_FILE" << EOF
#!/usr/bin/env bash
cd "$PROJECT_DIR"
export PATH="\$HOME/.local/bin:\$HOME/.cargo/bin:/opt/homebrew/bin:/usr/local/bin:\$PATH"
uv run python main_tui.py "\$@"
EOF
    chmod +x "$COMMAND_FILE"
    ok "Created: text2midi.command  (double-click in Finder)"
else
    # Linux: .desktop entry for application menus
    DESKTOP_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/applications"
    mkdir -p "$DESKTOP_DIR" 2>/dev/null || true
    cat > "$DESKTOP_DIR/text2midi.desktop" << EOF
[Desktop Entry]
Type=Application
Name=text2midi
Comment=AI-Powered MIDI Composer
Exec=bash -c 'cd "$PROJECT_DIR" && PATH="\$HOME/.local/bin:\$HOME/.cargo/bin:\$PATH" uv run python main_tui.py'
Terminal=true
Categories=Audio;Music;
EOF
    ok "Created desktop menu entry for text2midi"
fi
echo ""

# ── Done! ────────────────────────────────────────────────────────

# ================================================================
#  STEP 6 / 6  —  VST3 Plugin Installation  (OPTIONAL)
# ================================================================
echo "  ──────────────────────────────────────────────────────────────"
echo "   Step 6 of 6 : VST3 Plugin for DAW  (optional)"
echo "  ──────────────────────────────────────────────────────────────"
echo ""
echo "  If you use a DAW (Ableton Live, FL Studio, Bitwig, Reaper)"
echo "  you can install the text2midi VST3 plugin to generate MIDI"
echo "  directly inside your DAW."
echo ""

read -rp "  Press ENTER to install VST3 plugin, or S to skip: " vst_choice

if [[ "$vst_choice" == [sS] ]]; then
    echo ""
    ok "Skipped VST3 plugin installation."
    echo "       You can install it later by running:"
    echo "         bash installer/install_vst.sh"
else
    echo ""
    # Determine VST3 directory
    if [[ "$OS" == "Darwin" ]]; then
        VST3_SYSTEM_DIR="$HOME/Library/Audio/Plug-Ins/VST3"
    else
        VST3_SYSTEM_DIR="$HOME/.vst3"
    fi

    VST3_SOURCE=""
    # Check Release build
    if [[ -d "$PROJECT_DIR/vst-plugin/build/text2midi_artefacts/Release/VST3/text2midi.vst3" ]]; then
        VST3_SOURCE="$PROJECT_DIR/vst-plugin/build/text2midi_artefacts/Release/VST3/text2midi.vst3"
    fi
    # Check Debug build
    if [[ -z "$VST3_SOURCE" && -d "$PROJECT_DIR/vst-plugin/build/text2midi_artefacts/Debug/VST3/text2midi.vst3" ]]; then
        VST3_SOURCE="$PROJECT_DIR/vst-plugin/build/text2midi_artefacts/Debug/VST3/text2midi.vst3"
    fi

    if [[ -z "$VST3_SOURCE" ]]; then
        warn "Pre-built VST3 plugin not found."
        echo "         The plugin must be compiled from C++ source first."
        echo "         See: vst-plugin/BUILDING.md"
        echo "         After building, run:  bash installer/install_vst.sh"
    else
        VST3_DEST="$VST3_SYSTEM_DIR/text2midi.vst3"
        mkdir -p "$VST3_SYSTEM_DIR" 2>/dev/null
        # Remove old installation if present
        [[ -d "$VST3_DEST" ]] && rm -rf "$VST3_DEST" 2>/dev/null
        # Copy
        info "Installing text2midi.vst3 to $VST3_DEST..."
        cp -R "$VST3_SOURCE" "$VST3_DEST" 2>/dev/null
        if [[ ! -d "$VST3_DEST" ]]; then
            info "Requesting elevated privileges..."
            sudo cp -R "$VST3_SOURCE" "$VST3_DEST" 2>/dev/null
        fi
        if [[ -d "$VST3_DEST" ]]; then
            # Remove macOS quarantine
            [[ "$OS" == "Darwin" ]] && xattr -dr com.apple.quarantine "$VST3_DEST" 2>/dev/null || true
            ok "VST3 plugin installed to: $VST3_DEST"
            echo "       Rescan plugins in your DAW — look for 'text2midi' under Instruments."
        else
            warn "Could not install VST3 plugin."
            echo "         Try: bash installer/install_vst.sh"
        fi
    fi
fi
echo ""

# ── Final summary ────────────────────────────────────────────────
echo ""
printf "${BOLD}${CYAN}"
echo "  ================================================================"
echo ""
echo "    Installation complete!"
echo ""
echo "    To start making music:"
echo "      ./text2midi                     (from project folder)"
if [[ "$OS" == "Darwin" ]]; then
echo "      Double-click text2midi.command  (in Finder)"
fi
echo "      uv run python main_tui.py      (alternative)"
echo ""
echo "    To set up or change your AI provider later:"
echo "      uv run python main.py --setup"
echo "      Or press Ctrl+S inside the app"
echo ""
echo "    VST3 Plugin (for DAW users):"
echo "      - If installed, rescan plugins in your DAW"
echo "      - To install later:  bash installer/install_vst.sh"
echo ""
echo "  ================================================================"
printf "${NC}\n"
