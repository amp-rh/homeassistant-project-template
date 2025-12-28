# Local Development Workflow

This guide describes the rapid iteration workflow for developing Home Assistant add-ons locally without requiring a full Home Assistant installation.

## Quick Start

```bash
# 1. Setup development environment
make setup

# 2. Start local development server
make dev

# 3. Access at http://localhost:8000
```

## Development Modes

### Mode 1: Pure Python (Fastest)

Develop and test Python code without any containerization.

**Setup:**

```bash
# Install dependencies
uv sync --extra dev

# Create mock data directory
mkdir -p data
echo '{"log_level": "debug"}' > data/options.json
```

**Run:**

```bash
# Direct Python execution
uv run python -m my_addon

# Or use make
make dev
```

**Benefits:**
- Fastest iteration cycle
- Full debugger support
- No container overhead
- Easy IDE integration

**Limitations:**
- No bashio functions available
- No Supervisor API
- Different environment from production

### Mode 2: Container Testing

Test add-on in containerized environment.

**Build:**

```bash
# Build add-on container
make build

# Or with specific architecture
./scripts/build-addon.sh amd64
```

**Run:**

```bash
# Run container with mock data
podman run --rm \
    -p 8000:8000 \
    -v $(pwd)/data:/data:Z \
    local/my-addon:latest
```

**Benefits:**
- Close to production environment
- Tests Dockerfile and dependencies
- Verifies container behavior

**Limitations:**
- Slower iteration cycle
- Requires rebuild for code changes
- No Supervisor API available

### Mode 3: Home Assistant Integration

Test with actual Home Assistant Supervisor.

**Setup:**

```bash
# Set add-on directory
export HA_ADDONS_DIR=/usr/share/hassio/addons/local

# Build and copy
make test-addon
```

**Benefits:**
- Full integration testing
- Real Supervisor API
- Complete feature testing

**Limitations:**
- Slowest iteration
- Requires HA installation
- More complex setup

## Recommended Workflow

### Initial Development (Mode 1)

1. **Write code** in your IDE
2. **Test locally** with `make dev`
3. **Iterate quickly** without containers

```bash
# Edit src/my_addon/server.py
vim src/my_addon/server.py

# Test immediately
make dev

# Check changes at http://localhost:8000
curl http://localhost:8000/health
```

### Feature Testing (Mode 2)

1. **Build container** when feature is complete
2. **Test in container** to verify packaging
3. **Debug container issues**

```bash
# Build
make build

# Test
podman run --rm -p 8000:8000 -v $(pwd)/data:/data:Z local/my-addon:latest

# Debug
podman run --rm -it -v $(pwd)/data:/data:Z local/my-addon:latest /bin/bash
```

### Integration Testing (Mode 3)

1. **Deploy to HA** when ready for integration
2. **Test Supervisor features**
3. **Verify in production-like environment**

```bash
# Deploy
make test-addon

# Monitor logs in Home Assistant
# Test through HA UI
```

## Debugging

### Python Debugging

```python
# Add breakpoint
import pdb; pdb.set_trace()

# Or use debugger-friendly logging
import logging
logger = logging.getLogger(__name__)
logger.debug(f"Value: {variable}")
```

**VS Code (launch.json):**

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: My Add-on",
            "type": "python",
            "request": "launch",
            "module": "my_addon",
            "cwd": "${workspaceFolder}",
            "env": {
                "LOG_LEVEL": "debug"
            }
        }
    ]
}
```

### Container Debugging

```bash
# Run with shell
podman run --rm -it local/my-addon:latest /bin/bash

# Check installed packages
podman run --rm local/my-addon:latest uv pip list

# Inspect filesystem
podman run --rm local/my-addon:latest ls -la /usr/src/app

# View logs
podman logs <container-id>
```

### Network Debugging

```bash
# Check listening ports
podman run --rm -p 8000:8000 local/my-addon:latest &
netstat -tlnp | grep 8000

# Test API endpoints
curl -v http://localhost:8000/
curl -v http://localhost:8000/health
```

## Environment Simulation

### Mock Supervisor API

For local development, use mocks:

```python
# src/my_addon/supervisor.py
import os

def get_supervisor_api():
    """Get Supervisor API (real or mock)."""
    if os.getenv('SUPERVISOR_TOKEN'):
        return SupervisorAPI()
    else:
        logger.info("Using mock Supervisor API")
        return MockSupervisorAPI()

class MockSupervisorAPI:
    """Mock Supervisor for local development."""

    async def get_addon_info(self):
        return {
            'data': {
                'name': 'My Add-on (Local)',
                'version': '0.1.0-dev',
                'state': 'started'
            }
        }

    async def get_homeassistant_api(self):
        return {
            'data': {
                'ip': 'localhost',
                'port': 8123,
                'ssl': False,
                'password': 'dev-token'
            }
        }
```

### Mock Configuration

```bash
# Create mock options.json
mkdir -p data
cat > data/options.json <<EOF
{
  "log_level": "debug",
  "port": 8000,
  "ssl": false
}
EOF
```

### Environment Variables

```bash
# Simulate HA environment
export LOG_LEVEL=debug
export PORT=8000
export SUPERVISOR_TOKEN=dev-token

# Run with environment
uv run python -m my_addon
```

## Hot Reload

### Python Hot Reload

For web servers, implement hot reload:

```python
# Enable auto-reload in development
if os.getenv('ENV') == 'development':
    web.run_app(app, host='0.0.0.0', port=8000, reload=True)
else:
    web.run_app(app, host='0.0.0.0', port=8000)
```

### Container Volume Mounts

Mount source code for live updates:

```bash
# Mount source for development
podman run --rm \
    -p 8000:8000 \
    -v $(pwd)/src:/usr/src/app/src:Z \
    -v $(pwd)/data:/data:Z \
    local/my-addon:latest
```

## Testing During Development

### Unit Tests

```bash
# Run tests
make test

# With coverage
make test-cov

# Watch mode
uv run pytest --watch
```

### Integration Tests

```bash
# Test local instance
curl http://localhost:8000/health

# Test API endpoints
http POST http://localhost:8000/api/configure setting=value
```

### Manual Testing Checklist

- [ ] Add-on starts successfully
- [ ] Configuration loads correctly
- [ ] Web UI is accessible
- [ ] API endpoints respond
- [ ] Logs are formatted correctly
- [ ] Error handling works
- [ ] Shutdown is graceful

## Common Issues

### Port Already in Use

```bash
# Find process using port
lsof -i :8000

# Kill process
kill -9 <PID>
```

### Permission Denied (SELinux)

```bash
# Add :Z flag to volume mounts
-v $(pwd)/data:/data:Z
```

### Module Not Found

```bash
# Reinstall dependencies
uv sync --extra dev

# Verify installation
uv pip list | grep my-addon
```

### Configuration Not Loading

```bash
# Check options.json exists
ls -la data/options.json

# Verify JSON syntax
python -m json.tool < data/options.json

# Check file permissions
chmod 644 data/options.json
```

## Productivity Tips

1. **Use make targets** - Faster than remembering commands
2. **Keep terminal open** - Monitor logs in real-time
3. **Use hot reload** - Avoid restart cycles
4. **Test incrementally** - Don't wait until complete
5. **Use debugger** - Better than print statements
6. **Mock external services** - Remove dependencies
7. **Automate tests** - Catch regressions early

## Development Scripts

### Custom Make Targets

Add to Makefile for your workflow:

```makefile
dev-watch: ## Run with auto-reload
	uv run watchmedo auto-restart \
		--directory=src \
		--pattern=*.py \
		--recursive \
		-- python -m my_addon

logs: ## Tail add-on logs
	tail -f data/addon.log

reset: ## Reset development environment
	rm -rf data
	./scripts/setup-local-dev.sh
```

## Next Steps

- See `.agents/docs/workflows/testing.md` for testing strategies
- See `.agents/docs/workflows/publishing.md` for publishing add-ons
- See `.agents/docs/patterns/addon-structure.md` for code organization
