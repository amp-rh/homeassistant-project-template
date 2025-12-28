# AGENTS.md

This file is the authoritative index for AI agents working on this Home Assistant add-on project. Read this before making any changes.

## Project Overview

This is a Python project template for developing Home Assistant add-ons. It provides:
- Complete add-on structure with configuration files
- Modern Python tooling (uv, pytest, ruff)
- Local development workflow without requiring full HA installation
- Comprehensive documentation system for AI agents
- Production-ready containerization with Podman

## Project Structure

```
project-root/
├── AGENTS.md               # This file (root index)
├── addon/                  # Home Assistant add-on files
│   ├── config.yaml        # Add-on configuration
│   ├── build.yaml         # Build configuration
│   ├── Dockerfile         # Container definition
│   ├── DOCS.md            # User documentation
│   └── rootfs/            # Container filesystem overlay
│
├── .agents/                # Agent documentation
│   ├── commands/           # Slash command definitions
│   ├── docs/               # Granular, linked docs
│   │   ├── tooling/        # uv, pytest, ruff, bashio, podman
│   │   ├── patterns/       # addon-structure, options-handling, supervisor-api
│   │   ├── conventions/    # Naming, imports, structure
│   │   ├── workflows/      # Local development, publishing, testing
│   │   └── architecture/   # Design decisions
│   │       └── homeassistant/  # HA-specific architecture
│   ├── learnings/          # Discovered patterns and insights
│   ├── scratch/            # Agent working space
│   └── templates/          # Reusable templates
│
├── src/                    # Python source code - see @src/AGENTS.md
│   └── my_addon/
│       ├── __main__.py     # Entry point
│       ├── config.py       # Configuration handling
│       ├── supervisor.py   # Supervisor API client
│       └── server.py       # Application logic
│
├── tests/                  # Tests - see @tests/AGENTS.md
├── scripts/                # Development scripts
└── pyproject.toml          # Python project configuration
```

## Core Rules

- MUST read the relevant AGENTS.md before modifying files in any directory
- MUST run `uv sync --extra dev` after modifying `pyproject.toml`
- MUST run `pytest` before committing changes
- MUST test locally with `make dev` before building container
- MUST NOT add dependencies without documenting in relevant docs
- MUST update documentation when patterns are learned or decisions made

## Documentation Index

### Tooling (@.agents/docs/tooling/)

- `uv.md` - Package management with uv
- `pytest.md` - Testing with pytest
- `ruff.md` - Linting and formatting
- `bashio.md` - Home Assistant bash library
- `podman.md` - Container builds for HA add-ons

### Patterns (@.agents/docs/patterns/)

- `addon-structure.md` - Standard HA add-on file organization
- `options-handling.md` - Working with config.yaml and options.json
- `logging.md` - Structured logging best practices
- `supervisor-api.md` - Communicating with HA Supervisor
- `error-handling.md` - Graceful error handling

### Conventions (@.agents/docs/conventions/)

- `coding-style.md` - Coding style (clean, OOP, TDD)
- `naming.md` - Naming conventions
- `imports.md` - Import organization
- `project-structure.md` - Project layout

### Workflows (@.agents/docs/workflows/)

- `local-development.md` - Rapid iteration without full HA ⭐ START HERE
- `testing.md` - Testing strategy
- `publishing.md` - Publishing add-ons to repositories
- `pr-process.md` - Pull request workflow
- `contributing.md` - Contributing to this template

### Architecture (@.agents/docs/architecture/)

#### Home Assistant Specific (@.agents/docs/architecture/homeassistant/)

- `addon-communication.md` - Inter-add-on communication
- `ingress.md` - Serving web UIs via Ingress
- `authentication.md` - Authentication and long-lived tokens
- `discovery.md` - Service discovery mechanisms
- `storage.md` - Persistent storage patterns

#### General Architecture

- `containerization.md` - Container design principles
- `configuration.md` - Configuration management
- `security.md` - Security best practices
- `decisions.md` - Architecture Decision Records

## Commands

Slash commands are defined in `.agents/commands/`. When a `/command` is used, read the corresponding file.

- `/dev` - Start local development server
- `/build` - Build add-on container
- `/test-addon` - Test add-on with Home Assistant
- `/commit` - Stage and commit changes
- `/extract-learnings` - Document learnings
- `/extract-templates` - Extract reusable templates

See @.agents/commands/AGENTS.md for command format.

## Home Assistant Add-on Development

### Quick Start

```bash
# 1. Setup local development
make setup

# 2. Start development server (without HA)
make dev

# 3. Build add-on container
make build

# 4. Test with Home Assistant (requires HA installation)
make test-addon
```

### Development Workflow

1. **Local Development** (@.agents/docs/workflows/local-development.md)
   - Develop Python code without containers
   - Fast iteration cycle
   - Use `make dev` to run locally

2. **Container Testing**
   - Build with `make build`
   - Test container locally with `make run`

3. **HA Integration**
   - Deploy to HA with `make test-addon`
   - Test Supervisor API integration

### Key Concepts

**Add-on Structure** (@.agents/docs/patterns/addon-structure.md):
- `addon/config.yaml` - Add-on metadata and schema
- `addon/Dockerfile` - Multi-arch container build
- `addon/rootfs/` - Container filesystem overlay
- `src/my_addon/` - Python application code

**Configuration** (@.agents/docs/patterns/options-handling.md):
- Options defined in `addon/config.yaml`
- Runtime values in `/data/options.json`
- Read with bashio in scripts or Python in code

**Supervisor API** (@.agents/docs/patterns/supervisor-api.md):
- Access HA API with long-lived tokens
- Get add-on information
- Discover other services

**Ingress** (@.agents/docs/architecture/homeassistant/ingress.md):
- Serve web UIs through HA
- Automatic authentication
- No port exposure needed

## Before You Start

1. Read @.agents/docs/workflows/local-development.md for development workflow
2. Review @.agents/docs/patterns/addon-structure.md for file organization
3. Check @.agents/docs/tooling/ for tool-specific guidance

## When Working On

- **Add-on Configuration**: See @.agents/docs/patterns/options-handling.md
- **Supervisor Communication**: See @.agents/docs/patterns/supervisor-api.md
- **Web UI**: See @.agents/docs/architecture/homeassistant/ingress.md
- **Service Discovery**: See @.agents/docs/architecture/homeassistant/discovery.md
- **Persistent Data**: See @.agents/docs/architecture/homeassistant/storage.md
- **Testing**: See @.agents/docs/workflows/testing.md
- **Publishing**: See @.agents/docs/workflows/publishing.md

## Scratch Workspace

Use `.agents/scratch/` for working notes, decisions, and drafts. Templates are provided; working files are gitignored.

- @.agents/scratch/AGENTS.md - Workspace usage guide
- @.agents/scratch/decisions/_template.md - Decision-making template
- @.agents/scratch/notes/_template.md - Notes template
- @.agents/scratch/context/_template.md - Session context template
- @.agents/scratch/research/_template.md - Research template

## Directory Indexes

- @.agents/AGENTS.md - Agent resources
- @src/AGENTS.md - Source code guidance
- @tests/AGENTS.md - Test guidance

## Project Philosophy

1. **Python-First**: Leverage modern Python tooling (uv, ruff, pytest)
2. **Rapid Iteration**: Local development without HA Supervisor
3. **Production-Ready**: Matches HA Supervisor requirements exactly
4. **AI-Friendly**: Comprehensive documentation for AI agents
5. **Podman-Based**: Rootless containers, multi-arch builds

## Common Tasks

```bash
make dev           # Start local development server
make test          # Run test suite
make lint          # Run linting
make build         # Build add-on container
make run           # Run add-on container locally
make test-addon    # Test with Home Assistant
```
