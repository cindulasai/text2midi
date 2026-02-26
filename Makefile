.PHONY: help install dev test lint format type-check clean run shell update

help:
	@echo "🎵 MidiGen v2.0 - Poetry Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make install      Install dependencies"
	@echo "  make dev          Install with dev tools"
	@echo ""
	@echo "Running:"
	@echo "  make run          Run the app"
	@echo "  make shell        Activate virtual environment"
	@echo ""
	@echo "Development:"
	@echo "  make test         Run tests"
	@echo "  make lint         Run linter (ruff)"
	@echo "  make format       Format code (black)"
	@echo "  make type-check   Check types (mypy)"
	@echo ""
	@echo "Maintenance:"
	@echo "  make update       Update dependencies"
	@echo "  make clean        Remove cache files"
	@echo ""

install:
	@echo "📦 Installing dependencies..."
	poetry install --no-dev

dev:
	@echo "🛠️  Installing with dev dependencies..."
	poetry install

run:
	@echo "🚀 Running MidiGen..."
	poetry run python app_langgraph.py

shell:
	@echo "🐚 Activating virtual environment..."
	poetry shell

test:
	@echo "🧪 Running tests..."
	poetry run pytest -v

lint:
	@echo "🔍 Linting code..."
	poetry run ruff check .

format:
	@echo "✨ Formatting code..."
	poetry run black .

type-check:
	@echo "📋 Type checking..."
	poetry run mypy src/

clean:
	@echo "🧹 Cleaning up..."
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .mypy_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .ruff_cache -exec rm -rf {} + 2>/dev/null || true
	rm -rf .venv/ build/ dist/ *.egg-info 2>/dev/null || true
	@echo "✅ Clean complete"

update:
	@echo "🔄 Updating dependencies..."
	poetry update

add-dep:
	@echo "📥 Add dependency (usage: make add-dep PKG=package-name)"
	poetry add $(PKG)

add-dev-dep:
	@echo "📥 Add dev dependency (usage: make add-dev-dep PKG=package-name)"
	poetry add --group dev $(PKG)

# Quick shortcuts
i: install
dev-setup: dev
t: test
f: format
l: lint
c: clean
r: run
s: shell
