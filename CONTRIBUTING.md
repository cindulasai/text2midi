# Contributing to text2midi

Hi there! We're thrilled that you'd like to contribute to text2midi. Contributions to this project are [released](https://help.github.com/articles/github-terms-of-service/#6-contributions-under-repository-license) to the public under the [project's open source license](LICENSE).

Please note that this project is released with a [Contributor Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project you agree to abide by its terms.

## Prerequisites for running and testing code

These are one-time installations required to test your changes locally.

1. Install [Python 3.11+](https://www.python.org/downloads/)
2. Install [uv](https://docs.astral.sh/uv/) for package management
3. Install [Git](https://git-scm.com/downloads)
4. Obtain an LLM API key (Groq recommended - free): See [GETTING_STARTED.md](docs/GETTING_STARTED.md) for full list of 15+ supported providers

## Setup

```bash
git clone https://github.com/cindulasai/text2midi.git
cd text2midi
uv sync
cp .env.example .env
# Edit .env to add your API key
python main.py
```

## Testing changes

Before submitting a PR, make sure:

1. The app starts without errors: `python main.py`
2. Tests pass: `uv run pytest tests/`
3. Linting is clean: `uv run ruff check .`

## Development workflow

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-improvement`
3. Make your changes
4. Test thoroughly
5. Submit a Pull Request with a clear description of what you changed and why

## What we welcome

- Bug fixes with clear test cases
- New genre or instrument support
- Improved music theory logic
- Better LLM provider integrations
- Documentation improvements
- Performance improvements to the agent pipeline

## AI contributions

We welcome and encourage the use of AI tools to help improve text2midi. If you used AI assistance in your contribution, please mention it in your PR description.

## Questions?

Open a [GitHub issue](https://github.com/cindulasai/text2midi/issues/new) or start a [Discussion](https://github.com/cindulasai/text2midi/discussions).
