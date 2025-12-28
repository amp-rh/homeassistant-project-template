# Options Handling in Home Assistant Add-ons

This document describes how to work with configuration options in Home Assistant add-ons.

## Overview

Add-on configuration flows through multiple files:
1. `addon/config.yaml` - Define options and schema
2. `/data/options.json` - Runtime configuration (provided by Supervisor)
3. Bash scripts - Read with bashio
4. Python code - Parse and validate

## Defining Options

### addon/config.yaml

```yaml
options:
  log_level: "info"
  port: 8000
  ssl: false
  certfile: "fullchain.pem"
  keyfile: "privkey.pem"
  database:
    host: "localhost"
    port: 5432
    name: "mydb"

schema:
  log_level: "list(trace|debug|info|warning|error|fatal)?"
  port: "port"
  ssl: "bool"
  certfile: "str?"
  keyfile: "str?"
  database:
    host: "str"
    port: "port"
    name: "str"
```

## Schema Types

### Simple Types

```yaml
schema:
  string_value: "str"              # Required string
  optional_string: "str?"          # Optional string
  integer_value: "int"             # Required integer
  optional_int: "int?"             # Optional integer
  float_value: "float"             # Required float
  boolean_value: "bool"            # Required boolean
  port_number: "port"              # Port (1-65535)
```

### Lists

```yaml
schema:
  # List of specific values
  log_level: "list(trace|debug|info|warning|error)"

  # List of strings
  allowed_hosts: ["str"]

  # List of integers
  allowed_ports: ["int"]

  # Optional list
  tags: ["str"]?
```

### Nested Objects

```yaml
schema:
  database:
    host: "str"
    port: "port"
    username: "str"
    password: "password"
```

### Match Patterns

```yaml
schema:
  # Match specific pattern
  email: "match([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})"

  # URL validation
  webhook_url: "url"
```

## Reading Options in Bash

### Basic Reading

```bash
#!/usr/bin/with-contenv bashio

# Read simple values
LOG_LEVEL=$(bashio::config 'log_level')
PORT=$(bashio::config 'port')
SSL=$(bashio::config 'ssl')

# Read with default
TIMEOUT=$(bashio::config 'timeout' '30')

# Read nested values
DB_HOST=$(bashio::config 'database.host')
DB_PORT=$(bashio::config 'database.port')
DB_NAME=$(bashio::config 'database.name')
```

### Conditional Logic

```bash
# Check if option exists
if bashio::config.has_value 'ssl'; then
    SSL=$(bashio::config 'ssl')
    bashio::log.info "SSL enabled: ${SSL}"
fi

# Boolean checks
if bashio::config.true 'ssl'; then
    CERTFILE=$(bashio::config 'certfile')
    KEYFILE=$(bashio::config 'keyfile')
    bashio::log.info "Configuring SSL..."
fi

if bashio::config.false 'debug_mode'; then
    bashio::log.info "Debug mode disabled"
fi
```

### Lists and Arrays

```bash
# Check if list exists and has elements
if bashio::config.has_value 'allowed_hosts'; then
    # Iterate over list
    for host in $(bashio::config 'allowed_hosts'); do
        bashio::log.info "Allowed host: ${host}"
    done
fi
```

## Reading Options in Python

### Configuration Class

```python
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

@dataclass
class DatabaseConfig:
    """Database configuration."""
    host: str
    port: int
    name: str
    username: str = "postgres"
    password: str = ""

@dataclass
class Config:
    """Add-on configuration."""
    log_level: str = "info"
    port: int = 8000
    ssl: bool = False
    certfile: Optional[str] = None
    keyfile: Optional[str] = None
    database: Optional[DatabaseConfig] = None

    @classmethod
    def from_options(cls, path: Path = Path("/data/options.json")) -> "Config":
        """Load configuration from options.json."""
        # Fallback for local development
        if not path.exists():
            path = Path("data/options.json")
            if not path.exists():
                return cls()  # Return defaults

        with open(path) as f:
            options = json.load(f)

        # Parse database config if present
        database = None
        if "database" in options:
            database = DatabaseConfig(**options["database"])

        return cls(
            log_level=options.get("log_level", "info"),
            port=options.get("port", 8000),
            ssl=options.get("ssl", False),
            certfile=options.get("certfile"),
            keyfile=options.get("keyfile"),
            database=database,
        )
```

### Environment Variables Alternative

For local development, support environment variables:

```python
import os

@classmethod
def from_env(cls) -> "Config":
    """Load configuration from environment variables."""
    database = None
    if os.getenv("DB_HOST"):
        database = DatabaseConfig(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", "5432")),
            name=os.getenv("DB_NAME", "mydb"),
            username=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", ""),
        )

    return cls(
        log_level=os.getenv("LOG_LEVEL", "info"),
        port=int(os.getenv("PORT", "8000")),
        ssl=os.getenv("SSL", "false").lower() == "true",
        certfile=os.getenv("CERTFILE"),
        keyfile=os.getenv("KEYFILE"),
        database=database,
    )
```

### Validation

```python
from typing import Literal

LogLevel = Literal["trace", "debug", "info", "warning", "error", "fatal"]

@dataclass
class Config:
    log_level: LogLevel = "info"
    port: int = 8000

    def __post_init__(self):
        """Validate configuration after initialization."""
        # Validate port range
        if not 1 <= self.port <= 65535:
            raise ValueError(f"Invalid port: {self.port}")

        # Validate SSL configuration
        if self.ssl and (not self.certfile or not self.keyfile):
            raise ValueError("SSL enabled but certfile or keyfile missing")

        # Validate log level
        valid_levels = ["trace", "debug", "info", "warning", "error", "fatal"]
        if self.log_level not in valid_levels:
            raise ValueError(f"Invalid log level: {self.log_level}")
```

## Common Patterns

### Password Fields

```yaml
# config.yaml
options:
  password: ""

schema:
  password: "password"  # Special type for sensitive data
```

```python
# Validate password is set
if not config.password:
    raise ValueError("Password must be configured")
```

### Optional SSL

```yaml
options:
  ssl: false
  certfile: "fullchain.pem"
  keyfile: "privkey.pem"

schema:
  ssl: "bool"
  certfile: "str?"
  keyfile: "str?"
```

```python
if config.ssl:
    if not config.certfile or not config.keyfile:
        raise ValueError("SSL requires certfile and keyfile")
    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain(config.certfile, config.keyfile)
```

### Database Configuration

```yaml
options:
  database:
    host: "localhost"
    port: 5432
    name: "mydb"

schema:
  database:
    host: "str"
    port: "port"
    name: "str"
    username: "str?"
    password: "password?"
```

### List of Allowed Values

```yaml
options:
  allowed_hosts:
    - "192.168.1.0/24"
    - "10.0.0.0/8"

schema:
  allowed_hosts: ["str"]
```

```python
from ipaddress import ip_network

class Config:
    allowed_hosts: list[str] = None

    def is_host_allowed(self, ip: str) -> bool:
        """Check if IP is in allowed hosts."""
        if not self.allowed_hosts:
            return True  # Allow all if not configured

        for network in self.allowed_hosts:
            if ip_address(ip) in ip_network(network):
                return True
        return False
```

## Local Development

For development without Home Assistant:

### Mock options.json

```bash
mkdir -p data
cat > data/options.json <<EOF
{
  "log_level": "debug",
  "port": 8000,
  "ssl": false,
  "database": {
    "host": "localhost",
    "port": 5432,
    "name": "testdb"
  }
}
EOF
```

### Flexible Configuration Loading

```python
@classmethod
def load(cls) -> "Config":
    """Load configuration from options.json or environment."""
    options_path = Path("/data/options.json")

    # Try HA add-on path
    if options_path.exists():
        return cls.from_options(options_path)

    # Try local development path
    options_path = Path("data/options.json")
    if options_path.exists():
        return cls.from_options(options_path)

    # Fall back to environment variables
    return cls.from_env()
```

## Best Practices

1. **Provide sensible defaults** - Add-on should work with minimal configuration
2. **Validate early** - Check configuration at startup
3. **Use specific schema types** - `port` instead of `int` for ports
4. **Document all options** - Clear descriptions in DOCS.md
5. **Make passwords required** - Force users to set credentials
6. **Support optional features** - Use optional fields for non-essential config
7. **Validate relationships** - Check dependent options (SSL requires cert files)
8. **Use environment variables for dev** - Support local development

## See Also

- `.agents/docs/patterns/addon-structure.md` - Add-on structure
- `.agents/docs/tooling/bashio.md` - Bashio configuration functions
- [Home Assistant Add-on Configuration](https://developers.home-assistant.io/docs/add-ons/configuration)
