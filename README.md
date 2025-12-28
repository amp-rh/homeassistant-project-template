# Python Project Template

A Python project template with an AGENTS.md-based documentation system for AI agent guidance.

## Features

- **AGENTS.md System**: Hierarchical documentation indexes for AI agents
- **Modern Python Tooling**: uv, pytest, ruff
- **Container Support**: Rootless UBI9 S2I container builds
- **Agent Workspace**: Structured scratch space with templates

## Quick Start

```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and setup
git clone https://github.com/YOUR-USERNAME/python-project-template.git
cd python-project-template
uv sync --extra dev

# Run tests
make test

# Run linting
make lint
```

## Project Structure

```
├── AGENTS.md           # AI agent guidance (start here)
├── .agents/            # Agent-specific resources
│   ├── commands/       # Slash command definitions
│   ├── docs/           # Granular documentation
│   │   ├── tooling/    # uv, pytest, ruff
│   │   ├── patterns/   # Code patterns
│   │   ├── conventions/# Naming, imports
│   │   ├── workflows/  # PR, testing, releases, contributing
│   │   └── architecture/# Design decisions
│   ├── learnings/      # Discovered patterns
│   ├── scratch/        # Agent working space
│   └── templates/      # Reusable templates
├── src/my_package/     # Source code (rename to your package)
└── tests/              # Tests
```

## For AI Agents

This project uses AGENTS.md files as indexes. Before making changes:

1. Read the `AGENTS.md` in the directory you're working in
2. Follow linked documentation in `.agents/docs/`
3. Update docs when patterns are learned

See [AGENTS.md](AGENTS.md) for the root index.

## Using This Template

1. **Create from template** or clone this repository
2. **Rename package**: `mv src/my_package src/your_package`
3. **Update references**: Search for `my_package` and replace
4. **Update pyproject.toml**: Change name, description, authors

## Make Targets

```bash
make help          # Show all targets
make install       # Install dependencies
make dev           # Install with dev dependencies
make test          # Run tests
make lint          # Run linting
make format        # Format code
make build         # Build container image
make run           # Run container
```

## Contributing

See [.agents/docs/workflows/contributing.md](.agents/docs/workflows/contributing.md) for agent contribution guidelines.

## License

Apache License 2.0 - see [LICENSE](LICENSE)
