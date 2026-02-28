#!/usr/bin/env bash
# ================================================================
#  text2midi — VST3 Plugin Standalone Installer
#  macOS / Linux
#
#  Installs just the VST3 plugin and backend server so you
#  can use text2midi directly inside your DAW.
#
#  After running this script, rescan plugins in your DAW
#  and look for "text2midi" under Instruments.
# ================================================================

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

# ── Colours ──────────────────────────────────────────────────────
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

OS="$(uname -s)"

echo ""
printf "${BOLD}${CYAN}"
echo "  ================================================================"
echo "    text2midi — VST3 Plugin Installer"
echo "  ================================================================"
printf "${NC}\n"

if [[ "$OS" == "Darwin" ]]; then
    VST3_SYSTEM_DIR="$HOME/Library/Audio/Plug-Ins/VST3"
    echo "  This will install:"
    echo "    1. text2midi.vst3  →  $VST3_SYSTEM_DIR/"
    echo "    2. Backend server  →  /usr/local/bin/ (optional)"
else
    VST3_SYSTEM_DIR="$HOME/.vst3"
    echo "  This will install:"
    echo "    1. text2midi.vst3  →  $VST3_SYSTEM_DIR/"
    echo "    2. Backend server  →  ~/.local/bin/ (optional)"
fi

echo ""
echo "  After installation, rescan plugins in your DAW."
echo "  The plugin appears under 'Instruments' as 'text2midi'."
echo ""

if ! prompt_yn "Continue?"; then
    echo "  No problem — run this script whenever you are ready."
    exit 0
fi
echo ""

# ================================================================
#  STEP 1 / 3  —  Locate VST3 Build
# ================================================================
echo "  ──────────────────────────────────────────────────────────────"
echo "   Step 1 of 3 : Locating VST3 Plugin"
echo "  ──────────────────────────────────────────────────────────────"

VST3_SOURCE=""

# Check Release build
if [[ -d "$PROJECT_DIR/vst-plugin/build/text2midi_artefacts/Release/VST3/text2midi.vst3" ]]; then
    VST3_SOURCE="$PROJECT_DIR/vst-plugin/build/text2midi_artefacts/Release/VST3/text2midi.vst3"
    ok "Found Release build of text2midi.vst3"
fi

# Check Debug build
if [[ -z "$VST3_SOURCE" && -d "$PROJECT_DIR/vst-plugin/build/text2midi_artefacts/Debug/VST3/text2midi.vst3" ]]; then
    VST3_SOURCE="$PROJECT_DIR/vst-plugin/build/text2midi_artefacts/Debug/VST3/text2midi.vst3"
    ok "Found Debug build of text2midi.vst3"
fi

if [[ -z "$VST3_SOURCE" ]]; then
    err "VST3 plugin build not found."
    echo ""
    echo "         The plugin must be compiled from C++ source first."
    echo "         Follow these steps:"
    echo ""
    echo "           cd \"$PROJECT_DIR/vst-plugin\""
    if [[ "$OS" == "Darwin" ]]; then
        echo "           cmake -B build -G Xcode"
        echo "           cmake --build build --config Release"
    else
        echo "           cmake -B build"
        echo "           cmake --build build --config Release"
    fi
    echo ""
    echo "         Then run this script again."
    echo "         For full instructions see: vst-plugin/BUILDING.md"
    exit 1
fi
echo ""

# ================================================================
#  STEP 2 / 3  —  Install VST3 Plugin
# ================================================================
echo "  ──────────────────────────────────────────────────────────────"
echo "   Step 2 of 3 : Installing VST3 Plugin"
echo "  ──────────────────────────────────────────────────────────────"

VST3_DEST="$VST3_SYSTEM_DIR/text2midi.vst3"
info "Destination: $VST3_DEST"

# Create VST3 directory if it doesn't exist
mkdir -p "$VST3_SYSTEM_DIR" 2>/dev/null

# Remove old installation if present
if [[ -d "$VST3_DEST" ]]; then
    info "Removing previous installation..."
    rm -rf "$VST3_DEST" 2>/dev/null
    if [[ -d "$VST3_DEST" ]]; then
        sudo rm -rf "$VST3_DEST" 2>/dev/null
    fi
fi

# Copy VST3 bundle
info "Copying text2midi.vst3..."
cp -R "$VST3_SOURCE" "$VST3_DEST" 2>/dev/null

if [[ -d "$VST3_DEST" ]]; then
    ok "VST3 plugin installed to: $VST3_DEST"
else
    # Try with sudo
    info "Requesting elevated privileges..."
    sudo cp -R "$VST3_SOURCE" "$VST3_DEST" 2>/dev/null

    if [[ -d "$VST3_DEST" ]]; then
        ok "VST3 plugin installed to: $VST3_DEST"
    else
        err "Could not install VST3 plugin."
        echo "         Try running this script with sudo, or copy manually:"
        echo "         From: $VST3_SOURCE"
        echo "         To:   $VST3_DEST"
        exit 1
    fi
fi

# On macOS, remove quarantine attribute so Gatekeeper doesn't block it
if [[ "$OS" == "Darwin" ]]; then
    xattr -dr com.apple.quarantine "$VST3_DEST" 2>/dev/null || true
    ok "Removed macOS quarantine attribute"
fi
echo ""

# ================================================================
#  STEP 3 / 3  —  Backend Server  (optional)
# ================================================================
echo "  ──────────────────────────────────────────────────────────────"
echo "   Step 3 of 3 : Backend Server  (optional)"
echo "  ──────────────────────────────────────────────────────────────"
echo ""
echo "  The VST3 plugin needs a backend server for AI generation."
echo "  The server runs in the background and the plugin auto-launches it."
echo ""

BACKEND_SOURCE="$PROJECT_DIR/vst-plugin/python-backend/dist/text2midi-backend"

if [[ "$OS" == "Darwin" ]]; then
    BACKEND_EXE="$BACKEND_SOURCE/text2midi-backend"
    BACKEND_DEST_DIR="/usr/local/lib/text2midi-backend"
    BACKEND_DEST_BIN="/usr/local/bin/text2midi-backend"
else
    BACKEND_EXE="$BACKEND_SOURCE/text2midi-backend"
    BACKEND_DEST_DIR="$HOME/.local/lib/text2midi-backend"
    BACKEND_DEST_BIN="$HOME/.local/bin/text2midi-backend"
fi

if [[ ! -f "$BACKEND_EXE" ]]; then
    warn "Backend server executable not found."
    echo ""
    echo "         You can build it with:"
    echo "           cd vst-plugin/python-backend"
    echo "           python build_backend.py"
    echo ""
    echo "         Alternatively, start the server manually:"
    echo "           cd vst-plugin/python-backend"
    echo "           python server.py"
    echo ""
else
    if prompt_yn "Install backend server?"; then
        echo ""

        if [[ "$OS" == "Darwin" ]]; then
            # Copy entire backend directory (PyInstaller --onedir output)
            info "Installing backend server to $BACKEND_DEST_DIR..."
            sudo mkdir -p "$BACKEND_DEST_DIR" 2>/dev/null
            sudo cp -R "$BACKEND_SOURCE/"* "$BACKEND_DEST_DIR/" 2>/dev/null
            sudo chmod +x "$BACKEND_DEST_DIR/text2midi-backend" 2>/dev/null
            # Create a symlink in bin so PATH picks it up
            sudo ln -sf "$BACKEND_DEST_DIR/text2midi-backend" "$BACKEND_DEST_BIN" 2>/dev/null
        else
            mkdir -p "$BACKEND_DEST_DIR" 2>/dev/null
            mkdir -p "$(dirname "$BACKEND_DEST_BIN")" 2>/dev/null
            info "Installing backend server to $BACKEND_DEST_DIR..."
            cp -R "$BACKEND_SOURCE/"* "$BACKEND_DEST_DIR/" 2>/dev/null
            chmod +x "$BACKEND_DEST_DIR/text2midi-backend" 2>/dev/null
            # Create a symlink in bin so PATH picks it up
            ln -sf "$BACKEND_DEST_DIR/text2midi-backend" "$BACKEND_DEST_BIN" 2>/dev/null
        fi

        if [[ -f "$BACKEND_DEST_DIR/text2midi-backend" ]]; then
            ok "Backend server installed to: $BACKEND_DEST_DIR"

            # Offer to create a systemd service (Linux) or launchd plist (macOS)
            if [[ "$OS" == "Darwin" ]]; then
                if prompt_yn "Auto-start server on login?" "N"; then
                    PLIST_DIR="$HOME/Library/LaunchAgents"
                    mkdir -p "$PLIST_DIR" 2>/dev/null
                    cat > "$PLIST_DIR/com.text2midi.server.plist" << PLIST_EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.text2midi.server</string>
    <key>ProgramArguments</key>
    <array>
        <string>$BACKEND_DEST_DIR/text2midi-backend</string>
    </array>
    <key>WorkingDirectory</key>
    <string>$BACKEND_DEST_DIR</string>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <false/>
</dict>
</plist>
PLIST_EOF
                    ok "Server will auto-start on login."
                    echo "         To remove: launchctl unload '$PLIST_DIR/com.text2midi.server.plist'"
                fi
            else
                if prompt_yn "Auto-start server on login?" "N"; then
                    AUTOSTART_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/autostart"
                    mkdir -p "$AUTOSTART_DIR" 2>/dev/null
                    cat > "$AUTOSTART_DIR/text2midi-server.desktop" << DESKTOP_EOF
[Desktop Entry]
Type=Application
Name=text2midi Server
Exec=$BACKEND_DEST_DIR/text2midi-backend
Hidden=false
NoDisplay=true
X-GNOME-Autostart-enabled=true
Comment=text2midi backend server for VST3 plugin
DESKTOP_EOF
                    ok "Server will auto-start on login."
                    echo "         To remove: delete $AUTOSTART_DIR/text2midi-server.desktop"
                fi
            fi
        else
            warn "Could not install backend server."
            echo "         You can run it directly: python vst-plugin/python-backend/server.py"
        fi
    else
        echo ""
        ok "Skipped backend server installation."
        echo "       You can start it manually: python vst-plugin/python-backend/server.py"
    fi
fi
echo ""

# ================================================================
#  Done!
# ================================================================
echo ""
printf "${BOLD}${CYAN}"
echo "  ================================================================"
echo ""
echo "    VST3 Plugin Installation Complete!"
echo ""
echo "    Next steps:"
echo "      1. Open your DAW (Ableton Live, FL Studio, Bitwig, etc.)"
echo "      2. Rescan / refresh your VST3 plugins"
echo "      3. Add 'text2midi' as an instrument on a MIDI track"
echo "      4. Type a prompt and click Generate!"
echo ""
echo "    The plugin appears under:"
echo "      Instruments > text2midi"
echo ""
if [[ "$OS" == "Darwin" ]]; then
echo "    VST3 location: $VST3_SYSTEM_DIR/text2midi.vst3"
else
echo "    VST3 location: $VST3_SYSTEM_DIR/text2midi.vst3"
fi
echo ""
echo "    Troubleshooting:"
echo "      - Plugin not visible?  Rescan plugins in your DAW"
echo "      - 'Server offline'?    Start the backend server manually"
echo "      - See: vst-plugin/README.md for full docs"
echo ""
echo "  ================================================================"
printf "${NC}\n"
