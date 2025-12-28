# Bashio - Home Assistant Bash Library

Bashio is the official bash function library for Home Assistant add-ons. It provides convenient functions for logging, configuration management, and Supervisor API communication.

## Overview

Bashio is automatically available in Home Assistant base images and provides:
- Structured logging with levels (trace, debug, info, warning, error, fatal)
- Configuration reading from add-on options
- Supervisor API access
- Service management helpers
- Exit code handling

## Installation

Bashio comes pre-installed in all Home Assistant base images (`ghcr.io/home-assistant/*-base*`).

For local testing without Home Assistant, you can install it:
```bash
# Clone bashio repository
git clone https://github.com/hassio-addons/bashio.git
cd bashio
sudo make install
```

## Common Usage Patterns

### Logging

```bash
#!/usr/bin/with-contenv bashio

# Different log levels
bashio::log.trace "Detailed trace message"
bashio::log.debug "Debug information"
bashio::log.info "Informational message"
bashio::log.warning "Warning message"
bashio::log.error "Error occurred"
bashio::log.fatal "Fatal error, add-on will exit"

# Log with color
bashio::log.blue "Blue message"
bashio::log.green "Success message"
bashio::log.red "Error message"
bashio::log.yellow "Warning message"
```

### Reading Configuration

```bash
#!/usr/bin/with-contenv bashio

# Read a configuration option
LOG_LEVEL=$(bashio::config 'log_level')
PORT=$(bashio::config 'port')

# Read with default value
TIMEOUT=$(bashio::config 'timeout' '30')

# Check if option exists
if bashio::config.has_value 'custom_option'; then
    CUSTOM=$(bashio::config 'custom_option')
fi

# Read nested configuration
DATABASE_HOST=$(bashio::config 'database.host')
DATABASE_PORT=$(bashio::config 'database.port')
```

### Supervisor API

```bash
# Get Supervisor information
bashio::supervisor.info

# Get add-on information
bashio::addon.info

# Get Home Assistant information
bashio::homeassistant.info

# Check if Home Assistant is running
if bashio::homeassistant.api.ping; then
    bashio::log.info "Home Assistant is accessible"
fi
```

### Exit Handling

```bash
# Exit with error
bashio::exit.nok "Something went wrong"

# Exit successfully
bashio::exit.ok

# Check exit code in finish script
if test -s /run/s6-linux-init-container-results/exitcode; then
    exit "$(cat /run/s6-linux-init-container-results/exitcode)"
fi
```

## Example Run Script

```bash
#!/usr/bin/with-contenv bashio
# ==============================================================================
# Start the add-on service
# ==============================================================================

bashio::log.info "Starting My Add-on..."

# Read configuration
LOG_LEVEL=$(bashio::config 'log_level')
PORT=$(bashio::config 'port' '8000')

bashio::log.info "Log level: ${LOG_LEVEL}"
bashio::log.info "Port: ${PORT}"

# Export for Python application
export LOG_LEVEL
export PORT

# Change to app directory
cd /usr/src/app || bashio::exit.nok "Could not change directory"

# Start the application
bashio::log.info "Starting application..."
exec uv run python -m my_addon
```

## Example Finish Script

```bash
#!/usr/bin/with-contenv bashio
# ==============================================================================
# Handle add-on service shutdown
# ==============================================================================

bashio::log.info "Add-on stopped"

# Handle exit codes
if test -s /run/s6-linux-init-container-results/exitcode; then
    exit "$(cat /run/s6-linux-init-container-results/exitcode)"
else
    exit 0
fi
```

## Best Practices

1. **Always use bashio logging** instead of `echo` for consistent log formatting
2. **Use `bashio::config`** to read options instead of parsing JSON manually
3. **Check configuration** before using values to provide helpful error messages
4. **Use proper log levels** (info for normal operations, warning for issues, error for failures)
5. **Handle exits gracefully** with `bashio::exit.ok` or `bashio::exit.nok`

## Local Development

When developing locally without Home Assistant, bashio functions won't be available. You can:

1. **Mock bashio functions** for local testing:
```bash
if ! command -v bashio::log.info &> /dev/null; then
    bashio::log.info() { echo "[INFO] $*"; }
    bashio::config() { echo "default_value"; }
fi
```

2. **Use Python directly** instead of bash scripts for local development
3. **Test bash scripts** in a container with Home Assistant base image

## References

- [Bashio GitHub](https://github.com/hassio-addons/bashio)
- [Bashio Documentation](https://developers.home-assistant.io/docs/add-ons/bashio/)
- [Home Assistant Add-on Development](https://developers.home-assistant.io/docs/add-ons/)
