# Security Guide

text2midi prioritizes security for API keys and sensitive data. This guide explains how your credentials are protected.

## 🔐 API Key Storage

### Secure Credential Manager (Default)

Your API keys are stored in your operating system's native secure credential storage — never as plain text:

- **Windows**: Windows Credential Manager
- **macOS**: Keychain
- **Linux**: Secret Service (GNOME Keyring, KDE Wallet, etc.)

These systems use encryption and are designed specifically for storing sensitive credentials.

### How It Works

1. When you first run text2midi, it launches an interactive setup wizard
2. You paste your API key
3. The key is validated with the provider
4. The key is **immediately encrypted and stored in OS Keyring**
5. Your `~/.config/text2midi/settings.json` file stores a sentinel value (`__KEYRING__`) instead of the real key
6. On the next run, text2midi retrieves the key from OS Keyring automatically

### Manual Configuration (Fallback)

If OS Keyring is unavailable, you can configure via `.env` file:

```bash
cp .env.example .env
# Add your API keys
```

> **Note**: On first run, text2midi will move keys from `.env` to OS Keyring automatically.

---

## 📝 Log Redaction

All logs automatically redact API key patterns. The logging system detects and masks:

- Groq keys: `gsk_*`
- Anthropic/OpenAI-style: `sk-*`
- Generic patterns: `key-*`
- OpenAI legacy: `AIza*`
- xAI/Grok: `xai-*`

Example:
```
# Raw key
API key: sk-ant-myrealsecretkey

# In logs
API key: ***REDACTED***
```

---

## 🔒 File Permissions

Configuration files are restricted to your user only:

**Linux/macOS:**
```bash
~/.config/text2midi/settings.json  # 600 (read/write user only)
```

**Windows:**
```
%APPDATA%\text2midi\settings.json  # NTFS ACL (user only)
```

`userdir` on macOS, `~/.config` on Linux, and `%APPDATA%` on Windows.

---

## 🛡️ What's NOT Stored

- **Private keys**: Never transmitted or stored
- **Provider tokens**: Only API keys; not refresh tokens or session IDs
- **User data**: Prompts and generated MIDI are stored locally in `outputs/` only
- **Usage logs**: Usage metrics are NOT sent to external servers

---

## 🚨 Best Practices

### 1. Use Separate API Keys Per Project

If working on multiple projects, keep separate API keys:

```bash
text2midi/         # Production key
text2midi-dev/     # Development key
```

### 2. Rotate Your Keys Regularly

If you suspect a key was exposed:

1. Revoke the key in your provider's dashboard
2. Generate a new key
3. Run text2midi setup wizard to update the key
4. Delete the old key

### 3. Don't Share Credentials

```bash
# ❌ NEVER do this
echo $GROQ_API_KEY                    # Exposes key
git add .env                          # Commits key
git push                              # Uploads to GitHub
screen-share with API key visible    # Screen recording with key

# ✅ DO this instead
# Use the setup wizard (Ctrl+S in TUI)
# Keys are already in OS Keyring
```

### 4. Keep Your .env.example Clean

The `.env.example` file is version-controlled. Keep it free of real keys:

```bash
# .env.example (SAFE - no real keys)
GROQ_API_KEY=your-groq-key-here
OPENAI_API_KEY=your-openai-key-here

# .env (LOCAL ONLY - never committed)
GROQ_API_KEY=gsk_xxxxxxxxxxxxx
OPENAI_API_KEY=sk-xxxxxxxxxxxxx
```

---

## 🔧 Troubleshooting Security Issues

### "KeyringError: No keyring available"

This means the system's credential manager isn't available. Solutions:

1. **Linux**: Install a keyring service
   ```bash
   # Ubuntu/Debian
   sudo apt install gnome-keyring

   # Fedora
   sudo dnf install gnome-keyring
   ```

2. **Fallback**: Use `.env` directly (keys won't be in OS Keyring, but will be stored with file permissions)

### "Permission denied" on settings.json

This usually means the file permissions got reset. Fix it:

**Linux/macOS:**
```bash
chmod 600 ~/.config/text2midi/settings.json
```

**Windows** (in PowerShell as Admin):
```powershell
icacls "$env:APPDATA\text2midi\settings.json" /reset /Q
```

### Lost Your API Key?

The setup wizard can't recover a lost key (it's encrypted in OS Keyring). You'll need to:

1. Log in to your provider's dashboard (Groq, OpenAI, etc.)
2. Revoke or regenerate your key
3. Run the setup wizard to add the new key

---

## 📋 Security Checklist

- [ ] Using the setup wizard (not manually editing `.env`)
- [ ] OS Keyring is available and working on your system
- [ ] Never commit `.env` with real keys to Git
- [ ] Regularly rotate API keys
- [ ] File permissions on `settings.json` are restricted (600 on Unix)
- [ ] No API keys visible in terminal history
- [ ] Keys are different for different projects/environments

---

## 🆘 Reporting Security Issues

If you discover a security vulnerability in text2midi:

1. **Do NOT** post it publicly or open a GitHub issue
2. Email security details to the maintainers privately

See [SECURITY.md](../SECURITY.md) in the root for the full security policy and reporting procedures.

---

## 📚 Related Documentation

- [GETTING_STARTED.md](GETTING_STARTED.md) — Setup wizard and key configuration
- [One-Touch Installer](../installer/README.md) — Automated setup with security
- [pyproject.toml](../pyproject.toml) — Dependencies including `keyring` library
