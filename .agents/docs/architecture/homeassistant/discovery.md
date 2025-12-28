# Service Discovery in Home Assistant

Service discovery allows add-ons to publish and discover services, enabling communication between add-ons and with Home Assistant.

## Overview

The Supervisor provides a discovery mechanism that allows:
- Add-ons to publish services they provide
- Other add-ons to discover and use those services
- Home Assistant to automatically configure integrations

## Publishing Services

### In config.yaml

```yaml
# addon/config.yaml
discovery:
  - mqtt:
      host: "0.0.0.0"
      port: 1883
      username: "homeassistant"
      password: "!secret mqtt_password"
      protocol: "3.1.1"
      ssl: false
```

### Common Service Types

**MQTT Broker:**

```yaml
discovery:
  - mqtt:
      host: "0.0.0.0"
      port: 1883
      username: "mqtt"
      password: "!secret mqtt_password"
      protocol: "3.1.1"
      ssl: false
      addon: "Mosquitto MQTT"
```

**Database (PostgreSQL):**

```yaml
discovery:
  - postgres:
      host: "0.0.0.0"
      port: 5432
      username: "postgres"
      password: "!secret db_password"
      database: "homeassistant"
```

**Database (MySQL):**

```yaml
discovery:
  - mysql:
      host: "0.0.0.0"
      port: 3306
      username: "root"
      password: "!secret mysql_password"
      database: "homeassistant"
```

**Home Assistant Discovery:**

```yaml
discovery:
  - homeassistant:
      addon: "My Add-on"
      config:
        platform: "my_integration"
        host: "localhost"
        port: 8080
```

## Discovering Services

### Python API

```python
from my_addon.supervisor import SupervisorAPI

async with SupervisorAPI() as supervisor:
    # Discover MQTT brokers
    mqtt_services = await supervisor.discover_service("mqtt")

    for service in mqtt_services:
        print(f"MQTT Broker: {service['host']}:{service['port']}")
        print(f"Username: {service['username']}")
        print(f"SSL: {service.get('ssl', False)}")
```

### Bash (using bashio)

```bash
#!/usr/bin/with-contenv bashio

# Check if MQTT service exists
if bashio::discovery mqtt > /dev/null; then
    bashio::log.info "MQTT service found"

    # Get MQTT configuration
    MQTT_HOST=$(bashio::discovery mqtt host)
    MQTT_PORT=$(bashio::discovery mqtt port)
    MQTT_USER=$(bashio::discovery mqtt username)
    MQTT_PASS=$(bashio::discovery mqtt password)

    bashio::log.info "Connecting to MQTT: ${MQTT_HOST}:${MQTT_PORT}"
fi
```

## Using Discovered Services

### MQTT Example

```python
import asyncio_mqtt as mqtt
from my_addon.supervisor import SupervisorAPI

async def connect_mqtt():
    """Connect to discovered MQTT broker."""
    async with SupervisorAPI() as supervisor:
        services = await supervisor.discover_service("mqtt")

        if not services:
            raise RuntimeError("No MQTT broker found")

        mqtt_config = services[0]

        async with mqtt.Client(
            hostname=mqtt_config['host'],
            port=mqtt_config['port'],
            username=mqtt_config.get('username'),
            password=mqtt_config.get('password'),
        ) as client:
            # Subscribe to topic
            await client.subscribe("homeassistant/#")

            # Publish message
            await client.publish("my_addon/status", "online")

            # Listen for messages
            async with client.messages() as messages:
                async for message in messages:
                    print(f"{message.topic}: {message.payload}")
```

### Database Example

```python
import asyncpg
from my_addon.supervisor import SupervisorAPI

async def connect_database():
    """Connect to discovered PostgreSQL database."""
    async with SupervisorAPI() as supervisor:
        services = await supervisor.discover_service("postgres")

        if not services:
            raise RuntimeError("No PostgreSQL service found")

        db_config = services[0]

        conn = await asyncpg.connect(
            host=db_config['host'],
            port=db_config['port'],
            user=db_config['username'],
            password=db_config['password'],
            database=db_config.get('database', 'postgres')
        )

        # Use connection
        rows = await conn.fetch('SELECT * FROM my_table')

        await conn.close()
```

## Home Assistant Integration Discovery

### Publishing for Integration

When your add-on provides a service that Home Assistant can integrate:

```yaml
# addon/config.yaml
discovery:
  - homeassistant:
      addon: "My Service Add-on"
      service: "my_service"
      config:
        platform: "my_integration"
        host: "my_addon"
        port: 8080
        api_key: "!secret my_addon_api_key"
```

### Integration Auto-Configuration

Home Assistant will automatically discover and configure the integration:

```python
# In Home Assistant integration
async def async_setup_entry(hass, entry):
    """Set up from a config entry."""
    # Configuration provided via discovery
    config = entry.data
    host = config["host"]
    port = config["port"]
    api_key = config["api_key"]

    # Setup integration
    client = MyServiceClient(host, port, api_key)
    hass.data[DOMAIN][entry.entry_id] = client

    return True
```

## Dynamic Service Registration

### Register Service at Runtime

```python
import aiohttp

async def register_service(supervisor: SupervisorAPI, config: dict):
    """Register service with Supervisor."""
    # Note: This is typically done via config.yaml
    # Runtime registration requires Supervisor API support

    await supervisor._request(
        "POST",
        "discovery",
        json={
            "service": "my_service",
            "config": config
        }
    )
```

## Multi-Instance Services

When multiple instances of a service might exist:

```python
async def find_service(service_type: str, addon_name: str = None):
    """Find specific service instance."""
    async with SupervisorAPI() as supervisor:
        services = await supervisor.discover_service(service_type)

        if addon_name:
            # Filter by addon name
            services = [
                s for s in services
                if s.get('addon') == addon_name
            ]

        return services
```

## Best Practices

1. **Document discovery in DOCS.md** - Tell users what services your add-on provides
2. **Handle missing services gracefully** - Services might not be available
3. **Validate discovered configuration** - Ensure required fields are present
4. **Support multiple instances** - Filter by add-on name if needed
5. **Use discovery for loose coupling** - Don't hardcode service locations
6. **Provide fallback configuration** - Allow manual configuration if discovery fails
7. **Test without discovered services** - Ensure add-on works standalone

## Example: Using MQTT with Fallback

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class MQTTConfig:
    host: str
    port: int
    username: Optional[str] = None
    password: Optional[str] = None
    ssl: bool = False

async def get_mqtt_config(
    supervisor: SupervisorAPI,
    fallback_config: Optional[MQTTConfig] = None
) -> MQTTConfig:
    """Get MQTT configuration from discovery or fallback."""
    try:
        services = await supervisor.discover_service("mqtt")
        if services:
            mqtt = services[0]
            return MQTTConfig(
                host=mqtt['host'],
                port=mqtt['port'],
                username=mqtt.get('username'),
                password=mqtt.get('password'),
                ssl=mqtt.get('ssl', False)
            )
    except Exception as e:
        logger.warning("MQTT discovery failed: %s", e)

    if fallback_config:
        logger.info("Using fallback MQTT configuration")
        return fallback_config

    raise RuntimeError("No MQTT configuration available")

# Usage
mqtt_config = await get_mqtt_config(
    supervisor,
    fallback_config=MQTTConfig(
        host=config.mqtt_host,
        port=config.mqtt_port,
        username=config.mqtt_username,
        password=config.mqtt_password
    )
)
```

## Debugging Discovery

### List All Discovered Services

```python
async def list_all_services():
    """Debug: List all discovered services."""
    service_types = ["mqtt", "mysql", "postgres", "homeassistant"]

    async with SupervisorAPI() as supervisor:
        for service_type in service_types:
            try:
                services = await supervisor.discover_service(service_type)
                print(f"\n{service_type}: {len(services)} found")
                for service in services:
                    print(f"  {service}")
            except Exception as e:
                print(f"{service_type}: Error - {e}")
```

### Bash Debugging

```bash
#!/usr/bin/with-contenv bashio

# List available discovery services
for service in mqtt mysql postgres homeassistant; do
    if bashio::discovery "${service}" > /dev/null 2>&1; then
        bashio::log.info "Service ${service} is available"
        bashio::discovery "${service}"
    else
        bashio::log.debug "Service ${service} not available"
    fi
done
```

## See Also

- `.agents/docs/architecture/homeassistant/addon-communication.md` - Inter-add-on communication
- `.agents/docs/patterns/supervisor-api.md` - Supervisor API usage
- [Home Assistant Discovery](https://developers.home-assistant.io/docs/add-ons/communication#discovery)
