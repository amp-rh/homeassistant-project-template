# Inter-Add-on Communication

This document describes patterns for communication between Home Assistant add-ons.

## Communication Methods

### 1. Service Discovery

Add-ons can publish and discover services through the Supervisor.

**Publishing a Service:**

```yaml
# addon/config.yaml
discovery:
  - mqtt:
      host: "0.0.0.0"
      port: 1883
      username: "addon"
      password: "!secret mqtt_password"
```

**Discovering Services:**

```python
async with SupervisorAPI() as supervisor:
    services = await supervisor.discover_service("mqtt")
    for service in services:
        mqtt_host = service['host']
        mqtt_port = service['port']
```

### 2. Shared Storage

Use the `/share` directory for file-based communication.

**Writing Data:**

```python
import json
from pathlib import Path

share_dir = Path("/share")
data_file = share_dir / "my_addon_data.json"

data = {"status": "running", "port": 8000}
with open(data_file, 'w') as f:
    json.dump(data, f)
```

**Reading Data:**

```python
import json
from pathlib import Path

share_dir = Path("/share")
data_file = share_dir / "other_addon_data.json"

if data_file.exists():
    with open(data_file) as f:
        data = json.load(f)
```

### 3. Network Communication

Add-ons on the same network can communicate directly.

**Server Add-on:**

```python
from aiohttp import web

async def handle_request(request):
    return web.json_response({"status": "ok"})

app = web.Application()
app.router.add_get('/api/status', handle_request)

# Listen on all interfaces
web.run_app(app, host='0.0.0.0', port=8080)
```

**Client Add-on:**

```python
import aiohttp

async with aiohttp.ClientSession() as session:
    # Use add-on slug as hostname
    async with session.get('http://other_addon:8080/api/status') as resp:
        data = await resp.json()
```

### 4. Home Assistant as Message Bus

Use Home Assistant events for loosely-coupled communication.

**Publishing Events:**

```python
async def publish_event(ha_api, event_type: str, data: dict):
    """Publish event to Home Assistant."""
    await ha_api.call_service('event', 'fire', {
        'event_type': event_type,
        'event_data': data
    })

# Usage
await publish_event(ha_api, 'my_addon_status_change', {
    'status': 'ready',
    'port': 8000
})
```

**Subscribing to Events:**

```python
async with session.ws_connect(ws_url) as ws:
    # Authenticate
    await authenticate(ws, token)

    # Subscribe to custom events
    await ws.send_json({
        'id': 1,
        'type': 'subscribe_events',
        'event_type': 'my_addon_status_change'
    })

    # Handle events
    async for msg in ws:
        data = msg.json()
        if data.get('type') == 'event':
            handle_event(data['event'])
```

## Network Configuration

### Exposing Services

```yaml
# addon/config.yaml
ports:
  8080/tcp: 8080  # Map internal port to host port

ports_description:
  8080/tcp: "API port"
```

### Host Network Mode

For add-ons that need host network access:

```yaml
# addon/config.yaml
host_network: true
```

**Note:** Use sparingly, as it bypasses Docker networking isolation.

## Best Practices

1. **Use service discovery** for well-known services (MQTT, databases)
2. **Use shared storage** for large data or file exchange
3. **Use network communication** for real-time APIs
4. **Use HA events** for loose coupling and notifications
5. **Document communication requirements** in DOCS.md
6. **Version your APIs** for backward compatibility
7. **Handle service unavailability** gracefully

## Example: Database Add-on

**Database Add-on (Server):**

```yaml
# config.yaml
discovery:
  - postgres:
      host: "0.0.0.0"
      port: 5432
      username: "addon"
      password: "!secret db_password"

ports:
  5432/tcp: 5432
```

**Client Add-on:**

```python
import asyncpg

async with SupervisorAPI() as supervisor:
    # Discover database
    services = await supervisor.discover_service("postgres")
    if not services:
        raise RuntimeError("No PostgreSQL service found")

    db_config = services[0]

    # Connect
    conn = await asyncpg.connect(
        host=db_config['host'],
        port=db_config['port'],
        user=db_config['username'],
        password=db_config['password']
    )
```

## See Also

- `.agents/docs/patterns/supervisor-api.md` - Supervisor API usage
- `.agents/docs/architecture/homeassistant/discovery.md` - Service discovery
