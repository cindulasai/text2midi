# 📦 Poetry Migration Guide - MidiGen v2.0

## Why Poetry?

**Poetry** is the modern Python dependency management solution offering:

✅ **Lock files** - Reproducible installations across machines  
✅ **Dependency resolution** - Smart conflict resolution  
✅ **Virtual environment** - Integrated venv management  
✅ **Simple commands** - Cleaner than pip  
✅ **Publishing ready** - Built for distribution  
✅ **Widely adopted** - Industry standard  

---

## Installation

### Install Poetry (One-time setup)

```bash
# macOS & Linux
curl -sSL https://install.python-poetry.org | python3 -

# Windows (PowerShell)
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -

# Or use pip
pip install poetry
```

Add Poetry to PATH:
```bash
# macOS/Linux - Add to ~/.bashrc, ~/.zshrc, or ~/.profile
export PATH="$HOME/.local/bin:$PATH"

# Windows - Poetry installer does this automatically
```

Verify installation:
```bash
poetry --version
```

---

## Quick Start

### Option 1: Use New pyproject.toml

```bash
cd spec-kit

# Copy the new Poetry config
cp pyproject_midigen.toml pyproject.toml

# Install dependencies
poetry install

# Activate virtual environment
poetry shell

# Run the app
python app_langgraph.py
```

### Option 2: Initialize from Existing requirements.txt

```bash
# From the project root
poetry init --name midigen --dependency gradio --dependency langgraph

# Or if you have pyproject_midigen.toml ready
poetry install
```

---

## Common Commands

### Installation & Setup
```bash
# Install all dependencies (creates virtual env)
poetry install

# Install only production dependencies
poetry install --no-dev

# Add a new dependency
poetry add gradio@^4.0.0

# Add a dev dependency
poetry add --group dev pytest@^7.4.0

# Update dependencies
poetry update

# Check for security issues
poetry show --outdated
```

### Running Code
```bash
# Activate the virtual environment
poetry shell

# Run directly without activating
poetry run python app_langgraph.py

# Run scripts defined in pyproject.toml
poetry run pytest
```

### Lock Files & Reproducibility
```bash
# Create poetry.lock (automatic, but can force)
poetry lock

# Verify against lock file (recommended for CI/CD)
poetry install --no-directory

# Export to requirements.txt (for Docker, etc.)
poetry export -f requirements.txt --output requirements.txt
```

---

## File Structure

```
spec-kit/
├── pyproject.toml              ← Main Poetry config (use this)
├── poetry.lock                 ← Auto-generated (commit to git)
├── pyproject_midigen.toml      ← Keep as reference
├── requirements.txt            ← Old style (deprecated)
│
├── app_langgraph.py
├── src/agents/
│   ├── state.py
│   ├── nodes.py
│   ├── graph.py
│   └── __init__.py
│
└── tests/                      ← Add your tests here
```

---

## Virtual Environment Management

### View Environment Info
```bash
poetry env info

# Shows:
# Path to Python
# Python version
# Virtual env location
```

### List All Virtual Environments
```bash
poetry env list
```

### Switch Python Version
```bash
poetry env use python3.11

# Or specify full path
poetry env use /usr/bin/python3.11
```

### Remove Virtual Environment
```bash
poetry env remove python3.11
```

---

## Development Workflow

### Setting Up for Development

```bash
# Clone/enter project
cd spec-kit

# Install with dev dependencies
poetry install

# Activate shell
poetry shell

# Now you can:
python app_langgraph.py        # Run the app
pytest                         # Run tests
black .                        # Format code
ruff check .                   # Lint code
mypy src/                      # Type check
```

### Creating Your Own Virtual Environment

```bash
# Use specific Python version
poetry env use python3.10

# Install dependencies
poetry install

# List environments
poetry env list

# Show current environment
poetry env info
```

---

## Adding New Dependencies

### Add to Production
```bash
# Specific version
poetry add langchain@^0.1.0

# Latest compatible
poetry add langchain

# Exact version
poetry add langchain==0.1.5

# Specific range
poetry add "langchain>=0.1.0,<0.2.0"
```

### Add to Development Only
```bash
poetry add --group dev pytest
poetry add --group dev black
poetry add --group dev mypy
```

### Add to Documentation
```bash
poetry add --group docs sphinx
```

---

## Deployment

### Docker Support

**Dockerfile** example:
```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy Poetry files
COPY pyproject.toml poetry.lock* ./

# Install dependencies (no dev)
RUN poetry install --no-dev --no-directory

# Copy code
COPY . .

# Run app
CMD ["poetry", "run", "python", "app_langgraph.py"]
```

### CI/CD Integration

**GitHub Actions** example:
```yaml
- name: Install dependencies
  run: |
    poetry install --no-dev
    
- name: Run tests
  run: poetry run pytest
```

### Export to requirements.txt

For systems that don't support Poetry:
```bash
# Export all dependencies
poetry export -f requirements.txt --output requirements.txt

# Export without dev dependencies
poetry export -f requirements.txt --output requirements.txt --without dev
```

---

## Migration Path

### From requirements.txt to Poetry (2 Steps)

1. **Create pyproject.toml** (already done, see pyproject_midigen.toml)
   
2. **Use it:**
   ```bash
   cp pyproject_midigen.toml pyproject.toml
   poetry install
   ```

3. **Delete old files** (when ready):
   ```bash
   rm requirements.txt
   ```

4. **Commit to git:**
   ```bash
   git add pyproject.toml poetry.lock
   git commit -m "Migrate to Poetry for dependency management"
   ```

---

## Troubleshooting

### Issue: `command not found: poetry`

**Solution:** Add to PATH
```bash
# macOS/Linux
export PATH="$HOME/.local/bin:$PATH"

# Windows: Reinstall Poetry using installer
```

### Issue: Wrong Python version

**Solution:** Switch versions
```bash
poetry env use python3.10
poetry install
```

### Issue: Virtual environment not activating

**Solution:** Manual activation
```bash
# Get venv path
poetry env info --path

# macOS/Linux
source /path/to/venv/bin/activate

# Windows
/path/to/venv/Scripts/activate.bat
```

### Issue: Dependency conflicts

**Solution:** Update and resolve
```bash
poetry update --dry-run    # See what would change
poetry update              # Apply updates
```

### Issue: poetry.lock out of sync

**Solution:** Regenerate
```bash
poetry lock --no-update
poetry install
```

---

## Best Practices

✅ **Always commit poetry.lock** to version control  
✅ **Use exact versions for critical packages** (e.g., `python = "^3.8"`)  
✅ **Separate dev and prod dependencies** (use groups)  
✅ **Update regularly** (`poetry update`)  
✅ **Use poetry shell** for interactive work  
✅ **Use poetry run** for scripts  
✅ **Document Python version requirements**  

---

## Why Not Other Tools?

### vs. pip + requirements.txt
- ❌ No lock files
- ❌ No virtual env management
- ❌ Manual dependency resolution
- ✅ Poetry: All automatic

### vs. uv
- ❌ Newer, less mature
- ❌ Smaller ecosystem
- ✅ Poetry: Mature, stable, industry standard

### vs. conda
- ❌ Heavyweight
- ❌ Complex for Python projects
- ✅ Poetry: Lightweight, Python-focused

---

## Resources

- **Official Docs:** https://python-poetry.org/docs/
- **GitHub:** https://github.com/python-poetry/poetry
- **Community:** https://stackoverflow.com/questions/tagged/poetry

---

## Summary

### Before (pip)
```bash
pip install -r requirements.txt
python app_langgraph.py
```

### After (Poetry)
```bash
poetry install
poetry run python app_langgraph.py
# Or
poetry shell
python app_langgraph.py
```

**That's it!** Poetry handles virtual environments, lock files, and dependency resolution automatically. 🎉

---

**Status:** ✅ Poetry migration complete  
**Next Step:** Run `poetry install` to get started!
