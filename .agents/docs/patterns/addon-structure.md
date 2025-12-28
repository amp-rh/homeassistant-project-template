# Home Assistant Add-on Structure

This document describes the standard file and directory structure for Home Assistant add-ons.

## Directory Layout

```
project-root/
├── addon/                      # Home Assistant add-on files
│   ├── config.yaml            # Add-on configuration (required)
│   ├── build.yaml             # Build configuration (required)
│   ├── Dockerfile             # Container definition (required)
│   ├── DOCS.md                # User documentation (required)
│   ├── CHANGELOG.md           # Version history (recommended)
│   ├── icon.png               # Add-on icon (recommended, 128x128)
│   ├── logo.png               # Add-on logo (recommended, 256x256)
│   ├── translations/          # i18n support (optional)
│   │   └── en.yaml           # English translations
│   └── rootfs/                # Container filesystem overlay
│       ├── etc/
│       │   └── services.d/   # s6-overlay services
│       │       └── addon/    # Main add-on service
│       │           ├── run   # Service run script
│       │           └── finish # Service finish script
│       └── usr/
│           └── bin/
│
├── src/                        # Python source code
│   └── my_addon/
│       ├── __init__.py
│       ├── __main__.py        # Entry point
│       ├── config.py          # Configuration handling
│       ├── supervisor.py      # Supervisor API client
│       └── server.py          # Application logic
│
├── tests/                      # Test suite
├── scripts/                    # Development scripts
├── pyproject.toml             # Python project config
└── README.md                   # Developer documentation
```

## Required Files

### addon/config.yaml

Defines add-on metadata and configuration schema.

```yaml
name: "My Python Add-on"
description: "Description of your add-on"
version: "0.1.0"
slug: "my_python_addon"
init: false
arch:
  - aarch64
  - amd64
  - armv7
startup: services
boot: auto
options:
  log_level: "info"
schema:
  log_level: "list(trace|debug|info|warning|error|fatal)?"
```

**Key Fields:**
- `name`: Display name in UI
- `description`: Short description (1-2 sentences)
- `version`: Semantic version (x.y.z)
- `slug`: URL-safe identifier (lowercase, underscores)
- `arch`: Supported architectures
- `startup`: How the add-on starts (`services`, `application`, `once`)
- `boot`: When to start (`auto`, `manual`)
- `options`: Default configuration values
- `schema`: Configuration validation schema

### addon/build.yaml

Defines build settings for each architecture.

```yaml
build_from:
  aarch64: ghcr.io/home-assistant/aarch64-base-python:3.11-alpine3.18
  amd64: ghcr.io/home-assistant/amd64-base-python:3.11-alpine3.18
  armv7: ghcr.io/home-assistant/armv7-base-python:3.11-alpine3.18
args:
  PYTHON_VERSION: "3.11"
labels:
  org.opencontainers.image.title: "My Python Add-on"
  org.opencontainers.image.description: "A Python-based add-on"
  org.opencontainers.image.source: "https://github.com/user/repo"
  org.opencontainers.image.licenses: "Apache-2.0"
```

### addon/Dockerfile

Container image definition.

```dockerfile
ARG BUILD_FROM
FROM $BUILD_FROM

# Install dependencies
RUN apk add --no-cache python3 py3-pip

# Copy and install Python project
WORKDIR /usr/src/app
COPY pyproject.toml uv.lock ./
COPY src/ ./src/
RUN python3 -m pip install --break-system-packages uv \
    && uv sync --frozen --no-dev

# Copy rootfs
COPY addon/rootfs/ /

# Make scripts executable
RUN chmod a+x /etc/services.d/addon/run

# Set data directory as workdir
WORKDIR /data

# Labels (auto-populated by Home Assistant)
ARG BUILD_ARCH
ARG BUILD_VERSION
# ... other build args and labels
```

### addon/DOCS.md

User-facing documentation shown in Home Assistant UI.

```markdown
# Home Assistant Add-on: My Python Add-on

## About

Description of what this add-on does.

## Installation

1. Add this repository to your Home Assistant
2. Install the add-on
3. Configure options
4. Start the add-on

## Configuration

### Option: `log_level`

Description of the option.

## Usage

How to use the add-on after installation.

## Support

How to get help.
```

## Service Scripts

### run script

Located at `addon/rootfs/etc/services.d/addon/run`:

```bash
#!/usr/bin/with-contenv bashio

bashio::log.info "Starting add-on..."

# Read configuration
LOG_LEVEL=$(bashio::config 'log_level')
export LOG_LEVEL

# Start the application
cd /usr/src/app || bashio::exit.nok "Directory not found"
exec uv run python -m my_addon
```

**Requirements:**
- Must use `#!/usr/bin/with-contenv bashio` shebang
- Should use `bashio::log.*` for logging
- Should use `bashio::config` for reading options
- Must use `exec` for the final command (for signal handling)
- Must be executable (`chmod +x`)

### finish script

Located at `addon/rootfs/etc/services.d/addon/finish`:

```bash
#!/usr/bin/with-contenv bashio

bashio::log.info "Add-on stopped"

if test -s /run/s6-linux-init-container-results/exitcode; then
    exit "$(cat /run/s6-linux-init-container-results/exitcode)"
else
    exit 0
fi
```

## Python Package Structure

### Entry Point (__main__.py)

```python
import sys
from my_addon.config import Config
from my_addon.server import start_server

def main() -> int:
    config = Config.from_options()
    asyncio.run(start_server(config))
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

### Configuration Module

```python
from dataclasses import dataclass
from pathlib import Path
import json

@dataclass
class Config:
    log_level: str = "info"

    @classmethod
    def from_options(cls, path: Path = Path("/data/options.json")):
        with open(path) as f:
            options = json.load(f)
        return cls(**options)
```

## Data Directories

### /data

Persistent storage for the add-on. Contains:
- `/data/options.json` - Current configuration
- `/data/...` - Your add-on's persistent files

### /share

Shared directory accessible by all add-ons:
- Read/write access
- Use for sharing files between add-ons
- Mounted from Home Assistant host

### /config

Home Assistant configuration directory (if enabled):
- Read-only by default
- Requires `homeassistant_config` permission

## File Permissions

- Service scripts: Must be executable (`755`)
- Configuration files: Should be readable (`644`)
- Data directory: Add-on has full read/write access
- Shared directory: Add-on has full read/write access

## Best Practices

1. **Keep addon/ directory minimal** - Only HA-specific files
2. **Put application code in src/** - Separate concerns
3. **Use services.d/ for startup** - Leverage s6-overlay
4. **Read config with bashio** - Use `bashio::config` in scripts
5. **Use Python for business logic** - Bash only for service scripts
6. **Document in DOCS.md** - User-facing documentation
7. **Version semantically** - Use semver (x.y.z)
8. **Support multiple architectures** - At minimum: amd64, aarch64

## Common Patterns

### Multi-Service Add-on

```
addon/rootfs/etc/services.d/
├── frontend/
│   ├── run
│   └── finish
└── backend/
    ├── run
    └── finish
```

### With Init Script

```yaml
# config.yaml
init: true
```

```bash
# addon/rootfs/etc/cont-init.d/setup.sh
#!/usr/bin/with-contenv bashio
bashio::log.info "Running initialization..."
# One-time setup tasks
```

### With Web UI (Ingress)

```yaml
# config.yaml
panel_icon: mdi:web
ingress: true
ingress_port: 8000
```

```python
# Start server on configured ingress port
app.run(host='0.0.0.0', port=8000)
```

## See Also

- `.agents/docs/patterns/options-handling.md` - Configuration patterns
- `.agents/docs/tooling/bashio.md` - Bashio usage
- `.agents/docs/architecture/containerization.md` - Container design
