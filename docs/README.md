# Documentation

Complete documentation for Spec-Kit and MidiGen.

## 📚 Documentation Index

### MidiGen (AI Music Generator)

- **[Quick Start](QUICKSTART_MIDIGEN.md)** - Get started in 5 minutes
- **[Architecture](ARCHITECTURE.md)** - System design and components
- **[API Reference](API.md)** - Complete API documentation

### Spec-Kit (Spec-Driven Development)

- **[Quick Start](QUICKSTART.md)** - Spec-Kit setup and workflow
- **[Installation](installation.md)** - Detailed installation guide
- **[Local Development](local-development.md)** - Development workflow
- **[Upgrade Guide](upgrade.md)** - Version upgrades

## 🚀 Quick Links

**New to MidiGen?** Start with [QUICKSTART_MIDIGEN.md](QUICKSTART_MIDIGEN.md)

**Building systems with specs?** Start with [QUICKSTART.md](QUICKSTART.md)

## 📂 File Structure

```
docs/
├── README.md                    # This file (navigation hub)
├── ARCHITECTURE.md              # MidiGen system design
├── API.md                       # API reference
├── QUICKSTART.md                # Spec-Kit quick start
├── QUICKSTART_MIDIGEN.md        # MidiGen quick start
├── installation.md              # Installation guide
├── local-development.md         # Development setup
├── upgrade.md                   # Version upgrades
├── archive/                     # Old/legacy documentation
├── docfx.json                   # DocFX configuration
├── index.md                     # Homepage
├── toc.yml                      # Table of contents
└── ...
```

## 🛠️ Building Documentation (Spec-Kit)

To build the full documentation locally:

```bash
# Install DocFX
dotnet tool install -g docfx

# Build and serve
cd docs
docfx docfx.json --serve
```

Open `http://localhost:8080` to view the documentation.

## 📖 What's Included

### MidiGen
- Complete API reference
- Architecture diagrams and explanations
- Configuration guide
- Troubleshooting
- Code examples
- Performance guidelines

### Spec-Kit
- Installation instructions
- Development workflow
- Specification format guide
- Agent integration
- CLI reference
- Examples and templates

## 🔍 Search

Use the search function in the built documentation to find specific topics.

## 💡 Tips

- **Just starting?** See [QUICKSTART_MIDIGEN.md](QUICKSTART_MIDIGEN.md) for MidiGen or [QUICKSTART.md](QUICKSTART.md) for Spec-Kit
- **Need architecture details?** Check [ARCHITECTURE.md](ARCHITECTURE.md)
- **Looking for API docs?** See [API.md](API.md)
- **Having issues?** Check TROUBLESHOOTING sections in quick start guides

---

Last Updated: 2024
Part of [Spec-Kit](https://github.com/github/spec-kit)
- `_site/` - Generated documentation output (ignored by git)

## Deployment

Documentation is automatically built and deployed to GitHub Pages when changes are pushed to the `main` branch. The workflow is defined in `.github/workflows/docs.yml`.
