# Supervisor API Communication

This document describes how to communicate with the Home Assistant Supervisor API from your add-on.

## Overview

The Supervisor API allows add-ons to:
- Get information about the add-on, Home Assistant, and the system
- Access the Home Assistant API
- Communicate with other add-ons
- Manage services and configuration

## Authentication

The Supervisor automatically provides authentication via:
- **Environment Variable**: `SUPERVISOR_TOKEN`
- **Base URL**: `http://supervisor`

## Supervisor API Client

### Basic Implementation

```python
import aiohttp
import os
from typing import Any

class SupervisorAPI:
    """Client for Home Assistant Supervisor API."""

    def __init__(self, session: aiohttp.ClientSession | None = None):
        self.token = os.getenv("SUPERVISOR_TOKEN")
        self.base_url = "http://supervisor"
        self._session = session
        self._own_session = session is None

    async def __aenter__(self):
        if self._session is None:
            self._session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, *args):
        if self._own_session and self._session:
            await self._session.close()

    def _get_headers(self) -> dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    async def _request(
        self, method: str, endpoint: str, **kwargs
    ) -> dict[str, Any]:
        url = f"{self.base_url}/{endpoint}"
        headers = self._get_headers()

        async with self._session.request(
            method, url, headers=headers, **kwargs
        ) as response:
            response.raise_for_status()
            return await response.json()
```

## Common Endpoints

### Add-on Information

```python
async def get_addon_info(self) -> dict[str, Any]:
    """Get information about this add-on."""
    return await self._request("GET", "addons/self/info")

# Usage
info = await supervisor.get_addon_info()
print(f"Add-on name: {info['data']['name']}")
print(f"Version: {info['data']['version']}")
print(f"State: {info['data']['state']}")
```

### Supervisor Information

```python
async def get_supervisor_info(self) -> dict[str, Any]:
    """Get Supervisor information."""
    return await self._request("GET", "supervisor/info")

# Usage
info = await supervisor.get_supervisor_info()
print(f"Supervisor version: {info['data']['version']}")
print(f"Arch: {info['data']['arch']}")
```

### Home Assistant Information

```python
async def get_homeassistant_info(self) -> dict[str, Any]:
    """Get Home Assistant information."""
    return await self._request("GET", "core/info")

async def get_homeassistant_api(self) -> dict[str, Any]:
    """Get Home Assistant API access info."""
    return await self._request("GET", "homeassistant/api")

# Usage
api_info = await supervisor.get_homeassistant_api()
ha_url = f"http://{api_info['data']['ip']}:{api_info['data']['port']}"
ha_token = api_info['data']['password']  # Long-lived access token
```

### System Information

```python
async def get_host_info(self) -> dict[str, Any]:
    """Get host system information."""
    return await self._request("GET", "host/info")

# Usage
host = await supervisor.get_host_info()
print(f"Hostname: {host['data']['hostname']}")
print(f"OS: {host['data']['operating_system']}")
```

## Home Assistant API Access

### Getting Access Token

```python
async def get_ha_token(self) -> str:
    """Get long-lived Home Assistant access token."""
    api_info = await self.get_homeassistant_api()
    return api_info['data']['password']

async def get_ha_url(self) -> str:
    """Get Home Assistant URL."""
    api_info = await self.get_homeassistant_api()
    data = api_info['data']
    protocol = 'https' if data.get('ssl', False) else 'http'
    return f"{protocol}://{data['ip']}:{data['port']}"
```

### Calling Home Assistant API

```python
class HomeAssistantAPI:
    """Client for Home Assistant API."""

    def __init__(self, url: str, token: str, session: aiohttp.ClientSession):
        self.url = url
        self.token = token
        self.session = session

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    async def get_states(self) -> list[dict]:
        """Get all entity states."""
        async with self.session.get(
            f"{self.url}/api/states", headers=self._headers()
        ) as response:
            response.raise_for_status()
            return await response.json()

    async def get_state(self, entity_id: str) -> dict:
        """Get state of specific entity."""
        async with self.session.get(
            f"{self.url}/api/states/{entity_id}",
            headers=self._headers()
        ) as response:
            response.raise_for_status()
            return await response.json()

    async def call_service(
        self, domain: str, service: str, data: dict
    ) -> list[dict]:
        """Call a Home Assistant service."""
        async with self.session.post(
            f"{self.url}/api/services/{domain}/{service}",
            headers=self._headers(),
            json=data
        ) as response:
            response.raise_for_status()
            return await response.json()

# Usage
async with SupervisorAPI() as supervisor:
    ha_url = await supervisor.get_ha_url()
    ha_token = await supervisor.get_ha_token()

    ha_api = HomeAssistantAPI(ha_url, ha_token, supervisor._session)

    # Get all lights
    states = await ha_api.get_states()
    lights = [s for s in states if s['entity_id'].startswith('light.')]

    # Turn on a light
    await ha_api.call_service('light', 'turn_on', {
        'entity_id': 'light.bedroom'
    })
```

## Inter-Add-on Communication

### Service Discovery

```python
async def discover_service(self, service: str) -> list[dict]:
    """Discover add-ons providing a service."""
    return await self._request("GET", f"discovery/{service}")

# Usage
mqtt_addons = await supervisor.discover_service("mqtt")
for addon in mqtt_addons:
    print(f"MQTT broker: {addon['host']}:{addon['port']}")
```

### Publishing Services

Add to `config.yaml`:

```yaml
discovery:
  - mqtt:
      host: "0.0.0.0"
      port: 1883
      username: addon
      password: "!secret mqtt_password"
```

## WebSocket API

### Connecting to Home Assistant WebSocket

```python
import aiohttp

async def connect_websocket(ha_url: str, token: str):
    """Connect to Home Assistant WebSocket API."""
    ws_url = ha_url.replace('http', 'ws') + '/api/websocket'

    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(ws_url) as ws:
            # Receive auth required message
            msg = await ws.receive_json()
            assert msg['type'] == 'auth_required'

            # Send auth message
            await ws.send_json({
                'type': 'auth',
                'access_token': token
            })

            # Receive auth ok
            msg = await ws.receive_json()
            assert msg['type'] == 'auth_ok'

            # Subscribe to events
            await ws.send_json({
                'id': 1,
                'type': 'subscribe_events',
                'event_type': 'state_changed'
            })

            # Listen for events
            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    data = msg.json()
                    if data.get('type') == 'event':
                        print(f"Event: {data['event']}")
```

## Health Checks

### Ping Home Assistant

```python
async def ping_homeassistant(self) -> bool:
    """Check if Home Assistant is accessible."""
    try:
        await self._request("GET", "homeassistant/api")
        return True
    except Exception:
        return False

# Usage
if await supervisor.ping_homeassistant():
    print("Home Assistant is accessible")
else:
    print("Home Assistant is not accessible")
```

## Error Handling

### Graceful Degradation

```python
import logging

logger = logging.getLogger(__name__)

async def get_ha_info_safe(self) -> dict | None:
    """Get HA info with error handling."""
    try:
        return await self.get_homeassistant_info()
    except aiohttp.ClientError as e:
        logger.warning("Failed to get HA info: %s", e)
        return None
    except Exception as e:
        logger.error("Unexpected error getting HA info: %s", e)
        return None
```

### Retry Logic

```python
import asyncio
from typing import TypeVar, Callable

T = TypeVar('T')

async def retry(
    func: Callable[..., T],
    max_attempts: int = 3,
    delay: float = 1.0
) -> T:
    """Retry a function with exponential backoff."""
    for attempt in range(max_attempts):
        try:
            return await func()
        except Exception as e:
            if attempt == max_attempts - 1:
                raise
            wait_time = delay * (2 ** attempt)
            logger.warning(
                "Attempt %d failed: %s, retrying in %.1fs",
                attempt + 1, e, wait_time
            )
            await asyncio.sleep(wait_time)

# Usage
info = await retry(lambda: supervisor.get_homeassistant_info())
```

## Best Practices

1. **Use async/await** - Supervisor API calls are I/O-bound
2. **Reuse sessions** - Create one aiohttp.ClientSession
3. **Handle errors gracefully** - Supervisor/HA might be unavailable
4. **Cache when appropriate** - Don't repeatedly request static info
5. **Use environment check** - Detect if running in HA or locally
6. **Implement health checks** - Verify API availability
7. **Log API errors** - Help with debugging
8. **Use timeouts** - Prevent hanging on API calls

## Local Development

For local development without Supervisor:

```python
class MockSupervisorAPI:
    """Mock Supervisor API for local development."""

    async def get_addon_info(self):
        return {
            'data': {
                'name': 'My Add-on (Local)',
                'version': '0.1.0-dev',
                'state': 'started',
            }
        }

    async def get_homeassistant_api(self):
        return {
            'data': {
                'ip': 'localhost',
                'port': 8123,
                'ssl': False,
                'password': 'dev-token',
            }
        }

# Detect environment
def get_supervisor_api():
    if os.getenv('SUPERVISOR_TOKEN'):
        return SupervisorAPI()
    else:
        return MockSupervisorAPI()
```

## See Also

- `.agents/docs/architecture/homeassistant/addon-communication.md` - Inter-add-on communication
- `.agents/docs/architecture/homeassistant/authentication.md` - Authentication patterns
- [Supervisor API Documentation](https://developers.home-assistant.io/docs/api/supervisor/)
