# 🚀 MidiGen v2.0 - Poetry Setup & Quick Start

## ⚡ Ultra-Quick Start (3 steps)

```bash
# 1. Install Poetry (if not already installed)
pip install poetry

# 2. Install dependencies
poetry install

# 3. Run the app
poetry run python app_langgraph.py
```

Open browser: **http://localhost:7860** → Start creating music! 🎵

---

## 📦 Poetry Installation

### macOS & Linux
```bash
curl -sSL https://install.python-poetry.org | python3 -
export PATH="$HOME/.local/bin:$PATH"
```

### Windows
```bash
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

### Verify
```bash
poetry --version
```

---

## 🛠️ Setup MidiGen

### Step 1: Clone/Enter Project
```bash
cd spec-kit
```

### Step 2: Install Dependencies
```bash
# Full installation (includes dev tools)
poetry install

# OR just production
poetry install --no-dev
```

### Step 3: Activate Environment
```bash
poetry shell
```

### Step 4: Run the App
```bash
python app_langgraph.py
```

Or without activating shell:
```bash
poetry run python app_langgraph.py
```

---

## 📚 Using Make Commands (Optional)

If you have `make` installed, use shortcuts:

```bash
make dev       # Install with dev tools
make run       # Run the app
make shell     # Activate virtual environment
make test      # Run tests
make format    # Format code with black
make lint      # Lint with ruff
make clean     # Clean cache files
make update    # Update dependencies

# Quick versions
make i         # = make install
make r         # = make run
make s         # = make shell
make t         # = make test
```

---

## 📂 Project Structure

```
spec-kit/
├── pyproject.toml          ← Poetry config (main)
├── poetry.lock             ← Lock file (auto-generated)
├── Makefile                ← Convenience commands
├── .tool-versions          ← Python version (3.10)
│
├── app_langgraph.py        ← Main app
├── src/agents/             ← Agent system
│   ├── state.py
│   ├── nodes.py
│   ├── graph.py
│   └── __init__.py
│
├── outputs/                ← Generated MIDI files
└── docs/                   ← Documentation
```

---

## 🎵 Creating Music

Once the app is running:

1. **Open:** http://localhost:7860
2. **Type prompt:**
   ```
   "Create a peaceful ambient soundscape"
   "Epic cinematic orchestra with 6 tracks"
   "Funky beat at 120 BPM"
   ```
3. **Watch agents work** in console
4. **Download MIDI** from UI

---

## 🔧 Common Tasks

### Add a Dependency
```bash
poetry add package-name
```

### Add Dev Dependency
```bash
poetry add --group dev package-name
```

### Update All Dependencies
```bash
poetry update
```

### Export to requirements.txt
```bash
poetry export -f requirements.txt --output requirements.txt
```

### View Installed Packages
```bash
poetry show
```

### Check for Outdated Packages
```bash
poetry show --outdated
```

### Virtual Environment Info
```bash
poetry env info
```

---

## 🐍 Python Version Management

### View Current Environment
```bash
poetry env info
```

### Switch Python Version
```bash
poetry env use python3.11
poetry install
```

### List All Environments
```bash
poetry env list
```

---

## ✅ Troubleshooting

### Error: `command not found: poetry`

**Solution:**
```bash
# Add to PATH (macOS/Linux)
export PATH="$HOME/.local/bin:$PATH"

# Add to ~/.bashrc, ~/.zshrc, or ~/.profile permanently
```

### Error: Dependency conflict

**Solution:**
```bash
poetry update
poetry install
```

### Error: Wrong Python version

**Solution:**
```bash
poetry env use python3.10
poetry install
```

### Not finding gradio or other packages

**Solution:**
```bash
# Clear and reinstall
rm poetry.lock
poetry install
```

---

## 🎯 Development Workflow

### Setup for Development
```bash
cd spec-kit
poetry install              # Install everything
poetry shell                # Activate
python app_langgraph.py     # Run
```

### Format & Lint Your Code
```bash
poetry run black .          # Format
poetry run ruff check .     # Lint
poetry run mypy src/        # Type check
```

### Run Tests
```bash
poetry run pytest -v
```

### Clean Cache Files
```bash
make clean
# or
poetry run black --check .
```

---

## 📊 pyproject.toml Overview

```toml
[tool.poetry]
name = "midigen"
version = "2.0.0"
description = "AI music generation with LangGraph"

[tool.poetry.dependencies]
python = "^3.8"
gradio = "^4.0.0"
langgraph = "^0.1.0"
langchain = "^0.1.0"
# ... more dependencies

[tool.poetry.group.dev.dependencies]
pytest = "^7.4.0"
black = "^23.0.0"
ruff = "^0.1.0"
# ... more dev tools
```

---

## 🚀 Docker Support

If using Docker:

**Dockerfile:**
```dockerfile
FROM python:3.10-slim
WORKDIR /app

RUN pip install poetry
COPY pyproject.toml poetry.lock* ./
RUN poetry install --no-dev --no-directory

COPY . .
CMD ["poetry", "run", "python", "app_langgraph.py"]
```

**Build & Run:**
```bash
docker build -t midigen .
docker run -p 7860:7860 midigen
```

---

## 📖 More Information

- **Poetry Docs:** https://python-poetry.org/docs/
- **pyproject.toml Reference:** https://python-poetry.org/docs/pyproject/
- **Advanced Guide:** See [POETRY_MIGRATION.md](./POETRY_MIGRATION.md)

---

## 💡 Quick Tips

✅ **Use `poetry shell`** for interactive work  
✅ **Use `poetry run`** for scripts  
✅ **Commit poetry.lock** to git  
✅ **Don't commit venv** (Poetry manages it)  
✅ **Use `make` shortcuts** for common tasks  
✅ **Keep pyproject.toml** in version control  

---

## ✨ You're All Set!

```bash
poetry install
poetry run python app_langgraph.py
```

Your MidiGen instance is ready! 🎵

**Next Step:** Open http://localhost:7860 and create amazing music!
