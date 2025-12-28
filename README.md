# Home Assistant Add-on Python Template

A comprehensive Python project template for developing Home Assistant add-ons with modern tooling, local development workflow, and AI-friendly documentation.

## Features

- **Complete Add-on Structure**: Ready-to-use Home Assistant add-on configuration
- **AGENTS.md System**: Hierarchical documentation indexes for AI agent guidance
- **Modern Python Tooling**: uv, pytest, ruff, mypy
- **Local Development**: Rapid iteration without full HA installation
- **Multi-Architecture**: Build for aarch64, amd64, armv7, armhf, i386
- **Podman-Based**: Rootless containers using HA base images
- **Production-Ready**: Matches Home Assistant Supervisor requirements

## Quick Start

```bash
# 1. Clone this template
git clone https://github.com/YOUR-USERNAME/homeassistant-addon-template.git my-addon
cd my-addon

# 2. Install dependencies
uv sync --extra dev

# 3. Setup local development
make setup

# 4. Start development server (runs without Home Assistant!)
make dev

# 5. Access your add-on at http://localhost:8000
```

## Make Targets

```bash
make help          # Show all targets
make setup         # Setup local development environment
make dev           # Start local development server
make test          # Run tests
make lint          # Run linting
make format        # Format code
make build         # Build add-on container
make run           # Run add-on container locally
make test-addon    # Test with Home Assistant
make clean         # Clean up build artifacts
```

## Documentation for AI Agents

This project uses AGENTS.md files as documentation indexes:

- **Getting Started**: [.agents/docs/workflows/local-development.md](.agents/docs/workflows/local-development.md)
- **Add-on Structure**: [.agents/docs/patterns/addon-structure.md](.agents/docs/patterns/addon-structure.md)
- **Supervisor API**: [.agents/docs/patterns/supervisor-api.md](.agents/docs/patterns/supervisor-api.md)
- **Publishing**: [.agents/docs/workflows/publishing.md](.agents/docs/workflows/publishing.md)

See [AGENTS.md](AGENTS.md) for the complete index.

## Using This Template

1. Rename `src/my_addon` to your add-on name
2. Update `addon/config.yaml` with your add-on details
3. Update `pyproject.toml` with your project name
4. Implement your add-on logic in `src/`
5. Test locally with `make dev`
6. Build container with `make build`
7. Publish following `.agents/docs/workflows/publishing.md`

## License

Apache License 2.0 - see [LICENSE](LICENSE)
