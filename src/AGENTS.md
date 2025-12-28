# src/ - Home Assistant Add-on Source Code

This directory contains the Python source code for the Home Assistant add-on.

## Structure

```
src/my_addon/
├── __init__.py       # Package initialization
├── __main__.py       # Entry point (runnable module)
├── config.py         # Configuration management
├── supervisor.py     # Supervisor API client
└── server.py         # Application logic (example: web server)
```

## Core Modules

### `__main__.py` - Entry Point

Main entry point when running `python -m my_addon`.

**Responsibilities:**
- Setup logging
- Load configuration
- Initialize application
- Run main server/service
- Handle graceful shutdown

**Pattern:**

```python
def main() -> int:
    """Run the add-on."""
    try:
        config = Config.from_options()
        setup_logging(config.log_level)
        asyncio.run(start_server(config))
        return 0
    except KeyboardInterrupt:
        logger.info("Shutting down...")
        return 0
    except Exception as e:
        logger.exception("Fatal error: %s", e)
        return 1

if __name__ == "__main__":
    sys.exit(main())
```

### `config.py` - Configuration Management

Handles loading and validating configuration from Home Assistant.

**Responsibilities:**
- Load options from `/data/options.json`
- Provide fallback for local development
- Validate configuration values
- Convert to typed dataclass

**Pattern:**

```python
@dataclass
class Config:
    """Add-on configuration."""
    log_level: str = "info"
    port: int = 8000

    @classmethod
    def from_options(cls, path: Path = Path("/data/options.json")) -> "Config":
        """Load from Home Assistant options."""
        if not path.exists() and Path("data/options.json").exists():
            path = Path("data/options.json")  # Local development fallback

        if not path.exists():
            return cls()  # Use defaults

        with open(path) as f:
            options = json.load(f)

        return cls(
            log_level=options.get("log_level", "info"),
            port=options.get("port", 8000),
        )
```

### `supervisor.py` - Supervisor API Client

Client for communicating with Home Assistant Supervisor.

**Responsibilities:**
- Authenticate with Supervisor
- Get add-on information
- Access Home Assistant API
- Discover services

**Pattern:**

```python
class SupervisorAPI:
    """Client for Home Assistant Supervisor."""

    def __init__(self, session: aiohttp.ClientSession | None = None):
        self.token = os.getenv("SUPERVISOR_TOKEN")
        self.base_url = "http://supervisor"
        self._session = session

    async def get_addon_info(self) -> dict:
        """Get information about this add-on."""
        return await self._request("GET", "addons/self/info")

    async def get_homeassistant_api(self) -> dict:
        """Get Home Assistant API credentials."""
        return await self._request("GET", "homeassistant/api")
```

### `server.py` - Application Logic

Main application logic (example: web server).

**Responsibilities:**
- Implement add-on functionality
- Setup routes (if web server)
- Handle ingress (if using ingress)
- Integrate with Supervisor API

**Pattern:**

```python
async def start_server(config: Config) -> None:
    """Start the application."""
    app = web.Application()
    app["supervisor"] = SupervisorAPI()
    app["config"] = config

    # Setup routes with ingress support
    ingress_path = os.getenv('INGRESS_PATH', '')
    app.router.add_get(f'{ingress_path}/', handle_index)
    app.router.add_get(f'{ingress_path}/health', handle_health)

    # Run server
    web.run_app(app, host='0.0.0.0', port=config.port)
```

## Adding New Modules

When adding new modules to the add-on:

1. **Create module file** in `src/my_addon/`
2. **Import in `__init__.py`** if it's part of public API
3. **Add tests** in `tests/unit/`
4. **Document patterns** if it establishes new patterns

## Coding Conventions

Follow conventions documented in:
- @.agents/docs/conventions/naming.md
- @.agents/docs/conventions/imports.md
- @.agents/docs/conventions/coding-style.md

### Imports Organization

```python
# Standard library
import asyncio
import json
import logging
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

# Third-party
import aiohttp
from aiohttp import web

# Local
from my_addon.config import Config
from my_addon.supervisor import SupervisorAPI
```

### Type Hints

Always use type hints:

```python
async def get_data(url: str, timeout: int = 30) -> dict[str, Any]:
    """Fetch data from URL."""
    ...

class Service:
    def __init__(self, config: Config) -> None:
        self.config: Config = config
        self.client: Optional[aiohttp.ClientSession] = None
```

### Error Handling

```python
# Be specific with exceptions
try:
    data = await fetch_data()
except aiohttp.ClientError as e:
    logger.error("Failed to fetch data: %s", e)
    raise
except json.JSONDecodeError as e:
    logger.error("Invalid JSON response: %s", e)
    return {}
```

## Home Assistant Integration

### Using Supervisor Token

```python
import os

supervisor_token = os.getenv("SUPERVISOR_TOKEN")
if supervisor_token:
    # Running in Home Assistant
    supervisor = SupervisorAPI()
else:
    # Local development
    supervisor = MockSupervisorAPI()
```

### Ingress Support

```python
import os

# Get ingress path (if running with ingress)
ingress_path = os.getenv('INGRESS_PATH', '')

# Use in routes
app.router.add_get(f'{ingress_path}/', handle_index)
app.router.add_get(f'{ingress_path}/api/status', handle_status)

# Use in templates
html = f'''
<base href="{ingress_path or '.'}/">
<a href="./api/status">Status</a>
'''
```

### Local Development

Support both HA and local environments:

```python
@classmethod
def from_options_or_env(cls) -> "Config":
    """Load from options.json or environment variables."""
    options_path = Path("/data/options.json")

    # Try HA path
    if options_path.exists():
        return cls.from_options(options_path)

    # Try local dev path
    if Path("data/options.json").exists():
        return cls.from_options(Path("data/options.json"))

    # Fall back to environment variables
    return cls.from_env()
```

## Testing

Tests are located in `@tests/`. See @tests/AGENTS.md for testing guidance.

### Running Tests

```bash
# All tests
make test

# With coverage
make test-cov

# Specific module
uv run pytest tests/unit/test_config.py
```

## Documentation

When adding features, update:

1. **Code docstrings** - Document all public functions/classes
2. **Pattern docs** - If establishing new patterns
3. **Architecture docs** - If making architectural changes
4. **User docs** - Update `addon/DOCS.md` for user-facing features

## See Also

- @.agents/docs/patterns/addon-structure.md - Add-on file organization
- @.agents/docs/patterns/options-handling.md - Configuration patterns
- @.agents/docs/patterns/supervisor-api.md - Supervisor API usage
- @.agents/docs/conventions/coding-style.md - Coding standards
- @tests/AGENTS.md - Testing guidance
